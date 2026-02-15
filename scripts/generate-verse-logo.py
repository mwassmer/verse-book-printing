#!/usr/bin/env python3
"""
generate-verse-logo.py

Generates vector SVG files of the Verse "V" logo by defining
the geometry programmatically. Produces:
  1. verse-v-logo.svg       — detailed version with metallic effects
  2. verse-v-logo-foil.svg  — solid black on white for foil stamping
  3. compare.html           — side-by-side comparison tool
  4. debug-overlay.png      — Pillow overlay of V outline on source JPEG

Run from repo root:  python scripts/generate-verse-logo.py
"""

import os

# ---------------------------------------------------------------------------
# Geometry: all coordinates in a 100×100 viewBox
# Measured via OpenCV contour detection from verselanguageimage.jpeg.
#
# The V is a single 7-vertex concave polygon. The "notch" in the
# upper-right is not a separate cutout — it's the angular shape of
# the right arm's inner edge (vertices 4 and 5).
# ---------------------------------------------------------------------------

# V outline — single 7-vertex polygon.
# Clockwise from top-left:
#
#   1───────2               5───6
#   │        \             / ↗  │
#   │         \           / /   │
#   │          \        4╱     │
#   │           \       /      │
#   │            \     /       │
#   │             \   /        │
#   │              \ /         │
#   │               3          │
#   │              ╱ ╲         │
#   │            ╱     ╲       │
#   │          ╱         ╲     │
#   │        ╱             ╲   │
#   └──────╱       7        ╲──┘
#
V_OUTLINE = [
    (0, 0),     # 1 — top-left outer
    (22, 0),    # 2 — inner top-left (left arm inner edge, top)
    (53, 62),   # 3 — inner bottom (where inner edges meet)
    (78, 14),   # 4 — right arm inner angle (the "notch apex")
    (60, 0),    # 5 — right arm inner top (the "notch left")
    (100, 0),   # 6 — top-right outer
    (50, 100),  # 7 — outer bottom point
]

# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "cover-design", "assets")


def pts_to_subpath(points):
    """Convert list of (x, y) tuples to an SVG sub-path string."""
    parts = [f"M {points[0][0]},{points[0][1]}"]
    for x, y in points[1:]:
        parts.append(f"L {x},{y}")
    parts.append("Z")
    return " ".join(parts)


def v_path_d():
    """Return the path data for the V logo (single polygon)."""
    return pts_to_subpath(V_OUTLINE)


