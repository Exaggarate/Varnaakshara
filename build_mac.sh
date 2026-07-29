#!/bin/bash
# ============================================================
# Varnaakshara macOS Build Script
# ============================================================
# Builds a standalone .app bundle using PyInstaller.
#
# Prerequisites:
#   - Python 3.8+
#   - macOS 10.15+
#   - Xcode Command Line Tools (xcode-select --install)
#
# Usage:
#   chmod +x build_mac.sh
#   ./build_mac.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_NAME="Varnaakshara"
VERSION="2.0.0"
IDENTIFIER="com.varnaakshara.ime"

echo "============================================"
echo "  Varnaakshara macOS Build Script v${VERSION}"
echo "============================================"
echo ""

# ---- Check we're on macOS ----
if [[ "$(uname)" != "Darwin" ]]; then
    echo "ERROR: This script must be run on macOS."
    exit 1
fi

# ---- Check Python ----
PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" &> /dev/null; then
    echo "ERROR: Python 3 not found. Install from python.org or via Homebrew."
    exit 1
fi

echo "Python: $($PYTHON --version)"
echo ""

# ---- Install dependencies ----
echo "Installing dependencies..."
"$PYTHON" -m pip install --upgrade pip
"$PYTHON" -m pip install \
    PyQt5>=5.15.0 \
    pyobjc-framework-Quartz>=9.0 \
    pyobjc-framework-Cocoa>=9.0 \
    pyinstaller>=5.0

echo ""
echo "Dependencies installed."

# ---- Create Info.plist with Accessibility usage description ----
PLIST_PATH="${SCRIPT_DIR}/Info.plist"
cat > "$PLIST_PATH" << 'PLIST_EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>Varnaakshara</string>
    <key>CFBundleDisplayName</key>
    <string>Varnaakshara IME</string>
    <key>CFBundleIdentifier</key>
    <string>com.varnaakshara.ime</string>
    <key>CFBundleVersion</key>
    <string>2.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleExecutable</key>
    <string>Varnaakshara</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>LSUIElement</key>
    <true/>
    <key>NSAccessibilityUsageDescription</key>
    <string>Varnaakshara needs Accessibility access to intercept keyboard events and provide real-time Indian script transliteration.</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
PLIST_EOF

echo "Created Info.plist"

# ---- Build with PyInstaller ----
echo ""
echo "Building ${APP_NAME}.app with PyInstaller..."
echo ""

cd "$SCRIPT_DIR"

"$PYTHON" -m PyInstaller \
    --windowed \
    --onefile \
    --name "$APP_NAME" \
    --osx-bundle-identifier "$IDENTIFIER" \
    --add-data "transliteration.py:." \
    --add-data "suggestions.py:." \
    --add-data "suggestion_popup_qt.py:." \
    --hidden-import "Quartz" \
    --hidden-import "Cocoa" \
    --hidden-import "ApplicationServices" \
    --hidden-import "PyQt5" \
    --hidden-import "PyQt5.QtWidgets" \
    --hidden-import "PyQt5.QtCore" \
    --hidden-import "PyQt5.QtGui" \
    varnaakshara_ime_mac.py

# ---- Copy Info.plist into the .app bundle ----
APP_BUNDLE="dist/${APP_NAME}.app"
if [[ -d "$APP_BUNDLE" ]]; then
    cp "$PLIST_PATH" "${APP_BUNDLE}/Contents/Info.plist"
    echo "Copied Info.plist into ${APP_BUNDLE}/Contents/"
fi

# ---- Copy dictionary database if it exists ----
DICT_DB="$HOME/.varnaakshara/dictionary.db"
if [[ -f "$DICT_DB" && -d "$APP_BUNDLE" ]]; then
    mkdir -p "${APP_BUNDLE}/Contents/Resources"
    cp "$DICT_DB" "${APP_BUNDLE}/Contents/Resources/"
    echo "Copied dictionary.db into Resources/"
fi

echo ""
echo "============================================"
echo "  Build complete!"
echo "============================================"
echo ""
echo "Output: ${SCRIPT_DIR}/dist/${APP_NAME}.app"
echo ""
echo "To run:"
echo "  open dist/${APP_NAME}.app"
echo ""
echo "IMPORTANT: On first launch, macOS will ask for"
echo "Accessibility permission. Grant it in:"
echo "  System Settings → Privacy & Security → Accessibility"
echo ""
echo "To distribute, you may want to:"
echo "  1. Code-sign: codesign --force --deep --sign - dist/${APP_NAME}.app"
echo "  2. Create DMG: hdiutil create -volname ${APP_NAME} -srcfolder dist/${APP_NAME}.app -ov ${APP_NAME}.dmg"
echo ""

# ---- Cleanup ----
rm -f "$PLIST_PATH"
echo "Build artifacts in: ${SCRIPT_DIR}/dist/ and ${SCRIPT_DIR}/build/"
