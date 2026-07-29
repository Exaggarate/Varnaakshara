# Shree-Lipi DVD Fonts & PDF Extraction Report

**Date:** 2026-07-04  
**Source:** `/tmp/SL74DVD/`

---

## 1. UniFonts Inventory (`UniFonts/`)

**Location:** `unifonts_inventory.json`

### Summary
- **9 script directories:** Bangla, Devanagari, Gujarati, Kannada, Malayalam, Odia, Punjabi, Tamil, Telugu
- **73 total files** (64 encrypted `._TF` + 8 valid `.TTF` + 1 `.zip`)
- **2 font families per script** (except Odia which has 2 families + 1 zip archive)
- **4 styles per family:** Regular, Bold, Italic, BoldItalic

### Font Families by Script

| Script | Families | Files | Format |
|--------|----------|-------|--------|
| ban (Bangla) | SHREE0560, SHREE0592 | 8 | `._TF` (encrypted) |
| dev (Devanagari) | SHREE0708, SHREE0714 | 8 | `._TF` (encrypted) |
| Guj (Gujarati) | SHREE0750, SHREE0768 | 8 | `._TF` (encrypted) |
| kan (Kannada) | SHREE0850, SHREE0853 | 8 | `._TF` (encrypted) |
| mal (Malayalam) | SHREE0501, SHREE0507 | 8 | `._TF` (encrypted) |
| ori (Odia) | SHREE_ORI_OTF_0601, SHREE_ORI_OTF_0603 | 9 | **.TTF (valid!)** + `.zip` |
| pun (Punjabi) | SHREE0951, SHREE0953 | 8 | `._TF` (encrypted) |
| Tam (Tamil) | SHREE0800, SHREE0802 | 8 | `._TF` (encrypted) |
| tel (Telugu) | SHREE0900, SHREE0908 | 8 | `._TF` (encrypted) |

### ⚠️ Key Finding: `._TF` Files Are NOT Simple TTF Renames

**Verification performed:**
1. Copied `SHREE0708._TF` → renamed to `.ttf`
2. `file` command returns `data` (not `TrueType Font data`)
3. Hex header shows `d02e 8305 523a 554b...` — **no TTF magic bytes** (`00 01 00 00`)
4. These are **encrypted/obfuscated** proprietary font files

**Exception:** The `ori/` (Odia) directory contains **real TrueType fonts** with valid headers:
- `SHREE_ORI_OTF_0601 0601 Regular.TTF` → confirmed `TrueType Font data, 20 tables`
- 8 valid `.TTF` files (4 per family × 2 families)
- Plus `ori-Old.zip` archive with older versions

---

## 2. PDF Extraction (`SHREELIPI_SOFT_API.pdf`)

**Output:** `SLSOFT_API_EXTRACTED.md` (144KB, 131 pages)

### Document: "Shree-Samhita Reference Manual"
- **Publisher:** Modular InfoTech Pvt Ltd, Pune
- **Purpose:** SDK documentation for Shree-Lipi Soft API
- **~101 API functions** documented across 9 chapters + 2 appendices

### Chapter Summary

| Chapter | Topic | Key Content |
|---------|-------|-------------|
| 1 | Introduction | What Shree-Lipi Soft is, multilingual DLL toolkit |
| 2 | Installation | DLLs: `SLSDLL.DLL`, `SHREE.DLL`, `CONV32.DLL`, `CNVAPI32.DLL`, `TRANS32.DLL`, `DMP.DLL` |
| 3 | API Overview | **Script codes** (0=English, 1=Devanagari...9=Malayalam, 10=Sanskrit, 18=Assamese), **Font layouts** (Shree, Suchika, Akruti, ISCII, Unicode, UTF-8), **Keyboard layouts**, **Data Exchange Structure** |
| 4 | General Calls | `SLS_START2`, `SLS_CLOSE`, `SLS_SETUP`, script/font/keyboard management, tutor |
| 5 | Conversion Calls | **Format conversion:** SL→ISCII→PC-ISCII→EA-ISCII→Sort32→Unicode→UTF-8. `SLS_CONVERTDATA()`, `SLS_NUM_TO_WORDS()`, `SLS_DATETIME_TO_STR()`, custom sort |
| 6 | Transliteration | English↔Indian language transliteration with dictionary support (main/subject/user dictionaries). Phonetic fallback. |
| 7 | Dot Matrix Printing | Fast DMP printing, ISCII printer support, formatted printing, spooling |
| 8 | Error Codes | 37 error codes (0-160) |
| 9 | Utilities | Keyboard Tutor |
| App A | Data Exchange Structure | `SHREE_ERROR`, `CUR_SCR`, `FONT_NAME`, `FONT_LAYOUT`, `ACTIVATION_KEY`, `KEYBOARDNAME` |
| App B | Network Troubleshooter | HASP dongle / NetHASP license manager issues |

