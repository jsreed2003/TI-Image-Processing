"""
FastAPI Backend for Keystone Correction
Provides REST API endpoints for corner detection and keystone correction
"""

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from PIL import Image
import io
from typing import List, Tuple, Dict
from pydantic import BaseModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Keystone Correction API",
    description="API for automatic keystone correction of projector outputs",
    version="1.0.0"
)

# Configure CORS for React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app's domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class CornerResponse(BaseModel):
    originalCorners: List[List[float]]
    optimalCorners: List[List[float]]
    success: bool
    message: str
    imageWidth: int
    imageHeight: int

class HealthResponse(BaseModel):
    status: str
    message: str

# Constants
PATTERN_SIZE = (8, 8)  # Chessboard pattern: 8 columns x 8 rows
INPUT_IMAGE_WIDTH = 3829
INPUT_IMAGE_HEIGHT = 2159


def getTopLeft(corners_2d):
    """
    Determine which corner element is the top-left corner.
    Returns the index of the top-left corner.
    """
    corner_coords = [
        corners_2d[0, 0],      # Top-left element
        corners_2d[0, -1],     # Top-right element
        corners_2d[-1, -1],    # Bottom-right element
        corners_2d[-1, 0]      # Bottom-left element
    ]
    
    # Find corner with smallest x and y coordinates
    x_coords = [c[0] for c in corner_coords]
    y_coords = [c[1] for c in corner_coords]
    
    x_sorted_indices = np.argsort(x_coords)[:2]
    y_sorted_indices = np.argsort(y_coords)[:2]
    
    # Find common index
    for idx in x_sorted_indices:
        if idx in y_sorted_indices:
            return idx
    
    return 0  # Default to first corner


def refineEdgePoint(img_gray, approx_point, rect_size, max_corners=1):
    """
    Refine edge point using corner detection in a small region.
    """
    h, w = img_gray.shape
    half_size = rect_size // 2
    
    # Calculate bounds
    x, y = int(approx_point[0]), int(approx_point[1])
    x_min = max(0, x - half_size)
    x_max = min(w, x + half_size)
    y_min = max(0, y - half_size)
    y_max = min(h, y + half_size)
    
    # Extract region
    region = img_gray[y_min:y_max, x_min:x_max]
    
    # Detect corners in region
    corners = cv2.goodFeaturesToTrack(
        region,
        maxCorners=max_corners,
        qualityLevel=0.01,
        minDistance=10
    )
    
    if corners is not None and len(corners) > 0:
        # Adjust coordinates back to full image
        corner_x = corners[0][0][0] + x_min
        corner_y = corners[0][0][1] + y_min
        return np.array([corner_x, corner_y])
    
    # Return approximation if detection fails
    return approx_point


def findLineIntersection(line1, line2):
    """
    Find intersection point of two lines.
    Each line is (m, b) for y = mx + b, or x = constant for vertical lines.
    """
    if isinstance(line1, (int, float)) and isinstance(line2, (int, float)):
        # Both vertical - no intersection
        return None
    elif isinstance(line1, (int, float)):
        # line1 is vertical
        x = line1
        m2, b2 = line2
        y = m2 * x + b2
        return np.array([x, y])
    elif isinstance(line2, (int, float)):
        # line2 is vertical
        x = line2
        m1, b1 = line1
        y = m1 * x + b1
        return np.array([x, y])
    else:
        # Both non-vertical
        m1, b1 = line1
        m2, b2 = line2
        
        if abs(m1 - m2) < 1e-6:
            # Parallel lines
            return None
        
        x = (b2 - b1) / (m1 - m2)
        y = (m1 * x + b1 + m2 * x + b2) / 2  # Average for stability
        return np.array([x, y])


