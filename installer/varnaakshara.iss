; ════════════════════════════════════════════════════════════════════════
; Varnaakshara Suite Installer — Inno Setup 6.x Script
; Bundles: IME + Writer + Fonts (ANSI, Unicode, Vedic, Generated Weights)
; ════════════════════════════════════════════════════════════════════════
;
; Build prerequisites:
;   1. Run build.py to prepare staging directories
;   2. Compile with: iscc varnaakshara.iss
;
; Output: output\VarnaaksharaSetup-x64.exe
; ════════════════════════════════════════════════════════════════════════

#define SuiteVersion    "1.0.0"
#define SuiteName       "Varnaakshara Suite"
#define SuitePublisher  "Varnaakshara Project"
#define SuiteURL        "https://github.com/Exaggarate/Varnaakshara"
#define IMEExeName      "Varnaakshara.exe"
#define WriterExeName   "Varnaakshara Writer.exe"

; ── Staging paths (populated by build.py) ──
#define StagingDir      "staging"

[Setup]
; ── App Identity ──
AppId={{B2E9C47A-3F81-4DA6-A5C0-8E7F1D3B6A92}
AppName={#SuiteName}
AppVersion={#SuiteVersion}
AppVerName={#SuiteName} v{#SuiteVersion}
AppPublisher={#SuitePublisher}
AppPublisherURL={#SuiteURL}
AppSupportURL={#SuiteURL}/issues
AppUpdatesURL={#SuiteURL}/releases

; ── Installation ──
DefaultDirName={autopf}\Varnaakshara
DefaultGroupName=Varnaakshara
DisableProgramGroupPage=yes
AllowNoIcons=yes

; ── License & Info ──
LicenseFile=LICENSE.txt
InfoBeforeFile=README_INSTALL.txt

; ── Output ──
OutputDir=output
OutputBaseFilename=VarnaaksharaSetup-x64
SetupIconFile=icon.ico

; ── Compression ──
Compression=lzma2/ultra64
SolidCompression=yes
LZMANumBlockThreads=4

; ── Visual ──
WizardStyle=modern
WizardSizePercent=110,110
WizardImageFile=compiler:WizModernImage-IS.bmp
WizardSmallImageFile=compiler:WizModernSmallImage-IS.bmp

; ── Architecture ──
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0

; ── Privileges ──
; Admin preferred for system-wide font installation to {fonts};
; per-user fallback installs fonts to {autofonts}
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; ── Uninstaller ──
UninstallDisplayIcon={app}\{#IMEExeName}
UninstallDisplayName={#SuiteName}

; ── Misc ──
AppMutex=VarnaaksharaIME_SingleInstance_v2
CloseApplications=yes
RestartApplications=yes
CloseApplicationsFilter=Varnaakshara.exe,pythonw.exe,Varnaakshara Writer.exe
VersionInfoVersion={#SuiteVersion}.0
VersionInfoCompany={#SuitePublisher}
VersionInfoDescription=Varnaakshara Suite — Indian Script IME + Writer
VersionInfoCopyright=Copyright (c) 2026 Varnaakshara Project
VersionInfoProductName={#SuiteName}
VersionInfoProductVersion={#SuiteVersion}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
english.WelcomeLabel2=This will install {#SuiteName} on your computer.%n%nVarnaakshara (वर्णाक्षरः) is a free, system-wide Indian script input method and word processor suite.%n%nThe suite includes:%n  • Varnaakshara IME — Type in English, get Indian scripts%n  • Varnaakshara Writer — Word processor for Indian languages%n  • 130+ Indian script fonts%n%nSupports 12 Indian languages: Kannada, Hindi, Telugu, Tamil, Bengali, Gujarati, Malayalam, Marathi, Odia, Punjabi, Sanskrit, and Assamese.%n%nThis software is FREE and NOT FOR SALE.%n%nClick Next to continue.
english.FinishedHeadingLabel=Varnaakshara Suite has been installed! 🎉
english.FinishedLabel=वर्णाक्षरः — Thank you for installing Varnaakshara!%n%nThe suite has been installed with your selected components.%nYou can launch the IME from the Start Menu, Desktop, or system tray.%n%nHappy typing! 🙏

; ════════════════════════════════════════════════════════════
; COMPONENTS — User-selectable installation modules
; ════════════════════════════════════════════════════════════

[Types]
Name: "full";    Description: "Full installation (IME + Writer + All Fonts)"
Name: "compact"; Description: "Compact (IME + Essential Fonts only)"
Name: "custom";  Description: "Custom installation"; Flags: iscustom

[Components]
; Core IME — always installed
Name: "ime";            Description: "Varnaakshara IME (system-wide input method)";           Types: full compact custom; Flags: fixed
Name: "ime\python";     Description: "Embedded Python 3.11 runtime";                          Types: full compact custom; Flags: fixed

; Writer — optional, default selected
Name: "writer";         Description: "Varnaakshara Writer (word processor for Indian languages)"; Types: full custom

; Fonts
Name: "fonts";          Description: "Indian Script Font Families";                            Types: full compact custom
Name: "fonts\unicode";  Description: "Unicode fonts (Noto Sans — 7 scripts)";                 Types: full compact custom; Flags: fixed
Name: "fonts\vedic";    Description: "Vedic fonts (patched Noto Sans with Vedic diacritics)";  Types: full compact custom
Name: "fonts\ansi";     Description: "ANSI legacy fonts (23 curated Indian script fonts)";       Types: full custom
Name: "fonts\weights";  Description: "Extended weight variants (Regular through Black)";       Types: full custom

; ════════════════════════════════════════════════════════════
; TASKS — Optional user choices
; ════════════════════════════════════════════════════════════

[Tasks]
Name: "desktopicon";    Description: "Create &desktop shortcuts";                GroupDescription: "Additional shortcuts:"; Flags: checkedonce
Name: "startupentry";   Description: "Start Varnaakshara IME when Windows starts"; GroupDescription: "Startup:";             Flags: checkedonce

; ════════════════════════════════════════════════════════════
; FILES — Everything that gets installed
; ════════════════════════════════════════════════════════════

[Files]
; ── IME Application (PyInstaller --onedir output) ──
Source: "{#StagingDir}\ime\*"; DestDir: "{app}\ime"; Components: ime; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Embedded Python 3.11 ──
Source: "{#StagingDir}\python\*"; DestDir: "{app}\python"; Components: ime\python; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Core Engine & Data (shared between IME and Writer) ──
Source: "{#StagingDir}\core\*"; DestDir: "{app}\core"; Components: ime; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Writer Application (Electron) ──
Source: "{#StagingDir}\writer\*"; DestDir: "{app}\writer"; Components: writer; Flags: ignoreversion recursesubdirs createallsubdirs

; ── Writer Bridge (Python ↔ Electron) ──
Source: "{#StagingDir}\bridge\bridge.py"; DestDir: "{app}\bridge"; Components: writer; Flags: ignoreversion

; ── Application Icon ──
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; ── Updater Config ──
Source: "updater_config.json"; DestDir: "{app}"; Flags: ignoreversion

; ── License ──
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

; ──────────────────────────────────────────────────────────
; FONTS — Installed to Windows Fonts directory ({fonts})
; Uses FontInstall flag for proper GDI registration
; ──────────────────────────────────────────────────────────

; ── Unicode Fonts (Noto Sans) ──
Source: "{#StagingDir}\fonts\unicode\NotoSansBengali.ttf";          DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Bengali (Varnaakshara)";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\unicode\NotoSansDevanagari.ttf";       DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Devanagari (Varnaakshara)";  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\unicode\NotoSansGujarati.ttf";         DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Gujarati (Varnaakshara)";    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\unicode\NotoSansKannada-Regular.ttf";  DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Kannada (Varnaakshara)";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\unicode\NotoSansMalayalam.ttf";        DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Malayalam (Varnaakshara)";    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\unicode\NotoSansTamil.ttf";            DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Tamil (Varnaakshara)";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\unicode\NotoSansTelugu.ttf";           DestDir: "{fonts}"; Components: fonts\unicode; FontInstall: "Noto Sans Telugu (Varnaakshara)";       Flags: onlyifdoesntexist uninsneveruninstall

; ── Vedic Fonts ──
Source: "{#StagingDir}\fonts\vedic\NotoSansKannadaVedic.ttf";       DestDir: "{fonts}"; Components: fonts\vedic; FontInstall: "Noto Sans Kannada Vedic (Varnaakshara)";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\vedic\NotoSansDevanagariVedic.ttf";    DestDir: "{fonts}"; Components: fonts\vedic; FontInstall: "Noto Sans Devanagari Vedic (Varnaakshara)";  Flags: onlyifdoesntexist uninsneveruninstall

; ── ANSI Legacy Fonts (Varnaakshara series — installed to {fonts}) ──
Source: "{#StagingDir}\fonts\ansi\brhaknd.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 01";    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhben.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Bengali Lipi 01";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhbenrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Bengali Lipi 02";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhbglr.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 02";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhdevrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Devanagari Lipi 01";      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhguj.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Gujarati Lipi 01";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhgujrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Gujarati Lipi 02";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhkai.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 03";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhknd.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 04";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhkndb.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 05";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhknde.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 06";   Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhkndrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 07";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhmal.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Malayalam Lipi 01";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhmale.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Malayalam Lipi 02";  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhmalrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Malayalam Lipi 03";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhsknd.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 08";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhtab.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Tamil Lipi 01";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhtabe.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Tamil Lipi 02";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhtabrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Tamil Lipi 03";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhtel.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Telugu Lipi 01";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhtele.ttf";   DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Telugu Lipi 02";    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhtelrn.ttf";  DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Telugu Lipi 03";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\ansi\brhvjy.ttf";    DestDir: "{fonts}"; Components: fonts\ansi; FontInstall: "Varnaakshara Kannada Lipi 09";     Flags: onlyifdoesntexist uninsneveruninstall

; ── Generated Font Weight Variants ──
; Each font family has 5 weights: Regular, Medium, SemiBold, Bold, Black
; Installed to {app}\fonts\generated\ and registered via Pascal Script

; brhaknd weights
Source: "{#StagingDir}\fonts\generated\brhaknd\brhaknd-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 01";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhaknd\brhaknd-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 01 Medium";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhaknd\brhaknd-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 01 SemiBold";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhaknd\brhaknd-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 01 Bold";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhaknd\brhaknd-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 01 Black";        Flags: onlyifdoesntexist uninsneveruninstall

; brhben weights
Source: "{#StagingDir}\fonts\generated\brhben\brhben-Regular.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 01";                     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhben\brhben-Medium.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 01 Medium";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhben\brhben-SemiBold.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 01 SemiBold";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhben\brhben-Bold.ttf";        DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 01 Bold";                Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhben\brhben-Black.ttf";       DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 01 Black";               Flags: onlyifdoesntexist uninsneveruninstall

; brhbenrn weights
Source: "{#StagingDir}\fonts\generated\brhbenrn\brhbenrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 02";               Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbenrn\brhbenrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 02 Medium";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbenrn\brhbenrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 02 SemiBold";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbenrn\brhbenrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 02 Bold";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbenrn\brhbenrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Bengali Lipi 02 Black";          Flags: onlyifdoesntexist uninsneveruninstall

; brhbglr weights
Source: "{#StagingDir}\fonts\generated\brhbglr\brhbglr-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 02";                  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbglr\brhbglr-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 02 Medium";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbglr\brhbglr-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 02 SemiBold";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbglr\brhbglr-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 02 Bold";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhbglr\brhbglr-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 02 Black";             Flags: onlyifdoesntexist uninsneveruninstall

; brhdevrn weights
Source: "{#StagingDir}\fonts\generated\brhdevrn\brhdevrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Devanagari Lipi 01";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhdevrn\brhdevrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Devanagari Lipi 01 Medium";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhdevrn\brhdevrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Devanagari Lipi 01 SemiBold";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhdevrn\brhdevrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Devanagari Lipi 01 Bold";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhdevrn\brhdevrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Devanagari Lipi 01 Black";        Flags: onlyifdoesntexist uninsneveruninstall

; brhguj weights
Source: "{#StagingDir}\fonts\generated\brhguj\brhguj-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 01";                     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhguj\brhguj-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 01 Medium";               Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhguj\brhguj-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 01 SemiBold";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhguj\brhguj-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 01 Bold";                 Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhguj\brhguj-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 01 Black";                Flags: onlyifdoesntexist uninsneveruninstall

; brhgujrn weights
Source: "{#StagingDir}\fonts\generated\brhgujrn\brhgujrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 02";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhgujrn\brhgujrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 02 Medium";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhgujrn\brhgujrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 02 SemiBold";      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhgujrn\brhgujrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 02 Bold";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhgujrn\brhgujrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Gujarati Lipi 02 Black";         Flags: onlyifdoesntexist uninsneveruninstall

; brhkai weights
Source: "{#StagingDir}\fonts\generated\brhkai\brhkai-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 03";                  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkai\brhkai-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 03 Medium";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkai\brhkai-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 03 SemiBold";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkai\brhkai-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 03 Bold";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkai\brhkai-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 03 Black";             Flags: onlyifdoesntexist uninsneveruninstall

; brhknd weights
Source: "{#StagingDir}\fonts\generated\brhknd\brhknd-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 04";                      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknd\brhknd-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 04 Medium";                Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknd\brhknd-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 04 SemiBold";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknd\brhknd-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 05";                  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknd\brhknd-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 04 Black";                 Flags: onlyifdoesntexist uninsneveruninstall

; brhknde weights
Source: "{#StagingDir}\fonts\generated\brhknde\brhknde-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 06";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknde\brhknde-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 06 Medium";      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknde\brhknde-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 06 SemiBold";    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknde\brhknde-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 06 Bold";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhknde\brhknde-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 06 Black";       Flags: onlyifdoesntexist uninsneveruninstall

; brhkndrn weights
Source: "{#StagingDir}\fonts\generated\brhkndrn\brhkndrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 07";               Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkndrn\brhkndrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 07 Medium";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkndrn\brhkndrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 07 SemiBold";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkndrn\brhkndrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 07 Bold";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhkndrn\brhkndrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 07 Black";          Flags: onlyifdoesntexist uninsneveruninstall

; brhmal weights
Source: "{#StagingDir}\fonts\generated\brhmal\brhmal-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 01";                    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmal\brhmal-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 01 Medium";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmal\brhmal-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 01 SemiBold";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmal\brhmal-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 01 Bold";                Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmal\brhmal-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 01 Black";               Flags: onlyifdoesntexist uninsneveruninstall

; brhmale weights
Source: "{#StagingDir}\fonts\generated\brhmale\brhmale-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 02";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmale\brhmale-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 02 Medium";    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmale\brhmale-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 02 SemiBold";  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmale\brhmale-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 02 Bold";      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmale\brhmale-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 02 Black";     Flags: onlyifdoesntexist uninsneveruninstall

; brhmalrn weights
Source: "{#StagingDir}\fonts\generated\brhmalrn\brhmalrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 03";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmalrn\brhmalrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 03 Medium";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmalrn\brhmalrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 03 SemiBold";      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmalrn\brhmalrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 03 Bold";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhmalrn\brhmalrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Malayalam Lipi 03 Black";         Flags: onlyifdoesntexist uninsneveruninstall

; brhsknd weights
Source: "{#StagingDir}\fonts\generated\brhsknd\brhsknd-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 08";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhsknd\brhsknd-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 08 Medium";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhsknd\brhsknd-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 08 SemiBold";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhsknd\brhsknd-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 08 Bold";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhsknd\brhsknd-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 08 Black";        Flags: onlyifdoesntexist uninsneveruninstall

; brhtab weights
Source: "{#StagingDir}\fonts\generated\brhtab\brhtab-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 01";                        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtab\brhtab-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 01 Medium";                  Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtab\brhtab-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 01 SemiBold";                Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtab\brhtab-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 01 Bold";                    Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtab\brhtab-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 01 Black";                   Flags: onlyifdoesntexist uninsneveruninstall

; brhtabe weights
Source: "{#StagingDir}\fonts\generated\brhtabe\brhtabe-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 02";              Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabe\brhtabe-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 02 Medium";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabe\brhtabe-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 02 SemiBold";      Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabe\brhtabe-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 02 Bold";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabe\brhtabe-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 02 Black";         Flags: onlyifdoesntexist uninsneveruninstall

; brhtabrn weights
Source: "{#StagingDir}\fonts\generated\brhtabrn\brhtabrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 03";                 Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabrn\brhtabrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 03 Medium";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabrn\brhtabrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 03 SemiBold";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabrn\brhtabrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 03 Bold";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtabrn\brhtabrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Tamil Lipi 03 Black";            Flags: onlyifdoesntexist uninsneveruninstall

; brhtel weights
Source: "{#StagingDir}\fonts\generated\brhtel\brhtel-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 01";                       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtel\brhtel-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 01 Medium";                 Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtel\brhtel-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 01 SemiBold";               Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtel\brhtel-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 01 Bold";                   Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtel\brhtel-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 01 Black";                  Flags: onlyifdoesntexist uninsneveruninstall

; brhtele weights
Source: "{#StagingDir}\fonts\generated\brhtele\brhtele-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 02";             Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtele\brhtele-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 02 Medium";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtele\brhtele-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 02 SemiBold";     Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtele\brhtele-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 02 Bold";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtele\brhtele-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 02 Black";        Flags: onlyifdoesntexist uninsneveruninstall

; brhtelrn weights
Source: "{#StagingDir}\fonts\generated\brhtelrn\brhtelrn-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 03";                Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtelrn\brhtelrn-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 03 Medium";          Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtelrn\brhtelrn-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 03 SemiBold";        Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtelrn\brhtelrn-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 03 Bold";            Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhtelrn\brhtelrn-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Telugu Lipi 03 Black";           Flags: onlyifdoesntexist uninsneveruninstall

; brhvjy weights
Source: "{#StagingDir}\fonts\generated\brhvjy\brhvjy-Regular.ttf";   DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 09";               Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhvjy\brhvjy-Medium.ttf";    DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 09 Medium";         Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhvjy\brhvjy-SemiBold.ttf";  DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 09 SemiBold";       Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhvjy\brhvjy-Bold.ttf";      DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 09 Bold";           Flags: onlyifdoesntexist uninsneveruninstall
Source: "{#StagingDir}\fonts\generated\brhvjy\brhvjy-Black.ttf";     DestDir: "{fonts}"; Components: fonts\weights; FontInstall: "Varnaakshara Kannada Lipi 09 Black";          Flags: onlyifdoesntexist uninsneveruninstall

; ════════════════════════════════════════════════════════════
; DIRECTORIES
; ════════════════════════════════════════════════════════════

[Dirs]
Name: "{app}\ime"
Name: "{app}\python"
Name: "{app}\core"
Name: "{app}\writer"; Components: writer
Name: "{app}\bridge"; Components: writer

; ════════════════════════════════════════════════════════════
; SHORTCUTS — Start Menu + Desktop
; ════════════════════════════════════════════════════════════

[Icons]
; ── Start Menu ──
Name: "{group}\Varnaakshara IME";        Filename: "{app}\ime\{#IMEExeName}";      Comment: "Varnaakshara — Indian Script Input Method";   IconFilename: "{app}\icon.ico"
Name: "{group}\Varnaakshara Writer";     Filename: "{app}\writer\{#WriterExeName}"; Comment: "Varnaakshara Writer — Indian Language Word Processor"; Components: writer; IconFilename: "{app}\icon.ico"
Name: "{group}\Varnaakshara Settings";   Filename: "{app}\ime\{#IMEExeName}";      Parameters: "--settings"; Comment: "Open Varnaakshara Settings"; IconFilename: "{app}\icon.ico"
Name: "{group}\Uninstall Varnaakshara";  Filename: "{uninstallexe}";               Comment: "Uninstall Varnaakshara Suite"

; ── Desktop (optional) ──
Name: "{autodesktop}\Varnaakshara IME";    Filename: "{app}\ime\{#IMEExeName}";      Tasks: desktopicon; Comment: "Varnaakshara — Indian Script IME";       IconFilename: "{app}\icon.ico"
Name: "{autodesktop}\Varnaakshara Writer"; Filename: "{app}\writer\{#WriterExeName}"; Tasks: desktopicon; Components: writer; Comment: "Varnaakshara Writer"; IconFilename: "{app}\icon.ico"

; ════════════════════════════════════════════════════════════
; REGISTRY — Startup + App paths
; ════════════════════════════════════════════════════════════

[Registry]
; Auto-start IME at Windows login (optional)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Varnaakshara"; ValueData: """{app}\ime\{#IMEExeName}"""; Flags: uninsdeletevalue; Tasks: startupentry

; App Paths registration (allows launching via Win+R or search)
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\{#IMEExeName}"; ValueType: string; ValueName: ""; ValueData: "{app}\ime\{#IMEExeName}"; Flags: uninsdeletekey
Root: HKLM; Subkey: "Software\Microsoft\Windows\CurrentVersion\App Paths\{#IMEExeName}"; ValueType: string; ValueName: "Path"; ValueData: "{app}\ime"; Flags: uninsdeletekey

; Varnaakshara version info (for updater and other tools)
Root: HKCU; Subkey: "Software\Varnaakshara"; ValueType: string; ValueName: "Version"; ValueData: "{#SuiteVersion}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Varnaakshara"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Varnaakshara"; ValueType: string; ValueName: "WriterInstalled"; ValueData: "1"; Components: writer; Flags: uninsdeletekey

; ════════════════════════════════════════════════════════════
; RUN — Post-install actions
; ════════════════════════════════════════════════════════════

[Run]
; Launch IME after installation (optional)
Filename: "{app}\ime\{#IMEExeName}"; Description: "Launch Varnaakshara IME"; Flags: nowait postinstall skipifsilent unchecked
; Launch Writer after installation (optional)
Filename: "{app}\writer\{#WriterExeName}"; Description: "Launch Varnaakshara Writer"; Flags: nowait postinstall skipifsilent unchecked; Components: writer

; ════════════════════════════════════════════════════════════
; UNINSTALL DELETE — Clean removal of leftover files
; ════════════════════════════════════════════════════════════

[UninstallDelete]
Type: filesandordirs; Name: "{app}\ime"
Type: filesandordirs; Name: "{app}\python"
Type: filesandordirs; Name: "{app}\core"
Type: filesandordirs; Name: "{app}\writer"
Type: filesandordirs; Name: "{app}\bridge"
Type: filesandordirs; Name: "{app}"

; ════════════════════════════════════════════════════════════
; PASCAL SCRIPT — Font GDI registration + cleanup
; ════════════════════════════════════════════════════════════

[Code]
const
  WM_FONTCHANGE  = $001D;
  HWND_BROADCAST = $FFFF;

// ── GDI font functions ──
function AddFontResourceW(lpszFilename: String): Integer;
  external 'AddFontResourceW@gdi32.dll stdcall';

function RemoveFontResourceW(lpszFilename: String): Integer;
  external 'RemoveFontResourceW@gdi32.dll stdcall';

function SendMessageTimeout(hWnd: LongInt; Msg: LongInt; wParam: LongInt;
  lParam: LongInt; fuFlags: LongInt; uTimeout: LongInt; var lpdwResult: LongInt): LongInt;
  external 'SendMessageTimeoutW@user32.dll stdcall';

// ── Notify all apps about font changes ──
procedure BroadcastFontChange;
var
  Dummy: LongInt;
begin
  // SMTO_ABORTIFHUNG = 2, timeout 5000ms
  SendMessageTimeout(HWND_BROADCAST, WM_FONTCHANGE, 0, 0, 2, 5000, Dummy);
end;

// ── Register all .ttf in a directory with GDI ──
procedure RegisterFontsInDir(Dir: String);
var
  FindRec: TFindRec;
  FontPath: String;
begin
  if FindFirst(Dir + '\*.ttf', FindRec) then
  begin
    try
      repeat
        FontPath := Dir + '\' + FindRec.Name;
        if AddFontResourceW(FontPath) > 0 then
          Log('GDI registered: ' + FontPath)
        else
          Log('GDI register FAILED: ' + FontPath);
      until not FindNext(FindRec);
    finally
      FindClose(FindRec);
    end;
  end;
end;

// ── Unregister all .ttf in a directory from GDI ──
procedure UnregisterFontsInDir(Dir: String);
var
  FindRec: TFindRec;
  FontPath: String;
begin
  if FindFirst(Dir + '\*.ttf', FindRec) then
  begin
    try
      repeat
        FontPath := Dir + '\' + FindRec.Name;
        RemoveFontResourceW(FontPath);
        Log('GDI unregistered: ' + FontPath);
      until not FindNext(FindRec);
    finally
      FindClose(FindRec);
    end;
  end;
end;

// ── Kill running Varnaakshara processes before uninstall ──
procedure KillRunningProcesses;
var
  ResultCode: Integer;
begin
  Exec('taskkill.exe', '/F /IM Varnaakshara.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Exec('taskkill.exe', '/F /IM "Varnaakshara Writer.exe"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Exec('taskkill.exe', '/F /IM pythonw.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

// ── Post-install: broadcast font availability ──
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    Log('Post-install: broadcasting font change notification...');
    BroadcastFontChange;
    Log('Font change broadcast complete');
  end;
end;

// ── Pre-uninstall: kill processes and unregister GDI fonts ──
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    Log('Uninstall: killing running processes...');
    KillRunningProcesses;

    Log('Uninstall: broadcasting font change notification...');
    BroadcastFontChange;
    Log('Uninstall cleanup complete');
  end;
end;

// ── Version comparison for upgrade detection ──
function InitializeSetup: Boolean;
var
  InstalledVersion: String;
begin
  Result := True;

  if RegQueryStringValue(HKCU, 'Software\Varnaakshara', 'Version', InstalledVersion) then
  begin
    if InstalledVersion = '{#SuiteVersion}' then
    begin
      if MsgBox('Varnaakshara v{#SuiteVersion} is already installed.' + #13#10 +
                'Do you want to reinstall or repair?',
                mbConfirmation, MB_YESNO) = IDNO then
      begin
        Result := False;
      end;
    end
    else
    begin
      MsgBox('Upgrading Varnaakshara from v' + InstalledVersion + ' to v{#SuiteVersion}.',
             mbInformation, MB_OK);
    end;
  end;
end;
