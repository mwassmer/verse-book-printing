# Book of Verse - Premium Print Edition

Convert the Verse Programming Language documentation into a high-quality printed book suitable for professional custom printing.

## Overview

This project converts the official Verse documentation from https://verselang.github.io/book/ into a beautifully typeset PDF optimized for premium book printing as a team morale item.

### Features

- **Professional Typography**: Source Serif/Sans fonts with JetBrains Mono for code
- **Print-Optimized Layout**: 7" × 10" format with proper margins for binding
- **Syntax Highlighting**: Custom Verse language highlighting for code blocks
- **Structured Content**: Organized into 5 parts with 19 chapters
- **High-Quality Output**: Vector graphics, proper page breaks, widow/orphan control

### Estimated Output

- **Page Count**: 550-700 pages
- **Word Count**: ~140,000 words
- **Code Examples**: 400+
- **Format**: 7" × 10" (standard technical book size)

---

## Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   # Windows (via winget)
   winget install Python.Python.3.11

   # macOS (via Homebrew)
   brew install python@3.11

   # Ubuntu/Debian
   sudo apt install python3
   ```

2. **Pandoc 3.0+**
   ```bash
   # Windows (via winget)
   winget install JohnMacFarlane.Pandoc

   # macOS (via Homebrew)
   brew install pandoc

   # Ubuntu/Debian
   sudo apt install pandoc
   ```

3. **TeX Live (Full) or MiKTeX**

   **Windows (MiKTeX - recommended):**
   - Download from https://miktex.org/download
   - Install with "Install missing packages on-the-fly" enabled

   **Windows (TeX Live):**
   ```bash
   winget install TeXLive.TeXLive
   ```

   **macOS:**
   ```bash
   brew install --cask mactex
   # OR for smaller install:
   brew install --cask basictex
   sudo tlmgr update --self
   sudo tlmgr install collection-fontsrecommended collection-latexextra
   ```

   **Ubuntu/Debian:**
   ```bash
   sudo apt install texlive-full
   # OR for smaller install:
   sudo apt install texlive-xetex texlive-fonts-recommended texlive-latex-extra
   ```

### Required Fonts (for best results)

Install these fonts for optimal typography:

1. **Source Serif 4** - Body text
   - https://fonts.google.com/specimen/Source+Serif+4

2. **Source Sans 3** - Headings
   - https://fonts.google.com/specimen/Source+Sans+3

3. **JetBrains Mono** - Code blocks
   - https://www.jetbrains.com/lp/mono/

If fonts are not installed, the build will fall back to Latin Modern fonts.

---

## Building the PDF

### Windows (PowerShell)

```powershell
cd VerseBook
.\build.ps1
```

Options:
```powershell
.\build.ps1 -Clean              # Clean build directory
.\build.ps1 -PreprocessOnly     # Only run preprocessing
.\build.ps1 -Output "custom.pdf" # Custom output filename
```

### Unix/Linux/macOS

```bash
cd VerseBook
chmod +x build.sh
./build.sh
```

### Manual Build Steps

If you prefer to run steps manually:

```bash
# 1. Preprocess markdown
python scripts/preprocess.py ../verse-book-source/docs build/combined.md

# 2. Convert to PDF with Pandoc
pandoc build/combined.md \
    -o output/BookOfVerse.pdf \
    --template=templates/pandoc-template.tex \
    --pdf-engine=xelatex \
    --toc \
    --toc-depth=3 \
    --number-sections \
    --top-level-division=chapter