### Critical Data for VarnaAkshara IME

**Script Codes (internal numbering system):**
```
0 = English           5 = Oriya
1 = Devnagari         6 = Tamil
2 = Gujarati          7 = Kannada
3 = Punjabi           8 = Telugu
4 = Bengali/Assamese  9 = Malayalam
                     10 = Sanskrit
                     18 = Assamese (separate from Bengali)
```

**Font Layout Codes:**
```
0  = Shree-Lipi 2,3          15 = Shree-Lipi 4,5,6
18 = Suchika 4,5,6           22 = ISCII
23 = PC-ISCII                24 = EA-ISCII (7-bit)
25 = Sort32                  26 = Modular editor
45 = Unicode                 76 = UTF-8
```

**Font Naming Convention:**
- `SHREE-DEV-0708` = Shree layout, Devanagari, font #0708
- `SUCHI-DEV-0708` = Suchika (bilingual) layout, Devanagari, font #0708
- Number ranges map to scripts (700-750 = Devanagari, etc.)

**Key Conversion Function:**
```
SLS_CONVERTDATA(InputString, OutputString, OutputSize, ScriptCode, InputLayout, OutputLayout)
```
This is the core function for converting between ANY supported formats including SL↔ISCII↔Unicode↔UTF-8.

---

## 3. ExFonts Inventory (`ExFonts/`)

**Output:** `exfonts_inventory.json`

| Script | Files | Notes |
|--------|-------|-------|
| Ban (Bangla) | 139 | All extensionless (`SLX_` prefix) |
| Dev (Devanagari) | 1,281 | Largest collection |
| Dia (Diacritical) | 14 | |
| Guj (Gujarati) | 1,853 | Largest of all scripts |
| Kan (Kannada) | 421 | |
| Mal (Malayalam) | 317 | |
| Ori (Odia) | 113 | |
| Pun (Punjabi) | 179 | |
| San (Sanskrit) | 17 | |
| Tam (Tamil) | 450 | |
| Tel (Telugu) | 376 | |
| **Total** | **5,160** | All encrypted/proprietary format |

- Files named like `SLX_0700`, `SLX_0701`, etc.
- No file extensions — all report as `data` (encrypted)
- Hex headers show encrypted content (no standard font magic bytes)

---

## 4. SUFONTS Inventory (`SUFONTS/`)

**Output:** `sufonts_inventory.json`

"Supplementary Fonts" — smaller set per script.

| Script | Files | Sample Names |
|--------|-------|-------------|
| BAN | 4 | SU_0550, SU_0552, SU_0560 |
| DEV | 16 | SU_0708, SU_0709, SU_0710 |
| GUJ | 15 | SU_0760, SU_0762, SU_0763 |
| KAN | 15 | SU_0850, SU_0851, SU_0852 |
| MAL | 15 | SU_0501, SU_0502, SU_0504 |
| ORI | 15 | SU_0600, SU_0601, SU_0602 |
| PUN | 16 | SU_0950, SU_0951, SU_0952 |
| TAM | 15 | SU_0802, SU_0803, SU_0805 |
| TEL | 15 | SU_0900, SU_0902, SU_0908 |
| **Total** | **126** | All extensionless, encrypted |

---

## 5. FKFONTS Inventory (`FKFONTS/`)

**Output:** `fkfonts_inventory.json`

"FK Fonts" — includes additional scripts (Assamese, English, Symbols).

| Script | Files | Notes |
|--------|-------|-------|
| ASS (Assamese) | 132 | 131 fonts + 1 `.MAP` file |
| BAN (Bangla) | 132 | 131 + 1 `.MAP` |
| DEV (Devanagari) | 296 | 295 + 1 `.MAP` |
| ENG (English) | 61 | 60 + 1 `.MAP` |
| GUJ (Gujarati) | 186 | 185 + 1 `.MAP` |
| KAN (Kannada) | 67 | 66 + 1 `.MAP` |
| MAL (Malayalam) | 89 | 88 + 1 `.MAP` |
| ORI (Odia) | 51 | 50 + 1 `.MAP` |
| PUN (Punjabi) | 114 | 113 + 1 `.MAP` |
| SYM (Symbols) | 4 | 3 + 1 `.MAP` |
| TAM (Tamil) | 89 | 88 + 1 `.MAP` |
| TEL (Telugu) | 68 | 67 + 1 `.MAP` |
| **Total** | **1,289** | Each script has exactly 1 `.MAP` file |

