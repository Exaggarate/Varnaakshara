"""
Varnaakshara IME v1.0.0 — macOS Edition
Real-time Indian Script Input using Quartz Event Taps.

Architecture mirrors varnaakshara_ime.py (Windows):
- IMEEngine class with same interface
- Keyboard hooking via CGEventTapCreate (kCGSessionEventTap)
- Input injection via CGEventPost + CGEventKeyboardSetUnicodeString
- Backspace simulation via CGEventCreateKeyboardEvent(keycode=51)
- Modifier tracking (Cmd/Ctrl/Shift/Alt/Option)
- System tray via PyQt5 QSystemTrayIcon
- Suggestion popup via suggestion_popup_qt.py (pure Qt)
- Hotkeys: F11/F12 toggle, Cmd+number for language switch

IMPORTANT: Requires macOS Accessibility permissions.
System Preferences → Privacy & Security → Accessibility
"""

import sys
import os
import threading
import time
import struct
import unicodedata
import datetime
import fcntl

from transliteration import TransliterationEngine, LANGUAGES

# Suggestion engine (lazy import)
try:
    from suggestions import SuggestionEngine, LANG_CODES
    from suggestion_popup_qt import SuggestionPopup
    HAS_SUGGESTIONS = True
except ImportError:
    HAS_SUGGESTIONS = False

# ============================================================
# macOS Quartz imports (via pyobjc)
# ============================================================
try:
    from Quartz import (
        CGEventTapCreate,
        CGEventTapEnable,
        CGEventGetIntegerValueField,
        CGEventSetIntegerValueField,
        CGEventPost,
        CGEventCreateKeyboardEvent,
        CGEventKeyboardSetUnicodeString,
        CGEventGetFlags,
        CGEventSetFlags,
        kCGSessionEventTap,
        kCGHeadInsertEventTap,
        kCGEventTapOptionDefault,
        kCGEventKeyDown,
        kCGEventKeyUp,
        kCGEventFlagsChanged,
        kCGEventTapDisabledByTimeout,
        kCGEventTapDisabledByUserInput,
        kCGKeyboardEventKeycode,
        kCGEventFlagMaskShift,
        kCGEventFlagMaskControl,
        kCGEventFlagMaskAlternate,
        kCGEventFlagMaskCommand,
        kCGEventFlagMaskNonCoalesced,
    )
    from Quartz import (
        CFMachPortCreateRunLoopSource,
        CFRunLoopGetCurrent,
        CFRunLoopAddSource,
        CFRunLoopRun,
        CFRunLoopStop,
        kCFRunLoopDefaultMode,
        kCFAllocatorDefault,
    )
    HAS_QUARTZ = True
except ImportError:
    HAS_QUARTZ = False

# ============================================================
# macOS keycode constants
# ============================================================
# Keycodes for common keys (macOS virtual keycodes)
KC_RETURN = 36
KC_TAB = 48
KC_SPACE = 49
KC_DELETE = 51   # Backspace
KC_ESCAPE = 53
KC_COMMAND = 55
KC_SHIFT = 56
KC_CAPSLOCK = 57
KC_OPTION = 58   # Alt/Option
KC_CONTROL = 59
KC_RIGHT_SHIFT = 60
KC_RIGHT_OPTION = 61
KC_RIGHT_CONTROL = 62
KC_RIGHT_COMMAND = 54  # Right Command (not standard on all keyboards)
KC_F11 = 103
KC_F12 = 111
KC_LEFT = 123
KC_RIGHT = 124
KC_DOWN = 125
KC_UP = 126
KC_HOME = 115
KC_END = 119
KC_PAGE_UP = 116
KC_PAGE_DOWN = 121
KC_FORWARD_DELETE = 117
KC_BACKTICK = 50  # `/~

# Navigation keys that commit the buffer
NAV_KEYCODES = {
    KC_LEFT, KC_RIGHT, KC_UP, KC_DOWN,
    KC_HOME, KC_END, KC_PAGE_UP, KC_PAGE_DOWN,
    KC_FORWARD_DELETE, KC_ESCAPE, KC_TAB,
}