```

---

## Print Production Guide

### Recommended Print Specifications

| Specification | Value |
|--------------|-------|
| **Trim Size** | 7" × 10" (178mm × 254mm) |
| **Paper** | 60-70 lb natural/cream text |
| **Binding** | Perfect binding or case binding |
| **Cover** | Soft cover (laminated) or hardcover |
| **Color** | Interior: Black & white or 2-color |
| **Margins** | Inner: 0.875", Outer: 0.75", Top/Bottom: 0.875" |

### Print Vendors

For premium custom printing, consider:

1. **Lulu** (lulu.com) - Print-on-demand, no minimums
2. **Blurb** (blurb.com) - High-quality photo books and trade books
3. **IngramSpark** - Professional distribution quality
4. **PrintNinja** - Offset printing for larger quantities (100+)
5. **Local print shops** - For truly premium/custom work

### PDF Export Options

The generated PDF includes:
- Embedded fonts (all glyphs)
- Vector graphics where possible
- PDF bookmarks for navigation

For professional printing, you may want to:

1. **Add crop marks and bleed** (if required by printer)
2. **Convert to CMYK** (if printing in color)
3. **Verify page count** is divisible by 4 (for signatures)

### Cover Design

The PDF does not include a cover. For a custom cover:

1. Get spine width from your printer based on page count
2. Design cover at printer's required dimensions
3. Include bleed (typically 0.125" on all sides)
4. Export as separate PDF (CMYK, 300 DPI minimum)

---

## Book Structure

### Parts and Chapters

```
Front Matter
├── Half Title
├── Title Page
├── Copyright Page
└── Table of Contents

Part I: Fundamentals
├── Chapter 1: Overview
├── Chapter 2: Expressions
├── Chapter 3: Primitive Types
├── Chapter 4: Container Types
└── Chapter 5: Operators

Part II: Core Features
├── Chapter 6: Mutability
├── Chapter 7: Functions
├── Chapter 8: Control Flow
├── Chapter 9: Failure
└── Chapter 10: Structs and Enums

Part III: Object-Oriented Programming
├── Chapter 11: Classes and Interfaces
├── Chapter 12: Type System
└── Chapter 13: Access Specifiers

Part IV: Advanced Topics
├── Chapter 14: Effects
├── Chapter 15: Concurrency
├── Chapter 16: Live Variables
└── Chapter 17: Modules and Paths

Part V: Production
├── Chapter 18: Persistable Types
└── Chapter 19: Code Evolution

Back Matter
├── Concept Index
└── Colophon
```

---

## Customization

### Changing Page Size

Edit `templates/pandoc-template.tex`:

```latex
\usepackage[
    paperwidth=6in,      % Change dimensions
    paperheight=9in,
    inner=0.75in,        % Adjust margins
    outer=0.625in,
    ...
]{geometry}
```

Common sizes:
- 6" × 9" - Standard trade paperback
- 7" × 10" - Technical book (current)
- 8.5" × 11" - Letter size manual

### Changing Fonts

Edit the font definitions in `templates/pandoc-template.tex`:

```latex
\setmainfont{Your Font Name}
\setsansfont{Your Sans Font}
\setmonofont{Your Mono Font}[Scale=0.85]
```

### Adding a Custom Foreword

Edit `scripts/preprocess.py` and add content to the CHAPTERS list:

```python
CHAPTERS = [
    ("foreword.md", "Foreword", False),  # Add custom foreword
    ("index.md", "Preface", False),
    ...
]
```

Create `docs/foreword.md` in the source directory.

### Changing Colors

Edit the color definitions in `templates/pandoc-template.tex`:

```latex
\definecolor{verseblue}{RGB}{30, 90, 160}
\definecolor{verseorange}{RGB}{255, 87, 34}
```

---

## Troubleshooting

### "Font not found" errors

- Install the required fonts system-wide
- Or let the template fall back to Latin Modern (built into TeX Live)

### Build fails with LaTeX errors

1. Run with verbose output to see errors
2. Check `build/combined.md` for malformed content
3. Ensure all required LaTeX packages are installed

### PDF too large

- Reduce image quality (if any images added)
- Use `--pdf-engine-opt=-compress` with Pandoc
- Consider grayscale for code blocks

### Pages not breaking correctly

Edit the preprocessing script to add `\newpage` commands where needed, or manually edit `build/combined.md`.

---

## License

The Verse documentation is licensed under **CC0-1.0** (Public Domain).

This conversion toolkit is provided as-is for creating team morale items.

---

## Credits

- **Verse Language Documentation**: Tim Sweeney and the Verse Team at Epic Games
- **Source**: https://github.com/verselang/book
- **Conversion Toolkit**: Custom build pipeline for premium printing
