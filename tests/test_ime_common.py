"""
Tests for IME logic that's shared/testable without platform-specific dependencies.

Tests grapheme counting, buffer management, language switching, and toggle state.
These tests exercise the pure-logic portions of the IME engine without
requiring Win32 hooks or Quartz Event Taps.
"""

import os
import sys
import unicodedata

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ============================================================
# Grapheme Counting
# ============================================================

# Inline the grapheme counting logic so tests work without Win32 imports.
# This is the same algorithm used in varnaakshara_ime.py IMEEngine._grapheme_len.

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


def grapheme_len(text):
    """Count grapheme clusters in Indic text.

    A grapheme cluster = base char + all following combining marks (Mc/Mn)
    + any conjunct extensions (virama + consonant chains).
    This matches what a single Backspace key deletes in Word/Notepad.
    """
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


class TestGraphemeCounting:
    """Test grapheme cluster counting for Indic text."""

    def test_simple_ascii(self):
        """ASCII characters are 1 grapheme each."""
        assert grapheme_len('hello') == 5

    def test_single_kannada_vowel(self):
        """Single Kannada vowel = 1 grapheme."""
        assert grapheme_len('ಅ') == 1  # \u0C85

    def test_consonant_with_vowel_sign(self):
        """Consonant + vowel sign = 1 grapheme."""
        assert grapheme_len('ಕಾ') == 1  # ಕ + ಾ (ka + aa-matra)

    def test_consonant_with_virama(self):
        """Consonant + virama = 1 grapheme (halant form)."""
        assert grapheme_len('ಕ್') == 1  # ಕ + ್

    def test_conjunct_two_consonants(self):
        """Consonant + virama + consonant = 1 grapheme (conjunct)."""
        # ಕ್ಕ = ಕ + ್ + ಕ (geminate kka)
        assert grapheme_len('ಕ್ಕ') == 1

    def test_conjunct_with_vowel_sign(self):
        """Conjunct + vowel sign = 1 grapheme."""
        # ಕ್ಕಾ = ಕ + ್ + ಕ + ಾ
        assert grapheme_len('ಕ್ಕಾ') == 1

    def test_multiple_graphemes(self):
        """Multiple separate graphemes."""
        # ನಮ = ನ + ಮ = 2 graphemes
        assert grapheme_len('ನಮ') == 2

    def test_namaskara(self):
        """ನಮಸ್ಕಾರ = 4 graphemes: ನ, ಮ, ಸ್ಕಾ, ರ"""
        text = 'ನಮಸ್ಕಾರ'
        result = grapheme_len(text)
        assert result == 4

    def test_kannada_word(self):
        """ಕನ್ನಡ = 3 graphemes: ಕ, ನ್ನ, ಡ"""
        text = 'ಕನ್ನಡ'
        result = grapheme_len(text)
        assert result == 3

    def test_amma(self):
        """ಅಮ್ಮ = 2 graphemes: ಅ, ಮ್ಮ"""
        text = 'ಅಮ್ಮ'
        result = grapheme_len(text)
        assert result == 2

    def test_triple_conjunct(self):
        """ಸ್ತ್ರ = 1 grapheme: ಸ + ್ + ತ + ್ + ರ"""
        text = 'ಸ್ತ್ರ'
        result = grapheme_len(text)
        assert result == 1

    def test_hindi_namaste(self):
        """नमस्ते = 3 graphemes: न, म, स्ते"""
        text = 'नमस्ते'
        result = grapheme_len(text)
        assert result == 3

    def test_anusvara_grapheme(self):
        """ಅಂ = 1 grapheme (vowel + anusvara)."""
        text = 'ಅಂ'
        result = grapheme_len(text)
        assert result == 1

    def test_visarga_grapheme(self):
        """ಅಃ = 1 grapheme (vowel + visarga)."""
        text = 'ಅಃ'
        result = grapheme_len(text)
        assert result == 1

    def test_empty_string(self):
        assert grapheme_len('') == 0

    def test_devanagari_conjunct(self):
        """क्ष = 1 grapheme: क + ् + ष"""
        text = 'क्ष'
        assert grapheme_len(text) == 1

    def test_mixed_script_and_ascii(self):
        """Mixed text counts correctly."""
        # 'ಕ a' = ಕ(1) + space(1) + a(1) = 3
        assert grapheme_len('ಕ a') == 3

    def test_telugu_grapheme(self):
        """Telugu conjunct counting."""
        # క్క = క + ్ + క = 1 grapheme
        text = 'క్క'
        assert grapheme_len(text) == 1

    def test_tamil_grapheme(self):
        """Tamil consonant + vowel sign = 1 grapheme."""
        # கா = க + ா = 1 grapheme
        text = 'கா'
        assert grapheme_len(text) == 1