# macOS keycode → character mapping (US keyboard layout)
# Only needed for keys where we can't use the event's Unicode chars
_KEYCODE_TO_CHAR = {
    0: 'a', 1: 's', 2: 'd', 3: 'f', 4: 'h', 5: 'g', 6: 'z', 7: 'x',
    8: 'c', 9: 'v', 11: 'b', 12: 'q', 13: 'w', 14: 'e', 15: 'r',
    16: 'y', 17: 't', 18: '1', 19: '2', 20: '3', 21: '4', 22: '6',
    23: '5', 24: '=', 25: '9', 26: '7', 27: '-', 28: '8', 29: '0',
    30: ']', 31: 'o', 32: 'u', 33: '[', 34: 'i', 35: 'p',
    37: 'l', 38: 'j', 39: "'", 40: 'k', 41: ';', 42: '\\',
    43: ',', 44: '/', 45: 'n', 46: 'm', 47: '.',
}

_KEYCODE_SHIFT_MAP = {
    18: '!', 19: '@', 20: '#', 21: '$', 22: '^', 23: '%',
    24: '+', 25: '(', 26: '&', 27: '_', 28: '*', 29: ')',
    30: '}', 33: '{', 39: '"', 41: ':', 42: '|',
    43: '<', 44: '?', 47: '>',
    KC_BACKTICK: '~',
}

# Cmd+number keycodes for language switching
_CMD_NUMBER_KEYCODES = {
    18: '1', 19: '2', 20: '3', 21: '4', 23: '5',
    22: '6', 26: '7', 28: '8', 25: '9', 29: '0',
    27: '-', 24: '=',
}


# ============================================================
# Debug logging
# ============================================================
_DBG_PATH = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv[0] else __file__)),
    'varnaakshara_debug_mac.log'
)
_DBG_FILE = None


def _dbg(msg):
    global _DBG_FILE
    try:
        if _DBG_FILE is None:
            _DBG_FILE = open(_DBG_PATH, 'w', encoding='utf-8')
        ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
        _DBG_FILE.write(f'[{ts}] {msg}\n')
        _DBG_FILE.flush()
    except Exception:
        pass


# ============================================================
# Accessibility permission check
# ============================================================
def check_accessibility():
    """Check if Accessibility permissions are granted.
    Returns True if granted, False otherwise.
    Shows a dialog with instructions if not granted.
    """
    try:
        import Cocoa
        import ApplicationServices
        # AXIsProcessTrustedWithOptions — prompts user if not trusted
        trusted = ApplicationServices.AXIsProcessTrustedWithOptions({
            'AXTrustedCheckOptionPrompt': True
        })
        return trusted
    except (ImportError, AttributeError):
        # Fallback: try to create a tap and see if it works
        try:
            mask = (1 << kCGEventKeyDown)
            tap = CGEventTapCreate(
                kCGSessionEventTap,
                kCGHeadInsertEventTap,
                kCGEventTapOptionDefault,
                mask,
                lambda *a: None,
                None
            )
            if tap is None:
                return False
            # Clean up — we were just testing
            return True
        except Exception:
            return False


def show_accessibility_dialog():
    """Show a PyQt5 dialog explaining how to enable Accessibility."""
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from PyQt5.QtCore import Qt

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setWindowTitle('Varnaakshara — Accessibility Permission Required')
    msg.setText(
        '<h3>Accessibility Permission Required</h3>'
        '<p>Varnaakshara needs Accessibility access to intercept keyboard events.</p>'
        '<p><b>To enable:</b></p>'
        '<ol>'
        '<li>Open <b>System Settings</b> (or System Preferences)</li>'
        '<li>Go to <b>Privacy &amp; Security → Accessibility</b></li>'
        '<li>Click the <b>+</b> button and add Varnaakshara</li>'
        '<li>Toggle the switch <b>ON</b></li>'
        '<li>Restart Varnaakshara</li>'
        '</ol>'
        '<p>Without this permission, Varnaakshara cannot function.</p>'
    )
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


# ============================================================
# Input injection (macOS)
# ============================================================

# Marker to identify our own injected events
_INJECT_FLAG = 0xDEAD


