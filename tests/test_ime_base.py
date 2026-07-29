"""
Tests for VarnaaksharaIMEBase.

Tests the shared logic: buffer management, transliteration routing,
mode switching, output conversion, suggestion integration, and
key handling methods — all without requiring platform-specific
keyboard hooks or OS APIs.

Uses a concrete StubIME subclass that records calls to abstract methods
instead of performing real keyboard injection.
"""

import sys
import os
import unittest

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ime.ime_base import (
    VarnaaksharaIMEBase,
    LANGUAGES,
    SUPPORTED_LANGUAGES,
    INPUT_MODE_PHONETIC_BARAHA,
    INPUT_MODE_PHONETIC_ITRANS,
    INPUT_MODE_INSCRIPT,
    OUTPUT_MODE_UNICODE,
    OUTPUT_MODE_ANSI,
    grapheme_len,
    _dbg,
)


# ============================================================
# Stub IME for testing — records all abstract method calls
# ============================================================

class StubIME(VarnaaksharaIMEBase):
    """Concrete test double that records text injection calls."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sent_text = []           # list of strings sent
        self.sent_backspaces = []     # list of counts
        self.screen_edits = []        # list of (erase_count, to_type) tuples
        self.active = True            # active by default for tests

    def _send_text(self, text):
        self.sent_text.append(text)

    def _send_backspaces(self, count):
        self.sent_backspaces.append(count)

    def _apply_screen_edit(self, erase_count, to_type):
        self.screen_edits.append((erase_count, to_type))

    def _get_caret_screen_pos(self):
        return (100, 200)

    def start(self):
        pass

    def stop(self):
        pass

    def run_event_loop(self):
        pass


# ============================================================
# Tests
# ============================================================

class TestLanguages(unittest.TestCase):
    """Test language registry."""

    def test_supported_languages_has_12(self):
        self.assertEqual(len(SUPPORTED_LANGUAGES), 12)

    def test_all_languages_have_name_and_code(self):
        for key, lang in SUPPORTED_LANGUAGES.items():
            self.assertIn('name', lang, f'{key} missing name')
            self.assertIn('code', lang, f'{key} missing code')

    def test_languages_alias(self):
        """LANGUAGES should be the same as SUPPORTED_LANGUAGES."""
        self.assertIs(LANGUAGES, SUPPORTED_LANGUAGES)


class TestIMEInit(unittest.TestCase):
    """Test IME initialization."""

    def test_default_init(self):
        ime = StubIME()
        self.assertEqual(ime.lang, 'kannada')
        self.assertEqual(ime.scheme, 'baraha')
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_BARAHA)
        self.assertEqual(ime._output_mode, OUTPUT_MODE_UNICODE)
        self.assertEqual(ime._buf, '')
        self.assertEqual(ime._screen, '')
        self.assertTrue(ime.active)  # StubIME sets True

    def test_custom_language_init(self):
        ime = StubIME(language='hindi', scheme='itrans')
        self.assertEqual(ime.lang, 'hindi')
        self.assertEqual(ime.scheme, 'itrans')
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_ITRANS)

    def test_invalid_language_raises(self):
        with self.assertRaises(ValueError):
            StubIME(language='klingon')


class TestLanguageSwitch(unittest.TestCase):
    """Test language switching."""

    def test_set_language(self):
        ime = StubIME()
        ime.set_language('hindi')
        self.assertEqual(ime.lang, 'hindi')
        self.assertTrue(ime.active)

    def test_set_language_commits_buffer(self):
        ime = StubIME()
        ime._buf = 'hello'
        ime._screen = 'ಹೆಲ್ಲೋ'
        ime.set_language('telugu')
        self.assertEqual(ime._buf, '')
        self.assertEqual(ime._screen, '')

    def test_set_unknown_language_ignored(self):
        ime = StubIME()
        ime.set_language('unknown')
        self.assertEqual(ime.lang, 'kannada')  # unchanged


class TestInputMode(unittest.TestCase):
    """Test input mode switching."""

    def test_set_phonetic_baraha(self):
        ime = StubIME()
        ime.set_input_mode(INPUT_MODE_PHONETIC_BARAHA)
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_BARAHA)
        self.assertEqual(ime.scheme, 'baraha')

    def test_set_phonetic_itrans(self):
        ime = StubIME()
        ime.set_input_mode(INPUT_MODE_PHONETIC_ITRANS)
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_ITRANS)
        self.assertEqual(ime.scheme, 'itrans')

    def test_set_inscript(self):
        ime = StubIME()
        ime.set_input_mode(INPUT_MODE_INSCRIPT)
        self.assertEqual(ime._input_mode, INPUT_MODE_INSCRIPT)

    def test_invalid_mode_ignored(self):
        ime = StubIME()
        ime.set_input_mode('invalid')
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_BARAHA)

    def test_mode_switch_commits_buffer(self):
        ime = StubIME()
        ime._buf = 'test'
        ime.set_input_mode(INPUT_MODE_PHONETIC_ITRANS)
        self.assertEqual(ime._buf, '')


class TestOutputMode(unittest.TestCase):
    """Test output mode switching."""

    def test_set_unicode(self):
        ime = StubIME()
        ime.set_output_mode(OUTPUT_MODE_UNICODE)
        self.assertEqual(ime._output_mode, OUTPUT_MODE_UNICODE)

    def test_set_ansi(self):
        ime = StubIME()
        ime.set_output_mode(OUTPUT_MODE_ANSI, font_family='shree')
        self.assertEqual(ime._output_mode, OUTPUT_MODE_ANSI)
        self.assertEqual(ime._ansi_font_family, 'shree')

    def test_invalid_mode_ignored(self):
        ime = StubIME()
        ime.set_output_mode('invalid')
        self.assertEqual(ime._output_mode, OUTPUT_MODE_UNICODE)


class TestToggle(unittest.TestCase):
    """Test IME toggle."""

    def test_toggle_off(self):
        ime = StubIME()
        self.assertTrue(ime.active)
        ime.toggle()
        self.assertFalse(ime.active)

    def test_toggle_on(self):
        ime = StubIME()
        ime.active = False
        ime.toggle()
        self.assertTrue(ime.active)

    def test_toggle_commits_buffer(self):
        ime = StubIME()
        ime._buf = 'test'
        ime.toggle()
        self.assertEqual(ime._buf, '')


class TestBufferManagement(unittest.TestCase):
    """Test buffer and screen text management."""

    def test_commit_resets_buffer(self):
        ime = StubIME()
        ime._buf = 'namas'
        ime._screen = 'ನಮಸ್'
        ime._commit()
        self.assertEqual(ime._buf, '')
        self.assertEqual(ime._screen, '')

    def test_update_calls_apply_screen_edit(self):
        ime = StubIME()
        ime._buf = 'na'
        ime._update()
        self.assertTrue(len(ime.screen_edits) > 0)
        self.assertNotEqual(ime._screen, '')

    def test_update_with_no_buffer(self):
        ime = StubIME()
        ime._update()
        self.assertEqual(len(ime.screen_edits), 0)

    def test_transliterate_buffer_baraha(self):
        ime = StubIME(language='kannada')
        ime._buf = 'na'
        result = ime._transliterate_buffer()
        self.assertEqual(result, 'ನ')  # na → ನ (with virama removed since 'a' is explicit)

    def test_transliterate_buffer_ansi(self):
        ime = StubIME(language='kannada')
        ime._buf = 'ka'
        ime._output_mode = OUTPUT_MODE_ANSI
        result = ime._transliterate_buffer()
        # ANSI output should be different from Unicode
        # For kannada 'ka' → ಕ → ANSI 'k' (from the ANSI map)
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)


class TestKeyHandling(unittest.TestCase):
    """Test key handling methods."""

    def test_handle_toggle(self):
        ime = StubIME()
        result = ime.handle_toggle()
        self.assertTrue(result)
        self.assertFalse(ime.active)

    def test_handle_english_mode(self):
        ime = StubIME()
        result = ime.handle_english_mode()
        self.assertTrue(result)
        self.assertFalse(ime.active)

    def test_handle_language_switch(self):
        ime = StubIME()
        result = ime.handle_language_switch('hindi')
        self.assertTrue(result)
        self.assertEqual(ime.lang, 'hindi')

    def test_handle_language_switch_invalid(self):
        ime = StubIME()
        result = ime.handle_language_switch('unknown')
        self.assertFalse(result)
        self.assertEqual(ime.lang, 'kannada')

    def test_handle_backspace_with_buffer(self):
        ime = StubIME()
        ime._buf = 'na'
        ime._screen = 'ನ'
        result = ime.handle_backspace()
        self.assertTrue(result)  # consumed
        self.assertEqual(ime._buf, 'n')

    def test_handle_backspace_empty_buffer(self):
        ime = StubIME()
        result = ime.handle_backspace()
        self.assertFalse(result)  # pass through

    def test_handle_backspace_clears_screen(self):
        ime = StubIME()
        ime._buf = 'n'
        ime._screen = 'ನ್'
        result = ime.handle_backspace()
        self.assertTrue(result)
        self.assertEqual(ime._buf, '')
        self.assertEqual(ime._screen, '')
        # Should have sent backspaces
        self.assertTrue(len(ime.sent_backspaces) > 0)

    def test_handle_space(self):
        ime = StubIME()
        ime._buf = 'test'
        result = ime.handle_space()
        self.assertTrue(result)
        self.assertEqual(ime._buf, '')
        # Should have sent a space
        self.assertIn(' ', ime.sent_text)

    def test_handle_enter(self):
        ime = StubIME()
        ime._buf = 'test'
        result = ime.handle_enter()
        self.assertFalse(result)  # pass through
        self.assertEqual(ime._buf, '')  # but buffer committed

    def test_handle_nav(self):
        ime = StubIME()
        ime._buf = 'test'
        result = ime.handle_nav()
        self.assertFalse(result)  # pass through
        self.assertEqual(ime._buf, '')

    def test_handle_char_alpha(self):
        ime = StubIME()
        result = ime.handle_char('n')
        self.assertTrue(result)
        self.assertEqual(ime._buf, 'n')

    def test_handle_char_builds_buffer(self):
        ime = StubIME()
        ime.handle_char('n')
        ime.handle_char('a')
        ime.handle_char('m')
        self.assertEqual(ime._buf, 'nam')

    def test_handle_char_digit(self):
        ime = StubIME()
        result = ime.handle_char('5')
        self.assertTrue(result)
        # Should have sent the native numeral
        self.assertTrue(len(ime.sent_text) > 0)

    def test_handle_char_punctuation_commits(self):
        ime = StubIME()
        ime._buf = 'test'
        ime._screen = 'ತೆಸ್ತ್'
        result = ime.handle_char(',')
        self.assertTrue(result)
        self.assertEqual(ime._buf, '')
        # Should have sent the comma
        self.assertIn(',', ime.sent_text)

    def test_handle_char_inactive_ime(self):
        ime = StubIME()
        ime.active = False
        result = ime.handle_char('n')
        self.assertFalse(result)

    def test_handle_char_tilde(self):
        ime = StubIME()
        result = ime.handle_char('~')
        self.assertTrue(result)
        self.assertEqual(ime._buf, '~')

    def test_handle_char_baraha_symbols(self):
        """Baraha symbols &, |, #, $ should go through transliteration."""
        ime = StubIME()
        for ch in '&|#$':
            ime._buf = ''
            result = ime.handle_char(ch)
            self.assertTrue(result, f'char {ch!r} should be handled')

    def test_handle_ctrl_combo(self):
        ime = StubIME()
        ime._buf = 'test'
        result = ime.handle_ctrl_combo()
        self.assertFalse(result)  # pass through
        self.assertEqual(ime._buf, '')  # committed


