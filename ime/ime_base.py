"""
VarnaaksharaIMEBase — Abstract base class for the Varnaakshara IME.

Extracts ALL shared logic from the Windows and macOS IME implementations:
- Buffer management (Roman input → Indic output on screen)
- Transliteration via the new table-driven engine (core.engine.transliteration)
- Input mode switching (Phonetic Baraha / Phonetic ITRANS / INSCRIPT)
- Output mode switching (Unicode / ANSI with font family selection)
- Reverse transliteration
- Clipboard conversion (Unicode↔ANSI, script-to-script)
- Input scheme switching (Baraha vs ITRANS)
- Suggestion engine integration (async worker thread)
- Language management for 12 Indian scripts
- Debug logging

Platform subclasses implement ONLY:
- Keyboard hooking / event tapping
- Text injection (SendInput on Win, CGEventPost on macOS)
- Event loop management
- Caret position detection
"""

import os
import sys
import threading
import queue
import unicodedata
import datetime
import logging
from abc import ABC, abstractmethod

# Add project root to path for imports
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from core.engine.transliteration import TransliterationEngine, SUPPORTED_LANGUAGES

# Re-export for compatibility with existing tray/UI code
LANGUAGES = SUPPORTED_LANGUAGES

# Suggestion engine (optional)
try:
    from suggestions import SuggestionEngine, LANG_CODES
    HAS_SUGGESTIONS = True
except ImportError:
    HAS_SUGGESTIONS = False
    LANG_CODES = {}

# SuggestionPopup — try both implementations
try:
    from suggestion_popup import SuggestionPopup
    HAS_POPUP = True
except ImportError:
    try:
        from suggestion_popup_qt import SuggestionPopup
        HAS_POPUP = True
    except ImportError:
        HAS_POPUP = False
        SuggestionPopup = None


# ============================================================
# INPUT MODES
# ============================================================

INPUT_MODE_PHONETIC_BARAHA = 'phonetic_baraha'
INPUT_MODE_PHONETIC_ITRANS = 'phonetic_itrans'
INPUT_MODE_INSCRIPT = 'inscript'

VALID_INPUT_MODES = {
    INPUT_MODE_PHONETIC_BARAHA,
    INPUT_MODE_PHONETIC_ITRANS,
    INPUT_MODE_INSCRIPT,
}

# ============================================================
# OUTPUT MODES
# ============================================================

OUTPUT_MODE_UNICODE = 'unicode'
OUTPUT_MODE_BARAHA = 'baraha'
OUTPUT_MODE_SHREELIPI = 'shreelipi'

# Backward compatibility alias
OUTPUT_MODE_ANSI = OUTPUT_MODE_BARAHA

VALID_OUTPUT_MODES = {OUTPUT_MODE_UNICODE, OUTPUT_MODE_BARAHA, OUTPUT_MODE_SHREELIPI}

# Default ANSI font families
ANSI_FONT_FAMILIES = ['baraha', 'shree', 'kruti', 'shreelipi']


# ============================================================
# Debug Logging
# ============================================================

_logger = logging.getLogger('varnaakshara.ime')


def _dbg(msg):
    """Write a debug log message with timestamp."""
    _logger.debug(msg)


def setup_debug_log(log_path=None):
    """Set up file-based debug logging."""
    if log_path is None:
        log_path = os.path.join(
            os.path.dirname(os.path.abspath(sys.argv[0] if sys.argv[0] else __file__)),
            'varnaakshara_debug.log'
        )
    handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
    handler.setFormatter(logging.Formatter('[%(asctime)s.%(msecs)03d] %(message)s',
                                           datefmt='%H:%M:%S'))
    _logger.addHandler(handler)
    _logger.setLevel(logging.DEBUG)


# ============================================================
# Grapheme cluster counting
# ============================================================

# Viramas for all supported Indic scripts
_VIRAMAS = frozenset({
    '\u094D',  # Devanagari
    '\u09CD',  # Bengali
    '\u0A4D',  # Gurmukhi
    '\u0ACD',  # Gujarati
    '\u0B4D',  # Odia
    '\u0BCD',  # Tamil
    '\u0C4D',  # Telugu
    '\u0CCD',  # Kannada
    '\u0D4D',  # Malayalam
})