def send_unicode_string(text):
    """Send a Unicode string by creating keyboard events with
    CGEventKeyboardSetUnicodeString.
    
    Batches up to 20 characters per event for efficiency (macOS supports
    multi-char unicode strings in a single keyboard event).
    Falls back to per-character for very long strings.
    """
    # Send in chunks — macOS CGEventKeyboardSetUnicodeString supports
    # multi-character strings which is faster and more atomic
    CHUNK = 20
    for i in range(0, len(text), CHUNK):
        chunk = text[i:i+CHUNK]
        # Key down with full chunk
        event_down = CGEventCreateKeyboardEvent(None, 0, True)
        CGEventKeyboardSetUnicodeString(event_down, len(chunk), chunk)
        CGEventSetIntegerValueField(event_down, 99, _INJECT_FLAG)
        CGEventSetFlags(event_down, kCGEventFlagMaskNonCoalesced)
        CGEventPost(kCGSessionEventTap, event_down)

        # Key up
        event_up = CGEventCreateKeyboardEvent(None, 0, False)
        CGEventKeyboardSetUnicodeString(event_up, len(chunk), chunk)
        CGEventSetIntegerValueField(event_up, 99, _INJECT_FLAG)
        CGEventSetFlags(event_up, kCGEventFlagMaskNonCoalesced)
        CGEventPost(kCGSessionEventTap, event_up)

        if i + CHUNK < len(text):
            time.sleep(0.002)  # tiny gap between chunks


def send_backspaces(count):
    """Send `count` backspace key events with tiny delays to prevent swallowing."""
    for i in range(count):
        event_down = CGEventCreateKeyboardEvent(None, KC_DELETE, True)
        CGEventSetIntegerValueField(event_down, 99, _INJECT_FLAG)
        CGEventPost(kCGSessionEventTap, event_down)

        event_up = CGEventCreateKeyboardEvent(None, KC_DELETE, False)
        CGEventSetIntegerValueField(event_up, 99, _INJECT_FLAG)
        CGEventPost(kCGSessionEventTap, event_up)

        # Small gap between backspaces so apps can process them
        if i < count - 1:
            time.sleep(0.003)


def send_key(keycode):
    """Send a single key press+release."""
    event_down = CGEventCreateKeyboardEvent(None, keycode, True)
    CGEventSetIntegerValueField(event_down, 99, _INJECT_FLAG)
    CGEventPost(kCGSessionEventTap, event_down)

    event_up = CGEventCreateKeyboardEvent(None, keycode, False)
    CGEventSetIntegerValueField(event_up, 99, _INJECT_FLAG)
    CGEventPost(kCGSessionEventTap, event_up)


