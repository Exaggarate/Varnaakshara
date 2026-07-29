; ════════════════════════════════════════════════════════════════════════
; Varnaakshara Suite Installer — NSIS Script (Alternative to Inno Setup)
; Bundles: IME + Writer + Fonts (ANSI, Unicode, Vedic, Generated Weights)
; ════════════════════════════════════════════════════════════════════════
;
; Compile with: makensis varnaakshara.nsi
; Requires: NSIS 3.x with MUI2
;
; IMPORTANT: Run build.py first to populate the staging/ directory.
; ════════════════════════════════════════════════════════════════════════

!include "MUI2.nsh"
!include "Sections.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"
!include "x64.nsh"

; ══════════════════════════════════════
; DEFINES
; ══════════════════════════════════════

!define PRODUCT_NAME        "Varnaakshara Suite"
!define PRODUCT_VERSION     "1.0.0"
!define PRODUCT_PUBLISHER   "Varnaakshara Project"
!define PRODUCT_WEB_SITE    "https://github.com/Exaggarate/Varnaakshara"
!define PRODUCT_UNINST_KEY  "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_DIR_REGKEY  "Software\Varnaakshara"
!define IME_EXE_NAME        "Varnaakshara.exe"
!define WRITER_EXE_NAME     "Varnaakshara Writer.exe"
!define STAGING_DIR         "staging"

; ══════════════════════════════════════
; GENERAL SETTINGS
; ══════════════════════════════════════

Name "${PRODUCT_NAME} v${PRODUCT_VERSION}"
OutFile "output\VarnaaksharaSetup-x64.exe"
InstallDir "$PROGRAMFILES64\Varnaakshara"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" "InstallPath"
ShowInstDetails show
ShowUnInstDetails show
RequestExecutionLevel admin
SetCompressor /SOLID lzma
SetCompressorDictSize 64

; Unicode support (NSIS 3.x)
Unicode true

; 64-bit only
!ifdef NSIS_PACKEDVERSION
  ManifestSupportedOS all
!endif

; ══════════════════════════════════════
; VERSION INFO
; ══════════════════════════════════════

VIProductVersion "${PRODUCT_VERSION}.0"
VIAddVersionKey "ProductName"     "${PRODUCT_NAME}"
VIAddVersionKey "CompanyName"     "${PRODUCT_PUBLISHER}"
VIAddVersionKey "LegalCopyright"  "Copyright (c) 2026 ${PRODUCT_PUBLISHER}"
VIAddVersionKey "FileDescription" "Varnaakshara Suite Installer"
VIAddVersionKey "FileVersion"     "${PRODUCT_VERSION}"
VIAddVersionKey "ProductVersion"  "${PRODUCT_VERSION}"

; ══════════════════════════════════════
; MUI2 INTERFACE SETTINGS
; ══════════════════════════════════════

!define MUI_ABORTWARNING
!define MUI_ICON "icon.ico"
!define MUI_UNICON "icon.ico"

; Welcome page text
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${PRODUCT_NAME}"
!define MUI_WELCOMEPAGE_TEXT "This wizard will install ${PRODUCT_NAME} v${PRODUCT_VERSION} on your computer.$\r$\n$\r$\nVarnaakshara ($\"वर्णाक्षरः$\") is a free, system-wide Indian script input method and word processor suite.$\r$\n$\r$\nThe suite includes:$\r$\n  • Varnaakshara IME — Type in English, get Indian scripts$\r$\n  • Varnaakshara Writer — Word processor for Indian languages$\r$\n  • 130+ Indian script fonts$\r$\n$\r$\nThis software is FREE and NOT FOR SALE.$\r$\n$\r$\nClick Next to continue."

; Finish page settings
!define MUI_FINISHPAGE_RUN "$INSTDIR\ime\${IME_EXE_NAME}"
!define MUI_FINISHPAGE_RUN_TEXT "Launch Varnaakshara IME"
!define MUI_FINISHPAGE_SHOWREADME ""
!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
!define MUI_FINISHPAGE_LINK "Visit ${PRODUCT_WEB_SITE}"
!define MUI_FINISHPAGE_LINK_LOCATION "${PRODUCT_WEB_SITE}"

