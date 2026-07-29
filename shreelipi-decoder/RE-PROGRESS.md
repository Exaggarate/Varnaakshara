# Shree-Lipi Font RE Progress - 2026-07-07

## LZARI Decompressor: FIXED ✅
- `/tmp/lzari_v4.c` - working LZARI with correct DecodePosition
- Bug was: DecodePosition used position_cum[pos]/[pos+1] but should use [pos-1]/[pos] and return pos-1
- Roundtrip verified: 1-byte, text with back-refs, and full 56KB TTF

## Setup.exe Font Handler Disassembly
Found the EXACT font decompression function at **0x479A88** in Setup.exe:

### Flow:
1. CreateFile(source, READ) → source handle at [0x4A109C]  
2. CreateFile(dest, WRITE) → dest handle at [0x4A10A0]
3. GetFileSize → stored at [0x4A1070]
4. Read first 4 bytes of SL_ file INTO [0x4A1070] (overwrites file size!)
5. Read remaining (filesize-4) bytes into input buffer at [0x4A10AC]
6. Allocate output buffer of size = [0x4A1070] + 1 (the 4-byte header value)
7. Init text_buf with spaces, r = N-F = 4036 (0xFC4)
8. LZSS decode loop:
   - DecodeChar (0x47971C): if < 256 = literal, else = match
   - DecodePosition (0x4798EC): get match position
   - Match: len = c - 255 + 2, pos = (r - decode_pos - 1) & 0xFFF

### Confirmed Parameters:
- N = 4096 (0x1000)
- F = 60 (N-F = 0xFC4)
- THRESHOLD = 2
- N_CHAR = 314 (0x13A)
- Position table: 10000.0 / (i + 200) using FPU

### KEY PROBLEM:
First 4 bytes of SL_0708 = 0x9456E587 (2.48GB) — WAY too large for output size.
These 4 bytes must be ENCRYPTED before being used as the decompressed size.

### Next Steps:
1. Disassemble 0x479634 (StartModel) to find Q values
2. Disassemble 0x4794C0 (init) - PARTIALLY DONE, shows position_cum init
3. Disassemble 0x47971C (DecodeChar) to find Q1/Q2/Q3/Q4/MAX_CUM
4. Check if there's a DECRYPT step between reading 4-byte header and using it
5. Look for XOR/transform of the input data before decompression

### Key Addresses in Setup.exe:
- 0x479A88: Font decompress function (non-MITNET path)
- 0x479634: StartModel (sym freq + position_cum init)
- 0x4794C0: Arithmetic coder init  
- 0x47971C: DecodeChar
- 0x4798EC: DecodePosition
- 0x4A6464: text_buf (ring buffer)
- 0x4A10AC: input buffer pointer
- 0x4A10B0: output buffer pointer
- 0x4A1070: header/size variable
- 0x4A106C: compressed data size (file_size - 4)
