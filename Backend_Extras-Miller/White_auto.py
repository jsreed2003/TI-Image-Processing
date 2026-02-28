import cv2
import numpy as np


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

    tl_idx = np.argmin(s)
    br_idx = np.argmax(s)

    # remaining two indices
    all_idx = np.array([0, 1, 2, 3])
    remain = all_idx[(all_idx != tl_idx) & (all_idx != br_idx)]

    # smaller (y - x) is TR, other is BL
    if d[remain[0]] < d[remain[1]]:
        tr_idx = remain[0]
        bl_idx = remain[1]
    else:
        tr_idx = remain[1]
        bl_idx = remain[0]

    ordered = np.array([pts[tl_idx], pts[tr_idx], pts[br_idx], pts[bl_idx]], dtype=np.float32)
    return ordered


def main():
    img_path = "new_white_img.jpg"
    img = cv2.imread(img_path)

    if img is None:
        print(f"FAILED TO LOAD {img_path}")
        return -1

    # STEP 1 — Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # STEP 2 — Adaptive threshold (bright regions)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        75, -10
    )

    # STEP 3 — Low variance mask (uniform areas)
    blur_img = cv2.GaussianBlur(gray, (51, 51), 0)

    diff = cv2.absdiff(gray, blur_img)
    _, diff = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY_INV)

    # Combine brightness + uniformity mask
    combined = cv2.bitwise_and(thresh, diff)

    # STEP 4 — Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)

    # STEP 5 — Find contours
    contours, _hier = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0.0
    best_quad = None

    for c in contours:
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * perimeter, True)

        if len(approx) == 4:
            area = cv2.contourArea(approx)
            if area > max_area:
                max_area = area
                best_quad = approx

    if best_quad is None:
        print("No screen detected.")
        return -1

    # Convert to (4,2) float points
    pts = best_quad.reshape(4, 2).astype(np.float32)

    # ORDER POINTS: TL, TR, BR, BL
    ordered = order_points(pts)

    # Print ordered corners
    print("\n===== DETECTED CORNER COORDINATES =====")
    print(f"TL: ({ordered[0][0]}, {ordered[0][1]})")
    print(f"TR: ({ordered[1][0]}, {ordered[1][1]})")
    print(f"BR: ({ordered[2][0]}, {ordered[2][1]})")
    print(f"BL: ({ordered[3][0]}, {ordered[3][1]})")
    print("========================================\n")

    # STEP 6 — Draw detected corners
    debug = img.copy()
    for (x, y) in ordered:
        cv2.circle(debug, (int(x), int(y)), 20, (0, 0, 255), -1)

    cv2.imshow("Detected Corners", debug)
    cv2.waitKey(0)

    # STEP 7 — Warp to 1920×1080
    dst_pts = np.array([
        [0, 0], [1919, 0],
        [1919, 1079], [0, 1079]
    ], dtype=np.float32)

    H = cv2.getPerspectiveTransform(ordered, dst_pts)
    warped = cv2.warpPerspective(img, H, (1920, 1080))

    cv2.imshow("Warped 1920x1080", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
