# Shree-Lipi Keyboard Layout Extraction Report

## Source
- **Software:** Shree-Lipi 7.4 DVD
- **Path:** `/tmp/SL74DVD/COMMON/COMPOSE/DEV/`
- **Script:** Devanagari
- **Encoding:** ISCII (IS 13194:1991)

## File Format Analysis

### .DEV Files (406 bytes)
- **Bytes 0x00-0x1F (32 bytes):** Identity mapping — ASCII control codes pass through unchanged
- **Bytes 0x20-0x7F (96 bytes):** Key mapping table — maps ASCII key position to Shree-Lipi internal font character code
- **Bytes 0x80-0x195 (278 bytes):** Compose sequences and extended key data
  - Compose sequences start with marker byte `0x04`
  - Followed by 2-3 character codes
  - Terminated by `0xFF`
  - `0xFF` = unmapped/unused slot

### .IDV Files (501 bytes)
- Same structure as .DEV files but values are **standard ISCII codes** (0xA1-0xFA range)
- This is the **authoritative** source for key→character mapping
- The additional 95 bytes (501 vs 406) provide more compose sequence space
- ISCII codes map directly to Unicode Devanagari via the IS 13194 standard

### Key Layout Structure
Within bytes 0x20-0x7F, the mapping uses ASCII key positions:
- `0x20` = Space
- `0x21-0x2F` = Shifted digits and symbol keys (`!@#$%^&*()` etc.)
- `0x30-0x39` = Digit keys `0-9`
- `0x3A-0x40` = Punctuation/symbol keys (`:;<=>?@`)
- `0x41-0x5A` = Shift+letter keys (`A-Z`)
- `0x5B-0x60` = Bracket/symbol keys (`[\]^_\``)
- `0x61-0x7A` = Normal letter keys (`a-z`)
- `0x7B-0x7F` = Remaining symbols (`{|}~` + DEL)

### Value Interpretation
- `0xFF` = Key not mapped (no output)
- Value == Position = Passthrough (ASCII character output)
- `0xA1-0xFA` = ISCII character code (Devanagari)
- `0x20-0x7E` (non-identity) = ASCII character output (different from key)
- `0x80-0x9F` = Extended/special codes (ZWJ, ZWNJ, etc.)

## Extraction Summary

- **Total layouts found:** 39
- **With .IDV file (ISCII):** 39
- **With .DEV file (internal):** 39
- **With both files:** 39

## ISCII to Unicode Mapping Table (IS 13194:1991 → Devanagari)

| ISCII | Unicode | Character | Name |
|-------|---------|-----------|------|
| 0xA1 | U+0901 | ँ | Chandrabindu (DEVANAGARI SIGN CANDRABINDU) |
| 0xA2 | U+0902 | ं | Anusvar (DEVANAGARI SIGN ANUSVARA) |
| 0xA3 | U+0903 | ः | Visarga (DEVANAGARI SIGN VISARGA) |
| 0xA4 | U+0905 | अ | A (DEVANAGARI LETTER A) |
| 0xA5 | U+0906 | आ | AA (DEVANAGARI LETTER AA) |
| 0xA6 | U+0907 | इ | I (DEVANAGARI LETTER I) |
| 0xA7 | U+0908 | ई | II (DEVANAGARI LETTER II) |
| 0xA8 | U+0909 | उ | U (DEVANAGARI LETTER U) |
| 0xA9 | U+090A | ऊ | UU (DEVANAGARI LETTER UU) |
| 0xAA | U+090B | ऋ | Vocalic R (DEVANAGARI LETTER VOCALIC R) |
| 0xAB | U+090E | ऎ | Short E (DEVANAGARI LETTER SHORT E) |
| 0xAC | U+090F | ए | E (DEVANAGARI LETTER E) |
| 0xAD | U+0910 | ऐ | AI (DEVANAGARI LETTER AI) |
| 0xAE | U+090D | ऍ | Candra E (DEVANAGARI LETTER CANDRA E) |
| 0xAF | U+0912 | ऒ | Short O (DEVANAGARI LETTER SHORT O) |
| 0xB0 | U+0913 | ओ | O (DEVANAGARI LETTER O) |
| 0xB1 | U+0914 | औ | AU (DEVANAGARI LETTER AU) |
| 0xB2 | U+0911 | ऑ | Candra O (DEVANAGARI LETTER CANDRA O) |
| 0xB3 | U+0915 | क | KA (DEVANAGARI LETTER KA) |
| 0xB4 | U+0916 | ख | KHA (DEVANAGARI LETTER KHA) |
| 0xB5 | U+0917 | ग | GA (DEVANAGARI LETTER GA) |
| 0xB6 | U+0918 | घ | GHA (DEVANAGARI LETTER GHA) |
| 0xB7 | U+0919 | ङ | NGA (DEVANAGARI LETTER NGA) |
| 0xB8 | U+091A | च | CHA (DEVANAGARI LETTER CA) |
| 0xB9 | U+091B | छ | CHHA (DEVANAGARI LETTER CHA) |
| 0xBA | U+091C | ज | JA (DEVANAGARI LETTER JA) |
| 0xBB | U+091D | झ | JHA (DEVANAGARI LETTER JHA) |
| 0xBC | U+091E | ञ | NYA (DEVANAGARI LETTER NYA) |
| 0xBD | U+091F | ट | TTA (DEVANAGARI LETTER TTA) |
| 0xBE | U+0920 | ठ | TTHA (DEVANAGARI LETTER TTHA) |
| 0xBF | U+0921 | ड | DDA (DEVANAGARI LETTER DDA) |
| 0xC0 | U+0922 | ढ | DDHA (DEVANAGARI LETTER DDHA) |
| 0xC1 | U+0923 | ण | NNA (DEVANAGARI LETTER NNA) |
| 0xC2 | U+0924 | त | TA (DEVANAGARI LETTER TA) |
| 0xC3 | U+0925 | थ | THA (DEVANAGARI LETTER THA) |
| 0xC4 | U+0926 | द | DA (DEVANAGARI LETTER DA) |
| 0xC5 | U+0927 | ध | DHA (DEVANAGARI LETTER DHA) |
| 0xC6 | U+0928 | न | NA (DEVANAGARI LETTER NA) |
| 0xC7 | U+0929 | ऩ | NNNA (DEVANAGARI LETTER NNNA) |
| 0xC8 | U+092A | प | PA (DEVANAGARI LETTER PA) |
| 0xC9 | U+092B | फ | PHA (DEVANAGARI LETTER PHA) |
| 0xCA | U+092C | ब | BA (DEVANAGARI LETTER BA) |
| 0xCB | U+092D | भ | BHA (DEVANAGARI LETTER BHA) |
| 0xCC | U+092E | म | MA (DEVANAGARI LETTER MA) |
| 0xCD | U+092F | य | YA (DEVANAGARI LETTER YA) |
| 0xCE | U+0930 | र | RA (DEVANAGARI LETTER RA) |
| 0xCF | U+0931 | ऱ | RRA (DEVANAGARI LETTER RRA) |
| 0xD0 | U+0932 | ल | LA (DEVANAGARI LETTER LA) |
| 0xD1 | U+0933 | ळ | LLA (DEVANAGARI LETTER LLA) |
| 0xD2 | U+0934 | ऴ | LLLA (DEVANAGARI LETTER LLLA) |
| 0xD3 | U+0935 | व | VA (DEVANAGARI LETTER VA) |
| 0xD4 | U+0936 | श | SHA (DEVANAGARI LETTER SHA) |
| 0xD5 | U+0937 | ष | SSA (DEVANAGARI LETTER SSA) |
| 0xD6 | U+0938 | स | SA (DEVANAGARI LETTER SA) |
| 0xD7 | U+0939 | ह | HA (DEVANAGARI LETTER HA) |
| 0xD9 | U+093E | ा | Matra AA (DEVANAGARI VOWEL SIGN AA) |
| 0xDA | U+093F | ि | Matra I (DEVANAGARI VOWEL SIGN I) |
| 0xDB | U+0940 | ी | Matra II (DEVANAGARI VOWEL SIGN II) |
| 0xDC | U+0941 | ु | Matra U (DEVANAGARI VOWEL SIGN U) |
| 0xDD | U+0942 | ू | Matra UU (DEVANAGARI VOWEL SIGN UU) |
| 0xDE | U+0943 | ृ | Matra Vocalic R (DEVANAGARI VOWEL SIGN VOCALIC R) |
| 0xDF | U+0944 | ॄ | Matra Vocalic RR (DEVANAGARI VOWEL SIGN VOCALIC RR) |
| 0xE0 | U+0947 | े | Matra E (DEVANAGARI VOWEL SIGN E) |
| 0xE1 | U+0948 | ै | Matra AI (DEVANAGARI VOWEL SIGN AI) |
| 0xE2 | U+0945 | ॅ | Matra Candra E (DEVANAGARI VOWEL SIGN CANDRA E) |
| 0xE3 | U+094A | ॊ | Matra Short O (DEVANAGARI VOWEL SIGN SHORT O) |
| 0xE4 | U+094B | ो | Matra O (DEVANAGARI VOWEL SIGN O) |
| 0xE5 | U+094C | ौ | Matra AU (DEVANAGARI VOWEL SIGN AU) |
| 0xE6 | U+0949 | ॉ | Matra Candra O (DEVANAGARI VOWEL SIGN CANDRA O) |
| 0xE7 | U+094D | ् | Halant (DEVANAGARI SIGN VIRAMA) |
| 0xE8 | U+093C | ़ | Nukta (DEVANAGARI SIGN NUKTA) |
| 0xE9 | U+0964 | । | Danda (DEVANAGARI DANDA) |
| 0xEA | U+0965 | ॥ | Double Danda / Attr (DEVANAGARI DOUBLE DANDA) |
| 0xF1 | U+0966 | ० | Digit 0 (DEVANAGARI DIGIT ZERO) |
| 0xF2 | U+0967 | १ | Digit 1 (DEVANAGARI DIGIT ONE) |
| 0xF3 | U+0968 | २ | Digit 2 (DEVANAGARI DIGIT TWO) |
| 0xF4 | U+0969 | ३ | Digit 3 (DEVANAGARI DIGIT THREE) |
| 0xF5 | U+096A | ४ | Digit 4 (DEVANAGARI DIGIT FOUR) |
| 0xF6 | U+096B | ५ | Digit 5 (DEVANAGARI DIGIT FIVE) |
| 0xF7 | U+096C | ६ | Digit 6 (DEVANAGARI DIGIT SIX) |
| 0xF8 | U+096D | ७ | Digit 7 (DEVANAGARI DIGIT SEVEN) |
| 0xF9 | U+096E | ८ | Digit 8 (DEVANAGARI DIGIT EIGHT) |
| 0xFA | U+096F | ९ | Digit 9 (DEVANAGARI DIGIT NINE) |

## Keyboard Layouts

### ABITR
- **Devanagari key mappings:** 61
- **Files:** ABITR.IDV, ABITR.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| ' | 0xDC | U+0941 | ु | Matra U |
| , | 0xDE | U+0943 | ृ | Matra Vocalic R |
| / | 0xE2 | U+0945 | ॅ | Matra Candra E |
| 0 | 0xD2 | U+0934 | ऴ | LLLA |
| 1 | 0xCB | U+092D | भ | BHA |
| 2 | 0xBB | U+091D | झ | JHA |
| 3 | 0xBA | U+091C | ज | JA |
| 4 | 0xB9 | U+091B | छ | CHHA |
| 5 | 0xB8 | U+091A | च | CHA |
| 6 | 0xD7 | U+0939 | ह | HA |
| 7 | 0xD6 | U+0938 | स | SA |
| 8 | 0xD5 | U+0937 | ष | SSA |
| 9 | 0xB7 | U+0919 | ङ | NGA |
| Shift+; | 0xA6 | U+0907 | इ | I |
| ; | 0xDB | U+0940 | ी | Matra II |
| Shift+, | 0xA9 | U+090A | ऊ | UU |
| = | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0x8C |  |  | ISCII_0x8C |
| Shift+b | 0xC0 | U+0922 | ढ | DDHA |
| Shift+c | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+d | 0x80 |  |  | ISCII_0x80 |
| Shift+j | 0xA4 | U+0905 | अ | A |
| Shift+k | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+l | 0xAC | U+090F | ए | E |
| Shift+m | 0xA8 | U+0909 | उ | U |
| Shift+p | 0x8D | U+200D | ‍ | ZWJ |
| Shift+v | 0xBE | U+0920 | ठ | TTHA |
| [ | 0x8E | U+200C | ‌ | ZWNJ |
| \ | 0xE8 | U+093C | ़ | Nukta |
| ] | 0x8F |  |  | ISCII_0x8F |
| Shift+- | 0x90 |  |  | ISCII_0x90 |
| ` | 0xBC | U+091E | ञ | NYA |
| a | 0xCC | U+092E | म | MA |
| b | 0xBF | U+0921 | ड | DDA |
| c | 0xC5 | U+0927 | ध | DHA |
| d | 0xC6 | U+0928 | न | NA |
| e | 0xC9 | U+092B | फ | PHA |
| f | 0xCF | U+0931 | ऱ | RRA |
| g | 0x83 |  |  | ISCII_0x83 |
| h | 0xB3 | U+0915 | क | KA |
| i | 0xB6 | U+0918 | घ | GHA |
| j | 0xA2 | U+0902 | ं | Anusvar |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xE1 | U+0948 | ै | Matra AI |
| m | 0xDD | U+0942 | ू | Matra UU |
| n | 0xC1 | U+0923 | ण | NNA |
| o | 0xD8 |  |  | UNUSED_D8 |
| p | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| q | 0xCA | U+092C | ब | BA |
| r | 0xCD | U+092F | य | YA |
| s | 0xC2 | U+0924 | त | TA |
| t | 0xD4 | U+0936 | श | SHA |
| u | 0xB5 | U+0917 | ग | GA |
| v | 0xBD | U+091F | ट | TTA |
| w | 0xC8 | U+092A | प | PA |
| x | 0xC4 | U+0926 | द | DA |
| y | 0xB4 | U+0916 | ख | KHA |
| z | 0xC3 | U+0925 | थ | THA |
| Shift+[ | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+` | 0xA3 | U+0903 | ः | Visarga |

**Compose sequences (20):**

- JA + Nukta + NYA → ज़ञ
- Nukta + Nukta → ़़
- Chandrabindu + Danda → ँ।
- RRA + Nukta → ऱ़
- Nukta + RRA → ़ऱ
- Nukta + RRA → ़ऱ
- KA + Nukta + SA → क़स
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + RRA → त़ऱ
- TA + Nukta + TA → त़त
- Nukta + YA → ़य
- Nukta + NA → ़न

### AKRUTI
- **Devanagari key mappings:** 78
- **Files:** AKRUTI.IDV, AKRUTI.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xA3 | U+0903 | ः | Visarga |
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0xB7 | U+0919 | ङ | NGA |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+b | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0xA5 | U+0906 | आ | AA |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0xD4 | U+0936 | श | SHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+n | 0x8F |  |  | ISCII_0x8F |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+v | 0x90 |  |  | ISCII_0x90 |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+x | 0xAC | U+090F | ए | E |
| Shift+y | 0xCB | U+092D | भ | BHA |
| Shift+z | 0xB0 | U+0913 | ओ | O |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| ] | 0x91 |  |  | ISCII_0x91 |
| Shift+6 | 0x92 |  |  | ISCII_0x92 |
| Shift+- | 0xBC | U+091E | ञ | NYA |
| ` | 0xE3 | U+094A | ॊ | Matra Short O |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xA2 | U+0902 | ं | Anusvar |
| c | 0xCC | U+092E | म | MA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD8 |  |  | UNUSED_D8 |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD1 | U+0933 | ळ | LLA |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| x | 0xE1 | U+0948 | ै | Matra AI |
| y | 0xCA | U+092C | ब | BA |
| z | 0xE5 | U+094C | ौ | Matra AU |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xB2 | U+0911 | ऑ | Candra O |
| Shift+] | 0x93 |  |  | ISCII_0x93 |
| Shift+` | 0xAE | U+090D | ऍ | Candra E |

**Compose sequences (20):**

- KA + Nukta + SA → क़स
- TA + Nukta + RRA → त़ऱ
- JA + Nukta + NYA → ज़ञ
- RRA + Nukta → ऱ़
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + TA → त़त
- Nukta + RA → ़र
- Nukta + Nukta → ़़
- Nukta + RRA → ़ऱ
- Chandrabindu + Danda → ँ।
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- Nukta + NA → ़न

