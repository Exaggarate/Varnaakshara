# Varnaakshara Font Generation Report

**Generated:** 2026-07-27  
**Tools:** `tools/generate_font_weights.py`, `tools/generate_shreelipi_weights.py`, `tools/rename_fonts.py`  
**Dependencies:** Python fonttools 4.63.0, skia-pathops 0.9.2

---

## Grand Summary

| Metric | Value |
|--------|-------|
| **Total font families** | **136** (22 Baraha + 114 Shreelipi) |
| **Total font files** | **680** (110 Baraha + 570 Shreelipi) |
| Weights per family | 5 (Regular, Medium, SemiBold, Bold, Black) |
| Scripts covered | 14 (Bengali, Devanagari, Gujarati, Kannada, Malayalam, Tamil, Telugu, Assamese, Odia, Punjabi, Sanskrit, Sindhi, Diacritical, Arabic*) |
| Naming convention | `Varnaakshara [Script] Lipi [NN]` (Baraha), `Varnaakshara Shreelipi [Script] [NN]` (Shreelipi) |

*Arabic source font had corrupted tables and could not be processed.

---

## Naming Convention

### Baraha-based fonts (22 families, 110 files)
- **Family name:** `Varnaakshara [Script] Lipi [NN]`
- **Examples:** Varnaakshara Kannada Lipi 01, Varnaakshara Bengali Lipi 02
- **PostScript:** `Varnaakshara-[Script]-Lipi-[NN]-[Weight]`
- **Directory:** `core/fonts/generated/[baraha-code]/`
- **Source:** Baraha ANSI fonts from `fonts/ansi/`

### Shreelipi-based fonts (114 families, 570 files)
- **Family name:** `Varnaakshara Shreelipi [Script] [NN]`
- **Examples:** Varnaakshara Shreelipi Tamil 01, Varnaakshara Shreelipi Kannada 08
- **PostScript:** `Varnaakshara-Shreelipi-[Script]-[NN]-[Weight]`
- **Directory:** `core/fonts/generated/shreelipi/shreelipi-[code]-[nn]/`
- **Source:** Shreelipi ANSI fonts from `shreelipi_extracted/fonts/`

### Weight naming (all families)
| Weight | usWeightClass | OS/2 fsSelection |
|--------|--------------|-----------------|
| Regular | 400 | REGULAR |
| Medium | 500 | — |
| SemiBold | 600 | — |
| Bold | 700 | BOLD |
| Black | 900 | BOLD |

---

## Part 1: Baraha Font Families (22 families, 110 files)

**Rename:** All fonts renamed from "Varnaaksharam" → "Varnaakshara" (133 files total including 23 source fonts).

| # | Family Name | Source File | Script | Glyphs |
|---|-------------|-------------|--------|--------|
| 01 | Varnaakshara Kannada Lipi 01 | brhaknd.ttf | Kannada | 223 |
| 02 | Varnaakshara Bengali Lipi 01 | brhben.ttf | Bengali | 256 |
| 03 | Varnaakshara Bengali Lipi 02 | brhbenrn.ttf | Bengali | 256 |
| 04 | Varnaakshara Kannada Lipi 02 | brhbglr.ttf | Kannada | 224 |
| 05 | Varnaakshara Devanagari Lipi 01 | brhdevrn.ttf | Devanagari | 256 |
| 06 | Varnaakshara Gujarati Lipi 01 | brhguj.ttf | Gujarati | 250 |
| 07 | Varnaakshara Gujarati Lipi 02 | brhgujrn.ttf | Gujarati | 250 |
| 08 | Varnaakshara Kannada Lipi 03 | brhkai.ttf | Kannada | 224 |
| 09 | Varnaakshara Kannada Lipi 04 | brhknd.ttf | Kannada | 223 |
| 10 | Varnaakshara Kannada Lipi 06 | brhknde.ttf | Kannada | 223 |
| 11 | Varnaakshara Kannada Lipi 07 | brhkndrn.ttf | Kannada | 223 |
| 12 | Varnaakshara Malayalam Lipi 01 | brhmal.ttf | Malayalam | 240 |
| 13 | Varnaakshara Malayalam Lipi 02 | brhmale.ttf | Malayalam | 240 |
| 14 | Varnaakshara Malayalam Lipi 03 | brhmalrn.ttf | Malayalam | 240 |
| 15 | Varnaakshara Kannada Lipi 08 | brhsknd.ttf | Kannada | 224 |
| 16 | Varnaakshara Tamil Lipi 01 | brhtab.ttf | Tamil | 256 |
| 17 | Varnaakshara Tamil Lipi 02 | brhtabe.ttf | Tamil | 256 |
| 18 | Varnaakshara Tamil Lipi 03 | brhtabrn.ttf | Tamil | 256 |
| 19 | Varnaakshara Telugu Lipi 01 | brhtel.ttf | Telugu | 254 |
| 20 | Varnaakshara Telugu Lipi 02 | brhtele.ttf | Telugu | 254 |
| 21 | Varnaakshara Telugu Lipi 03 | brhtelrn.ttf | Telugu | 254 |
| 22 | Varnaakshara Kannada Lipi 09 | brhvjy.ttf | Kannada | 224 |

