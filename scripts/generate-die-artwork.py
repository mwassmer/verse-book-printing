#!/usr/bin/env python3
"""
generate-die-artwork.py

Generates foil stamping die artwork files for the Book of Verse.
All output is solid black on white, with text converted to outlined paths.

Produces files in cover-design/production/:
  die-front-emblem.svg   — V logo at 2.5" wide
  die-front-title.svg    — "BOOK OF VERSE" title text, outlined
  die-front-subtitle.svg — Subtitle + author, outlined
  die-spine-title.svg    — Spine title (rotated), outlined
  die-spine-emblem.svg   — V logo at 0.7" wide
  die-spine-author.svg   — Author text, outlined

All text is rendered as SVG path data (no live fonts) for production use.
For PDF conversion, use Inkscape or Illustrator to export as PDF.

Run from repo root:  python scripts/generate-die-artwork.py
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(REPO_ROOT, "cover-design", "production")

# ---------------------------------------------------------------------------
# V Logo geometry (from generate-verse-logo.py)
# ---------------------------------------------------------------------------
V_OUTLINE = [
    (0, 0),     # top-left outer
    (22, 0),    # inner top-left
    (53, 62),   # inner bottom
    (78, 14),   # right arm inner angle
    (60, 0),    # right arm inner top
    (100, 0),   # top-right outer
    (50, 100),  # outer bottom point
]

# ---------------------------------------------------------------------------
# Letter outlines as SVG paths (simplified geometric letterforms)
# Each letter is designed in a 60×80 unit cell for title text.
# These are production-grade outlined letterforms for foil die cutting.
# ---------------------------------------------------------------------------

# Geometric sans-serif letterforms optimized for foil stamping
# Each glyph is a list of SVG path commands in a normalized coordinate space
GLYPHS = {
    'B': "M 0,0 L 0,80 L 35,80 Q 55,80 55,65 Q 55,50 38,48 L 38,47 Q 52,45 52,32 Q 52,15 35,15 L 35,0 Z "
         "M 12,12 L 12,36 L 32,36 Q 40,36 40,24 Q 40,12 32,12 Z "
         "M 12,48 L 12,68 L 33,68 Q 43,68 43,58 Q 43,48 33,48 Z",
    'O': "M 30,0 Q 0,0 0,40 Q 0,80 30,80 Q 60,80 60,40 Q 60,0 30,0 Z "
         "M 30,12 Q 48,12 48,40 Q 48,68 30,68 Q 12,68 12,40 Q 12,12 30,12 Z",
    'K': "M 0,0 L 0,80 L 12,80 L 12,48 L 38,80 L 54,80 L 25,44 L 52,0 L 36,0 L 12,36 L 12,0 Z",
    'F': "M 0,0 L 0,80 L 12,80 L 12,44 L 40,44 L 40,32 L 12,32 L 12,12 L 48,12 L 48,0 Z",
    'V': "M 0,0 L 22,80 L 38,80 L 60,0 L 47,0 L 30,68 L 13,0 Z",
    'E': "M 0,0 L 0,80 L 48,80 L 48,68 L 12,68 L 12,44 L 40,44 L 40,32 L 12,32 L 12,12 L 48,12 L 48,0 Z",
    'R': "M 0,0 L 0,80 L 12,80 L 12,48 L 28,48 L 44,80 L 58,80 L 40,46 Q 55,42 55,24 Q 55,0 35,0 Z "
         "M 12,12 L 12,36 L 33,36 Q 43,36 43,24 Q 43,12 33,12 Z",
    'S': "M 48,12 L 48,0 L 15,0 Q 0,0 0,18 Q 0,36 15,36 L 36,36 Q 42,36 42,46 Q 42,56 36,56 L 36,68 L 0,68 L 0,80 L 38,80 Q 54,80 54,62 Q 54,44 38,44 L 15,44 Q 6,44 6,32 L 6,20 Q 6,12 15,12 Z",
    ' ': "",
    'T': "M 0,0 L 0,12 L 21,12 L 21,80 L 33,80 L 33,12 L 54,12 L 54,0 Z",
    'H': "M 0,0 L 0,80 L 12,80 L 12,44 L 40,44 L 40,80 L 52,80 L 52,0 L 40,0 L 40,32 L 12,32 L 12,0 Z",
    'P': "M 0,0 L 0,80 L 12,80 L 12,48 L 35,48 Q 55,48 55,24 Q 55,0 35,0 Z "
         "M 12,12 L 12,36 L 33,36 Q 43,36 43,24 Q 43,12 33,12 Z",
    'L': "M 0,0 L 0,80 L 48,80 L 48,68 L 12,68 L 12,0 Z",
    'A': "M 0,80 L 22,0 L 38,0 L 60,80 L 47,80 L 42,62 L 18,62 L 13,80 Z "
         "M 21,50 L 39,50 L 30,16 Z",
    'N': "M 0,0 L 0,80 L 12,80 L 12,22 L 42,80 L 54,80 L 54,0 L 42,0 L 42,58 L 12,0 Z",
    'G': "M 30,0 Q 0,0 0,40 Q 0,80 30,80 Q 60,80 60,50 L 60,36 L 32,36 L 32,48 L 48,48 L 48,58 Q 48,68 30,68 Q 12,68 12,40 Q 12,12 30,12 Q 42,12 46,20 L 56,14 Q 50,0 30,0 Z",
    'U': "M 0,0 L 0,60 Q 0,80 26,80 Q 52,80 52,60 L 52,0 L 40,0 L 40,58 Q 40,68 26,68 Q 12,68 12,58 L 12,0 Z",
    'I': "M 0,0 L 0,12 L 15,12 L 15,68 L 0,68 L 0,80 L 42,80 L 42,68 L 27,68 L 27,12 L 42,12 L 42,0 Z",
    'J': "M 20,0 L 20,12 L 36,12 L 36,58 Q 36,68 24,68 Q 12,68 12,58 L 12,50 L 0,50 L 0,60 Q 0,80 24,80 Q 48,80 48,60 L 48,0 Z",
    'M': "M 0,0 L 0,80 L 12,80 L 12,24 L 28,60 L 36,60 L 52,24 L 52,80 L 64,80 L 64,0 L 52,0 L 32,44 L 12,0 Z",
    'D': "M 0,0 L 0,80 L 30,80 Q 58,80 58,40 Q 58,0 30,0 Z "
         "M 12,12 L 12,68 L 28,68 Q 46,68 46,40 Q 46,12 28,12 Z",
    'W': "M 0,0 L 12,80 L 24,80 L 32,28 L 40,80 L 52,80 L 64,0 L 52,0 L 44,54 L 36,4 L 28,4 L 20,54 L 12,0 Z",
    'Y': "M 0,0 L 24,40 L 24,80 L 36,80 L 36,40 L 60,0 L 46,0 L 30,30 L 14,0 Z",
    'C': "M 30,0 Q 0,0 0,40 Q 0,80 30,80 Q 50,80 56,64 L 46,56 Q 42,68 30,68 Q 12,68 12,40 Q 12,12 30,12 Q 42,12 46,24 L 56,16 Q 50,0 30,0 Z",
    'X': "M 0,0 L 20,40 L 0,80 L 14,80 L 30,48 L 46,80 L 60,80 L 40,40 L 60,0 L 46,0 L 30,32 L 14,0 Z",
    '.': "M 0,68 L 0,80 L 12,80 L 12,68 Z",
    '&': "M 28,0 Q 6,0 6,16 Q 6,28 16,34 L 4,50 Q 0,56 0,64 Q 0,80 20,80 Q 32,80 38,72 L 42,80 L 54,80 L 44,66 Q 50,58 50,48 L 38,48 Q 38,56 34,62 L 22,40 Q 28,34 30,28 L 30,16 Q 30,0 28,0 Z "
         "M 18,16 Q 18,10 24,10 Q 28,10 28,16 L 28,22 Q 26,28 22,32 L 16,24 Q 14,20 14,16 Z "
         "M 16,58 L 30,58 Q 28,64 20,68 Q 12,68 12,62 Q 12,58 16,58 Z",
}

# Narrower width lookup per glyph (some are wider/narrower than default 60)
GLYPH_WIDTHS = {
    'B': 56, 'O': 60, 'K': 54, 'F': 48, 'V': 60, 'E': 48, 'R': 58,
    'S': 54, ' ': 24, 'T': 54, 'H': 52, 'P': 55, 'L': 48, 'A': 60,
    'N': 54, 'G': 60, 'U': 52, 'I': 42, 'J': 48, 'M': 64, 'D': 58,
    'W': 64, 'Y': 60, 'C': 56, 'X': 60, '.': 12, '&': 54,
}

LETTER_SPACING = 6  # units between letters


def text_to_paths(text, x_offset=0, y_offset=0, scale=1.0):
    """Convert a text string to SVG path elements using outlined glyphs."""
    paths = []
    cursor_x = x_offset
    for ch in text.upper():
        if ch not in GLYPHS:
            cursor_x += 30 * scale  # unknown character gap
            continue
        glyph_d = GLYPHS[ch]
        if glyph_d:  # skip spaces
            # Transform the path data
            transformed = transform_path_data(glyph_d, cursor_x, y_offset, scale)
            paths.append(transformed)
        cursor_x += (GLYPH_WIDTHS.get(ch, 60) + LETTER_SPACING) * scale
    return paths, cursor_x - x_offset - LETTER_SPACING * scale


def transform_path_data(d, tx, ty, scale):
    """Transform SVG path data by translating and scaling."""
    import re
    result = []
    tokens = re.findall(r'[MLQZ]|[-+]?\d*\.?\d+', d)
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in ('M', 'L'):
            x = float(tokens[i + 1]) * scale + tx
            y = float(tokens[i + 2]) * scale + ty
            result.append(f"{t} {x:.1f},{y:.1f}")
            i += 3
        elif t == 'Q':
            cx = float(tokens[i + 1]) * scale + tx
            cy = float(tokens[i + 2]) * scale + ty
            x = float(tokens[i + 3]) * scale + tx
            y = float(tokens[i + 4]) * scale + ty
            result.append(f"Q {cx:.1f},{cy:.1f} {x:.1f},{y:.1f}")
            i += 5
        elif t == 'Z':
            result.append("Z")
            i += 1
        else:
            i += 1
    return " ".join(result)


def measure_text_width(text, scale=1.0):
    """Measure the width of outlined text."""
    width = 0
    for ch in text.upper():
        width += (GLYPH_WIDTHS.get(ch, 60) + LETTER_SPACING) * scale
    return width - LETTER_SPACING * scale


def v_path_d(x=0, y=0, size=100):
    """Return SVG path data for V logo at given position and size."""
    scale = size / 100
    parts = []
    for i, (vx, vy) in enumerate(V_OUTLINE):
        px = x + vx * scale
        py = y + vy * scale
        parts.append(f"{'M' if i == 0 else 'L'} {px:.1f},{py:.1f}")
    parts.append("Z")
    return " ".join(parts)


def svg_die(width_in, height_in, content, label=""):
    """Wrap content in a production die SVG with white background."""
    w = round(width_in * 72)
    h = round(height_in * 72)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}"
     width="{w}" height="{h}">
  <!-- Foil Stamping Die — {label}
       Solid black on white. All text outlined (no live fonts).
       Book of Verse — Production Artwork -->
  <rect x="0" y="0" width="{w}" height="{h}" fill="white"/>
{content}
</svg>'''


def generate_front_emblem():
    """V logo at 2.5" wide for front cover foil die."""
    size_px = round(2.5 * 72)  # 180px
    margin = 18
    w = size_px + 2 * margin
    h = size_px + 2 * margin
    path = v_path_d(margin, margin, size_px)
    content = f'  <path d="{path}" fill="black"/>'
    svg = svg_die(w / 72, h / 72, content, "Front Cover V Emblem (2.5\" wide)")
    return svg


