#!/usr/bin/env python3
"""
Varnaakshara Portable ZIP Builder
===================================
Creates a portable (no-install) ZIP package that runs without installation.

Output: installer/output/VarnaaksharaPortable-x64.zip

Contents:
  VarnaaksharaPortable/
  ├── IME/              — IME application + embedded Python
  ├── Writer/           — Electron Writer app
  ├── Fonts/            — All font files (user installs manually)
  ├── StartIME.bat      — Launch the IME
  ├── StartWriter.bat   — Launch the Writer
  └── README.txt        — Quick start guide

Usage:
    python build_portable.py                # Full portable build
    python build_portable.py --skip-writer  # IME only
    python build_portable.py --from-staging # Use existing staging dir

Requirements:
    - The staging/ directory must be populated (run build.py --skip-iscc first)
    - OR pass --from-source to build from source
"""

import os
import sys
import shutil
import zipfile
import argparse
from pathlib import Path
from datetime import datetime

# ════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════

VERSION = "1.0.0"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INSTALLER_DIR = PROJECT_ROOT / "installer"
STAGING_DIR = INSTALLER_DIR / "staging"
OUTPUT_DIR = INSTALLER_DIR / "output"
PORTABLE_DIR = INSTALLER_DIR / "portable_build"  # Temp assembly dir
ZIP_NAME = f"VarnaaksharaPortable-x64.zip"

# ════════════════════════════════════════════════════════════
# BATCH LAUNCHER SCRIPTS
# ════════════════════════════════════════════════════════════

START_IME_BAT = r"""@echo off
title Varnaakshara IME
echo ============================================
echo   Varnaakshara IME — Portable Edition
echo   Version {version}
echo ============================================
echo.
echo Starting Varnaakshara IME...
echo Press F11 to toggle IME on/off
echo Press F12 to open Settings
echo.

cd /d "%~dp0IME"
start "" "Varnaakshara.exe"
""".format(version=VERSION)

START_WRITER_BAT = r"""@echo off
title Varnaakshara Writer
echo ============================================
echo   Varnaakshara Writer — Portable Edition
echo   Version {version}
echo ============================================
echo.
echo Starting Varnaakshara Writer...
echo.

cd /d "%~dp0Writer"
start "" "Varnaakshara Writer.exe"
""".format(version=VERSION)

README_TXT = """═══════════════════════════════════════════════════════════
          VARNAAKSHARA PORTABLE — वर्णाक्षरः
      Indian Script Input Method Engine v{version}
          Portable Edition (No Installation)
═══════════════════════════════════════════════════════════

QUICK START:

  1. INSTALL FONTS (first time only):
     - Open the "Fonts" folder
     - Select all .ttf files (Ctrl+A)
     - Right-click → "Install" or "Install for all users"
     - This installs the Indian script fonts to your system

  2. LAUNCH IME:
     - Double-click "StartIME.bat"
     - The IME will start in the system tray
     - Press F11 to toggle IME on/off
     - Press F12 to open Settings

  3. LAUNCH WRITER:
     - Double-click "StartWriter.bat"
     - A word processor optimized for Indian languages will open

HOW TO TYPE:

  With the IME active (F11 to toggle):
  - Type in English and get Indian script output
  - Example: Type "namaskara" → ನಮಸ್ಕಾರ (Kannada)
  - Press Ctrl+1 through Ctrl+= to switch languages

  Supported languages (12):
  • Assamese  • Bengali   • Gujarati  • Hindi
  • Kannada   • Malayalam • Marathi   • Odia
  • Punjabi   • Sanskrit  • Tamil     • Telugu

  Both Baraha-style and ITRANS transliteration schemes.

FOLDER CONTENTS:

  IME/         — The input method engine (PyInstaller bundle)
  Writer/      — Word processor (Electron app)
  Fonts/       — Indian script font files
    unicode/   — Noto Sans Unicode fonts (7 scripts)
    vedic/     — Vedic fonts (patched Noto Sans)
    ansi/      — Legacy ANSI fonts (23 fonts)
    generated/ — Extended weight variants (Regular–Black)

NOTES:

  • This is a portable edition — no installation required
  • Fonts must be installed manually (one-time)
  • Settings are saved in your user profile (%APPDATA%)
  • No admin rights needed to run (fonts may need admin to install)
  • This software is FREE and NOT FOR SALE

  Homepage: https://github.com/Exaggarate/Varnaakshara

═══════════════════════════════════════════════════════════
""".format(version=VERSION)