**Skipped:** `brhkndb.ttf` (Kannada Lipi 05) — already Bold variant; weights generated from its Regular sibling `brhknd.ttf`.

---

## Part 2: Shreelipi Font Families (114 families, 570 files)

### Per-Script Breakdown

| Script | Families | Font Files | Source |
|--------|----------|------------|--------|
| Assamese | 6 | 30 | DEFFONTS/ASS, LNGFONTS/ASS |
| Bengali | 17 | 85 | DEFFONTS/BAN, LNGFONTS/BAN |
| Devanagari | 17 | 85 | DEFFONTS/DEV, LNGFONTS/DEV |
| Diacritical | 2 | 10 | DEFFONTS/DIA |
| Gujarati | 7 | 35 | DEFFONTS/GUJ |
| Kannada | 8 | 40 | DEFFONTS/KAN, LNGFONTS/KAN |
| Malayalam | 10 | 50 | DEFFONTS/MAL, LNGFONTS/MAL |
| Odia | 7 | 35 | DEFFONTS/ORI, top-level OTF |
| Punjabi | 5 | 25 | DEFFONTS/PUN |
| Sanskrit | 2 | 10 | DEFFONTS/SAN |
| Sindhi | 1 | 5 | DEFFONTS/SND |
| Tamil | 24 | 120 | DEFFONTS/TAM, LNGFONTS/TAM |
| Telugu | 8 | 40 | DEFFONTS/TEL, LNGFONTS/TEL |
| **Total** | **114** | **570** | |

### Font Selection Rules

1. **Minimum glyphs:** Fonts with < 50 glyphs skipped (6 auxiliary fonts)
2. **Bold/Italic variants:** For families with Bold/Italic siblings, only the Regular weight was used as source (24 variants skipped)
3. **Corrupted fonts:** Arabic (Shree664S.ttf) — corrupted post table; Assamese 05 (Shree-Ass7-001W.TTF) — corrupted cmap table (2 fonts skipped)

### Full Shreelipi Family Inventory

