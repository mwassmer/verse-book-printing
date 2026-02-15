#!/usr/bin/env python3
"""
generate-cover-mockups.py

Generates cover color scheme mockup SVGs showing full spread
(back + spine + front) for the Book of Verse.

Produces 4 mockups in cover-design/mockups/:
  A. Navy + Gold      (mockup-navy-gold.svg)
  B. Black + Gold     (mockup-black-gold.svg)
  C. Black + Silver   (mockup-black-silver.svg)
  D. Dark Brown + Gold (mockup-brown-gold.svg)

Run from repo root:  python scripts/generate-cover-mockups.py
"""

import os

# ---------------------------------------------------------------------------
# Geometry from generate-verse-logo.py
# ---------------------------------------------------------------------------
V_OUTLINE = [
    (0, 0),     # 1 — top-left outer
    (22, 0),    # 2 — inner top-left
    (53, 62),   # 3 — inner bottom
    (78, 14),   # 4 — right arm inner angle
    (60, 0),    # 5 — right arm inner top
    (100, 0),   # 6 — top-right outer
    (50, 100),  # 7 — outer bottom point
]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "cover-design", "mockups")

# ---------------------------------------------------------------------------
# Cover dimensions (in pixels at 72 DPI)
# Updated for 469 pages: spine = 1.33"
# ---------------------------------------------------------------------------
DPI = 72
BLEED = 0.3125  # inches
COVER_W = 7.0   # inches (each cover panel)
SPINE_W = 1.33  # inches (469 pages × 0.0025" + 0.16" boards)
HEIGHT = 10.0   # inches

# Pixel conversions
BLEED_PX = round(BLEED * DPI)        # ~22px
COVER_W_PX = round(COVER_W * DPI)    # 504px
SPINE_W_PX = round(SPINE_W * DPI)    # ~96px
HEIGHT_PX = round(HEIGHT * DPI)      # 720px

TOTAL_W_PX = 2 * BLEED_PX + 2 * COVER_W_PX + SPINE_W_PX
TOTAL_H_PX = 2 * BLEED_PX + HEIGHT_PX

# Key positions
TRIM_LEFT = BLEED_PX
TRIM_TOP = BLEED_PX
BACK_LEFT = TRIM_LEFT
BACK_RIGHT = TRIM_LEFT + COVER_W_PX
SPINE_LEFT = BACK_RIGHT
SPINE_RIGHT = SPINE_LEFT + SPINE_W_PX
FRONT_LEFT = SPINE_RIGHT
FRONT_RIGHT = FRONT_LEFT + COVER_W_PX
TRIM_BOTTOM = TRIM_TOP + HEIGHT_PX

# Front cover center
FRONT_CX = FRONT_LEFT + COVER_W_PX // 2
FRONT_CY = TRIM_TOP + HEIGHT_PX // 2

# Spine center
SPINE_CX = SPINE_LEFT + SPINE_W_PX // 2
SPINE_CY = TRIM_TOP + HEIGHT_PX // 2

# ---------------------------------------------------------------------------
# Color schemes
# ---------------------------------------------------------------------------
MOCKUPS = [
    {
        "name": "A",
        "label": "Navy + Gold",
        "filename": "mockup-navy-gold",
        "cover_color": "#1a2744",
        "cover_darker": "#121c33",
        "foil_color": "#d4af37",
        "band_color": "#0f1825",
    },
    {
        "name": "B",
        "label": "Black + Gold",
        "filename": "mockup-black-gold",
        "cover_color": "#111111",
        "cover_darker": "#080808",
        "foil_color": "#d4af37",
        "band_color": "#000000",
    },
    {
        "name": "C",
        "label": "Black + Silver",
        "filename": "mockup-black-silver",
        "cover_color": "#111111",
        "cover_darker": "#080808",
        "foil_color": "#c0c0c0",
        "band_color": "#000000",
    },
    {
        "name": "D",
        "label": "Dark Brown + Gold",
        "filename": "mockup-brown-gold",
        "cover_color": "#3d2b1f",
        "cover_darker": "#2a1d14",
        "foil_color": "#d4af37",
        "band_color": "#261a11",
    },
]


