"""
MacOSIME — macOS-specific Varnaakshara IME implementation.

Extends VarnaaksharaIMEBase with:
- CGEventTapCreate for keyboard event interception
- CGEventPost + CGEventKeyboardSetUnicodeString for text injection
- CFRunLoop for event processing
- macOS Accessibility permission detection

IMPORTANT: Requires macOS Accessibility permissions.
System Preferences → Privacy & Security → Accessibility
"""

import sys
import os
import time
import threading

from .ime_base import (
    VarnaaksharaIMEBase, LANGUAGES, SUPPORTED_LANGUAGES,
    _dbg, setup_debug_log,
)

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
KC_RIGHT_COMMAND = 54
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
KC_BACKTICK = 50

NAV_KEYCODES = frozenset({
    KC_LEFT, KC_RIGHT, KC_UP, KC_DOWN,
    KC_HOME, KC_END, KC_PAGE_UP, KC_PAGE_DOWN,
    KC_FORWARD_DELETE, KC_ESCAPE, KC_TAB,
})

# US keyboard layout keycode → char
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

_CMD_LANG_MAP = {
    '1': 'assamese',  '2': 'bengali',   '3': 'gujarati',
    '4': 'hindi',     '5': 'kannada',   '6': 'malayalam',
    '7': 'marathi',   '8': 'odia',      '9': 'punjabi',
    '0': 'sanskrit',  '-': 'tamil',     '=': 'telugu',
}


# ============================================================
# Marker for injected events
# ============================================================
_INJECT_FLAG = 0xDEAD


# ============================================================
# Accessibility check
# ============================================================
def check_accessibility():
    """Check if Accessibility permissions are granted."""
    try:
        import ApplicationServices
        trusted = ApplicationServices.AXIsProcessTrustedWithOptions({
            'AXTrustedCheckOptionPrompt': True
        })
        return trusted
    except (ImportError, AttributeError):
        try:
            mask = (1 << kCGEventKeyDown)
            tap = CGEventTapCreate(
                kCGSessionEventTap, kCGHeadInsertEventTap,
                kCGEventTapOptionDefault, mask,
                lambda *a: None, None
            )
            return tap is not None
        except Exception:
            return False


def show_accessibility_dialog():
    """Show a PyQt5 dialog explaining how to enable Accessibility."""
    from PyQt5.QtWidgets import QApplication, QMessageBox
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
    )
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