def grapheme_len(text):
    """Count grapheme clusters in Indic text.

    A grapheme cluster = base char + all following combining marks (Mc/Mn)
    + any conjunct extensions (virama + consonant chains).
    Matches what a single Backspace key deletes in Word/Notepad.
    """
    count = 0
    i = 0
    while i < len(text):
        cat = unicodedata.category(text[i])
        if cat in ('Mc', 'Mn'):
            count += 1
            i += 1
            continue
        count += 1
        i += 1
        while i < len(text):
            c = unicodedata.category(text[i])
            if c in ('Mc', 'Mn'):
                is_virama = text[i] in _VIRAMAS
                i += 1
                if is_virama and i < len(text) and unicodedata.category(text[i]) == 'Lo':
                    i += 1
            else:
                break
    return count


# ============================================================
# VarnaaksharaIMEBase
# ============================================================

class VarnaaksharaIMEBase(ABC):
    """Abstract base class for the Varnaakshara IME.

    Subclasses must implement the platform-specific methods for keyboard
    hooking, text injection, and event loops. All transliteration logic,
    buffer management, mode switching, and suggestion handling live here.
    """

    def __init__(self, language='kannada', scheme='baraha', custom_mappings=None):
        # ── Transliteration engine (NEW table-driven engine) ──
        self.engine = TransliterationEngine(language, scheme=scheme,
                                            custom_mappings=custom_mappings)
        self.lang = language
        self.scheme = scheme
        self.active = False  # Start in English mode

        # ── Input mode ──
        self._input_mode = INPUT_MODE_PHONETIC_BARAHA
        if scheme == 'itrans':
            self._input_mode = INPUT_MODE_PHONETIC_ITRANS

        # ── Output mode ──
        self._output_mode = OUTPUT_MODE_UNICODE
        self._ansi_font_family = 'baraha'

        # ── Buffer state ──
        self._buf = ''      # Roman input buffer
        self._screen = ''   # Indic text currently visible on screen

        # ── Modifier state (tracked by platform hook) ──
        self._ctrl = False
        self._alt = False
        self._shift = False
        self._cmd = False   # macOS Command key

        # ── State change callback ──
        self._on_state_change = None

        # ── Suggestion engine ──
        self._suggestions = None
        self._popup = None
        self._current_suggestions = []
        self._suggestion_queue = queue.Queue()
        self._suggestions_enabled = False
        self._suggestion_worker_thread = None

        # ── Clipboard conversion hotkey (default: Ctrl+Shift+C / Cmd+Shift+C) ──
        self._clipboard_hotkey = 'ctrl+shift+c'

        _dbg(f'IMEBase init: lang={language}, scheme={scheme}, '
             f'mode={self._input_mode}')

    # ============================================================
    # STATE CALLBACK
    # ============================================================

    def set_state_callback(self, cb):
        """Set callback for state changes: cb(lang, active)."""
        self._on_state_change = cb

    def _notify(self):
        """Notify the UI of a state change."""
        if self._on_state_change:
            self._on_state_change(self.lang, self.active)

    # ============================================================
    # LANGUAGE MANAGEMENT
    # ============================================================

    def set_language(self, key):
        """Switch to a different language. Commits current buffer first."""
        if key not in SUPPORTED_LANGUAGES:
            _dbg(f'Unknown language: {key}')
            return
        self._commit()
        self.lang = key
        self.engine.set_language(key)
        self.active = True
        _dbg(f'Language changed to: {key}')
        self._notify()

    # ============================================================
    # INPUT SCHEME / MODE MANAGEMENT
    # ============================================================

    def set_scheme(self, scheme):
        """Switch input scheme (baraha/itrans). Commits current buffer first."""
        self._commit()
        self.scheme = scheme
        self.engine.set_scheme(scheme)
        # Update input mode to match
        if scheme == 'baraha':
            self._input_mode = INPUT_MODE_PHONETIC_BARAHA
        elif scheme == 'itrans':
            self._input_mode = INPUT_MODE_PHONETIC_ITRANS
        _dbg(f'Scheme changed to: {scheme}')

    def set_input_mode(self, mode):
        """Set input mode: phonetic_baraha, phonetic_itrans, or inscript.

        For phonetic modes, also updates the underlying scheme.
        For INSCRIPT, uses the engine's keyboard layout transliteration.
        """
        if mode not in VALID_INPUT_MODES:
            _dbg(f'Invalid input mode: {mode}')
            return
        self._commit()
        self._input_mode = mode
        if mode == INPUT_MODE_PHONETIC_BARAHA:
            self.scheme = 'baraha'
            self.engine.set_scheme('baraha')
        elif mode == INPUT_MODE_PHONETIC_ITRANS:
            self.scheme = 'itrans'
            self.engine.set_scheme('itrans')
        elif mode == INPUT_MODE_INSCRIPT:
            pass  # INSCRIPT uses get_keyboard_layout, no scheme change
        _dbg(f'Input mode changed to: {mode}')
        self._notify()

    # ============================================================
    # OUTPUT MODE MANAGEMENT
    # ============================================================

    def set_output_mode(self, mode, font_family=None):
        """Set output mode: unicode, baraha, or shreelipi.

        For ANSI modes (baraha/shreelipi), optionally set the font family.
        Accepts legacy 'ansi' as alias for 'baraha'.
        """
        # Legacy alias: 'ansi' → 'baraha'
        if mode == 'ansi':
            mode = OUTPUT_MODE_BARAHA
        if mode not in VALID_OUTPUT_MODES:
            _dbg(f'Invalid output mode: {mode}')
            return
        self._output_mode = mode
        if font_family:
            self._ansi_font_family = font_family
        elif mode == OUTPUT_MODE_SHREELIPI:
            self._ansi_font_family = 'shreelipi'
        elif mode == OUTPUT_MODE_BARAHA:
            self._ansi_font_family = 'baraha'
        _dbg(f'Output mode: {mode}, font_family={self._ansi_font_family}')

    # ============================================================
    # CUSTOM MAPPINGS
    # ============================================================

    def set_custom_mappings(self, custom_mappings):
        """Update custom key→character mappings on the engine."""
        self.engine.set_custom_mappings(custom_mappings)
        _dbg(f'Custom mappings updated')

    # ============================================================
    # TOGGLE
    # ============================================================

    def toggle(self):
        """Toggle IME active/inactive."""
        self._commit()
        self.active = not self.active
        _dbg(f'Toggle: active={self.active}')
        self._notify()

    # ============================================================
    # BUFFER MANAGEMENT
    # ============================================================

    def _commit(self):
        """Finalize current word — text stays on screen, reset buffers."""
        if self._buf:
            _dbg(f'COMMIT buf="{self._buf}" screen="{self._screen}"')
            # Learn the completed word
            if self._suggestions and self._screen:
                lang_code = LANG_CODES.get(self.lang, '')
                if lang_code:
                    self._safe_learn(self._screen, lang_code)
        self._buf = ''
        self._screen = ''
        self._current_suggestions = []
        if self._popup:
            try:
                self._popup.hide()
            except Exception:
                pass

    def _transliterate_buffer(self):
        """Transliterate the current buffer based on input mode and output mode.

        Returns the target-script string ready for display.
        """
        if not self._buf:
            return ''

        # Stage 1: Input conversion based on mode
        if self._input_mode == INPUT_MODE_INSCRIPT:
            result = self.engine.transliterate_inscript(self._buf)
        else:
            # Phonetic (Baraha or ITRANS — engine already set to correct scheme)
            result = self.engine.transliterate(self._buf)

        # Stage 2: Output conversion
        if self._output_mode in (OUTPUT_MODE_BARAHA, OUTPUT_MODE_SHREELIPI):
            result = self.engine.to_ansi(result, font_family=self._ansi_font_family)

        return result

    def _update(self):
        """Transliterate buffer and update screen text.

        Uses smart diff: finds the common prefix between old and new
        screen text, erases only the changed suffix, and types only
        the new suffix. Handles combining characters correctly.
        """
        if not self._buf:
            return

        new_text = self._transliterate_buffer()
        if new_text == self._screen:
            return

        # Find longest common prefix
        common = 0
        for i in range(min(len(self._screen), len(new_text))):
            if self._screen[i] == new_text[i]:
                common += 1
            else:
                break

        # If new suffix starts with combining char, back up one
        to_type = new_text[common:]
        if to_type and common > 0:
            cat = unicodedata.category(to_type[0])
            if cat in ('Mc', 'Mn'):
                common -= 1
                to_type = new_text[common:]

        erase_count = len(self._screen) - common

        _dbg(f'UPDATE buf="{self._buf}" common={common} '
             f'erase={erase_count} type={len(to_type)} '
             f'new_len={len(new_text)}')

        # Platform-specific: erase old suffix + type new suffix
        self._apply_screen_edit(erase_count, to_type)

        self._screen = new_text

        # Query suggestions
        self._query_suggestions()

    # ============================================================
    # KEY HANDLING — called by platform hook/callback
    # ============================================================

    def handle_toggle(self):
        """Handle F11/F12 toggle. Returns True (always handled)."""
        self.toggle()
        return True

    def handle_english_mode(self):
        """Handle Ctrl+`/Cmd+` — switch to English. Returns True."""
        self._commit()
        self.active = False
        self._notify()
        return True

    def handle_language_switch(self, lang_key):
        """Handle Ctrl+num/Cmd+num language switch. Returns True."""
        if lang_key in SUPPORTED_LANGUAGES:
            self.set_language(lang_key)
            return True
        return False

    def handle_backspace(self):
        """Handle Backspace key.

        Returns True if the IME consumed the backspace (suppress original).
        Returns False if the platform should pass through the original key.
        """
        if self._buf:
            self._buf = self._buf[:-1]
            if self._buf:
                self._update()
            else:
                # Buffer empty → erase everything on screen
                if self._screen:
                    self._send_backspaces(len(self._screen))
                self._screen = ''
                self._query_suggestions()
            return True  # suppress
        return False  # pass through (empty buffer, normal backspace)

    def handle_space(self):
        """Handle Space key. Commits buffer, sends space. Returns True."""
        self._commit()
        self._send_text(' ')
        return True

    def handle_enter(self):
        """Handle Enter key. Commits buffer. Returns False (pass through)."""
        self._commit()
        return False  # let platform pass through the Enter key

    def handle_nav(self):
        """Handle navigation keys (arrows, Home, End, etc.).
        Commits buffer. Returns False (pass through)."""
        self._commit()
        return False

    def handle_ctrl_combo(self):
        """Handle Ctrl/Cmd/Alt combos. Commits buffer.
        Returns False (pass through)."""
        self._commit()
        return False

    def handle_char(self, ch):
        """Handle a character input.

        Determines whether the character should be buffered for
        transliteration, sent as a native numeral, or committed
        with the character sent directly.

        Returns True if handled (suppress original key), False to pass through.
        """
        if not self.active:
            return False

        # Alphabetic or tilde → add to buffer and transliterate
        if ch.isalpha() or ch == '~':
            self._buf += ch
            self._update()
            return True

        # Baraha symbol chars → route through transliteration
        if ch in ('&', '|', '#', '$'):
            self._buf += ch
            self._update()
            return True

        # Digit → convert to native script numeral
        if ch.isdigit():
            if self._buf:
                self._commit()
            native = self.engine.transliterate(ch)
            self._send_text(native)
            return True

        # OM. trigger → convert OM to ॐ symbol
        if ch == '.' and self._buf.endswith('OM'):
            if self._screen:
                self._send_backspaces(len(self._screen))
            pre = self._buf[:-2]
            if pre:
                pre_text = self._transliterate_buffer_text(pre)
                self._send_text(pre_text)
            self._send_text('\u0950')
            self._buf = ''
            self._screen = ''
            return True

        # Punctuation/other → commit current buffer, send the char
        self._commit()
        self._send_text(ch)
        return True

    def handle_suggestion_accept(self, index):
        """Accept suggestion at the given index.

        Returns True if a suggestion was accepted, False if none available.
        """
        return self._accept_suggestion(index)

    def handle_clipboard_convert(self, conversion='unicode_to_ansi'):
        """Convert clipboard text between formats.

        Conversion types:
        - 'unicode_to_ansi': Unicode Indic → Baraha ANSI (legacy alias)
        - 'ansi_to_unicode': Baraha ANSI → Unicode Indic (legacy alias)
        - 'unicode_to_baraha': Unicode Indic → Baraha ANSI
        - 'baraha_to_unicode': Baraha ANSI → Unicode Indic
        - 'unicode_to_shreelipi': Unicode Indic → Shreelipi ANSI
        - 'shreelipi_to_unicode': Shreelipi ANSI → Unicode Indic
        - 'baraha_to_shreelipi': Baraha ANSI → Shreelipi ANSI
        - 'shreelipi_to_baraha': Shreelipi ANSI → Baraha ANSI
        - 'auto_to_unicode': Auto-detect encoding, convert to Unicode
        - 'to_roman': Unicode Indic → Roman (reverse transliterate)
        - 'script_to_script': Cross-script conversion (needs from_lang, to_lang)

        Returns True if conversion was performed.
        """
        text = self._get_clipboard_text()
        if not text:
            return False

        # Mapping of conversion aliases to (from_encoding, to_encoding) pairs
        _CONVERSION_MAP = {
            'unicode_to_ansi':      ('unicode',   'baraha'),
            'ansi_to_unicode':      ('baraha',    'unicode'),
            'unicode_to_baraha':    ('unicode',   'baraha'),
            'baraha_to_unicode':    ('baraha',    'unicode'),
            'unicode_to_shreelipi': ('unicode',   'shreelipi'),
            'shreelipi_to_unicode': ('shreelipi', 'unicode'),
            'baraha_to_shreelipi':  ('baraha',    'shreelipi'),
            'shreelipi_to_baraha':  ('shreelipi', 'baraha'),
        }

        try:
            if conversion == 'auto_to_unicode':
                encoding, lang, confidence = self.engine.detect_encoding(text)
                _dbg(f'Auto-detect: encoding={encoding}, lang={lang}, confidence={confidence:.2f}')
                if encoding == 'unicode':
                    # Already Unicode, nothing to do
                    return False
                result = self.engine.convert_encoding(
                    text, from_encoding=encoding, to_encoding='unicode', language=lang
                )
            elif conversion in _CONVERSION_MAP:
                from_enc, to_enc = _CONVERSION_MAP[conversion]
                result = self.engine.convert_encoding(
                    text, from_encoding=from_enc, to_encoding=to_enc
                )
            elif conversion == 'to_roman':
                result = self.engine.reverse_transliterate(text)
            else:
                _dbg(f'Unknown clipboard conversion: {conversion}')
                return False

            self._set_clipboard_text(result)
            _dbg(f'Clipboard converted ({conversion}): {len(text)} → {len(result)} chars')
            return True
        except Exception as e:
            _dbg(f'Clipboard conversion error: {e}')
            return False

    # ============================================================
    # HELPER: transliterate arbitrary text (not buffer)
    # ============================================================

    def _transliterate_buffer_text(self, text):
        """Transliterate arbitrary text using current mode and output settings."""
        if self._input_mode == INPUT_MODE_INSCRIPT:
            result = self.engine.transliterate_inscript(text)
        else:
            result = self.engine.transliterate(text)
        if self._output_mode in (OUTPUT_MODE_BARAHA, OUTPUT_MODE_SHREELIPI):
            result = self.engine.to_ansi(result, font_family=self._ansi_font_family)
        return result

    # ============================================================
    # REVERSE TRANSLITERATION
    # ============================================================

    def reverse_transliterate_text(self, text):
        """Convert Indic script text back to Roman (Baraha scheme)."""
        return self.engine.reverse_transliterate(text)

    # ============================================================
    # CLIPBOARD ACCESS
    # ============================================================

    def _get_clipboard_text(self):
        """Get text from system clipboard.

        Default implementation uses PyQt5. Override for platform-specific.
        """
        try:
            from PyQt5.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                return app.clipboard().text() or ''
        except Exception:
            pass
        return ''

    def _set_clipboard_text(self, text):
        """Set text to system clipboard.

        Default implementation uses PyQt5. Override for platform-specific.
        """
        try:
            from PyQt5.QtWidgets import QApplication
            app = QApplication.instance()
            if app:
                app.clipboard().setText(text)
        except Exception:
            pass

    # ============================================================
    # SUGGESTION ENGINE
    # ============================================================

    def enable_suggestions(self, enabled=True):
        """Enable or disable the suggestion engine at runtime."""
        if enabled and not self._suggestions and HAS_SUGGESTIONS:
            try:
                self._suggestions = SuggestionEngine(min_prefix=3)
                if HAS_POPUP:
                    self._popup = SuggestionPopup()
                    # Init widget on Qt thread if QApplication exists
                    try:
                        from PyQt5.QtWidgets import QApplication
                        if QApplication.instance():
                            self._popup.init_widget()
                            _dbg('Popup widget initialized on enable')
                    except Exception:
                        pass
                # Start async worker thread
                self._suggestion_worker_thread = threading.Thread(
                    target=self._suggestion_worker_loop, daemon=True
                )
                self._suggestion_worker_thread.start()
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
        """Learn a word in a background thread (never blocks hook)."""
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
                item = self._suggestion_queue.get()
                if item is None:
                    return  # shutdown sentinel
                # Drain to latest
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
                if results and self._popup:
                    x, y = self._get_caret_screen_pos()
                    if x is not None:
                        scale = self._get_dpi_scale(x, y)
                        self._popup.show(results, x, y, dpi_scale=scale)
                    else:
                        self._popup.show(results)
                elif self._popup:
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
        try:
            self._suggestion_queue.put_nowait((self._screen, lang_code))
        except Exception:
            pass

    def _accept_suggestion(self, index):
        """Accept suggestion at index. Replace current screen text."""
        if not self._popup or index >= len(self._current_suggestions):
            return False
        word, source = self._current_suggestions[index]
        _dbg(f'ACCEPT suggestion [{index}]: "{word}"')

        # Erase current screen text
        if self._screen:
            self._send_backspaces(len(self._screen))

        # Apply output conversion if ANSI mode
        output_word = word
        if self._output_mode in (OUTPUT_MODE_BARAHA, OUTPUT_MODE_SHREELIPI):
            output_word = self.engine.to_ansi(word, font_family=self._ansi_font_family)

        # Type the suggestion
        self._send_text(output_word)

        # Learn the word
        lang_code = LANG_CODES.get(self.lang, '')
        if lang_code and self._suggestions:
            self._safe_learn(word, lang_code)

        # Reset state
        self._buf = ''
        self._screen = ''
        self._current_suggestions = []
        self._popup.hide()

        # Send space after accepted word
        self._send_text(' ')
        return True

    # ============================================================
    # VIRTUAL METHODS (can be overridden by subclass)
    # ============================================================

    def _get_dpi_scale(self, x, y):
        """Get DPI scale factor for the monitor at (x, y).
        Default: 1.0. Override on Windows for per-monitor DPI.
        """
        return 1.0

    # ============================================================
    # ABSTRACT METHODS — platform MUST implement
    # ============================================================

    @abstractmethod
    def _send_text(self, text):
        """Inject a Unicode string into the focused application.

        On Windows: SendInput with KEYEVENTF_UNICODE
        On macOS: CGEventKeyboardSetUnicodeString + CGEventPost
        """
        ...

    @abstractmethod
    def _send_backspaces(self, count):
        """Inject `count` Backspace key events.

        On Windows: SendInput with VK_BACK
        On macOS: CGEventCreateKeyboardEvent(keycode=51)
        """
        ...

    @abstractmethod
    def _apply_screen_edit(self, erase_count, to_type):
        """Apply a screen edit: erase `erase_count` characters, then type `to_type`.

        On Windows: batched into one atomic SendInput call.
        On macOS: sequential with inter-event delays.
        """
        ...

    @abstractmethod
    def _get_caret_screen_pos(self):
        """Get the caret position in screen coordinates.

        Returns (x, y) tuple, or (None, None) if unavailable.
        Used for positioning the suggestion popup.
        """
        ...

    @abstractmethod
    def start(self):
        """Install the keyboard hook/event tap and prepare for input."""
        ...

    @abstractmethod
    def stop(self):
        """Remove the keyboard hook/event tap and clean up."""
        ...

    @abstractmethod
    def run_event_loop(self):
        """Run the platform event/message loop. Blocks until stopped."""
        ...