# ============================================================
# IME Engine
# ============================================================
class IMEEngine:
    def __init__(self):
        self.engine = TransliterationEngine('kannada')
        self.lang = 'kannada'
        self.active = True

        self._buf = ''       # Roman input buffer
        self._screen = ''    # Indian text currently on screen

        # Modifier state
        self._cmd = False
        self._ctrl = False
        self._shift = False
        self._option = False

        # Run loop ref for stopping
        self._run_loop = None
        self._tap = None

        # Callbacks for UI
        self._on_state_change = None

        # Suggestion engine
        self._suggestions = None
        self._popup = None
        self._current_suggestions = []
        if HAS_SUGGESTIONS:
            try:
                self._suggestions = SuggestionEngine(min_prefix=3)
                self._popup = SuggestionPopup()
                _dbg('Suggestion engine initialized')
            except Exception as e:
                _dbg(f'Suggestion engine failed: {e}')
                self._suggestions = None
                self._popup = None

    def set_state_callback(self, cb):
        self._on_state_change = cb

    def _notify(self):
        if self._on_state_change:
            self._on_state_change(self.lang, self.active)

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
            # Learn the completed word
            if self._suggestions and self._screen:
                lang_code = LANG_CODES.get(self.lang, '')
                if lang_code:
                    try:
                        self._suggestions.learn_word(self._screen, lang_code)
                    except Exception:
                        pass
        self._buf = ''
        self._screen = ''
        self._current_suggestions = []
        if self._popup:
            try:
                self._popup.hide()
            except Exception:
                pass

    def _update(self):
        """Transliterate buffer and update screen.

        Smart diff: find the common prefix between old and new screen text,
        erase only the changed suffix, and type only the new suffix.
        """
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

        # If new suffix starts with combining char, back up
        to_type = new_text[common:]
        if to_type and common > 0:
            cat = unicodedata.category(to_type[0])
            if cat in ('Mc', 'Mn'):
                common -= 1
                to_type = new_text[common:]

        erase_count = len(self._screen) - common

        _dbg(f'UPDATE buf="{self._buf}" common={common} erase={erase_count} '
             f'type={len(to_type)} new_len={len(new_text)}')

        # Erase changed suffix + type new text with minimal delay
        if erase_count > 0:
            send_backspaces(erase_count)
            # Fixed delay for backspace processing (not per-char — too slow)
            time.sleep(0.01 + 0.002 * erase_count)

        # Type new suffix
        if to_type:
            send_unicode_string(to_type)

        self._screen = new_text

        # Query suggestions
        self._query_suggestions()

    def _query_suggestions(self):
        """Query suggestion engine and update popup."""
        if not self._suggestions or not self._popup:
            return
        if not self._screen or len(self._screen) < 3:
            self._current_suggestions = []
            self._popup.hide()
            return
        lang_code = LANG_CODES.get(self.lang, '')
        if not lang_code:
            return
        try:
            results = self._suggestions.suggest(self._screen, lang_code, limit=5)
            results = [(w, s) for w, s in results if w != self._screen]
            self._current_suggestions = results
            if results:
                # Use cursor position for popup placement
                try:
                    from PyQt5.QtGui import QCursor
                    pos = QCursor.pos()
                    self._popup.show(results, pos.x(), pos.y())
                except Exception:
                    self._popup.show(results)
            else:
                self._popup.hide()
        except Exception as e:
            _dbg(f'Suggestion query failed: {e}')
            self._current_suggestions = []

    def _accept_suggestion(self, index):
        """Accept suggestion at index."""
        if not self._popup or index >= len(self._current_suggestions):
            return False
        word, source = self._current_suggestions[index]
        _dbg(f'ACCEPT suggestion [{index}]: "{word}"')

        # Erase current screen text
        if self._screen:
            n = len(self._screen)
            send_backspaces(n)
            time.sleep(0.01 + 0.002 * n)

        # Type the suggestion
        send_unicode_string(word)

        # Learn the word
        lang_code = LANG_CODES.get(self.lang, '')
        if lang_code and self._suggestions:
            try:
                self._suggestions.learn_word(word, lang_code)
            except Exception:
                pass

        # Reset state
        self._buf = ''
        self._screen = ''
        self._current_suggestions = []
        self._popup.hide()

        # Send a space after the accepted word
        send_unicode_string(' ')
        return True

    def _keycode_to_char(self, keycode):
        """Convert a macOS keycode to a character, accounting for shift."""
        if self._shift and keycode in _KEYCODE_SHIFT_MAP:
            return _KEYCODE_SHIFT_MAP[keycode]
        ch = _KEYCODE_TO_CHAR.get(keycode)
        if ch and self._shift:
            return ch.upper()
        return ch

    def _event_callback(self, proxy, event_type, event, refcon):
        """CGEventTap callback. Process keyboard events."""
        # Re-enable tap if it gets disabled
        if event_type in (kCGEventTapDisabledByTimeout,
                          kCGEventTapDisabledByUserInput):
            _dbg(f'Event tap disabled (type={event_type}), re-enabling')
            if self._tap:
                CGEventTapEnable(self._tap, True)
            return event

        # Only process key events
        if event_type not in (kCGEventKeyDown, kCGEventKeyUp,
                              kCGEventFlagsChanged):
            return event

        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        flags = CGEventGetFlags(event)

        # Skip our own injected events
        user_data = CGEventGetIntegerValueField(event, 99)
        if user_data == _INJECT_FLAG:
            return event

        # ---- Track modifier state from flags ----
        if event_type == kCGEventFlagsChanged:
            self._shift = bool(flags & kCGEventFlagMaskShift)
            self._ctrl = bool(flags & kCGEventFlagMaskControl)
            self._option = bool(flags & kCGEventFlagMaskAlternate)
            self._cmd = bool(flags & kCGEventFlagMaskCommand)
            return event

        # Update modifier state from flags on every key event
        self._shift = bool(flags & kCGEventFlagMaskShift)
        self._ctrl = bool(flags & kCGEventFlagMaskControl)
        self._option = bool(flags & kCGEventFlagMaskAlternate)
        self._cmd = bool(flags & kCGEventFlagMaskCommand)

        # Only process key-down events for main logic
        if event_type != kCGEventKeyDown:
            return event

        # ---- Global shortcuts (always active) ----

        # F11 / F12 → toggle
        if keycode in (KC_F11, KC_F12):
            self.toggle()
            return None  # suppress

        # Cmd+` → switch to English
        if self._cmd and keycode == KC_BACKTICK:
            self._commit()
            self.active = False
            self._notify()
            return None

        # Cmd+Number → language switch
        if self._cmd and not self._option:
            if keycode in _CMD_NUMBER_KEYCODES:
                num = _CMD_NUMBER_KEYCODES[keycode]
                lang_map = {
                    '1': 'assamese',  '2': 'bengali',   '3': 'gujarati',
                    '4': 'hindi',     '5': 'kannada',   '6': 'malayalam',
                    '7': 'marathi',   '8': 'odia',      '9': 'punjabi',
                    '0': 'sanskrit',  '-': 'tamil',     '=': 'telugu',
                }
                if num in lang_map:
                    self.set_language(lang_map[num])
                    return None

        # ---- Number keys 1-5 to accept suggestions ----
        if (self._current_suggestions and self._popup and
                self._popup.is_visible and not self._cmd and
                not self._ctrl and not self._option):
            num_keycodes = {18: 0, 19: 1, 20: 2, 21: 3, 23: 4}  # 1-5
            if keycode in num_keycodes:
                idx = num_keycodes[keycode]
                if idx < len(self._current_suggestions):
                    self._accept_suggestion(idx)
                    return None

        _dbg(f'HOOK kc={keycode} flags=0x{flags:X} '
             f'cmd={self._cmd} ctrl={self._ctrl} '
             f'shift={self._shift} opt={self._option} '
             f'active={self.active} buf="{self._buf}"')

        # ---- If IME is off, pass everything through ----
        if not self.active:
            return event

        # ---- Cmd/Ctrl/Option combos → commit and pass through ----
        if self._cmd or self._ctrl or self._option:
            self._commit()
            return event

        # ---- Backspace ----
        if keycode == KC_DELETE:
            if self._buf:
                self._buf = self._buf[:-1]
                # Erase entire screen text
                if self._screen:
                    n = len(self._screen)
                    send_backspaces(n)
                    time.sleep(0.01 + 0.002 * n)
                self._screen = ''
                # Re-render remaining buffer
                if self._buf:
                    self._update()
                return None  # suppress original backspace
            return event  # empty buffer → pass through

        # ---- Space → commit + send space ----
        if keycode == KC_SPACE:
            self._commit()
            send_unicode_string(' ')
            return None

        # ---- Enter → commit + pass through ----
        if keycode == KC_RETURN:
            self._commit()
            return event

        # ---- Navigation keys → commit + pass through ----
        if keycode in NAV_KEYCODES:
            self._commit()
            return event

        # ---- Convert keycode to character ----
        ch = self._keycode_to_char(keycode)

        if ch:
            # Check caps lock from flags
            caps = bool(flags & 0x00010000)  # kCGEventFlagMaskAlphaShift
            if ch.isalpha():
                want_upper = self._shift ^ caps
                ch = ch.upper() if want_upper else ch.lower()

            _dbg(f'KEY kc={keycode} -> ch={ch!r} buf_before="{self._buf}" '
                 f'shift={self._shift}')

            # Alphabetic or tilde → add to buffer and transliterate
            if ch.isalpha() or ch == '~':
                self._buf += ch
                self._update()
                return None  # suppress original key

            # Digit while there's a buffer
            if ch.isdigit() and self._buf:
                self._buf += ch
                self._update()
                return None

            # Punctuation/other → commit current buffer, send the char
            self._commit()
            send_unicode_string(ch)
            return None

        # Unknown key → commit and pass through
        self._commit()
        return event

    def install_tap(self):
        """Install the CGEventTap. Must have Accessibility permissions."""
        mask = (
            (1 << kCGEventKeyDown) |
            (1 << kCGEventKeyUp) |
            (1 << kCGEventFlagsChanged)
        )

        self._tap = CGEventTapCreate(
            kCGSessionEventTap,
            kCGHeadInsertEventTap,
            kCGEventTapOptionDefault,
            mask,
            self._event_callback,
            None
        )

        if self._tap is None:
            raise RuntimeError(
                "Failed to create event tap. "
                "Accessibility permission may not be granted.\n"
                "Go to System Settings → Privacy & Security → Accessibility "
                "and add this application."
            )

        source = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, self._tap, 0)
        self._run_loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(self._run_loop, source, kCFRunLoopDefaultMode)
        CGEventTapEnable(self._tap, True)

        _dbg('Event tap installed successfully')

    def run_event_loop(self):
        """Run the CFRunLoop. Blocks until stopped."""
        _dbg('Starting CFRunLoop')
        CFRunLoopRun()

    def stop(self):
        """Disable the event tap and stop the run loop."""
        if self._tap:
            CGEventTapEnable(self._tap, False)
            self._tap = None
        if self._run_loop:
            CFRunLoopStop(self._run_loop)
            self._run_loop = None


