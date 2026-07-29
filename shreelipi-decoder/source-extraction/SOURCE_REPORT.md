# Shreelipi 7.4 — Complete Source Code Extraction

## Summary

**226,421 lines** of source code and analysis extracted from the entire Shreelipi 7.4 suite.

## Source Code Breakdown

### 1. .NET Caligrafer Source (C# — Full Decompilation)
- **462 files, 107,938 lines** of fully decompiled C# source
- Decompiled using ILSpy from .NET assemblies (pe_000 through pe_024)
- Includes complete source for:
  - `SLFont.dll` — Font rendering engine (ReadGlyph, Strokes, FontHandler)
  - `FontLib.dll` — Font library management
  - `Caligrafer.exe` — Main Caligrapher application (5,228 lines MainWindow)
  - `Language.cs` — Language/font handling (2,462 lines)
  - `Conversion.cs` — Format conversion utilities

### 2. Delphi Form Definitions (30 DFM files)
- UI layout source for all Delphi applications
- Extracted from: SL7_32, MFM6, SHREE.DLL, MITXLS.DLL, MLUtil6.DLL, FONTLIST.DLL, KbShcut.DLL
- Key forms: SL5FORM1 (main editor), frmInstall (font installer), frmMain (font manager)

### 3. Native Code Disassembly (83,113 lines)
- **MFM6.exe**: 1,149 functions, top 100 decompiled (30,288 lines)
- **SL7_32.EXE**: 1,441 functions, top 150 decompiled (30,604 lines)
- **SHREE.DLL**: 1,104 functions, top 100 decompiled (22,221 lines)

### 4. Binary Analysis Reports (34,729 lines)
- Complete string dumps, import tables, export tables
- Delphi class/RTTI metadata (1,107 classes from SL7_32 alone)
- All DLL imports and function names

### 5. DLL Public APIs (113 exported functions)
- **SHREE.DLL**: 57 exports (START_SHREE, SET_KEYBOARD, GET_FONTNAMES, etc.)
- **MITXLS.DLL**: 51 exports (rendering engine API)
- **MLUtil6.DLL**: 5 exports (hardware lock functions F1-F5)

## Key Discoveries

### SL_ Font Format (from C# source)
The `ReadGlyph.cs` file (959 lines) contains the COMPLETE SL_/SLX_ font reader:
- Variable-length opcodes for stroke-based glyph rendering
- Coordinate system: 500 units per em, big-endian
- Composition system for building complex glyphs from base components

### Cipher Implementations Found in Source
- **PRNG stream cipher** (SL_/SLX_/SU_ fonts)
- **LFSR 24-bit cipher** (FK_ fonts)
- **DES-based registration** (SLREGIS.DLL)
- **Rijndael/AES** (Install.exe license management)
- **XOR stream cipher** (._TF Unicode fonts)
- **LZARI compression** (installer files)

### Application Architecture
```
SL7_32.EXE (Main App - Delphi, 1.5MB)
├── SHREE.DLL (Input/Rendering - Delphi, 950KB)
│   ├── Keyboard input handling
│   ├── Font rendering dispatch
│   └── Script/language management
├── MITXLS.DLL (Excel/External rendering - Delphi, 950KB)
├── MFM6.EXE (Font Manager - Delphi, 926KB)
├── MLUtil6.DLL (Hardware lock - Delphi)
├── DEVDL32.DLL (Keyboard/Language DLL)
├── DEVVFC32.DLL (Virtual Font Cache)
├── KbShcut.DLL (Keyboard shortcuts)
├── Extutor.DLL (Tutorial system)
├── Caligrafer.exe (.NET)
│   ├── SLFont.dll (.NET - Font handler)
│   └── FontLib.dll (.NET - Font library)
└── 22 Language DLLs (Hindi, Tamil, Telugu, etc.)
```

## Tools Used
- **ILSpy 8.2** — .NET assembly decompilation to C#
- **Capstone 5.0** — x86 disassembly
- **Custom Python tools** — PE analysis, DFM extraction, string extraction
- **Ghidra 11.3.2** — Initial binary analysis and function identification

## Cracked Binaries
- `MFM6.exe` — 15 patches, all protection removed
- `SL7_32.EXE` — 19 patches, all protection removed
- `SHREE.DLL` — 2 patches (CRC + virus check)

## Update: Full Pseudocode Decompilation Complete

### radare2 pdc Decompilation (1,854,492 total lines)

Ghidra headless was choking on the VPS. Switched to **radare2's pdc** 
(pseudo-C decompiler) which ripped through all binaries in ~2 minutes total.

**Core Applications (804,078 lines):**
| Binary | Functions | Lines | Time |
|--------|-----------|-------|------|
| SL7_32.EXE | 3,260 | 211,899 | 30.5s |
| MFM6.EXE | 2,367 | 181,831 | 26.2s |
| SHREE.DLL | 2,471 | 157,491 | 22.4s |
| MITXLS.DLL | 2,357 | 148,841 | 20.2s |
| MLUtil6.DLL | 1,768 | 104,016 | 14.2s |

**Language/Device DLLs (907,106 lines):**
14 additional Shreelipi DLLs decompiled including:
- DEVVFC32.DLL (268,520 lines — largest, Virtual Font Cache)
- FONTLIST.DLL (89,529 lines — font enumeration)
- 8 DEV*32.DLL language drivers
- 2 SU*DEV32.DLL Unicode support DLLs

**Source Code Type Breakdown:**
- C# (compilable): 107,938 lines
- Delphi DFM (UI layout): 641 lines  
- Pseudo-C (readable): 1,711,184 lines
- Binary analysis: 34,729 lines
