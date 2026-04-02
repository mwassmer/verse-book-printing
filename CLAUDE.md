# Book of Verse — Printing Project

## Overview

100 copies of the Verse programming language documentation as a premium hardcover book. Team morale item for the Epic Games Verse team.

## Build Pipeline

Source repo (`verse-book-source/`, clone of github.com/verselang/book) is **read-only — never modify it**.
All print fixes live in this repo's pipeline.

1. **Preprocess:** `python scripts/preprocess.py ../verse-book-source/docs build/combined.md`
   - Combines markdown, converts admonitions, fixes links
   - `fix_print_overflows()` applies code line breaks for print margins
2. **Pandoc:** `pandoc build/combined.md -o build/BookOfVerse-print.tex --template=templates/print-ready.tex --toc --toc-depth=3 --number-sections --top-level-division=chapter --highlight-style=tango "--variable=date:March 2026" "--metadata=title:Book of Verse" "--metadata=author:Tim Sweeney and the Verse Team" -V documentclass=book -V papersize=letter -V fontsize=11pt`
3. **XeLaTeX:** Run twice for correct TOC/page refs: `xelatex -interaction=nonstopmode -output-directory=build build/BookOfVerse-print.tex`
4. **Output:** `build/BookOfVerse-print.pdf` (480 pages, 30 x 16 signatures)

## Key Constraints

- **Never modify `verse-book-source/`** — it's upstream verselang/book
- **Formatting fixes only** — no changing content, identifiers, comments, or table columns
- When fixing overflows, add replacements to `scripts/preprocess.py` `fix_print_overflows()` or modify LaTeX templates
- **Verify with text diff** after changes to guarantee no content was altered
- Check overflows: compile with xelatex, parse log for `Overfull \hbox` warnings using `build/check_overflows.py`

## Print Specs

- 7" x 10" trim, print-ready template has 0.125" bleed + crop marks
- JetBrains Mono at Scale=0.85 (~73 chars per code line)
- Template overflow fixes: `\emergencystretch=5em`, `\tolerance=400`, breakable `\texttt`, `\scriptsize` tables
- One known remaining overflow: precedence table (Ch5, ~53pt into outer margin)

## Vendors

- **Printer:** O'Neill Printing (Brandee Shill, Zach) — offset, 16-page signatures
- **Binder:** BindTech Phoenix, Quote #80686R1, $107.99/unit + dies — Dawn Adair (602-272-9338 x4108)
- **Slipcase:** Jay Guitierrez (602-570-8218) — open-spine, black Brillianta/Prestige

## Book Specs

- Cover: Arizona Bonded Leather (Goat emboss, Matte), Black
- Foil: Silver gloss on front + spine (book), front face + fore-edge (slipcase)
- Binding: Smyth-sewn, round back, 0.118" boards, square corners
- Endpapers: 100# White
- Headbands: Black/Gold
- Ribbons: 2x 1/4" (color TBD — darker grays/blacks/silvers requested)
- Edge staining: Silver (pending binder confirmation)
- Slipcase: open-spine design (book spine visible when shelved)

## Bash Preferences

- Use absolute paths, not `cd path && command`
- No heredocs or quoted newlines in commands
- Both trigger manual approval prompts
