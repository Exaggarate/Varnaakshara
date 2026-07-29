# Vedic Patched Fonts

## Problem

Standard Noto Sans Kannada and Noto Sans Devanagari fonts render the **dīrgha svarita** mark (U+1CDA, ᳚) as what looks like ASCII quotation marks `"`. This is because the glyph consists of two separate thin rectangular contours that visually resemble double quotes at display sizes.

The **svarita** (U+0951) and **anudātta** (U+0952) render correctly in both fonts — only U+1CDA has visual issues.

## Solution

We patched the U+1CDA glyph in both fonts to use a **∏-shaped single contour** — two vertical strokes connected by a horizontal bar at the bottom. This creates a visually distinct "double svarita" mark that cannot be confused with quotation marks.

### Glyph Design

```
Original (2 contours):       Patched (1 contour, ∏ shape):
  ║  ║                         ║  ║
  ║  ║                         ║  ║
  ║  ║                         ║  ║
                               ╚══╝
(looks like ")                (clearly double-line mark)
```

### Technical Details

- **Tool**: fontTools (Python) — modified `coordinates` in the `glyf` table
- **Glyph**: Single clockwise TrueType contour with 8 on-curve points
- **GPOS anchors**: Kept from original font (mark positioning unchanged)
- **Font names**: Renamed to avoid conflicts with system fonts
  - `Noto Sans Kannada` → `Noto Sans Kannada Vedic`
  - `Noto Sans Devanagari` → `Noto Sans Devanagari Vedic`

### Parameters

| Parameter | Kannada | Devanagari |
|-----------|---------|------------|
| Stroke width | 45 units | 45 units |
| Gap between strokes | 80 units | 80 units |
| Connecting bar height | 30 units | 30 units |
| Y range | 583–839 | 656–902 |

## Installation

Copy the `.ttf` files to:
- **Windows**: `C:\Users\<user>\AppData\Local\Microsoft\Windows\Fonts\`
- Register in: `HKCU\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts`

## Base Fonts

- Noto Sans Kannada (from Google Fonts / bundled with Windows)
- Noto Sans Devanagari (from Google Fonts / bundled with Windows)

Both are licensed under the SIL Open Font License 1.1.

## What Still Works

- All standard Kannada/Devanagari characters — unchanged
- U+0951 (svarita) — unchanged, works in original
- U+0952 (anudātta) — unchanged, works in original
- All other Vedic Extension marks — unchanged
- GPOS mark positioning — unchanged
- GSUB substitution rules — unchanged

Only the single glyph for U+1CDA was modified.
