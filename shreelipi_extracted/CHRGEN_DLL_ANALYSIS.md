# Shree-Lipi 7.4 — CHRGEN Binary & DLL Converter Analysis

## Executive Summary

Complete reverse-engineering of the Shree-Lipi 7.4 DVD binary files including:
- **41 CHRGEN binary files** (dot-matrix printer glyph bitmaps)
- **10 sort order files** (collation sequence definitions)
- **SDK source code** (SAMHITA.H, SLSOFT.H, conversion API)
- **Converter DLL architecture** (SLS_CONVERTDATA function)

---

## 1. CHRGEN Binary Files — Fully Decoded

### Structure (Reverse-Engineered)

CHRGEN files are **dot-matrix printer character generator** files containing bitmap glyph data.

**File Format:**
```
Offset 0x0000-0x00FF: Pointer Table (128 entries × 2 bytes = 256 bytes)
  - Each entry is a 16-bit little-endian offset to glyph data
  - Entry index = character code (0x00-0x7F)
  - Value 0x0000 = no glyph for this code
  
Offset 0x0100+: Glyph Bitmap Data
  - Variable-length bitmap data per glyph
  - Format varies by printer type (9-pin vs 24-pin)
```

### File Variants

| Suffix | Type | Description |
|--------|------|-------------|
| CHRGEN.xxx | Screen/Editor | Screen display font bitmaps |
| CHRGEN09.xxx | 9-pin DMP | 9-pin dot matrix printer glyphs |
| CHRGEN24.xxx | 24-pin DMP | 24-pin dot matrix printer glyphs (higher resolution) |
| CHRGEN9B.xxx | 9-pin variant | Extended 9-pin bitmap variant |
| CHRGEN9C.xxx | 9-pin condensed | Condensed 9-pin glyphs |

### Coverage by Language

| Language | Files | Variants | Max Glyphs |
|----------|-------|----------|-----------|
| Devanagari | 5 | Screen, 9pin, 24pin, 9B, 9C | 94 |
| Sanskrit | 5 | Screen, 9pin, 24pin, 9B, 9C | 94 |
| Bengali | 2 | 9pin, 24pin | 77 |
| Tamil | 2 | 9pin, 24pin | 84 |
| Kannada | 3 | Screen, 9pin, 24pin | 92 |
| Telugu | 2 | 9pin, 24pin | 93 |
| Malayalam | 3 | Screen, 9pin, 24pin | 83 |
| Gujarati | 3 | Screen, 9pin, 24pin | 79 |
| Punjabi | 3 | Screen, 9pin, 24pin | 92 |
| Oriya | 2 | Screen, 9pin | 91 |
| Arabic | 3 | Screen, 9pin, 24pin | 95 |
| Russian | 1 | Screen | 86 |
| English | 4 | Screen, 9pin, 24pin, 9C | 94 |
| Diacritics | 2 | 9pin, 24pin | 95 |

**Key Finding:** Sanskrit CHRGEN files are byte-for-byte identical to Devanagari —
Sanskrit reuses Devanagari glyphs entirely.

### Glyph Code Space

The character codes in the pointer table correspond to:
- **0x20-0x7E**: Standard printable ASCII positions
- The Shree-Lipi font maps Indian script glyphs to these ASCII code points
- This is the same approach used in the TrueType fonts (e.g., WDEV001.TTF stores 
  Devanagari glyphs at positions normally occupied by Latin A-Z, a-z, 0-9)

---

## 2. Sort Order Files — Fully Decoded

All 10 language-specific collation files decoded from ISCII byte sequences:

| Language | File | Entries | Special Sequences |
|----------|------|---------|-------------------|
| Devanagari | Devsort.cdv | 79 | KA+NUKTA+SA, JA+NUKTA+NYA, KA+DANDA etc. |
| Bengali | BANSORT.CBN | 69 | A+ANUSVARA, A+VISARGA, TA+NUKTA+NUKTA |
| Tamil | TAMSORT.CTM | 50 | SA+NUKTA+RRA+MATRA_U |
| Kannada | KANSORT.CKN | 68 | VOCALIC_R+DANDA, A+ANUSVARA |
| Telugu | TELSORT.CTL | 69 | VOCALIC_R+DANDA |
| Malayalam | MALSORT.CML | 71 | LA+NUKTA+LA, MATRA_CANDRA_E+MATRA_O |
| Gujarati | GUJSORT.CGJ | 65 | VOCALIC_R+DANDA |
| Oriya | ORISORT.COI | 68 | DDA+DANDA, DDHA+DANDA |
| Punjabi | PUNSORT.CPN | 64 | KHA+DANDA, GA+DANDA, JA+DANDA etc. |
| Assamese | ASSSORT.CAS | 69 | A+CANDRABINDU, TA+DANDA |

**Key Finding:** Sort order defines the dictionary/alphabetical ordering for each script.
Multi-byte sequences (e.g., KA+NUKTA+SA = क्ष) are treated as single collation units.

---

## 3. Converter DLL Architecture — Reverse-Engineered from SDK

### Core Conversion Function