def generate_detailed_svg(path_d, filepath):
    """Generate the detailed SVG with metallic gradient and effects."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="400" height="400">
  <defs>
    <!-- Metallic gradient -->
    <linearGradient id="metallic" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e0e0e0"/>
      <stop offset="20%" stop-color="#a8a8a8"/>
      <stop offset="45%" stop-color="#d0d0d0"/>
      <stop offset="70%" stop-color="#888888"/>
      <stop offset="100%" stop-color="#b8b8b8"/>
    </linearGradient>

    <!-- Drop shadow -->
    <filter id="shadow" x="-15%" y="-10%" width="140%" height="140%">
      <feDropShadow dx="1.5" dy="2.5" stdDeviation="3" flood-color="#000" flood-opacity="0.55"/>
    </filter>

    <!-- Crosshatch texture pattern -->
    <pattern id="crosshatch" width="3" height="3" patternUnits="userSpaceOnUse"
             patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="3" stroke="#888" stroke-width="0.25" opacity="0.12"/>
    </pattern>

    <!-- Edge highlight gradient (top-lit) -->
    <linearGradient id="edgeHighlight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="30%" stop-color="#ffffff" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- V shape: metallic fill + shadow -->
  <path d="{path_d}" fill="url(#metallic)" filter="url(#shadow)"/>

  <!-- Crosshatch texture overlay -->
  <path d="{path_d}" fill="url(#crosshatch)"/>

  <!-- Edge highlight stroke -->
  <path d="{path_d}" fill="none" stroke="url(#edgeHighlight)" stroke-width="0.7"/>
</svg>'''
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Created: {filepath}")


def generate_foil_svg(path_d, filepath):
    """Generate the foil-ready SVG: solid black on white, no effects."""
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="400" height="400">
  <!-- Foil-ready: solid black on white, no gradients/filters/strokes -->
  <rect x="0" y="0" width="100" height="100" fill="white"/>
  <path d="{path_d}" fill="black"/>
</svg>'''
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"  Created: {filepath}")


def generate_compare_html(filepath, jpeg_relpath):
    """Generate an HTML page for side-by-side visual comparison."""
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Verse V Logo — Visual Comparison</title>
  <style>
    body {{
      background: #1a1a1a; color: #eee;
      font-family: system-ui, -apple-system, sans-serif;
      margin: 2rem; line-height: 1.5;
    }}
    h1 {{ text-align: center; margin-bottom: 0.25rem; }}
    .subtitle {{ text-align: center; color: #888; margin-bottom: 2rem; }}
    .grid {{
      display: grid; grid-template-columns: repeat(3, 1fr);
      gap: 1.5rem; max-width: 1200px; margin: 0 auto 3rem;
    }}
    .card {{
      background: #2a2a2a; border-radius: 8px; padding: 1.25rem;
      text-align: center; border: 1px solid #333;
    }}
    .card img, .card object {{
      max-width: 100%; height: 280px; object-fit: contain; display: block; margin: 0 auto;
    }}
    .card h2 {{ margin: 0.75rem 0 0; font-size: 0.95rem; color: #ccc; }}
    .overlay {{
      max-width: 500px; margin: 0 auto; text-align: center;
      background: #2a2a2a; border-radius: 8px; padding: 1.5rem; border: 1px solid #333;
    }}
    .stack {{
      position: relative; width: 400px; height: 400px; margin: 1rem auto;
      background: #111;
    }}
    .stack img {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: contain;
    }}
    .stack img.svg-overlay {{ mix-blend-mode: difference; }}
    input[type=range] {{ width: 280px; vertical-align: middle; }}
    label {{ color: #aaa; }}
    .notes {{
      max-width: 700px; margin: 2rem auto; padding: 1rem;
      background: #2a2a2a; border-radius: 8px; border: 1px solid #333;
      font-size: 0.85rem; color: #999;
    }}
    .notes code {{ background: #333; padding: 0.15em 0.4em; border-radius: 3px; color: #ddd; }}
  </style>
</head>
<body>

<h1>Verse "V" Logo — Comparison</h1>
<p class="subtitle">Compare the vectorized SVG against the source JPEG</p>

<div class="grid">
  <div class="card">
    <img src="{jpeg_relpath}" alt="Source JPEG">
    <h2>Source JPEG</h2>
  </div>
  <div class="card">
    <img src="verse-v-logo.svg" alt="Detailed SVG">
    <h2>Detailed SVG (metallic)</h2>
  </div>
  <div class="card">
    <img src="verse-v-logo-foil.svg" alt="Foil SVG">
    <h2>Foil-Ready SVG</h2>
  </div>
</div>

<div class="overlay">
  <h2 style="margin-top:0">Overlay Comparison</h2>
  <div class="stack">
    <img src="{jpeg_relpath}" alt="Source">
    <img class="svg-overlay" id="overlayImg" src="verse-v-logo.svg" alt="SVG Overlay">
  </div>
  <label>Overlay opacity:
    <input type="range" min="0" max="100" value="50"
           oninput="document.getElementById('overlayImg').style.opacity = this.value/100">
  </label>
</div>

<div class="notes">
  <strong>Refinement:</strong> Edit the <code>V_OUTLINE</code> coordinate array
  in <code>scripts/generate-verse-logo.py</code>,
  then re-run the script to regenerate. Use the overlay slider above to compare alignment.
</div>

</body>
</html>'''
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Created: {filepath}")


def generate_debug_overlay():
    """Generate a PNG overlay of the V polygon on the source JPEG for visual debugging."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("  [SKIP] Pillow not installed — run: pip install Pillow")
        return

    import cv2
    import numpy as np

    jpeg_path = os.path.join(REPO_ROOT, "verselanguageimage.jpeg")
    if not os.path.exists(jpeg_path):
        print(f"  [SKIP] Source JPEG not found: {jpeg_path}")
        return

    # Use OpenCV to find the V's bounding box for precise crop
    img_cv = cv2.imread(jpeg_path)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 55, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    bx, by, bw, bh = cv2.boundingRect(contours[0])

    # Open with Pillow for the overlay
    img = Image.open(jpeg_path).convert("RGBA")

    # Crop to the V bounding box with some padding
    pad_px = 20
    crop_left = max(0, bx - pad_px)
    crop_top = max(0, by - pad_px)
    crop_right = min(img.width, bx + bw + pad_px)
    crop_bottom = min(img.height, by + bh + pad_px)
    crop = img.crop((crop_left, crop_top, crop_right, crop_bottom))

    # Scale to 800×800
    canvas_size = 800
    crop = crop.resize((canvas_size, canvas_size), Image.LANCZOS)

    # Map viewBox (0-100) coordinates to pixel coordinates
    # viewBox maps to the bounding box, which maps to the crop
    # bounding box in crop-relative coords:
    bb_left = (bx - crop_left) / (crop_right - crop_left) * canvas_size
    bb_top = (by - crop_top) / (crop_bottom - crop_top) * canvas_size
    bb_w = bw / (crop_right - crop_left) * canvas_size
    bb_h = bh / (crop_bottom - crop_top) * canvas_size

    def vb_to_px(points):
        """Convert viewBox coordinates to pixel coordinates."""
        return [
            (bb_left + x / 100 * bb_w, bb_top + y / 100 * bb_h)
            for x, y in points
        ]

    # Draw green filled V at 30% opacity
    overlay = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    v_px = vb_to_px(V_OUTLINE)
    draw_overlay.polygon(v_px, fill=(0, 200, 0, 76))

    crop = Image.alpha_composite(crop, overlay)

    # Draw red outline of V
    draw = ImageDraw.Draw(crop)
    for i in range(len(v_px)):
        p1 = v_px[i]
        p2 = v_px[(i + 1) % len(v_px)]
        draw.line([p1, p2], fill=(255, 0, 0, 255), width=3)

    # Add vertex labels
    for i, (px, py) in enumerate(v_px):
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 0, 255))
        draw.text((px + 10, py - 10), str(i + 1), fill=(255, 255, 0, 255))

    output_path = os.path.join(OUTPUT_DIR, "debug-overlay.png")
    crop.save(output_path, "PNG")
    print(f"  Created: {output_path}")


