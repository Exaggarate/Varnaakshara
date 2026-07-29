"""
Varnaakshara IME — Real-time Indian Script Input
Proven method: WH_KEYBOARD_LL hook + PostMessageW(WM_CHAR) for output.
Exact same technique as Baraha's brh_direct.dll.

CRITICAL: All ctypes return types MUST be declared correctly.
Qt tray runs on MAIN thread (required by Qt/Windows).
Hook + message loop run on background thread.
"""

import sys
import os
import ctypes
import ctypes.wintypes as wt
import threading
import queue
import faulthandler

# Enable faulthandler to capture segfaults to a file
try:
    _fault_path = os.path.join(
        os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv else __file__)),
        'varnaakshara_crash.log'
    )
    _fault_file = open(_fault_path, 'w')
    faulthandler.enable(file=_fault_file, all_threads=True)
except Exception:
    pass  # Best-effort
import time

from transliteration import TransliterationEngine, LANGUAGES

# Auto-updater
try:
    from updater import check_for_update, download_and_install, check_post_update, CURRENT_VERSION
    HAS_UPDATER = True
except ImportError:
    HAS_UPDATER = False
    CURRENT_VERSION = '1.3.0'

# Suggestion engine (lazy import — only on Windows with DB available)
try:
    from suggestions import SuggestionEngine, LANG_CODES
    from suggestion_popup import SuggestionPopup
    HAS_SUGGESTIONS = True
except ImportError:
    HAS_SUGGESTIONS = False

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
VK_PRIOR = 0x21  # Page Up
VK_NEXT = 0x22   # Page Down
VK_F11 = 0x7A
VK_F12 = 0x7B
VK_OEM_3 = 0xC0  # `/~

NAV_KEYS = {VK_LEFT, VK_UP, VK_RIGHT, VK_DOWN, VK_HOME, VK_END,
            VK_DELETE, VK_ESCAPE, VK_TAB, VK_PRIOR, VK_NEXT}

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
# Win32 API — CORRECT TYPE DECLARATIONS
# ============================================================
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Hook functions
user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, wt.HINSTANCE, wt.DWORD]
user32.SetWindowsHookExW.restype = wt.HHOOK

user32.CallNextHookEx.argtypes = [wt.HHOOK, ctypes.c_int, wt.WPARAM, wt.LPARAM]
user32.CallNextHookEx.restype = ctypes.c_long

user32.UnhookWindowsHookEx.argtypes = [wt.HHOOK]
user32.UnhookWindowsHookEx.restype = wt.BOOL

# Window functions
user32.GetForegroundWindow.restype = wt.HWND
user32.GetFocus.restype = wt.HWND
user32.GetWindowThreadProcessId.restype = wt.DWORD
user32.GetWindowThreadProcessId.argtypes = [wt.HWND, ctypes.POINTER(wt.DWORD)]
user32.AttachThreadInput.argtypes = [wt.DWORD, wt.DWORD, wt.BOOL]
user32.AttachThreadInput.restype = wt.BOOL

# Message functions (Baraha method)
user32.PostMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.PostMessageW.restype = wt.BOOL
user32.SendMessageW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]
user32.SendMessageW.restype = wt.LPARAM

# Keyboard state
user32.GetKeyboardState.argtypes = [ctypes.POINTER(ctypes.c_ubyte * 256)]
user32.GetKeyboardState.restype = wt.BOOL
user32.ToUnicode.argtypes = [wt.UINT, wt.UINT, ctypes.POINTER(ctypes.c_ubyte * 256),
                             ctypes.c_wchar_p, ctypes.c_int, wt.UINT]
user32.ToUnicode.restype = ctypes.c_int

# Module handle
kernel32.GetModuleHandleW.restype = wt.HMODULE
kernel32.GetCurrentThreadId.restype = wt.DWORD


# ============================================================
# Target Window Helper (Baraha uses AttachThreadInput + GetFocus)
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
# Debug logging
# ============================================================
import datetime
_DBG_PATH = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv[0] else __file__)), 'varnaakshara_debug.log')
_DBG_FILE = None

def _dbg(msg):
    global _DBG_FILE
    try:
        if _DBG_FILE is None:
            _DBG_FILE = open(_DBG_PATH, 'w', encoding='utf-8')
        ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        _DBG_FILE.write(f'[{ts}] {msg}\n')
        _DBG_FILE.flush()
    except:
        pass

# ============================================================
# Input simulation via SendInput (KEYEVENTF_UNICODE)
# Works in ALL apps: Notepad, Word, Chrome, VS Code, etc.
# ============================================================
INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', ctypes.c_long),
        ('dy', ctypes.c_long),
        ('mouseData', wt.DWORD),
        ('dwFlags', wt.DWORD),
        ('time', wt.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', wt.WORD),
        ('wScan', wt.WORD),
        ('dwFlags', wt.DWORD),
        ('time', wt.DWORD),
        ('dwExtraInfo', ctypes.POINTER(ctypes.c_ulong)),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', wt.DWORD),
        ('wParamL', wt.WORD),
        ('wParamH', wt.WORD),
    ]


class INPUT_U(ctypes.Union):
    # MUST include MOUSEINPUT so the union is the correct size (32 bytes on x64)
    # Without it, sizeof(INPUT) = 32 instead of 40, and SendInput silently fails
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


def send_string(text):
    """Send a Unicode string via SendInput(KEYEVENTF_UNICODE).
    All characters are batched into a single SendInput call
    so they arrive atomically. Works in every app.
    Returns: number of key-down events sent (= len(text))."""
    events = []
    for ch in text:
        events.append(_make_unicode_input(ch, keyup=False))
        events.append(_make_unicode_input(ch, keyup=True))
    n = len(events)
    arr = (INPUT * n)(*events)
    user32.SendInput(n, arr, ctypes.sizeof(INPUT))
    return len(text)