; ══════════════════════════════════════
; PAGES
; ══════════════════════════════════════

; Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Language
!insertmacro MUI_LANGUAGE "English"

; ══════════════════════════════════════
; ARCHITECTURE CHECK
; ══════════════════════════════════════

Function .onInit
  ${IfNot} ${RunningX64}
    MessageBox MB_OK|MB_ICONSTOP "Varnaakshara requires a 64-bit version of Windows."
    Abort
  ${EndIf}

  ${IfNot} ${AtLeastWin10}
    MessageBox MB_OK|MB_ICONSTOP "Varnaakshara requires Windows 10 or later."
    Abort
  ${EndIf}

  ; Check for running instances
  FindWindow $0 "" "Varnaakshara"
  ${If} $0 != 0
    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
      "Varnaakshara is currently running. It will be closed before installation.$\r$\nClick OK to continue or Cancel to abort." \
      IDOK +2
    Abort
    ; Kill running processes
    nsExec::ExecToLog 'taskkill /F /IM "${IME_EXE_NAME}"'
    nsExec::ExecToLog 'taskkill /F /IM "${WRITER_EXE_NAME}"'
    nsExec::ExecToLog 'taskkill /F /IM pythonw.exe'
    Sleep 1000
  ${EndIf}
FunctionEnd

; ══════════════════════════════════════════════════════════════
; SECTION: Varnaakshara IME (Core — always installed)
; ══════════════════════════════════════════════════════════════

Section "Varnaakshara IME (required)" SecIME
  SectionIn RO  ; Read-only — cannot be deselected

  SetOutPath "$INSTDIR\ime"
  File /r "${STAGING_DIR}\ime\*.*"

  ; Embedded Python runtime
  SetOutPath "$INSTDIR\python"
  File /r "${STAGING_DIR}\python\*.*"

  ; Core engine and data
  SetOutPath "$INSTDIR\core"
  File /r "${STAGING_DIR}\core\*.*"

  ; Icon
  SetOutPath "$INSTDIR"
  File "icon.ico"
  File "LICENSE.txt"
  File "updater_config.json"

  ; ── Start Menu shortcuts ──
  CreateDirectory "$SMPROGRAMS\Varnaakshara"
  CreateShortCut "$SMPROGRAMS\Varnaakshara\Varnaakshara IME.lnk" \
    "$INSTDIR\ime\${IME_EXE_NAME}" "" "$INSTDIR\icon.ico"
  CreateShortCut "$SMPROGRAMS\Varnaakshara\Varnaakshara Settings.lnk" \
    "$INSTDIR\ime\${IME_EXE_NAME}" "--settings" "$INSTDIR\icon.ico"
  CreateShortCut "$SMPROGRAMS\Varnaakshara\Uninstall Varnaakshara.lnk" \
    "$INSTDIR\Uninstall.exe"

  ; ── Registry ──
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayName" "${PRODUCT_NAME}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "UninstallString" '"$INSTDIR\Uninstall.exe"'
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\icon.ico"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr HKLM "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "NoRepair" 1

  ; Version info for updater
  WriteRegStr HKCU "${PRODUCT_DIR_REGKEY}" "Version" "${PRODUCT_VERSION}"
  WriteRegStr HKCU "${PRODUCT_DIR_REGKEY}" "InstallPath" "$INSTDIR"

  ; Calculate installed size
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "${PRODUCT_UNINST_KEY}" "EstimatedSize" $0

  ; Write uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"
SectionEnd

; ══════════════════════════════════════════════════════════════
; SECTION: Varnaakshara Writer (optional, default selected)
; ══════════════════════════════════════════════════════════════

Section "Varnaakshara Writer" SecWriter
  SetOutPath "$INSTDIR\writer"
  File /r "${STAGING_DIR}\writer\*.*"

  ; Bridge script
  SetOutPath "$INSTDIR\bridge"
  File "${STAGING_DIR}\bridge\bridge.py"

  ; Start Menu shortcut
  CreateShortCut "$SMPROGRAMS\Varnaakshara\Varnaakshara Writer.lnk" \
    "$INSTDIR\writer\${WRITER_EXE_NAME}" "" "$INSTDIR\icon.ico"

  ; Registry
  WriteRegStr HKCU "${PRODUCT_DIR_REGKEY}" "WriterInstalled" "1"
