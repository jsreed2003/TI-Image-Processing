"""
FastAPI Backend for Keystone Correction
Provides REST API endpoints for corner detection and keystone correction

Now supports TWO detection modes:
- mode="checkerboard"  -> chessboard-based detection (original code)
- mode="white"         -> white-screen contour-based detection (your code)
"""

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import cv2
import numpy as np
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
    version="1.1.0"
)

# Configure CORS for React Native app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app's domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Response models
# =============================================================================

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

# =============================================================================
# Constants
# =============================================================================

PATTERN_SIZE = (8, 8)  # Chessboard pattern: 8 columns x 8 rows (inner corners)
INPUT_IMAGE_WIDTH = 3829
INPUT_IMAGE_HEIGHT = 2159

# =============================================================================
# CHECKERBOARD (existing pipeline)
# =============================================================================

def getTopLeft(corners_2d: np.ndarray) -> int:
    """
    Determine which corner element is the top-left corner.
    Returns the index (0..3) among the four outer indices extracted from corners_2d.
    """
    corner_coords = [
        corners_2d[0, 0],      # Top-left element
        corners_2d[0, -1],     # Top-right element
        corners_2d[-1, -1],    # Bottom-right element
        corners_2d[-1, 0]      # Bottom-left element
    ]

    x_coords = [c[0] for c in corner_coords]
    y_coords = [c[1] for c in corner_coords]

    x_sorted_indices = np.argsort(x_coords)[:2]
    y_sorted_indices = np.argsort(y_coords)[:2]

    for idx in x_sorted_indices:
        if idx in y_sorted_indices:
            return int(idx)

    return 0


def refineEdgePoint(img_gray: np.ndarray, approx_point: np.ndarray, rect_size: int, max_corners: int = 1) -> np.ndarray:
    """
    Refine edge point using corner detection in a small region.
    """
    h, w = img_gray.shape
    half_size = rect_size // 2

    x, y = int(approx_point[0]), int(approx_point[1])
    x_min = max(0, x - half_size)
    x_max = min(w, x + half_size)
    y_min = max(0, y - half_size)
    y_max = min(h, y + half_size)

    region = img_gray[y_min:y_max, x_min:x_max]

    corners = cv2.goodFeaturesToTrack(
        region,
        maxCorners=max_corners,
        qualityLevel=0.01,
        minDistance=10
    )

    if corners is not None and len(corners) > 0:
        corner_x = corners[0][0][0] + x_min
        corner_y = corners[0][0][1] + y_min
        return np.array([corner_x, corner_y], dtype=np.float32)

    return np.asarray(approx_point, dtype=np.float32)


def findLineIntersection(line1, line2):
    """
    Find intersection point of two lines.
    Each line is (m, b) for y = mx + b, or x = constant for vertical lines.
    """
    if isinstance(line1, (int, float)) and isinstance(line2, (int, float)):
        return None
    elif isinstance(line1, (int, float)):
        x = float(line1)
        m2, b2 = line2
        y = m2 * x + b2
        return np.array([x, y], dtype=np.float32)
    elif isinstance(line2, (int, float)):
        x = float(line2)
        m1, b1 = line1
        y = m1 * x + b1
        return np.array([x, y], dtype=np.float32)
    else:
        m1, b1 = line1
        m2, b2 = line2

        if abs(m1 - m2) < 1e-6:
            return None

        x = (b2 - b1) / (m1 - m2)
        y = (m1 * x + b1 + m2 * x + b2) / 2.0  # Average for stability
        return np.array([x, y], dtype=np.float32)


