"""
WindowsIME — Windows-specific Varnaakshara IME implementation.

Extends VarnaaksharaIMEBase with:
- WH_KEYBOARD_LL hook via SetWindowsHookExW (ctypes)
- SendInput with KEYEVENTF_UNICODE for text injection
- AttachThreadInput + GetFocus for target window detection
- GetGUIThreadInfo / GetCaretPos for caret position
- Per-monitor DPI awareness via shcore
- Windows CreateMutex single-instance check

Architecture mirrors the proven varnaakshara_ime.py approach.
"""

import sys
import os
import ctypes
import ctypes.wintypes as wt
import threading

from .ime_base import (
    VarnaaksharaIMEBase, LANGUAGES, SUPPORTED_LANGUAGES,
    _dbg, setup_debug_log, grapheme_len,
    INPUT_MODE_INSCRIPT,
)

# ============================================================
# Win32 Constants
# ============================================================
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
WM_CHAR = 0x0102

VK_BACK = 0x08
VK_TAB = 0x09
VK_RETURN = 0x0D
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_MENU = 0x12   # Alt
VK_LSHIFT = 0xA0
VK_RSHIFT = 0xA1
VK_LCONTROL = 0xA2
VK_RCONTROL = 0xA3
VK_LMENU = 0xA4
VK_RMENU = 0xA5
VK_CAPITAL = 0x14
VK_ESCAPE = 0x1B
VK_SPACE = 0x20
VK_LEFT = 0x25
VK_UP = 0x26
VK_RIGHT = 0x27
VK_DOWN = 0x28
VK_DELETE = 0x2E
VK_HOME = 0x24
VK_END = 0x23
VK_PRIOR = 0x21   # Page Up
VK_NEXT = 0x22    # Page Down
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_OEM_3 = 0xC0   # `/~

NAV_KEYS = frozenset({VK_LEFT, VK_UP, VK_RIGHT, VK_DOWN, VK_HOME, VK_END,
                      VK_DELETE, VK_ESCAPE, VK_TAB, VK_PRIOR, VK_NEXT})

LLKHF_INJECTED = 0x00000010

# Ctrl+number → language mapping (VK codes)
CTRL_LANG_MAP = {
    0x31: 'assamese',  0x32: 'bengali',   0x33: 'gujarati',
    0x34: 'hindi',     0x35: 'kannada',   0x36: 'malayalam',
    0x37: 'marathi',   0x38: 'odia',      0x39: 'punjabi',
    0x30: 'sanskrit',  0xBD: 'tamil',     0xBB: 'telugu',
}


# ============================================================
# Win32 Structures
# ============================================================
class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ('vkCode', wt.DWORD),
        ('scanCode', wt.DWORD),
        ('flags', wt.DWORD),
        ('time', wt.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]

HOOKPROC = ctypes.CFUNCTYPE(ctypes.c_long, ctypes.c_int,
                            wt.WPARAM, wt.LPARAM)


# ============================================================
# Win32 API declarations
# ============================================================
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, wt.HINSTANCE, wt.DWORD]
user32.SetWindowsHookExW.restype = wt.HHOOK
user32.CallNextHookEx.argtypes = [wt.HHOOK, ctypes.c_int, wt.WPARAM, wt.LPARAM]
user32.CallNextHookEx.restype = ctypes.c_long
user32.UnhookWindowsHookEx.argtypes = [wt.HHOOK]
user32.UnhookWindowsHookEx.restype = wt.BOOL
user32.GetForegroundWindow.restype = wt.HWND
user32.GetFocus.restype = wt.HWND
user32.GetWindowThreadProcessId.restype = wt.DWORD
user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
user32.AttachThreadInput.argtypes = [wt.DWORD, wt.DWORD, wt.BOOL]
user32.AttachThreadInput.restype = wt.BOOL
user32.PostMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.PostMessageW.restype = wt.BOOL
user32.SendMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.SendMessageW.restype = wt.LPARAM
user32.GetKeyboardState.argtypes = [ctypes.POINTER(ctypes.c_ubyte * 256)]
user32.GetKeyboardState.restype = wt.BOOL
user32.ToUnicode.argtypes = [wt.UINT, wt.UINT, ctypes.POINTER(ctypes.c_ubyte * 256),
                             ctypes.c_wchar_p, ctypes.c_int, wt.UINT]