# ============================================================
# Qt Tray (runs on a background thread — same as Windows)
# ============================================================
def run_tray(ime):
    from PyQt5.QtWidgets import (
        QApplication, QSystemTrayIcon, QMenu, QAction,
        QActionGroup, QMessageBox, QWidget
    )
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

    # Load the app icon for tray
    _icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
    if getattr(sys, '_MEIPASS', None):
        _icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
    # Also check for .png variant on macOS
    if not os.path.exists(_icon_path):
        _icon_path_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
        if getattr(sys, '_MEIPASS', None):
            _icon_path_png = os.path.join(sys._MEIPASS, 'icon.png')
        if os.path.exists(_icon_path_png):
            _icon_path = _icon_path_png
    _app_icon = QIcon(_icon_path) if os.path.exists(_icon_path) else None

    def make_icon(code, active=True):
        # Use the Varnaakshara logo as tray icon
        if _app_icon and not _app_icon.isNull():
            if not active:
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
        p.setFont(QFont('Helvetica Neue', 20, QFont.Bold))
        p.drawText(pm.rect(), Qt.AlignCenter, code.upper())
        p.end()
        return QIcon(pm)

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Initialize suggestion popup on Qt thread
    if ime._popup:
        try:
            ime._popup.init_widget()
            _dbg('Suggestion popup widget initialized')
        except Exception as e:
            _dbg(f'Popup init failed: {e}')

    w = QWidget()
    tray = QSystemTrayIcon(w)

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

    ime.set_state_callback(lambda l, a: refresh())

    # Initial icon
    tray.setIcon(make_icon(LANGUAGES[ime.lang]['code'], True))
    tray.setToolTip(f'Varnaakshara — {LANGUAGES[ime.lang]["name"]}')

    # ── Styled tray menu (purple/gold theme) ──
    _menu_style = """
        QMenu {
            background-color: #1A0E28;
            border: 1px solid #3A2A4A;
            border-radius: 8px;
            padding: 8px 0px;
            font-family: 'Helvetica Neue';
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

    w._atog = QAction('✅  Indian Script   F11/F12', w)
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

    menu.addSeparator()

    settings_action = QAction('⚙️  Settings', w)
    def _open_settings():
        try:
            from settings_ui import SettingsPanel
            w._settings_panel = SettingsPanel()
            w._settings_panel.settings_changed.connect(lambda cfg: (
                ime.set_language(cfg.get('language', 'kannada')),
                refresh()
            ))
            w._settings_panel.show()
        except Exception as e:
            _dbg(f'Settings panel error: {e}')
    settings_action.triggered.connect(_open_settings)
    menu.addAction(settings_action)

    menu.addSeparator()

    about_action = QAction('ℹ️  About', w)
    def _show_about():
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QPixmap, QFont as QF

        dlg = QDialog()
        dlg.setWindowTitle('About Varnaakshara')
        dlg.setFixedSize(480, 640)
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

        # Logo
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        if getattr(sys, '_MEIPASS', None):
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        if not os.path.exists(icon_path):
            icon_path_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
            if getattr(sys, '_MEIPASS', None):
                icon_path_png = os.path.join(sys._MEIPASS, 'icon.png')
            if os.path.exists(icon_path_png):
                icon_path = icon_path_png
        if os.path.exists(icon_path):
            logo_label = QLabel()
            pm = QPixmap(icon_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pm)
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        # Title in Sanskrit
        title = QLabel('वर्णाक्षरः')
        title.setFont(QF('Noto Sans Devanagari', 28, QF.Bold))
        title.setStyleSheet('color: #E8C862; margin-top: 5px;')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        sub = QLabel('Varnaakshara IME v1.0.0')
        sub.setFont(QF('Helvetica Neue', 12))
        sub.setStyleSheet('color: #8A7B9A;')
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        div1 = QLabel()
        div1.setFixedHeight(1)
        div1.setStyleSheet('background: #C9973E; margin: 8px 40px; opacity: 0.3;')
        layout.addWidget(div1)

        desc = QLabel('Type in English → Get output in Indian scripts')
        desc.setFont(QF('Helvetica Neue', 11))
        desc.setStyleSheet('color: #B8A88A;')
        desc.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc)

        langs_text = (
            '<table cellspacing="6" style="color:#A89878; font-size:11px;" align="center">'
            '<tr><td>ಕನ್ನಡ Kannada</td><td>•</td><td>हिन्दी Hindi</td><td>•</td><td>తెలుగు Telugu</td></tr>'
            '<tr><td>தமிழ் Tamil</td><td>•</td><td>বাংলা Bengali</td><td>•</td><td>ગુજ Gujarati</td></tr>'
            '<tr><td>മലയാളം Malayalam</td><td>•</td><td>ଓଡ଼ିଆ Odia</td><td>•</td><td>ਪੰਜਾਬી Punjabi</td></tr>'
            '<tr><td>संस्कृत Sanskrit</td><td>•</td><td>অसमीया Assamese</td><td>•</td><td>मराठी Marathi</td></tr>'
            '</table>'
        )
        langs = QLabel(langs_text)
        langs.setAlignment(Qt.AlignCenter)
        layout.addWidget(langs)

        div2 = QLabel()
        div2.setFixedHeight(1)
        div2.setStyleSheet('background: #C9973E; margin: 8px 40px; opacity: 0.3;')
        layout.addWidget(div2)

        shortcuts_text = (
            '<table cellspacing="4" style="color:#7A6B8A; font-size:10px;" align="center">'
            '<tr><td style="color:#C9973E;">F11 / F12</td><td>Toggle Indian / English</td></tr>'
            '<tr><td style="color:#C9973E;">⌘1-0</td><td>Select language</td></tr>'
            '<tr><td style="color:#C9973E;">⌘`</td><td>English mode</td></tr>'
            '</table>'
        )
        sc = QLabel(shortcuts_text)
        sc.setAlignment(Qt.AlignCenter)
        layout.addWidget(sc)

        # Accessibility note
        acc = QLabel('⚠️ Requires Accessibility permission in\nSystem Settings → Privacy & Security')
        acc.setFont(QF('Helvetica Neue', 9))
        acc.setStyleSheet('color: #5A4B6A;')
        acc.setAlignment(Qt.AlignCenter)
        layout.addWidget(acc)

        layout.addStretch()

        contact = QLabel('<a href="mailto:aksaram.folios@gmail.com" style="color:#C9973E; text-decoration:none;">aksaram.folios@gmail.com</a>')
        contact.setOpenExternalLinks(True)
        contact.setAlignment(Qt.AlignCenter)
        contact.setFont(QF('Helvetica Neue', 10))
        layout.addWidget(contact)

        copy_lbl = QLabel('© 2026 Varnaakshara Project. Free and not for sale.')
        copy_lbl.setFont(QF('Helvetica Neue', 9))
        copy_lbl.setStyleSheet('color: #5A4B6A;')
        copy_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(copy_lbl)

        layout.addSpacing(10)
        btn = QPushButton('Close')
        btn.setFixedWidth(140)
        btn.clicked.connect(dlg.close)
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        if _app_icon:
            dlg.setWindowIcon(_app_icon)
        dlg.exec_()

    about_action.triggered.connect(_show_about)
    menu.addAction(about_action)

    # Check for Updates
    update_action = QAction('🔄  Check for Updates', w)
    def _check_updates():
        try:
            from updater import check_and_prompt, CURRENT_VERSION
            result = check_and_prompt(force=True)
            if result is None:
                msg = QMessageBox()
                msg.setWindowTitle('Varnaakshara')
                msg.setText('You\'re up to date!')
                msg.setInformativeText(f'Version {CURRENT_VERSION}')
                msg.setIcon(QMessageBox.Information)
                if _app_icon:
                    msg.setWindowIcon(_app_icon)
                msg.exec_()
        except Exception as e:
            _dbg(f'Update check error: {e}')
    update_action.triggered.connect(_check_updates)
    menu.addAction(update_action)

    menu.addSeparator()

    quit_action = QAction('❌  Quit', w)
    quit_action.triggered.connect(lambda: (ime.stop(), tray.hide(),
                                           app.quit(), os._exit(0)))
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.activated.connect(
        lambda r: ime.toggle() if r == QSystemTrayIcon.DoubleClick else None)
    tray.show()
    tray.showMessage('Varnaakshara',
                     f'{LANGUAGES[ime.lang]["name"]} mode active\n'
                     'F11/F12 to toggle',
                     QSystemTrayIcon.Information, 3000)

    # Poll for state changes from hook thread
    timer = QTimer()
    timer.timeout.connect(refresh)
    timer.start(500)

    app.exec_()


# ============================================================
# Main
# ============================================================
def check_single_instance():
    """Ensure only one instance of Varnaakshara runs at a time.
    Uses a file-based lock since macOS has no CreateMutexW.
    Lock file at ~/Library/Application Support/Varnaakshara/.lock
    """
    lock_dir = os.path.expanduser('~/Library/Application Support/Varnaakshara')
    os.makedirs(lock_dir, exist_ok=True)
    lock_path = os.path.join(lock_dir, '.lock')
    try:
        _lock_fh = open(lock_path, 'w')
        fcntl.flock(_lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Keep file handle alive — store on module
        check_single_instance._fh = _lock_fh
        return True
    except (IOError, OSError):
        return False


def main():
    # Single instance check
    if not check_single_instance():
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            from PyQt5.QtGui import QIcon
            app = QApplication(sys.argv)
            msg = QMessageBox()
            msg.setWindowTitle('Varnaakshara')
            msg.setText('Varnaakshara is already running!')
            msg.setInformativeText(
                'The application is active in the system tray.\n\n'
                'Right-click the tray icon for options.\n'
                'F11/F12 to toggle Indian script mode.'
            )
            msg.setIcon(QMessageBox.Information)
            # Load icon if available
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
            if getattr(sys, '_MEIPASS', None):
                icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
            if not os.path.exists(icon_path):
                icon_path_png = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
                if getattr(sys, '_MEIPASS', None):
                    icon_path_png = os.path.join(sys._MEIPASS, 'icon.png')
                if os.path.exists(icon_path_png):
                    icon_path = icon_path_png
            if os.path.exists(icon_path):
                msg.setWindowIcon(QIcon(icon_path))
            msg.exec_()
        except Exception:
            print('Varnaakshara is already running!')
        sys.exit(0)

    if not HAS_QUARTZ:
        print("ERROR: pyobjc-framework-Quartz is required on macOS.")
        print("Install with: pip install pyobjc-framework-Quartz pyobjc-framework-Cocoa")
        sys.exit(1)

    # Mandatory update check — blocks app if newer version exists
    try:
        from updater import check_for_update
        update_info = check_for_update(force=False)
        if update_info:
            from PyQt5.QtWidgets import QApplication
            _upd_app = QApplication(sys.argv)
            from updater import show_update_dialog
            show_update_dialog(update_info, blocking=True)
            sys.exit(0)
    except Exception as e:
        print(f'[Varnaakshara] Update check skipped: {e}')

    # Check accessibility permissions
    if not check_accessibility():
        print("ERROR: Accessibility permission not granted.")
        print("Go to System Settings → Privacy & Security → Accessibility")
        print("and add this application.")
        show_accessibility_dialog()
        sys.exit(1)

    ime = IMEEngine()

    # macOS requires ALL UI (AppKit/Qt) on the main thread.
    # CFRunLoop for the event tap runs on a background thread.
    def _run_event_tap():
        try:
            ime.install_tap()
            ime.run_event_loop()
        except RuntimeError as e:
            print(f'ERROR: {e}')
        except Exception as e:
            print(f'Event tap error: {e}')

    tap_thread = threading.Thread(target=_run_event_tap, daemon=True)
    tap_thread.start()

    # Give the tap a moment to install
    time.sleep(0.5)

    # Run Qt tray on the MAIN thread (required by macOS AppKit)
    try:
        run_tray(ime)
    except KeyboardInterrupt:
        ime.stop()
        print('\nVarnaakshara stopped.')


if __name__ == '__main__':
    main()