def detectCorners(img: np.ndarray, pattern_size: Tuple[int, int] = None) -> List[List[float]]:
    """
    Detect the four outer corners of the projector's output using a chessboard pattern.

    Args:
        img: BGR image (numpy array)
        pattern_size: (cols, rows) inner corner count. Defaults to PATTERN_SIZE.

    Returns:
        corners: List of 4 corner coordinates [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                 ordered as: top-left, top-right, bottom-right, bottom-left
    """
    if pattern_size is None:
        pattern_size = PATTERN_SIZE

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)
    if not ret:
        raise ValueError("Could not find chessboard pattern in image")

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

    corners_2d = corners.reshape(pattern_size[1], pattern_size[0], 2)

    top_left_idx = getTopLeft(corners_2d)
    corners_2d = np.rot90(corners_2d, k=top_left_idx)

    top_left = corners_2d[0, 0]
    top_right_internal = corners_2d[0, 1]
    bottom_left_internal = corners_2d[1, 0]

    dx = top_right_internal[0] - top_left[0]
    dy = bottom_left_internal[1] - top_left[1]

    edge_points = {}

    # Top edge
    top_left_edge = top_left - np.array([dx, 0], dtype=np.float32)
    rect_size = int(abs(dx) // 2) if abs(dx) >= 2 else 3
    edge_points['top_left'] = refineEdgePoint(gray, top_left_edge, rect_size)

    top_right = corners_2d[0, -1]
    top_right_edge = top_right + np.array([dx, 0], dtype=np.float32)
    edge_points['top_right'] = refineEdgePoint(gray, top_right_edge, rect_size)

    # Right edge
    right_top = corners_2d[0, -1]
    right_top_edge = right_top - np.array([0, dy], dtype=np.float32)
    rect_size = int(abs(dy) // 2) if abs(dy) >= 2 else 3
    edge_points['right_top'] = refineEdgePoint(gray, right_top_edge, rect_size)

    right_bottom = corners_2d[-1, -1]
    right_bottom_edge = right_bottom + np.array([0, dy], dtype=np.float32)
    edge_points['right_bottom'] = refineEdgePoint(gray, right_bottom_edge, rect_size)

    # Bottom edge
    bottom_right = corners_2d[-1, -1]
    bottom_right_edge = bottom_right + np.array([dx, 0], dtype=np.float32)
    rect_size = int(abs(dx) // 2) if abs(dx) >= 2 else 3
    edge_points['bottom_right'] = refineEdgePoint(gray, bottom_right_edge, rect_size)

    bottom_left = corners_2d[-1, 0]
    bottom_left_edge = bottom_left - np.array([dx, 0], dtype=np.float32)
    edge_points['bottom_left'] = refineEdgePoint(gray, bottom_left_edge, rect_size)

    # Left edge
    left_bottom = corners_2d[-1, 0]
    left_bottom_edge = left_bottom + np.array([0, dy], dtype=np.float32)
    rect_size = int(abs(dy) // 2) if abs(dy) >= 2 else 3
    edge_points['left_bottom'] = refineEdgePoint(gray, left_bottom_edge, rect_size)

    left_top = corners_2d[0, 0]
    left_top_edge = left_top - np.array([0, dy], dtype=np.float32)
    edge_points['left_top'] = refineEdgePoint(gray, left_top_edge, rect_size)

    def getLineEquation(p1, p2):
        if abs(p1[0] - p2[0]) < 1e-6:
            return float(p1[0])  # Vertical line x = constant
        m = (p2[1] - p1[1]) / (p2[0] - p1[0])
        mid_x = (p1[0] + p2[0]) / 2.0
        mid_y = (p1[1] + p2[1]) / 2.0
        b = mid_y - m * mid_x
        return (float(m), float(b))

    top_line = getLineEquation(edge_points['top_left'], edge_points['top_right'])
    right_line = getLineEquation(edge_points['right_top'], edge_points['right_bottom'])
    bottom_line = getLineEquation(edge_points['bottom_left'], edge_points['bottom_right'])
    left_line = getLineEquation(edge_points['left_top'], edge_points['left_bottom'])

    corner_top_left = findLineIntersection(left_line, top_line)
    corner_top_right = findLineIntersection(top_line, right_line)
    corner_bottom_right = findLineIntersection(right_line, bottom_line)
    corner_bottom_left = findLineIntersection(bottom_line, left_line)

    if any(c is None for c in [corner_top_left, corner_top_right, corner_bottom_right, corner_bottom_left]):
        raise ValueError("Failed to compute projector corners from line intersections")

    return [
        corner_top_left.tolist(),
        corner_top_right.tolist(),
        corner_bottom_right.tolist(),
        corner_bottom_left.tolist()
    ]


def findBiggestRectangle(corners: List[List[float]], aspect_ratio: float = 16 / 9) -> List[List[float]]:
    """
    Find the largest axis-aligned rectangle (with given aspect ratio) that fits inside the quadrilateral.
    Requires scipy.
    """
    from scipy.optimize import minimize, NonlinearConstraint

    corners_np = np.array(corners, dtype=np.float32)

    # Lines in ax + by + c = 0 form
    lines = []
    for i in range(4):
        p1 = corners_np[i]
        p2 = corners_np[(i + 1) % 4]
        a = p2[1] - p1[1]
        b = p1[0] - p2[0]
        c = -(a * p1[0] + b * p1[1])
        lines.append((a, b, c))

    centroid = np.mean(corners_np, axis=0)
    for i in range(4):
        a, b, c = lines[i]
        if a * centroid[0] + b * centroid[1] + c > 0:
            lines[i] = (-a, -b, -c)

    def constraints_func(params):
        x0, y0, w = params
        h = w / aspect_ratio
        rect_corners = [
            [x0 - w / 2, y0 - h / 2],
            [x0 + w / 2, y0 - h / 2],
            [x0 + w / 2, y0 + h / 2],
            [x0 - w / 2, y0 + h / 2],
        ]

        constraints = []
        for corner in rect_corners:
            for a, b, c in lines:
                constraints.append(-(a * corner[0] + b * corner[1] + c))
        return constraints

    def objective(params):
        w = params[2]
        h = w / aspect_ratio
        return -(w * h)

    x0_init, y0_init = float(centroid[0]), float(centroid[1])
    bbox_width = float(np.max(corners_np[:, 0]) - np.min(corners_np[:, 0]))
    w_init = bbox_width / 3 if bbox_width > 0 else 1.0

    x_min, x_max = float(np.min(corners_np[:, 0])), float(np.max(corners_np[:, 0]))
    y_min, y_max = float(np.min(corners_np[:, 1])), float(np.max(corners_np[:, 1]))
    bounds = [(x_min, x_max), (y_min, y_max), (1.0, max(2.0, bbox_width))]

    nlc = NonlinearConstraint(constraints_func, 0, np.inf)

    result = minimize(
        objective,
        [x0_init, y0_init, w_init],
        method="SLSQP",
        bounds=bounds,
        constraints=nlc,
    )

    if not result.success:
        logger.warning(f"Optimization did not fully converge: {result.message}")

    x0, y0, w = result.x
    h = w / aspect_ratio

    return [
        [x0 - w / 2, y0 - h / 2],
        [x0 + w / 2, y0 - h / 2],
        [x0 + w / 2, y0 + h / 2],
        [x0 - w / 2, y0 + h / 2],
    ]


def calculateHomography(original_corners: List[List[float]], optimal_corners: List[List[float]]) -> List[List[float]]:
    """
    Calculate homography matrix to transform output-corner coordinates into input-image coordinates.
    """
    original_input_corners = np.array(
        [
            [0, 0],
            [INPUT_IMAGE_WIDTH, 0],
            [INPUT_IMAGE_WIDTH, INPUT_IMAGE_HEIGHT],
            [0, INPUT_IMAGE_HEIGHT],
        ],
        dtype=np.float32,
    )

    H, _ = cv2.findHomography(
        np.array(original_corners, dtype=np.float32),
        original_input_corners,
    )

    if H is None:
        raise ValueError("Failed to compute homography from original corners")

    optimal_corners_np = np.array(optimal_corners, dtype=np.float32)
    optimal_input_corners = cv2.perspectiveTransform(
        optimal_corners_np.reshape(-1, 1, 2),
        H,
    ).reshape(-1, 2)

    return optimal_input_corners.tolist()

# =============================================================================
# WHITE SCREEN (your pipeline)
# =============================================================================

def order_points(pts: np.ndarray) -> np.ndarray:
    """
    Order 4 points in the order: TL, TR, BR, BL.
    pts: (4,2) array of float32/float64
    returns: (4,2) float32 array ordered as TL, TR, BR, BL
    """
    pts = np.asarray(pts, dtype=np.float32)

    s = pts[:, 0] + pts[:, 1]          # x + y
    d = pts[:, 1] - pts[:, 0]          # y - x

    tl_idx = int(np.argmin(s))  # Smallest sum (TL)
    br_idx = int(np.argmax(s))  # largest sum (BR)

    all_idx = np.array([0, 1, 2, 3])
    remain = all_idx[(all_idx != tl_idx) & (all_idx != br_idx)]

    if d[remain[0]] < d[remain[1]]:
        tr_idx = int(remain[0])
        bl_idx = int(remain[1])
    else:
        tr_idx = int(remain[1])
        bl_idx = int(remain[0])

    ordered = np.array(
        [pts[tl_idx], pts[tr_idx], pts[br_idx], pts[bl_idx]],
        dtype=np.float32
    )
    return ordered


def detect_white_screen_corners(
    img_bgr: np.ndarray,
    adaptive_block_size: int = 75,
    adaptive_C: int = -10,
    blur_ksize: int = 51,
    diff_thresh: int = 20,
    close_ksize: int = 25,
    approx_eps_frac: float = 0.02
) -> List[List[float]]:

    if img_bgr is None or img_bgr.size == 0:
        raise ValueError("Empty/invalid image input")

    # STEP 1 — Grayscale
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # STEP 2 — Adaptive threshold (bright regions)
    if adaptive_block_size < 3:
        adaptive_block_size = 3
    if adaptive_block_size % 2 == 0:
        adaptive_block_size += 1

    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        adaptive_block_size,
        adaptive_C
    )

    # STEP 3 — Low variance mask (uniform areas)
    if blur_ksize < 3:
        blur_ksize = 3
    if blur_ksize % 2 == 0:
        blur_ksize += 1

    blur_img = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)
    diff = cv2.absdiff(gray, blur_img)

    _, diff = cv2.threshold(diff, diff_thresh, 255, cv2.THRESH_BINARY_INV)

    combined = cv2.bitwise_and(thresh, diff)

    # STEP 4 — Morph close (fill holes)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (close_ksize, close_ksize))
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)

    # STEP 5 — Find contours and choose biggest 4-point polygon
    contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_quad = None
    max_area = 0.0

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, approx_eps_frac * perimeter, True)

        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > max_area:
                max_area = area
                best_quad = approx

    if best_quad is None:
        raise ValueError("No screen detected (no 4-point contour found).")

    pts = best_quad.reshape(4, 2).astype(np.float32)
    ordered = order_points(pts)

    return ordered.tolist()