### AKSHAR
- **Devanagari key mappings:** 72
- **Files:** AKSHAR.IDV, AKSHAR.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xD6 | U+0938 | स | SA |
| Shift+3 | 0xA3 | U+0903 | ः | Visarga |
| ' | 0xD5 | U+0937 | ष | SSA |
| Shift+9 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+0 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+8 | 0x8B |  |  | ISCII_0x8B |
| Shift+= | 0x8C |  |  | ISCII_0x8C |
| , | 0xAC | U+090F | ए | E |
| . | 0xC1 | U+0923 | ण | NNA |
| / | 0xC5 | U+0927 | ध | DHA |
| Shift+; | 0x8D | U+200D | ‍ | ZWJ |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| = | 0xBD | U+091F | ट | TTA |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0xB6 | U+0918 | घ | GHA |
| Shift+a | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+d | 0x8F |  |  | ISCII_0x8F |
| Shift+e | 0x90 |  |  | ISCII_0x90 |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0xCB | U+092D | भ | BHA |
| Shift+i | 0x91 |  |  | ISCII_0x91 |
| Shift+j | 0x92 |  |  | ISCII_0x92 |
| Shift+k | 0x93 |  |  | ISCII_0x93 |
| Shift+l | 0x94 |  |  | ISCII_0x94 |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x95 |  |  | ISCII_0x95 |
| Shift+p | 0x96 |  |  | ISCII_0x96 |
| Shift+q | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x97 |  |  | ISCII_0x97 |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x98 |  |  | ISCII_0x98 |
| Shift+u | 0x99 |  |  | ISCII_0x99 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0x9A |  |  | ISCII_0x9A |
| Shift+y | 0xD1 | U+0933 | ळ | LLA |
| Shift+z | 0x9B |  |  | ISCII_0x9B |
| [ | 0xB4 | U+0916 | ख | KHA |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0x83 |  |  | ISCII_0x83 |
| z | 0x9C |  |  | ISCII_0x9C |
| Shift+[ | 0x9D |  |  | ISCII_0x9D |
| Shift+] | 0xA9 | U+090A | ऊ | UU |
| Shift+` | 0x9E |  |  | ISCII_0x9E |

**Compose sequences (34):**

- TA + Nukta + RRA → त़ऱ
- DA + Nukta + DHA → द़ध
- Nukta + Nukta → ़़
- RRA + Matra UU → ऱू
- BA + Nukta → ब़
- KA + Nukta + Matra AA → क़ा
- MA + Nukta → म़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- RRA + Nukta → ऱ़
- Nukta + RRA → ़ऱ
- KA + Nukta + SA → क़स
- DA + Nukta + YA → द़य
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- Nukta + RA → ़र
- Chandrabindu + Danda → ँ।
- Nukta + NA → ़न
- TA + Nukta + TA → त़त
- GA + Danda → ग।
- JA + Danda → ज।

### APPLE
- **Devanagari key mappings:** 76
- **Files:** APPLE.IDV, APPLE.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xA3 | U+0903 | ः | Visarga |
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0xB7 | U+0919 | ङ | NGA |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+b | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0x8F |  |  | ISCII_0x8F |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0xD4 | U+0936 | श | SHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+n | 0x90 |  |  | ISCII_0x90 |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+v | 0x91 |  |  | ISCII_0x91 |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+x | 0x80 |  |  | ISCII_0x80 |
| Shift+y | 0xCB | U+092D | भ | BHA |
| Shift+z | 0x92 |  |  | ISCII_0x92 |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| ] | 0x93 |  |  | ISCII_0x93 |
| Shift+- | 0xBC | U+091E | ञ | NYA |
| ` | 0xE8 | U+093C | ़ | Nukta |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xA2 | U+0902 | ं | Anusvar |
| c | 0xCC | U+092E | म | MA |
| d | 0x94 |  |  | ISCII_0x94 |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD8 |  |  | UNUSED_D8 |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD1 | U+0933 | ळ | LLA |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| x | 0x95 |  |  | ISCII_0x95 |
| y | 0xCA | U+092C | ब | BA |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xB2 | U+0911 | ऑ | Candra O |
| Shift+] | 0x96 |  |  | ISCII_0x96 |
| Shift+` | 0x89 |  |  | ISCII_0x89 |

**Compose sequences (22):**

- KA + Nukta + SA → क़स
- TA + Nukta + RRA → त़ऱ
- JA + Nukta + NYA → ज़ञ
- RRA + Nukta → ऱ़
- SSA + Nukta + RRA → ष़ऱ
- KHA + Danda → ख।
- JA + Danda → ज।
- KHA + Danda → ख।
- Chandrabindu + Danda → ँ।
- DDA + Danda → ड।
- GA + Danda → ग।
- PHA + Danda → फ।
- DDHA + Danda → ढ।
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- Nukta + RRA → ़ऱ
- Nukta + RA → ़र
- Nukta + Nukta → ़़
- KA + Danda → क।
- TA + Nukta + TA → त़त
- Nukta + NA → ़न
- Matra Vocalic RR + Danda → ॄ।

### ASTERIX
- **Devanagari key mappings:** 73
- **Files:** ASTERIX.IDV, ASTERIX.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xA3 | U+0903 | ः | Visarga |
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0xB7 | U+0919 | ङ | NGA |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+b | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0xA5 | U+0906 | आ | AA |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0xD4 | U+0936 | श | SHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+v | 0x8F |  |  | ISCII_0x8F |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+y | 0xCB | U+092D | भ | BHA |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| ] | 0x90 |  |  | ISCII_0x90 |
| Shift+6 | 0x91 |  |  | ISCII_0x91 |
| Shift+- | 0xBC | U+091E | ञ | NYA |
| ` | 0xE3 | U+094A | ॊ | Matra Short O |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xA2 | U+0902 | ं | Anusvar |
| c | 0xCC | U+092E | म | MA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD8 |  |  | UNUSED_D8 |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD1 | U+0933 | ळ | LLA |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| y | 0xCA | U+092C | ब | BA |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xAE | U+090D | ऍ | Candra E |
| Shift+] | 0x92 |  |  | ISCII_0x92 |
| Shift+` | 0xAE | U+090D | ऍ | Candra E |

**Compose sequences (19):**

- KA + Nukta + SA → क़स
- TA + Nukta + RRA → त़ऱ
- JA + Nukta + NYA → ज़ञ
- RRA + Nukta → ऱ़
- SSA + Nukta + RRA → ष़ऱ
- Nukta + Nukta → ़़
- DDHA + Danda → ढ।
- Nukta + RRA → ़ऱ
- Chandrabindu + Danda → ँ।
- Matra Vocalic RR + Danda → ॄ।
- GA + Danda → ग।
- DDA + Danda → ड।
- JA + Danda → ज।
- Nukta + YA → ़य
- Nukta + NA → ़न
- PHA + Danda → फ।
- KHA + Danda → ख।
- KA + Danda → क।
- TA + Nukta + TA → त़त

### Akrphone
- **Devanagari key mappings:** 74
- **Files:** Akrphone.idv, Akrphone.dev

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0xB7 | U+0919 | ङ | NGA |
| Shift+= | 0x8E | U+200C | ‌ | ZWNJ |
| - | 0x88 | U+0952 | ॒ | Stress sign |
| Shift+, | 0x80 |  |  | ISCII_0x80 |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8F |  |  | ISCII_0x8F |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0xCB | U+092D | भ | BHA |
| Shift+c | 0xB9 | U+091B | छ | CHHA |
| Shift+d | 0xC5 | U+0927 | ध | DHA |
| Shift+e | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+f | 0xA5 | U+0906 | आ | AA |
| Shift+g | 0xB6 | U+0918 | घ | GHA |
| Shift+h | 0xD6 | U+0938 | स | SA |
| Shift+i | 0xDC | U+0941 | ु | Matra U |
| Shift+j | 0xBB | U+091D | झ | JHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0x90 |  |  | ISCII_0x90 |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+p | 0xC9 | U+092B | फ | PHA |
| Shift+q | 0xA9 | U+090A | ऊ | UU |
| Shift+r | 0x91 |  |  | ISCII_0x91 |
| Shift+s | 0xD5 | U+0937 | ष | SSA |
| Shift+t | 0xC3 | U+0925 | थ | THA |
| Shift+u | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+v | 0x92 |  |  | ISCII_0x92 |
| Shift+w | 0x93 |  |  | ISCII_0x93 |
| Shift+x | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+y | 0x94 |  |  | ISCII_0x94 |
| Shift+z | 0xA7 | U+0908 | ई | II |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+6 | 0x95 |  |  | ISCII_0x95 |
| Shift+- | 0xBC | U+091E | ञ | NYA |
| ` | 0xB0 | U+0913 | ओ | O |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0x96 |  |  | ISCII_0x96 |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| q | 0xA8 | U+0909 | उ | U |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xAC | U+090F | ए | E |
| x | 0xA2 | U+0902 | ं | Anusvar |
| y | 0xCD | U+092F | य | YA |
| z | 0xA6 | U+0907 | इ | I |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xE7 | U+094D | ् | Halant |
| Shift+] | 0x97 |  |  | ISCII_0x97 |
| Shift+` | 0xB1 | U+0914 | औ | AU |

**Compose sequences (19):**

- KA + Nukta + SA → क़स
- TA + Nukta + RRA → त़ऱ
- JA + Nukta + NYA → ज़ञ
- RRA + Nukta → ऱ़
- Vocalic R + Danda → ऋ।
- SSA + Nukta + RRA → ष़ऱ
- DDHA + Danda → ढ।
- RRA + Nukta → ऱ़
- DDA + Danda → ड।
- E + Matra Candra E → एॅ
- Nukta + RA → ़र
- Nukta + RRA → ़ऱ
- Nukta + Nukta → ़़
- Chandrabindu + Danda → ँ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- PHA + Danda → फ।

### BPMK
- **Devanagari key mappings:** 72
- **Files:** BPMK.IDV, BPMK.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| ' | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+= | 0xA2 | U+0902 | ं | Anusvar |
| , | 0xD1 | U+0933 | ळ | LLA |
| - | 0xC0 | U+0922 | ढ | DDHA |
| . | 0xA6 | U+0907 | इ | I |
| / | 0xD2 | U+0934 | ऴ | LLLA |
| 0 | 0xBF | U+0921 | ड | DDA |
| 1 | 0x8B |  |  | ISCII_0x8B |
| 2 | 0xE1 | U+0948 | ै | Matra AI |
| 3 | 0xC5 | U+0927 | ध | DHA |
| 5 | 0xC8 | U+092A | प | PA |
| 6 | 0xC1 | U+0923 | ण | NNA |
| 7 | 0x8C |  |  | ISCII_0x8C |
| 8 | 0xBD | U+091F | ट | TTA |
| 9 | 0xBE | U+0920 | ठ | TTHA |
| Shift+; | 0x8D | U+200D | ‍ | ZWJ |
| ; | 0xD7 | U+0939 | ह | HA |
| Shift+, | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+. | 0xA7 | U+0908 | ई | II |
| Shift+/ | 0xA6 | U+0907 | इ | I |
| Shift+a | 0x8F |  |  | ISCII_0x8F |
| Shift+b | 0x90 |  |  | ISCII_0x90 |
| Shift+d | 0x91 |  |  | ISCII_0x91 |
| Shift+e | 0x92 |  |  | ISCII_0x92 |
| Shift+g | 0x93 |  |  | ISCII_0x93 |
| Shift+h | 0xBB | U+091D | झ | JHA |
| Shift+i | 0x94 |  |  | ISCII_0x94 |
| Shift+j | 0x95 |  |  | ISCII_0x95 |
| Shift+k | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+l | 0xDB | U+0940 | ी | Matra II |
| Shift+n | 0x96 |  |  | ISCII_0x96 |
| Shift+p | 0xA8 | U+0909 | उ | U |
| Shift+q | 0xA9 | U+090A | ऊ | UU |
| Shift+r | 0x97 |  |  | ISCII_0x97 |
| Shift+t | 0x98 |  |  | ISCII_0x98 |
| Shift+u | 0x99 |  |  | ISCII_0x99 |
| Shift+w | 0x9A |  |  | ISCII_0x9A |
| Shift+x | 0x9B |  |  | ISCII_0x9B |
| Shift+y | 0x9C |  |  | ISCII_0x9C |
| Shift+z | 0x84 |  |  | ISCII_0x84 |
| [ | 0x9D |  |  | ISCII_0x9D |
| ] | 0xDD | U+0942 | ू | Matra UU |
| ` | 0xE8 | U+093C | ़ | Nukta |
| a | 0xCA | U+092C | ब | BA |
| b | 0xB4 | U+0916 | ख | KHA |
| c | 0xD8 |  |  | UNUSED_D8 |
| d | 0xCC | U+092E | म | MA |
| e | 0xCB | U+092D | भ | BHA |
| f | 0xDA | U+093F | ि | Matra I |
| g | 0xC6 | U+0928 | न | NA |
| h | 0xBA | U+091C | ज | JA |
| i | 0xCD | U+092F | य | YA |
| j | 0xD4 | U+0936 | श | SHA |
| k | 0xB9 | U+091B | छ | CHHA |
| l | 0xDC | U+0941 | ु | Matra U |
| m | 0xE5 | U+094C | ौ | Matra AU |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xC9 | U+092B | फ | PHA |
| r | 0x9E |  |  | ISCII_0x9E |
| s | 0xB3 | U+0915 | क | KA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xB5 | U+0917 | ग | GA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xB6 | U+0918 | घ | GHA |
| x | 0xD5 | U+0937 | ष | SSA |
| y | 0xC3 | U+0925 | थ | THA |
| z | 0xCF | U+0931 | ऱ | RRA |
| Shift+[ | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+\ | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+] | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+` | 0xEA | U+0965 | ॥ | Double Danda / Attr |

**Compose sequences (28):**

- RRA + Nukta → ऱ़
- Nukta + RRA → ़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- LLA + Nukta → ऴ
- BA + Nukta → ब़
- KHA + Nukta → ख़
- MA + Nukta → म़
- BHA + Nukta → भ़
- NA + Nukta → ऩ
- Nukta + RA → ़र
- SHA + Nukta → श़
- DA + Nukta + Nukta → द़़
- YA + Nukta → य़
- TA + Nukta → त़
- GA + Nukta → ग़
- GHA + Nukta → घ़
- SSA + Nukta → ष़
- THA + Nukta → थ़
- Nukta + Nukta → ़़
- Nukta + RA → ़र
- Matra Vocalic RR + Danda → ॄ।
- Vocalic R + Danda → ऋ।
- Nukta + Nukta → ़़
- TA + Nukta + RRA → त़ऱ
- Chandrabindu + Danda → ँ।
- TA + Nukta + TA → त़त
- Nukta + RRA → ़ऱ

### COMPSET
- **Devanagari key mappings:** 70
- **Files:** COMPSET.IDV, COMPSET.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xD6 | U+0938 | स | SA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+5 | 0xE5 | U+094C | ौ | Matra AU |
| Shift+7 | 0xB4 | U+0916 | ख | KHA |
| ' | 0xD5 | U+0937 | ष | SSA |
| Shift+8 | 0xE6 | U+0949 | ॉ | Matra Candra O |
| / | 0xAC | U+090F | ए | E |
| Shift+; | 0x8B |  |  | ISCII_0x8B |
| ; | 0xD7 | U+0939 | ह | HA |
| Shift+. | 0x8C |  |  | ISCII_0x8C |
| Shift+/ | 0x8D | U+200D | ‍ | ZWJ |
| Shift+2 | 0xC9 | U+092B | फ | PHA |
| Shift+a | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0xC5 | U+0927 | ध | DHA |
| Shift+d | 0x8F |  |  | ISCII_0x8F |
| Shift+e | 0x90 |  |  | ISCII_0x90 |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+h | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+i | 0x91 |  |  | ISCII_0x91 |
| Shift+j | 0xA3 | U+0903 | ः | Visarga |
| Shift+k | 0x92 |  |  | ISCII_0x92 |
| Shift+l | 0x93 |  |  | ISCII_0x93 |
| Shift+m | 0xC0 | U+0922 | ढ | DDHA |
| Shift+n | 0xBF | U+0921 | ड | DDA |
| Shift+o | 0xB9 | U+091B | छ | CHHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0x94 |  |  | ISCII_0x94 |
| Shift+r | 0x95 |  |  | ISCII_0x95 |
| Shift+s | 0x96 |  |  | ISCII_0x96 |
| Shift+t | 0x97 |  |  | ISCII_0x97 |
| Shift+u | 0x98 |  |  | ISCII_0x98 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0x99 |  |  | ISCII_0x99 |
| Shift+x | 0xCB | U+092D | भ | BHA |
| Shift+y | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+z | 0xB6 | U+0918 | घ | GHA |
| [ | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| ] | 0x9A |  |  | ISCII_0x9A |
| Shift+6 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| ` | 0xE8 | U+093C | ़ | Nukta |
| a | 0xB3 | U+0915 | क | KA |
| b | 0xA4 | U+0905 | अ | A |
| c | 0xC4 | U+0926 | द | DA |
| d | 0xD8 |  |  | UNUSED_D8 |
| e | 0xC2 | U+0924 | त | TA |
| f | 0xDC | U+0941 | ु | Matra U |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xDE | U+0943 | ृ | Matra Vocalic R |
| i | 0xD4 | U+0936 | श | SHA |
| j | 0xDA | U+093F | ि | Matra I |
| k | 0xCF | U+0931 | ऱ | RRA |
| l | 0xCD | U+092F | य | YA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xA6 | U+0907 | इ | I |
| o | 0xB8 | U+091A | च | CHA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xCC | U+092E | म | MA |
| r | 0xC6 | U+0928 | न | NA |
| s | 0xDB | U+0940 | ी | Matra II |
| t | 0xA2 | U+0902 | ं | Anusvar |
| u | 0xD1 | U+0933 | ळ | LLA |
| v | 0xC1 | U+0923 | ण | NNA |
| w | 0xC8 | U+092A | प | PA |
| x | 0xCA | U+092C | ब | BA |
| y | 0xE1 | U+0948 | ै | Matra AI |
| z | 0xB5 | U+0917 | ग | GA |
| Shift+[ | 0x9B |  |  | ISCII_0x9B |

**Compose sequences (30):**

- TA + Nukta + RRA → त़ऱ
- HA + Nukta → ह़
- DA + Nukta + DHA → द़ध
- JA + Nukta + NYA → ज़ञ
- KA + Nukta + Matra AA → क़ा
- UNUSED_D8 + Nukta → [0xD8]़
- TA + Nukta → त़
- SHA + Nukta → श़
- Nukta + RRA → ़ऱ
- YA + Nukta → य़
- MA + Nukta → म़
- NA + Nukta → ऩ
- RRA + Nukta → ऱ़
- Nukta + Nukta → ़़
- LLA + Nukta → ऴ
- PA + Nukta → प़
- KA + Nukta + SA → क़स
- SSA + Nukta + RRA → ष़ऱ
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- Nukta + YA → ़य
- Matra Vocalic RR + Danda → ॄ।
- Nukta + NA → ़न
- TA + Nukta + TA → त़त

### COMPSET1
- **Devanagari key mappings:** 71
- **Files:** COMPSET1.IDV, COMPSET1.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+3 | 0x8B |  |  | ISCII_0x8B |
| Shift+4 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+5 | 0xE5 | U+094C | ौ | Matra AU |
| Shift+7 | 0x8C |  |  | ISCII_0x8C |
| ' | 0x8D | U+200D | ‍ | ZWJ |
| Shift+8 | 0xE6 | U+0949 | ॉ | Matra Candra O |
| / | 0xAC | U+090F | ए | E |
| Shift+; | 0x8E | U+200C | ‌ | ZWNJ |
| ; | 0xD7 | U+0939 | ह | HA |
| Shift+. | 0x8F |  |  | ISCII_0x8F |
| Shift+/ | 0x90 |  |  | ISCII_0x90 |
| Shift+2 | 0x91 |  |  | ISCII_0x91 |
| Shift+a | 0x92 |  |  | ISCII_0x92 |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x93 |  |  | ISCII_0x93 |
| Shift+d | 0x94 |  |  | ISCII_0x94 |
| Shift+e | 0x95 |  |  | ISCII_0x95 |
| Shift+f | 0x96 |  |  | ISCII_0x96 |
| Shift+g | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+h | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+i | 0x97 |  |  | ISCII_0x97 |
| Shift+j | 0xA3 | U+0903 | ः | Visarga |
| Shift+k | 0x98 |  |  | ISCII_0x98 |
| Shift+l | 0x99 |  |  | ISCII_0x99 |
| Shift+m | 0xC0 | U+0922 | ढ | DDHA |
| Shift+n | 0xBF | U+0921 | ड | DDA |
| Shift+o | 0xB9 | U+091B | छ | CHHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0x9A |  |  | ISCII_0x9A |
| Shift+r | 0x9B |  |  | ISCII_0x9B |
| Shift+s | 0x9C |  |  | ISCII_0x9C |
| Shift+t | 0x9D |  |  | ISCII_0x9D |
| Shift+u | 0x9E |  |  | ISCII_0x9E |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0x9F |  |  | ISCII_0x9F |
| Shift+x | 0xA0 |  |  | ISCII_0xA0 |
| Shift+y | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+z | 0xEB |  |  | ISCII_0xEB |
| [ | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| ] | 0xEC |  |  | ISCII_0xEC |
| Shift+6 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| ` | 0xE8 | U+093C | ़ | Nukta |
| a | 0xB3 | U+0915 | क | KA |
| b | 0xA4 | U+0905 | अ | A |
| c | 0xC4 | U+0926 | द | DA |
| d | 0xD8 |  |  | UNUSED_D8 |
| e | 0xC2 | U+0924 | त | TA |
| f | 0xDC | U+0941 | ु | Matra U |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xDE | U+0943 | ृ | Matra Vocalic R |
| i | 0xD4 | U+0936 | श | SHA |
| j | 0xDA | U+093F | ि | Matra I |
| k | 0xCF | U+0931 | ऱ | RRA |
| l | 0xCD | U+092F | य | YA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xA6 | U+0907 | इ | I |
| o | 0xED |  |  | ISCII_0xED |
| p | 0xEE |  |  | ISCII_0xEE |
| q | 0xCC | U+092E | म | MA |
| r | 0xC6 | U+0928 | न | NA |
| s | 0xDB | U+0940 | ी | Matra II |
| t | 0xA2 | U+0902 | ं | Anusvar |
| u | 0xD1 | U+0933 | ळ | LLA |
| v | 0xFB |  |  | ISCII_0xFB |
| w | 0xC8 | U+092A | प | PA |
| x | 0xFC |  |  | ISCII_0xFC |
| y | 0xE1 | U+0948 | ै | Matra AI |
| z | 0xFD |  |  | ISCII_0xFD |
| Shift+[ | 0xFE |  |  | ISCII_0xFE |
| Shift+] | 0xA9 | U+090A | ऊ | UU |

**Compose sequences (46):**

- SA + Nukta → स़
- TA + Nukta + RRA → त़ऱ
- KHA + Nukta → ख़
- SSA + Nukta + Matra AA → ष़ा
- HA + Nukta → ह़
- DA + Nukta + DHA → द़ध
- JA + Nukta + NYA → ज़ञ
- PHA + Nukta → फ़
- KA + Nukta + Matra AA → क़ा
- DHA + Nukta → ध़
- UNUSED_D8 + Nukta → [0xD8]़
- TA + Nukta → त़
- THA + Nukta → थ़
- SHA + Nukta → श़
- Nukta + RRA → ़ऱ
- YA + Nukta → य़
- MA + Nukta → म़
- NA + Nukta → ऩ
- RRA + Nukta → ऱ़
- Nukta + Nukta → ़़
- LLA + Nukta → ऴ
- PA + Nukta → प़
- BHA + Nukta → भ़
- GHA + Nukta → घ़
- KA + Nukta + SA + Nukta → क़स़
- CHA + Nukta → च़
- JA + Nukta → ज़
- NNA + Nukta → ण़
- BA + Nukta → ब़
- GA + Nukta → ग़
- SSA + Nukta + RRA → ष़ऱ
- NYA + Nukta → ञ़
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- Nukta + RA → ़र
- Matra Vocalic RR + Danda → ॄ।
- Nukta + NA → ़न
- TA + Nukta + TA → त़त
- Chandrabindu + Danda → ँ।

### CRTRONIC
- **Devanagari key mappings:** 72
- **Files:** CRTRONIC.IDV, CRTRONIC.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xAA | U+090B | ऋ | Vocalic R |
| ' | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| - | 0xC9 | U+092B | फ | PHA |
| . | 0xE6 | U+0949 | ॉ | Matra Candra O |
| 0 | 0xBB | U+091D | झ | JHA |
| 1 | 0xBD | U+091F | ट | TTA |
| 2 | 0xB4 | U+0916 | ख | KHA |
| 3 | 0xC5 | U+0927 | ध | DHA |
| 4 | 0xB9 | U+091B | छ | CHHA |
| 5 | 0xCB | U+092D | भ | BHA |
| 6 | 0xC3 | U+0925 | थ | THA |
| 7 | 0xB6 | U+0918 | घ | GHA |
| 8 | 0xBE | U+0920 | ठ | TTHA |
| 9 | 0xC0 | U+0922 | ढ | DDHA |
| Shift+; | 0xA9 | U+090A | ऊ | UU |
| ; | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+, | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+. | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+b | 0x8B |  |  | ISCII_0x8B |
| Shift+c | 0xA2 | U+0902 | ं | Anusvar |
| Shift+e | 0x80 |  |  | ISCII_0x80 |
| Shift+f | 0xA2 | U+0902 | ं | Anusvar |
| Shift+g | 0xD5 | U+0937 | ष | SSA |
| Shift+h | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+i | 0x8C |  |  | ISCII_0x8C |
| Shift+j | 0x8D | U+200D | ‍ | ZWJ |
| Shift+k | 0xAD | U+0910 | ऐ | AI |
| Shift+l | 0xA7 | U+0908 | ई | II |
| Shift+m | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+n | 0x8F |  |  | ISCII_0x8F |
| Shift+o | 0xA6 | U+0907 | इ | I |
| Shift+p | 0xA8 | U+0909 | उ | U |
| Shift+q | 0x90 |  |  | ISCII_0x90 |
| Shift+t | 0x91 |  |  | ISCII_0x91 |
| Shift+u | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+v | 0x92 |  |  | ISCII_0x92 |
| Shift+w | 0x93 |  |  | ISCII_0x93 |
| Shift+x | 0x94 |  |  | ISCII_0x94 |
| Shift+y | 0x95 |  |  | ISCII_0x95 |
| Shift+z | 0xAC | U+090F | ए | E |
| [ | 0x83 |  |  | ISCII_0x83 |
| \ | 0xE8 | U+093C | ़ | Nukta |
| Shift+- | 0x96 |  |  | ISCII_0x96 |
| ` | 0xBF | U+0921 | ड | DDA |
| a | 0xA4 | U+0905 | अ | A |
| b | 0xCA | U+092C | ब | BA |
| c | 0xBC | U+091E | ञ | NYA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xC6 | U+0928 | न | NA |
| g | 0xC1 | U+0923 | ण | NNA |
| h | 0xCC | U+092E | म | MA |
| i | 0xBA | U+091C | ज | JA |
| j | 0xB5 | U+0917 | ग | GA |
| k | 0xE1 | U+0948 | ै | Matra AI |
| l | 0xDC | U+0941 | ु | Matra U |
| m | 0xE5 | U+094C | ौ | Matra AU |
| n | 0xC8 | U+092A | प | PA |
| o | 0xDB | U+0940 | ी | Matra II |
| p | 0xDD | U+0942 | ू | Matra UU |
| q | 0xD6 | U+0938 | स | SA |
| r | 0xD4 | U+0936 | श | SHA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xCF | U+0931 | ऱ | RRA |
| u | 0xCD | U+092F | य | YA |
| v | 0xB8 | U+091A | च | CHA |
| w | 0xB3 | U+0915 | क | KA |
| x | 0xE2 | U+0945 | ॅ | Matra Candra E |
| y | 0xC2 | U+0924 | त | TA |
| z | 0xD8 |  |  | UNUSED_D8 |
| Shift+\ | 0x89 |  |  | ISCII_0x89 |
| Shift+` | 0xB7 | U+0919 | ङ | NGA |

**Compose sequences (28):**

- RRA + Nukta + Matra U → ऱ़ु
- JA + Nukta + NYA → ज़ञ
- JA + Danda → ज।
- Nukta + RRA → ़ऱ
- RRA + Nukta + Matra AI → ऱ़ै
- Nukta + Nukta → ़़
- KA + Nukta + SA → क़स
- RRA + Nukta → ऱ़
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- RRA + Nukta + Matra Candra E → ऱ़ॅ
- TA + Nukta + TA → त़त
- PHA + Danda → फ।
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KHA + Danda → ख।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- SSA + Nukta + RRA → ष़ऱ
- Matra Candra E + Anusvar → ॅं
- RRA + Nukta + Matra Candra E + Anusvar → ऱ़ॅं
- RRA + Nukta + Matra AI + Anusvar → ऱ़ैं
- TA + Nukta + RRA → त़ऱ
- GA + Danda → ग।
- Matra AI + Anusvar → ैं
- Chandrabindu + Danda → ँ।
- Nukta + NA → ़न
- Nukta + RA → ़र

### DEVYANI
- **Devanagari key mappings:** 81
- **Files:** DEVYANI.IDV, DEVYANI.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+' | 0x8B |  |  | ISCII_0x8B |
| Shift+3 | 0x8C |  |  | ISCII_0x8C |
| Shift+4 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+5 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+7 | 0x8F |  |  | ISCII_0x8F |
| ' | 0xA2 | U+0902 | ं | Anusvar |
| Shift+9 | 0x90 |  |  | ISCII_0x90 |
| Shift+0 | 0x91 |  |  | ISCII_0x91 |
| Shift+8 | 0xBC | U+091E | ञ | NYA |
| Shift+= | 0xA1 | U+0901 | ँ | Chandrabindu |
| - | 0x92 |  |  | ISCII_0x92 |
| / | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+; | 0xE2 | U+0945 | ॅ | Matra Candra E |
| ; | 0xE1 | U+0948 | ै | Matra AI |
| Shift+, | 0xE5 | U+094C | ौ | Matra AU |
| = | 0x93 |  |  | ISCII_0x93 |
| Shift+. | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+2 | 0x94 |  |  | ISCII_0x94 |
| Shift+a | 0x95 |  |  | ISCII_0x95 |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0xA8 | U+0909 | उ | U |
| Shift+d | 0x96 |  |  | ISCII_0x96 |
| Shift+e | 0x97 |  |  | ISCII_0x97 |
| Shift+f | 0x98 |  |  | ISCII_0x98 |
| Shift+g | 0xB4 | U+0916 | ख | KHA |
| Shift+h | 0xB6 | U+0918 | घ | GHA |
| Shift+i | 0xB9 | U+091B | छ | CHHA |
| Shift+j | 0x99 |  |  | ISCII_0x99 |
| Shift+k | 0x9A |  |  | ISCII_0x9A |
| Shift+l | 0xD6 | U+0938 | स | SA |
| Shift+m | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+n | 0xC0 | U+0922 | ढ | DDHA |
| Shift+o | 0xBB | U+091D | झ | JHA |
| Shift+p | 0x9B |  |  | ISCII_0x9B |
| Shift+q | 0xCB | U+092D | भ | BHA |
| Shift+r | 0x9C |  |  | ISCII_0x9C |
| Shift+s | 0x9D |  |  | ISCII_0x9D |
| Shift+t | 0x9E |  |  | ISCII_0x9E |
| Shift+u | 0x9F |  |  | ISCII_0x9F |
| Shift+v | 0xAC | U+090F | ए | E |
| Shift+w | 0xA0 |  |  | ISCII_0xA0 |
| Shift+x | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+y | 0xEB |  |  | ISCII_0xEB |
| Shift+z | 0xC5 | U+0927 | ध | DHA |
| [ | 0xDC | U+0941 | ु | Matra U |
| \ | 0xEC |  |  | ISCII_0xEC |
| ] | 0xDD | U+0942 | ू | Matra UU |
| Shift+6 | 0xB7 | U+0919 | ङ | NGA |
| Shift+- | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| ` | 0xED |  |  | ISCII_0xED |
| a | 0xCC | U+092E | म | MA |
| b | 0xBD | U+091F | ट | TTA |
| c | 0xA4 | U+0905 | अ | A |
| d | 0xC6 | U+0928 | न | NA |
| e | 0xC9 | U+092B | फ | PHA |
| f | 0xB3 | U+0915 | क | KA |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xDA | U+093F | ि | Matra I |
| i | 0xB8 | U+091A | च | CHA |
| j | 0xD8 |  |  | UNUSED_D8 |
| k | 0xD7 | U+0939 | ह | HA |
| l | 0xD5 | U+0937 | ष | SSA |
| m | 0xC1 | U+0923 | ण | NNA |
| n | 0xBF | U+0921 | ड | DDA |
| o | 0xBA | U+091C | ज | JA |
| p | 0xDB | U+0940 | ी | Matra II |
| q | 0xCA | U+092C | ब | BA |
| r | 0xCD | U+092F | य | YA |
| s | 0xC2 | U+0924 | त | TA |
| t | 0xCF | U+0931 | ऱ | RRA |
| u | 0xD4 | U+0936 | श | SHA |
| v | 0xA6 | U+0907 | इ | I |
| w | 0xC8 | U+092A | प | PA |
| x | 0xC3 | U+0925 | थ | THA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xC4 | U+0926 | द | DA |
| Shift+[ | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+\ | 0xEE |  |  | ISCII_0xEE |
| Shift+] | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+` | 0xFB |  |  | ISCII_0xFB |

**Compose sequences (46):**

- TA + Nukta + RRA → त़ऱ
- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- YA + Nukta → य़
- RRA + Matra Vocalic R → ऱृ
- Matra AI + Anusvar → ैं
- SSA + Nukta → ष़
- Chandrabindu + Danda → ँ।
- Nukta + Nukta → ़़
- RRA + Nukta + Anusvar → ऱ़ं
- KA + Nukta + SA → क़स
- MA + Nukta → म़
- NA + Nukta → ऩ
- PHA + Nukta → फ़
- KA + Nukta + Matra AA → क़ा
- UNUSED_D8 + Nukta → [0xD8]़
- HA + Nukta → ह़
- Nukta + RRA → ़ऱ
- Nukta + RA → ़र
- TA + Nukta → त़
- RRA + Nukta → ऱ़
- SHA + Nukta → श़
- PA + Nukta → प़
- LLA + Nukta → ऴ
- Nukta + RRA → ़ऱ
- Nukta + RRA → ़ऱ
- TA + Nukta + RRA + Nukta → त़ऱ़
- TA + Nukta + TA + Nukta → त़त़
- PHA + Danda → फ।
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- DA + Nukta + YA → द़य
- DDHA + Danda → ढ।
- DDA + Nukta + DDA → ड़ड
- Nukta + NA → ़न
- KHA + Danda → ख।
- UNUSED_D8 + Matra Vocalic RR → [0xD8]ॄ
- DA + Nukta + DA → द़द
- DA + Nukta + DHA → द़ध
- SSA + Nukta + RRA → ष़ऱ
- DDA + Nukta + DDHA → ड़ढ
- Nukta + Nukta → ़़

### DEVYANI2
- **Devanagari key mappings:** 68
- **Files:** DEVYANI2.IDV, DEVYANI2.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+3 | 0x8B |  |  | ISCII_0x8B |
| Shift+4 | 0x8C |  |  | ISCII_0x8C |
| Shift+5 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+7 | 0x8E | U+200C | ‌ | ZWNJ |
| ' | 0xA2 | U+0902 | ं | Anusvar |
| Shift+9 | 0x8F |  |  | ISCII_0x8F |
| Shift+0 | 0x90 |  |  | ISCII_0x90 |
| Shift+8 | 0x91 |  |  | ISCII_0x91 |
| Shift+= | 0xA1 | U+0901 | ँ | Chandrabindu |
| - | 0x92 |  |  | ISCII_0x92 |
| / | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+; | 0xE2 | U+0945 | ॅ | Matra Candra E |
| ; | 0xE1 | U+0948 | ै | Matra AI |
| = | 0x93 |  |  | ISCII_0x93 |
| Shift+2 | 0x94 |  |  | ISCII_0x94 |
| Shift+a | 0x95 |  |  | ISCII_0x95 |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0xA8 | U+0909 | उ | U |
| Shift+d | 0x96 |  |  | ISCII_0x96 |
| Shift+e | 0x97 |  |  | ISCII_0x97 |
| Shift+f | 0x98 |  |  | ISCII_0x98 |
| Shift+g | 0x99 |  |  | ISCII_0x99 |
| Shift+h | 0x9A |  |  | ISCII_0x9A |
| Shift+i | 0xB9 | U+091B | छ | CHHA |
| Shift+j | 0x9B |  |  | ISCII_0x9B |
| Shift+k | 0x9C |  |  | ISCII_0x9C |
| Shift+l | 0x9D |  |  | ISCII_0x9D |
| Shift+m | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+n | 0xC0 | U+0922 | ढ | DDHA |
| Shift+o | 0x9E |  |  | ISCII_0x9E |
| Shift+p | 0x9F |  |  | ISCII_0x9F |
| Shift+q | 0xA0 |  |  | ISCII_0xA0 |
| Shift+r | 0xEB |  |  | ISCII_0xEB |
| Shift+s | 0xEC |  |  | ISCII_0xEC |
| Shift+t | 0xED |  |  | ISCII_0xED |
| Shift+u | 0xEE |  |  | ISCII_0xEE |
| Shift+v | 0xAC | U+090F | ए | E |
| Shift+w | 0xFB |  |  | ISCII_0xFB |
| Shift+x | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+y | 0xFC |  |  | ISCII_0xFC |
| Shift+z | 0xFD |  |  | ISCII_0xFD |
| [ | 0xDC | U+0941 | ु | Matra U |
| \ | 0xFE |  |  | ISCII_0xFE |
| ] | 0xDD | U+0942 | ू | Matra UU |
| Shift+6 | 0xB7 | U+0919 | ङ | NGA |
| Shift+- | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| a | 0xCC | U+092E | म | MA |
| b | 0xBD | U+091F | ट | TTA |
| c | 0xA4 | U+0905 | अ | A |
| d | 0xC6 | U+0928 | न | NA |
| e | 0xC9 | U+092B | फ | PHA |
| f | 0xB3 | U+0915 | क | KA |
| h | 0xDA | U+093F | ि | Matra I |
| j | 0xD8 |  |  | UNUSED_D8 |
| k | 0xD7 | U+0939 | ह | HA |
| n | 0xBF | U+0921 | ड | DDA |
| p | 0xDB | U+0940 | ी | Matra II |
| r | 0xCD | U+092F | य | YA |
| s | 0xC2 | U+0924 | त | TA |
| t | 0xCF | U+0931 | ऱ | RRA |
| u | 0xD4 | U+0936 | श | SHA |
| v | 0xA6 | U+0907 | इ | I |
| w | 0xC8 | U+092A | प | PA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xC4 | U+0926 | द | DA |
| Shift+[ | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+] | 0xDE | U+0943 | ृ | Matra Vocalic R |

**Compose sequences (55):**

- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- YA + Nukta → य़
- RRA + Matra Vocalic R → ऱृ
- Matra AI + Anusvar → ैं
- SSA + Nukta → ष़
- Chandrabindu + Danda → ँ।
- NYA + Nukta → ञ़
- Nukta + Nukta → ़़
- RRA + Nukta + Anusvar → ऱ़ं
- KA + Nukta + SA + Nukta → क़स़
- MA + Nukta → म़
- NA + Nukta → ऩ
- PHA + Nukta → फ़
- KA + Nukta + Matra AA → क़ा
- KHA + Nukta → ख़
- GHA + Nukta → घ़
- UNUSED_D8 + Nukta → [0xD8]़
- HA + Nukta → ह़
- SA + Nukta → स़
- JHA + Nukta → झ़
- Nukta + RRA + Nukta → ़ऱ़
- BHA + Nukta → भ़
- Nukta + RA → ़र
- TA + Nukta → त़
- RRA + Nukta → ऱ़
- SHA + Nukta → श़
- PA + Nukta → प़
- LLA + Nukta → ऴ
- DHA + Nukta → ध़
- Nukta + RRA → ़ऱ
- Nukta + RRA → ़ऱ
- GA + Nukta → ग़
- CHA + Nukta → च़
- SSA + Nukta → ष़
- NNA + Nukta → ण़
- JA + Nukta → ज़
- BA + Nukta → ब़
- THA + Nukta → थ़
- Nukta + Matra UU → ़ू
- TA + Nukta + TA + Nukta → त़त़
- Chandrabindu + Danda → ँ।
- RRA + Nukta + Matra AU → ऱ़ौ
- Matra Vocalic RR + Danda → ॄ।
- DA + Nukta + MA → द़म
- DDA + Danda → ड।
- DA + Nukta + YA → द़य
- DDHA + Danda → ढ।
- DDA + Nukta + DDA → ड़ड
- Nukta + NA → ़न
- UNUSED_D8 + Matra Vocalic RR → [0xD8]ॄ
- DA + Nukta + DA → द़द
- DA + Nukta + DHA → द़ध
- SSA + Nukta + RRA → ष़ऱ
- DDA + Nukta + DDHA → ड़ढ

### DOE
- **Devanagari key mappings:** 74
- **Files:** DOE.IDV, DOE.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xAE | U+090D | ऍ | Candra E |
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0xA5 | U+0906 | आ | AA |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0x8F |  |  | ISCII_0x8F |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+n | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xB7 | U+0919 | ङ | NGA |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+x | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+y | 0xCB | U+092D | भ | BHA |
| Shift+z | 0x89 |  |  | ISCII_0x89 |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| ] | 0x90 |  |  | ISCII_0x90 |
| Shift+6 | 0x91 |  |  | ISCII_0x91 |
| Shift+- | 0xA3 | U+0903 | ः | Visarga |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xD4 | U+0936 | श | SHA |
| c | 0xCC | U+092E | म | MA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD1 | U+0933 | ळ | LLA |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD8 |  |  | UNUSED_D8 |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| x | 0xA2 | U+0902 | ं | Anusvar |
| y | 0xCA | U+092C | ब | BA |
| z | 0x92 |  |  | ISCII_0x92 |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xB2 | U+0911 | ऑ | Candra O |
| Shift+] | 0xBC | U+091E | ञ | NYA |

**Compose sequences (19):**

- Nukta + RRA → ़ऱ
- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- KA + Nukta + SA → क़स
- SSA + Nukta + RRA → ष़ऱ
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- TA + Nukta + RRA → त़ऱ
- Nukta + Nukta → ़़
- Matra Vocalic RR + Danda → ॄ।
- GA + Danda → ग।
- JA + Danda → ज।
- PHA + Danda → फ।
- KHA + Danda → ख।
- KA + Danda → क।
- TA + Nukta + TA → त़त
- Chandrabindu + Danda → ँ।
- Nukta + YA → ़य
- Nukta + NA → ़न

### ENG
- **Devanagari key mappings:** 53
- **Files:** ENG.iDV, ENG.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x84 |  |  | ISCII_0x84 |
| Shift+7 | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+, | 0x80 |  |  | ISCII_0x80 |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0x8C |  |  | ISCII_0x8C |
| Shift+d | 0xBF | U+0921 | ड | DDA |
| Shift+e | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+f | 0x8D | U+200D | ‍ | ZWJ |
| Shift+g | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+h | 0xA3 | U+0903 | ः | Visarga |
| Shift+i | 0xA6 | U+0907 | इ | I |
| Shift+j | 0x8F |  |  | ISCII_0x8F |
| Shift+k | 0x90 |  |  | ISCII_0x90 |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE7 | U+094D | ् | Halant |
| Shift+q | 0x89 |  |  | ISCII_0x89 |
| Shift+r | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+s | 0xD6 | U+0938 | स | SA |
| Shift+t | 0xBD | U+091F | ट | TTA |
| Shift+u | 0xA8 | U+0909 | उ | U |
| Shift+x | 0x91 |  |  | ISCII_0x91 |
| Shift+y | 0x92 |  |  | ISCII_0x92 |
| Shift+- | 0xE9 | U+0964 | । | Danda |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0xC9 | U+092B | फ | PHA |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xD4 | U+0936 | श | SHA |
| x | 0x93 |  |  | ISCII_0x93 |
| y | 0xCD | U+092F | य | YA |
| z | 0xBB | U+091D | झ | JHA |

**Compose sequences (15):**

- Nukta + NA → ़न
- Matra Vocalic RR + Danda → ॄ।
- Nukta + NA → ़न
- PHA + Danda → फ।
- GA + Danda → ग।
- JA + Danda → ज।
- KA + Danda → क।
- Nukta + Nukta → ़़
- Nukta + RA → ़र
- KA + Nukta + SA → क़स
- LA + Nukta → ल़
- Chandrabindu + Danda → ँ।
- Nukta + Nukta → ़़
- DDA + Danda → ड।
- Nukta + NA → ़न

### GODREJ
- **Devanagari key mappings:** 67
- **Files:** GODREJ.IDV, GODREJ.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0x86 |  |  | ISCII_0x86 |
| Shift+' | 0xD6 | U+0938 | स | SA |
| ' | 0xD5 | U+0937 | ष | SSA |
| Shift+0 | 0xAA | U+090B | ऋ | Vocalic R |
| , | 0xAC | U+090F | ए | E |
| . | 0xC1 | U+0923 | ण | NNA |
| / | 0xC5 | U+0927 | ध | DHA |
| Shift+; | 0x8A | U+0970 | ॰ | Abbreviation sign |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0xB6 | U+0918 | घ | GHA |
| Shift+a | 0xAD | U+0910 | ऐ | AI |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+d | 0x8B |  |  | ISCII_0x8B |
| Shift+e | 0x8C |  |  | ISCII_0x8C |
| Shift+f | 0x8D | U+200D | ‍ | ZWJ |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0xCB | U+092D | भ | BHA |
| Shift+i | 0xD1 | U+0933 | ळ | LLA |
| Shift+j | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+k | 0x8F |  |  | ISCII_0x8F |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x90 |  |  | ISCII_0x90 |
| Shift+q | 0x91 |  |  | ISCII_0x91 |
| Shift+r | 0x92 |  |  | ISCII_0x92 |
| Shift+s | 0x87 |  |  | ISCII_0x87 |
| Shift+t | 0x93 |  |  | ISCII_0x93 |
| Shift+u | 0x94 |  |  | ISCII_0x94 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xC9 | U+092B | फ | PHA |
| Shift+y | 0xB7 | U+0919 | ङ | NGA |
| Shift+z | 0x95 |  |  | ISCII_0x95 |
| [ | 0xB4 | U+0916 | ख | KHA |
| Shift+- | 0x96 |  |  | ISCII_0x96 |
| ` | 0xE8 | U+093C | ़ | Nukta |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0x83 |  |  | ISCII_0x83 |
| z | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+[ | 0x97 |  |  | ISCII_0x97 |
| Shift+\ | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+] | 0x98 |  |  | ISCII_0x98 |
| Shift+` | 0x99 |  |  | ISCII_0x99 |

**Compose sequences (26):**

- RRA + Matra UU → ऱू
- KA + Danda → क।
- Chandrabindu + Danda → ँ।
- KA + Nukta + SA → क़स
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- TA + Nukta + TA → त़त
- PHA + Matra Short O → फॊ
- TA + Nukta + RRA → त़ऱ
- JA + Danda → ज।
- PHA + Danda + Chandrabindu → फ।ँ
- RRA + Nukta → ऱ़
- Nukta + RRA → ़ऱ
- KA + Nukta + SA + Nukta → क़स़
- RRA + Matra Vocalic R → ऱृ
- Nukta + Nukta → ़़
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- Nukta + RA → ़र
- Matra Candra E + Anusvar → ॅं
- KHA + Danda → ख।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- GA + Danda → ग।
- PHA + Danda → फ।
- Nukta + NA → ़न

### GODREJ1
- **Devanagari key mappings:** 77
- **Files:** GODREJ1.IDV, GODREJ1.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+' | 0xD6 | U+0938 | स | SA |
| Shift+7 | 0x8B |  |  | ISCII_0x8B |
| ' | 0xD5 | U+0937 | ष | SSA |
| Shift+9 | 0x8C |  |  | ISCII_0x8C |
| Shift+0 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+= | 0xA2 | U+0902 | ं | Anusvar |
| , | 0xAC | U+090F | ए | E |
| . | 0xC1 | U+0923 | ण | NNA |
| / | 0xC5 | U+0927 | ध | DHA |
| 1 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+; | 0x8F |  |  | ISCII_0x8F |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| = | 0x90 |  |  | ISCII_0x90 |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0xB6 | U+0918 | घ | GHA |
| Shift+2 | 0xA9 | U+090A | ऊ | UU |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x91 |  |  | ISCII_0x91 |
| Shift+d | 0x92 |  |  | ISCII_0x92 |
| Shift+e | 0x93 |  |  | ISCII_0x93 |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0xCB | U+092D | भ | BHA |
| Shift+i | 0x94 |  |  | ISCII_0x94 |
| Shift+j | 0x95 |  |  | ISCII_0x95 |
| Shift+k | 0x96 |  |  | ISCII_0x96 |
| Shift+l | 0x97 |  |  | ISCII_0x97 |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x98 |  |  | ISCII_0x98 |
| Shift+p | 0x99 |  |  | ISCII_0x99 |
| Shift+q | 0x9A |  |  | ISCII_0x9A |
| Shift+r | 0x9B |  |  | ISCII_0x9B |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x9C |  |  | ISCII_0x9C |
| Shift+u | 0x9D |  |  | ISCII_0x9D |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0x9E |  |  | ISCII_0x9E |
| Shift+y | 0x9F |  |  | ISCII_0x9F |
| Shift+z | 0xA0 |  |  | ISCII_0xA0 |
| [ | 0xB4 | U+0916 | ख | KHA |
| Shift+- | 0xAA | U+090B | ऋ | Vocalic R |
| ` | 0xE8 | U+093C | ़ | Nukta |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+[ | 0xEB |  |  | ISCII_0xEB |
| Shift+\ | 0xEC |  |  | ISCII_0xEC |
| Shift+] | 0xED |  |  | ISCII_0xED |
| Shift+` | 0x89 |  |  | ISCII_0x89 |

**Compose sequences (37):**

- Nukta + Nukta → ़़
- JA + Nukta + NYA → ज़ञ
- DA + Nukta + DHA → द़ध
- TA + Nukta + RRA → त़ऱ
- RRA + Nukta → ऱ़
- RRA + Matra Vocalic R → ऱृ
- Nukta + RRA → ़ऱ
- BA + Nukta → ब़
- KA + Nukta + Matra AA → क़ा
- MA + Nukta → म़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + TA → त़त
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- Chandrabindu + Danda → ँ।
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- KA + Nukta + SA → क़स
- DA + Nukta + YA → द़य
- DA + Nukta + SHA → द़श
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- UNUSED_D8 + Matra Vocalic RR → [0xD8]ॄ
- UNUSED_D8 + Nukta → [0xD8]़
- SSA + Nukta → ष़
- Nukta + YA → ़य
- DDA + Danda → ड।
- PHA + Nukta → फ़
- PHA + Danda → फ।

### INDICA
- **Devanagari key mappings:** 76
- **Files:** INDICA.IDV, INDICA.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xAD | U+0910 | ऐ | AI |
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x83 |  |  | ISCII_0x83 |
| Shift+4 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+5 | 0x8B |  |  | ISCII_0x8B |
| Shift+7 | 0x8C |  |  | ISCII_0x8C |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+b | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0xA5 | U+0906 | आ | AA |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0x8F |  |  | ISCII_0x8F |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+n | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xB7 | U+0919 | ङ | NGA |
| Shift+v | 0x90 |  |  | ISCII_0x90 |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+x | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+y | 0xA9 | U+090A | ऊ | UU |
| Shift+z | 0xB0 | U+0913 | ओ | O |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| Shift+6 | 0x91 |  |  | ISCII_0x91 |
| Shift+- | 0xA3 | U+0903 | ः | Visarga |
| ` | 0xE3 | U+094A | ॊ | Matra Short O |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xD4 | U+0936 | श | SHA |
| c | 0xCC | U+092E | म | MA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD1 | U+0933 | ळ | LLA |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD8 |  |  | UNUSED_D8 |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| x | 0xA2 | U+0902 | ं | Anusvar |
| y | 0xCA | U+092C | ब | BA |
| z | 0xE5 | U+094C | ौ | Matra AU |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xB2 | U+0911 | ऑ | Candra O |
| Shift+] | 0xBC | U+091E | ञ | NYA |
| Shift+` | 0xAE | U+090D | ऍ | Candra E |

**Compose sequences (20):**

- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- KA + Nukta + SA → क़स
- PHA + Danda → फ।
- Nukta + RA → ़र
- Nukta + RRA → ़ऱ
- Nukta + NA → ़न
- TA + Nukta + RRA → त़ऱ
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- Nukta + Nukta → ़़
- Chandrabindu + Danda → ँ।
- DDHA + Danda → ढ।
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + TA → त़त

### ITR
- **Devanagari key mappings:** 65
- **Files:** ITR.IDV, ITR.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xC5 | U+0927 | ध | DHA |
| Shift+4 | 0x88 | U+0952 | ॒ | Stress sign |
| Shift+7 | 0xA3 | U+0903 | ः | Visarga |
| ' | 0xC4 | U+0926 | द | DA |
| Shift+; | 0xC3 | U+0925 | थ | THA |
| ; | 0xC2 | U+0924 | त | TA |
| = | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0xBC | U+091E | ञ | NYA |
| Shift+a | 0xB9 | U+091B | छ | CHHA |
| Shift+b | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+c | 0xCB | U+092D | भ | BHA |
| Shift+d | 0xB6 | U+0918 | घ | GHA |
| Shift+e | 0xB7 | U+0919 | ङ | NGA |
| Shift+f | 0xB4 | U+0916 | ख | KHA |
| Shift+g | 0x8B |  |  | ISCII_0x8B |
| Shift+j | 0xD4 | U+0936 | श | SHA |
| Shift+k | 0xC1 | U+0923 | ण | NNA |
| Shift+l | 0x8C |  |  | ISCII_0x8C |
| Shift+m | 0xD6 | U+0938 | स | SA |
| Shift+n | 0xD5 | U+0937 | ष | SSA |
| Shift+p | 0x8D | U+200D | ‍ | ZWJ |
| Shift+q | 0xA9 | U+090A | ऊ | UU |
| Shift+r | 0xA6 | U+0907 | इ | I |
| Shift+s | 0xBB | U+091D | झ | JHA |
| Shift+t | 0xE8 | U+093C | ़ | Nukta |
| Shift+u | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+v | 0xC9 | U+092B | फ | PHA |
| Shift+w | 0xA8 | U+0909 | उ | U |
| Shift+x | 0xBE | U+0920 | ठ | TTHA |
| Shift+y | 0xAC | U+090F | ए | E |
| Shift+z | 0xC0 | U+0922 | ढ | DDHA |
| [ | 0x8F |  |  | ISCII_0x8F |
| \ | 0x90 |  |  | ISCII_0x90 |
| ] | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+- | 0xA1 | U+0901 | ँ | Chandrabindu |
| a | 0xB8 | U+091A | च | CHA |
| b | 0xCC | U+092E | म | MA |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB5 | U+0917 | ग | GA |
| e | 0xDC | U+0941 | ु | Matra U |
| f | 0xB3 | U+0915 | क | KA |
| g | 0xCD | U+092F | य | YA |
| h | 0xCF | U+0931 | ऱ | RRA |
| i | 0xE2 | U+0945 | ॅ | Matra Candra E |
| j | 0x83 |  |  | ISCII_0x83 |
| k | 0xA2 | U+0902 | ं | Anusvar |
| l | 0xC6 | U+0928 | न | NA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD8 |  |  | UNUSED_D8 |
| o | 0x91 |  |  | ISCII_0x91 |
| p | 0xE3 | U+094A | ॊ | Matra Short O |
| q | 0xDE | U+0943 | ृ | Matra Vocalic R |
| r | 0xDB | U+0940 | ी | Matra II |
| s | 0xBA | U+091C | ज | JA |
| t | 0xDA | U+093F | ि | Matra I |
| u | 0xE1 | U+0948 | ै | Matra AI |
| v | 0xC8 | U+092A | प | PA |
| w | 0xDD | U+0942 | ू | Matra UU |
| x | 0xBD | U+091F | ट | TTA |
| y | 0xA4 | U+0905 | अ | A |
| z | 0xBF | U+0921 | ड | DDA |
| Shift+[ | 0x92 |  |  | ISCII_0x92 |
| Shift+\ | 0x80 |  |  | ISCII_0x80 |
| Shift+] | 0xAA | U+090B | ऋ | Vocalic R |

**Compose sequences (22):**

- Nukta + Nukta → ़़
- KA + Nukta + SA → क़स
- JA + Nukta + NYA → ज़ञ
- NA + Nukta → ऩ
- KA + Nukta + Matra AA → क़ा
- Nukta + RRA → ़ऱ
- Chandrabindu + Danda → ँ।
- RRA + Nukta → ऱ़
- Nukta + RRA → ़ऱ
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + RRA → त़ऱ
- TA + Nukta + TA → त़त
- Nukta + RA → ़र
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- PHA + Danda → फ।

### Inscript
- **Devanagari key mappings:** 79
- **Files:** INSCRIPT.IDV, Inscript.dev

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xAE | U+090D | ऍ | Candra E |
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+/ | 0xCE | U+0930 | र | RA |
| Shift+2 | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+b | 0xD3 | U+0935 | व | VA |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0xA5 | U+0906 | आ | AA |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0xD0 | U+0932 | ल | LA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+n | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xB7 | U+0919 | ङ | NGA |
| Shift+v | 0xC7 | U+0929 | ऩ | NNNA |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+x | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+y | 0xCB | U+092D | भ | BHA |
| Shift+z | 0x8F |  |  | ISCII_0x8F |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| ] | 0xE9 | U+0964 | । | Danda |
| Shift+6 | 0x90 |  |  | ISCII_0x90 |
| Shift+- | 0xA3 | U+0903 | ः | Visarga |
| ` | 0xE4 | U+094B | ो | Matra O |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xD4 | U+0936 | श | SHA |
| c | 0xCC | U+092E | म | MA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD1 | U+0933 | ळ | LLA |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD8 |  |  | UNUSED_D8 |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| x | 0xA2 | U+0902 | ं | Anusvar |
| y | 0xCA | U+092C | ब | BA |
| z | 0xE0 | U+0947 | े | Matra E |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xB2 | U+0911 | ऑ | Candra O |
| Shift+] | 0xBC | U+091E | ञ | NYA |
| Shift+` | 0xAF | U+0912 | ऒ | Short O |

**Compose sequences (7):**

- Nukta + RRA → ़ऱ
- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- KA + Nukta + SA → क़स
- SSA + Nukta + RRA → ष़ऱ
- E + Matra E → एे
- TA + Nukta + RRA → त़ऱ

### K_P_RAO
- **Devanagari key mappings:** 66
- **Files:** K_P_RAO.IDV, K_P_RAO.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x80 |  |  | ISCII_0x80 |
| Shift+7 | 0x8B |  |  | ISCII_0x8B |
| Shift+= | 0x8C |  |  | ISCII_0x8C |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0xCB | U+092D | भ | BHA |
| Shift+c | 0xB9 | U+091B | छ | CHHA |
| Shift+d | 0xC5 | U+0927 | ध | DHA |
| Shift+e | 0x8D | U+200D | ‍ | ZWJ |
| Shift+f | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+g | 0xB6 | U+0918 | घ | GHA |
| Shift+h | 0xA3 | U+0903 | ः | Visarga |
| Shift+i | 0xDC | U+0941 | ु | Matra U |
| Shift+j | 0xBB | U+091D | झ | JHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+p | 0xC9 | U+092B | फ | PHA |
| Shift+q | 0xBE | U+0920 | ठ | TTHA |
| Shift+r | 0x8F |  |  | ISCII_0x8F |
| Shift+s | 0xD5 | U+0937 | ष | SSA |
| Shift+t | 0xC3 | U+0925 | थ | THA |
| Shift+u | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+v | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+w | 0xC0 | U+0922 | ढ | DDHA |
| Shift+x | 0x90 |  |  | ISCII_0x90 |
| Shift+y | 0xAD | U+0910 | ऐ | AI |
| Shift+z | 0xB0 | U+0913 | ओ | O |
| [ | 0x91 |  |  | ISCII_0x91 |
| \ | 0x92 |  |  | ISCII_0x92 |
| ] | 0x93 |  |  | ISCII_0x93 |
| Shift+6 | 0xA6 | U+0907 | इ | I |
| ` | 0xE2 | U+0945 | ॅ | Matra Candra E |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0xE8 | U+093C | ़ | Nukta |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| q | 0xBD | U+091F | ट | TTA |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xBF | U+0921 | ड | DDA |
| x | 0xD6 | U+0938 | स | SA |
| y | 0xCD | U+092F | य | YA |
| z | 0xAC | U+090F | ए | E |
| Shift+[ | 0xA8 | U+0909 | उ | U |
| Shift+\ | 0x94 |  |  | ISCII_0x94 |
| Shift+] | 0xA9 | U+090A | ऊ | UU |
| Shift+` | 0xDF | U+0944 | ॄ | Matra Vocalic RR |

**Compose sequences (22):**

- DDA + Danda → ड।
- Nukta + NA → ़न
- Nukta + RA → ़र
- Nukta + RRA → ़ऱ
- Nukta + Nukta → ़़
- RRA + Nukta → ऱ़
- TA + Nukta + RRA → त़ऱ
- Chandrabindu + Danda → ँ।
- DDHA + Danda → ढ।
- SSA + Nukta + RRA + Matra U → ष़ऱु
- TA + Nukta + TA → त़त
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- PHA + Danda → फ।
- GA + Danda → ग।
- A + Visarga → अः
- JA + Danda → ज।
- JA + Nukta + NYA → ज़ञ
- KA + Nukta + SA → क़स
- SSA + Nukta + RRA → ष़ऱ

### MARATHI
- **Devanagari key mappings:** 65
- **Files:** MARATHI.IDV, MARATHI.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+7 | 0xAA | U+090B | ऋ | Vocalic R |
| ' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+, | 0xAC | U+090F | ए | E |
| Shift+. | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0x8C |  |  | ISCII_0x8C |
| Shift+b | 0xA8 | U+0909 | उ | U |
| Shift+c | 0xBB | U+091D | झ | JHA |
| Shift+d | 0x8D | U+200D | ‍ | ZWJ |
| Shift+e | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0x8F |  |  | ISCII_0x8F |
| Shift+h | 0x90 |  |  | ISCII_0x90 |
| Shift+i | 0xBE | U+0920 | ठ | TTHA |
| Shift+j | 0xC1 | U+0923 | ण | NNA |
| Shift+k | 0xD5 | U+0937 | ष | SSA |
| Shift+l | 0xD6 | U+0938 | स | SA |
| Shift+m | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+n | 0xA9 | U+090A | ऊ | UU |
| Shift+o | 0xBF | U+0921 | ड | DDA |
| Shift+p | 0xC0 | U+0922 | ढ | DDHA |
| Shift+q | 0x91 |  |  | ISCII_0x91 |
| Shift+r | 0xC5 | U+0927 | ध | DHA |
| Shift+s | 0xB4 | U+0916 | ख | KHA |
| Shift+t | 0xA6 | U+0907 | इ | I |
| Shift+u | 0xBD | U+091F | ट | TTA |
| Shift+v | 0xB9 | U+091B | छ | CHHA |
| Shift+w | 0xC9 | U+092B | फ | PHA |
| Shift+x | 0xB6 | U+0918 | घ | GHA |
| Shift+y | 0x92 |  |  | ISCII_0x92 |
| Shift+z | 0xB7 | U+0919 | ङ | NGA |
| [ | 0xA4 | U+0905 | अ | A |
| \ | 0x89 |  |  | ISCII_0x89 |
| ] | 0x93 |  |  | ISCII_0x93 |
| ` | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| a | 0xCC | U+092E | म | MA |
| b | 0xDD | U+0942 | ू | Matra UU |
| c | 0xBA | U+091C | ज | JA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xC6 | U+0928 | न | NA |
| f | 0xC2 | U+0924 | त | TA |
| g | 0xDB | U+0940 | ी | Matra II |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xA2 | U+0902 | ं | Anusvar |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xE1 | U+0948 | ै | Matra AI |
| m | 0x83 |  |  | ISCII_0x83 |
| n | 0xDE | U+0943 | ृ | Matra Vocalic R |
| o | 0xD8 |  |  | UNUSED_D8 |
| p | 0xE2 | U+0945 | ॅ | Matra Candra E |
| q | 0xCA | U+092C | ब | BA |
| r | 0xC4 | U+0926 | द | DA |
| s | 0xB3 | U+0915 | क | KA |
| t | 0xD7 | U+0939 | ह | HA |
| u | 0xCD | U+092F | य | YA |
| v | 0xB8 | U+091A | च | CHA |
| w | 0xC8 | U+092A | प | PA |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD4 | U+0936 | श | SHA |
| z | 0xCB | U+092D | भ | BHA |
| Shift+[ | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+\ | 0xBC | U+091E | ञ | NYA |
| Shift+] | 0x80 |  |  | ISCII_0x80 |
| Shift+` | 0xA3 | U+0903 | ः | Visarga |

**Compose sequences (19):**

- RRA + Nukta → ऱ़
- Nukta + RA → ़र
- JA + Nukta + NYA → ज़ञ
- Nukta + Nukta → ़़
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + RRA → त़ऱ
- KA + Nukta + SA → क़स
- Chandrabindu + Danda → ँ।
- TA + Nukta + TA → त़त
- Nukta + RRA → ़ऱ
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- KHA + Danda → ख।
- KA + Danda → क।
- PHA + Danda → फ।
- GA + Danda → ग।
- JA + Danda → ज।
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।

### MTNK
- **Devanagari key mappings:** 75
- **Files:** MTNK.IDV, MTNK.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+' | 0x8B |  |  | ISCII_0x8B |
| Shift+3 | 0x8C |  |  | ISCII_0x8C |
| Shift+4 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+5 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+7 | 0x8F |  |  | ISCII_0x8F |
| ' | 0xA2 | U+0902 | ं | Anusvar |
| Shift+9 | 0x90 |  |  | ISCII_0x90 |
| Shift+8 | 0xBC | U+091E | ञ | NYA |
| Shift+= | 0xA1 | U+0901 | ँ | Chandrabindu |
| - | 0x89 |  |  | ISCII_0x89 |
| / | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+; | 0xE2 | U+0945 | ॅ | Matra Candra E |
| ; | 0xE1 | U+0948 | ै | Matra AI |
| = | 0x91 |  |  | ISCII_0x91 |
| Shift+2 | 0x92 |  |  | ISCII_0x92 |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0xA8 | U+0909 | उ | U |
| Shift+d | 0xE8 | U+093C | ़ | Nukta |
| Shift+e | 0x93 |  |  | ISCII_0x93 |
| Shift+f | 0x94 |  |  | ISCII_0x94 |
| Shift+g | 0xB4 | U+0916 | ख | KHA |
| Shift+h | 0xB6 | U+0918 | घ | GHA |
| Shift+i | 0xB9 | U+091B | छ | CHHA |
| Shift+j | 0x95 |  |  | ISCII_0x95 |
| Shift+k | 0x96 |  |  | ISCII_0x96 |
| Shift+l | 0xD6 | U+0938 | स | SA |
| Shift+m | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+n | 0xC0 | U+0922 | ढ | DDHA |
| Shift+o | 0xBB | U+091D | झ | JHA |
| Shift+p | 0x97 |  |  | ISCII_0x97 |
| Shift+q | 0xCB | U+092D | भ | BHA |
| Shift+r | 0x98 |  |  | ISCII_0x98 |
| Shift+s | 0x99 |  |  | ISCII_0x99 |
| Shift+t | 0x9A |  |  | ISCII_0x9A |
| Shift+u | 0xAD | U+0910 | ऐ | AI |
| Shift+v | 0xAC | U+090F | ए | E |
| Shift+w | 0x9B |  |  | ISCII_0x9B |
| Shift+x | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+y | 0x9C |  |  | ISCII_0x9C |
| Shift+z | 0xC5 | U+0927 | ध | DHA |
| [ | 0xDC | U+0941 | ु | Matra U |
| ] | 0xDD | U+0942 | ू | Matra UU |
| Shift+6 | 0xB7 | U+0919 | ङ | NGA |
| Shift+- | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| ` | 0x9D |  |  | ISCII_0x9D |
| a | 0xCC | U+092E | म | MA |
| b | 0xBD | U+091F | ट | TTA |
| c | 0xA4 | U+0905 | अ | A |
| d | 0xC6 | U+0928 | न | NA |
| e | 0xC9 | U+092B | फ | PHA |
| f | 0xB3 | U+0915 | क | KA |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xDA | U+093F | ि | Matra I |
| i | 0xB8 | U+091A | च | CHA |
| j | 0xD8 |  |  | UNUSED_D8 |
| k | 0xD7 | U+0939 | ह | HA |
| l | 0xD5 | U+0937 | ष | SSA |
| m | 0xC1 | U+0923 | ण | NNA |
| n | 0xBF | U+0921 | ड | DDA |
| o | 0xBA | U+091C | ज | JA |
| p | 0xDB | U+0940 | ी | Matra II |
| q | 0xCA | U+092C | ब | BA |
| r | 0xCD | U+092F | य | YA |
| s | 0xC2 | U+0924 | त | TA |
| t | 0xCF | U+0931 | ऱ | RRA |
| u | 0xD4 | U+0936 | श | SHA |
| v | 0xA6 | U+0907 | इ | I |
| w | 0xC8 | U+092A | प | PA |
| x | 0xC3 | U+0925 | थ | THA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xC4 | U+0926 | द | DA |
| Shift+[ | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+] | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+` | 0x9E |  |  | ISCII_0x9E |

**Compose sequences (25):**

- TA + Nukta + RRA → त़ऱ
- RRA + Nukta → ऱ़
- SSA + Nukta + RRA → ष़ऱ
- Chandrabindu + Danda → ँ।
- RRA + Matra UU → ऱू
- Matra AU + Anusvar → ौं
- DDHA + Danda → ढ।
- RRA + Nukta + Anusvar → ऱ़ं
- KA + Nukta + SA → क़स
- PHA + Danda → फ।
- KA + Danda → क।
- JA + Danda → ज।
- JA + Nukta + NYA → ज़ञ
- Nukta + RRA → ़ऱ
- Nukta + YA → ़य
- Matra Candra E + Anusvar → ॅं
- GA + Danda → ग।
- KA + Nukta + SA → क़स
- RRA + Matra Vocalic R → ऱृ
- KHA + Danda → ख।
- TA + Nukta + TA → त़त
- Matra Vocalic RR + Danda → ॄ।
- Nukta + Nukta → ़़
- Nukta + NA → ़न
- DDA + Danda → ड।

### NAIDUNIA
- **Devanagari key mappings:** 71
- **Files:** NAIDUNIA.IDV, NAIDUNIA.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+3 | 0xA7 | U+0908 | ई | II |
| Shift+4 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| ' | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+9 | 0x89 |  |  | ISCII_0x89 |
| Shift+= | 0xAC | U+090F | ए | E |
| , | 0x8B |  |  | ISCII_0x8B |
| . | 0xE5 | U+094C | ौ | Matra AU |
| / | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+; | 0xA3 | U+0903 | ः | Visarga |
| ; | 0xD7 | U+0939 | ह | HA |
| Shift+, | 0xA1 | U+0901 | ँ | Chandrabindu |
| = | 0xAD | U+0910 | ऐ | AI |
| Shift+. | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+/ | 0xE7 | U+094D | ् | Halant |
| Shift+a | 0x8C |  |  | ISCII_0x8C |
| Shift+b | 0xBC | U+091E | ञ | NYA |
| Shift+c | 0xBB | U+091D | झ | JHA |
| Shift+d | 0x8D | U+200D | ‍ | ZWJ |
| Shift+e | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0x8F |  |  | ISCII_0x8F |
| Shift+h | 0x90 |  |  | ISCII_0x90 |
| Shift+i | 0xBE | U+0920 | ठ | TTHA |
| Shift+j | 0xC1 | U+0923 | ण | NNA |
| Shift+k | 0xD5 | U+0937 | ष | SSA |
| Shift+l | 0xD6 | U+0938 | स | SA |
| Shift+n | 0x91 |  |  | ISCII_0x91 |
| Shift+o | 0xBF | U+0921 | ड | DDA |
| Shift+p | 0xC0 | U+0922 | ढ | DDHA |
| Shift+q | 0xDB | U+0940 | ी | Matra II |
| Shift+r | 0xC5 | U+0927 | ध | DHA |
| Shift+s | 0xB4 | U+0916 | ख | KHA |
| Shift+t | 0xA6 | U+0907 | इ | I |
| Shift+u | 0xBD | U+091F | ट | TTA |
| Shift+v | 0xB9 | U+091B | छ | CHHA |
| Shift+w | 0xC9 | U+092B | फ | PHA |
| Shift+x | 0xB6 | U+0918 | घ | GHA |
| Shift+y | 0x92 |  |  | ISCII_0x92 |
| Shift+z | 0xB7 | U+0919 | ङ | NGA |
| \ | 0xD2 | U+0934 | ऴ | LLLA |
| ] | 0xA8 | U+0909 | उ | U |
| Shift+- | 0xAA | U+090B | ऋ | Vocalic R |
| a | 0xCC | U+092E | म | MA |
| b | 0xDD | U+0942 | ू | Matra UU |
| c | 0xBA | U+091C | ज | JA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xC6 | U+0928 | न | NA |
| f | 0xC2 | U+0924 | त | TA |
| g | 0xDB | U+0940 | ी | Matra II |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xA2 | U+0902 | ं | Anusvar |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xE1 | U+0948 | ै | Matra AI |
| m | 0xD1 | U+0933 | ळ | LLA |
| n | 0xDE | U+0943 | ृ | Matra Vocalic R |
| o | 0xD8 |  |  | UNUSED_D8 |
| p | 0xE2 | U+0945 | ॅ | Matra Candra E |
| q | 0xCA | U+092C | ब | BA |
| r | 0xC4 | U+0926 | द | DA |
| s | 0xB3 | U+0915 | क | KA |
| t | 0xA4 | U+0905 | अ | A |
| u | 0xCD | U+092F | य | YA |
| v | 0xB8 | U+091A | च | CHA |
| w | 0xC8 | U+092A | प | PA |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD4 | U+0936 | श | SHA |
| z | 0xCB | U+092D | भ | BHA |
| Shift+] | 0xA9 | U+090A | ऊ | UU |
| Shift+` | 0x87 |  |  | ISCII_0x87 |

