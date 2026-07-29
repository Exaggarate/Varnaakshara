; ════════════════════════════════════════════════════════════
; Varnaakshara Installer — Inno Setup Script
; Professional Windows installer with font bundling
; ════════════════════════════════════════════════════════════

#define MyAppName "Varnaakshara"
#define MyAppVersion "1.3.0"
#define MyAppPublisher "Varnaakshara Project"
#define MyAppURL "mailto:aksaram.folios@gmail.com"
#define MyAppExeName "Varnaakshara.exe"

[Setup]
; App identity
AppId={{7A8E3C21-4F6B-4D92-B8A1-9E3F5C7D2A01}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}

; Install location
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; License and info
LicenseFile=LICENSE.txt
InfoBeforeFile=README_INSTALL.txt

; Output
OutputDir=output
OutputBaseFilename=Varnaakshara_Setup_v{#MyAppVersion}
SetupIconFile=icon.ico

; Compression
Compression=lzma2/ultra64
SolidCompression=yes

; Visual
WizardStyle=modern
WizardSizePercent=110,110

; Privileges — per-user install (no admin needed)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Uninstaller
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

; Misc
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
AppMutex=VarnaaksharaIME_SingleInstance_v2
CloseApplications=yes
RestartApplications=yes
CloseApplicationsFilter=Varnaakshara.exe,pythonw.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
english.WelcomeLabel2=This will install [name] on your computer.%n%nVarnaakshara (वर्णाक्षरः) is a free, system-wide Indian script input method.%nType in English — get output in 12 Indian languages including Kannada, Hindi, Telugu, Tamil, Bengali, Gujarati, Malayalam, Marathi, Odia, Punjabi, Sanskrit and Assamese.%n%nBoth Baraha and ITRANS transliteration schemes supported.%nNo admin rights required. No internet needed.%n%nThis software is FREE and NOT FOR SALE.%n%nClick Next to continue.
english.FinishedHeadingLabel=Varnaakshara has been installed! 🎉
english.FinishedLabel=वर्णाक्षरः — Thank you for installing Varnaakshara!%n%nThe application has been installed along with Indian script fonts.%nYou can launch it from the Start Menu or Desktop shortcut.%n%nHappy typing! 🙏

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: checkedonce
Name: "startupentry"; Description: "Start Varnaakshara when Windows starts"; GroupDescription: "Startup:"; Flags: checkedonce

[Files]
; Main application (--onedir: entire folder with exe + _internal DLLs)
Source: "dist\Varnaakshara\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Application icon
Source: "..\icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Unicode fonts — install to app's own fonts folder
Source: "..\fonts\unicode\NotoSansBengali.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion
Source: "..\fonts\unicode\NotoSansDevanagari.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion
Source: "..\fonts\unicode\NotoSansGujarati.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion
Source: "..\fonts\unicode\NotoSansKannada-Regular.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion
Source: "..\fonts\unicode\NotoSansMalayalam.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion
Source: "..\fonts\unicode\NotoSansTamil.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion
Source: "..\fonts\unicode\NotoSansTelugu.ttf"; DestDir: "{app}\fonts\unicode"; Flags: ignoreversion

; Vedic fonts (patched Noto Sans with corrected U+1CDA glyph)
Source: "..\fonts\NotoSansKannadaVedic.ttf"; DestDir: "{app}\fonts"; Flags: ignoreversion
Source: "..\fonts\NotoSansDevanagariVedic.ttf"; DestDir: "{app}\fonts"; Flags: ignoreversion

; ANSI fonts (legacy) — separate from existing fonts
Source: "..\fonts\ansi\*.ttf"; DestDir: "{app}\fonts\ansi"; Flags: ignoreversion

; License
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
Name: "{app}\fonts"
Name: "{app}\fonts\unicode"
Name: "{app}\fonts\ansi"

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Varnaakshara — Indian Script IME"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "Varnaakshara — Indian Script IME"

[Registry]
; Startup entry (optional)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "Varnaakshara"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startupentry

; Font registration — each font registered under HKCU (per-user, no admin)
; Unicode fonts
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Bengali (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansBengali.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Devanagari (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansDevanagari.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Gujarati (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansGujarati.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Kannada (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansKannada-Regular.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Malayalam (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansMalayalam.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Tamil (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansTamil.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Telugu (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\unicode\NotoSansTelugu.ttf"; Flags: uninsdeletevalue

; Vedic fonts (patched)
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Kannada Vedic (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\NotoSansKannadaVedic.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "Noto Sans Devanagari Vedic (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\NotoSansDevanagariVedic.ttf"; Flags: uninsdeletevalue

; ANSI fonts — registered with "(Varnaakshara)" suffix to avoid conflicts
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Akhand Kannada (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhaknd.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Bengali (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhben.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Bengali RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhbenrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Bangalore (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhbglr.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Devanagari RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhdevrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Gujarati (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhguj.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Gujarati RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhgujrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Kai Kannada (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhkai.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Kannada (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhknd.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Kannada Bold (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhkndb.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Kannada Extended (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhknde.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Kannada RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhkndrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Malayalam (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhmal.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Malayalam Extended (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhmale.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Malayalam RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhmalrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Siddha Kannada (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhsknd.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Tamil (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhtab.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Tamil Extended (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhtabe.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Tamil RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhtabrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Telugu (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhtel.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Telugu Extended (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhtele.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Telugu RN (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhtelrn.ttf"; Flags: uninsdeletevalue
Root: HKCU; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\Fonts"; ValueType: string; ValueName: "BRH Vijaya Kannada (Varnaakshara) (TrueType)"; ValueData: "{app}\fonts\ansi\brhvjy.ttf"; Flags: uninsdeletevalue

[Run]
; Launch after install (optional)
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
// Pascal Script — register fonts with GDI on install, notify apps
const
  WM_FONTCHANGE = $001D;

function AddFontResourceEx(lpszFilename: String; fl: Cardinal; pdv: Cardinal): Integer;
  external 'AddFontResourceExW@gdi32.dll stdcall';

function RemoveFontResourceEx(lpszFilename: String; fl: Cardinal; pdv: Cardinal): Integer;
  external 'RemoveFontResourceExW@gdi32.dll stdcall';

function SendMessage(hWnd: LongInt; Msg: LongInt; wParam: LongInt; lParam: LongInt): LongInt;
  external 'SendMessageW@user32.dll stdcall';

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
        AddFontResourceEx(FontPath, 0, 0);
        Log('Registered font: ' + FontPath);
      until not FindNext(FindRec);
    finally
      FindClose(FindRec);
    end;
  end;
end;

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
        RemoveFontResourceEx(FontPath, 0, 0);
        Log('Unregistered font: ' + FontPath);
      until not FindNext(FindRec);
    finally
      FindClose(FindRec);
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Register all bundled fonts with GDI for immediate use
    RegisterFontsInDir(ExpandConstant('{app}\fonts\unicode'));
    RegisterFontsInDir(ExpandConstant('{app}\fonts'));
    RegisterFontsInDir(ExpandConstant('{app}\fonts\ansi'));
    
    // Notify all applications about new fonts
    SendMessage($FFFF, WM_FONTCHANGE, 0, 0);
    
    Log('All fonts registered and applications notified');
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    // Unregister fonts before removal
    UnregisterFontsInDir(ExpandConstant('{app}\fonts\unicode'));
    UnregisterFontsInDir(ExpandConstant('{app}\fonts'));
    UnregisterFontsInDir(ExpandConstant('{app}\fonts\ansi'));
    
    // Notify all applications
    SendMessage($FFFF, WM_FONTCHANGE, 0, 0);
    
    Log('All fonts unregistered');
  end;
end;
