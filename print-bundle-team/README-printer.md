# Book of Verse — Team Edition
## Printer Submission Package

### Overview

| Specification | Value |
|--------------|-------|
| **Title** | Book of Verse |
| **Author** | Tim Sweeney and the Verse Team |
| **Quantity** | 100 copies |
| **Trim Size** | 7" x 10" |
| **Page Count** | 488 pages (padded for 16-page signatures) |
| **Spine Width** | TBD (confirm with mock-up) |

---

### Interior

- **File:** `interior.pdf` (print-ready with crop marks and 0.125" bleed)
- **Paper Size:** 7.25" x 10.25" (7" x 10" trim + 0.125" bleed per side)
- **Paper Stock:** 70-80 gsm natural/cream uncoated
- **Color:** Black text only (no color plates)
- **Crop Marks:** Included in PDF

---

### Binding

- **Type:** Smyth-sewn signatures
- **Cover Material:** Arizona Bonded Leather (Ecofibers), Goat emboss, Matte finish, Black (#111111)
- **Backing:** Round back
- **Boards:** 0.118" (3mm) binder's board
- **Corners:** Square
- **Case-in:** Loose
- **Endpapers:** 100# White
- **Head/Tail Bands:** TBD (color selection pending)
- **Ribbon Bookmarks:** 2 ribbons, 1/4" width (colors TBD)
- **Edge Staining:** Yes, 3 sides (color TBD)
- **Slipcase:** Yes — black Brillianta/Prestige, 1-color foil on spine (Jay Guitierrez)
- **Shrink Wrap:** Yes, individually

---

### Foil Stamping

- **Foil Color:** Silver (gloss)
- **See layout files** in `cover-artwork/` for full positioning with crop marks and dimensions

**Book foil elements:**

| Element | Content | Placement |
|---------|---------|-----------|
| Front: V emblem | Verse "V" logo, 2.5" wide | Centered horizontally, upper third of front cover |
| Front: Title | "BOOK OF VERSE" | Centered, below emblem |
| Front: Subtitle | "The Verse Programming Language" + author | Centered, below title |
| Spine: V emblem (x2) | Verse "V" logo, 0.7" wide | Top and bottom of spine |
| Spine: Title | "BOOK OF VERSE" rotated | Centered on spine, read bottom-to-top |

**Slipcase foil elements:**

| Element | Content | Placement |
|---------|---------|-----------|
| Front face: V emblem | Verse "V" logo, ~2.5" wide | Centered, upper portion (same die as book front) |
| Front face: Title | "BOOK OF VERSE" + subtitle | Centered, below emblem |
| Fore-edge: V emblem (x2) | Verse "V" logo, 0.7" wide | Each end of fore-edge panel (same die as book spine) |
| Fore-edge: Title | "BOOK OF VERSE" | Centered on fore-edge panel (same die as book spine) |

*Note: The slipcase is open-spine — the book's own spine foil is visible when shelved.*

---

### Die Artwork Files

All die artwork is vector SVG, solid black on white, with all text converted to
outlined paths (no live fonts). Files are at 100% actual size.

**Unique die elements (5 files):**

| File | Content | Physical Size | Used On |
|------|---------|---------------|---------|
| `die-v-emblem-2.5in.svg` | V logo (large) | 2.5" x 2.5" | Book front, Slipcase front |
| `die-v-emblem-0.7in.svg` | V logo (small) | 0.7" x 0.7" | Book spine, Slipcase fore-edge |
| `die-title-large.svg` | "BOOK OF VERSE" | 6.6" x 1.2" | Book front, Slipcase front |
| `die-title-spine.svg` | "BOOK OF VERSE" (spine size) | 3.4" x 0.7" | Book spine, Slipcase fore-edge |
| `die-subtitle.svg` | Subtitle + author (2 lines) | 7.2" x 0.75" | Book front, Slipcase front |

*Note: The binder's die maker will determine whether elements on the same surface
should be combined into a single die or kept separate, based on their press and
maximum die size. Elements in the same foil color on the same surface can be
combined for perfect registration.*

**Layout reference files (2 files):**

| File | Content |
|------|---------|
| `book-cover-layout.svg` | Full case spread showing all foil positions with crop marks and dimensions |
| `slipcase-layout.svg` | All slipcase faces with foil positions, dimensions, and 3D reference |

**Production composite (pending):** Once the mock-up confirms spine width and
slipcase dimensions, a full-size production composite PDF will be created showing
all foil elements positioned at exact final scale with crop marks and fold lines.
The binder can overlay this on the cover layout to verify registration.

---

### Package Contents

```
print-bundle-team/
  README-printer.md              ← This file
  specs.md                       ← Detailed material specifications
  interior.pdf                   ← Print-ready interior (crop marks + bleed)
  cover-artwork/
    book-cover-layout.svg        ← Layout reference: book case spread with foil positions
    slipcase-layout.svg          ← Layout reference: slipcase faces with foil positions
    die-v-emblem-2.5in.svg       ← Die art: V logo 2.5" (book front + slipcase front)
    die-v-emblem-0.7in.svg       ← Die art: V logo 0.7" (book spine + slipcase fore-edge)
    die-title-large.svg          ← Die art: "BOOK OF VERSE" large (book front + slipcase front)
    die-title-spine.svg          ← Die art: "BOOK OF VERSE" spine size (book spine + slipcase fore-edge)
    die-subtitle.svg             ← Die art: subtitle + author (book front + slipcase front)
```

---

### Notes

- All die artwork is vector, solid black on white, text outlined — ready for die production
- Dies are shared between book and slipcase where sizes match (see table above)
- Slipcase front face foil matches book front cover design (may need quote adjustment)
- Slipcase is open-spine — book spine is visible when shelved
- All dimensions TBD — spine width and slipcase sizing from binder's mock-up
- Final production composite will be created after mock-up confirms dimensions
- Request 1 proof copy before full production run
- On Arizona Bonded Leather (Goat texture), minimum line weight 0.75mm recommended;
  all die artwork exceeds this minimum