# ============================================================
# MacOSIME
# ============================================================
class MacOSIME(VarnaaksharaIMEBase):
    """macOS implementation of the Varnaakshara IME.

    Uses CGEventTap for keyboard interception and CGEventPost
    for Unicode text injection.
    """

    def __init__(self, language='kannada', scheme='baraha', custom_mappings=None):
        super().__init__(language=language, scheme=scheme,
                         custom_mappings=custom_mappings)
        self.active = True  # macOS starts active by default
        self._tap = None
        self._run_loop = None

    # ============================================================
    # Abstract method implementations
    # ============================================================

    def _send_text(self, text):
        """Send Unicode string via CGEventKeyboardSetUnicodeString."""
        CHUNK = 20
        for i in range(0, len(text), CHUNK):
            chunk = text[i:i + CHUNK]
            event_down = CGEventCreateKeyboardEvent(None, 0, True)
            CGEventKeyboardSetUnicodeString(event_down, len(chunk), chunk)
            CGEventSetIntegerValueField(event_down, 99, _INJECT_FLAG)
            CGEventSetFlags(event_down, kCGEventFlagMaskNonCoalesced)
            CGEventPost(kCGSessionEventTap, event_down)

            event_up = CGEventCreateKeyboardEvent(None, 0, False)
            CGEventKeyboardSetUnicodeString(event_up, len(chunk), chunk)
            CGEventSetIntegerValueField(event_up, 99, _INJECT_FLAG)
            CGEventSetFlags(event_up, kCGEventFlagMaskNonCoalesced)
            CGEventPost(kCGSessionEventTap, event_up)

            if i + CHUNK < len(text):
                time.sleep(0.002)

    def _send_backspaces(self, count):
        """Send backspace key events with tiny delays."""
        for i in range(count):
            event_down = CGEventCreateKeyboardEvent(None, KC_DELETE, True)
            CGEventSetIntegerValueField(event_down, 99, _INJECT_FLAG)
            CGEventPost(kCGSessionEventTap, event_down)

            event_up = CGEventCreateKeyboardEvent(None, KC_DELETE, False)
            CGEventSetIntegerValueField(event_up, 99, _INJECT_FLAG)
            CGEventPost(kCGSessionEventTap, event_up)

            if i < count - 1:
                time.sleep(0.003)

    def _apply_screen_edit(self, erase_count, to_type):
        """Sequential: send backspaces, delay, then type new text."""
        if erase_count > 0:
            self._send_backspaces(erase_count)
            time.sleep(0.01 + 0.002 * erase_count)
        if to_type:
            self._send_text(to_type)

    def _get_caret_screen_pos(self):
        """Get caret position. Falls back to cursor position."""
        try:
            from PyQt5.QtGui import QCursor
            pos = QCursor.pos()
            return (pos.x(), pos.y())
        except Exception:
            return (None, None)

    # ============================================================
    # Override handle_backspace for macOS timing
    # ============================================================

    def handle_backspace(self):
        """Handle Backspace — macOS version erases everything and re-renders."""
        if self._buf:
            self._buf = self._buf[:-1]
            # Erase entire screen text
            if self._screen:
                n = len(self._screen)
                self._send_backspaces(n)
                time.sleep(0.01 + 0.002 * n)
            self._screen = ''
            # Re-render remaining buffer
            if self._buf:
                self._update()
            else:
                self._query_suggestions()
            return True  # suppress
        return False  # pass through

    # ============================================================
    # Keycode to character
    # ============================================================

    def _keycode_to_char(self, keycode, flags):
        """Convert macOS keycode to character, accounting for shift."""
        if self._shift and keycode in _KEYCODE_SHIFT_MAP:
            return _KEYCODE_SHIFT_MAP[keycode]
        ch = _KEYCODE_TO_CHAR.get(keycode)
        if ch and self._shift:
            return ch.upper()
        return ch

    # ============================================================
    # Event tap callback
    # ============================================================

    def _event_callback(self, proxy, event_type, event, refcon):
        """CGEventTap callback."""
        # Re-enable tap if disabled
        if event_type in (kCGEventTapDisabledByTimeout,
                          kCGEventTapDisabledByUserInput):
            _dbg(f'Event tap disabled (type={event_type}), re-enabling')
            if self._tap:
                CGEventTapEnable(self._tap, True)
            return event

        if event_type not in (kCGEventKeyDown, kCGEventKeyUp,
                              kCGEventFlagsChanged):
            return event

        keycode = CGEventGetIntegerValueField(event, kCGKeyboardEventKeycode)
        flags = CGEventGetFlags(event)

        # Skip injected events
        if CGEventGetIntegerValueField(event, 99) == _INJECT_FLAG:
            return event

        # Track modifiers
        if event_type == kCGEventFlagsChanged:
            self._shift = bool(flags & kCGEventFlagMaskShift)
            self._ctrl = bool(flags & kCGEventFlagMaskControl)
            self._alt = bool(flags & kCGEventFlagMaskAlternate)
            self._cmd = bool(flags & kCGEventFlagMaskCommand)
            return event

        self._shift = bool(flags & kCGEventFlagMaskShift)
        self._ctrl = bool(flags & kCGEventFlagMaskControl)
        self._alt = bool(flags & kCGEventFlagMaskAlternate)
        self._cmd = bool(flags & kCGEventFlagMaskCommand)

        if event_type != kCGEventKeyDown:
            return event

        # ---- Global shortcuts ----

        if keycode in (KC_F11, KC_F12):
            self.handle_toggle()
            return None

        if self._cmd and keycode == KC_BACKTICK:
            self.handle_english_mode()
            return None

        if self._cmd and not self._alt and keycode in _CMD_NUMBER_KEYCODES:
            num = _CMD_NUMBER_KEYCODES[keycode]
            if num in _CMD_LANG_MAP:
                self.handle_language_switch(_CMD_LANG_MAP[num])
                return None

        # ---- Suggestion accept (1-5) ----
        if (self._current_suggestions and self._popup and
                self._popup.is_visible and
                not self._cmd and not self._ctrl and not self._alt):
            num_keycodes = {18: 0, 19: 1, 20: 2, 21: 3, 23: 4}
            if keycode in num_keycodes:
                idx = num_keycodes[keycode]
                if idx < len(self._current_suggestions):
                    self.handle_suggestion_accept(idx)
                    return None

        _dbg(f'HOOK kc={keycode} flags=0x{flags:X} '
             f'cmd={self._cmd} ctrl={self._ctrl} '
             f'shift={self._shift} opt={self._alt} '
             f'active={self.active} buf="{self._buf}"')

        # ---- IME off → pass through ----
        if not self.active:
            return event

        # ---- Cmd/Ctrl/Option combos ----
        if self._cmd or self._ctrl or self._alt:
            self.handle_ctrl_combo()
            return event

        # ---- Backspace ----
        if keycode == KC_DELETE:
            if self.handle_backspace():
                return None
            return event

        # ---- Space ----
        if keycode == KC_SPACE:
            self.handle_space()
            return None

        # ---- Enter ----
        if keycode == KC_RETURN:
            self.handle_enter()
            return event

        # ---- Navigation ----
        if keycode in NAV_KEYCODES:
            self.handle_nav()
            return event

        # ---- Convert keycode to character ----
        ch = self._keycode_to_char(keycode, flags)

        if ch:
            caps = bool(flags & 0x00010000)  # kCGEventFlagMaskAlphaShift
            if ch.isalpha():
                want_upper = self._shift ^ caps
                ch = ch.upper() if want_upper else ch.lower()

            _dbg(f'KEY kc={keycode} -> ch={ch!r} buf="{self._buf}" '
                 f'shift={self._shift}')

            if self.handle_char(ch):
                return None

        # Unknown → commit and pass through
        self._commit()
        return event

    # ============================================================
    # Tap lifecycle
    # ============================================================

    def start(self):
        """Install the CGEventTap."""
        if not HAS_QUARTZ:
            raise ImportError(
                "pyobjc-framework-Quartz is required on macOS. "
                "Install with: pip install pyobjc-framework-Quartz"
            )
        mask = (
            (1 << kCGEventKeyDown) |
            (1 << kCGEventKeyUp) |
            (1 << kCGEventFlagsChanged)
        )
        self._tap = CGEventTapCreate(
            kCGSessionEventTap, kCGHeadInsertEventTap,
            kCGEventTapOptionDefault, mask,
            self._event_callback, None
        )
        if self._tap is None:
            raise RuntimeError(
                "Failed to create event tap. "
                "Accessibility permission may not be granted."
            )
        source = CFMachPortCreateRunLoopSource(
            kCFAllocatorDefault, self._tap, 0
        )
        self._run_loop = CFRunLoopGetCurrent()
        CFRunLoopAddSource(self._run_loop, source, kCFRunLoopDefaultMode)
        CGEventTapEnable(self._tap, True)
        _dbg('Event tap installed')

    # Alias for backward compatibility
    install_tap = start

    def run_event_loop(self):
        """Run the CFRunLoop. Blocks until stopped."""
        _dbg('Starting CFRunLoop')
        CFRunLoopRun()

    def stop(self):
        """Disable event tap and stop run loop."""
        if self._tap:
            CGEventTapEnable(self._tap, False)
            self._tap = None
        if self._run_loop:
            CFRunLoopStop(self._run_loop)
            self._run_loop = None
        _dbg('Event tap removed')


# ============================================================
# Single instance check (macOS)
# ============================================================
def check_single_instance():
    """Ensure only one instance using file lock."""
    import fcntl
    lock_dir = os.path.expanduser(
        '~/Library/Application Support/Varnaakshara'
    )
    os.makedirs(lock_dir, exist_ok=True)
    lock_path = os.path.join(lock_dir, '.lock')
    try:
        _lock_fh = open(lock_path, 'w')
        fcntl.flock(_lock_fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
        check_single_instance._fh = _lock_fh
        return True
    except (IOError, OSError):
        return False