**Notable:** Each script directory contains exactly one `.MAP` file alongside the encrypted font files. These `.MAP` files likely contain the character mapping/encoding tables.

---

## 6. FONTS Full Inventory (`FONTS/`)

**Output:** `fonts_full_inventory.json`

The main font library — the largest collection on the DVD.

| Script | Files | Size (MB) | Font # Range | Notes |
|--------|-------|-----------|-------------|-------|
| ARA (Arabic) | 12 | 0.27 | 664-675 | |
| ASS (Assamese) | 139 | 6.25 | 550-5132 | |
| Ban (Bangla) | 139 | 6.36 | 550-5132 | |
| DIA (Diacritical) | 15 | 0.38 | 1900-1914 | |
| Dev (Devanagari) | 1,324 | 50.13 | 700-6050 | Largest by far |
| ENG (English) | 509 | 6.62 | 2-6298 | |
| ENS | 9 | 0.08 | 2140-2148 | |
| GUJ (Gujarati) | 624 | 25.49 | 750-5799 | |
| IDIA | 15 | 0.25 | 1900-1914 | |
| KAN (Kannada) | 421 | 18.38 | 850-5370 | |
| MAL (Malayalam) | 317 | 16.03 | 501-4479 | |
| MUS (Music?) | 1 | 0.00 | 2001 | Single font |
| ORI (Odia) | 113 | 6.30 | 600-3062 | |
| PUN (Punjabi) | 179 | 2.90 | 950-5823 | |
| RUS (Russian) | 5 | 0.05 | 73-450 | |
| SAN (Sanskrit) | 17 | 0.56 | 960-1963 | |
| SLS | 19 | 0.74 | 540-1708 | |
| SND (Sindhi) | 16 | 0.41 | 680-695 | |
| SNDENG | 9 | 0.08 | 2140-2148 | |
| SYM (Symbols) | 143 | 11.71 | 3-4859 | |
| TAM (Tamil) | 544 | 28.01 | 800-5493 | |
| TEL (Telugu) | 375 | 14.04 | 900-5527 | |
| **Total** | **4,945** | **195.05** | | **22 script directories** |

All files are extensionless and in Shree-Lipi's proprietary encrypted format.

---

## Grand Totals

| Directory | Scripts | Files | Format |
|-----------|---------|-------|--------|
| UniFonts | 9 | 73 | `._TF` encrypted (except 8 Odia `.TTF`) |
| ExFonts | 11 | 5,160 | Extensionless, encrypted |
| SUFONTS | 9 | 126 | Extensionless, encrypted |
| FKFONTS | 12 | 1,289 | Extensionless + `.MAP` |
| FONTS | 22 | 4,945 | Extensionless, encrypted |
| **Total** | — | **11,593** | |

**Usable (unencrypted) fonts: 8** — Only the Odia `.TTF` files in `UniFonts/ori/`

---

## Relevance to VarnaAkshara IME

### What's Useful
1. **API Documentation** (`SLSOFT_API_EXTRACTED.md`) — Critical reference for understanding:
   - Shree-Lipi's internal script codes and font layout system
   - Conversion pathways between formats (SL → ISCII → Unicode → UTF-8)
   - The `SLS_CONVERTDATA()` function and layout code system
   - Keyboard layout file format (e.g., `MODULAR.DEV`, `ENG.DEV`)
   - Font naming conventions and number→script mapping

2. **Font Number Mapping** — Font numbers reveal script assignments:
   - 500-599: Malayalam/Bangla/Odia
   - 600-699: Odia/Arabic/Sindhi
   - 700-799: Devanagari/Gujarati
   - 800-899: Tamil/Kannada
   - 900-999: Telugu/Punjabi

3. **FKFONTS `.MAP` files** — May contain character encoding mappings useful for conversion table reconstruction

### What's NOT Directly Usable
- **All encrypted font files** — Cannot be used without Shree-Lipi's proprietary DLLs
- The `._TF` and extensionless files are encrypted/obfuscated, not standard font formats
- No glyph data or Unicode mappings can be extracted from encrypted fonts

### Recommended Next Steps
1. Extract and analyze the `.MAP` files from FKFONTS — they may contain encoding tables
2. Examine keyboard layout files (`.DEV`, `.GUJ`, etc.) from the installation directories
3. Use the API documentation's layout codes to understand conversion pathways for building equivalent functionality in VarnaAkshara
4. The 8 usable Odia TTF fonts could be analyzed for glyph structure and OpenType tables