def v_path_d(offset_x=0, offset_y=0, scale=1.0):
    """Return SVG path data for the V logo, transformed."""
    parts = []
    for i, (x, y) in enumerate(V_OUTLINE):
        px = offset_x + x * scale
        py = offset_y + y * scale
        parts.append(f"{'M' if i == 0 else 'L'} {px:.1f},{py:.1f}")
    parts.append("Z")
    return " ".join(parts)


def generate_cover_mockup(scheme):
    """Generate a single cover mockup SVG."""
    cc = scheme["cover_color"]
    cd = scheme["cover_darker"]
    fc = scheme["foil_color"]
    bc = scheme["band_color"]

    # Emblem sizes
    front_emblem_size = 180  # ~2.5" at 72dpi
    spine_emblem_size = 50   # ~0.7" at 72dpi

    # Front cover emblem position (centered horizontally, upper portion)
    fe_x = FRONT_CX - front_emblem_size // 2
    fe_y = TRIM_TOP + 140

    # Spine emblem position (centered, near bottom)
    se_x = SPINE_CX - spine_emblem_size // 2
    se_y = TRIM_BOTTOM - 90

    # Raised band positions (5 evenly spaced)
    band_spacing = HEIGHT_PX // 6
    bands = [TRIM_TOP + band_spacing * (i + 1) - 3 for i in range(5)]

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {TOTAL_W_PX} {TOTAL_H_PX}"
     width="{TOTAL_W_PX}" height="{TOTAL_H_PX}">
  <!--
    Book of Verse — Cover Mockup {scheme["name"]}: {scheme["label"]}
    Full spread: Back Cover + Spine + Front Cover
    Trim: 7" + 1.33" + 7" = 15.33" × 10"
    With bleed: {TOTAL_W_PX}px × {TOTAL_H_PX}px at 72 DPI
  -->

  <!-- Bleed area background -->
  <rect x="0" y="0" width="{TOTAL_W_PX}" height="{TOTAL_H_PX}" fill="#e0e0e0"/>

  <!-- Full trim area -->
  <rect x="{TRIM_LEFT}" y="{TRIM_TOP}" width="{FRONT_RIGHT - TRIM_LEFT}" height="{HEIGHT_PX}" fill="{cc}"/>

  <!-- Back Cover panel -->
  <rect x="{BACK_LEFT}" y="{TRIM_TOP}" width="{COVER_W_PX}" height="{HEIGHT_PX}" fill="{cc}"/>

  <!-- Spine panel (slightly darker) -->
  <rect x="{SPINE_LEFT}" y="{TRIM_TOP}" width="{SPINE_W_PX}" height="{HEIGHT_PX}" fill="{cd}"/>

  <!-- Front Cover panel -->
  <rect x="{FRONT_LEFT}" y="{TRIM_TOP}" width="{COVER_W_PX}" height="{HEIGHT_PX}" fill="{cc}"/>

  <!-- ====== FRONT COVER ELEMENTS ====== -->

  <!-- V emblem on front cover (foil color) -->
  <path d="{v_path_d(fe_x, fe_y, front_emblem_size / 100)}" fill="{fc}"/>

  <!-- Title: BOOK OF VERSE -->
  <text x="{FRONT_CX}" y="{fe_y + front_emblem_size + 60}"
        text-anchor="middle" fill="{fc}"
        font-family="Georgia, 'Times New Roman', serif"
        font-size="36" font-weight="bold" letter-spacing="3">BOOK OF VERSE</text>

  <!-- Subtitle -->
  <text x="{FRONT_CX}" y="{fe_y + front_emblem_size + 100}"
        text-anchor="middle" fill="{fc}" opacity="0.8"
        font-family="Arial, Helvetica, sans-serif"
        font-size="16" font-style="italic">The Verse Programming Language</text>

  <!-- ====== SPINE ELEMENTS ====== -->

  <!-- Raised bands on spine (5 bands) -->
  <rect x="{SPINE_LEFT}" y="{bands[0]}" width="{SPINE_W_PX}" height="6" fill="{bc}" opacity="0.6"/>
  <rect x="{SPINE_LEFT}" y="{bands[1]}" width="{SPINE_W_PX}" height="6" fill="{bc}" opacity="0.6"/>
  <rect x="{SPINE_LEFT}" y="{bands[2]}" width="{SPINE_W_PX}" height="6" fill="{bc}" opacity="0.6"/>
  <rect x="{SPINE_LEFT}" y="{bands[3]}" width="{SPINE_W_PX}" height="6" fill="{bc}" opacity="0.6"/>
  <rect x="{SPINE_LEFT}" y="{bands[4]}" width="{SPINE_W_PX}" height="6" fill="{bc}" opacity="0.6"/>

  <!-- Spine title (rotated, reading top-to-bottom) -->
  <g transform="translate({SPINE_CX}, {TRIM_TOP + 80})">
    <text transform="rotate(90)" x="0" y="0"
          text-anchor="start" fill="{fc}"
          font-family="Georgia, 'Times New Roman', serif"
          font-size="16" font-weight="bold" letter-spacing="2">BOOK OF VERSE</text>
  </g>

  <!-- V emblem on spine -->
  <path d="{v_path_d(se_x, se_y, spine_emblem_size / 100)}" fill="{fc}"/>

  <!-- ====== BACK COVER ====== -->

  <!-- Back cover placeholder text -->
  <text x="{BACK_LEFT + COVER_W_PX // 2}" y="{FRONT_CY - 20}"
        text-anchor="middle" fill="{fc}" opacity="0.3"
        font-family="Arial, Helvetica, sans-serif" font-size="14">BACK COVER</text>
  <text x="{BACK_LEFT + COVER_W_PX // 2}" y="{FRONT_CY + 5}"
        text-anchor="middle" fill="{fc}" opacity="0.2"
        font-family="Arial, Helvetica, sans-serif" font-size="11">(description or blind deboss pattern)</text>

  <!-- ====== DIMENSION LABELS ====== -->

  <!-- Top dimension lines -->
  <line x1="{BACK_LEFT}" y1="10" x2="{BACK_RIGHT}" y2="10" stroke="#888" stroke-width="0.5"/>
  <text x="{BACK_LEFT + COVER_W_PX // 2}" y="8" text-anchor="middle"
        fill="#888" font-family="Arial, sans-serif" font-size="9">7" (Back)</text>

  <line x1="{SPINE_LEFT}" y1="10" x2="{SPINE_RIGHT}" y2="10" stroke="#888" stroke-width="0.5"/>
  <text x="{SPINE_CX}" y="8" text-anchor="middle"
        fill="#888" font-family="Arial, sans-serif" font-size="9">1.33"</text>

  <line x1="{FRONT_LEFT}" y1="10" x2="{FRONT_RIGHT}" y2="10" stroke="#888" stroke-width="0.5"/>
  <text x="{FRONT_CX}" y="8" text-anchor="middle"
        fill="#888" font-family="Arial, sans-serif" font-size="9">7" (Front)</text>

  <!-- Label -->
  <text x="{TOTAL_W_PX // 2}" y="{TOTAL_H_PX - 5}" text-anchor="middle"
        fill="#888" font-family="Arial, sans-serif" font-size="10">
    Mockup {scheme["name"]}: {scheme["label"]} — Book of Verse Cover Spread</text>