| Family Name | Source Font | Original Name | Script | Glyphs |
|-------------|------------|---------------|--------|--------|
| Varnaakshara Shreelipi Assamese 01 | SHRIM560.TTF | SHREE-ASS-0560M | Assamese | 220 |
| Varnaakshara Shreelipi Assamese 02 | WAss001.TTF | Shree-Ass-001 | Assamese | 221 |
| Varnaakshara Shreelipi Assamese 03 | WAss002.TTF | Shree-Ass-002 | Assamese | 221 |
| Varnaakshara Shreelipi Assamese 04 | WASS7001.TTF | Shree-Ass7-001 | Assamese | 220 |
| Varnaakshara Shreelipi Assamese 06 | WASS7002.TTF | Shree-Ass7-002 | Assamese | 220 |
| Varnaakshara Shreelipi Assamese 07 | Shree-Ass7-002W.TTF | Shree-Ass7-002W | Assamese | 220 |
| Varnaakshara Shreelipi Bengali 01 | SHREM560.TTF | SHREE-BAN-0560M | Bengali | 220 |
| Varnaakshara Shreelipi Bengali 02 | SHRELBT0592.TTF | SHREE-BANT-0592 | Bengali | 217 |
| Varnaakshara Shreelipi Bengali 03 | SHRELBT0592I.TTF | SHREE-BANT-0592 (Italic) | Bengali | 217 |
| Varnaakshara Shreelipi Bengali 04 | SHRELBT0594.TTF | SHREE-BANT-0594 | Bengali | 217 |
| Varnaakshara Shreelipi Bengali 05 | SHRELBT0594I.TTF | SHREE-BANT-0594 (Italic) | Bengali | 217 |
| Varnaakshara Shreelipi Bengali 06 | WBan001.TTF | Shree-Ban-001 | Bengali | 222 |
| Varnaakshara Shreelipi Bengali 07 | WBan002.TTF | Shree-Ban-002 | Bengali | 222 |
| Varnaakshara Shreelipi Bengali 08 | WBAN7001.TTF | Shree-Ban7-001 | Bengali | 222 |
| Varnaakshara Shreelipi Bengali 09 | Shree-Ban7-001W.TTF | Shree-Ban7-001W | Bengali | 222 |
| Varnaakshara Shreelipi Bengali 10 | WBAN7002.TTF | Shree-Ban7-002 | Bengali | 222 |
| Varnaakshara Shreelipi Bengali 11 | Shree-Ban7-002W.TTF | Shree-Ban7-002W | Bengali | 222 |
| Varnaakshara Shreelipi Bengali 12 | Shreb___.ttf | Shreelipi Bangla | Bengali | 214 |
| Varnaakshara Shreelipi Bengali 13 | Shrebb__.ttf | Shreelipi Bangla Bold | Bengali | 214 |
| Varnaakshara Shreelipi Bengali 14 | Shrebl__.ttf | Shreelipi Bangla Lekha | Bengali | 214 |
| Varnaakshara Shreelipi Bengali 15 | SHBTL.TTF | Shreelipi Bangla LekhaT | Bengali | 219 |
| Varnaakshara Shreelipi Bengali 16 | SHBT.TTF | Shreelipi BanglaT | Bengali | 217 |
| Varnaakshara Shreelipi Bengali 17 | SHBTB.TTF | Shreelipi BanglaT Bold | Bengali | 217 |
| Varnaakshara Shreelipi Devanagari 01 | SHRDM708.TTF | DV-SHREE-0708 | Devanagari | 196 |
| Varnaakshara Shreelipi Devanagari 02 | SHRDM709.TTF | DV-SHREE-0709 | Devanagari | 196 |
| Varnaakshara Shreelipi Devanagari 03 | SHRDM714.TTF | DV-SHREE-0714 | Devanagari | 196 |
| Varnaakshara Shreelipi Devanagari 04 | SHRDM715.TTF | DV-SHREE-0715 | Devanagari | 196 |
| Varnaakshara Shreelipi Devanagari 05 | SHDB708.TTF | DVB-SHREE-0708 | Devanagari | 224 |
| Varnaakshara Shreelipi Devanagari 06 | SHDB714.TTF | DVB-SHREE-0714 | Devanagari | 224 |
| Varnaakshara Shreelipi Devanagari 07 | SHREM726.TTF | SHREE-DEV-0726M | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 08 | WDEV001.TTF | Shree-Dev-001 | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 09 | WDEV001E.TTF | Shree-Dev-001E | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 10 | WDEV002.TTF | Shree-Dev-002 | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 11 | WDEV002E.TTF | Shree-Dev-002E | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 12 | WDEV7001.TTF | Shree-Dev7-001 | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 13 | WDEV7001E.TTF | Shree-Dev7-001E | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 14 | Shree-Dev7-001W.TTF | Shree-Dev7-001W | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 15 | WDEV7002.TTF | Shree-Dev7-002 | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 16 | WDEV7002E.TTF | Shree-Dev7-002E | Devanagari | 223 |
| Varnaakshara Shreelipi Devanagari 17 | Shree-Dev7-002W.TTF | Shree-Dev7-002W | Devanagari | 223 |
| Varnaakshara Shreelipi Diacritical 01 | Shree-Dia-1900W.TTF | Shree-Dia-1900W | Diacritical | 223 |
| Varnaakshara Shreelipi Diacritical 02 | Shree-Diai-1900W.TTF | Shree-Diai-1900W | Diacritical | 205 |
| Varnaakshara Shreelipi Gujarati 01 | SHREMB43.TTF | SHREE-GUJ-1143M | Gujarati | 221 |
| Varnaakshara Shreelipi Gujarati 02 | WGUJ001.TTF | Shree-Guj-001 | Gujarati | 222 |
| Varnaakshara Shreelipi Gujarati 03 | WGUJ002.TTF | Shree-Guj-002 | Gujarati | 222 |
| Varnaakshara Shreelipi Gujarati 04 | WGUJ7001.TTF | Shree-Guj7-001 | Gujarati | 222 |
| Varnaakshara Shreelipi Gujarati 05 | Shree-Guj7-001W.TTF | Shree-Guj7-001W | Gujarati | 222 |
| Varnaakshara Shreelipi Gujarati 06 | WGUJ7002.TTF | Shree-Guj7-002 | Gujarati | 222 |
| Varnaakshara Shreelipi Gujarati 07 | Shree-Guj7-002W.TTF | Shree-Guj7-002W | Gujarati | 222 |
| Varnaakshara Shreelipi Kannada 01 | SHREM854.TTF | SHREE-KAN-0854M | Kannada | 218 |
| Varnaakshara Shreelipi Kannada 02 | SHKGP850.ttf | SHREE-SKAN-0850 | Kannada | 179 |
| Varnaakshara Shreelipi Kannada 03 | WKAN001.TTF | Shree-Kan-001 | Kannada | 219 |
| Varnaakshara Shreelipi Kannada 04 | WKAN002.TTF | Shree-Kan-002 | Kannada | 219 |
| Varnaakshara Shreelipi Kannada 05 | WKAN7001.TTF | Shree-Kan7-001 | Kannada | 219 |
| Varnaakshara Shreelipi Kannada 06 | Shree-Kan7-001W.TTF | Shree-Kan7-001W | Kannada | 220 |
| Varnaakshara Shreelipi Kannada 07 | WKAN7002.TTF | Shree-Kan7-002 | Kannada | 219 |
| Varnaakshara Shreelipi Kannada 08 | Shree-Kan7-002W.TTF | Shree-Kan7-002W | Kannada | 220 |
| Varnaakshara Shreelipi Malayalam 01 | SHMB501.TTF | MLB-SHREE-0501 | Malayalam | 220 |
| Varnaakshara Shreelipi Malayalam 02 | SHMB502.TTF | MLB-SHREE-0502 | Malayalam | 220 |
| Varnaakshara Shreelipi Malayalam 03 | SHMB506.TTF | MLB-SHREE-0506 | Malayalam | 220 |
| Varnaakshara Shreelipi Malayalam 04 | Shremw28.ttf | SHREE-MAL-3228M | Malayalam | 174 |
| Varnaakshara Shreelipi Malayalam 05 | WMAL001.TTF | Shree-Mal-001 | Malayalam | 189 |
| Varnaakshara Shreelipi Malayalam 06 | WMAL002.TTF | Shree-Mal-002 | Malayalam | 189 |
| Varnaakshara Shreelipi Malayalam 07 | WMAL7001.TTF | Shree-Mal7-001 | Malayalam | 193 |
| Varnaakshara Shreelipi Malayalam 08 | Shree-Mal7-001W.TTF | Shree-Mal7-001W | Malayalam | 193 |
| Varnaakshara Shreelipi Malayalam 09 | WMAL7002.TTF | Shree-Mal7-002 | Malayalam | 193 |
| Varnaakshara Shreelipi Malayalam 10 | Shree-Mal7-002W.TTF | Shree-Mal7-002W | Malayalam | 193 |
| Varnaakshara Shreelipi Odia 01 | SHREM601.TTF | SHREE-ORI-0601M | Odia | 221 |
| Varnaakshara Shreelipi Odia 02 | SHREE_ORI_OTF_0601 0601 Regular.TTF | SHREE_ORI_OTF_0601 | Odia | 655 |
| Varnaakshara Shreelipi Odia 03 | SHREE_ORI_OTF_0603 0603 Regular.TTF | SHREE_ORI_OTF_0603 | Odia | 655 |
| Varnaakshara Shreelipi Odia 04 | WORI001.TTF | Shree-Ori-001 | Odia | 221 |
| Varnaakshara Shreelipi Odia 05 | WORI002.TTF | Shree-Ori-002 | Odia | 221 |
| Varnaakshara Shreelipi Odia 06 | Shree-Ori7-001W.TTF | Shree-Ori7-001W | Odia | 221 |
| Varnaakshara Shreelipi Odia 07 | Shree-Ori7-002W.TTF | Shree-Ori7-002W | Odia | 221 |
| Varnaakshara Shreelipi Punjabi 01 | SHREM951.TTF | SHREE-PUN-0951M | Punjabi | 119 |
| Varnaakshara Shreelipi Punjabi 02 | WPUN001.TTF | Shree-Pun-001 | Punjabi | 121 |
| Varnaakshara Shreelipi Punjabi 03 | WPUN002.TTF | Shree-Pun-002 | Punjabi | 121 |
| Varnaakshara Shreelipi Punjabi 04 | Shree-Pun7-001W.TTF | Shree-Pun7-001W | Punjabi | 121 |
| Varnaakshara Shreelipi Punjabi 05 | Shree-Pun7-002W.TTF | Shree-Pun7-002W | Punjabi | 121 |
| Varnaakshara Shreelipi Sanskrit 01 | SHREE-SAN7-001W.TTF | Shree-San7-001W | Sanskrit | 219 |
| Varnaakshara Shreelipi Sanskrit 02 | Shree-San7-002W.TTF | Shree-San7-002W | Sanskrit | 219 |
| Varnaakshara Shreelipi Sindhi 01 | Shree680S.ttf | SHREE-SNDS-0680 | Sindhi | 223 |
| Varnaakshara Shreelipi Tamil 01 | WTAM001.TTF | Shree-Tam-001 | Tamil | 215 |
| Varnaakshara Shreelipi Tamil 02 | WTAM002.TTF | Shree-Tam-002 | Tamil | 215 |
| Varnaakshara Shreelipi Tamil 03 | WTAM7001.TTF | Shree-Tam7-001 | Tamil | 218 |
| Varnaakshara Shreelipi Tamil 04 | Shree-Tam7-001W.TTF | Shree-Tam7-001W | Tamil | 218 |
| Varnaakshara Shreelipi Tamil 05 | WTAM7002.TTF | Shree-Tam7-002 | Tamil | 218 |
| Varnaakshara Shreelipi Tamil 06 | Shree-Tam7-002W.TTF | Shree-Tam7-002W | Tamil | 218 |
| Varnaakshara Shreelipi Tamil 07 | BTAM800.TTF | TAB-Shree800 | Tamil | 195 |
| Varnaakshara Shreelipi Tamil 08 | BTAM801.TTF | TAB-Shree801 | Tamil | 195 |
| Varnaakshara Shreelipi Tamil 09 | BTAM802.TTF | TAB-Shree802 | Tamil | 195 |
| Varnaakshara Shreelipi Tamil 10 | BTAM803.TTF | TAB-Shree803 | Tamil | 195 |
| Varnaakshara Shreelipi Tamil 11 | TAC-BarathiX.ttf | TAC-Barathi | Tamil | 447 |
| Varnaakshara Shreelipi Tamil 12 | TAC-KabilarX.ttf | TAC-Kabilar | Tamil | 447 |
| Varnaakshara Shreelipi Tamil 13 | TAC-KambarX.ttf | TAC-Kambar | Tamil | 447 |
| Varnaakshara Shreelipi Tamil 14 | TAC-Kaveri.ttf | TAC-Kaveri | Tamil | 447 |
| Varnaakshara Shreelipi Tamil 15 | TAC-ValluvarX.ttf | TAC-Valluvar | Tamil | 447 |
| Varnaakshara Shreelipi Tamil 16 | TAM0800.TTF | TAM-Shree0800 | Tamil | 219 |
| Varnaakshara Shreelipi Tamil 17 | TAM0801.TTF | TAM-Shree0801 | Tamil | 219 |
| Varnaakshara Shreelipi Tamil 18 | TAM0802.TTF | TAM-Shree0802 | Tamil | 219 |
| Varnaakshara Shreelipi Tamil 19 | TAM0803.TTF | TAM-Shree0803 | Tamil | 219 |
| Varnaakshara Shreelipi Tamil 20 | TAMS81.TTF | TAM-ShreeS81 | Tamil | 219 |
| Varnaakshara Shreelipi Tamil 21 | TSC0800.ttf | TSC_Shree-0800 | Tamil | 225 |
| Varnaakshara Shreelipi Tamil 22 | TSC0801.ttf | TSC_Shree-0801 | Tamil | 225 |
| Varnaakshara Shreelipi Tamil 23 | TSC0802.ttf | TSC_Shree-0802 | Tamil | 225 |
| Varnaakshara Shreelipi Tamil 24 | TSC0803.ttf | TSC_Shree-0803 | Tamil | 225 |
| Varnaakshara Shreelipi Telugu 01 | SHREMG42.TTF | SHREE-TEL-1642M | Telugu | 220 |
| Varnaakshara Shreelipi Telugu 02 | S090016A.TTF | SUCHI-TEL5-0900 | Telugu | 210 |
| Varnaakshara Shreelipi Telugu 03 | WTEL001.TTF | Shree-Tel-001 | Telugu | 220 |
| Varnaakshara Shreelipi Telugu 04 | WTEL002.TTF | Shree-Tel-002 | Telugu | 220 |
| Varnaakshara Shreelipi Telugu 05 | WTEL7001.TTF | Shree-Tel7-001 | Telugu | 220 |
| Varnaakshara Shreelipi Telugu 06 | Shree-Tel7-001W.TTF | Shree-Tel7-001W | Telugu | 220 |
| Varnaakshara Shreelipi Telugu 07 | WTEL7002.TTF | Shree-Tel7-002 | Telugu | 220 |
| Varnaakshara Shreelipi Telugu 08 | Shree-Tel7-002W.TTF | Shree-Tel7-002W | Telugu | 220 |

