# Varnaakshara Suite — Installer Build Guide

Build instructions for creating the Windows installer and portable packages.

## Quick Start

```powershell
cd installer
python build.py
```

This produces `output/VarnaaksharaSetup-x64.exe`.

## Prerequisites

### Required Software

| Tool | Version | Purpose | Download |
|------|---------|---------|----------|
| **Python** | 3.8+ | Build scripts, IME runtime | [python.org](https://www.python.org/downloads/) |
| **Node.js** | 18+ | Writer build (Electron) | [nodejs.org](https://nodejs.org/) |
| **Inno Setup** | 6.x | Installer compiler | [jrsoftware.org](https://jrsoftware.org/isdl.php) |
| **PyInstaller** | 5.0+ | IME packaging | `pip install pyinstaller` |

### Optional

| Tool | Purpose |
|------|---------|
| **NSIS** 3.x | Alternative installer compiler (if you prefer NSIS over Inno Setup) |
| **electron-builder** | Installed via `npm install` in the `writer/` directory |

### Python Dependencies

```powershell
pip install PyQt5 pyinstaller
```

### Node.js Dependencies (Writer)

```powershell
cd ../writer
npm install
```

## Build Options

### Full Suite Installer (Inno Setup)

```powershell
# Full build: IME + Writer + Fonts → Installer
python build.py

# Skip Writer (IME only)
python build.py --skip-writer

# Clean build from scratch
python build.py --clean

# Stage files only (don't compile installer)
python build.py --skip-iscc
```

### NSIS Alternative

If you prefer NSIS over Inno Setup:

```powershell
# First, stage the files
python build.py --skip-iscc

# Then compile with NSIS
makensis varnaakshara.nsi
```

### Portable ZIP (No Installation)

```powershell
# Build portable ZIP (requires staging dir from build.py)
python build.py --skip-iscc    # Prepare staging
python build_portable.py       # Create ZIP

# Or skip Writer
python build_portable.py --skip-writer
```

### Manual Inno Setup Compilation

If `iscc` is not in your PATH:

```powershell
# Default Inno Setup 6 location
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" varnaakshara.iss
```

## Directory Structure

```
installer/
├── varnaakshara.iss       # Inno Setup 6.x script (Suite installer)
├── varnaakshara_setup.iss # Legacy IME-only installer
├── varnaakshara.nsi       # NSIS alternative script
├── build.py               # Main build orchestrator
├── build_portable.py      # Portable ZIP builder
├── updater_config.json    # Auto-updater configuration
├── icon.ico               # Installer icon
├── LICENSE.txt            # License shown during install
├── README_INSTALL.txt     # Pre-install info page
├── dmg_background.png     # macOS DMG background
├── dmg_background.py      # macOS DMG background generator
├── staging/               # [Generated] Assembled files for packaging
│   ├── ime/               #   PyInstaller --onedir output
│   ├── writer/            #   Electron packaged output
│   ├── python/            #   Embedded Python 3.11
│   ├── core/              #   Engine, data, modules
│   ├── bridge/            #   Python ↔ Electron bridge
│   └── fonts/             #   All font files
│       ├── unicode/       #     Noto Sans (7 scripts)
│       ├── vedic/         #     Vedic fonts (2)
│       ├── ansi/          #     Legacy BRH fonts (23)
│       └── generated/     #     Weight variants (110)
├── output/                # [Generated] Final installer/ZIP output
│   ├── VarnaaksharaSetup-x64.exe
│   └── VarnaaksharaPortable-x64.zip
└── .cache/                # [Generated] Downloaded Python embed
```

## Build Pipeline

```
┌─────────────────────────────────────────────────────┐
│  Step 1: Build IME (PyInstaller --onedir)           │
│    varnaakshara_ime.py → dist/Varnaakshara/         │
├─────────────────────────────────────────────────────┤
│  Step 2: Build Writer (npm build + electron-builder)│
│    writer/src/ → writer/dist/win-unpacked/          │
├─────────────────────────────────────────────────────┤
│  Step 3: Download Embedded Python 3.11              │
│    python.org → .cache/ → staging/python/           │
├─────────────────────────────────────────────────────┤
│  Step 4: Stage Core Engine & Data                   │
│    core/ + ime/ + *.py → staging/core/              │
├─────────────────────────────────────────────────────┤
│  Step 5: Stage Fonts                                │
│    fonts/ + core/fonts/generated/ → staging/fonts/  │
├─────────────────────────────────────────────────────┤
│  Step 6: Compile Installer                          │
│    iscc varnaakshara.iss → output/Setup-x64.exe     │
│    ─ OR ─                                           │
│    makensis varnaakshara.nsi → output/Setup-x64.exe │
└─────────────────────────────────────────────────────┘
```

## What Gets Installed

### Components

| Component | Files | Size (est.) |
|-----------|-------|-------------|
| **Varnaakshara IME** | PyInstaller bundle + Python DLLs | ~25 MB |
| **Embedded Python 3.11** | Minimal Python runtime | ~15 MB |
| **Varnaakshara Writer** | Electron app | ~80 MB |
| **Unicode Fonts** | 7 Noto Sans fonts | ~2 MB |
| **Vedic Fonts** | 2 patched Noto Sans | ~0.5 MB |
| **ANSI Fonts** | 23 BRH legacy fonts | ~3 MB |
| **Generated Weights** | 110 weight variants | ~15 MB |

### Font Installation

Fonts are installed to the Windows Fonts directory (`C:\Windows\Fonts`) with proper registry entries under:
```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts
```

Each font is registered with `FontInstall` (Inno Setup) or `AddFontResourceW` (NSIS) for immediate availability without reboot.

### Registry Entries

| Key | Purpose |
|-----|---------|
| `HKCU\...\Run\Varnaakshara` | Auto-start at login (optional) |
| `HKCU\Software\Varnaakshara\Version` | Installed version (for updater) |
| `HKCU\Software\Varnaakshara\InstallPath` | Installation directory |
| `HKLM\...\App Paths\Varnaakshara.exe` | Win+R launch support |
| `HKLM\...\Uninstall\Varnaakshara Suite` | Add/Remove Programs entry |

## Auto-Updater

The `updater_config.json` configures the built-in auto-updater:

```json
{
  "update_url": "https://api.github.com/repos/Exaggarate/Varnaakshara/releases/latest",
  "current_version": "1.0.0",
  "check_interval_hours": 24,
  "auto_download": false
}
```

- Checks GitHub Releases API for new versions
- Notifies user when update is available
- Does NOT auto-download by default (user must opt in)
- Can be disabled entirely in Settings

## Signing (Optional)

For production releases, sign the installer with a code signing certificate:

```powershell
# Sign the installer EXE
signtool sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 ^
  /a output\VarnaaksharaSetup-x64.exe

# Verify signature
signtool verify /pa output\VarnaaksharaSetup-x64.exe
```

## Troubleshooting

### PyInstaller "DLL load failed"
Use `--onedir` mode (not `--onefile`). Python 3.14's DLL loading fails with `--onefile` temp extraction.

### Inno Setup "File not found"
Run `python build.py --skip-iscc` first to populate the `staging/` directory.

### Fonts not appearing after install
The installer broadcasts `WM_FONTCHANGE`. If fonts still don't appear, restart the application or log out/in.

### NSIS compilation errors
Ensure NSIS 3.x is installed (not 2.x). The script uses Unicode mode and MUI2.

### Writer build fails
```powershell
cd ../writer
rm -rf node_modules
npm install
npm run build
```

## Release Checklist

1. Update version in:
   - `varnaakshara.iss` (`SuiteVersion`)
   - `varnaakshara.nsi` (`PRODUCT_VERSION`)
   - `build.py` (`VERSION`)
   - `build_portable.py` (`VERSION`)
   - `updater_config.json` (`current_version`)
2. Run `python build.py --clean`
3. Test installer on clean Windows 10/11 VM
4. Sign the output EXE (if code signing cert available)
5. Create GitHub Release with:
   - `VarnaaksharaSetup-x64.exe`
   - `VarnaaksharaPortable-x64.zip`
6. Update `updater_config.json` on the release branch