SectionEnd

; ══════════════════════════════════════════════════════════════
; SECTION GROUP: Fonts
; ══════════════════════════════════════════════════════════════

SectionGroup "Indian Script Fonts" SecFonts

  ; ── Unicode Fonts (Noto Sans) ──
  Section "Unicode fonts (Noto Sans)" SecFontsUnicode
    SectionIn RO  ; Required

    SetOutPath "$FONTS"
    File "${STAGING_DIR}\fonts\unicode\NotoSansBengali.ttf"
    File "${STAGING_DIR}\fonts\unicode\NotoSansDevanagari.ttf"
    File "${STAGING_DIR}\fonts\unicode\NotoSansGujarati.ttf"
    File "${STAGING_DIR}\fonts\unicode\NotoSansKannada-Regular.ttf"
    File "${STAGING_DIR}\fonts\unicode\NotoSansMalayalam.ttf"
    File "${STAGING_DIR}\fonts\unicode\NotoSansTamil.ttf"
    File "${STAGING_DIR}\fonts\unicode\NotoSansTelugu.ttf"

    ; Register Unicode fonts
    !insertmacro InstallTTFFont "$FONTS\NotoSansBengali.ttf"          "Noto Sans Bengali (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansDevanagari.ttf"       "Noto Sans Devanagari (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansGujarati.ttf"         "Noto Sans Gujarati (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansKannada-Regular.ttf"  "Noto Sans Kannada (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansMalayalam.ttf"        "Noto Sans Malayalam (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansTamil.ttf"            "Noto Sans Tamil (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansTelugu.ttf"           "Noto Sans Telugu (Varnaakshara) (TrueType)"
  SectionEnd

  ; ── Vedic Fonts ──
  Section "Vedic fonts (patched Noto Sans)" SecFontsVedic
    SetOutPath "$FONTS"
    File "${STAGING_DIR}\fonts\vedic\NotoSansKannadaVedic.ttf"
    File "${STAGING_DIR}\fonts\vedic\NotoSansDevanagariVedic.ttf"

    !insertmacro InstallTTFFont "$FONTS\NotoSansKannadaVedic.ttf"    "Noto Sans Kannada Vedic (Varnaakshara) (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\NotoSansDevanagariVedic.ttf" "Noto Sans Devanagari Vedic (Varnaakshara) (TrueType)"
  SectionEnd

  ; ── ANSI Legacy Fonts (Varnaakshara series) ──
  Section "ANSI legacy fonts (Varnaakshara series)" SecFontsANSI
    SetOutPath "$FONTS"
    File "${STAGING_DIR}\fonts\ansi\brhaknd.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhben.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhbenrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhbglr.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhdevrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhguj.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhgujrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhkai.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhknd.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhkndb.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhknde.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhkndrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhmal.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhmale.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhmalrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhsknd.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhtab.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhtabe.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhtabrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhtel.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhtele.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhtelrn.ttf"
    File "${STAGING_DIR}\fonts\ansi\brhvjy.ttf"

    ; Register ANSI fonts
    !insertmacro InstallTTFFont "$FONTS\brhaknd.ttf"   "Varnaakshara Kannada Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhben.ttf"    "Varnaakshara Bengali Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhbenrn.ttf"  "Varnaakshara Bengali Lipi 02 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhbglr.ttf"   "Varnaakshara Kannada Lipi 02 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhdevrn.ttf"  "Varnaakshara Devanagari Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhguj.ttf"    "Varnaakshara Gujarati Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhgujrn.ttf"  "Varnaakshara Gujarati Lipi 02 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhkai.ttf"    "Varnaakshara Kannada Lipi 03 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhknd.ttf"    "Varnaakshara Kannada Lipi 04 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhkndb.ttf"   "Varnaakshara Kannada Lipi 05 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhknde.ttf"   "Varnaakshara Kannada Lipi 06 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhkndrn.ttf"  "Varnaakshara Kannada Lipi 07 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhmal.ttf"    "Varnaakshara Malayalam Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhmale.ttf"   "Varnaakshara Malayalam Lipi 02 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhmalrn.ttf"  "Varnaakshara Malayalam Lipi 03 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhsknd.ttf"   "Varnaakshara Kannada Lipi 08 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhtab.ttf"    "Varnaakshara Tamil Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhtabe.ttf"   "Varnaakshara Tamil Lipi 02 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhtabrn.ttf"  "Varnaakshara Tamil Lipi 03 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhtel.ttf"    "Varnaakshara Telugu Lipi 01 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhtele.ttf"   "Varnaakshara Telugu Lipi 02 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhtelrn.ttf"  "Varnaakshara Telugu Lipi 03 (TrueType)"
    !insertmacro InstallTTFFont "$FONTS\brhvjy.ttf"    "Varnaakshara Kannada Lipi 09 (TrueType)"
  SectionEnd

  ; ── Generated Weight Variants ──
  Section "Extended weight variants" SecFontsWeights
    SetOutPath "$FONTS"

    ; Install all generated font weights from each family subdirectory
    ; Using /r to recurse through family subdirectories
    File /r "${STAGING_DIR}\fonts\generated\*.*"

    ; Register generated fonts dynamically via nsExec
    ; Each family has: Regular, Medium, SemiBold, Bold, Black
    Call RegisterGeneratedFonts
  SectionEnd