</svg>'''
    return svg


def generate_slipcase_mockup(scheme):
    """Generate a slipcase mockup SVG (ultra-premium only)."""
    cc = scheme["cover_color"]
    fc = scheme["foil_color"]

    # Slipcase dimensions: slightly larger than the book
    # Width: covers book front/back + spine + clearance
    sc_w = round((COVER_W + SPINE_W + 0.25) * DPI)  # front panel + depth
    sc_h = round((HEIGHT + 0.25) * DPI)              # slightly taller
    sc_depth = round((SPINE_W + 0.25) * DPI)         # spine + clearance

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {sc_w + 80} {sc_h + 80}"
     width="{sc_w + 80}" height="{sc_h + 80}">
  <!--
    Book of Verse — Slipcase Mockup {scheme["name"]}: {scheme["label"]}
    Ultra-Premium Edition
  -->

  <!-- Background -->
  <rect x="0" y="0" width="{sc_w + 80}" height="{sc_h + 80}" fill="#f5f5f5"/>

  <!-- Slipcase body (front-facing panel) -->
  <rect x="40" y="40" width="{sc_w}" height="{sc_h}"
        fill="{cc}" stroke="#333" stroke-width="1" rx="2"/>

  <!-- Slipcase spine edge (visible depth) -->
  <rect x="{40 + sc_w}" y="40" width="{sc_depth // 3}" height="{sc_h}"
        fill="{cc}" stroke="#333" stroke-width="1" opacity="0.7"/>

  <!-- Foil title on slipcase spine -->
  <g transform="translate({40 + sc_w + sc_depth // 6}, {40 + sc_h // 4})">
    <text transform="rotate(90)" x="0" y="0"
          text-anchor="start" fill="{fc}"
          font-family="Georgia, 'Times New Roman', serif"
          font-size="14" font-weight="bold" letter-spacing="1">BOOK OF VERSE</text>
  </g>

  <!-- Opening indicator -->
  <rect x="40" y="40" width="3" height="{sc_h}"
        fill="#222" opacity="0.3"/>

  <!-- Label -->
  <text x="{(sc_w + 80) // 2}" y="{sc_h + 70}" text-anchor="middle"
        fill="#888" font-family="Arial, sans-serif" font-size="10">
    Slipcase — Mockup {scheme["name"]}: {scheme["label"]} (Ultra-Premium)</text>

</svg>'''
    return svg