def detectCorners(img, pattern_size=None):
    """
    Detect the four outer corners of the projector's output.

    Args:
        img: BGR image (numpy array)
        pattern_size: (cols, rows) inner corner count. Defaults to PATTERN_SIZE constant.

    Returns:
        corners: List of 4 corner coordinates [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                 ordered as: top-left, top-right, bottom-right, bottom-left
    """
    if pattern_size is None:
        pattern_size = PATTERN_SIZE

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    
    if not ret:
        raise ValueError("Could not find chessboard pattern in image")
    
    # Refine corner positions
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    
    # Reshape to 2D array
    corners_2d = corners.reshape(pattern_size[1], pattern_size[0], 2)
    
    # Determine top-left and rotate array
    top_left_idx = getTopLeft(corners_2d)
    corners_2d = np.rot90(corners_2d, k=top_left_idx)
    
    # Calculate distances for extrapolation
    top_left = corners_2d[0, 0]
    top_right_internal = corners_2d[0, 1]
    bottom_left_internal = corners_2d[1, 0]
    
    dx = top_right_internal[0] - top_left[0]
    dy = bottom_left_internal[1] - top_left[1]
    
    # Find edge points
    edge_points = {}
    
    # Top edge
    top_left_edge = top_left - np.array([dx, 0])
    rect_size = int(abs(dx) // 2)
    edge_points['top_left'] = refineEdgePoint(gray, top_left_edge, rect_size)
    
    top_right = corners_2d[0, -1]
    top_right_edge = top_right + np.array([dx, 0])
    edge_points['top_right'] = refineEdgePoint(gray, top_right_edge, rect_size)
    
    # Right edge
    right_top = corners_2d[0, -1]
    right_top_edge = right_top - np.array([0, dy])
    rect_size = int(abs(dy) // 2)
    edge_points['right_top'] = refineEdgePoint(gray, right_top_edge, rect_size)
    
    right_bottom = corners_2d[-1, -1]
    right_bottom_edge = right_bottom + np.array([0, dy])
    edge_points['right_bottom'] = refineEdgePoint(gray, right_bottom_edge, rect_size)
    
    # Bottom edge
    bottom_right = corners_2d[-1, -1]
    bottom_right_edge = bottom_right + np.array([dx, 0])
    rect_size = int(abs(dx) // 2)
    edge_points['bottom_right'] = refineEdgePoint(gray, bottom_right_edge, rect_size)
    
    bottom_left = corners_2d[-1, 0]
    bottom_left_edge = bottom_left - np.array([dx, 0])
    edge_points['bottom_left'] = refineEdgePoint(gray, bottom_left_edge, rect_size)
    
    # Left edge
    left_bottom = corners_2d[-1, 0]
    left_bottom_edge = left_bottom + np.array([0, dy])
    rect_size = int(abs(dy) // 2)
    edge_points['left_bottom'] = refineEdgePoint(gray, left_bottom_edge, rect_size)
    
    left_top = corners_2d[0, 0]
    left_top_edge = left_top - np.array([0, dy])
    edge_points['left_top'] = refineEdgePoint(gray, left_top_edge, rect_size)
    
    # Calculate line equations
    def getLineEquation(p1, p2):
        if abs(p1[0] - p2[0]) < 1e-6:
            return p1[0]  # Vertical line
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        mid_x = (p1[0] + p2[0]) / 2
        mid_y = (p1[1] + p2[1]) / 2
        b = mid_y - m * mid_x
        return (m, b)
    
    top_line = getLineEquation(edge_points['top_left'], edge_points['top_right'])
    right_line = getLineEquation(edge_points['right_top'], edge_points['right_bottom'])
    bottom_line = getLineEquation(edge_points['bottom_left'], edge_points['bottom_right'])
    left_line = getLineEquation(edge_points['left_top'], edge_points['left_bottom'])
    
    # Find corners at intersections
    corner_top_left = findLineIntersection(left_line, top_line)
    corner_top_right = findLineIntersection(top_line, right_line)
    corner_bottom_right = findLineIntersection(right_line, bottom_line)
    corner_bottom_left = findLineIntersection(bottom_line, left_line)
    
    corners = [
        corner_top_left.tolist(),
        corner_top_right.tolist(),
        corner_bottom_right.tolist(),
        corner_bottom_left.tolist()
    ]
    
    return corners


def findBiggestRectangle(corners, aspect_ratio=16/9):
    """
    Find the largest rectangle that fits inside the quadrilateral.
    
    Args:
        corners: List of 4 corner coordinates (top-left, top-right, bottom-right, bottom-left)
        aspect_ratio: Desired aspect ratio (width/height)
    
    Returns:
        optimal_corners: List of 4 corner coordinates for the optimal rectangle
    """
    from scipy.optimize import minimize
    
    # Convert to numpy array
    corners_np = np.array(corners)
    
    # Calculate line equations (ax + by + c = 0)
    lines = []
    for i in range(4):
        p1 = corners_np[i]
        p2 = corners_np[(i + 1) % 4]
        
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = -(a * p1[0] + b * p1[1])
        
        lines.append((a, b, c))
    
    # Orient lines so interior is on negative side
    centroid = np.mean(corners_np, axis=0)
    for i in range(4):
        a, b, c = lines[i]
        if a * centroid[0] + b * centroid[1] + c > 0:
            lines[i] = (-a, -b, -c)
    
    # Constraint function
    def constraints_func(params):
        x0, y0, w = params
        h = w / aspect_ratio
        
        # Rectangle corners
        rect_corners = [
            [x0 - w/2, y0 - h/2],
            [x0 + w/2, y0 - h/2],
            [x0 + w/2, y0 + h/2],
            [x0 - w/2, y0 + h/2]
        ]
        
        constraints = []
        for corner in rect_corners:
            for a, b, c in lines:
                constraints.append(-(a * corner[0] + b * corner[1] + c))
        
        return constraints
    
    # Objective: maximize area (minimize negative area)
    def objective(params):
        w = params[2]
        h = w / aspect_ratio
        return -(w * h)
    
    # Initial guess
    x0_init = centroid[0]
    y0_init = centroid[1]
    bbox_width = np.max(corners_np[:, 0]) - np.min(corners_np[:, 0])
    w_init = bbox_width / 3
    
    # Bounds
    x_min, x_max = np.min(corners_np[:, 0]), np.max(corners_np[:, 0])
    y_min, y_max = np.min(corners_np[:, 1]), np.max(corners_np[:, 1])
    bounds = [(x_min, x_max), (y_min, y_max), (1, bbox_width)]
    
    # Optimize
    from scipy.optimize import NonlinearConstraint
    nlc = NonlinearConstraint(constraints_func, 0, np.inf)
    
    result = minimize(
        objective,
        [x0_init, y0_init, w_init],
        method='SLSQP',
        bounds=bounds,
        constraints=nlc
    )
    
    if not result.success:
        logger.warning("Optimization did not fully converge")
    
    # Extract optimal rectangle
    x0, y0, w = result.x
    h = w / aspect_ratio
    
    optimal_corners = [
        [x0 - w/2, y0 - h/2],  # Top-left
        [x0 + w/2, y0 - h/2],  # Top-right
        [x0 + w/2, y0 + h/2],  # Bottom-right
        [x0 - w/2, y0 + h/2]   # Bottom-left
    ]
    
    return optimal_corners


def calculateHomography(original_corners, optimal_corners):
    """
    Calculate homography matrix to transform input image.
    
    Args:
        original_corners: 4 corners of original projector output
        optimal_corners: 4 corners of optimal projector output
    
    Returns:
        optimal_input_corners: Corner coordinates for the input image
    """
    # Original input image corners (3829x2159 resolution, 16:9 aspect ratio)
    original_input_corners = np.array([
        [0, 0],
        [INPUT_IMAGE_WIDTH, 0],
        [INPUT_IMAGE_WIDTH, INPUT_IMAGE_HEIGHT],
        [0, INPUT_IMAGE_HEIGHT]
    ], dtype=np.float32)
    
    # Calculate homography from output to input
    H, _ = cv2.findHomography(
        np.array(original_corners, dtype=np.float32),
        original_input_corners
    )
    
    # Apply to optimal corners
    optimal_corners_np = np.array(optimal_corners, dtype=np.float32)
    optimal_input_corners = cv2.perspectiveTransform(
        optimal_corners_np.reshape(-1, 1, 2),
        H
    ).reshape(-1, 2)
    
    return optimal_input_corners.tolist()


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Keystone Correction API is running"
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "message": "All systems operational"
    }


@app.post("/api/detect_corners", response_model=CornerResponse)
async def detect_corners_endpoint(
    file: UploadFile = File(...),
    cols: int = Form(8),
    rows: int = Form(8),
    aspect_ratio: float = Form(16 / 9),
):
    """
    Detect corners and calculate keystone correction parameters.

    Args:
        file: Image file of projector output (JPEG/PNG)
        cols: Number of inner corners horizontally (default 8)
        rows: Number of inner corners vertically (default 8)
        aspect_ratio: Desired output aspect ratio as a decimal (default 1.777 = 16/9)

    Returns:
        JSON with original corners, optimal corners, and correction parameters
    """
    try:
        # Read image file
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        logger.info(f"Processing image of size: {img.shape}, pattern: ({cols}x{rows}), aspect: {aspect_ratio:.3f}")

        # Step 1: Detect corners
        logger.info("Detecting corners...")
        original_corners = detectCorners(img, pattern_size=(cols, rows))

        # Step 2: Find optimal rectangle
        logger.info("Finding optimal rectangle...")
        optimal_corners = findBiggestRectangle(original_corners, aspect_ratio=aspect_ratio)
        
        # Step 3: Calculate homography (optional, for input image transformation)
        # optimal_input_corners = calculateHomography(original_corners, optimal_corners)
        
        logger.info("Corner detection successful")
        
        return {
            "originalCorners": original_corners,
            "optimalCorners": optimal_corners,
            "success": True,
            "message": "Corner detection successful",
            "imageWidth": img.shape[1],
            "imageHeight": img.shape[0]
        }
        
    except ValueError as e:
        logger.error(f"Corner detection failed: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail=f"Corner detection failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.post("/api/process_image")
async def process_image_endpoint(file: UploadFile = File(...)):
    """
    Full processing pipeline with more detailed response.
    Alternative endpoint with additional metadata.
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Detect corners
        original_corners = detectCorners(img)
        
        # Find optimal rectangle
        optimal_corners = findBiggestRectangle(original_corners)
        
        # Calculate input image corners
        optimal_input_corners = calculateHomography(original_corners, optimal_corners)
        
        return JSONResponse({
            "success": True,
            "data": {
                "originalCorners": original_corners,
                "optimalCorners": optimal_corners,
                "optimalInputCorners": optimal_input_corners,
                "imageWidth": img.shape[1],
                "imageHeight": img.shape[0],
                "inputImageWidth": INPUT_IMAGE_WIDTH,
                "inputImageHeight": INPUT_IMAGE_HEIGHT
            },
            "message": "Processing complete"
        })
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