SectionGroupEnd

; ══════════════════════════════════════════════════════════════
; SECTION: Desktop Shortcuts (optional)
; ══════════════════════════════════════════════════════════════

Section "Desktop shortcuts" SecDesktop
  CreateShortCut "$DESKTOP\Varnaakshara IME.lnk" \
    "$INSTDIR\ime\${IME_EXE_NAME}" "" "$INSTDIR\icon.ico"

  ; Only create Writer shortcut if Writer is installed
  SectionGetFlags ${SecWriter} $0
  IntOp $0 $0 & ${SF_SELECTED}
  ${If} $0 == ${SF_SELECTED}
    CreateShortCut "$DESKTOP\Varnaakshara Writer.lnk" \
      "$INSTDIR\writer\${WRITER_EXE_NAME}" "" "$INSTDIR\icon.ico"
  ${EndIf}
SectionEnd

; ══════════════════════════════════════════════════════════════
; SECTION: Startup Entry (optional, default on)
; ══════════════════════════════════════════════════════════════

Section "Start with Windows" SecStartup
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Run" \
    "Varnaakshara" '"$INSTDIR\ime\${IME_EXE_NAME}"'
SectionEnd

; ══════════════════════════════════════════════════════════════
; SECTION DESCRIPTIONS
; ══════════════════════════════════════════════════════════════

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecIME}           "The core Varnaakshara Input Method Engine. Type in English and get output in 12 Indian scripts. This component is required."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecWriter}        "A free word processor designed for Indian languages. Built with Lexical editor and Electron."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFonts}         "Indian script font families for proper text rendering."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFontsUnicode}  "Noto Sans Unicode fonts for 7 Indian scripts (Bengali, Devanagari, Gujarati, Kannada, Malayalam, Tamil, Telugu)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFontsVedic}    "Patched Noto Sans fonts with corrected Vedic diacritic glyphs (U+1CDA)."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFontsANSI}     "23 legacy Varnaakshara ANSI fonts for backward compatibility with older documents."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecFontsWeights}  "Extended weight variants (Regular, Medium, SemiBold, Bold, Black) for each font family. 110 fonts total."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop}       "Create desktop shortcuts for quick access to IME and Writer."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartup}       "Automatically start the IME when you log in to Windows."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; ══════════════════════════════════════════════════════════════
; FONT INSTALLATION MACRO
; ══════════════════════════════════════════════════════════════

; Macro: Install a TrueType font and register it
!macro InstallTTFFont FontFile FontName
  ; Add font resource for current session
  System::Call "gdi32::AddFontResourceW(w '${FontFile}') i .r0"
  ; Register in registry for persistence across reboots
  WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" \
    "${FontName}" "${FontFile}"
