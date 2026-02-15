#!/usr/bin/env python3
"""
extract-v-geometry.py

Uses OpenCV to detect the V shape in verselanguageimage.jpeg
and extract the polygon vertices. Outputs coordinates in both
pixel space and mapped to a 100×100 viewBox.
"""

import cv2
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "cover-design", "assets")

def main():
    jpeg_path = os.path.join(REPO_ROOT, "verselanguageimage.jpeg")
    img = cv2.imread(jpeg_path)
    h, w = img.shape[:2]
    print(f"Image size: {w}×{h}")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # The V is a bright metallic shape on a dark background.
    # Threshold to isolate the V.
    # Try multiple thresholds and pick the one that gives us a good V contour.
    _, thresh = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)

    # Save threshold image for inspection
    thresh_path = os.path.join(OUTPUT_DIR, "debug-threshold.png")
    cv2.imwrite(thresh_path, thresh)
    print(f"  Saved threshold image: {thresh_path}")

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort by area, largest first
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    print(f"  Found {len(contours)} contours")

    if not contours:
        print("  ERROR: No contours found!")
        return

    # The largest contour should be the V
    v_contour = contours[0]
    area = cv2.contourArea(v_contour)
    print(f"  Largest contour area: {area:.0f} px²")

    # Get bounding box
    x, y, bw, bh = cv2.boundingRect(v_contour)
    print(f"  Bounding box: x={x}, y={y}, w={bw}, h={bh}")
    print(f"  Bounding box (relative): x={x/w:.3f}, y={y/h:.3f}, w={bw/w:.3f}, h={bh/h:.3f}")

    # Approximate the contour with fewer points
    # The V should be approximable with 6-8 key vertices
    for eps_factor in [0.02, 0.03, 0.04, 0.05]:
        epsilon = eps_factor * cv2.arcLength(v_contour, True)
        approx = cv2.approxPolyDP(v_contour, epsilon, True)
        print(f"\n  Approximation (eps={eps_factor}): {len(approx)} vertices")

        if len(approx) <= 12:
            for i, pt in enumerate(approx):
                px, py = pt[0]
                # Map to viewBox coordinates relative to bounding box
                vx = (px - x) / bw * 100
                vy = (py - y) / bh * 100
                print(f"    [{i}] pixel=({px}, {py})  viewBox=({vx:.1f}, {vy:.1f})")

    # Use 0.03 approximation for the debug drawing
    epsilon = 0.03 * cv2.arcLength(v_contour, True)
    approx = cv2.approxPolyDP(v_contour, epsilon, True)

    # Draw the contour and approximation on the image
    debug_img = img.copy()
    cv2.drawContours(debug_img, [v_contour], -1, (0, 255, 0), 2)
    cv2.drawContours(debug_img, [approx], -1, (0, 0, 255), 3)

    # Draw vertex numbers
    for i, pt in enumerate(approx):
        px, py = pt[0]
        cv2.circle(debug_img, (px, py), 8, (0, 255, 255), -1)
        cv2.putText(debug_img, str(i), (px + 12, py + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    contour_path = os.path.join(OUTPUT_DIR, "debug-contours.png")
    cv2.imwrite(contour_path, debug_img)
    print(f"\n  Saved contour debug image: {contour_path}")

    # Also find the inner void (hole in the V)
    # Re-find contours with hierarchy to get inner contours
    contours_h, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"\n  Contours with hierarchy: {len(contours_h)}")

    if hierarchy is not None:
        for i, (cnt, hier) in enumerate(zip(contours_h, hierarchy[0])):
            a = cv2.contourArea(cnt)
            if a > 1000:  # skip tiny noise
                parent = hier[3]
                cx, cy, cw, ch = cv2.boundingRect(cnt)
                print(f"    Contour {i}: area={a:.0f}, parent={parent}, "
                      f"bbox=({cx},{cy},{cw},{ch})")

    # Try to find the notch as an inner contour
    # Look for contours that are children of the main V contour
    main_idx = 0
    for i, cnt in enumerate(contours_h):
        if cv2.contourArea(cnt) == cv2.contourArea(v_contour):
            main_idx = i
            break

    print(f"\n  Main V contour index: {main_idx}")
    if hierarchy is not None:
        for i, (cnt, hier) in enumerate(zip(contours_h, hierarchy[0])):
            if hier[3] == main_idx:  # parent is the main V
                a = cv2.contourArea(cnt)
                if a > 500:
                    eps = 0.04 * cv2.arcLength(cnt, True)
                    inner_approx = cv2.approxPolyDP(cnt, eps, True)
                    print(f"    Inner contour {i}: area={a:.0f}, "
                          f"{len(inner_approx)} approx vertices")
                    for j, pt in enumerate(inner_approx):
                        px, py = pt[0]
                        vx = (px - x) / bw * 100
                        vy = (py - y) / bh * 100
                        print(f"      [{j}] pixel=({px}, {py})  "
                              f"viewBox=({vx:.1f}, {vy:.1f})")


if __name__ == "__main__":
    main()