def render_png(svg_path):
    """Render SVG to PNG using cairosvg if available, else Pillow placeholder."""
    try:
        import cairosvg
        png_path = svg_path.replace(".svg", ".png")
        cairosvg.svg2png(url=svg_path, write_to=png_path, scale=2)
        print(f"  Created PNG: {png_path}")
        return True
    except (ImportError, OSError):
        pass

    try:
        from PIL import Image, ImageDraw
        png_path = svg_path.replace(".svg", ".png")
        img = Image.new("RGB", (800, 100), "#ffffff")
        draw = ImageDraw.Draw(img)
        draw.text((20, 40),
                  f"Open {os.path.basename(svg_path)} in a browser for full render",
                  fill="#333333")
        img.save(png_path, "PNG")
        print(f"  Created placeholder PNG: {png_path}")
        return True
    except ImportError:
        print(f"  [SKIP] No PNG renderer available (install cairosvg or Pillow)")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating Book of Verse cover mockups...\n")
    print(f"  Spine width: {SPINE_W}\" (469 pages × 0.0025\" + 0.16\" boards)")
    print(f"  Output: {OUTPUT_DIR}\n")

    for scheme in MOCKUPS:
        # Cover spread mockup
        svg_content = generate_cover_mockup(scheme)
        svg_path = os.path.join(OUTPUT_DIR, f"{scheme['filename']}.svg")
        with open(svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"  [{scheme['name']}] Created: {svg_path}")
        render_png(svg_path)

        # Slipcase mockup (ultra-premium)
        sc_content = generate_slipcase_mockup(scheme)
        sc_path = os.path.join(OUTPUT_DIR, f"{scheme['filename']}-slipcase.svg")
        with open(sc_path, "w", encoding="utf-8") as f:
            f.write(sc_content)
        print(f"  [{scheme['name']}] Created: {sc_path} (slipcase)")
        render_png(sc_path)

        print()

    # Generate comparison HTML
    generate_comparison_html()

    print("Done! Open cover-design/mockups/compare-mockups.html in a browser.")