class TestTransliteration(unittest.TestCase):
    """Test end-to-end transliteration through the IME."""

    def test_kannada_word(self):
        ime = StubIME(language='kannada')
        for ch in 'namaskaara':
            ime.handle_char(ch)
        result = ime._screen
        self.assertEqual(result, 'ನಮಸ್ಕಾರ')

    def test_hindi_word(self):
        ime = StubIME(language='hindi')
        for ch in 'namaste':
            ime.handle_char(ch)
        result = ime._screen
        self.assertEqual(result, 'नमस्ते')

    def test_telugu_word(self):
        ime = StubIME(language='telugu')
        for ch in 'telugu':
            ime.handle_char(ch)
        result = ime._screen
        self.assertEqual(result, 'తెలుగు')


class TestReverseTransliteration(unittest.TestCase):
    """Test reverse transliteration."""

    def test_reverse_kannada(self):
        ime = StubIME(language='kannada')
        result = ime.reverse_transliterate_text('ನಮಸ್ಕಾರ')
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
        # Should contain romanized text
        self.assertTrue(result.isascii())


class TestClipboardConversion(unittest.TestCase):
    """Test clipboard conversion (mock clipboard)."""

    def test_convert_clipboard_no_text(self):
        ime = StubIME()
        result = ime.handle_clipboard_convert('unicode_to_ansi')
        self.assertFalse(result)  # no clipboard text