def warp_to_1920x1080(img_bgr: np.ndarray, corners_tl_tr_br_bl: List[List[float]]) -> np.ndarray:
    """
    Warp the input image into a 1920x1080 rectangle using TL,TR,BR,BL corners.
    """
    src = np.array(corners_tl_tr_br_bl, dtype=np.float32)
    dst = np.array([[0, 0], [1919, 0], [1919, 1079], [0, 1079]], dtype=np.float32)
    H = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(img_bgr, H, (1920, 1080))
    return warped


def draw_corners(img_bgr: np.ndarray, corners_tl_tr_br_bl: List[List[float]], radius: int = 20) -> np.ndarray:
    out = img_bgr.copy()
    for x, y in corners_tl_tr_br_bl:
        cv2.circle(out, (int(x), int(y)), radius, (0, 0, 255), -1)
    return out

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/", response_model=HealthResponse)
async def root():
    return {"status": "ok", "message": "Keystone Correction API is running"}


@app.get("/health", response_model=HealthResponse)
async def health():
    return {"status": "healthy", "message": "All systems operational"}


@app.post("/api/detect_corners", response_model=CornerResponse)
async def detect_corners_endpoint(
    file: UploadFile = File(...),

    # shared
    aspect_ratio: float = Form(16 / 9),

    # NEW: choose pipeline
    mode: str = Form("checkerboard"),  # "checkerboard" or "white"

    # checkerboard params
    cols: int = Form(8),
    rows: int = Form(8),

    # white-screen params
    adaptive_block_size: int = Form(75),
    adaptive_C: int = Form(-10),
    blur_ksize: int = Form(51),
    diff_thresh: int = Form(20),
    close_ksize: int = Form(25),
    approx_eps_frac: float = Form(0.02),
):
    """
    Detect corners and calculate keystone correction parameters.

    mode="checkerboard": detectCorners() using chessboard pattern
    mode="white": detect_white_screen_corners() using bright/contrast + contour
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        mode_l = mode.strip().lower()
        logger.info(f"Processing image size={img.shape}, mode={mode_l}, aspect={aspect_ratio:.3f}")

        # Step 1: Detect corners
        if mode_l == "checkerboard":
            logger.info(f"Detecting corners (checkerboard) pattern=({cols}x{rows})...")
            original_corners = detectCorners(img, pattern_size=(cols, rows))
        elif mode_l == "white":
            logger.info("Detecting corners (white screen)...")
            original_corners = detect_white_screen_corners(
                img,
                adaptive_block_size=adaptive_block_size,
                adaptive_C=adaptive_C,
                blur_ksize=blur_ksize,
                diff_thresh=diff_thresh,
                close_ksize=close_ksize,
                approx_eps_frac=approx_eps_frac,
            )
        else:
            raise HTTPException(status_code=400, detail="mode must be 'checkerboard' or 'white'")

        # Step 2: Find optimal rectangle
        logger.info("Finding optimal rectangle...")
        optimal_corners = findBiggestRectangle(original_corners, aspect_ratio=aspect_ratio)

        return {
            "originalCorners": original_corners,
            "optimalCorners": optimal_corners,
            "success": True,
            "message": f"Corner detection successful ({mode_l})",
            "imageWidth": img.shape[1],
            "imageHeight": img.shape[0],
        }

    except ValueError as e:
        logger.error(f"Corner detection failed: {str(e)}")
        raise HTTPException(status_code=422, detail=f"Corner detection failed: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/api/process_image")
async def process_image_endpoint(
    file: UploadFile = File(...),
    mode: str = Form("checkerboard"),  # allow both here too
    cols: int = Form(8),
    rows: int = Form(8),

    adaptive_block_size: int = Form(75),
    adaptive_C: int = Form(-10),
    blur_ksize: int = Form(51),
    diff_thresh: int = Form(20),
    close_ksize: int = Form(25),
    approx_eps_frac: float = Form(0.02),
):
    """
    Full processing pipeline with more detailed response.
    Includes optimalInputCorners.
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        mode_l = mode.strip().lower()

        if mode_l == "checkerboard":
            original_corners = detectCorners(img, pattern_size=(cols, rows))
        elif mode_l == "white":
            original_corners = detect_white_screen_corners(
                img,
                adaptive_block_size=adaptive_block_size,
                adaptive_C=adaptive_C,
                blur_ksize=blur_ksize,
                diff_thresh=diff_thresh,
                close_ksize=close_ksize,
                approx_eps_frac=approx_eps_frac,
            )
        else:
            raise HTTPException(status_code=400, detail="mode must be 'checkerboard' or 'white'")

        optimal_corners = findBiggestRectangle(original_corners)
        optimal_input_corners = calculateHomography(original_corners, optimal_corners)

        return JSONResponse({
            "success": True,
            "data": {
                "mode": mode_l,
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

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# OPTIONAL: Return a warped 1920x1080 PNG (useful for debugging or demo)
@app.post("/api/warp_1920x1080")
async def warp_1920x1080_endpoint(
    file: UploadFile = File(...),
    mode: str = Form("white"),

    cols: int = Form(8),
    rows: int = Form(8),

    adaptive_block_size: int = Form(75),
    adaptive_C: int = Form(-10),
    blur_ksize: int = Form(51),
    diff_thresh: int = Form(20),
    close_ksize: int = Form(25),
    approx_eps_frac: float = Form(0.02),
):
    """
    Returns a PNG image warped to 1920x1080 using detected corners.
    """
    try:
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image file")

        mode_l = mode.strip().lower()

        if mode_l == "checkerboard":
            corners = detectCorners(img, pattern_size=(cols, rows))
        elif mode_l == "white":
            corners = detect_white_screen_corners(
                img,
                adaptive_block_size=adaptive_block_size,
                adaptive_C=adaptive_C,
                blur_ksize=blur_ksize,
                diff_thresh=diff_thresh,
                close_ksize=close_ksize,
                approx_eps_frac=approx_eps_frac,
            )
        else:
            raise HTTPException(status_code=400, detail="mode must be 'checkerboard' or 'white'")

        warped = warp_to_1920x1080(img, corners)

        ok, buf = cv2.imencode(".png", warped)
        if not ok:
            raise HTTPException(status_code=500, detail="Failed to encode image")

        return Response(content=buf.tobytes(), media_type="image/png")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Warp endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