!macroend

; ══════════════════════════════════════════════════════════════
; FUNCTION: Register generated font weight variants
; ══════════════════════════════════════════════════════════════

Function RegisterGeneratedFonts
  ; Generated fonts are in $FONTS\generated\<family>\<family>-<weight>.ttf
  ; We iterate through known families and weights

  ; Define families and their display names
  !define FONT_WEIGHTS "Regular Medium SemiBold Bold Black"

  ; Helper: register one family's weights
  !macro RegFontFamily prefix displayName
    !define _idx 0
    System::Call "gdi32::AddFontResourceW(w '$FONTS\${prefix}-Regular.ttf') i .r0"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "${displayName} (TrueType)" "$FONTS\${prefix}-Regular.ttf"
    System::Call "gdi32::AddFontResourceW(w '$FONTS\${prefix}-Medium.ttf') i .r0"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "${displayName} Medium (TrueType)" "$FONTS\${prefix}-Medium.ttf"
    System::Call "gdi32::AddFontResourceW(w '$FONTS\${prefix}-SemiBold.ttf') i .r0"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "${displayName} SemiBold (TrueType)" "$FONTS\${prefix}-SemiBold.ttf"
    System::Call "gdi32::AddFontResourceW(w '$FONTS\${prefix}-Bold.ttf') i .r0"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "${displayName} Bold (TrueType)" "$FONTS\${prefix}-Bold.ttf"
    System::Call "gdi32::AddFontResourceW(w '$FONTS\${prefix}-Black.ttf') i .r0"
    WriteRegStr HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "${displayName} Black (TrueType)" "$FONTS\${prefix}-Black.ttf"
  !macroend

  !insertmacro RegFontFamily "brhaknd"  "Varnaakshara Kannada Lipi 01"
  !insertmacro RegFontFamily "brhben"   "Varnaakshara Bengali Lipi 01"
  !insertmacro RegFontFamily "brhbenrn" "Varnaakshara Bengali Lipi 02"
  !insertmacro RegFontFamily "brhbglr"  "Varnaakshara Kannada Lipi 02"
  !insertmacro RegFontFamily "brhdevrn" "Varnaakshara Devanagari Lipi 01"
  !insertmacro RegFontFamily "brhguj"   "Varnaakshara Gujarati Lipi 01"
  !insertmacro RegFontFamily "brhgujrn" "Varnaakshara Gujarati Lipi 02"
  !insertmacro RegFontFamily "brhkai"   "Varnaakshara Kannada Lipi 03"
  !insertmacro RegFontFamily "brhknd"   "Varnaakshara Kannada Lipi 04"
  !insertmacro RegFontFamily "brhknde"  "Varnaakshara Kannada Lipi 06"
  !insertmacro RegFontFamily "brhkndrn" "Varnaakshara Kannada Lipi 07"
  !insertmacro RegFontFamily "brhmal"   "Varnaakshara Malayalam Lipi 01"
  !insertmacro RegFontFamily "brhmale"  "Varnaakshara Malayalam Lipi 02"
  !insertmacro RegFontFamily "brhmalrn" "Varnaakshara Malayalam Lipi 03"
  !insertmacro RegFontFamily "brhsknd"  "Varnaakshara Kannada Lipi 08"
  !insertmacro RegFontFamily "brhtab"   "Varnaakshara Tamil Lipi 01"
  !insertmacro RegFontFamily "brhtabe"  "Varnaakshara Tamil Lipi 02"
  !insertmacro RegFontFamily "brhtabrn" "Varnaakshara Tamil Lipi 03"
  !insertmacro RegFontFamily "brhtel"   "Varnaakshara Telugu Lipi 01"
  !insertmacro RegFontFamily "brhtele"  "Varnaakshara Telugu Lipi 02"
  !insertmacro RegFontFamily "brhtelrn" "Varnaakshara Telugu Lipi 03"
  !insertmacro RegFontFamily "brhvjy"   "Varnaakshara Kannada Lipi 09"

  ; Broadcast WM_FONTCHANGE to all windows
  SendMessage ${HWND_BROADCAST} ${WM_FONTCHANGE} 0 0 /TIMEOUT=5000
