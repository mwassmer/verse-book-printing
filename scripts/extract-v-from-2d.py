#!/usr/bin/env python3
"""
Extract V geometry from the canonical 2D logo (VerseLogo2D.png).
This is a clean white-on-black image, so threshold detection is very precise.
"""

import cv2
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "cover-design", "assets")

def main():
    png_path = os.path.join(REPO_ROOT, "VerseLogo2D.png")
    img = cv2.imread(png_path)
    h, w = img.shape[:2]
    print(f"Image size: {w}×{h}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Clean white on black — threshold at 128
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Save threshold
    cv2.imwrite(os.path.join(OUTPUT_DIR, "debug-2d-threshold.png"), thresh)

    # Find outer contour
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_ext, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_ext = sorted(contours_ext, key=cv2.contourArea, reverse=True)

    v_contour = contours_ext[0]
    area = cv2.contourArea(v_contour)
    bx, by, bw, bh = cv2.boundingRect(v_contour)
    print(f"  Bounding box: x={bx}, y={by}, w={bw}, h={bh}")
    print(f"  Area: {area:.0f} px²")

    # Try multiple epsilon values
    for eps_factor in [0.01, 0.015, 0.02, 0.025, 0.03]:
        epsilon = eps_factor * cv2.arcLength(v_contour, True)
        approx = cv2.approxPolyDP(v_contour, epsilon, True)
        print(f"\n  eps={eps_factor}: {len(approx)} vertices")

        if 6 <= len(approx) <= 10:
            for i, pt in enumerate(approx):
                px, py = pt[0]
                vx = (px - bx) / bw * 100
                vy = (py - by) / bh * 100
                print(f"    [{i}] pixel=({px:4d}, {py:4d})  viewBox=({vx:5.1f}, {vy:5.1f})")

    # Use eps=0.02 for the debug drawing
    epsilon = 0.02 * cv2.arcLength(v_contour, True)
    approx = cv2.approxPolyDP(v_contour, epsilon, True)

    # Draw debug image
    debug_img = img.copy()
    cv2.drawContours(debug_img, [v_contour], -1, (0, 255, 0), 1)
    cv2.drawContours(debug_img, [approx], -1, (0, 0, 255), 2)
    for i, pt in enumerate(approx):
        px, py = pt[0]
        cv2.circle(debug_img, (px, py), 6, (0, 255, 255), -1)
        cv2.putText(debug_img, str(i), (px + 10, py + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imwrite(os.path.join(OUTPUT_DIR, "debug-2d-contours.png"), debug_img)
    print(f"\n  Saved debug images to {OUTPUT_DIR}")

    # Also print current vs measured comparison
    print("\n--- Current vs 2D Canonical ---")
    current = [
        (0, 1), (24, 1), (53, 64), (77, 15), (59, 1), (99, 1), (49, 100),
    ]
    labels = ["TL outer", "inner TL", "inner bottom", "notch apex",
              "notch left", "TR outer", "bottom"]

    # Find the best matching 7-vertex approximation
    best_approx = None
    for eps_factor in [0.015, 0.02, 0.025, 0.03]:
        epsilon = eps_factor * cv2.arcLength(v_contour, True)
        a = cv2.approxPolyDP(v_contour, epsilon, True)
        if len(a) == 7:
            best_approx = a
            print(f"  Using eps={eps_factor} for 7-vertex match")
            break

    if best_approx is None:
        # Fall back to closest
        for eps_factor in [0.015, 0.02, 0.025, 0.03]:
            epsilon = eps_factor * cv2.arcLength(v_contour, True)
            a = cv2.approxPolyDP(v_contour, epsilon, True)
            if len(a) >= 7:
                best_approx = a
                print(f"  Using eps={eps_factor} ({len(a)} vertices)")
                break

    if best_approx is not None:
        # Convert to viewBox coordinates and sort to match our vertex order
        measured = []
        for pt in best_approx:
            px, py = pt[0]
            vx = (px - bx) / bw * 100
            vy = (py - by) / bh * 100
            measured.append((round(vx, 1), round(vy, 1)))

        # Sort by a heuristic to match our ordering (TL, inner-TL, inner-bottom, etc.)
        # Just print all and let human match
        print(f"\n  Measured vertices ({len(measured)}):")
        for i, (vx, vy) in enumerate(measured):
            print(f"    [{i}] ({vx:5.1f}, {vy:5.1f})")

        print(f"\n  Current vertices:")
        for i, ((cx, cy), label) in enumerate(zip(current, labels)):
            print(f"    [{i}] ({cx:5.1f}, {cy:5.1f})  — {label}")


if __name__ == "__main__":
    main()