def send_backspaces(count):
    """Send backspace(s) via SendInput."""
    events = []
    for _ in range(count):
        events.append(_make_vk_input(VK_BACK, keyup=False))
        events.append(_make_vk_input(VK_BACK, keyup=True))
    n = len(events)
    arr = (INPUT * n)(*events)
    user32.SendInput(n, arr, ctypes.sizeof(INPUT))


def _select_back(count):
    """Select backwards by sending Shift+Left `count` times.
    This selects exactly what we previously typed, regardless
    of whether the app counts by codepoints or grapheme clusters."""
    events = []
    # Press Shift down
    events.append(_make_vk_input(VK_SHIFT, keyup=False))
    # Press Left `count` times
    for _ in range(count):
        events.append(_make_vk_input(VK_LEFT, keyup=False))
        events.append(_make_vk_input(VK_LEFT, keyup=True))
    # Release Shift
    events.append(_make_vk_input(VK_SHIFT, keyup=True))
    n = len(events)
    arr = (INPUT * n)(*events)
    user32.SendInput(n, arr, ctypes.sizeof(INPUT))


def _send_key(vk):
    """Send a single key press+release via SendInput."""
    events = [_make_vk_input(vk, False), _make_vk_input(vk, True)]
    arr = (INPUT * 2)(*events)
    user32.SendInput(2, arr, ctypes.sizeof(INPUT))


