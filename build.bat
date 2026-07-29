@echo off
echo ============================================
echo   Varnaakshara IME v1.2.0 - Build Script
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Install Python 3.8+ first.
    pause
    exit /b 1
)

:: Install dependencies
echo Installing dependencies...
pip install PyQt5 pyinstaller
echo.

:: Build IME (system tray version) — MUST use --onedir (not --onefile)
:: Python 3.14's python314.dll fails to load from _MEI temp extraction
echo Building Varnaakshara.exe (System Tray IME)...
pyinstaller --noconfirm --onedir --windowed ^
    --name "Varnaakshara" ^
    --icon "icon.ico" ^
    --add-data "icon.ico;." ^
    --add-data "transliteration.py;." ^
    --add-data "suggestions.py;." ^
    --add-data "suggestion_popup.py;." ^
    --add-data "settings_ui.py;." ^
    --add-data "font_installer.py;." ^
    --add-data "updater.py;." ^
    --hidden-import "suggestions" ^
    --hidden-import "suggestion_popup" ^
    --hidden-import "settings_ui" ^
    --hidden-import "transliteration" ^
    --hidden-import "font_installer" ^
    --hidden-import "updater" ^
    --hidden-import "faulthandler" ^
    varnaakshara_ime.py

echo.
if not exist "dist\Varnaakshara\Varnaakshara.exe" (
    echo ============================================
    echo   BUILD FAILED - check errors above
    echo ============================================
    pause
    exit /b 1
)

echo BUILD SUCCESS! Copying to installer...

:: Copy onedir output to installer/dist/ for Inno Setup
if exist "installer\dist\Varnaakshara" rmdir /s /q "installer\dist\Varnaakshara"
mkdir "installer\dist\Varnaakshara" 2>nul
xcopy /s /e /y "dist\Varnaakshara\*" "installer\dist\Varnaakshara\" >nul

echo.
echo ============================================
echo   BUILD SUCCESS!
echo   Output: installer\dist\Varnaakshara\
echo.
echo   Next: Run Inno Setup on installer\varnaakshara_setup.iss
echo ============================================
echo.
pause
