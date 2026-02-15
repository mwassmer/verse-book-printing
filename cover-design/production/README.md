# Foil Stamping Die Artwork

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