# ============================================================
# IME Engine
# ============================================================
class IMEEngine:
    def __init__(self):
        self.scheme = 'baraha'  # default, overridden by config
        self.engine = TransliterationEngine('kannada', scheme=self.scheme)
        self.lang = 'kannada'
        self.active = False   # Start in English; user toggles when ready

        self._buf = ''       # Roman input buffer
        self._screen = ''    # Indian text currently on screen
        self._sent_events = 0  # number of SendInput key-down events for current screen text
        self._hook = None
        self._proc = None    # prevent GC of callback

        # Modifier state
        self._ctrl = False
        self._alt = False
        self._shift = False

        # Callbacks for UI
        self._on_state_change = None

        # Suggestion engine
        self._suggestions = None  # SuggestionEngine instance
        self._popup = None        # SuggestionPopup instance
        self._current_suggestions = []  # list of (word, source)
        self._suggestion_queue = queue.Queue()  # async suggestion queries
        self._suggestions_enabled = False  # off by default, toggled via settings
        # Don't init suggestions here — wait for config to enable them
        _dbg('Suggestions disabled by default (enable in Settings)')

    def set_state_callback(self, cb):
        self._on_state_change = cb

    def _notify(self):
        if self._on_state_change:
            self._on_state_change(self.lang, self.active)

    def set_scheme(self, scheme):
        """Switch input scheme (baraha/itrans). Commits current buffer first."""
        self._commit()
        self.scheme = scheme
        self.engine.set_scheme(scheme)
        _dbg(f'Scheme changed to: {scheme}')

    def set_language(self, key):
        self._commit()
        self.lang = key
        self.engine.set_language(key)
        self.active = True
        self._notify()

    def toggle(self):
        self._commit()
        self.active = not self.active
        self._notify()

    def _commit(self):
        """Finalize current word — text stays on screen, reset buffers."""
        if self._buf:
            _dbg(f'COMMIT buf="{self._buf}" screen="{self._screen}"')
            # Learn the completed word (background thread — never block hook)
            if self._suggestions and self._screen:
                lang_code = LANG_CODES.get(self.lang, '')
                if lang_code:
                    self._safe_learn(self._screen, lang_code)
        self._buf = ''
        self._screen = ''
        self._sent_events = 0
        self._current_suggestions = []
        # Hide suggestion popup
        if self._popup:
            try:
                self._popup.hide()
            except Exception:
                pass

    @staticmethod
    def _grapheme_len(text):
        """Count grapheme clusters in Indic text.
        
        A grapheme cluster = base char + all following combining marks (Mc/Mn)
        + any conjunct extensions (virama + consonant chains).
        This matches what a single Backspace key deletes in Word/Notepad.
        """
        import unicodedata
        # Set of viramas for all supported Indic scripts
        VIRAMAS = {
            '\u094D',  # Devanagari
            '\u09CD',  # Bengali
            '\u0A4D',  # Gurmukhi
            '\u0ACD',  # Gujarati
            '\u0B4D',  # Odia
            '\u0BCD',  # Tamil
            '\u0C4D',  # Telugu
            '\u0CCD',  # Kannada
            '\u0D4D',  # Malayalam
        }
        count = 0
        i = 0
        while i < len(text):
            cat = unicodedata.category(text[i])
            if cat in ('Mc', 'Mn'):
                # Stray combining mark — count as cluster
                count += 1
                i += 1
                continue
            # Base character — start of a grapheme cluster
            count += 1
            i += 1
            # Consume combining marks and conjunct chains
            while i < len(text):
                c = unicodedata.category(text[i])
                if c in ('Mc', 'Mn'):
                    is_virama = text[i] in VIRAMAS
                    i += 1
                    # Virama + following consonant = conjunct (same cluster)
                    if is_virama and i < len(text) and unicodedata.category(text[i]) == 'Lo':
                        i += 1  # consume consonant into this cluster
                else:
                    break
        return count

    def _update(self, hwnd=None):
        """Transliterate buffer and update screen.
        
        Smart diff: find the common prefix between old and new screen text,
        erase only the changed suffix, and type only the new suffix.
        This keeps SendInput event counts small even for long words.
        
        When the new suffix starts with a combining char (Mc/Mn), back up
        one position so the base char + combining mark are sent together.
        
        All operations in ONE atomic SendInput call.
        """
        import unicodedata
        if not self._buf:
            return

        new_text = self.engine.transliterate(self._buf)
        if new_text == self._screen:
            return

        # Find longest common prefix
        common = 0
        for i in range(min(len(self._screen), len(new_text))):
            if self._screen[i] == new_text[i]:
                common += 1
            else:
                break

        # If new suffix starts with combining char, back up to include base
        to_type = new_text[common:]
        if to_type and common > 0:
            cat = unicodedata.category(to_type[0])
            if cat in ('Mc', 'Mn'):
                common -= 1
                to_type = new_text[common:]

        erase_count = len(self._screen) - common

        # DEBUG LOG
        _dbg(f'UPDATE buf="{self._buf}" common={common} erase={erase_count} type={len(to_type)} new_len={len(new_text)}')

        # Build ONE atomic SendInput batch
        events = []
        
        # Backspaces to erase changed suffix
        for _ in range(erase_count):
            events.append(_make_vk_input(VK_BACK, keyup=False))
            events.append(_make_vk_input(VK_BACK, keyup=True))
        
        # New suffix characters
        for ch in to_type:
            events.append(_make_unicode_input(ch, keyup=False))
            events.append(_make_unicode_input(ch, keyup=True))
        
        # Send everything as ONE call — atomic, no interleaving
        if events:
            n = len(events)
            arr = (INPUT * n)(*events)
            ret = user32.SendInput(n, arr, ctypes.sizeof(INPUT))
            _dbg(f'  SendInput({n} events) = {ret}')

        self._screen = new_text

        # Query suggestions
        self._query_suggestions()

    def _get_caret_screen_pos(self):
        """Get caret position in screen coordinates.
        
        Strategy: GetGUIThreadInfo (most reliable) → GetCaretPos → mouse cursor fallback.
        Returns (x, y) or (None, None) if all fail.
        """
        import ctypes
        import ctypes.wintypes as wt

        class GUITHREADINFO(ctypes.Structure):
            _fields_ = [
                ('cbSize', wt.DWORD),
                ('flags', wt.DWORD),
                ('hwndActive', wt.HWND),
                ('hwndFocus', wt.HWND),
                ('hwndCapture', wt.HWND),
                ('hwndMenuOwner', wt.HWND),
                ('hwndMoveSize', wt.HWND),
                ('hwndCaret', wt.HWND),
                ('rcCaret', wt.RECT),
            ]

        try:
            # Method 1: GetGUIThreadInfo — works in most apps including Chrome/Edge
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
            # Method 2: GetCaretPos — works in classic Win32 apps
            pt = wt.POINT()
            if ctypes.windll.user32.GetCaretPos(ctypes.byref(pt)):
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                ctypes.windll.user32.ClientToScreen(hwnd, ctypes.byref(pt))
                if pt.x != 0 or pt.y != 0:
                    return (pt.x, pt.y)
        except Exception:
            pass

        try:
            # Method 3: Fall back to mouse cursor position
            pt = wt.POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            return (pt.x, pt.y)
        except Exception:
            pass

        return (None, None)

    def _get_dpi_scale(self, x, y):
        """Get DPI scale factor for the monitor containing point (x, y)."""
        try:
            import ctypes
            import ctypes.wintypes
            monitor = ctypes.windll.user32.MonitorFromPoint(
                ctypes.wintypes.POINT(x, y), 2  # MONITOR_DEFAULTTONEAREST
            )
            dpi_x = ctypes.c_uint()
            ctypes.windll.shcore.GetDpiForMonitor(
                monitor, 0, ctypes.byref(dpi_x), ctypes.byref(ctypes.c_uint())
            )
            return dpi_x.value / 96.0  # 96 DPI = 100% scaling
        except Exception:
            return 1.0

    def enable_suggestions(self, enabled=True):
        """Enable or disable the suggestion engine at runtime."""
        if enabled and not self._suggestions and HAS_SUGGESTIONS:
            try:
                self._suggestions = SuggestionEngine(min_prefix=3)
                self._popup = SuggestionPopup()
                # Init widget on Qt thread if QApplication exists
                try:
                    from PyQt5.QtWidgets import QApplication
                    if QApplication.instance():
                        self._popup.init_widget()
                        _dbg('Popup widget initialized on enable')
                except Exception:
                    pass
                self._suggestion_worker = threading.Thread(
                    target=self._suggestion_worker_loop, daemon=True
                )
                self._suggestion_worker.start()
                self._suggestions_enabled = True
                _dbg('Suggestion engine enabled (async worker)')
            except Exception as e:
                _dbg(f'Suggestion engine enable failed: {e}')
                self._suggestions = None
                self._popup = None
                self._suggestions_enabled = False
        elif enabled and self._suggestions:
            self._suggestions_enabled = True
            _dbg('Suggestions re-enabled')
        elif not enabled:
            self._suggestions_enabled = False
            if self._popup:
                self._popup.hide()
            self._current_suggestions = []
            _dbg('Suggestions disabled')

    def _safe_learn(self, word, lang_code):
        """Learn a word in a background thread so it never blocks the hook."""
        def _do():
            try:
                self._suggestions.learn_word(word, lang_code)
            except Exception:
                pass
        threading.Thread(target=_do, daemon=True).start()

    def _suggestion_worker_loop(self):
        """Background thread that processes suggestion queries.
        
        Drains the queue to the latest request so we skip stale queries
        when the user types faster than SQLite can respond.
        """
        _dbg('Suggestion worker thread started')
        while True:
            try:
                # Block until at least one request arrives
                item = self._suggestion_queue.get()
                if item is None:
                    return  # shutdown sentinel
                # Drain to latest — skip stale intermediate queries
                while True:
                    try:
                        newer = self._suggestion_queue.get_nowait()
                        if newer is None:
                            return
                        item = newer
                    except queue.Empty:
                        break
                screen_text, lang_code = item
                results = self._suggestions.suggest(screen_text, lang_code, limit=5)
                results = [(w, s) for w, s in results if w != screen_text]
                self._current_suggestions = results
                if results:
                    x, y = self._get_caret_screen_pos()
                    if x is not None:
                        scale = self._get_dpi_scale(x, y)
                        self._popup.show(results, x, y, dpi_scale=scale)
                    else:
                        self._popup.show(results)
                else:
                    self._popup.hide()
            except Exception as e:
                _dbg(f'Suggestion worker error: {e}')
                self._current_suggestions = []

    def _query_suggestions(self):
        """Post a suggestion query to the worker thread (non-blocking)."""
        if not self._suggestions_enabled or not self._suggestions or not self._popup:
            return
        if not self._screen or len(self._screen) < 3:
            self._current_suggestions = []
            self._popup.hide()
            return
        lang_code = LANG_CODES.get(self.lang, '')
        if not lang_code:
            return
        # Non-blocking post — worker thread handles the actual SQLite query
        try:
            self._suggestion_queue.put_nowait((self._screen, lang_code))
        except Exception:
            pass

    def _accept_suggestion(self, index):
        """Accept suggestion at index. Replace current screen text with the word."""
        if not self._popup or index >= len(self._current_suggestions):
            return False
        word, source = self._current_suggestions[index]
        _dbg(f'ACCEPT suggestion [{index}]: "{word}"')

        # Erase current screen text
        if self._screen:
            send_backspaces(len(self._screen))

        # Type the suggestion
        send_string(word)

        # Learn the word (background thread — never block hook)
        lang_code = LANG_CODES.get(self.lang, '')
        if lang_code and self._suggestions:
            self._safe_learn(word, lang_code)

        # Reset state (word is committed)
        self._buf = ''
        self._screen = ''
        self._sent_events = 0
        self._current_suggestions = []
        self._popup.hide()

        # Send a space after the accepted word (natural typing flow)
        send_string(' ')
        return True

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
            self.toggle()
            return 1

        # Ctrl+` → switch to English
        if self._ctrl and vk == VK_OEM_3:
            self._commit()
            self.active = False
            self._notify()
            return 1

        # Ctrl+Number → language switch
        if self._ctrl and not self._alt:
            lang_map = {
                0x31: 'assamese',  0x32: 'bengali',   0x33: 'gujarati',
                0x34: 'hindi',     0x35: 'kannada',   0x36: 'malayalam',
                0x37: 'marathi',   0x38: 'odia',      0x39: 'punjabi',
                0x30: 'sanskrit',  0xBD: 'tamil',     0xBB: 'telugu',
            }
            if vk in lang_map:
                self.set_language(lang_map[vk])
                return 1

        # Skip injected events (our own SendInput output).
        # Windows sets LLKHF_INJECTED (bit 4) in flags for all SendInput events.
        LLKHF_INJECTED = 0x00000010
        if kb.flags & LLKHF_INJECTED:
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Number keys 1-5 to accept suggestions ----
        if (self._current_suggestions and self._popup and
                self._popup.is_visible and not self._ctrl and not self._alt):
            if 0x31 <= vk <= 0x35:  # VK_1 through VK_5
                idx = vk - 0x31
                if idx < len(self._current_suggestions):
                    self._accept_suggestion(idx)
                    return 1

        _dbg(f'HOOK vk=0x{vk:02X} flags=0x{kb.flags:X} wParam=0x{wParam:X} ctrl={self._ctrl} alt={self._alt} shift={self._shift} active={self.active} buf="{self._buf}"')

        # ---- If IME is off, pass everything through ----
        if not self.active:
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Ctrl/Alt combos → commit and pass through ----
        if self._ctrl or self._alt:
            self._commit()
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Backspace ----
        if vk == VK_BACK:
            if self._buf:
                # Remove last char from buffer and let _update diff
                self._buf = self._buf[:-1]
                if self._buf:
                    # _update() diffs old _screen vs new transliteration
                    # and sends minimal backspace+type operations
                    self._update(None)
                else:
                    # Buffer empty → erase everything on screen
                    if self._screen:
                        send_backspaces(len(self._screen))
                    self._screen = ''
                    self._query_suggestions()  # hides popup
                return 1  # suppress original backspace
            # Empty buffer → pass through (normal backspace)
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Space → commit + send space ----
        if vk == VK_SPACE:
            self._commit()
            send_string(' ')
            return 1

        # ---- Enter → commit + pass through ----
        if vk == VK_RETURN:
            self._commit()
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Navigation keys → commit + pass through ----
        if vk in NAV_KEYS:
            self._commit()
            return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

        # ---- Convert virtual key to character ----
        kb_state = (ctypes.c_ubyte * 256)()
        user32.GetKeyboardState(kb_state)
        # GetKeyboardState often misses physical Shift/Ctrl in LL hooks.
        # Force our tracked modifier state into the array so ToUnicode
        # produces the correct shifted character (? instead of /, | instead of \, etc.).
        if self._shift:
            kb_state[VK_SHIFT] = 0x80
            kb_state[VK_LSHIFT] = 0x80
        else:
            kb_state[VK_SHIFT] = 0
            kb_state[VK_LSHIFT] = 0
        # Preserve CapsLock toggle state
        caps = user32.GetKeyState(VK_CAPITAL) & 0x0001
        kb_state[VK_CAPITAL] = 0x01 if caps else 0x00
        char_buf = (ctypes.c_wchar * 5)()
        ret = user32.ToUnicode(vk, kb.scanCode, kb_state, char_buf, 5, 0)

        if ret == 1:
            ch = char_buf[0]
            
            # For alpha keys, apply our shift+caps logic explicitly
            if ch.isalpha():
                want_upper = self._shift ^ bool(caps)  # XOR: shift flips caps
                ch = ch.upper() if want_upper else ch.lower()
            
            _dbg(f'KEY vk=0x{vk:02X} -> ch={ch!r} buf_before="{self._buf}" shift={self._shift}')

            # Alphabetic or tilde → add to buffer and transliterate
            if ch.isalpha() or ch == '~':
                self._buf += ch
                self._update()
                return 1  # SUPPRESS original key

            # Baraha symbol chars (& | # $) → route through transliteration
            # & → avagraha (ऽ), | → danda (।), || → double danda (॥)
            # # → udatta, $ → anudatta (Vedic accents)
            if ch in ('&', '|', '#', '$'):
                self._buf += ch
                self._update()
                return 1  # SUPPRESS original key

            # Digit → convert to native script numeral
            if ch.isdigit():
                if self._buf:
                    self._commit()
                native = self.engine.transliterate(ch)
                send_string(native)
                return 1

            # OM. trigger → convert OM to ॐ symbol
            if ch == '.' and self._buf.endswith('OM'):
                # Erase current screen text
                if self._screen:
                    send_backspaces(len(self._screen))
                # Remove OM from buffer, commit anything before it
                pre = self._buf[:-2]
                if pre:
                    pre_text = self.engine.transliterate(pre)
                    send_string(pre_text)
                # Send ॐ mapped to target script (it's universal, stays ॐ)
                send_string('\u0950')
                self._buf = ''
                self._screen = ''
                return 1  # consume the period

            # Punctuation/other → commit current buffer, send the char
            self._commit()
            send_string(ch)
            return 1

        # Dead key / function key / unknown → commit and pass through
        self._commit()
        return user32.CallNextHookEx(self._hook, nCode, wParam, lParam)

    def install_hook(self):
        """Install the keyboard hook. MUST be called from main thread."""
        self._proc = HOOKPROC(self._hook_callback)
        hmod = kernel32.GetModuleHandleW(None)
        self._hook = user32.SetWindowsHookExW(
            WH_KEYBOARD_LL, self._proc, hmod, 0
        )
        if not self._hook:
            raise RuntimeError(f"SetWindowsHookExW failed: {ctypes.get_last_error()}")

    def run_message_loop(self):
        """Pump messages. MUST be on same thread as hook."""
        msg = wt.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            user32.TranslateMessage(ctypes.byref(msg))
            user32.DispatchMessageW(ctypes.byref(msg))

    def stop(self):
        if self._hook:
            user32.UnhookWindowsHookEx(self._hook)
            self._hook = None


