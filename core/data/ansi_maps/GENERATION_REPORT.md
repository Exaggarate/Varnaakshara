# ANSI Map Generation Report

Generated: 2026-07-27 04:30:47 UTC

Languages: 12

## Baraha BrhCode Maps

| Language | Unicode→ANSI | ANSI→Unicode | Round-trip OK | Issues |
|----------|-------------|-------------|---------------|--------|
| Kannada      |          85 |          85 |            85 |      0 |
| Hindi        |          93 |          93 |            93 |      0 |
| Telugu       |          82 |          82 |            82 |      0 |
| Tamil        |          61 |          61 |            61 |      0 |
| Malayalam    |          84 |          84 |            84 |      0 |
| Marathi      |          93 |          89 |            89 |      4 |
| Sanskrit     |          93 |          93 |            93 |      0 |
| Bengali      |          84 |          84 |            84 |      0 |
| Assamese     |          84 |          84 |            84 |      0 |
| Gujarati     |          78 |          78 |            78 |      0 |
| Punjabi      |          76 |          76 |            76 |      0 |
| Odia         |          78 |          78 |            78 |      0 |

## Shreelipi Maps

| Language | Status | Mappings | Source Table |
|----------|--------|----------|-------------|
| Kannada      | ✅ generated | 61 | 01_shree_kan_0850_to_brh_kannada.json |
| Hindi        | ✅ generated | 56 | 05_shree_dev_0709_to_brh_devanagari.json |
| Telugu       | ⚠️ needs_table | 0 | N/A |
| Tamil        | ⚠️ needs_table | 0 | N/A |
| Malayalam    | ⚠️ needs_table | 0 | N/A |
| Marathi      | ✅ generated | 60 | 05_shree_dev_0709_to_brh_devanagari.json |
| Sanskrit     | ✅ generated | 56 | 05_shree_dev_0709_to_brh_devanagari.json |
| Bengali      | ⚠️ needs_table | 0 | N/A |
| Assamese     | ⚠️ needs_table | 0 | N/A |
| Gujarati     | ⚠️ needs_table | 0 | N/A |
| Punjabi      | ⚠️ needs_table | 0 | N/A |
| Odia         | ⚠️ needs_table | 0 | N/A |

## Detailed Validation

### Kannada

- Forward mappings (Unicode→ANSI): 85
- Reverse mappings (ANSI→Unicode): 85
- Round-trip successes: 85
- Round-trip mismatches: 0

### Hindi

- Forward mappings (Unicode→ANSI): 93
- Reverse mappings (ANSI→Unicode): 93
- Round-trip successes: 93
- Round-trip mismatches: 0

### Telugu

- Forward mappings (Unicode→ANSI): 82
- Reverse mappings (ANSI→Unicode): 82
- Round-trip successes: 82
- Round-trip mismatches: 0

### Tamil

- Forward mappings (Unicode→ANSI): 61
- Reverse mappings (ANSI→Unicode): 61
- Round-trip successes: 61
- Round-trip mismatches: 0

### Malayalam

- Forward mappings (Unicode→ANSI): 84
- Reverse mappings (ANSI→Unicode): 84
- Round-trip successes: 84
- Round-trip mismatches: 0

### Marathi

- Forward mappings (Unicode→ANSI): 93
- Reverse mappings (ANSI→Unicode): 89
- Round-trip successes: 89
- Round-trip mismatches: 4
- Issues (showing up to 10):
  Round-trip mismatch: U+090F (ए) → 'E' → U+090E (ऎ)
  Round-trip mismatch: U+0913 (ओ) → 'O' → U+0912 (ऒ)
  Round-trip mismatch: U+0947 (े) → 'e' → U+0946 (ॆ)
  Round-trip mismatch: U+094B (ो) → 'o' → U+094A (ॊ)

### Sanskrit

- Forward mappings (Unicode→ANSI): 93
- Reverse mappings (ANSI→Unicode): 93
- Round-trip successes: 93
- Round-trip mismatches: 0

### Bengali

- Forward mappings (Unicode→ANSI): 84
- Reverse mappings (ANSI→Unicode): 84
- Round-trip successes: 84
- Round-trip mismatches: 0

### Assamese

- Forward mappings (Unicode→ANSI): 84
- Reverse mappings (ANSI→Unicode): 84
- Round-trip successes: 84
- Round-trip mismatches: 0

### Gujarati

- Forward mappings (Unicode→ANSI): 78
- Reverse mappings (ANSI→Unicode): 78
- Round-trip successes: 78
- Round-trip mismatches: 0

### Punjabi

- Forward mappings (Unicode→ANSI): 76
- Reverse mappings (ANSI→Unicode): 76
- Round-trip successes: 76
- Round-trip mismatches: 0

### Odia

- Forward mappings (Unicode→ANSI): 78
- Reverse mappings (ANSI→Unicode): 78
- Round-trip successes: 78
- Round-trip mismatches: 0

## BrhCode Reference

The Baraha BrhCode scheme uses ASCII characters to represent
Indian script characters. The same ASCII codes are used across
all languages - only the Unicode codepoints differ per script.

### Core mappings:

| Category | Example (Devanagari) | BrhCode |
|----------|---------------------|---------|
| Vowel | अ (U+0905) | A |
| Vowel | आ (U+0906) | Aa |
| Consonant | क (U+0915) | k |
| Consonant | ख (U+0916) | K |
| Matra | ा (U+093E) | a |
| Matra | ि (U+093F) | i |
| Sign | ं (U+0902) | M |
| Sign | ् (U+094D) | \\ |

## File Manifest

### Baraha maps (`core/data/ansi_maps/`)

- `kannada.json`
- `hindi.json`
- `telugu.json`
- `tamil.json`
- `malayalam.json`
- `marathi.json`
- `sanskrit.json`
- `bengali.json`
- `assamese.json`
- `gujarati.json`
- `punjabi.json`
- `odia.json`

### Shreelipi maps (`core/data/ansi_maps/shreelipi/`)

- `shreelipi/kannada.json` ✅
- `shreelipi/hindi.json` ✅
- `shreelipi/telugu.json` ⚠️ placeholder
- `shreelipi/tamil.json` ⚠️ placeholder
- `shreelipi/malayalam.json` ⚠️ placeholder
- `shreelipi/marathi.json` ✅
- `shreelipi/sanskrit.json` ✅
- `shreelipi/bengali.json` ⚠️ placeholder
- `shreelipi/assamese.json` ⚠️ placeholder
- `shreelipi/gujarati.json` ⚠️ placeholder
- `shreelipi/punjabi.json` ⚠️ placeholder
- `shreelipi/odia.json` ⚠️ placeholder

---
*Auto-generated by `generate_all.py`*