FunctionEnd

; ══════════════════════════════════════════════════════════════
; UNINSTALLER
; ══════════════════════════════════════════════════════════════

Section "Uninstall"
  ; Kill running processes
  nsExec::ExecToLog 'taskkill /F /IM "${IME_EXE_NAME}"'
  nsExec::ExecToLog 'taskkill /F /IM "${WRITER_EXE_NAME}"'
  nsExec::ExecToLog 'taskkill /F /IM pythonw.exe'
  Sleep 1000

  ; ── Remove startup registry entry ──
  DeleteRegValue HKCU "Software\Microsoft\Windows\CurrentVersion\Run" "Varnaakshara"

  ; ── Unregister and remove Unicode fonts ──
  !macro RemoveTTFFont FontFile FontRegName
    System::Call "gdi32::RemoveFontResourceW(w '${FontFile}') i .r0"
    DeleteRegValue HKLM "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" "${FontRegName}"
    Delete "${FontFile}"
  !macroend

  !insertmacro RemoveTTFFont "$FONTS\NotoSansBengali.ttf"          "Noto Sans Bengali (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansDevanagari.ttf"       "Noto Sans Devanagari (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansGujarati.ttf"         "Noto Sans Gujarati (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansKannada-Regular.ttf"  "Noto Sans Kannada (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansMalayalam.ttf"        "Noto Sans Malayalam (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansTamil.ttf"            "Noto Sans Tamil (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansTelugu.ttf"           "Noto Sans Telugu (Varnaakshara) (TrueType)"

  ; ── Unregister and remove Vedic fonts ──
  !insertmacro RemoveTTFFont "$FONTS\NotoSansKannadaVedic.ttf"    "Noto Sans Kannada Vedic (Varnaakshara) (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\NotoSansDevanagariVedic.ttf" "Noto Sans Devanagari Vedic (Varnaakshara) (TrueType)"

  ; ── Unregister and remove ANSI fonts ──
  !insertmacro RemoveTTFFont "$FONTS\brhaknd.ttf"   "Varnaakshara Kannada Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhben.ttf"    "Varnaakshara Bengali Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhbenrn.ttf"  "Varnaakshara Bengali Lipi 02 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhbglr.ttf"   "Varnaakshara Kannada Lipi 02 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhdevrn.ttf"  "Varnaakshara Devanagari Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhguj.ttf"    "Varnaakshara Gujarati Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhgujrn.ttf"  "Varnaakshara Gujarati Lipi 02 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhkai.ttf"    "Varnaakshara Kannada Lipi 03 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhknd.ttf"    "Varnaakshara Kannada Lipi 04 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhkndb.ttf"   "Varnaakshara Kannada Lipi 05 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhknde.ttf"   "Varnaakshara Kannada Lipi 06 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhkndrn.ttf"  "Varnaakshara Kannada Lipi 07 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhmal.ttf"    "Varnaakshara Malayalam Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhmale.ttf"   "Varnaakshara Malayalam Lipi 02 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhmalrn.ttf"  "Varnaakshara Malayalam Lipi 03 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhsknd.ttf"   "Varnaakshara Kannada Lipi 08 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhtab.ttf"    "Varnaakshara Tamil Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhtabe.ttf"   "Varnaakshara Tamil Lipi 02 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhtabrn.ttf"  "Varnaakshara Tamil Lipi 03 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhtel.ttf"    "Varnaakshara Telugu Lipi 01 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhtele.ttf"   "Varnaakshara Telugu Lipi 02 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhtelrn.ttf"  "Varnaakshara Telugu Lipi 03 (TrueType)"
  !insertmacro RemoveTTFFont "$FONTS\brhvjy.ttf"    "Varnaakshara Kannada Lipi 09 (TrueType)"

  ; ── Unregister and remove generated font weights ──
  !macro RemoveGenFontFamily prefix displayName
    !insertmacro RemoveTTFFont "$FONTS\${prefix}-Regular.ttf"  "${displayName} (TrueType)"
    !insertmacro RemoveTTFFont "$FONTS\${prefix}-Medium.ttf"   "${displayName} Medium (TrueType)"
    !insertmacro RemoveTTFFont "$FONTS\${prefix}-SemiBold.ttf" "${displayName} SemiBold (TrueType)"
    !insertmacro RemoveTTFFont "$FONTS\${prefix}-Bold.ttf"     "${displayName} Bold (TrueType)"
    !insertmacro RemoveTTFFont "$FONTS\${prefix}-Black.ttf"    "${displayName} Black (TrueType)"
  !macroend

  !insertmacro RemoveGenFontFamily "brhaknd"  "Varnaakshara Kannada Lipi 01"
  !insertmacro RemoveGenFontFamily "brhben"   "Varnaakshara Bengali Lipi 01"
  !insertmacro RemoveGenFontFamily "brhbenrn" "Varnaakshara Bengali Lipi 02"
  !insertmacro RemoveGenFontFamily "brhbglr"  "Varnaakshara Kannada Lipi 02"
  !insertmacro RemoveGenFontFamily "brhdevrn" "Varnaakshara Devanagari Lipi 01"
  !insertmacro RemoveGenFontFamily "brhguj"   "Varnaakshara Gujarati Lipi 01"
  !insertmacro RemoveGenFontFamily "brhgujrn" "Varnaakshara Gujarati Lipi 02"
  !insertmacro RemoveGenFontFamily "brhkai"   "Varnaakshara Kannada Lipi 03"
  !insertmacro RemoveGenFontFamily "brhknd"   "Varnaakshara Kannada Lipi 04"
  !insertmacro RemoveGenFontFamily "brhknde"  "Varnaakshara Kannada Lipi 06"
  !insertmacro RemoveGenFontFamily "brhkndrn" "Varnaakshara Kannada Lipi 07"
  !insertmacro RemoveGenFontFamily "brhmal"   "Varnaakshara Malayalam Lipi 01"
  !insertmacro RemoveGenFontFamily "brhmale"  "Varnaakshara Malayalam Lipi 02"
  !insertmacro RemoveGenFontFamily "brhmalrn" "Varnaakshara Malayalam Lipi 03"
  !insertmacro RemoveGenFontFamily "brhsknd"  "Varnaakshara Kannada Lipi 08"
  !insertmacro RemoveGenFontFamily "brhtab"   "Varnaakshara Tamil Lipi 01"
  !insertmacro RemoveGenFontFamily "brhtabe"  "Varnaakshara Tamil Lipi 02"
  !insertmacro RemoveGenFontFamily "brhtabrn" "Varnaakshara Tamil Lipi 03"
  !insertmacro RemoveGenFontFamily "brhtel"   "Varnaakshara Telugu Lipi 01"
  !insertmacro RemoveGenFontFamily "brhtele"  "Varnaakshara Telugu Lipi 02"
  !insertmacro RemoveGenFontFamily "brhtelrn" "Varnaakshara Telugu Lipi 03"
  !insertmacro RemoveGenFontFamily "brhvjy"   "Varnaakshara Kannada Lipi 09"

  ; Broadcast font change
  SendMessage ${HWND_BROADCAST} ${WM_FONTCHANGE} 0 0 /TIMEOUT=5000

  ; ── Remove shortcuts ──
  Delete "$DESKTOP\Varnaakshara IME.lnk"
  Delete "$DESKTOP\Varnaakshara Writer.lnk"
  RMDir /r "$SMPROGRAMS\Varnaakshara"

  ; ── Remove installed files ──
  RMDir /r "$INSTDIR\ime"
  RMDir /r "$INSTDIR\python"
  RMDir /r "$INSTDIR\core"
  RMDir /r "$INSTDIR\writer"
  RMDir /r "$INSTDIR\bridge"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\LICENSE.txt"
  Delete "$INSTDIR\updater_config.json"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"

  ; ── Remove registry entries ──
  DeleteRegKey HKLM "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKCU "${PRODUCT_DIR_REGKEY}"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\${IME_EXE_NAME}"
SectionEnd