# ============================================================
# Qt Tray (runs on background thread)
# ============================================================
def run_tray(ime):
    _dbg('run_tray thread started')
    try:
        _run_tray_inner(ime)
    except Exception as e:
        _dbg(f'run_tray CRASHED: {e}')
        import traceback
        _dbg(traceback.format_exc())

def _run_tray_inner(ime):
    # Set Qt plugin debug + platform hint before importing Qt
    os.environ.setdefault('QT_DEBUG_PLUGINS', '0')
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.qpa.fonts=false'
    _dbg('_run_tray_inner: importing PyQt5')
    from PyQt5.QtWidgets import (
        QApplication, QSystemTrayIcon, QMenu, QAction,
        QActionGroup, QMessageBox, QWidget
    )
    _dbg('_run_tray_inner: PyQt5 widgets imported')
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
    _dbg('_run_tray_inner: all Qt imports done')

    # Determine the icon path — don't load yet (need QApplication first)
    _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
    if getattr(sys, '_MEIPASS', None):
        _icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    _dbg(f'_run_tray_inner: icon path={_icon_path}, exists={os.path.exists(_icon_path)}')

    def make_icon(code, active=True):
        # Use the Varnaakshara logo as tray icon
        if _app_icon and not _app_icon.isNull():
            if not active:
                # Greyed out version when inactive
                s = 64
                pm = _app_icon.pixmap(s, s)
                grey_pm = QPixmap(s, s)
                grey_pm.fill(Qt.transparent)
                p = QPainter(grey_pm)
                p.setOpacity(0.4)
                p.drawPixmap(0, 0, pm)
                p.end()
                return QIcon(grey_pm)
            return _app_icon
        # Fallback if icon file not found
        s = 64
        pm = QPixmap(s, s)
        bg = QColor('#1A0E28') if active else QColor('#616161')
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(bg)
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(2, 2, s - 4, s - 4, 10, 10)
        p.setPen(QColor('#C9973E'))
        p.setFont(QFont('Segoe UI', 20, QFont.Bold))
        p.drawText(pm.rect(), Qt.AlignCenter, code.upper())
        p.end()
        return QIcon(pm)

    _dbg('_run_tray_inner: creating QApplication')
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        _dbg(f'QApplication FAILED: {e}')
        raise
    _dbg('_run_tray_inner: QApplication created OK')
    app.setQuitOnLastWindowClosed(False)

    # Load icon AFTER QApplication exists (QIcon/QPixmap need it)
    _app_icon = QIcon(_icon_path) if os.path.exists(_icon_path) else None
    if _app_icon and not _app_icon.isNull():
        app.setWindowIcon(_app_icon)
    _dbg(f'_run_tray_inner: icon loaded, isNull={_app_icon.isNull() if _app_icon else "N/A"}')

    # Initialize suggestion popup on Qt thread
    if ime._popup:
        try:
            ime._popup.init_widget()
            _dbg('Suggestion popup widget initialized')
        except Exception as e:
            _dbg(f'Popup init failed: {e}')

    w = QWidget()
    tray = QSystemTrayIcon(w)

    _last_state = [None, None]  # [lang, active] — track to avoid duplicate toasts

    def refresh():
        code = LANGUAGES[ime.lang]['code'] if ime.active else 'EN'
        tray.setIcon(make_icon(code, ime.active))
        name = LANGUAGES[ime.lang]['name'] if ime.active else 'English'
        tray.setToolTip(f'Varnaakshara — {name}')
        if hasattr(w, '_atog'):
            w._atog.setText('✅  Indian Script   F11/F12' if ime.active
                            else '❌  English Mode   F11/F12')
        for a in lang_group.actions():
            if LANGUAGES.get(ime.lang, {}).get('name', '') in a.text():
                a.setChecked(True)
        # Track state (no toast — user requested removal)
        _last_state[:] = [ime.lang, ime.active]

    # State callback from hook thread — use signal to safely dispatch to Qt thread
    # QTimer.start() is NOT thread-safe; using QMetaObject.invokeMethod instead
    from PyQt5.QtCore import QMetaObject, Q_ARG
    _refresh_timer = QTimer(w)
    _refresh_timer.setSingleShot(True)
    _refresh_timer.setInterval(50)
    _refresh_timer.timeout.connect(refresh)

    def _schedule_refresh(lang, active):
        # Thread-safe: invokeMethod queues the call on the Qt event loop
        QMetaObject.invokeMethod(_refresh_timer, 'start', Qt.QueuedConnection)

    ime.set_state_callback(_schedule_refresh)

    # Initial icon — respect ime.active (starts False = English)
    tray.setIcon(make_icon(LANGUAGES[ime.lang]['code'] if ime.active else 'EN', ime.active))
    tray.setToolTip(f'Varnaakshara — {LANGUAGES[ime.lang]["name"] if ime.active else "English"}')

    # ── Styled tray menu (purple/gold theme) ──
    _menu_style = """
        QMenu {
            background-color: #1A0E28;
            border: 1px solid #3A2A4A;
            border-radius: 8px;
            padding: 8px 0px;
            font-family: 'Segoe UI';
            font-size: 13px;
        }
        QMenu::item {
            color: #D4C5A0;
            padding: 10px 28px 10px 20px;
            margin: 1px 6px;
            border-radius: 6px;
        }
        QMenu::item:selected {
            background-color: #2D1845;
            color: #E8C862;
        }
        QMenu::item:checked {
            color: #E8C862;
        }
        QMenu::item:disabled {
            color: #C9973E;
            padding: 6px 20px 4px 20px;
            font-size: 10px;
            font-weight: bold;
        }
        QMenu::separator {
            height: 1px;
            background: #2D1845;
            margin: 6px 16px;
        }
        QMenu::indicator {
            width: 16px;
            height: 16px;
            margin-left: 8px;
        }
        QMenu::indicator:checked {
            background: #C9973E;
            border: 2px solid #E8C862;
            border-radius: 8px;
        }
        QMenu::indicator:unchecked {
            background: transparent;
            border: 2px solid #3A2A4A;
            border-radius: 8px;
        }
    """

    menu = QMenu()
    menu.setStyleSheet(_menu_style)

    # Toggle at the top
    w._atog = QAction('❌  English Mode   F11/F12', w)
    w._atog.triggered.connect(lambda: ime.toggle())
    menu.addAction(w._atog)
    menu.addSeparator()

    lm = menu.addMenu('🌐  Languages')
    lm.setStyleSheet(_menu_style)
    lang_group = QActionGroup(w)
    lang_group.setExclusive(True)

    # Language entries with script characters
    lang_display = {
        'kannada':   ('ಕನ್ನಡ', '5'),
        'hindi':     ('हिन्दी', '4'),
        'telugu':    ('తెలుగు', '='),
        'tamil':     ('தமிழ்', '-'),
        'malayalam': ('മലയാളം', '6'),
        'marathi':   ('मराठी', '7'),
        'sanskrit':  ('संस्कृत', '0'),
        'bengali':   ('বাংলা', '2'),
        'assamese':  ('অसमीया', '1'),
        'gujarati':  ('ગુજરાતી', '3'),
        'punjabi':   ('ਪੰਜਾਬી', '9'),
        'odia':      ('ଓଡ଼ିଆ', '8'),
    }
    for k, v in LANGUAGES.items():
        script_name, shortcut = lang_display.get(k, ('', ''))
        display = f'{script_name}   {v["name"]}' if script_name else v['name']
        a = QAction(f'{display}', w)
        a.setCheckable(True)
        a.setChecked(k == 'kannada')
        a.triggered.connect(lambda _, k=k: ime.set_language(k))
        lang_group.addAction(a)
        lm.addAction(a)

    # Scheme submenu
    sm = menu.addMenu('Scheme')
    sm.setStyleSheet(_menu_style)
    scheme_group = QActionGroup(w)
    scheme_group.setExclusive(True)
    for scheme_key, scheme_label in [('baraha', 'Baraha (default)'), ('itrans', 'ITRANS (academic)')]:
        sa = QAction(scheme_label, w)
        sa.setCheckable(True)
        sa.setChecked(scheme_key == ime.scheme)
        sa.triggered.connect(lambda _, s=scheme_key: ime.set_scheme(s))
        scheme_group.addAction(sa)
        sm.addAction(sa)

    menu.addSeparator()

    settings_action = QAction('⚙️ Settings', w)
    def _open_settings():
        try:
            from settings_ui import SettingsPanel
            w._settings_panel = SettingsPanel()
            def _on_settings_changed(cfg):
                from settings_ui import load_custom_mappings
                cm = load_custom_mappings()
                ime.engine.set_custom_mappings(cm)
                ime.set_scheme(cfg.get('scheme', 'baraha'))
                ime.set_language(cfg.get('language', 'kannada'))
                ime.enable_suggestions(cfg.get('suggestions_enabled', False))
                refresh()
            w._settings_panel.settings_changed.connect(_on_settings_changed)
            w._settings_panel.show()
        except Exception as e:
            _dbg(f'Settings panel error: {e}')
    settings_action.triggered.connect(_open_settings)
    menu.addAction(settings_action)

    menu.addSeparator()

    about_action = QAction('ℹ️ About', w)
    def _show_about():
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPixmap, QFont as QF

        dlg = QDialog()
        dlg.setWindowTitle('About Varnaakshara')
        dlg.setFixedSize(640, 640)
        dlg.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1A0E28, stop:0.5 #201030, stop:1 #0D0D12);
            }
            QLabel { color: #D4C5A0; }
            QPushButton {
                background: #C9973E;
                color: #1A0E28;
                border: none;
                border-radius: 6px;
                padding: 10px 40px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover { background: #E8C862; }
        """)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(8)
        layout.setContentsMargins(30, 25, 30, 25)

        # Logo removed — ICO looks blurry at large sizes

        # Title in Sanskrit
        title = QLabel('वर्णाक्षरः')
        title.setFont(QF('Noto Sans Devanagari', 28, QF.Bold))
        title.setStyleSheet('color: #E8C862; margin-top: 5px;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        sub = QLabel(f'Varnaakshara IME v{CURRENT_VERSION}')
        sub.setFont(QF('Segoe UI', 12))
        sub.setStyleSheet('color: #8A7B9A;')
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # Divider
        div1 = QLabel()
        div1.setFixedHeight(1)
        div1.setStyleSheet('background: #C9973E; margin: 8px 40px; opacity: 0.3;')
        layout.addWidget(div1)

        # Description
        desc = QLabel('Type in English \u2192 Get output in Indian scripts')
        desc.setFont(QF('Segoe UI', 11))
        desc.setStyleSheet('color: #B8A88A;')
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        # Language grid — use just English names to avoid font-width issues
        langs_text = (
            '<table cellspacing="8" cellpadding="4" style="color:#A89878; font-size:13px;" align="center">'
            '<tr>'
            '<td>Kannada</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Hindi</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Telugu</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Tamil</td>'
            '</tr>'
            '<tr>'
            '<td>Bengali</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Gujarati</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Malayalam</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Odia</td>'
            '</tr>'
            '<tr>'
            '<td>Punjabi</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Sanskrit</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Assamese</td><td style="color:#3A2A4A;">&middot;</td>'
            '<td>Marathi</td>'
            '</tr>'
            '</table>'
        )
        langs = QLabel(langs_text)
        langs.setAlignment(Qt.AlignCenter)
        layout.addWidget(langs)

        # Divider
        div2 = QLabel()
        div2.setFixedHeight(1)
        div2.setStyleSheet('background: #C9973E; margin: 8px 40px; opacity: 0.3;')
        layout.addWidget(div2)

        # Shortcuts
        shortcuts_text = (
            '<table cellspacing="6" cellpadding="2" style="color:#8A7B9A; font-size:12px;" align="center">'
            '<tr><td style="color:#C9973E; font-weight:bold;">F11 / F12</td><td>&nbsp;&nbsp;Toggle Indian / English</td></tr>'
            '<tr><td style="color:#C9973E; font-weight:bold;">Ctrl+1-0</td><td>&nbsp;&nbsp;Select language</td></tr>'
            '<tr><td style="color:#C9973E; font-weight:bold;">Ctrl+`</td><td>&nbsp;&nbsp;English mode</td></tr>'
            '</table>'
        )
        sc = QLabel(shortcuts_text)
        sc.setAlignment(Qt.AlignCenter)
        layout.addWidget(sc)

        layout.addStretch()

        # Contact
        contact = QLabel('<a href="mailto:aksaram.folios@gmail.com" style="color:#C9973E; text-decoration:none; font-size:11px;">aksaram.folios@gmail.com</a>')
        contact.setOpenExternalLinks(True)
        contact.setAlignment(Qt.AlignCenter)
        contact.setFont(QF('Segoe UI', 9))
        layout.addWidget(contact)

        # Copyright
        copy_lbl = QLabel('\u00a9 2026 Varnaakshara Project. Free and not for sale.')
        copy_lbl.setFont(QF('Segoe UI', 9))
        copy_lbl.setStyleSheet('color: #5A4B6A;')
        copy_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(copy_lbl)

        # Close button
        layout.addSpacing(10)
        btn = QPushButton('Close')
        btn.setFixedWidth(140)
        btn.clicked.connect(dlg.close)
        from PyQt5.QtWidgets import QHBoxLayout
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        if _app_icon:
            dlg.setWindowIcon(_app_icon)
        dlg.exec_()

    about_action.triggered.connect(_show_about)

    # Update + About + Quit at the bottom, separated
    menu.addSeparator()

    # --- Auto-updater integration ---
    if HAS_UPDATER:
        from PyQt5.QtCore import QObject, pyqtSignal

        class _UpdateSignal(QObject):
            update_ready = pyqtSignal(bool, str, str, str, str)  # has_update, version, url, notes, error
            progress = pyqtSignal(int, str)

        _usig = _UpdateSignal()
        update_action = QAction(f'🔄  Check for Updates (v{CURRENT_VERSION})', w)
        _update_state = {'checking': False, 'url': None, 'version': None, 'notes': None}

        def _on_ui_update(has_update, version, url, notes, error):
            _update_state['checking'] = False
            if error:
                update_action.setText('❌  Update check failed')
                tray.showMessage('Update Check', f'Failed: {error}',
                                 QSystemTrayIcon.Warning, 3000)
            elif has_update:
                _update_state['url'] = url
                _update_state['version'] = version
                _update_state['notes'] = notes
                update_action.setText(f'⬆️  Update to v{version}')
                update_action.setEnabled(True)
                tray.showMessage('Update Available 🚀',
                                 f'Varnaakshara v{version} is available.\nRight-click tray → Update to install.',
                                 QSystemTrayIcon.Information, 5000)
            else:
                update_action.setText(f'✅  Up to date (v{CURRENT_VERSION})')
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(5000, lambda: update_action.setText(
                    f'🔄  Check for Updates (v{CURRENT_VERSION})'))

        def _on_ui_progress(pct, status):
            if pct >= 0:
                update_action.setText(f'⬇️  {status}')
            else:
                update_action.setText(f'❌  {status}')
                update_action.setEnabled(True)

        _usig.update_ready.connect(_on_ui_update)
        _usig.progress.connect(_on_ui_progress)

        def _on_update_check(has_update, version, url, notes, error):
            _usig.update_ready.emit(has_update, str(version or ''), str(url or ''), str(notes or ''), str(error or ''))

        def _on_update_progress(pct, status):
            _usig.progress.emit(pct, status)

        def _do_update():
            if _update_state['url']:
                update_action.setEnabled(False)
                update_action.setText('⬇️  Downloading update...')
                download_and_install(_update_state['url'], _on_update_progress,
                                     version=_update_state['version'],
                                     notes=_update_state['notes'])
            elif not _update_state['checking']:
                _update_state['checking'] = True
                update_action.setText('🔄  Checking...')
                update_action.setEnabled(False)
                check_for_update(_on_update_check)
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(20000, lambda: update_action.setEnabled(True))

        update_action.triggered.connect(_do_update)
        menu.addAction(update_action)

        # Auto-check on startup (after 10 second delay)
        from PyQt5.QtCore import QTimer
        def _startup_check():
            _update_state['checking'] = True
            check_for_update(_on_update_check)
        QTimer.singleShot(10000, _startup_check)

    menu.addAction(about_action)

    quit_action = QAction('❌  Quit', w)
    quit_action.triggered.connect(lambda: (ime.stop(), tray.hide(),
                                           app.quit(), os._exit(0)))
    menu.addAction(quit_action)

    # Force the context menu to pop upward near the system tray
    def _show_menu(reason):
        if reason in (QSystemTrayIcon.Context, QSystemTrayIcon.Trigger):
            pos = QCursor.pos()
            menu_h = menu.sizeHint().height()
            # Show menu above the cursor so it doesn't get clipped by taskbar
            menu.popup(QPoint(pos.x(), pos.y() - menu_h))
        elif reason == QSystemTrayIcon.DoubleClick:
            ime.toggle()

    from PyQt5.QtGui import QCursor
    from PyQt5.QtCore import QPoint
    tray.setContextMenu(None)  # Disable default context menu
    tray.activated.connect(_show_menu)
    tray.show()

    # Check if we just updated — show "What's New" instead of normal startup
    if HAS_UPDATER:
        updated_ver, updated_notes = check_post_update()
        if updated_ver:
            notes_preview = updated_notes[:150] if updated_notes else 'Bug fixes and improvements'
            tray.showMessage(
                f'✅ Updated to v{updated_ver}!',
                notes_preview,
                QSystemTrayIcon.Information, 8000)
        else:
            tray.showMessage('Varnaakshara ready ✨',
                             'F11/F12 to switch languages',
                             QSystemTrayIcon.Information, 3000)
    else:
        tray.showMessage('Varnaakshara ready ✨',
                         'F11/F12 to switch languages',
                         QSystemTrayIcon.Information, 3000)

    app.exec_()


# ============================================================
# Main
# ============================================================
def check_single_instance():
    """Ensure only one instance of Varnaakshara runs at a time."""
    import ctypes
    MUTEX_NAME = 'VarnaaksharaIME_SingleInstance_v2'
    kernel32 = ctypes.windll.kernel32
    mutex = kernel32.CreateMutexW(None, True, MUTEX_NAME)
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:  # ERROR_ALREADY_EXISTS
        return False
    return True


def main():
    # Enable per-monitor DPI awareness (Windows 10 1703+)
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows
        except Exception:
            pass

    # Single instance check — show message if already running
    if not check_single_instance():
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            'Varnaakshara is already running in the system tray!\n\n'
            'Right-click the tray icon for options.\n'
            'F11/F12 to toggle Indian script mode.',
            'Varnaakshara \u2014 Already Running',
            0x40 | 0x00040000  # MB_ICONINFORMATION | MB_TOPMOST
        )
        sys.exit(0)

    _dbg('main() started — past single instance check')

    # Install bundled fonts on first run (silent, per-user, no admin)
    try:
        from font_installer import install_fonts
        installed = install_fonts()
        if installed:
            _dbg(f'Installed {len(installed)} fonts')
        else:
            _dbg('Font install: nothing new to install')
    except Exception as e:
        _dbg(f'Font install skipped: {e}')

    _dbg('Creating IMEEngine')
    ime = IMEEngine()
    _dbg('IMEEngine created OK')

    # Apply saved settings (scheme, language, custom mappings)
    try:
        from settings_ui import load_config, load_custom_mappings
        cfg = load_config()
        saved_scheme = cfg.get('scheme', 'baraha')
        saved_lang = cfg.get('language', 'kannada')
        # Load custom mappings first — they get overlaid on scheme tables
        cm = load_custom_mappings()
        if cm:
            ime.engine.set_custom_mappings(cm)
            _dbg(f'Custom mappings loaded: {sum(len(v) for v in cm.values() if isinstance(v, dict))} entries')
        if saved_scheme != 'baraha':
            ime.set_scheme(saved_scheme)
        if saved_lang != 'kannada':
            ime.set_language(saved_lang)
        if cfg.get('start_active', False):
            ime.active = True
        if cfg.get('suggestions_enabled', False):
            ime.enable_suggestions(True)
        _dbg(f'Config applied: scheme={saved_scheme}, lang={saved_lang}, active={ime.active}')
    except Exception as e:
        _dbg(f'Config load skipped: {e}')

    # Start keyboard hook + message pump on a background thread
    # Qt MUST run on the main thread (Windows/PyInstaller requirement)
    def hook_thread_fn():
        _dbg('Hook thread: installing keyboard hook')
        try:
            ime.install_hook()
            _dbg('Hook thread: hook installed OK')
        except Exception as e:
            _dbg(f'Hook thread: hook install FAILED: {e}')
            return
        _dbg('Hook thread: entering message loop')
        ime.run_message_loop()
        _dbg('Hook thread: message loop exited')

    _dbg('Starting hook thread')
    hook_t = threading.Thread(target=hook_thread_fn, daemon=True)
    hook_t.start()

    # Give hook time to install
    time.sleep(0.5)

    # Run Qt tray on MAIN thread (required by Qt/Windows)
    _dbg('Starting Qt tray on main thread')
    run_tray(ime)  # blocks here (app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        _dbg(f'FATAL CRASH: {e}')
        import traceback
        _dbg(traceback.format_exc())
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, f'Varnaakshara crashed:\n{e}',
                'Varnaakshara Error', 0x10 | 0x00040000
            )
        except:
            pass
        sys.exit(1)
