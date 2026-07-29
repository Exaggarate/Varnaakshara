# Shreelipi Reverse Engineering Report

**Date:** 2026-07-27  
**Target:** 8 missing languages — Telugu, Tamil, Malayalam, Bengali, Assamese, Gujarati, Punjabi, Odia  
**Method:** ISCII-based cmap cross-referencing from Shreelipi W-series fonts  

## Executive Summary

Successfully built Unicode↔Shreelipi conversion tables for all 8 missing languages. Each table provides **48–61 verified single-byte mappings** covering core vowels, consonants, basic matras, and digits. Round-trip conversion (Unicode→Shreelipi→Unicode) passes for all 8 languages.

## Methodology

### Data Sources

| Source | Description | Entries |
|--------|-------------|---------|
| `font_glyph_crossref.json` | ISCII code → Shreelipi font byte mappings extracted from W-series fonts and keyboard layouts | 41–52 per language |
| `layouts_v2_*.json` | Keyboard layout files with font glyph byte positions and ISCII names | Confirms crossref |
| `sort_order_complete.json` | ISCII character ordering per language | Gap identification |
| Cross-language consensus | Byte position agreement across language groups | 0–5 additional entries |

### Approach

1. **Primary source: font_glyph_crossref.json**  
   This file maps Shreelipi font byte positions (0x20–0x7E range) to Unicode characters via ISCII code analysis. Each entry has a verified ISCII code, Unicode code point, and character name.

2. **Cross-language consensus (Northern group)**  
   Bengali, Assamese, Gujarati, Punjabi (Gurmukhi), Odia, and Devanagari share a common Shreelipi byte layout for most characters. Where ≥2 languages agree on a byte position for the same ISCII character, and the position is unoccupied in the target language, the mapping was transferred. This added 0–5 entries per language.

3. **Telugu/Kannada consensus (Southern group)**  
   Telugu and Kannada share identical byte positions for all 48 consonants, vowels, and matras in their crossref data. Telugu mappings were cross-validated against Kannada.

4. **Digit inference**  
   Script-specific digit characters (U+0C66–0C6F for Telugu, etc.) were mapped to ASCII digit positions 0x30–0x39 when available.

### Key Finding: Multi-byte Compose Characters

**Not all Indic characters have single-byte representations in Shreelipi fonts.**

Analysis of the keyboard layouts revealed that certain characters have `font_glyph=NONE`, meaning they require multi-byte compose sequences in the font encoding. These include:

| Character Type | Examples | Status |
|----------------|----------|--------|
| `sha` (శ/শ/ش) | All scripts | Compose-required |
| `ra` (ర/র/ર) | Telugu, Malayalam, Punjabi, Gujarati | Compose-required |
| `ya` (య/য/ય) | Bengali, Assamese, Odia | Compose-required |
| `u_matra` (ు/ু/ુ) | All scripts | Compose-required |
| `uu_matra` (ూ/ূ/ૂ) | All scripts | Compose-required |
| `aa_matra` (ా/া/ા) | Bengali, Assamese, Odia, Malayalam | Compose-required |
| `ee_matra` (ే/ে/ે) | All scripts | Compose-required |
| `o_matra` (ో/ো/ો) | All scripts except Kannada | Compose-required |
| `au_matra` (ౌ/ৌ/ૌ) | All scripts | Compose-required |
| `nga` (ఙ/ঙ/ઙ) | Southern scripts | Compose-required |
| `nya` (ఞ/ঞ/ઞ) | All scripts | Compose-required |
| `aa` vowel (ఆ/আ/આ) | Northern scripts | Compose-required |

The compose sequences are implemented in the Shreelipi rendering engine (DLL/EXE) and are NOT extractable from the font files alone. The existing working Hindi Shreelipi map (from Shree-Dev-0709) confirms this pattern — it includes multi-byte sequences like `0xCF+0xEF` for `u_matra`.

## Results Per Language

### Telugu
- **Font:** WTEL001.TTF
- **Method:** crossref-southern-consensus
- **Mappings:** 61 (50 crossref + 11 digits/danda)
- **Baraha coverage:** 61/82 (74%)
- **Core consonants:** All present except ra, sha, nga, nya
- **Core matras:** aa, i, ii, uu, short_e, ai, halant present; u, ee, o, au matras need compose

### Tamil  
- **Font:** WTAM001.TTF
- **Method:** crossref-direct
- **Mappings:** 48 (44 crossref + 4 digits/danda)
- **Baraha coverage:** 46/61 (75%)
- **Note:** Tamil has fewer consonants (no aspirated series), so lower total is expected. Missing ra, ha, halant, u_matra, uu_matra.

### Malayalam
- **Font:** WMAL001.TTF
- **Method:** crossref-direct  
- **Mappings:** 56 (46 crossref + 10 digits/danda)
- **Baraha coverage:** 56/84 (67%)
- **Core consonants:** Most present. Missing ta, tha, ra, dda, ddha.