class TestStateCallback(unittest.TestCase):
    """Test state change notifications."""

    def test_callback_on_toggle(self):
        ime = StubIME()
        calls = []
        ime.set_state_callback(lambda l, a: calls.append((l, a)))
        ime.toggle()
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], ('kannada', False))

    def test_callback_on_language_switch(self):
        ime = StubIME()
        calls = []
        ime.set_state_callback(lambda l, a: calls.append((l, a)))
        ime.set_language('hindi')
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], ('hindi', True))


class TestGraphemeLen(unittest.TestCase):
    """Test grapheme cluster counting."""

    def test_ascii(self):
        self.assertEqual(grapheme_len('hello'), 5)

    def test_simple_indic(self):
        # ನ (single grapheme)
        self.assertEqual(grapheme_len('ನ'), 1)

    def test_consonant_vowel_sign(self):
        # ನಾ = ನ + ಾ (one grapheme)
        self.assertEqual(grapheme_len('ನಾ'), 1)

    def test_conjunct(self):
        # ಸ್ಕ = ಸ + ್ + ಕ (one grapheme cluster with virama conjunct)
        self.assertEqual(grapheme_len('ಸ್ಕ'), 1)

    def test_multiple_graphemes(self):
        # ನಮ = two graphemes
        self.assertEqual(grapheme_len('ನಮ'), 2)


