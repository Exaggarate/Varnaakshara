#!/usr/bin/env python3
"""
Varnaakshara Suite — Build Script
==================================
Prepares the staging directory and compiles the Inno Setup installer.

Steps:
  1. Package IME (PyInstaller --onedir)
  2. Package Writer (npm run build + npm run package)
  3. Download embedded Python 3.11 if not cached
  4. Copy core engine, data, and fonts to staging
  5. Run Inno Setup compiler (iscc)

Usage:
    python build.py              # Full build
    python build.py --skip-ime   # Skip IME build (use existing)
    python build.py --skip-writer # Skip Writer build
    python build.py --skip-iscc  # Prepare staging only, don't compile
    python build.py --clean      # Clean staging + output first

Requirements (Windows):
    - Python 3.8+ with pip
    - Node.js 18+ with npm
    - PyInstaller: pip install pyinstaller
    - Inno Setup 6.x: https://jrsoftware.org/isinfo.php
      (iscc.exe must be in PATH or at default install location)
"""

import os
import sys
import shutil
import subprocess
import argparse
import zipfile
import urllib.request
import hashlib
from pathlib import Path

# ════════════════════════════════════════════════════════════
# CONFIGURATION
# ════════════════════════════════════════════════════════════

VERSION = "1.0.0"

# Paths relative to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INSTALLER_DIR = PROJECT_ROOT / "installer"
STAGING_DIR = INSTALLER_DIR / "staging"
OUTPUT_DIR = INSTALLER_DIR / "output"

# Embedded Python
PYTHON_VERSION = "3.11.9"
PYTHON_EMBED_URL = f"https://www.python.org/ftp/python/{PYTHON_VERSION}/python-{PYTHON_VERSION}-embed-amd64.zip"
PYTHON_EMBED_SHA256 = ""  # Set after first download for verification
PYTHON_CACHE_DIR = INSTALLER_DIR / ".cache"
PYTHON_EMBED_ZIP = PYTHON_CACHE_DIR / f"python-{PYTHON_VERSION}-embed-amd64.zip"

# Inno Setup compiler paths (checked in order)
ISCC_PATHS = [
    "iscc",  # PATH
    r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    r"C:\Program Files\Inno Setup 6\ISCC.exe",
    r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
]

# ════════════════════════════════════════════════════════════
# UTILITIES
# ════════════════════════════════════════════════════════════

class Colors:
    """ANSI color codes for terminal output."""
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    END = "\033[0m"

def log(msg, color=Colors.BLUE):
    print(f"{color}{Colors.BOLD}[BUILD]{Colors.END} {msg}")

def log_step(msg):
    print(f"\n{Colors.HEADER}{'═' * 60}")
    print(f"  {msg}")
    print(f"{'═' * 60}{Colors.END}\n")

def log_ok(msg):
    log(msg, Colors.GREEN)

def log_warn(msg):
    log(msg, Colors.YELLOW)

def log_error(msg):
    log(msg, Colors.RED)

def run(cmd, cwd=None, check=True, capture=False):
    """Run a subprocess command."""
    log(f"$ {cmd if isinstance(cmd, str) else ' '.join(cmd)}")
    kwargs = {
        "cwd": cwd,
        "shell": isinstance(cmd, str),
    }
    if capture:
        kwargs["capture_output"] = True
        kwargs["text"] = True
    result = subprocess.run(cmd, **kwargs)
    if check and result.returncode != 0:
        log_error(f"Command failed with exit code {result.returncode}")
        if capture and result.stderr:
            log_error(result.stderr)
        sys.exit(1)
    return result