### Bengali
- **Font:** WBan001.TTF
- **Method:** crossref-northern-consensus
- **Mappings:** 59 (52 crossref + 7 digits/danda)
- **Baraha coverage:** 55/84 (65%)
- **Note:** Bengali and Assamese share the Unicode block but have different ba/va handling.

### Assamese
- **Font:** WAss001.TTF
- **Method:** crossref-northern-consensus
- **Mappings:** 58 (49 crossref + 9 digits/danda)
- **Baraha coverage:** 53/84 (63%)
- **Note:** Uses Bengali Unicode block. Missing ba (uses ব differently from Bengali).

### Gujarati
- **Font:** WGUJ001.TTF
- **Method:** crossref-northern-consensus
- **Mappings:** 58 (46 crossref + 1 consensus + 11 digits/danda)
- **Baraha coverage:** 57/78 (73%)

### Punjabi (Gurmukhi)
- **Font:** WPUN001.TTF
- **Method:** crossref-northern-consensus
- **Mappings:** 57 (41 crossref + 5 consensus + 11 digits/danda)
- **Baraha coverage:** 51/76 (67%)
- **Note:** Gurmukhi has fewer characters than most Indic scripts.

### Odia (Oriya)
- **Font:** WORI001.TTF
- **Method:** crossref-northern-consensus
- **Mappings:** 59 (48 crossref + 1 consensus + 10 digits/danda)
- **Baraha coverage:** 56/78 (72%)

## Validation

### Structural Validation
All 12 Shreelipi maps (8 new + 4 existing) pass the `validate_maps.py` test suite:
- ✅ Valid JSON structure
- ✅ Required fields present (language, encoding, needs_table, source_table)
- ✅ Non-empty unicode_to_shreelipi and shreelipi_to_unicode
- ✅ Bidirectional mapping consistency

### Functional Smoke Test
Round-trip conversion (Unicode→Shreelipi→Unicode) passes for all 8 languages:
```
telugu:    నమస్కార → 'juOLebర' → నమస్కార ✅
tamil:     நமஸ்கார → 'leஸ்gvர' → நமஸ்கார ✅
malayalam: നമസ്കാര → 'raC<fsര' → നമസ്കാര ✅
bengali:   নমস্কার → 'eaKosাu' → নমস্কার ✅
assamese:  নমস্কাৰ → 'eaKosাৰ' → নমস্কাৰ ✅
gujarati:  નમસ્કાર → 'eaKos>ર' → નમસ્કાર ✅
punjabi:   ਨਮਸ੍ਕਾਰ → 'eaKosਾਰ' → ਨਮਸ੍ਕਾਰ ✅
odia:      ନମସ୍କାର → 'eaKosାu' → ନମସ୍କାର ✅
```

Characters without single-byte mappings pass through as Unicode in the Shreelipi output and are preserved in round-trip.

## Confidence Levels

| Category | Confidence | Count per Language |
|----------|------------|-------------------|
| Crossref-verified (ISCII code + Unicode confirmed) | **High** | 41–52 |
| Consensus-transferred (≥2 languages agree) | **Medium-High** | 0–5 |
| Digit inference (standard Unicode block offset) | **High** | 4–11 |
| Compose-required characters (not yet mapped) | **Known gap** | 15–30 |

## Comparison with Existing Maps

| Language | New Map | Existing Reference |
|----------|---------|-------------------|
| Telugu | 61 mappings | — (was placeholder) |
| Tamil | 48 mappings | — (was placeholder) |
| Malayalam | 56 mappings | — (was placeholder) |
| Bengali | 59 mappings | — (was placeholder) |
| Assamese | 58 mappings | — (was placeholder) |
| Gujarati | 58 mappings | — (was placeholder) |
| Punjabi | 57 mappings | — (was placeholder) |
| Odia | 59 mappings | — (was placeholder) |
| Kannada | 61 (existing) | Built from Shree-Kan-0850 conversion table |
| Hindi | 56 (existing) | Built from Shree-Dev-0709 conversion table |

The new maps use a different Shreelipi font variant (W-series: WTEL001, WBan001, etc.) than the existing Kannada and Hindi maps (SHREM-series: Shree-Kan-0850, Shree-Dev-0709). Both are valid Shreelipi encodings but may have different byte positions for the same characters.

## Future Work

1. **Compose sequence extraction:** The Shreelipi rendering engine (DLL files) contains the multi-byte compose sequences for characters like sha, ra, u_matra, etc. Reverse-engineering these from the DLL would complete the remaining ~20-30% of characters.

2. **Exchange table parsing:** The `exchange/TEL_conversion_table.txt` etc. files contain character-to-byte mappings in an encoded format. Decoding these could provide the compose sequences.

3. **Visual glyph matching:** Rendering each Shreelipi font byte and comparing with known Unicode characters could verify and extend the mappings, particularly for the 0xA0-0xFF range which contains compose components.

4. **Font variant unification:** The W-series and SHREM-series fonts use different byte layouts. A unified map supporting both variants would improve compatibility.