user32.ToUnicode.restype = ctypes.c_int
kernel32.GetModuleHandleW.restype = wt.HMODULE
kernel32.GetCurrentThreadId.restype = wt.DWORD


# ============================================================
# SendInput structures
# ============================================================
INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', ctypes.c_long), ('dy', ctypes.c_long),
        ('mouseData', wt.DWORD), ('dwFlags', wt.DWORD),
        ('time', wt.DWORD), ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', wt.WORD), ('wScan', wt.WORD),
        ('dwFlags', wt.DWORD), ('time', wt.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', wt.DWORD), ('wParamL', wt.WORD), ('wParamH', wt.WORD),
    ]


class INPUT_U(ctypes.Union):
    _fields_ = [('mi', MOUSEINPUT), ('ki', KEYBDINPUT), ('hi', HARDWAREINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [('type', wt.DWORD), ('u', INPUT_U)]


# Magic marker so our hook ignores our own injected events
_extra_val = ctypes.c_ulong(0x494E4454)
_extra_ptr = ctypes.pointer(_extra_val)


def _make_unicode_input(ch, keyup=False):
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.u.ki.wScan = ord(ch)
    inp.u.ki.dwFlags = KEYEVENTF_UNICODE | (KEYEVENTF_KEYUP if keyup else 0)
    inp.u.ki.dwExtraInfo = _extra_ptr
    return inp


def _make_vk_input(vk, keyup=False):
    inp = INPUT()
    inp.type = INPUT_KEYBOARD
    inp.u.ki.wVk = vk
    inp.u.ki.dwFlags = KEYEVENTF_KEYUP if keyup else 0
    inp.u.ki.dwExtraInfo = _extra_ptr
    return inp


# ============================================================
# Target Window Helper
# ============================================================
def get_target():
    """Get the focused control in the foreground window."""
    fg = user32.GetForegroundWindow()
    if not fg:
        return None
    tid = user32.GetWindowThreadProcessId(fg, None)
    our = kernel32.GetCurrentThreadId()
    hwnd = None
    if tid != our:
        user32.AttachThreadInput(our, tid, True)
        hwnd = user32.GetFocus()
        user32.AttachThreadInput(our, tid, False)
    else:
        hwnd = user32.GetFocus()
    return hwnd if hwnd else fg


# ============================================================
# GUITHREADINFO for caret position
# ============================================================
class GUITHREADINFO(ctypes.Structure):
    _fields_ = [
        ('cbSize', wt.DWORD), ('flags', wt.DWORD),
        ('hwndActive', wt.HWND), ('hwndFocus', wt.HWND),
        ('hwndCapture', wt.HWND), ('hwndMenuOwner', wt.HWND),
        ('hwndMoveSize', wt.HWND), ('hwndCaret', wt.HWND),
        ('rcCaret', wt.RECT),
    ]


# ============================================================
# WindowsIME
# ============================================================
class WindowsIME(VarnaaksharaIMEBase):
    """Windows implementation of the Varnaakshara IME.

    Uses WH_KEYBOARD_LL low-level keyboard hook and SendInput
    for Unicode text injection. Exact same technique as Baraha's
    brh_direct.dll.
    """

    def __init__(self, language='kannada', scheme='baraha', custom_mappings=None):
        super().__init__(language=language, scheme=scheme,
                         custom_mappings=custom_mappings)
        self._hook = None
        self._proc = None  # prevent GC of HOOKPROC callback

    # ============================================================
    # Abstract method implementations
    # ============================================================

    def _send_text(self, text):
        """Send a Unicode string via SendInput(KEYEVENTF_UNICODE)."""
        events = []
        for ch in text:
            events.append(_make_unicode_input(ch, keyup=False))
            events.append(_make_unicode_input(ch, keyup=True))
        n = len(events)
        if n > 0:
            arr = (INPUT * n)(*events)
            user32.SendInput(n, arr, ctypes.sizeof(INPUT))

    def _send_backspaces(self, count):
        """Send backspace(s) via SendInput."""
        events = []
        for _ in range(count):
            events.append(_make_vk_input(VK_BACK, keyup=False))
            events.append(_make_vk_input(VK_BACK, keyup=True))
        n = len(events)
        if n > 0:
            arr = (INPUT * n)(*events)
            user32.SendInput(n, arr, ctypes.sizeof(INPUT))

    def _apply_screen_edit(self, erase_count, to_type):
        """Atomic batch: backspaces + new text in ONE SendInput call."""
        events = []
        for _ in range(erase_count):
            events.append(_make_vk_input(VK_BACK, keyup=False))
            events.append(_make_vk_input(VK_BACK, keyup=True))
        for ch in to_type:
            events.append(_make_unicode_input(ch, keyup=False))
            events.append(_make_unicode_input(ch, keyup=True))
        if events:
            n = len(events)
            arr = (INPUT * n)(*events)
            ret = user32.SendInput(n, arr, ctypes.sizeof(INPUT))
            _dbg(f'  SendInput({n} events) = {ret}')

    def _get_caret_screen_pos(self):
        """Get caret position using GetGUIThreadInfo → GetCaretPos → cursor fallback."""
        try:
            gti = GUITHREADINFO()
            gti.cbSize = ctypes.sizeof(GUITHREADINFO)
            if ctypes.windll.user32.GetGUIThreadInfo(0, ctypes.byref(gti)):
                if gti.hwndCaret:
                    pt = wt.POINT(gti.rcCaret.left, gti.rcCaret.bottom)
                    ctypes.windll.user32.ClientToScreen(gti.hwndCaret, ctypes.byref(pt))
                    if pt.x != 0 or pt.y != 0:
                        return (pt.x, pt.y)
        except Exception:
            pass
        try:
            pt = wt.POINT()
            if ctypes.windll.user32.GetCaretPos(ctypes.byref(pt)):
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                ctypes.windll.user32.ClientToScreen(hwnd, ctypes.byref(pt))
                if pt.x != 0 or pt.y != 0:
                    return (pt.x, pt.y)
        except Exception:
            pass
        try:
            pt = wt.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            return (pt.x, pt.y)
        except Exception:
            pass
        return (None, None)

    def _get_dpi_scale(self, x, y):
        """Get DPI scale factor for the monitor containing point (x, y)."""
        try:
            monitor = ctypes.windll.user32.MonitorFromPoint(
                wt.POINT(x, y), 2  # MONITOR_DEFAULTTONEAREST
            )
            dpi_x = ctypes.c_uint()
            ctypes.windll.shcore.GetDpiForMonitor(
                monitor, 0, ctypes.byref(dpi_x), ctypes.byref(ctypes.c_uint())
            )
            return dpi_x.value / 96.0
        except Exception:
            return 1.0

    # ============================================================
    # Keyboard hook
    # ============================================================

    def _hook_callback(self, nCode, wParam, lParam):
        """Low-level keyboard hook callback."""
        if nCode < 0:
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        kb = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk = kb.vkCode

        # ---- Track modifier state ----
        if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
            if vk in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
                self._ctrl = True
                return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)
            if vk in (VK_MENU, VK_LMENU, VK_RMENU):
                self._alt = True
                return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)
            if vk in (VK_SHIFT, VK_LSHIFT, VK_RSHIFT):
                self._shift = True
                return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)
            if vk == VK_CAPITAL:
                return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)
        elif wParam in (WM_KEYUP, WM_SYSKEYUP):
            if vk in (VK_CONTROL, VK_LCONTROL, VK_RCONTROL):
                self._ctrl = False
            elif vk in (VK_MENU, VK_LMENU, VK_RMENU):
                self._alt = False
            elif vk in (VK_SHIFT, VK_LSHIFT, VK_RSHIFT):
                self._shift = False
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # Only process WM_KEYDOWN
        if wParam not in (WM_KEYDOWN, WM_SYSKEYDOWN):
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Global shortcuts (always active) ----

        # F11 / F12 → toggle
        if vk in (VK_F11, VK_F12):
            self.handle_toggle()
            return 1

        # Ctrl+` → English mode
        if self._ctrl and vk == VK_OEM_3:
            self.handle_english_mode()
            return 1

        # Ctrl+Number → language switch
        if self._ctrl and not self._alt and vk in CTRL_LANG_MAP:
            self.handle_language_switch(CTRL_LANG_MAP[vk])
            return 1

        # Skip injected events (our own SendInput output)
        if kb.flags & LLKHF_INJECTED:
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Number keys 1-5 to accept suggestions ----
        if (self._current_suggestions and self._popup and
                self._popup.is_visible and not self._ctrl and not self._alt):
            if 0x31 <= vk <= 0x35:
                idx = vk - 0x31
                if idx < len(self._current_suggestions):
                    self.handle_suggestion_accept(idx)
                    return 1

        _dbg(f'HOOK vk=0x{vk:02X} flags=0x{kb.flags:X} '
             f'ctrl={self._ctrl} alt={self._alt} shift={self._shift} '
             f'active={self.active} buf="{self._buf}"')

        # ---- If IME is off, pass through ----
        if not self.active:
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Ctrl/Alt combos → commit and pass through ----
        if self._ctrl or self._alt:
            self.handle_ctrl_combo()
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Backspace ----
        if vk == VK_BACK:
            if self.handle_backspace():
                return 1  # suppress
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Space ----
        if vk == VK_SPACE:
            self.handle_space()
            return 1

        # ---- Enter ----
        if vk == VK_RETURN:
            self.handle_enter()
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Navigation keys ----
        if vk in NAV_KEYS:
            self.handle_nav()
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Convert virtual key to character ----
        kb_state = (ctypes.c_ubyte * 256)()
        user32.GetKeyboardState(kb_state)
        if self._shift:
            kb_state[VK_SHIFT] = 0x80
            kb_state[VK_LSHIFT] = 0x80
        else:
            kb_state[VK_SHIFT] = 0
            kb_state[VK_LSHIFT] = 0
        caps = user32.GetKeyState(VK_CAPITAL) & 0x0001
        kb_state[VK_CAPITAL] = 0x01 if caps else 0x00
        char_buf = (ctypes.c_wchar * 5)()
        ret = user32.ToUnicode(vk, kb.scanCode, kb_state, char_buf, 5, 0)

        if ret == 1:
            ch = char_buf[0]
            if ch.isalpha():
                want_upper = self._shift ^ bool(caps)
                ch = ch.upper() if want_upper else ch.lower()

            _dbg(f'KEY vk=0x{vk:02X} -> ch={ch!r} buf="{self._buf}" '
                 f'shift={self._shift}')

            if self.handle_char(ch):
                return 1  # suppress

        # Dead key / function key / unknown → commit and pass through
        self._commit()
        return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

    # ============================================================
    # Hook lifecycle
    # ============================================================

    def start(self):
        """Install the keyboard hook."""
        self._proc = HOOKPROC(self._hook_callback)
        hmod = kernel32.GetModuleHandleW(None)
        self._hook = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL, self._proc, hmod, 0
        )
        if not self._hook:
            raise RuntimeError(
                f"SetWindowsHookExW failed: {ctypes.get_last_error()}"
            )
        _dbg('Keyboard hook installed')

    # Alias for backward compatibility
    install_hook = start

    def run_event_loop(self):
        """Pump Windows messages (required for LL keyboard hook)."""
        msg = wt.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    # Alias for backward compatibility
    run_message_loop = run_event_loop

    def stop(self):
        """Unhook the keyboard hook."""
        if self._hook:
            user32.UnhookWindowsHookEx(self._hook)
            self._hook = None
            _dbg('Keyboard hook removed')


# ============================================================
# Single instance check (Windows)
# ============================================================
def check_single_instance():
    """Ensure only one instance of Varnaakshara runs at a time."""
    MUTEX_NAME = 'VarnaaksharaIME_SingleInstance_v2'
    _kernel32 = ctypes.windll.kernel32
    mutex = _kernel32.CreateMutexW(None, True, MUTEX_NAME)
    last_error = _kernel32.GetLastError()
    if last_error == 183:  # ERROR_ALREADY_EXISTS
        return False
    return True
