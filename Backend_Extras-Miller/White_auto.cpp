#include <opencv2/opencv.hpp>
using namespace cv;

// ORDER 4 POINTS (TL, TR, BR, BL) with OpenCV Point2f class
std::vector<Point2f> orderPoints(const std::vector<Point2f>& pts) { 
    std::vector<Point2f> ordered(4);

    // compute sums and diffs (lambda functions)
    auto sum  = [](Point2f p){ return p.x + p.y; }; // (x + y)
    auto diff = [](Point2f p){ return p.y - p.x; }; // (y - x)

    /* 
    General logic:

    TL = smallest sum  (x + y)
    TR = smallest diff (y - x)
    BR = largest sum   (x + y)
    BL = largest diff  (y - x)

    */

// Example:
 /*.     
         (349, 199) ------------------------ (2545, 409)
             |                                  |
             |                                  |
             |                                  |
        (444, 1475) ------------------------- (2525, 1437)
*/

    // First Identify TL & BR corners:
    int tl = 0, br = 0;
    for (int i = 1; i < 4; i++) {
        if (sum(pts[i]) < sum(pts[tl])) tl = i;
        if (sum(pts[i]) > sum(pts[br])) br = i;
    }
  
    // Elminiate TL and BR and find the remaining TR and BL:
    std::vector<int> remain;
    for (int i = 0; i < 4; i++)
        if (i != tl && i != br) remain.push_back(i);

    // Distinguish TR vs BL using (y - x) --- point with smaller (y - x) is TR
    int tr = diff(pts[remain[0]]) < diff(pts[remain[1]]) ? remain[0] : remain[1];
    int bl = tr == remain[0] ? remain[1] : remain[0];

    // Return ordered points:
    ordered[0] = pts[tl]; // getPerspectiveTransform expects this order
    ordered[1] = pts[tr];
    ordered[2] = pts[br];
    ordered[3] = pts[bl];

    return ordered;
}


int main() {

    Mat img = imread("new_white_img.jpg");
    if (img.empty()) {
        std::cout << "FAILED TO LOAD new_white_img.jpg\n";
        return -1;
    }

    // STEP 1 — Grayscale (Removes color completely and keeps only brightness)
    Mat gray;
    cvtColor(img, gray, COLOR_BGR2GRAY);

    // STEP 2 — Adaptive threshold (bright regions)
    Mat thresh;
    adaptiveThreshold(gray, thresh, 255,
                      ADAPTIVE_THRESH_GAUSSIAN_C,
                      THRESH_BINARY,
                      75, -10);

    // STEP 3 — Low variance mask (uniform areas). Finds the smooth/constant brightness:
    Mat blurImg; 
    GaussianBlur(gray, blurImg, Size(51, 51), 0); // Removes noise and imperfections by replacing it with the average 51x51 neighborhood around it


    // Isolate the smooth, uniform screen region:
    Mat diff; 
    absdiff(gray, blurImg, diff); // Compute the absolute difference between the gray and blur (positive value)
    threshold(diff, diff, 20, 255, THRESH_BINARY_INV); // Within Threshold of 20 if < 20 --> White ELSE: BLACK

    // Combine brightness + uniformity mask
    Mat combined;
    bitwise_and(thresh, diff, combined);

    // STEP 4 — Morph close (Makes it a solid filled in white shape)
    Mat kernel = getStructuringElement(MORPH_RECT, Size(25, 25)); 
    morphologyEx(combined, combined, MORPH_CLOSE, kernel); // Smooth the inside of the mask by filling in the holes

    // STEP 5 — Find contours (the outline around the shape)
    std::vector<std::vector<Point>> contours;
    findContours(combined, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);

    double maxArea = 0;
    std::vector<Point> bestQuad;

    for (auto &c : contours) {
        double perimeter = arcLength(c, true);
        std::vector<Point> approx;
        approxPolyDP(c, approx, 0.02 * perimeter, true); // Keeps the corners (derivations from the straight line segments) 
        // Big geometric changes (segment to corner to segment) are kept. Small changes like edge noises are removed.

        if (approx.size() == 4) {
            double area = contourArea(approx);
            if (area > maxArea) {
                maxArea = area;
                bestQuad = approx;
            }
        }
    }

    if (bestQuad.empty()) {
        std::cout << "No screen detected.\n";
        return -1;
    }

    // Convert to float points (from Point to Point2f) for warpPerspective
    std::vector<Point2f> pts;
    for (auto &p : bestQuad)
        pts.push_back(Point2f(p.x, p.y));

    // ORDER POINTS: TL, TR, BR, BL
    std::vector<Point2f> ordered = orderPoints(pts);

    // Print ordered corners:
    std::cout << "\n===== DETECTED CORNER COORDINATES =====\n";
    std::cout << "TL: (" << ordered[0].x << ", " << ordered[0].y << ")\n";
    std::cout << "TR: (" << ordered[1].x << ", " << ordered[1].y << ")\n";
    std::cout << "BR: (" << ordered[2].x << ", " << ordered[2].y << ")\n";
    std::cout << "BL: (" << ordered[3].x << ", " << ordered[3].y << ")\n";
    std::cout << "========================================\n\n";

    // STEP 6 — Draw detected corners
    Mat debug = img.clone();
    for (auto &p : ordered)
        circle(debug, p, 20, Scalar(0, 0, 255), -1);

    imshow("Detected Corners", debug);
    waitKey(0);

    // STEP 7 — Warp to 1920×1080
    std::vector<Point2f> dstPts = {
        Point2f(0, 0), Point2f(1919, 0),
        Point2f(1919, 1079), Point2f(0, 1079)
    };

    Mat H = getPerspectiveTransform(ordered, dstPts);
    Mat warped;
    warpPerspective(img, warped, H, Size(1920, 1080));

    imshow("Warped 1920x1080", warped);
    waitKey(0);

    return 0;
}


// Compile: g++ -std=c++17 white_auto.cpp -o white_auto `pkg-config --cflags --libs opencv4`
// Run: ./white_auto