**Compose sequences (10):**

- Chandrabindu + Danda → ँ।
- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- Nukta + Nukta → ़़
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + RRA → त़ऱ
- KA + Nukta + SA → क़स
- Nukta + NA → ़न
- RRA + Matra UU → ऱू
- Vocalic R + Danda → ऋ।

### NETWORK
- **Devanagari key mappings:** 71
- **Files:** NETWORK.IDV, NETWORK.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| ' | 0x8B |  |  | ISCII_0x8B |
| Shift+0 | 0x8C |  |  | ISCII_0x8C |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| , | 0xAC | U+090F | ए | E |
| . | 0x8D | U+200D | ‍ | ZWJ |
| / | 0x8E | U+200C | ‌ | ZWNJ |
| 2 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+; | 0x8F |  |  | ISCII_0x8F |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0x90 |  |  | ISCII_0x90 |
| Shift+2 | 0x91 |  |  | ISCII_0x91 |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x92 |  |  | ISCII_0x92 |
| Shift+d | 0x93 |  |  | ISCII_0x93 |
| Shift+e | 0x94 |  |  | ISCII_0x94 |
| Shift+f | 0x95 |  |  | ISCII_0x95 |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0x96 |  |  | ISCII_0x96 |
| Shift+i | 0x97 |  |  | ISCII_0x97 |
| Shift+j | 0x98 |  |  | ISCII_0x98 |
| Shift+k | 0x99 |  |  | ISCII_0x99 |
| Shift+l | 0x9A |  |  | ISCII_0x9A |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x9B |  |  | ISCII_0x9B |
| Shift+p | 0x9C |  |  | ISCII_0x9C |
| Shift+q | 0xA9 | U+090A | ऊ | UU |
| Shift+r | 0x9D |  |  | ISCII_0x9D |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x9E |  |  | ISCII_0x9E |
| Shift+u | 0x9F |  |  | ISCII_0x9F |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0xA0 |  |  | ISCII_0xA0 |
| Shift+y | 0xEB |  |  | ISCII_0xEB |
| Shift+z | 0xEC |  |  | ISCII_0xEC |
| [ | 0xED |  |  | ISCII_0xED |
| \ | 0xEE |  |  | ISCII_0xEE |
| Shift+- | 0xFB |  |  | ISCII_0xFB |
| ` | 0xFC |  |  | ISCII_0xFC |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xFD |  |  | ISCII_0xFD |
| Shift+[ | 0xFE |  |  | ISCII_0xFE |

**Compose sequences (46):**

- SA + Nukta → स़
- SSA + Nukta → ष़
- DA + Nukta + DHA → द़ध
- NNA + Nukta → ण़
- DHA + Nukta → ध़
- RRA + Matra Vocalic R → ऱृ
- GHA + Nukta → घ़
- Nukta + Nukta → ़़
- BA + Nukta → ब़
- KA + Nukta + Matra AA → क़ा
- MA + Nukta → म़
- THA + Nukta → थ़
- BHA + Nukta → भ़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- KHA + Nukta → ख़
- Nukta + NA → ़न
- TA + Nukta + RRA → त़ऱ
- Nukta + RRA → ़ऱ
- Nukta + RRA → ़ऱ
- KA + Nukta + SA + Nukta → क़स़
- DA + Nukta + YA → द़य
- DA + Nukta + SHA → द़श
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- UNUSED_D8 + Matra Vocalic RR → [0xD8]ॄ
- UNUSED_D8 + Nukta → [0xD8]़
- SSA + Nukta → ष़
- Nukta + RA → ़र
- DDA + Danda → ड।
- PHA + Nukta → फ़
- PHA + Danda → फ।

### NEWROMA
- **Devanagari key mappings:** 65
- **Files:** NEWROMA.IDV, NEWROMA.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+3 | 0x88 | U+0952 | ॒ | Stress sign |
| Shift+7 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| - | 0x88 | U+0952 | ॒ | Stress sign |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xE8 | U+093C | ़ | Nukta |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0xCB | U+092D | भ | BHA |
| Shift+c | 0xB9 | U+091B | छ | CHHA |
| Shift+d | 0xBF | U+0921 | ड | DDA |
| Shift+e | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+f | 0xC9 | U+092B | फ | PHA |
| Shift+g | 0xB6 | U+0918 | घ | GHA |
| Shift+i | 0xDC | U+0941 | ु | Matra U |
| Shift+j | 0xBB | U+091D | झ | JHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+p | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x8C |  |  | ISCII_0x8C |
| Shift+s | 0xD5 | U+0937 | ष | SSA |
| Shift+t | 0xBD | U+091F | ट | TTA |
| Shift+u | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+v | 0xBC | U+091E | ञ | NYA |
| Shift+w | 0x80 |  |  | ISCII_0x80 |
| Shift+x | 0x8D | U+200D | ‍ | ZWJ |
| Shift+y | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+z | 0x8F |  |  | ISCII_0x8F |
| [ | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| \ | 0x81 |  |  | ISCII_0x81 |
| ] | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+6 | 0x86 |  |  | ISCII_0x86 |
| ` | 0x90 |  |  | ISCII_0x90 |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0x9D |  |  | ISCII_0x9D |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xB7 | U+0919 | ङ | NGA |
| w | 0xD4 | U+0936 | श | SHA |
| x | 0x91 |  |  | ISCII_0x91 |
| y | 0xCD | U+092F | य | YA |
| z | 0x92 |  |  | ISCII_0x92 |
| Shift+[ | 0x93 |  |  | ISCII_0x93 |
| Shift+\ | 0x82 |  |  | ISCII_0x82 |
| Shift+] | 0x83 |  |  | ISCII_0x83 |
| Shift+` | 0x84 |  |  | ISCII_0x84 |

**Compose sequences (20):**

- Nukta + Nukta → ़़
- Chandrabindu + Danda → ँ।
- Vocalic R + Danda → ऋ।
- SSA + Nukta + RRA → ष़ऱ
- Nukta + RA → ़र
- DDHA + Danda → ढ।
- Nukta → ़
- KA + Nukta + SA → क़स
- JA + Nukta + NYA → ज़ञ
- Matra Vocalic RR + Danda → ॄ।
- KHA + Danda → ख।
- Matra Vocalic RR + Danda → ॄ।
- DDA + Danda → ड।
- PHA + Danda → फ।
- JA + Nukta + NYA → ज़ञ
- JA + Danda → ज।
- KA + Danda → क।
- GA + Danda → ग।
- Nukta + NA → ़न
- Nukta + Matra AA → ़ा

### PHONET86
- **Devanagari key mappings:** 78
- **Files:** PHONET86.IDV, PHONET86.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xBE | U+0920 | ठ | TTHA |
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0x8C |  |  | ISCII_0x8C |
| Shift+7 | 0x8D | U+200D | ‍ | ZWJ |
| ' | 0xBD | U+091F | ट | TTA |
| Shift+8 | 0xB7 | U+0919 | ङ | NGA |
| Shift+= | 0x8E | U+200C | ‌ | ZWNJ |
| / | 0xCD | U+092F | य | YA |
| Shift+; | 0xB9 | U+091B | छ | CHHA |
| ; | 0xB8 | U+091A | च | CHA |
| Shift+, | 0xD6 | U+0938 | स | SA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+/ | 0x8F |  |  | ISCII_0x8F |
| Shift+2 | 0x90 |  |  | ISCII_0x90 |
| Shift+a | 0xB0 | U+0913 | ओ | O |
| Shift+b | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+c | 0xC1 | U+0923 | ण | NNA |
| Shift+d | 0xA4 | U+0905 | अ | A |
| Shift+e | 0xA5 | U+0906 | आ | AA |
| Shift+f | 0xA6 | U+0907 | इ | I |
| Shift+g | 0xA8 | U+0909 | उ | U |
| Shift+h | 0xC9 | U+092B | फ | PHA |
| Shift+i | 0xB6 | U+0918 | घ | GHA |
| Shift+j | 0xD4 | U+0936 | श | SHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xC3 | U+0925 | थ | THA |
| Shift+m | 0xD5 | U+0937 | ष | SSA |
| Shift+n | 0x91 |  |  | ISCII_0x91 |
| Shift+o | 0xC5 | U+0927 | ध | DHA |
| Shift+p | 0xBB | U+091D | झ | JHA |
| Shift+q | 0xB1 | U+0914 | औ | AU |
| Shift+r | 0xA7 | U+0908 | ई | II |
| Shift+s | 0xAC | U+090F | ए | E |
| Shift+t | 0xA9 | U+090A | ऊ | UU |
| Shift+u | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+v | 0x80 |  |  | ISCII_0x80 |
| Shift+w | 0xAD | U+0910 | ऐ | AI |
| Shift+x | 0x92 |  |  | ISCII_0x92 |
| Shift+y | 0xCB | U+092D | भ | BHA |
| Shift+z | 0x93 |  |  | ISCII_0x93 |
| [ | 0xBF | U+0921 | ड | DDA |
| \ | 0xE7 | U+094D | ् | Halant |
| ] | 0xE9 | U+0964 | । | Danda |
| Shift+6 | 0x94 |  |  | ISCII_0x94 |
| Shift+- | 0xBC | U+091E | ञ | NYA |
| ` | 0xE3 | U+094A | ॊ | Matra Short O |
| a | 0xE5 | U+094C | ौ | Matra AU |
| b | 0xA2 | U+0902 | ं | Anusvar |
| c | 0xCC | U+092E | म | MA |
| d | 0xE8 | U+093C | ़ | Nukta |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xDD | U+0942 | ू | Matra UU |
| h | 0xC8 | U+092A | प | PA |
| i | 0xB5 | U+0917 | ग | GA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xC2 | U+0924 | त | TA |
| m | 0xD7 | U+0939 | ह | HA |
| n | 0xD8 |  |  | UNUSED_D8 |
| o | 0xC4 | U+0926 | द | DA |
| p | 0xBA | U+091C | ज | JA |
| q | 0xE6 | U+0949 | ॉ | Matra Candra O |
| r | 0xDC | U+0941 | ु | Matra U |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xDE | U+0943 | ृ | Matra Vocalic R |
| u | 0xD1 | U+0933 | ळ | LLA |
| v | 0xC6 | U+0928 | न | NA |
| w | 0xE2 | U+0945 | ॅ | Matra Candra E |
| x | 0x95 |  |  | ISCII_0x95 |
| y | 0xCA | U+092C | ब | BA |
| z | 0x96 |  |  | ISCII_0x96 |
| Shift+[ | 0xC0 | U+0922 | ढ | DDHA |
| Shift+\ | 0xB2 | U+0911 | ऑ | Candra O |
| Shift+] | 0x97 |  |  | ISCII_0x97 |
| Shift+` | 0xAE | U+090D | ऍ | Candra E |

**Compose sequences (15):**

- KA + Nukta + SA → क़स
- TA + Nukta + RRA → त़ऱ
- JA + Nukta + NYA → ज़ञ
- RRA + Nukta → ऱ़
- Vocalic R + Danda → ऋ।
- Nukta + RA → ़र
- SSA + Nukta + RRA → ष़ऱ
- RRA + Nukta → ऱ़
- DDHA + Danda → ढ।
- JA + Danda → ज।
- Nukta + RRA → ़ऱ
- DDA + Danda → ड।
- KA + Danda → क।
- Chandrabindu + Danda → ँ।
- Nukta + Nukta → ़़

### PHONETIC
- **Devanagari key mappings:** 53
- **Files:** PHONETIC.IDV, PHONETIC.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x84 |  |  | ISCII_0x84 |
| Shift+7 | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+, | 0x80 |  |  | ISCII_0x80 |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+2 | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0x8C |  |  | ISCII_0x8C |
| Shift+d | 0xBF | U+0921 | ड | DDA |
| Shift+e | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+f | 0x8D | U+200D | ‍ | ZWJ |
| Shift+g | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+h | 0xA3 | U+0903 | ः | Visarga |
| Shift+i | 0xA6 | U+0907 | इ | I |
| Shift+j | 0x8F |  |  | ISCII_0x8F |
| Shift+k | 0x90 |  |  | ISCII_0x90 |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE7 | U+094D | ् | Halant |
| Shift+q | 0x89 |  |  | ISCII_0x89 |
| Shift+r | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+s | 0xD6 | U+0938 | स | SA |
| Shift+t | 0xBD | U+091F | ट | TTA |
| Shift+u | 0xA8 | U+0909 | उ | U |
| Shift+x | 0x91 |  |  | ISCII_0x91 |
| Shift+y | 0x92 |  |  | ISCII_0x92 |
| Shift+- | 0xE9 | U+0964 | । | Danda |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0xC9 | U+092B | फ | PHA |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xD4 | U+0936 | श | SHA |
| x | 0x93 |  |  | ISCII_0x93 |
| y | 0xCD | U+092F | य | YA |
| z | 0xBB | U+091D | झ | JHA |

**Compose sequences (15):**

- Nukta + NA → ़न
- Matra Vocalic RR + Danda → ॄ।
- Nukta + NA → ़न
- PHA + Danda → फ।
- GA + Danda → ग।
- JA + Danda → ज।
- KA + Danda → क।
- Nukta + Nukta → ़़
- Nukta + RA → ़र
- KA + Nukta + SA → क़स
- LA + Nukta → ल़
- Chandrabindu + Danda → ँ।
- Nukta + Nukta → ़़
- DDHA + Danda → ढ।
- Nukta + NA → ़न

### RAJYA
- **Devanagari key mappings:** 71
- **Files:** RAJYA.IDV, RAJYA.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+7 | 0x88 | U+0952 | ॒ | Stress sign |
| ' | 0x8B |  |  | ISCII_0x8B |
| Shift+0 | 0x8C |  |  | ISCII_0x8C |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| , | 0xAC | U+090F | ए | E |
| . | 0x8D | U+200D | ‍ | ZWJ |
| / | 0x8E | U+200C | ‌ | ZWNJ |
| 2 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+; | 0x8F |  |  | ISCII_0x8F |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0x90 |  |  | ISCII_0x90 |
| Shift+2 | 0x91 |  |  | ISCII_0x91 |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x92 |  |  | ISCII_0x92 |
| Shift+d | 0x93 |  |  | ISCII_0x93 |
| Shift+e | 0x94 |  |  | ISCII_0x94 |
| Shift+f | 0x95 |  |  | ISCII_0x95 |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0x96 |  |  | ISCII_0x96 |
| Shift+i | 0x97 |  |  | ISCII_0x97 |
| Shift+j | 0x98 |  |  | ISCII_0x98 |
| Shift+k | 0x99 |  |  | ISCII_0x99 |
| Shift+l | 0x9A |  |  | ISCII_0x9A |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x9B |  |  | ISCII_0x9B |
| Shift+p | 0x9C |  |  | ISCII_0x9C |
| Shift+q | 0x9D |  |  | ISCII_0x9D |
| Shift+r | 0x9E |  |  | ISCII_0x9E |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x9F |  |  | ISCII_0x9F |
| Shift+u | 0xA0 |  |  | ISCII_0xA0 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0xEB |  |  | ISCII_0xEB |
| Shift+y | 0xEC |  |  | ISCII_0xEC |
| Shift+z | 0xED |  |  | ISCII_0xED |
| [ | 0xEE |  |  | ISCII_0xEE |
| \ | 0xFB |  |  | ISCII_0xFB |
| Shift+- | 0xFC |  |  | ISCII_0xFC |
| ` | 0xFD |  |  | ISCII_0xFD |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xFE |  |  | ISCII_0xFE |

**Compose sequences (49):**

- SA + Nukta → स़
- SSA + Nukta → ष़
- DA + Nukta + DHA → द़ध
- NNA + Nukta → ण़
- DHA + Nukta → ध़
- RRA + Matra Vocalic R → ऱृ
- GHA + Nukta → घ़
- Nukta + Nukta → ़़
- BA + Nukta → ब़
- KA + Nukta + Matra AA → क़ा
- MA + Nukta → म़
- THA + Nukta → थ़
- BHA + Nukta → भ़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- DA + Nukta + DHA → द़ध
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- KHA + Nukta → ख़
- Nukta + NA → ़न
- TA + Nukta + RRA → त़ऱ
- Nukta + RRA → ़ऱ
- Nukta + RRA → ़ऱ
- KA + Nukta + SA + Nukta → क़स़
- DA + Nukta + YA → द़य
- DA + Nukta + SHA → द़श
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- Chandrabindu + Danda → ँ।
- DDHA + Danda → ढ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- UNUSED_D8 + Matra Vocalic RR → [0xD8]ॄ
- UNUSED_D8 + Nukta → [0xD8]़
- SSA + Nukta → ष़
- Nukta + RA → ़र
- DDA + Danda → ड।
- PHA + Nukta → फ़
- PHA + Danda → फ।

### RAMING
- **Devanagari key mappings:** 68
- **Files:** RAMING.IDV, RAMING.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+' | 0xD6 | U+0938 | स | SA |
| Shift+3 | 0x80 |  |  | ISCII_0x80 |
| ' | 0xD5 | U+0937 | ष | SSA |
| Shift+= | 0xAA | U+090B | ऋ | Vocalic R |
| , | 0xC1 | U+0923 | ण | NNA |
| . | 0xC5 | U+0927 | ध | DHA |
| 1 | 0x8B |  |  | ISCII_0x8B |
| 2 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+; | 0x8C |  |  | ISCII_0x8C |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xBB | U+091D | झ | JHA |
| Shift+. | 0xB6 | U+0918 | घ | GHA |
| Shift+/ | 0x8D | U+200D | ‍ | ZWJ |
| Shift+2 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+a | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+b | 0xB9 | U+091B | छ | CHHA |
| Shift+c | 0xBD | U+091F | ट | TTA |
| Shift+d | 0x8F |  |  | ISCII_0x8F |
| Shift+e | 0xA9 | U+090A | ऊ | UU |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0xCB | U+092D | भ | BHA |
| Shift+i | 0x90 |  |  | ISCII_0x90 |
| Shift+j | 0x91 |  |  | ISCII_0x91 |
| Shift+k | 0x92 |  |  | ISCII_0x92 |
| Shift+m | 0xC0 | U+0922 | ढ | DDHA |
| Shift+n | 0xBF | U+0921 | ड | DDA |
| Shift+o | 0xA3 | U+0903 | ः | Visarga |
| Shift+q | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x93 |  |  | ISCII_0x93 |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+v | 0xBE | U+0920 | ठ | TTHA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0xBC | U+091E | ञ | NYA |
| Shift+y | 0x83 |  |  | ISCII_0x83 |
| Shift+z | 0xB7 | U+0919 | ङ | NGA |
| [ | 0xB4 | U+0916 | ख | KHA |
| \ | 0xE8 | U+093C | ़ | Nukta |
| Shift+- | 0x94 |  |  | ISCII_0x94 |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xC4 | U+0926 | द | DA |
| c | 0xA4 | U+0905 | अ | A |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xAC | U+090F | ए | E |
| n | 0xA8 | U+0909 | उ | U |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA6 | U+0907 | इ | I |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xCA | U+092C | ब | BA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xB5 | U+0917 | ग | GA |
| Shift+\ | 0x95 |  |  | ISCII_0x95 |
| Shift+] | 0x89 |  |  | ISCII_0x89 |

**Compose sequences (20):**

- Nukta + RRA → ़ऱ
- Matra Vocalic RR + Danda → ॄ।
- KA + Nukta + SA → क़स
- Nukta + YA → ़य
- Nukta + Nukta → ़़
- KA + Danda → क।
- Chandrabindu + Danda → ँ।
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- TA + Nukta + TA → त़त
- TA + Nukta + RRA → त़ऱ
- RRA + Nukta → ऱ़
- Matra Vocalic RR + Danda → ॄ।
- PHA + Danda → फ।
- DDHA + Danda → ढ।
- KHA + Danda → ख।
- Nukta + NA → ़न
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।

### RAMING2
- **Devanagari key mappings:** 74
- **Files:** RAMING2.IDV, RAMING2.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+' | 0xD6 | U+0938 | स | SA |
| ' | 0xD5 | U+0937 | ष | SSA |
| Shift+9 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+0 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+8 | 0x8B |  |  | ISCII_0x8B |
| Shift+= | 0x8C |  |  | ISCII_0x8C |
| , | 0xAC | U+090F | ए | E |
| . | 0xC1 | U+0923 | ण | NNA |
| / | 0xB6 | U+0918 | घ | GHA |
| Shift+; | 0x8D | U+200D | ‍ | ZWJ |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0xC5 | U+0927 | ध | DHA |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+d | 0x8F |  |  | ISCII_0x8F |
| Shift+e | 0x90 |  |  | ISCII_0x90 |
| Shift+f | 0xC3 | U+0925 | थ | THA |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0xCB | U+092D | भ | BHA |
| Shift+i | 0x91 |  |  | ISCII_0x91 |
| Shift+j | 0x92 |  |  | ISCII_0x92 |
| Shift+k | 0x93 |  |  | ISCII_0x93 |
| Shift+l | 0x94 |  |  | ISCII_0x94 |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x95 |  |  | ISCII_0x95 |
| Shift+p | 0x96 |  |  | ISCII_0x96 |
| Shift+q | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x97 |  |  | ISCII_0x97 |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x98 |  |  | ISCII_0x98 |
| Shift+u | 0x99 |  |  | ISCII_0x99 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0x9A |  |  | ISCII_0x9A |
| Shift+y | 0x9B |  |  | ISCII_0x9B |
| Shift+z | 0x9C |  |  | ISCII_0x9C |
| [ | 0xB4 | U+0916 | ख | KHA |
| \ | 0xE8 | U+093C | ़ | Nukta |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0x9D |  |  | ISCII_0x9D |
| Shift+[ | 0x9E |  |  | ISCII_0x9E |
| Shift+\ | 0x89 |  |  | ISCII_0x89 |
| Shift+] | 0x9F |  |  | ISCII_0x9F |
| Shift+` | 0xA0 |  |  | ISCII_0xA0 |

**Compose sequences (35):**

- TA + Nukta + RRA → त़ऱ
- DA + Nukta + SHA → द़श
- Nukta + Nukta → ़़
- RRA + Matra Vocalic R → ऱृ
- BA + Nukta → ब़
- KA + Nukta → क़
- MA + Nukta → म़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- Nukta + RRA → ़ऱ
- KA + Nukta + SA → क़स
- DA + Nukta + BA → द़ब
- DA + Nukta + YA → द़य
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- Nukta + Nukta → ़़
- Chandrabindu + Danda → ँ।
- TA + Nukta + TA → त़त
- Nukta + RA → ़र
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- PHA + Danda → फ।
- DDA + Danda → ड।

### ROMA
- **Devanagari key mappings:** 66
- **Files:** ROMA.IDV, ROMA.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+3 | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+4 | 0x84 |  |  | ISCII_0x84 |
| Shift+7 | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| , | 0xA6 | U+0907 | इ | I |
| . | 0xA7 | U+0908 | ई | II |
| Shift+2 | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0xCB | U+092D | भ | BHA |
| Shift+c | 0xB9 | U+091B | छ | CHHA |
| Shift+d | 0xC5 | U+0927 | ध | DHA |
| Shift+e | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+f | 0x8C |  |  | ISCII_0x8C |
| Shift+g | 0xB6 | U+0918 | घ | GHA |
| Shift+h | 0xA3 | U+0903 | ः | Visarga |
| Shift+i | 0xDC | U+0941 | ु | Matra U |
| Shift+j | 0xBB | U+091D | झ | JHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xD1 | U+0933 | ळ | LLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE5 | U+094C | ौ | Matra AU |
| Shift+p | 0xC9 | U+092B | फ | PHA |
| Shift+q | 0xBE | U+0920 | ठ | TTHA |
| Shift+r | 0x8D | U+200D | ‍ | ZWJ |
| Shift+s | 0xD5 | U+0937 | ष | SSA |
| Shift+t | 0xC3 | U+0925 | थ | THA |
| Shift+u | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+v | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+w | 0xC0 | U+0922 | ढ | DDHA |
| Shift+x | 0x80 |  |  | ISCII_0x80 |
| Shift+y | 0xAD | U+0910 | ऐ | AI |
| Shift+z | 0xB0 | U+0913 | ओ | O |
| [ | 0xA8 | U+0909 | उ | U |
| \ | 0xB0 | U+0913 | ओ | O |
| ] | 0x8E | U+200C | ‌ | ZWNJ |
| ` | 0xE2 | U+0945 | ॅ | Matra Candra E |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0xE8 | U+093C | ़ | Nukta |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD2 | U+0934 | ऴ | LLLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| q | 0xBD | U+091F | ट | TTA |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xBF | U+0921 | ड | DDA |
| x | 0xD6 | U+0938 | स | SA |
| y | 0xCD | U+092F | य | YA |
| z | 0xAC | U+090F | ए | E |
| Shift+[ | 0xA9 | U+090A | ऊ | UU |
| Shift+\ | 0xB1 | U+0914 | औ | AU |
| Shift+] | 0x8F |  |  | ISCII_0x8F |
| Shift+` | 0xDF | U+0944 | ॄ | Matra Vocalic RR |

**Compose sequences (20):**

- Nukta + NA → ़न
- Matra Vocalic RR + Danda → ॄ।
- Nukta + Nukta → ़़
- Nukta + RRA → ़ऱ
- SSA + Nukta + RRA → ष़ऱ
- Chandrabindu + Danda → ँ।
- Matra Vocalic RR + Danda → ॄ।
- Nukta + YA → ़य
- RRA + Nukta → ऱ़
- JA + Nukta + NYA → ज़ञ
- TA + Nukta + RRA → त़ऱ
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDA + Danda → ड।
- KA + Nukta + SA → क़स
- TA + Nukta + TA → त़त
- DDHA + Danda → ढ।
- PHA + Danda → फ।

### Raming3
- **Devanagari key mappings:** 74
- **Files:** Raming3.idv, Raming3.dev

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| ' | 0x8B |  |  | ISCII_0x8B |
| Shift+9 | 0x8C |  |  | ISCII_0x8C |
| Shift+0 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+8 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+= | 0x8E | U+200C | ‌ | ZWNJ |
| , | 0xAC | U+090F | ए | E |
| . | 0x8F |  |  | ISCII_0x8F |
| / | 0x90 |  |  | ISCII_0x90 |
| Shift+; | 0x91 |  |  | ISCII_0x91 |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0x92 |  |  | ISCII_0x92 |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x93 |  |  | ISCII_0x93 |
| Shift+d | 0x94 |  |  | ISCII_0x94 |
| Shift+e | 0x95 |  |  | ISCII_0x95 |
| Shift+f | 0x96 |  |  | ISCII_0x96 |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0x97 |  |  | ISCII_0x97 |
| Shift+i | 0x98 |  |  | ISCII_0x98 |
| Shift+j | 0x99 |  |  | ISCII_0x99 |
| Shift+k | 0x9A |  |  | ISCII_0x9A |
| Shift+l | 0x9B |  |  | ISCII_0x9B |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x9C |  |  | ISCII_0x9C |
| Shift+p | 0x9D |  |  | ISCII_0x9D |
| Shift+q | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x9E |  |  | ISCII_0x9E |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x9F |  |  | ISCII_0x9F |
| Shift+u | 0xA0 |  |  | ISCII_0xA0 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0xEB |  |  | ISCII_0xEB |
| Shift+y | 0xEC |  |  | ISCII_0xEC |
| Shift+z | 0xED |  |  | ISCII_0xED |
| [ | 0xEE |  |  | ISCII_0xEE |
| \ | 0xE8 | U+093C | ़ | Nukta |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xFB |  |  | ISCII_0xFB |
| Shift+[ | 0xFC |  |  | ISCII_0xFC |
| Shift+\ | 0x89 |  |  | ISCII_0x89 |
| Shift+] | 0xFD |  |  | ISCII_0xFD |
| Shift+` | 0xFE |  |  | ISCII_0xFE |

**Compose sequences (44):**

- SA + Nukta → स़
- SSA + Nukta → ष़
- TA + Nukta + RRA → त़ऱ
- DA + Nukta + DHA → द़ध
- Nukta + Nukta → ़़
- NNA + Nukta → ण़
- DHA + Nukta → ध़
- RRA + Matra Vocalic R → ऱृ
- GHA + Nukta → घ़
- BA + Nukta → ब़
- KA + Nukta → क़
- MA + Nukta → म़
- THA + Nukta → थ़
- BHA + Nukta → भ़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- KHA + Nukta → ख़
- Nukta + RRA → ़ऱ
- KA + Nukta + SA + Nukta → क़स़
- DA + Nukta + BA → द़ब
- DA + Nukta + YA → द़य
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- DDHA + Danda → ढ।
- BHA + Nukta → भ़
- Chandrabindu + Danda → ँ।
- TA + Nukta + TA → त़त
- Nukta + RA → ़र
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- PHA + Danda → फ।
- DDA + Danda → ड।

### SCRIPT
- **Devanagari key mappings:** 74
- **Files:** SCRIPT.IDV, SCRIPT.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xAA | U+090B | ऋ | Vocalic R |
| ' | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| , | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| . | 0xE6 | U+0949 | ॉ | Matra Candra O |
| / | 0xE8 | U+093C | ़ | Nukta |
| 0 | 0xBB | U+091D | झ | JHA |
| 1 | 0xBD | U+091F | ट | TTA |
| 2 | 0xB4 | U+0916 | ख | KHA |
| 3 | 0xC5 | U+0927 | ध | DHA |
| 4 | 0xB9 | U+091B | छ | CHHA |
| 5 | 0xCB | U+092D | भ | BHA |
| 6 | 0xC3 | U+0925 | थ | THA |
| 7 | 0xB6 | U+0918 | घ | GHA |
| 8 | 0xBE | U+0920 | ठ | TTHA |
| 9 | 0xC0 | U+0922 | ढ | DDHA |
| Shift+; | 0xA9 | U+090A | ऊ | UU |
| ; | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+, | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+. | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+/ | 0x8B |  |  | ISCII_0x8B |
| Shift+a | 0xA3 | U+0903 | ः | Visarga |
| Shift+c | 0x8C |  |  | ISCII_0x8C |
| Shift+e | 0x8D | U+200D | ‍ | ZWJ |
| Shift+f | 0xA2 | U+0902 | ं | Anusvar |
| Shift+h | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+i | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+j | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+k | 0x8F |  |  | ISCII_0x8F |
| Shift+l | 0xA7 | U+0908 | ई | II |
| Shift+m | 0x90 |  |  | ISCII_0x90 |
| Shift+n | 0x91 |  |  | ISCII_0x91 |
| Shift+o | 0x92 |  |  | ISCII_0x92 |
| Shift+p | 0xA6 | U+0907 | इ | I |
| Shift+q | 0x93 |  |  | ISCII_0x93 |
| Shift+r | 0x80 |  |  | ISCII_0x80 |
| Shift+u | 0x94 |  |  | ISCII_0x94 |
| Shift+v | 0x95 |  |  | ISCII_0x95 |
| Shift+w | 0x96 |  |  | ISCII_0x96 |
| Shift+x | 0x97 |  |  | ISCII_0x97 |
| Shift+y | 0x98 |  |  | ISCII_0x98 |
| Shift+z | 0xAC | U+090F | ए | E |
| [ | 0xDD | U+0942 | ू | Matra UU |
| ] | 0xD1 | U+0933 | ळ | LLA |
| Shift+- | 0x99 |  |  | ISCII_0x99 |
| ` | 0xBF | U+0921 | ड | DDA |
| a | 0xA4 | U+0905 | अ | A |
| b | 0xCA | U+092C | ब | BA |
| c | 0xBC | U+091E | ञ | NYA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xB3 | U+0915 | क | KA |
| f | 0xC6 | U+0928 | न | NA |
| g | 0xC1 | U+0923 | ण | NNA |
| h | 0xCC | U+092E | म | MA |
| i | 0xCD | U+092F | य | YA |
| j | 0xB5 | U+0917 | ग | GA |
| k | 0xE1 | U+0948 | ै | Matra AI |
| l | 0xDC | U+0941 | ु | Matra U |
| m | 0xE5 | U+094C | ौ | Matra AU |
| n | 0xC8 | U+092A | प | PA |
| o | 0xBA | U+091C | ज | JA |
| p | 0xDB | U+0940 | ी | Matra II |
| q | 0xD5 | U+0937 | ष | SSA |
| r | 0xDA | U+093F | ि | Matra I |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xD4 | U+0936 | श | SHA |
| u | 0xC2 | U+0924 | त | TA |
| v | 0xB8 | U+091A | च | CHA |
| w | 0xD6 | U+0938 | स | SA |
| x | 0xE2 | U+0945 | ॅ | Matra Candra E |
| y | 0xCF | U+0931 | ऱ | RRA |
| z | 0xD8 |  |  | UNUSED_D8 |
| Shift+[ | 0xA8 | U+0909 | उ | U |
| Shift+] | 0xC9 | U+092B | फ | PHA |
| Shift+` | 0xB7 | U+0919 | ङ | NGA |

**Compose sequences (30):**

- RRA + Nukta + Matra U → ऱ़ु
- JA + Nukta + NYA → ज़ञ
- DDA + Danda → ड।
- KA + Danda → क।
- GA + Danda → ग।
- RRA + Nukta + Anusvar → ऱ़ं
- RRA + Nukta + Matra AI → ऱ़ै
- Nukta + Nukta → ़़
- JA + Danda → ज।
- SSA + Nukta + RRA → ष़ऱ
- TA + Nukta + TA → त़त
- DDHA + Danda → ढ।
- KA + Nukta + SA → क़स
- RRA + Nukta + Matra Candra E → ऱ़ॅ
- RRA + Nukta → ऱ़
- PHA + Danda → फ।
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- TA + Nukta + RRA → त़ऱ
- Nukta + RRA → ़ऱ
- RRA + Nukta + Anusvar → ऱ़ं
- Chandrabindu + Danda → ँ।
- KHA + Danda → ख।
- RRA + Nukta + Matra Candra E + Anusvar → ऱ़ॅं
- Nukta + RRA + Matra UU → ़ऱू
- Nukta + RRA + Matra Vocalic R → ़ऱृ
- Nukta + RA → ़र
- Matra AI + Anusvar → ैं
- RRA + Nukta + Matra U + Anusvar → ऱ़ुं
- Nukta + NA → ़न

### SCRIPT1
- **Devanagari key mappings:** 72
- **Files:** SCRIPT1.IDV, SCRIPT1.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xAA | U+090B | ऋ | Vocalic R |
| ' | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+= | 0x8A | U+0970 | ॰ | Abbreviation sign |
| , | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| - | 0xBB | U+091D | झ | JHA |
| . | 0xE6 | U+0949 | ॉ | Matra Candra O |
| / | 0x8B |  |  | ISCII_0x8B |
| 0 | 0xC0 | U+0922 | ढ | DDHA |
| 1 | 0xBF | U+0921 | ड | DDA |
| 2 | 0xBD | U+091F | ट | TTA |
| 3 | 0xB4 | U+0916 | ख | KHA |
| 4 | 0xC5 | U+0927 | ध | DHA |
| 5 | 0xB9 | U+091B | छ | CHHA |
| 6 | 0xCB | U+092D | भ | BHA |
| 7 | 0xC3 | U+0925 | थ | THA |
| 8 | 0xB6 | U+0918 | घ | GHA |
| 9 | 0xBE | U+0920 | ठ | TTHA |
| Shift+; | 0xA9 | U+090A | ऊ | UU |
| ; | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+, | 0x8C |  |  | ISCII_0x8C |
| = | 0xC9 | U+092B | फ | PHA |
| Shift+. | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+/ | 0x8D | U+200D | ‍ | ZWJ |
| Shift+c | 0xE8 | U+093C | ़ | Nukta |
| Shift+f | 0xA2 | U+0902 | ं | Anusvar |
| Shift+g | 0x80 |  |  | ISCII_0x80 |
| Shift+h | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+i | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+j | 0x8F |  |  | ISCII_0x8F |
| Shift+k | 0x90 |  |  | ISCII_0x90 |
| Shift+l | 0xA7 | U+0908 | ई | II |
| Shift+m | 0x91 |  |  | ISCII_0x91 |
| Shift+n | 0x92 |  |  | ISCII_0x92 |
| Shift+o | 0xA6 | U+0907 | इ | I |
| Shift+p | 0xA8 | U+0909 | उ | U |
| Shift+q | 0x93 |  |  | ISCII_0x93 |
| Shift+t | 0x94 |  |  | ISCII_0x94 |
| Shift+u | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+v | 0x89 |  |  | ISCII_0x89 |
| Shift+w | 0x95 |  |  | ISCII_0x95 |
| Shift+x | 0x96 |  |  | ISCII_0x96 |
| Shift+z | 0xAC | U+090F | ए | E |
| [ | 0xD1 | U+0933 | ळ | LLA |
| \ | 0xD5 | U+0937 | ष | SSA |
| ` | 0xB7 | U+0919 | ङ | NGA |
| a | 0xA4 | U+0905 | अ | A |
| b | 0xCA | U+092C | ब | BA |
| c | 0xBC | U+091E | ञ | NYA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xDA | U+093F | ि | Matra I |
| f | 0xC6 | U+0928 | न | NA |
| g | 0xC1 | U+0923 | ण | NNA |
| h | 0xCC | U+092E | म | MA |
| i | 0xBA | U+091C | ज | JA |
| j | 0xB5 | U+0917 | ग | GA |
| k | 0xE1 | U+0948 | ै | Matra AI |
| l | 0xDC | U+0941 | ु | Matra U |
| m | 0xE5 | U+094C | ौ | Matra AU |
| n | 0xC8 | U+092A | प | PA |
| o | 0xDB | U+0940 | ी | Matra II |
| p | 0xDD | U+0942 | ू | Matra UU |
| q | 0xD6 | U+0938 | स | SA |
| r | 0xD4 | U+0936 | श | SHA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xCF | U+0931 | ऱ | RRA |
| u | 0xCD | U+092F | य | YA |
| v | 0xB8 | U+091A | च | CHA |
| w | 0xB3 | U+0915 | क | KA |
| x | 0xE2 | U+0945 | ॅ | Matra Candra E |
| y | 0xC2 | U+0924 | त | TA |
| z | 0xD8 |  |  | UNUSED_D8 |
| Shift+\ | 0x97 |  |  | ISCII_0x97 |

**Compose sequences (30):**

- PHA + Danda → फ।
- RRA + Matra UU → ऱू
- RRA + Nukta + Matra U → ऱ़ु
- RRA + Matra Vocalic R → ऱृ
- JA + Danda → ज।
- GA + Danda → ग।
- Nukta + YA → ़य
- RRA + Nukta + Matra AI → ऱ़ै
- Nukta + Nukta → ़़
- KA + Nukta + SA → क़स
- RRA + Nukta → ऱ़
- KA + Danda → क।
- RRA + Nukta + Matra Candra E → ऱ़ॅ
- SSA + Nukta + RRA → ष़ऱ
- Matra Vocalic RR + Danda → ॄ।
- Chandrabindu + Danda → ँ।
- SSA + Nukta → ष़
- Nukta + RRA + Matra Vocalic R → ़ऱृ
- JA + Nukta + NYA → ज़ञ
- Matra Candra E + Anusvar → ॅं
- RRA + Nukta + Matra Candra E + Anusvar → ऱ़ॅं
- RRA + Nukta + Matra AI + Anusvar → ऱ़ैं
- RRA + Nukta + Anusvar → ऱ़ं
- Nukta + RRA → ़ऱ
- TA + Nukta + TA → त़त
- Matra AI + Anusvar → ैं
- RRA + Nukta + Matra U + Anusvar → ऱ़ुं
- DDA + Danda → ड।
- DDHA + Danda → ढ।
- TA + Nukta + RRA → त़ऱ

### SRG
- **Devanagari key mappings:** 77
- **Files:** SRG.IDV, SRG.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0xD6 | U+0938 | स | SA |
| Shift+3 | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+4 | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+5 | 0xA3 | U+0903 | ः | Visarga |
| Shift+7 | 0x83 |  |  | ISCII_0x83 |
| ' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+9 | 0x8B |  |  | ISCII_0x8B |
| Shift+0 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+8 | 0x8C |  |  | ISCII_0x8C |
| , | 0xAC | U+090F | ए | E |
| . | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| / | 0x8D | U+200D | ‍ | ZWJ |
| Shift+; | 0x8E | U+200C | ‌ | ZWNJ |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+2 | 0x8F |  |  | ISCII_0x8F |
| Shift+a | 0x90 |  |  | ISCII_0x90 |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x91 |  |  | ISCII_0x91 |
| Shift+d | 0x92 |  |  | ISCII_0x92 |
| Shift+e | 0x93 |  |  | ISCII_0x93 |
| Shift+f | 0x94 |  |  | ISCII_0x94 |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0x95 |  |  | ISCII_0x95 |
| Shift+i | 0xC9 | U+092B | फ | PHA |
| Shift+j | 0x96 |  |  | ISCII_0x96 |
| Shift+k | 0x97 |  |  | ISCII_0x97 |
| Shift+l | 0x98 |  |  | ISCII_0x98 |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x99 |  |  | ISCII_0x99 |
| Shift+p | 0x9A |  |  | ISCII_0x9A |
| Shift+q | 0xBC | U+091E | ञ | NYA |
| Shift+r | 0x9B |  |  | ISCII_0x9B |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x9C |  |  | ISCII_0x9C |
| Shift+u | 0x9D |  |  | ISCII_0x9D |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xA1 | U+0901 | ँ | Chandrabindu |
| Shift+x | 0x9E |  |  | ISCII_0x9E |
| Shift+y | 0x9F |  |  | ISCII_0x9F |
| Shift+z | 0xA0 |  |  | ISCII_0xA0 |
| [ | 0xB4 | U+0916 | ख | KHA |
| \ | 0xE8 | U+093C | ़ | Nukta |
| Shift+- | 0xEB |  |  | ISCII_0xEB |
| ` | 0xB7 | U+0919 | ङ | NGA |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xEC |  |  | ISCII_0xEC |
| Shift+[ | 0xED |  |  | ISCII_0xED |
| Shift+\ | 0x89 |  |  | ISCII_0x89 |
| Shift+] | 0xEE |  |  | ISCII_0xEE |
| Shift+` | 0xFB |  |  | ISCII_0xFB |

**Compose sequences (37):**

- SSA + Nukta → ष़
- TA + Nukta + RRA → त़ऱ
- DA + Nukta + DHA → द़ध
- DHA + Nukta → ध़
- RRA + Matra UU → ऱू
- Nukta + Nukta → ़़
- Matra AI + Anusvar → ैं
- BA + Nukta → ब़
- KA + Nukta + TA → क़त
- MA + Nukta → म़
- THA + Nukta → थ़
- DDHA + Danda → ढ।
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- DDA + Danda → ड।
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta + TA → त़त
- JA + Danda → ज।
- NA + Nukta → ऩ
- Nukta + RA → ़र
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- Chandrabindu + Danda → ँ।
- Nukta + RRA → ़ऱ
- KHA + Danda → ख।
- DA + Nukta + SHA → द़श
- DA + Nukta + YA → द़य
- Vocalic R + Danda → ऋ।
- Matra Vocalic RR + Danda → ॄ।
- PHA + Danda → फ।
- Matra AU + Anusvar → ौं
- KA + Danda → क।
- KA + Nukta + SA → क़स
- RRA + Nukta + Matra U → ऱ़ु
- GA + Danda → ग।
- PHA + Nukta → फ़

### TYPEWRI2
- **Devanagari key mappings:** 73
- **Files:** TYPEWRI2.IDV, TYPEWRI2.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+3 | 0xA3 | U+0903 | ः | Visarga |
| Shift+5 | 0x88 | U+0952 | ॒ | Stress sign |
| ' | 0x8B |  |  | ISCII_0x8B |
| Shift+9 | 0x8C |  |  | ISCII_0x8C |
| Shift+0 | 0x8D | U+200D | ‍ | ZWJ |
| Shift+8 | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+= | 0x8F |  |  | ISCII_0x8F |
| , | 0xAC | U+090F | ए | E |
| . | 0x90 |  |  | ISCII_0x90 |
| / | 0x91 |  |  | ISCII_0x91 |
| Shift+; | 0x92 |  |  | ISCII_0x92 |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| = | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0x93 |  |  | ISCII_0x93 |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x94 |  |  | ISCII_0x94 |
| Shift+d | 0x95 |  |  | ISCII_0x95 |
| Shift+e | 0x96 |  |  | ISCII_0x96 |
| Shift+f | 0x97 |  |  | ISCII_0x97 |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0x98 |  |  | ISCII_0x98 |
| Shift+i | 0x99 |  |  | ISCII_0x99 |
| Shift+j | 0x9A |  |  | ISCII_0x9A |
| Shift+k | 0x9B |  |  | ISCII_0x9B |
| Shift+l | 0x9C |  |  | ISCII_0x9C |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x9D |  |  | ISCII_0x9D |
| Shift+p | 0x9E |  |  | ISCII_0x9E |
| Shift+q | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x9F |  |  | ISCII_0x9F |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0xA0 |  |  | ISCII_0xA0 |
| Shift+u | 0xEB |  |  | ISCII_0xEB |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0xEC |  |  | ISCII_0xEC |
| Shift+y | 0xED |  |  | ISCII_0xED |
| Shift+z | 0xEE |  |  | ISCII_0xEE |
| [ | 0xFB |  |  | ISCII_0xFB |
| ` | 0xE9 | U+0964 | । | Danda |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xFD |  |  | ISCII_0xFD |
| Shift+[ | 0xFE |  |  | ISCII_0xFE |

**Compose sequences (47):**

- SA + Nukta → स़
- SSA + Nukta + Matra AA → ष़ा
- TA + Nukta + RRA → त़ऱ
- Vocalic R + Danda → ऋ।
- DA + Nukta + DHA → द़ध
- Nukta + Nukta → ़़
- NNA + Nukta → ण़
- DHA + Nukta → ध़
- RRA + Matra Vocalic R → ऱृ
- GHA + Nukta → घ़
- BA + Nukta → ब़
- KA + Nukta + Matra AA → क़ा
- MA + Nukta → म़
- THA + Nukta → थ़
- BHA + Nukta → भ़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- KHA + Nukta → ख़
- DDA + Danda → ड।
- Nukta + RRA → ़ऱ
- KA + Nukta + SA + Nukta → क़स़
- DA + Nukta + YA → द़य
- DA + Nukta + SHA → द़श
- DA + Nukta + YA → द़य
- Nukta + NA → ़न
- TA + Nukta + TA → त़त
- Matra Vocalic RR + Danda → ॄ।
- Nukta + RA → ़र
- Chandrabindu + Danda → ँ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- DDA + Danda → ड।
- KA + Nukta + SA → क़स

### TYPEWRIT
- **Devanagari key mappings:** 71
- **Files:** TYPEWRIT.IDV, TYPEWRIT.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+' | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+3 | 0x8B |  |  | ISCII_0x8B |
| Shift+5 | 0xA3 | U+0903 | ः | Visarga |
| ' | 0x8C |  |  | ISCII_0x8C |
| Shift+0 | 0x8D | U+200D | ‍ | ZWJ |
| , | 0xAC | U+090F | ए | E |
| . | 0x8E | U+200C | ‌ | ZWNJ |
| / | 0x8F |  |  | ISCII_0x8F |
| Shift+; | 0x90 |  |  | ISCII_0x90 |
| ; | 0xCD | U+092F | य | YA |
| Shift+, | 0xC0 | U+0922 | ढ | DDHA |
| = | 0x91 |  |  | ISCII_0x91 |
| Shift+. | 0xBB | U+091D | झ | JHA |
| Shift+/ | 0x92 |  |  | ISCII_0x92 |
| Shift+a | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+b | 0xBE | U+0920 | ठ | TTHA |
| Shift+c | 0x93 |  |  | ISCII_0x93 |
| Shift+d | 0x94 |  |  | ISCII_0x94 |
| Shift+e | 0x95 |  |  | ISCII_0x95 |
| Shift+f | 0x96 |  |  | ISCII_0x96 |
| Shift+g | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+h | 0x97 |  |  | ISCII_0x97 |
| Shift+i | 0x98 |  |  | ISCII_0x98 |
| Shift+j | 0x99 |  |  | ISCII_0x99 |
| Shift+k | 0x9A |  |  | ISCII_0x9A |
| Shift+l | 0x9B |  |  | ISCII_0x9B |
| Shift+m | 0xBF | U+0921 | ड | DDA |
| Shift+n | 0xB9 | U+091B | छ | CHHA |
| Shift+o | 0x9C |  |  | ISCII_0x9C |
| Shift+p | 0x9D |  |  | ISCII_0x9D |
| Shift+q | 0xC9 | U+092B | फ | PHA |
| Shift+r | 0x9E |  |  | ISCII_0x9E |
| Shift+s | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+t | 0x9F |  |  | ISCII_0x9F |
| Shift+u | 0xA0 |  |  | ISCII_0xA0 |
| Shift+v | 0xBD | U+091F | ट | TTA |
| Shift+w | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+x | 0xEB |  |  | ISCII_0xEB |
| Shift+y | 0xEC |  |  | ISCII_0xEC |
| Shift+z | 0xED |  |  | ISCII_0xED |
| [ | 0xEE |  |  | ISCII_0xEE |
| ` | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| a | 0xA2 | U+0902 | ं | Anusvar |
| b | 0xA6 | U+0907 | इ | I |
| c | 0xCA | U+092C | ब | BA |
| d | 0xB3 | U+0915 | क | KA |
| e | 0xCC | U+092E | म | MA |
| f | 0xDB | U+0940 | ी | Matra II |
| g | 0xD8 |  |  | UNUSED_D8 |
| h | 0xDC | U+0941 | ु | Matra U |
| i | 0xC8 | U+092A | प | PA |
| j | 0xCF | U+0931 | ऱ | RRA |
| k | 0xDA | U+093F | ि | Matra I |
| l | 0xD7 | U+0939 | ह | HA |
| m | 0xA8 | U+0909 | उ | U |
| n | 0xC4 | U+0926 | द | DA |
| o | 0xD4 | U+0936 | श | SHA |
| p | 0xB8 | U+091A | च | CHA |
| q | 0xDD | U+0942 | ू | Matra UU |
| r | 0xC2 | U+0924 | त | TA |
| s | 0xE1 | U+0948 | ै | Matra AI |
| t | 0xBA | U+091C | ज | JA |
| u | 0xC6 | U+0928 | न | NA |
| v | 0xA4 | U+0905 | अ | A |
| w | 0xDE | U+0943 | ृ | Matra Vocalic R |
| x | 0xB5 | U+0917 | ग | GA |
| y | 0xD1 | U+0933 | ळ | LLA |
| z | 0xFB |  |  | ISCII_0xFB |
| Shift+[ | 0xFC |  |  | ISCII_0xFC |
| Shift+\ | 0xFD |  |  | ISCII_0xFD |
| Shift+] | 0xFE |  |  | ISCII_0xFE |

**Compose sequences (45):**

- SA + Nukta → स़
- RRA + Matra UU → ऱू
- SSA + Nukta → ष़
- DA + Nukta + DHA → द़ध
- NNA + Nukta → ण़
- DHA + Nukta → ध़
- RRA + Matra Vocalic R → ऱृ
- TA + Nukta + RRA → त़ऱ
- GHA + Nukta → घ़
- BA + Nukta → ब़
- KA + Nukta + Matra AA → क़ा
- MA + Nukta → म़
- THA + Nukta → थ़
- BHA + Nukta → भ़
- PA + Nukta → प़
- SSA + Nukta + RRA → ष़ऱ
- JA + Nukta + NYA → ज़ञ
- HA + Nukta → ह़
- SHA + Nukta → श़
- CHA + Nukta → च़
- TA + Nukta → त़
- JA + Nukta → ज़
- NA + Nukta → ऩ
- GA + Nukta → ग़
- LLA + Nukta → ऴ
- RRA + Nukta → ऱ़
- KHA + Nukta → ख़
- Nukta + RRA → ़ऱ
- KA + Nukta + SA + Nukta → क़स़
- DA + Nukta + YA → द़य
- DA + Nukta + SHA → द़श
- Nukta + Nukta → ़़
- Nukta + NA → ़न
- TA + Nukta + TA → त़त
- Matra Vocalic RR + Danda → ॄ।
- Nukta + YA → ़य
- Chandrabindu + Danda → ँ।
- KA + Danda → क।
- KHA + Danda → ख।
- GA + Danda → ग।
- JA + Danda → ज।
- DDHA + Danda → ढ।
- PHA + Danda → फ।
- DDA + Danda → ड।
- KA + Nukta + SA → क़स

### sulipi
- **Devanagari key mappings:** 59
- **Files:** SULIPI.IDV, sulipi.DEV

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| , | 0x8A | U+0970 | ॰ | Abbreviation sign |
| - | 0x88 | U+0952 | ॒ | Stress sign |
| = | 0xE8 | U+093C | ़ | Nukta |
| Shift+. | 0xEA | U+0965 | ॥ | Double Danda / Attr |
| Shift+a | 0xA4 | U+0905 | अ | A |
| Shift+b | 0xCB | U+092D | भ | BHA |
| Shift+c | 0xB9 | U+091B | छ | CHHA |
| Shift+d | 0xBF | U+0921 | ड | DDA |
| Shift+e | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+f | 0xC9 | U+092B | फ | PHA |
| Shift+g | 0xB6 | U+0918 | घ | GHA |
| Shift+i | 0xDC | U+0941 | ु | Matra U |
| Shift+j | 0xBB | U+091D | झ | JHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xE6 | U+0949 | ॉ | Matra Candra O |
| Shift+p | 0xC9 | U+092B | फ | PHA |
| Shift+q | 0xBE | U+0920 | ठ | TTHA |
| Shift+r | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+s | 0xD5 | U+0937 | ष | SSA |
| Shift+t | 0xBD | U+091F | ट | TTA |
| Shift+u | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+w | 0xC0 | U+0922 | ढ | DDHA |
| Shift+x | 0x8B |  |  | ISCII_0x8B |
| Shift+z | 0x8C |  |  | ISCII_0x8C |
| [ | 0xA8 | U+0909 | उ | U |
| \ | 0x81 |  |  | ISCII_0x81 |
| ] | 0xA6 | U+0907 | इ | I |
| a | 0xDA | U+093F | ि | Matra I |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xC4 | U+0926 | द | DA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0x89 |  |  | ISCII_0x89 |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xE5 | U+094C | ौ | Matra AU |
| p | 0xC8 | U+092A | प | PA |
| q | 0xC3 | U+0925 | थ | THA |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xC2 | U+0924 | त | TA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xC5 | U+0927 | ध | DHA |
| x | 0x8D | U+200D | ‍ | ZWJ |
| y | 0xCD | U+092F | य | YA |
| z | 0xAC | U+090F | ए | E |
| Shift+[ | 0xA9 | U+090A | ऊ | UU |
| Shift+\ | 0x82 |  |  | ISCII_0x82 |
| Shift+] | 0xA7 | U+0908 | ई | II |

**Compose sequences (24):**

- Nukta + Nukta → ़़
- SSA + Nukta + RRA → ष़ऱ
- A + Matra Candra E → अॅ
- KA + Nukta + SA → क़स
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- Vocalic R + Danda → ऋ।
- SSA + Nukta + Matra I → ष़ि
- Nukta + RA → ़र
- DDA + Danda → ड।
- PHA + Danda → फ।
- JA + Nukta + NYA → ज़ञ
- KA + Danda → क।
- DDHA + Danda → ढ।
- JA + Danda → ज।
- KA + Nukta + Matra AA → क़ा

### wx_dev
- **Devanagari key mappings:** 65
- **Files:** WX_DEV.IDV, wx_dev.Dev

| Key | ISCII | Unicode | Char | Name |
|-----|-------|---------|------|------|
| Shift+1 | 0xA6 | U+0907 | इ | I |
| Shift+3 | 0xA8 | U+0909 | उ | U |
| Shift+4 | 0xA9 | U+090A | ऊ | UU |
| Shift+5 | 0xAA | U+090B | ऋ | Vocalic R |
| Shift+7 | 0xE3 | U+094A | ॊ | Matra Short O |
| Shift+8 | 0xA3 | U+0903 | ः | Visarga |
| , | 0xAC | U+090F | ए | E |
| - | 0xE8 | U+093C | ़ | Nukta |
| Shift+2 | 0xA7 | U+0908 | ई | II |
| Shift+a | 0xDA | U+093F | ि | Matra I |
| Shift+b | 0xCB | U+092D | भ | BHA |
| Shift+c | 0xB9 | U+091B | छ | CHHA |
| Shift+d | 0xC0 | U+0922 | ढ | DDHA |
| Shift+e | 0xE2 | U+0945 | ॅ | Matra Candra E |
| Shift+f | 0x8A | U+0970 | ॰ | Abbreviation sign |
| Shift+g | 0xB6 | U+0918 | घ | GHA |
| Shift+h | 0xBC | U+091E | ञ | NYA |
| Shift+i | 0xDC | U+0941 | ु | Matra U |
| Shift+j | 0xBB | U+091D | झ | JHA |
| Shift+k | 0xB4 | U+0916 | ख | KHA |
| Shift+l | 0xD2 | U+0934 | ऴ | LLLA |
| Shift+m | 0xA2 | U+0902 | ं | Anusvar |
| Shift+n | 0xC1 | U+0923 | ण | NNA |
| Shift+o | 0xB1 | U+0914 | औ | AU |
| Shift+p | 0xC9 | U+092B | फ | PHA |
| Shift+q | 0x8B |  |  | ISCII_0x8B |
| Shift+r | 0xD6 | U+0938 | स | SA |
| Shift+s | 0xD5 | U+0937 | ष | SSA |
| Shift+t | 0xBE | U+0920 | ठ | TTHA |
| Shift+u | 0xDE | U+0943 | ृ | Matra Vocalic R |
| Shift+v | 0xC1 | U+0923 | ण | NNA |
| Shift+w | 0xC3 | U+0925 | थ | THA |
| Shift+x | 0xC5 | U+0927 | ध | DHA |
| Shift+y | 0x8C |  |  | ISCII_0x8C |
| [ | 0x8D | U+200D | ‍ | ZWJ |
| \ | 0x8E | U+200C | ‌ | ZWNJ |
| Shift+6 | 0x8F |  |  | ISCII_0x8F |
| Shift+- | 0x89 |  |  | ISCII_0x89 |
| ` | 0xD6 | U+0938 | स | SA |
| a | 0xA4 | U+0905 | अ | A |
| b | 0xCA | U+092C | ब | BA |
| c | 0xB8 | U+091A | च | CHA |
| d | 0xBF | U+0921 | ड | DDA |
| e | 0xE1 | U+0948 | ै | Matra AI |
| f | 0xBC | U+091E | ञ | NYA |
| g | 0xB5 | U+0917 | ग | GA |
| h | 0xD8 |  |  | UNUSED_D8 |
| i | 0xDB | U+0940 | ी | Matra II |
| j | 0xBA | U+091C | ज | JA |
| k | 0xB3 | U+0915 | क | KA |
| l | 0xD1 | U+0933 | ळ | LLA |
| m | 0xCC | U+092E | म | MA |
| n | 0xC6 | U+0928 | न | NA |
| o | 0xB0 | U+0913 | ओ | O |
| p | 0xC8 | U+092A | प | PA |
| q | 0xDF | U+0944 | ॄ | Matra Vocalic RR |
| r | 0xCF | U+0931 | ऱ | RRA |
| s | 0xD7 | U+0939 | ह | HA |
| t | 0xBD | U+091F | ट | TTA |
| u | 0xDD | U+0942 | ू | Matra UU |
| v | 0xD4 | U+0936 | श | SHA |
| w | 0xC2 | U+0924 | त | TA |
| x | 0xC4 | U+0926 | द | DA |
| y | 0xCD | U+092F | य | YA |
| Shift+` | 0x90 |  |  | ISCII_0x90 |

**Compose sequences (24):**

- 0x9F + 0x02 + 0x83 + 0xA0 + 0x00 → [0x9F][0x02][0x83][0xA0][0x00]
- TA + Nukta + RRA → त़ऱ
- Nukta + RRA → ़ऱ
- Nukta + RA → ़र
- TA + Nukta + TA → त़त
- RRA + Nukta → ऱ़
- Vocalic R + Danda → ऋ।
- KA + Nukta + SA → क़स
- Chandrabindu + Danda → ँ।
- Matra Vocalic RR + Danda → ॄ।
- KA + Danda → क।
- KHA + Danda → ख।
- PHA + Danda → फ।
- DDA + Danda → ड।
- JA + Danda → ज।
- GA + Danda → ग।
- Nukta + Nukta → ़़
- SSA + Nukta + RRA → ष़ऱ
- DDA + Danda → ड।
- PHA + Danda → फ।
- GA + Danda → ग।
- JA + Danda → ज।
- PHA + Danda → फ।
- JA + Nukta + NYA → ज़ञ
