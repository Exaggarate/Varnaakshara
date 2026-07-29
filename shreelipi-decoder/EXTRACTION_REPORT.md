# Shreelipi 7.4 DVD — Complete Font Extraction Report

## Final Score: 11,960 / 11,960 = 100% ✅

**Every single encrypted font file on the Shreelipi 7.4 DVD has been decrypted.**

## Summary by Format

| Format | Count | Status | Cipher | Seed Formula | Decoder |
|--------|-------|--------|--------|--------------|---------|
| TTF (direct) | 138 | ✅ Plain | None | N/A | Direct copy |
| LZARI installer | 2,778 | ✅ Done | LZARI compression | N/A | `lzari_decode.c` |
| ._TF (Unicode TTF) | 64 | ✅ Done | XOR stream cipher | Per-file key in header | `sl_font_decrypt.py` |
| SL_ (vector fonts) | 4,945 | ✅ Done | PRNG stream cipher | font_num + 1 | `sl_font_decrypt.py` |
| SLX_ (ExFonts) | 5,260 | ✅ Done | PRNG stream cipher | font_num | `sl_font_decrypt.py` |
| SU_ (SUFONTS) | 126 | ✅ Done | PRNG stream cipher | font_num + 1 | `sl_font_decrypt.py` |
| S_ (style fonts) | N/A | ✅ Done | PRNG stream cipher | font_num + 1 | `sl_font_decrypt.py` |
| DEFFONTS | 80 | ✅ Plain | None | N/A | Direct copy |
| LNGFONTS | 58 | ✅ Plain | None | N/A | Direct copy |
| FK_ (bitmap fonts) | 1,277 | ✅ Done | LFSR parity cipher | font_num | `fk_font_decrypt.py` |
| FK_ MAP files | 12 | ✅ Plain | None | N/A | Direct copy |

## Cipher Details

### SL_/SLX_/SU_ PRNG Cipher
- **Algorithm**: 3-state linear recurrence, 10 mode-dependent multiplier sets
- **Modulus**: 0x7D03 (32,003)
- **Additive constant**: 0x40E6D (265,837)
- **Feedback**: CBC-like XOR: `plain = ks ^ prev_cipher ^ cipher ^ prev_plain`
- **Init**: `signed_byte_extract(seed)` → 11-round warmup
- **Mode**: `seed % 10` selects multiplier triplet
- **Key file**: `sl_font_decrypt.py` (Python), `sl_decrypt.c` (C)

### FK_ LFSR Parity Cipher
- **Algorithm**: 24-bit LFSR with bitmask parity feedback
- **State init**: Same PRNG warmup but with constant **0x668B7** (not 0x40E6D)
- **Fixed mode**: 8 (not seed-dependent)
- **Bitmasks**: bits 1, 4, 6, 30 (bit 255 overflows to 0)
- **Keystream**: 8 rounds per byte; each round: popcount(state & masks), shift state left, if odd parity → set LSB of output and state
- **Feedback**: Same CBC-like XOR as SL_
- **Key file**: `fk_font_decrypt.py`
- **Discovered in**: SL7_32.EXE (Shreelipi main application, LZARI-compressed on DVD)

### ._TF (Unicode TTF) Cipher
- **Algorithm**: XOR stream cipher with per-file key embedded in header
- **DES variant also exists** in newer Caligrafer version (not used on DVD)

## Reverse Engineering Timeline

1. **LZARI decoder** — Standard Okumura LZARI with Shreelipi-specific bug fixes (N_CHAR=314, removed spurious +1 in DecodeChar/DecodePosition)
2. **._TF cipher** — Cracked via .NET IL decompilation of Caligrafer Setup.exe
3. **SL_ PRNG cipher** — Cracked via Ghidra RE of MITXLS.dll + Wine DLL injection verification
4. **SLX_ cipher** — Same as SL_ with seed=font_num (no +1)
5. **SU_ cipher** — Same as SL_ with seed=font_num+1
6. **FK_ LFSR cipher** — Cracked via Ghidra RE of SL7_32.EXE (required fixing LZARI decoder first to decompress SL7_32.EX_)

## Key Breakthrough: LZARI Decoder Fix

The LZARI decoder had TWO bugs that prevented decompression of .EX_/.DL_ files:
1. `N_CHAR = 315` should be `N_CHAR = 314` (standard Okumura value: 256 - THRESHOLD + F)
2. Both `DecodeChar` and `DecodePosition` had `+ 1` appended to the `low` calculation that doesn't exist in standard LZARI

Fixing these allowed SL7_32.EX_ to decompress to a valid PE32 executable (1.5MB),
which contained the FK_ cipher code at functions 0x452D30 (init) and 0x453020 (keystream).

## Output Locations

- `/tmp/shreelipi_all_ttf/` — 138 direct TTFs
- `/tmp/shreelipi_fonts/ttf_ansi/` — 147 unique ANSI TTFs from LZARI
- `/tmp/shreelipi_unicode_ttf/` — 64 Unicode TTFs from ._TF
- `/tmp/sl_decrypted_full/` — 4,945 SL_ vector fonts (22 language dirs)
- `/tmp/slx_decrypted/` — 5,260 SLX_ ExFonts
- `/tmp/su_decrypted/` — 126 SU_ SUFONTS
- `/tmp/fk_decrypted/` — 1,277 FK_ bitmap fonts (12 language dirs)

## Tools

- `sl_font_decrypt.py` — SL_/SLX_/SU_/S_ PRNG cipher decoder (Python)
- `sl_decrypt.c` — SL_ PRNG cipher decoder (C, fast)
- `fk_font_decrypt.py` — FK_ LFSR parity cipher decoder (Python)
- `lzari_decode.c` — Fixed LZARI decompressor (C)