def verify_feature_sizes():
    """Print verification of minimum feature sizes for foil stamping."""
    print("\n--- Feature Size Verification (foil stamping) ---")

    # Arm widths at the top of the V (in viewBox units)
    left_arm = V_OUTLINE[1][0] - V_OUTLINE[0][0]   # inner-TL.x - TL.x
    right_arm = V_OUTLINE[5][0] - V_OUTLINE[4][0]   # TR.x - notch-left.x
    v_width = V_OUTLINE[5][0] - V_OUTLINE[0][0]     # TR.x - TL.x

    # Right arm narrowest width is at the notch apex (vertex 4)
    # Compute outer edge x at notch apex y
    notch_y = V_OUTLINE[3][1]  # y of notch apex
    # Outer right edge: from TR to bottom
    tr_x, tr_y = V_OUTLINE[5]
    bot_x, bot_y = V_OUTLINE[6]
    t = (notch_y - tr_y) / (bot_y - tr_y)
    outer_x_at_notch = tr_x + t * (bot_x - tr_x)
    right_arm_narrow = outer_x_at_notch - V_OUTLINE[3][0]

    # Front cover: V fits in max 3" x 3"
    front_scale = 3.0 / v_width  # inches per viewBox unit
    # Spine: V fits in max 0.75" wide
    spine_scale = 0.75 / v_width

    def mm(units, scale):
        return units * scale * 25.4

    checks = [
        ("Front cover (3\" wide)", [
            ("Left arm width (top)", left_arm, front_scale),
            ("Right arm width (top)", right_arm, front_scale),
            ("Right arm (narrowest)", right_arm_narrow, front_scale),
        ]),
        ("Spine (0.75\" wide)", [
            ("Left arm width (top)", left_arm, spine_scale),
            ("Right arm width (top)", right_arm, spine_scale),
            ("Right arm (narrowest)", right_arm_narrow, spine_scale),
        ]),
    ]

    all_pass = True
    for section, items in checks:
        print(f"\n  {section}:")
        for name, units, scale in items:
            size = mm(units, scale)
            ok = size >= 1.0
            if not ok:
                all_pass = False
            print(f"    {name:25s} = {size:5.1f} mm  {'PASS' if ok else 'FAIL'} (min 1 mm)")

    print(f"\n  Overall: {'ALL PASS' if all_pass else 'SOME FEATURES BELOW MINIMUM'}")
    return all_pass


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    path_d = v_path_d()

    print("Generating Verse V logo SVGs...\n")
    generate_detailed_svg(path_d, os.path.join(OUTPUT_DIR, "verse-v-logo.svg"))
    generate_foil_svg(path_d, os.path.join(OUTPUT_DIR, "verse-v-logo-foil.svg"))

    # Relative path from compare.html (in cover-design/assets/) to the JPEG (in repo root)
    jpeg_relpath = "../../verselanguageimage.jpeg"
    generate_compare_html(os.path.join(OUTPUT_DIR, "compare.html"), jpeg_relpath)

    # Generate debug overlay for visual comparison
    generate_debug_overlay()

    verify_feature_sizes()

    print("\nDone! Open cover-design/assets/compare.html in a browser to compare.")


if __name__ == "__main__":
    main()
