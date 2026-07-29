# Varnaakshara IME — Application Compatibility Matrix

## How It Works

Varnaakshara uses a system-wide `WH_KEYBOARD_LL` low-level keyboard hook to intercept keystrokes, then injects the transliterated output via `SendInput`. This approach works at the OS level — it doesn't depend on any app-specific API.

### Why This Matters for Compatibility

- **SendInput** simulates real keyboard events. Most applications accept these without issues.
- **Some apps** use custom text input frameworks (e.g., Chromium's IME handling, Java Swing) that may behave differently.
- **Protected/elevated apps** may not receive injected keystrokes if Varnaakshara is running at a lower privilege level.

## Compatibility Status

### ✅ Fully Compatible (Tested)

| Application | Version | Notes |
|---|---|---|
| **Notepad** | Windows 11 built-in | Perfect — the gold standard test |
| **Microsoft Word** | Office 365 | Full support including formatting |
| **WordPad** | Windows 11 built-in | Works perfectly |
| **Google Chrome** | Latest | Works in all text fields, address bar, and web apps |
| **Microsoft Edge** | Latest | Same engine as Chrome, works identically |
| **WhatsApp Desktop** | Latest | Electron-based, works via Chromium layer |
| **Telegram Desktop** | Latest | Works in message input |

### ⚠️ Expected Compatible (Architecture Predicts Success, Needs Formal Testing)

| Application | Reason | Risk |
|---|---|---|
| **Microsoft Excel** | SendInput works in cells, but cell commit behavior (Enter/Tab) may interact with buffer | Low — likely works, test cell navigation |
| **Microsoft PowerPoint** | Text boxes accept SendInput | Low |
| **LibreOffice Writer** | Standard Win32 text input | Low |
| **LibreOffice Calc** | Same concerns as Excel — cell navigation | Low-Medium |
| **Visual Studio Code** | Electron-based (Chromium), should work like Chrome | Low |
| **Sublime Text** | Standard Win32, known to work with keyboard hooks | Low |
| **Adobe InDesign** | Custom text engine, but SendInput at OS level should work | Medium |
| **Adobe Photoshop** | Text tool accepts OS-level input | Low |
| **Firefox** | Gecko engine handles keyboard differently than Chromium | Low-Medium |

### ❌ Known Limitations

| Scenario | Issue | Workaround |
|---|---|---|
| **Elevated apps (Run as Admin)** | If an app runs as Administrator and Varnaakshara doesn't, `SendInput` may be blocked by UIPI | Run Varnaakshara as Administrator |
| **Remote Desktop (RDP)** | Keyboard hook may not work across RDP sessions | Install Varnaakshara on the remote machine |
| **Virtual machines** | Keyboard hook is local to the host OS | Install inside the VM |
| **Game anti-cheat** | Some anti-cheat software blocks `SendInput` | Disable IME while gaming |
| **Full-screen DirectX/Vulkan** | Exclusive full-screen may bypass keyboard hook | Use windowed/borderless mode |

## Technical Details

### Input Method
- **Hook type:** `WH_KEYBOARD_LL` (low-level keyboard hook via `SetWindowsHookEx`)
- **Output method:** `SendInput` with `KEYEVENTF_UNICODE` flag
- **Injected event filtering:** `LLKHF_INJECTED` flag checked to avoid processing own output
- **Buffer management:** Diff-based — only erases/types what changed, minimizing visible flicker

### DPI Awareness
- Process declares `PROCESS_PER_MONITOR_DPI_AWARE` via `SetProcessDpiAwareness(2)`
- Suggestion popup positions scale with monitor DPI
- Popup clamps to screen bounds on multi-monitor setups

### Known App-Specific Behaviors
1. **Chrome/Edge:** `GetGUIThreadInfo` returns caret position correctly. `GetCaretPos` may return (0,0) — the 3-tier fallback handles this.
2. **Classic Win32 apps (Notepad, WordPad):** `GetCaretPos` is the primary method. Works perfectly.
3. **Electron apps:** Behave like Chrome. `GetGUIThreadInfo` method works.
4. **Java Swing apps:** May not expose caret position via Win32 APIs. Suggestion popup falls back to mouse cursor position.

## Testing Checklist

When testing a new application:

- [ ] Type a simple word (e.g., `namaste` → नमस्ते)
- [ ] Test backspace (should undo one transliteration step)
- [ ] Test suggestion popup appears near cursor
- [ ] Test language switching (Ctrl+1 through Ctrl+0)
- [ ] Test F11/F12 toggle (enable/disable IME)
- [ ] Test special characters: `|` (danda), `&` (avagraha), `OM.` (ॐ)
- [ ] Test in different input contexts (main editor, search box, dialog boxes)
- [ ] Test copy/paste doesn't interfere with transliteration buffer

---
*Last updated: v1.2.0 — June 18, 2026*