def ensure_dir(path):
    """Create directory if it doesn't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)

def clean_dir(path):
    """Remove and recreate a directory."""
    p = Path(path)
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True, exist_ok=True)

def copy_tree(src, dst, pattern=None):
    """Copy directory tree, optionally filtering by glob pattern."""
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        log_warn(f"Source not found, skipping: {src}")
        return 0

    count = 0
    if pattern:
        for f in src.rglob(pattern):
            if f.is_file():
                rel = f.relative_to(src)
                dest = dst / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
                count += 1
    else:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        count = sum(1 for _ in dst.rglob("*") if _.is_file())

    return count

def copy_file(src, dst):
    """Copy a single file."""
    src = Path(src)
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)

# ════════════════════════════════════════════════════════════
# BUILD STEPS
# ════════════════════════════════════════════════════════════

def step_clean():
    """Clean staging and output directories."""
    log_step("CLEAN — Removing previous build artifacts")
    clean_dir(STAGING_DIR)
    clean_dir(OUTPUT_DIR)
    log_ok("Clean complete")

def step_build_ime():
    """Build IME with PyInstaller."""
    log_step("STEP 1 — Building Varnaakshara IME (PyInstaller)")

    # Check PyInstaller
    result = run("pyinstaller --version", capture=True, check=False)
    if result.returncode != 0:
        log("PyInstaller not found, installing...")
        run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Check PyQt5
    try:
        import PyQt5
    except ImportError:
        log("PyQt5 not found, installing...")
        run([sys.executable, "-m", "pip", "install", "PyQt5"])

    # Build with PyInstaller (--onedir for reliability with Python DLLs)
    ime_main = PROJECT_ROOT / "varnaakshara_ime.py"
    icon_file = PROJECT_ROOT / "icon.ico"

    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--name", "Varnaakshara",
        "--icon", str(icon_file),
        "--add-data", f"{icon_file};.",
        "--add-data", f"{PROJECT_ROOT / 'transliteration.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'suggestions.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'suggestion_popup.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'suggestion_popup_qt.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'settings_ui.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'font_installer.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'updater.py'};.",
        "--add-data", f"{PROJECT_ROOT / 'launcher.py'};.",
        "--hidden-import", "suggestions",
        "--hidden-import", "suggestion_popup",
        "--hidden-import", "suggestion_popup_qt",
        "--hidden-import", "settings_ui",
        "--hidden-import", "transliteration",
        "--hidden-import", "font_installer",
        "--hidden-import", "updater",
        "--hidden-import", "faulthandler",
        str(ime_main),
    ]

    run(pyinstaller_args, cwd=PROJECT_ROOT)

    # Copy PyInstaller output to staging
    dist_dir = PROJECT_ROOT / "dist" / "Varnaakshara"
    if not dist_dir.exists():
        log_error(f"PyInstaller output not found at {dist_dir}")
        sys.exit(1)

    staging_ime = STAGING_DIR / "ime"
    count = copy_tree(dist_dir, staging_ime)
    log_ok(f"IME staged: {count} files → {staging_ime}")

def step_build_writer():
    """Build Writer with npm + electron-builder."""
    log_step("STEP 2 — Building Varnaakshara Writer (Electron)")

    writer_dir = PROJECT_ROOT / "writer"
    if not writer_dir.exists():
        log_warn("Writer directory not found, skipping")
        return

    # Install npm dependencies
    if not (writer_dir / "node_modules").exists():
        log("Installing npm dependencies...")
        run("npm install", cwd=writer_dir)

    # Build webpack bundle
    log("Building webpack bundle...")
    run("npm run build", cwd=writer_dir)

    # Package with electron-builder
    log("Packaging with electron-builder...")
    run("npm run package", cwd=writer_dir)

    # Find the unpacked Electron output
    # electron-builder outputs to writer/dist/win-unpacked/
    unpacked = writer_dir / "dist" / "win-unpacked"
    if not unpacked.exists():
        log_warn(f"Electron output not found at {unpacked}")
        log_warn("Trying alternative path: dist/Varnaakshara Writer-win32-x64/")
        unpacked = writer_dir / "dist" / "Varnaakshara Writer-win32-x64"

    if not unpacked.exists():
        log_error("Could not find packaged Writer output. Check electron-builder output.")
        sys.exit(1)

    # Copy to staging
    staging_writer = STAGING_DIR / "writer"
    count = copy_tree(unpacked, staging_writer)
    log_ok(f"Writer staged: {count} files → {staging_writer}")

    # Copy bridge script
    bridge_src = writer_dir / "src" / "bridge.py"
    if bridge_src.exists():
        staging_bridge = STAGING_DIR / "bridge"
        ensure_dir(staging_bridge)
        copy_file(bridge_src, staging_bridge / "bridge.py")
        log_ok("Bridge script staged")

def step_download_python():
    """Download embedded Python 3.11 if not cached."""
    log_step("STEP 3 — Embedded Python Runtime")

    staging_python = STAGING_DIR / "python"

    # Check cache first
    if PYTHON_EMBED_ZIP.exists():
        log(f"Using cached: {PYTHON_EMBED_ZIP}")
    else:
        log(f"Downloading embedded Python {PYTHON_VERSION}...")
        ensure_dir(PYTHON_CACHE_DIR)
        try:
            urllib.request.urlretrieve(PYTHON_EMBED_URL, str(PYTHON_EMBED_ZIP))
            log_ok(f"Downloaded: {PYTHON_EMBED_ZIP}")
        except Exception as e:
            log_error(f"Failed to download Python: {e}")
            log_warn("You can manually download from:")
            log_warn(f"  {PYTHON_EMBED_URL}")
            log_warn(f"  Save to: {PYTHON_EMBED_ZIP}")
            sys.exit(1)

    # Verify hash if configured
    if PYTHON_EMBED_SHA256:
        sha = hashlib.sha256(PYTHON_EMBED_ZIP.read_bytes()).hexdigest()
        if sha != PYTHON_EMBED_SHA256:
            log_error(f"SHA256 mismatch! Expected {PYTHON_EMBED_SHA256}, got {sha}")
            sys.exit(1)
        log_ok("SHA256 verified")

    # Extract to staging
    ensure_dir(staging_python)
    with zipfile.ZipFile(PYTHON_EMBED_ZIP, "r") as zf:
        zf.extractall(staging_python)
    log_ok(f"Extracted Python {PYTHON_VERSION} to {staging_python}")

    # Enable pip in embedded Python by uncommenting import site
    pth_file = staging_python / f"python311._pth"
    if pth_file.exists():
        content = pth_file.read_text()
        content = content.replace("#import site", "import site")
        pth_file.write_text(content)
        log("Enabled site-packages in embedded Python")

def step_stage_core():
    """Copy core engine and data files to staging."""
    log_step("STEP 4 — Staging Core Engine & Data")

    staging_core = STAGING_DIR / "core"

    # Copy engine
    engine_src = PROJECT_ROOT / "core" / "engine"
    if engine_src.exists():
        count = copy_tree(engine_src, staging_core / "engine")
        log_ok(f"Engine: {count} files")

    # Copy data
    data_src = PROJECT_ROOT / "core" / "data"
    if data_src.exists():
        count = copy_tree(data_src, staging_core / "data")
        log_ok(f"Data: {count} files")

    # Copy core __init__.py
    init_src = PROJECT_ROOT / "core" / "__init__.py"
    if init_src.exists():
        copy_file(init_src, staging_core / "__init__.py")

    # Copy IME module
    ime_src = PROJECT_ROOT / "ime"
    if ime_src.exists():
        count = copy_tree(ime_src, staging_core / "ime", pattern="*.py")
        log_ok(f"IME module: {count} files")

    # Copy top-level Python modules
    for module in [
        "transliteration.py",
        "suggestions.py",
        "suggestion_popup.py",
        "suggestion_popup_qt.py",
        "settings_ui.py",
        "font_installer.py",
        "updater.py",
        "launcher.py",
        "generate_data.py",
    ]:
        src = PROJECT_ROOT / module
        if src.exists():
            copy_file(src, staging_core / module)

    log_ok(f"Core staged to {staging_core}")

def step_stage_fonts():
    """Copy all font files to staging."""
    log_step("STEP 5 — Staging Font Files")

    staging_fonts = STAGING_DIR / "fonts"

    # Unicode fonts
    unicode_src = PROJECT_ROOT / "fonts" / "unicode"
    if unicode_src.exists():
        count = copy_tree(unicode_src, staging_fonts / "unicode")
        log_ok(f"Unicode fonts: {count} files")

    # Vedic fonts
    vedic_dst = staging_fonts / "vedic"
    ensure_dir(vedic_dst)
    vedic_count = 0
    for vf in ["NotoSansKannadaVedic.ttf", "NotoSansDevanagariVedic.ttf"]:
        src = PROJECT_ROOT / "fonts" / vf
        if src.exists():
            copy_file(src, vedic_dst / vf)
            vedic_count += 1
    log_ok(f"Vedic fonts: {vedic_count} files")

    # ANSI fonts
    ansi_src = PROJECT_ROOT / "fonts" / "ansi"
    if ansi_src.exists():
        count = copy_tree(ansi_src, staging_fonts / "ansi")
        log_ok(f"ANSI fonts: {count} files")

    # Generated weight variants
    generated_src = PROJECT_ROOT / "core" / "fonts" / "generated"
    if generated_src.exists():
        count = copy_tree(generated_src, staging_fonts / "generated")
        log_ok(f"Generated font weights: {count} files")

    # Summary
    total = sum(1 for _ in staging_fonts.rglob("*.ttf"))
    log_ok(f"Total fonts staged: {total}")

def step_compile_installer():
    """Run Inno Setup compiler."""
    log_step("STEP 6 — Compiling Installer (Inno Setup)")

    # Find iscc.exe
    iscc = None
    for path in ISCC_PATHS:
        if os.path.isfile(path):
            iscc = path
            break
        # Check if it's in PATH
        result = subprocess.run(
            ["where" if os.name == "nt" else "which", path],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            iscc = result.stdout.strip().split("\n")[0]
            break

    if not iscc:
        log_error("Inno Setup compiler (iscc.exe) not found!")
        log_error("Install Inno Setup 6.x from: https://jrsoftware.org/isinfo.php")
        log_error("Or add iscc to your PATH")
        sys.exit(1)

    log(f"Using Inno Setup: {iscc}")

    # Ensure output directory exists
    ensure_dir(OUTPUT_DIR)

    # Compile
    iss_file = INSTALLER_DIR / "varnaakshara.iss"
    run([iscc, str(iss_file)], cwd=INSTALLER_DIR)

    # Verify output
    expected_output = OUTPUT_DIR / "VarnaaksharaSetup-x64.exe"
    if expected_output.exists():
        size_mb = expected_output.stat().st_size / (1024 * 1024)
        log_ok(f"Installer created: {expected_output}")
        log_ok(f"Size: {size_mb:.1f} MB")
    else:
        log_error("Installer not found after compilation!")
        sys.exit(1)

# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Build Varnaakshara Suite installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python build.py                    Full build
  python build.py --skip-writer      IME only, no Writer
  python build.py --skip-ime         Rebuild Writer only
  python build.py --skip-iscc        Stage files without compiling
  python build.py --clean            Clean build from scratch
  python build.py --clean --skip-ime Skip IME rebuild after clean
        """,
    )
    parser.add_argument("--skip-ime", action="store_true", help="Skip IME PyInstaller build")
    parser.add_argument("--skip-writer", action="store_true", help="Skip Writer Electron build")
    parser.add_argument("--skip-iscc", action="store_true", help="Skip Inno Setup compilation")
    parser.add_argument("--clean", action="store_true", help="Clean build directories first")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    print(f"""
{Colors.BOLD}╔════════════════════════════════════════════════════════════╗
║        Varnaakshara Suite — Installer Builder v{VERSION}       ║
╚════════════════════════════════════════════════════════════╝{Colors.END}
""")

    log(f"Project root: {PROJECT_ROOT}")
    log(f"Staging dir:  {STAGING_DIR}")
    log(f"Output dir:   {OUTPUT_DIR}")

    # Clean if requested
    if args.clean:
        step_clean()
    else:
        ensure_dir(STAGING_DIR)
        ensure_dir(OUTPUT_DIR)

    # Step 1: Build IME
    if not args.skip_ime:
        step_build_ime()
    else:
        log_warn("Skipping IME build (--skip-ime)")
        # Check if staging has existing IME files
        if not (STAGING_DIR / "ime").exists():
            # Try to use existing dist output
            dist_dir = PROJECT_ROOT / "dist" / "Varnaakshara"
            if dist_dir.exists():
                copy_tree(dist_dir, STAGING_DIR / "ime")
                log("Using existing PyInstaller output from dist/")
            else:
                log_warn("No existing IME build found — installer may be incomplete")

    # Step 2: Build Writer
    if not args.skip_writer:
        step_build_writer()
    else:
        log_warn("Skipping Writer build (--skip-writer)")

    # Step 3: Download embedded Python
    step_download_python()

    # Step 4: Stage core engine & data
    step_stage_core()

    # Step 5: Stage fonts
    step_stage_fonts()

    # Step 6: Compile installer
    if not args.skip_iscc:
        step_compile_installer()
    else:
        log_warn("Skipping Inno Setup compilation (--skip-iscc)")
        log("Staging directory is ready for manual compilation")

    # Summary
    print(f"""
{Colors.GREEN}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗
║                    BUILD COMPLETE! ✓                       ║
╚════════════════════════════════════════════════════════════╝{Colors.END}
""")

    if not args.skip_iscc:
        output_exe = OUTPUT_DIR / "VarnaaksharaSetup-x64.exe"
        if output_exe.exists():
            log_ok(f"Installer: {output_exe}")
            log_ok(f"Size: {output_exe.stat().st_size / (1024 * 1024):.1f} MB")

    log("Staging directory contents:")
    for item in sorted(STAGING_DIR.rglob("*")):
        if item.is_dir():
            count = sum(1 for _ in item.iterdir() if _.is_file())
            if count > 0:
                rel = item.relative_to(STAGING_DIR)
                log(f"  {rel}/ ({count} files)")


if __name__ == "__main__":
    main()