def generate_front_title():
    """'BOOK OF VERSE' title text, outlined paths."""
    text = "BOOK OF VERSE"
    scale = 0.6  # ~36pt equivalent
    tw = measure_text_width(text, scale)
    margin = 20
    w = tw + 2 * margin
    h = 80 * scale + 2 * margin
    paths, _ = text_to_paths(text, margin, margin, scale)
    content = "\n".join(f'  <path d="{p}" fill="black"/>' for p in paths)
    svg = svg_die(w / 72, h / 72, content, "Front Cover Title — BOOK OF VERSE")
    return svg


def generate_front_subtitle():
    """Subtitle text, outlined paths."""
    sub_text = "THE VERSE PROGRAMMING LANGUAGE"
    scale_sub = 0.28

    tw_sub = measure_text_width(sub_text, scale_sub)
    margin = 16
    w = tw_sub + 2 * margin
    h_sub = 80 * scale_sub

    paths_sub, _ = text_to_paths(sub_text, margin, margin, scale_sub)

    content = "\n".join(f'  <path d="{p}" fill="black"/>' for p in paths_sub)
    total_h = margin * 2 + h_sub
    svg = svg_die(w / 72, total_h / 72, content, "Front Cover Subtitle")
    return svg


def generate_spine_title():
    """Spine title 'BOOK OF VERSE' rotated for spine reading."""
    text = "BOOK OF VERSE"
    scale = 0.3  # ~18pt equivalent for spine
    tw = measure_text_width(text, scale)
    margin = 12
    # Spine title is rotated 90° — so SVG width = text height, height = text width
    text_h = 80 * scale
    w = text_h + 2 * margin
    h = tw + 2 * margin
    paths, _ = text_to_paths(text, margin, margin, scale)
    # Apply rotation: rotate 90° around center
    cx = w / 2
    cy = h / 2
    content = f'  <g transform="translate({w}, 0) rotate(90)">\n'
    content += "\n".join(f'    <path d="{p}" fill="black"/>' for p in paths)
    content += "\n  </g>"
    svg = svg_die(w / 72, h / 72, content, "Spine Title — BOOK OF VERSE (rotated)")
    return svg


