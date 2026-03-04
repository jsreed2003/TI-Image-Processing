import cv2
import numpy as np
from typing import List


def order_points(pts: np.ndarray) -> np.ndarray:
    """
    Order 4 points in the order: TL, TR, BR, BL.
    pts: (4,2) array of float32/float64
    returns: (4,2) float32 array ordered as TL, TR, BR, BL
    """
    pts = np.asarray(pts, dtype=np.float32)

    # sums and diffs
    s = pts[:, 0] + pts[:, 1]          # x + y
    d = pts[:, 1] - pts[:, 0]          # y - x

    tl_idx = int(np.argmin(s)) # Smallest sum (TL)
    br_idx = int(np.argmax(s)) # largest sum (BR)

    # remaining two indices
    all_idx = np.array([0, 1, 2, 3])
    remain = all_idx[(all_idx != tl_idx) & (all_idx != br_idx)]

    # smaller (y - x) is TR, other is BL
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


"""Example:
     
           (0, 0) -----------------------   (1919, 0)
             |                                  |
             |                                  |
             |                                  |
        (0, 1079) ----------------------- (1919, 1079)

         (349, 199) ------------------------ (2545, 409)
             |                                  |
             |                                  |
             |                                  |
        (444, 1475) ------------------------- (2525, 1437)
*/
"""

# Detect the 4 corners of the white image through bright contrast:
def detect_white_screen_corners(
    img_bgr: np.ndarray,
    adaptive_block_size: int = 75,
    adaptive_C: int = -10,
    blur_ksize: int = 51,
    diff_thresh: int = 20,
    close_ksize: int = 25,
    approx_eps_frac: float = 0.02
) -> List[List[float]]:
    
    # If no 4 point screen contour is detected:
    if img_bgr is None or img_bgr.size == 0:
        raise ValueError("Empty/invalid image input")

    # STEP 1 — Grayscale (Removes color completely and keeps only brightness) (RGB -> grayscale)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

    # STEP 2 — Adaptive threshold (bright regions)
    # block size must be odd and >= 3
    # Odd to detect the nearby pixels from the center when computing the threshold
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

    # STEP 3 — Low variance mask (uniform areas) Finds the smooth/constant brightness:
    # blur kernel must be odd and >= 3
    if blur_ksize < 3:
        blur_ksize = 3
    if blur_ksize % 2 == 0:
        blur_ksize += 1

    # Smooth image with Gaussian blur so uniform regions remain similar while noise is reduced
    blur_img = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), 0) 

    # Gets the difference to find the smooth vs textured regions of the white image
    diff = cv2.absdiff(gray, blur_img) 

    # Used to keep smooth areas
    _, diff = cv2.threshold(diff, diff_thresh, 255, cv2.THRESH_BINARY_INV) # returns threshold value used and resulting thresholded image

    # Combine brightness + uniformity mask
    # white = bright + smooth regions (binary mask 255 (1 for ususal cases outside of OpenCV))
    # black = everything else (binary mask 0)
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
        approx = cv2.approxPolyDP(c, approx_eps_frac * perimeter, True) # reduces points in the ocntur

        if len(approx) == 4: # Finds corners and area inside the shape
            area = cv2.contourArea(approx)
            if area > max_area:
                max_area = area
                best_quad = approx

    if best_quad is None:
        raise ValueError("No screen detected (no 4-point contour found).")

    pts = best_quad.reshape(4, 2).astype(np.float32) # gets the points from the max white contrast area
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

# Draw the red circles on the detected corners
def draw_corners(img_bgr: np.ndarray, corners_tl_tr_br_bl: List[List[float]], radius: int = 20) -> np.ndarray:
    out = img_bgr.copy()
    for x, y in corners_tl_tr_br_bl:
        cv2.circle(out, (int(x), int(y)), radius, (0, 0, 255), -1)
    return out