---

## Skipped Shreelipi Fonts

### Corrupted fonts (2)
| Font | Issue |
|------|-------|
| DEFFONTS/ARA/Shree664S.ttf | Corrupted post table (array index out of range) |
| DEFFONTS/ASS/Shree-Ass7-001W.TTF | Corrupted cmap table format 4 |

### Bold/Italic variants skipped (24)
Used Regular sibling as source instead:
- DVB-SHREE-0708 Bold, DVB-SHREE-0714 Bold (Devanagari)
- SHREE-SKAN-0850 Bold (Kannada)
- SHREE_ORI_OTF_0601 Italic/Bold/Bold Italic, SHREE_ORI_OTF_0603 Italic/Bold/Bold Italic (Odia)
- SHREE-BANT-0592 Italic, SHREE-BANT-0594 Italic (Bengali)
- TAC-Barathi Bold/Italic/BoldItalic (Tamil)
- TAC-Kabilar Bold/Italic/BoldItalic (Tamil)
- TAC-Kambar Bold/Italic/BoldItalic (Tamil)
- TAC-Kaveri Bold/Italic/BoldItalic (Tamil)
- TAC-Valluvar Bold/Italic/BoldItalic (Tamil)

### Auxiliary fonts skipped (6, < 50 glyphs)
- WBAN701T.TTF (16 glyphs), WBAN702T.TTF (16 glyphs)
- WORI01T.TTF (15 glyphs), WORI02T.TTF (15 glyphs)
- WTEL701T.TTF (11 glyphs), WTEL702T.TTF (11 glyphs)