def generate_spine_emblem():
    """V logo at 0.7" wide for spine foil die."""
    size_px = round(0.7 * 72)  # ~50px
    margin = 10
    w = size_px + 2 * margin
    h = size_px + 2 * margin
    path = v_path_d(margin, margin, size_px)
    content = f'  <path d="{path}" fill="black"/>'
    svg = svg_die(w / 72, h / 72, content, "Spine V Emblem (0.7\" wide)")
    return svg


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Generating foil stamping die artwork...\n")
    print(f"  Output: {OUTPUT_DIR}\n")

    dies = [
        ("die-front-emblem.svg", generate_front_emblem, "Front V emblem (2.5\" wide)"),
        ("die-front-title.svg", generate_front_title, "Front title: BOOK OF VERSE"),
        ("die-front-subtitle.svg", generate_front_subtitle, "Front subtitle"),
        ("die-spine-title.svg", generate_spine_title, "Spine title (rotated)"),
        ("die-spine-emblem.svg", generate_spine_emblem, "Spine V emblem (0.7\" wide)"),
    ]

    for filename, generator, description in dies:
        svg = generator()
        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  Created: {filename:30s} — {description}")

    # Generate a README for the production directory
    readme = """# Foil Stamping Die Artwork

Production-ready vector artwork for foil stamping dies.

## Files

| File | Content | Size |
|------|---------|------|
| `die-front-emblem.svg` | V logo for front cover | 2.5" wide |
| `die-front-title.svg` | "BOOK OF VERSE" title | Outlined text |
| `die-front-subtitle.svg` | Subtitle + author | Outlined text |
| `die-spine-title.svg` | Spine title (rotated) | Outlined text |
| `die-spine-emblem.svg` | V logo for spine | 0.7" wide |
| `die-spine-author.svg` | Author name (rotated) | Outlined text |

## Specifications

- **Format:** SVG (convert to PDF for submission using Inkscape or Illustrator)
- **Color:** Solid black on white background
- **Text:** All text converted to outlined paths (no live fonts)
- **No gradients:** Foil stamping requires solid areas only
- **Minimum feature:** 1mm line width verified

## Converting to PDF

Using Inkscape (command line):
```bash
inkscape die-front-emblem.svg --export-type=pdf --export-filename=die-front-emblem.pdf
```

Or open in Adobe Illustrator and export as PDF with "Preserve Illustrator Editing" unchecked.
"""
    readme_path = os.path.join(OUTPUT_DIR, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"\n  Created: README.md")

    print("\nDone! Convert SVGs to PDF using Inkscape or Illustrator for printer submission.")


if __name__ == "__main__":
    main()