def generate_comparison_html():
    """Generate an HTML page showing all mockups side by side."""
    cards = ""
    for s in MOCKUPS:
        cards += f'''
    <div class="card">
      <img src="{s['filename']}.svg" alt="Mockup {s['name']}">
      <h3>Mockup {s['name']}: {s['label']}</h3>
      <div class="swatches">
        <span class="swatch" style="background:{s['cover_color']}"></span> Cover
        <span class="swatch" style="background:{s['foil_color']}"></span> Foil
      </div>
    </div>'''

    slipcase_cards = ""
    for s in MOCKUPS:
        slipcase_cards += f'''
    <div class="card">
      <img src="{s['filename']}-slipcase.svg" alt="Slipcase {s['name']}">
      <h3>Slipcase {s['name']}: {s['label']}</h3>
    </div>'''

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Book of Verse — Cover Mockup Comparison</title>
  <style>
    body {{
      background: #1a1a1a; color: #eee;
      font-family: system-ui, -apple-system, sans-serif;
      margin: 2rem; line-height: 1.5;
    }}
    h1 {{ text-align: center; margin-bottom: 0.25rem; }}
    h2 {{ text-align: center; color: #aaa; margin: 2rem 0 1rem; border-bottom: 1px solid #333; padding-bottom: 0.5rem; }}
    .subtitle {{ text-align: center; color: #888; margin-bottom: 2rem; }}
    .grid {{
      display: grid; grid-template-columns: repeat(2, 1fr);
      gap: 1.5rem; max-width: 1400px; margin: 0 auto 3rem;
    }}
    .card {{
      background: #2a2a2a; border-radius: 8px; padding: 1.25rem;
      text-align: center; border: 1px solid #333;
    }}
    .card img {{
      max-width: 100%; height: auto; display: block; margin: 0 auto;
      border: 1px solid #444;
    }}
    .card h3 {{ margin: 0.75rem 0 0.25rem; font-size: 1rem; color: #ccc; }}
    .swatches {{ font-size: 0.85rem; color: #999; }}
    .swatch {{
      display: inline-block; width: 16px; height: 16px;
      border-radius: 3px; vertical-align: middle; margin-right: 2px;
      border: 1px solid #555;
    }}
    .specs {{
      max-width: 800px; margin: 2rem auto; padding: 1.5rem;
      background: #2a2a2a; border-radius: 8px; border: 1px solid #333;
      font-size: 0.9rem;
    }}
    .specs table {{ width: 100%; border-collapse: collapse; }}
    .specs td, .specs th {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #333; }}
    .specs th {{ color: #aaa; }}
  </style>
</head>
<body>

<h1>Book of Verse — Cover Mockup Comparison</h1>
<p class="subtitle">4 color schemes for side-by-side review</p>

<h2>Full Cover Spreads</h2>
<div class="grid">{cards}
</div>

<h2>Slipcase Mockups (Ultra-Premium Edition)</h2>
<div class="grid">{slipcase_cards}
</div>

<div class="specs">
  <h3>Cover Specifications</h3>
  <table>
    <tr><th>Trim Size</th><td>7" &times; 10"</td></tr>
    <tr><th>Page Count</th><td>469 pages</td></tr>
    <tr><th>Spine Width</th><td>1.33" (469 &times; 0.0025" + 0.16" boards)</td></tr>
    <tr><th>Full Spread</th><td>15.33" &times; 10"</td></tr>
    <tr><th>Bleed</th><td>0.3125" all sides</td></tr>
    <tr><th>Front Emblem</th><td>2.5" wide V logo</td></tr>
    <tr><th>Spine Emblem</th><td>0.7" wide V logo</td></tr>
  </table>
</div>

</body>
</html>'''
    filepath = os.path.join(OUTPUT_DIR, "compare-mockups.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Created: {filepath}")


if __name__ == "__main__":
    main()