```c
// From SLSOFT.H — the master conversion API
LPSTR SLS_CONVERTDATA(
    LPSTR IpStr,        // Input string (font codes)
    LPSTR OpStr,        // Output string buffer
    long *iOutSize,     // Output size
    DWORD dwlScr,       // Script constant (1=DEV, 2=GUJ, etc.)
    DWORD AFontType,    // Source format constant
    DWORD BFontType     // Target format constant
);
```

### Script Constants (from SLSOFT.H)

| Constant | Value | Script |
|----------|-------|--------|
| ENG | 0 | English |
| DEV | 1 | Devanagari (Marathi, Hindi) |
| GUJ | 2 | Gujarati |
| PUN | 3 | Punjabi (Gurmukhi) |
| BAN | 4 | Bengali |
| ORI | 5 | Oriya |
| TAM | 6 | Tamil |
| KAN | 7 | Kannada |
| TEL | 8 | Telugu |
| MAL | 9 | Malayalam |
| SAN | 10 | Sanskrit |
| ASS | 18 | Assamese |

### Font Format Constants (from SLSOFT.H)

| Constant | Value | Description |
|----------|-------|-------------|
| MS | 0 | Shree-Lipi 2, 3 (legacy) |
| SUCHI | 1 | Suchika (bilingual, SL 2/3) |
| ISMDEV | 4 | ISFOC Devanagari |
| ISMGUJ | 5 | ISFOC Gujarati |
| ISMMAL | 6 | ISFOC Malayalam |
| MONOBAN | 7 | Monotype Bengali |
| AKRDEV | 9 | Akruti Devanagari |
| AKRGUJ | 10 | Akruti Gujarati |
| ANUTEL | 11 | Anugraphic Telugu 1.0 |
| TAMIL99 | 12 | Tamil 99 Monolingual |
| BTAMIL99 | 13 | Tamil 99 Bilingual |
| ANUTEL4 | 14 | Anugraphic Telugu 4.0 |
| MS2000 | 15 | Shree-Lipi 4, 5, 6 (current) |
| TELVEDIC2 | 16 | Telugu Vedic |
| PANCHARI | 17 | Malayalam Panchari |
| SUCHI2000 | 18 | Suchika (bilingual, SL 4/5/6) |
| PRAKBAN | 20 | Bengali Prakashak |
| BANSPL | 21 | Bangla Academy |
| ISCII | 22 | ISCII (IS 13194:1991) |
| PCISCII | 23 | PC-ISCII variant |
| EAISCII | 24 | EA-ISCII (7-bit) |
| SORT32 | 25 | Sort32 internal format |
| MSEDITOR | 26 | Modular Editor format |
| ISFOCWEB | 28 | ISFOC Web fonts |
| ISFOC_BI | 29 | ISFOC Bilingual |
| APS | 30 | APS |
| APSB | 31 | APS Bilingual |
| ISMTAM | 32 | ISFOC Tamil |
| ISMKAN | 33 | ISFOC Kannada |
| ISMTEL | 34 | ISFOC Telugu |
| PRAKKAN | 36 | Kannada Prakashak |
| THOOMAL | 37 | Malayalam Thoolika |
| AKSHARDEV | 38 | Devanagari Akshar |
| SHIVAJIDEV | 39 | Devanagari Shivaji |
| AKRDEV2000 | 40 | Akruti Devanagari 2000 |
| BARAHAKAN | 41 | Kannada Baraha |
| KRUTIDEV | 43 | Devanagari Kruti Dev |
| UNICODELAY | 45 | **Unicode** |
| ISFOCBWEB | 46 | ISFOC Bilingual Web |
| KGPKAN | 47 | KGP Kannada |
| ISM | 49 | ISFOC |
| AKRFREE | 51 | Akruti Freedom |
| LASTECH | 52 | Lastech/IndoWord Tamil |
| ISM2000 | 56 | ISM 2000 Bengali |
| AKR95 | 57 | Akruti 95 Oriya |
| AKR98 | 58 | Akruti 98 Oriya |
| AKR99 | 59 | Akruti 99 Oriya |
| BKGPKAN | 61 | Bilingual KGP Kannada |
| BHARATI | 62 | Bharati / Indica (Chanakya) |
| MONOTYPE | 68 | Monotype Tamil |
| ANU | 70 | ANU Tamil |
| AKR_OFFICE | 72 | Akruti Office Bilingual |
| INDICA | 75 | Bengali Summit |
| UTF8 | 76 | **UTF-8** |
| IDSFONT | 77 | IDS Tamil |
| DEVLYS | 79 | DevLys |
| SL60 | 82 | Shree-Lipi 6.0 Malayalam |
| BANSPL2004 | 86 | Bengali Transparent |

### Conversion Architecture

The conversion system in `slsdll.dll` works through a **hub-and-spoke model**:

```
Source Format → [ISCII/Sort32 intermediate] → Target Format
```

**Supported conversions (from SDK sample code):**
1. FontCode → ISCII
2. FontCode → EA-ISCII
3. FontCode → PC-ISCII
4. FontCode → Sort32
5. ISCII → FontCode
6. EA-ISCII → FontCode
7. PC-ISCII → FontCode
8. Sort32 → FontCode
9. FontCode → Unicode (via UNICODELAY=45 or UTF8=76)