class TestSuggestionToggle(unittest.TestCase):
    """Test suggestion enable/disable."""

    def test_disable_suggestions(self):
        ime = StubIME()
        ime.enable_suggestions(False)
        self.assertFalse(ime._suggestions_enabled)

    def test_accept_suggestion_no_popup(self):
        ime = StubIME()
        result = ime.handle_suggestion_accept(0)
        self.assertFalse(result)


class TestSchemeSwitch(unittest.TestCase):
    """Test scheme switching."""

    def test_switch_to_itrans(self):
        ime = StubIME()
        ime.set_scheme('itrans')
        self.assertEqual(ime.scheme, 'itrans')
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_ITRANS)

    def test_switch_to_baraha(self):
        ime = StubIME(scheme='itrans')
        ime.set_scheme('baraha')
        self.assertEqual(ime.scheme, 'baraha')
        self.assertEqual(ime._input_mode, INPUT_MODE_PHONETIC_BARAHA)

    def test_switch_commits_buffer(self):
        ime = StubIME()
        ime._buf = 'hello'
        ime.set_scheme('itrans')
        self.assertEqual(ime._buf, '')


class TestCustomMappings(unittest.TestCase):
    """Test custom mapping support."""

    def test_set_custom_mappings(self):
        ime = StubIME()
        cm = {'consonants': {'q': '\u0958'}}
        ime.set_custom_mappings(cm)
        # Should not crash; engine applies mappings internally


class TestImport(unittest.TestCase):
    """Test that the ime package is importable."""

    def test_import_base(self):
        from ime.ime_base import VarnaaksharaIMEBase
        self.assertTrue(hasattr(VarnaaksharaIMEBase, 'handle_char'))

    def test_import_package(self):
        from ime import VarnaaksharaIMEBase
        self.assertTrue(hasattr(VarnaaksharaIMEBase, '_commit'))

    def test_import_languages(self):
        from ime.ime_base import LANGUAGES, SUPPORTED_LANGUAGES
        self.assertIn('kannada', LANGUAGES)
        self.assertEqual(LANGUAGES, SUPPORTED_LANGUAGES)


if __name__ == '__main__':
    unittest.main()