# ════════════════════════════════════════════════════════════
# UTILITIES
# ════════════════════════════════════════════════════════════

def log(msg, prefix="BUILD"):
    print(f"[{prefix}] {msg}")

def log_ok(msg):
    print(f"[  OK ] {msg}")

def log_warn(msg):
    print(f"[ WARN] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}")

def copy_tree(src, dst):
    """Copy directory tree."""
    src, dst = Path(src), Path(dst)
    if not src.exists():
        log_warn(f"Source not found, skipping: {src}")
        return 0
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return sum(1 for _ in dst.rglob("*") if _.is_file())

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)

# ════════════════════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════════════════════

def build_portable(include_writer=True, from_staging=True):
    """Assemble the portable directory and create ZIP."""

    print(f"""
╔════════════════════════════════════════════════════════════╗
║    Varnaakshara Portable ZIP Builder v{VERSION}               ║
╚════════════════════════════════════════════════════════════╝
""")

    root = PORTABLE_DIR / "VarnaaksharaPortable"

    # Clean previous build
    if PORTABLE_DIR.exists():
        shutil.rmtree(PORTABLE_DIR)

    ensure_dir(root)

    if from_staging:
        if not STAGING_DIR.exists():
            log_error(f"Staging directory not found: {STAGING_DIR}")
            log_error("Run 'python build.py --skip-iscc' first to populate staging.")
            sys.exit(1)

    # ── Step 1: IME ──
    log("Copying IME application...")
    ime_src = STAGING_DIR / "ime" if from_staging else PROJECT_ROOT / "dist" / "Varnaakshara"
    if ime_src.exists():
        count = copy_tree(ime_src, root / "IME")
        log_ok(f"IME: {count} files")
    else:
        log_error(f"IME source not found: {ime_src}")
        sys.exit(1)

    # Copy embedded Python alongside IME
    python_src = STAGING_DIR / "python"
    if python_src.exists():
        count = copy_tree(python_src, root / "IME" / "python")
        log_ok(f"Embedded Python: {count} files")

    # Copy core engine
    core_src = STAGING_DIR / "core" if from_staging else PROJECT_ROOT / "core"
    if core_src.exists():
        count = copy_tree(core_src, root / "IME" / "core")
        log_ok(f"Core engine: {count} files")

    # ── Step 2: Writer ──
    if include_writer:
        log("Copying Writer application...")
        writer_src = STAGING_DIR / "writer"
        if writer_src.exists():
            count = copy_tree(writer_src, root / "Writer")
            log_ok(f"Writer: {count} files")

            # Bridge
            bridge_src = STAGING_DIR / "bridge" / "bridge.py"
            if bridge_src.exists():
                ensure_dir(root / "Writer" / "bridge")
                shutil.copy2(bridge_src, root / "Writer" / "bridge" / "bridge.py")
        else:
            log_warn("Writer not found in staging, skipping")

    # ── Step 3: Fonts ──
    log("Copying font files...")
    fonts_dst = root / "Fonts"

    # Unicode
    unicode_src = STAGING_DIR / "fonts" / "unicode" if from_staging else PROJECT_ROOT / "fonts" / "unicode"
    if unicode_src.exists():
        count = copy_tree(unicode_src, fonts_dst / "unicode")
        log_ok(f"Unicode fonts: {count}")

    # Vedic
    vedic_src = STAGING_DIR / "fonts" / "vedic"
    if from_staging and vedic_src.exists():
        count = copy_tree(vedic_src, fonts_dst / "vedic")
        log_ok(f"Vedic fonts: {count}")
    else:
        # Copy from source
        ensure_dir(fonts_dst / "vedic")
        for vf in ["NotoSansKannadaVedic.ttf", "NotoSansDevanagariVedic.ttf"]:
            src = PROJECT_ROOT / "fonts" / vf
            if src.exists():
                shutil.copy2(src, fonts_dst / "vedic" / vf)
        log_ok("Vedic fonts: copied from source")

    # ANSI
    ansi_src = STAGING_DIR / "fonts" / "ansi" if from_staging else PROJECT_ROOT / "fonts" / "ansi"
    if ansi_src.exists():
        count = copy_tree(ansi_src, fonts_dst / "ansi")
        log_ok(f"ANSI fonts: {count}")

    # Generated weights
    gen_src = STAGING_DIR / "fonts" / "generated" if from_staging else PROJECT_ROOT / "core" / "fonts" / "generated"
    if gen_src.exists():
        count = copy_tree(gen_src, fonts_dst / "generated")
        log_ok(f"Generated weights: {count}")

    total_fonts = sum(1 for _ in fonts_dst.rglob("*.ttf"))
    log_ok(f"Total fonts: {total_fonts}")

    # ── Step 4: Launcher scripts ──
    log("Creating launcher scripts...")

    with open(root / "StartIME.bat", "w", encoding="utf-8") as f:
        f.write(START_IME_BAT)
    log_ok("StartIME.bat")

    if include_writer:
        with open(root / "StartWriter.bat", "w", encoding="utf-8") as f:
            f.write(START_WRITER_BAT)
        log_ok("StartWriter.bat")

    with open(root / "README.txt", "w", encoding="utf-8") as f:
        f.write(README_TXT)
    log_ok("README.txt")

    # Copy icon and license
    icon_src = INSTALLER_DIR / "icon.ico"
    if icon_src.exists():
        shutil.copy2(icon_src, root / "icon.ico")

    license_src = INSTALLER_DIR / "LICENSE.txt"
    if license_src.exists():
        shutil.copy2(license_src, root / "LICENSE.txt")

    # ── Step 5: Create ZIP ──
    log("Creating ZIP archive...")
    ensure_dir(OUTPUT_DIR)
    zip_path = OUTPUT_DIR / ZIP_NAME

    if zip_path.exists():
        zip_path.unlink()

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for file_path in sorted(PORTABLE_DIR.rglob("*")):
            if file_path.is_file():
                arcname = file_path.relative_to(PORTABLE_DIR)
                zf.write(file_path, arcname)
                file_count += 1

    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    log_ok(f"Created: {zip_path}")
    log_ok(f"Files: {file_count}")
    log_ok(f"Size: {zip_size_mb:.1f} MB")

    # ── Cleanup temp dir ──
    shutil.rmtree(PORTABLE_DIR)
    log("Cleaned up temporary build directory")

    # ── Summary ──
    print(f"""
╔════════════════════════════════════════════════════════════╗
║               PORTABLE BUILD COMPLETE! ✓                   ║
╚════════════════════════════════════════════════════════════╝

  Output: {zip_path}
  Size:   {zip_size_mb:.1f} MB
  Files:  {file_count}
  Date:   {datetime.now().strftime('%Y-%m-%d %H:%M')}
""")

# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Build Varnaakshara Portable ZIP package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--skip-writer", action="store_true",
                        help="Exclude Writer from portable package")
    parser.add_argument("--from-staging", action="store_true", default=True,
                        help="Use staging/ directory (default, requires build.py first)")
    parser.add_argument("--from-source", action="store_true",
                        help="Build from source directories (requires prior PyInstaller build)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    use_staging = not args.from_source
    build_portable(
        include_writer=not args.skip_writer,
        from_staging=use_staging,
    )


if __name__ == "__main__":
    main()