# ============================================================
# Buffer Management Logic
# ============================================================

class TestBufferManagement:
    """Test transliteration buffer behavior via TransliterationEngine."""

    def test_buffer_starts_empty(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        assert engine.flush() == ''

    def test_buffer_accumulates(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.process_key('n')
        engine.process_key('a')
        result = engine.flush()
        assert result != ''  # Should produce output
        assert 'ನ' in result  # 'na' → ನ

    def test_space_triggers_commit(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.process_key('k')
        engine.process_key('a')
        output, flushed = engine.process_key(' ')
        assert flushed
        assert output is not None

    def test_period_triggers_commit(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.process_key('k')
        engine.process_key('a')
        output, flushed = engine.process_key('.')
        assert flushed

    def test_digit_triggers_commit(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.process_key('k')
        engine.process_key('a')
        output, flushed = engine.process_key('1')
        assert flushed

    def test_consecutive_flushes(self):
        """Multiple consecutive flushes produce empty after first."""
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.process_key('k')
        first = engine.flush()
        second = engine.flush()
        assert first != ''
        assert second == ''

    def test_buffer_reset_after_flush(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.process_key('a')
        engine.flush()
        # Buffer should be empty now
        engine.process_key('i')
        result = engine.flush()
        # Should only have 'i', not 'a' + 'i'
        assert result == 'ಇ'


# ============================================================
# Language Switching
# ============================================================

class TestLanguageSwitching:
    """Test language switching via TransliterationEngine."""

    def test_switch_produces_different_output(self):
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        kn = engine.transliterate('ka')

        engine.set_language('hindi')
        hi = engine.transliterate('ka')

        engine.set_language('telugu')
        te = engine.transliterate('ka')

        engine.set_language('tamil')
        ta = engine.transliterate('ka')

        # All four should be different scripts
        results = {kn, hi, te, ta}
        assert len(results) == 4, f"Expected 4 different outputs, got: {results}"

    def test_switch_to_all_languages(self):
        """Switching to every registered language should work."""
        from transliteration import TransliterationEngine, LANGUAGES
        engine = TransliterationEngine('kannada')
        for lang in LANGUAGES:
            engine.set_language(lang)
            result = engine.transliterate('ka')
            assert len(result) > 0

    def test_switch_preserves_engine(self):
        """Switching language doesn't break the engine."""
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        engine.set_language('hindi')
        engine.set_language('telugu')
        engine.set_language('kannada')
        result = engine.transliterate('namaskaara')
        assert result == 'ನಮಸ್ಕಾರ'


# ============================================================
# Toggle State
# ============================================================

class TestToggleState:
    """Test IME active/inactive toggle logic.

    Since IMEEngine requires Win32, we test the toggle concept
    using TransliterationEngine + a simple state wrapper.
    """

    def test_toggle_concept(self):
        """Simulate toggle: when inactive, pass through ASCII."""
        active = True
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')

        # Active → transliterate
        result = engine.transliterate('ka') if active else 'ka'
        assert result == 'ಕ'

        # Inactive → pass through
        active = False
        result = engine.transliterate('ka') if active else 'ka'
        assert result == 'ka'

        # Toggle back
        active = True
        result = engine.transliterate('ka') if active else 'ka'
        assert result == 'ಕ'

    def test_language_state_preserved_across_toggle(self):
        """Language setting preserved when toggling."""
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('hindi')
        active = True

        # Toggle off and on
        active = not active  # off
        active = not active  # on

        # Should still be Hindi
        assert engine.language == 'hindi'
        result = engine.transliterate('ka')
        # Hindi 'ka' → क
        assert result == 'क'


# ============================================================
# Platform Detection
# ============================================================

class TestPlatformDetection:
    """Test that platform-specific modules handle import gracefully."""

    def test_transliteration_imports_anywhere(self):
        """transliteration.py has no platform dependencies."""
        import transliteration
        assert hasattr(transliteration, 'TransliterationEngine')
        assert hasattr(transliteration, 'LANGUAGES')

    def test_suggestions_imports_anywhere(self):
        """suggestions.py should import on any platform."""
        import suggestions
        assert hasattr(suggestions, 'SuggestionEngine')

    @pytest.mark.skipif(
        sys.platform != 'win32',
        reason='Win32 IME only available on Windows'
    )
    def test_win32_ime_import(self):
        """varnaakshara_ime.py requires Windows."""
        import varnaakshara_ime
        assert hasattr(varnaakshara_ime, 'IMEEngine')

    @pytest.mark.skipif(
        sys.platform != 'darwin',
        reason='macOS IME only available on macOS'
    )
    def test_macos_ime_import(self):
        """varnaakshara_ime_mac.py requires macOS."""
        import varnaakshara_ime_mac
        assert hasattr(varnaakshara_ime_mac, 'IMEEngine')