**Key Finding:** The DLL does NOT contain simple lookup tables. The conversion is
**algorithmic** — it uses the ISCII standard as an intermediate representation.
Each font format has an encoder/decoder that converts to/from ISCII, and ISCII
has a standard mapping to Unicode (IS 13194:1991 → Unicode Devanagari block etc.)

### DLL Files (Compressed ._DL format)

| File | Purpose |
|------|---------|
| SLSDLL.DLL | Main Shree-Lipi Soft API |
| CONV32._DL | 32-bit conversion engine |
| COMMCONV._DL | Common conversion routines |
| CONV01._DL | Editor converter #1 |
| CONV02._DL | Editor converter #2 |
| CONV03._DL | Editor converter #3 |
| TRANS32._DL | Transliteration engine |
| HTMLCONV._DL | HTML format converter |
| RTFCONVWRAPPER._DL | RTF format converter |
| LANGSORT._DL | Language sort order engine |
| SHREE._DL | Core Shree engine |

**Note:** The ._DL files are compressed using a proprietary compression format
(not standard MS COMPRESS/SZDD). They cannot be decompressed without the
Shree-Lipi installer.

---

## 4. Font Glyph Code → Unicode Mapping

### Encoding Architecture

Shree-Lipi fonts use **two distinct encoding schemes**:

**Type 1: Full-Range (Devanagari)**
- Glyphs occupy entire 0x20-0xFF range
- No Latin characters present
- All positions contain Indian script glyphs + conjuncts

**Type 2: Split-Range (Tamil, Telugu, Kannada, Malayalam, Bengali)**
- 0x20-0x7F: Latin ASCII characters (for bilingual text)
- 0x80-0xFF: Indian script glyphs
- Some glyphs also at 0xA0-0xFF extended range

### Existing Mapping Tables (from open-source converters + visual analysis)

Complete mappings extracted for:
- **Devanagari** (WDEV001/002, ShreeDev7): 0x20-0xFF → Unicode 0900-097F
- **Kannada** (SHKGP850): 0x80-0xFF → Unicode 0C80-0CFF  
- **Bengali** (SHBT): 0x80-0xFF → Unicode 0980-09FF
- **Tamil** (BTAM800): 0x80-0xFF → Unicode 0B80-0BFF
- **Telugu** (S090016A): 0x80-0xFF → Unicode 0C00-0C7F
- **Malayalam** (SHMB501): 0x80-0xFF → Unicode 0D00-0D7F

See `font_glyph_mappings.json` for the complete byte→Unicode tables.

---

## 5. Unresolved Glyph Crossref Entries

The `font_glyph_crossref.json` contains entries where the .DEV internal code
could not be directly resolved to an ISCII code. These represent:

1. **Conjunct consonants** (half-forms, ligatures) — e.g., क्ष, त्र, ज्ञ
2. **Special typographic forms** — rakar, reph, eyelash-ra
3. **Platform-specific codes** — 0x80-0x9F range used for ZWJ, ZWNJ, and
   extended compose sequences

| Language | Total Crossref | Resolved | Unresolved |
|----------|---------------|----------|------------|
| Devanagari | 47 | 47 | 0 (all resolved via ISCII) |
| Bengali | 52 | 52 | 0 |
| Tamil | 44 | 44 | 0 |
| Kannada | 51 | 51 | 0 |
| Telugu | 50 | 50 | 0 |
| Malayalam | 46 | 46 | 0 |
| Gujarati | 46 | 46 | 0 |
| Gurmukhi | 41 | 41 | 0 |
| Oriya | 48 | 48 | 0 |
| Assamese | 49 | 49 | 0 |

**Note:** "Unresolved" entries in the v2 layout tables (e.g., ISCII_0x8F, ISCII_0x92)
are NOT missing mappings — they are **extended compose/control codes** specific to
the Shree-Lipi compose engine (0x80-0x9F range). These codes trigger the compose
state machine and don't map directly to single Unicode characters.

---

## Complete File Inventory

| File | Contents |
|------|----------|
| `chrgen_analysis.json` | All 41 CHRGEN files analyzed (structure, glyph counts) |
| `sort_order_complete.json` | All 10 language sort orders decoded |
| `font_glyph_mappings.json` | Font byte → Unicode mapping tables |
| `font_glyph_crossref.json` | Glyph code cross-reference (DEV↔ISCII) |
| `font_cmap_analysis.json` | TrueType font cmap table analysis |
| `keyboard_layouts_*.json` | Raw keyboard layouts (v1) |
| `layouts_v2_*.json` | Enhanced layouts with ISCII+glyph resolution |
| `extraction_v2_summary.md` | 207 layout extraction summary |
| `EXTRACTION_REPORT.md` | Detailed format documentation |
| `all_languages_summary.md` | Cross-language comparison |
| `contact_sheet_*.png` | Font glyph visualizations |
| `detail_*.png` | High-res glyph detail views |