---

## Weight Generation Technique

All weights are generated using **pathops outline expansion** (same technique for both Baraha and Shreelipi):

1. **Regular (w400):** Direct copy from source font, no outline modification
2. **Medium (w500):** Stroke expansion of 10 font units
3. **SemiBold (w600):** Stroke expansion of 20 font units
4. **Bold (w700):** Stroke expansion of 35 font units
5. **Black (w900):** Stroke expansion of 55 font units

Each glyph's outlines are stroked with increasing width and unioned with the original filled shape using `pathops.op(UNION)`. This expands outer contours outward and shrinks inner counters, producing a natural bolding effect. Composite glyphs and empty glyphs are preserved unchanged. Original advance widths are maintained.

---

## Directory Structure

```
core/fonts/generated/
├── brhaknd/                          # Baraha Kannada Lipi 01
│   ├── brhaknd-Regular.ttf
│   ├── brhaknd-Medium.ttf
│   ├── brhaknd-SemiBold.ttf
│   ├── brhaknd-Bold.ttf
│   └── brhaknd-Black.ttf
├── brhben/                           # Baraha Bengali Lipi 01
│   └── ...
├── ... (22 Baraha families)
│
└── shreelipi/
    ├── shreelipi-ass-01/             # Shreelipi Assamese 01
    │   ├── shreelipi-ass-01-Regular.ttf
    │   ├── shreelipi-ass-01-Medium.ttf
    │   ├── shreelipi-ass-01-SemiBold.ttf
    │   ├── shreelipi-ass-01-Bold.ttf
    │   └── shreelipi-ass-01-Black.ttf
    ├── shreelipi-ban-01/             # Shreelipi Bengali 01
    │   └── ...
    ├── ... (114 Shreelipi families)
    └── shreelipi_inventory.json      # Machine-readable inventory
```

---

## Tools

| Tool | Purpose |
|------|---------|
| `tools/generate_font_weights.py` | Generate 5-weight families from Baraha source fonts |
| `tools/generate_shreelipi_weights.py` | Generate 5-weight families from Shreelipi source fonts |
| `tools/rename_fonts.py` | Rename Varnaaksharam → Varnaakshara in all font name tables |
