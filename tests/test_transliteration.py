"""
Comprehensive tests for Varnaakshara transliteration engine.

Tests the Baraha-scheme transliteration for Kannada, Hindi, Telugu, and Tamil.
Covers vowels, consonants, conjuncts, matras, yogavaahas, edge cases,
case sensitivity, word-level transliteration, and the TransliterationEngine API.

70+ test cases organized by category.
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from transliteration import (
    TransliterationEngine,
    LANGUAGES,
    BARAHA_VOWELS,
    BARAHA_CONSONANTS,
    BARAHA_VOWEL_SIGNS,
    BARAHA_YOGAVAAHAS,
    BARAHA_DIGITS,
    BARAHA_SYMBOLS,
    DEVANAGARI_VIRAMA,
    convert_to_ansi,
)


# ============================================================
# TransliterationEngine API Tests
# ============================================================

class TestTransliterationEngineAPI:
    """Test the TransliterationEngine class interface."""

    def test_default_language_is_kannada(self):
        engine = TransliterationEngine()
        assert engine.language == 'kannada'

    def test_set_language_valid(self):
        engine = TransliterationEngine('kannada')
        engine.set_language('hindi')
        assert engine.language == 'hindi'

    def test_set_language_invalid(self):
        engine = TransliterationEngine()
        with pytest.raises(ValueError, match='Unsupported language'):
            engine.set_language('klingon')

    def test_all_registered_languages(self):
        """Every language in LANGUAGES should be constructible."""
        for lang in LANGUAGES:
            engine = TransliterationEngine(lang)
            assert engine.language == lang

    def test_transliterate_returns_string(self):
        engine = TransliterationEngine('kannada')
        result = engine.transliterate('namaste')
        assert isinstance(result, str)

    def test_transliterate_empty_string(self):
        engine = TransliterationEngine('kannada')
        assert engine.transliterate('') == ''

    def test_process_key_and_flush(self):
        """Test incremental key processing with buffer flush."""
        engine = TransliterationEngine('kannada')
        # Process individual characters
        out, flushed = engine.process_key('k')
        assert not flushed  # not yet flushed, waiting for more input

        out, flushed = engine.process_key('a')
        assert not flushed

        # Space triggers flush
        out, flushed = engine.process_key(' ')
        assert flushed
        assert out is not None
        assert 'ಕ' in out  # 'ka ' should contain ಕ

    def test_flush_explicit(self):
        engine = TransliterationEngine('kannada')
        engine.process_key('n')
        engine.process_key('a')
        result = engine.flush()
        assert result  # should produce transliterated output
        # Second flush should be empty
        assert engine.flush() == ''

    def test_language_switch_mid_use(self):
        engine = TransliterationEngine('kannada')
        kn_result = engine.transliterate('ka')
        engine.set_language('hindi')
        hi_result = engine.transliterate('ka')
        assert kn_result != hi_result  # different scripts

    def test_passthrough_ascii_symbols(self):
        """Non-Baraha characters pass through unchanged.
        Note: # and $ are now Vedic swaras, not passthrough."""
        engine = TransliterationEngine('kannada')
        assert engine.transliterate('@%') == '@%'


# ============================================================
# Kannada Transliteration Tests
# ============================================================

class TestKannadaVowels:
    """Test standalone vowels in Kannada."""

    @pytest.mark.parametrize("baraha,expected", [
        ('a', 'ಅ'),      # short a
        ('A', 'ಆ'),      # long a
        ('aa', 'ಆ'),     # long a (alias)
        ('i', 'ಇ'),      # short i
        ('I', 'ಈ'),      # long i
        ('u', 'ಉ'),      # short u
        ('U', 'ಊ'),      # long u
        ('e', 'ಎ'),      # short e
        ('E', 'ಏ'),      # long e
        ('ai', 'ಐ'),     # ai diphthong
        ('o', 'ಒ'),      # short o
        ('O', 'ಓ'),      # long o
        ('au', 'ಔ'),     # au diphthong
        ('Ru', 'ಋ'),     # vocalic r
    ])
    def test_standalone_vowels(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected


class TestKannadaConsonants:
    """Test consonants with inherent 'a' vowel in Kannada."""

    @pytest.mark.parametrize("baraha,expected", [
        ('ka', 'ಕ'),       # ka
        ('kha', 'ಖ'),      # kha
        ('ga', 'ಗ'),       # ga
        ('gha', 'ಘ'),      # gha
        ('cha', 'ಚ'),      # cha
        ('ja', 'ಜ'),       # ja
        ('Ta', 'ಟ'),       # retroflex Ta
        ('Da', 'ಡ'),       # retroflex Da
        ('Na', 'ಣ'),       # retroflex Na
        ('ta', 'ತ'),       # dental ta
        ('da', 'ದ'),       # dental da
        ('na', 'ನ'),       # dental na
        ('pa', 'ಪ'),       # pa
        ('ba', 'ಬ'),       # ba
        ('ma', 'ಮ'),       # ma
        ('ya', 'ಯ'),       # ya
        ('ra', 'ರ'),       # ra
        ('la', 'ಲ'),       # la
        ('va', 'ವ'),       # va
        ('sha', 'ಶ'),      # sha
        ('Sha', 'ಷ'),      # Sha (retroflex)
        ('sa', 'ಸ'),       # sa
        ('ha', 'ಹ'),       # ha
        ('La', 'ಳ'),       # La (retroflex lateral)
    ])
    def test_consonants_with_a(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected


class TestKannadaMatras:
    """Test vowel signs (matras) after consonants."""

    @pytest.mark.parametrize("baraha,expected", [
        ('kA', 'ಕಾ'),     # ka + aa matra
        ('ki', 'ಕಿ'),     # ka + i matra
        ('kI', 'ಕೀ'),     # ka + ii matra
        ('ku', 'ಕು'),     # ka + u matra
        ('kU', 'ಕೂ'),     # ka + uu matra
        ('ke', 'ಕೆ'),     # ka + e matra
        ('kE', 'ಕೇ'),     # ka + ee matra
        ('kai', 'ಕೈ'),    # ka + ai matra
        ('ko', 'ಕೊ'),     # ka + o matra
        ('kO', 'ಕೋ'),     # ka + oo matra
        ('kau', 'ಕೌ'),    # ka + au matra
        ('kRu', 'ಕೃ'),    # ka + Ru matra
    ])
    def test_vowel_signs(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected


class TestKannadaConjuncts:
    """Test consonant clusters (virama + consonant conjuncts)."""

    @pytest.mark.parametrize("baraha,expected", [
        ('kka', 'ಕ್ಕ'),       # geminate kk
        ('nna', 'ನ್ನ'),       # geminate nn
        ('mma', 'ಮ್ಮ'),       # geminate mm
        ('sta', 'ಸ್ತ'),       # s + t cluster
        ('stra', 'ಸ್ತ್ರ'),     # s + t + r triple cluster
        ('ksha', 'ಕ್ಶ'),      # ksh cluster (k+virama+sh)
        ('nda', 'ನ್ದ'),       # nd cluster
        ('ndha', 'ನ್ಧ'),      # ndh cluster
    ])
    def test_conjuncts(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected


class TestKannadaSpecialConjuncts:
    """Test special pre-combined conjunct tokens."""

    def test_ksha_conjunct(self, kannada_engine):
        # kSh is a special token → क्ष → ಕ್ಷ
        assert kannada_engine.transliterate('kSha') == 'ಕ್ಷ'

    def test_jna_conjunct(self, kannada_engine):
        # j~j is a special token → ज्ञ → ಜ್ಞ
        assert kannada_engine.transliterate('j~ja') == 'ಜ್ಞ'


class TestKannadaYogavaahas:
    """Test anusvara, visarga, and chandrabindu."""

    def test_anusvara(self, kannada_engine):
        assert kannada_engine.transliterate('aM') == 'ಅಂ'

    def test_visarga(self, kannada_engine):
        assert kannada_engine.transliterate('aH') == 'ಅಃ'

    def test_chandrabindu(self, kannada_engine):
        assert kannada_engine.transliterate('a~M') == 'ಅಁ'

    def test_anusvara_after_consonant(self, kannada_engine):
        # rAmaM → ರಾಮಂ
        assert kannada_engine.transliterate('rAmaM') == 'ರಾಮಂ'

    def test_visarga_after_consonant(self, kannada_engine):
        # duHkha → ದುಃಖ
        assert kannada_engine.transliterate('duHkha') == 'ದುಃಖ'


class TestKannadaCaseSensitivity:
    """Test Baraha case-sensitivity: T vs t, D vs d, etc."""

    def test_T_vs_t(self, kannada_engine):
        # T = retroflex ट → ಟ, t = dental त → ತ
        T_result = kannada_engine.transliterate('Ta')
        t_result = kannada_engine.transliterate('ta')
        assert T_result == 'ಟ'
        assert t_result == 'ತ'
        assert T_result != t_result

    def test_D_vs_d(self, kannada_engine):
        # D = retroflex ड → ಡ, d = dental द → ದ
        D_result = kannada_engine.transliterate('Da')
        d_result = kannada_engine.transliterate('da')
        assert D_result == 'ಡ'
        assert d_result == 'ದ'
        assert D_result != d_result

    def test_N_vs_n(self, kannada_engine):
        # N = retroflex ण → ಣ, n = dental न → ನ
        N_result = kannada_engine.transliterate('Na')
        n_result = kannada_engine.transliterate('na')
        assert N_result == 'ಣ'
        assert n_result == 'ನ'
        assert N_result != n_result

    def test_S_vs_s(self, kannada_engine):
        # S = palatal श → ಶ, s = dental स → ಸ
        S_result = kannada_engine.transliterate('Sa')
        s_result = kannada_engine.transliterate('sa')
        assert S_result == 'ಶ'
        assert s_result == 'ಸ'
        assert S_result != s_result

    def test_K_vs_k(self, kannada_engine):
        # K = ख → ಖ, k = क → ಕ
        K_result = kannada_engine.transliterate('Ka')
        k_result = kannada_engine.transliterate('ka')
        assert K_result == 'ಖ'
        assert k_result == 'ಕ'

    def test_G_vs_g(self, kannada_engine):
        # G = घ → ಘ, g = ग → ಗ
        G_result = kannada_engine.transliterate('Ga')
        g_result = kannada_engine.transliterate('ga')
        assert G_result == 'ಘ'
        assert g_result == 'ಗ'


class TestKannadaWords:
    """Test full word-level transliteration in Kannada."""

    @pytest.mark.parametrize("baraha,expected", [
        ('nAnu', 'ನಾನು'),
        ('namaskaara', 'ನಮಸ್ಕಾರ'),
        ('namaskAra', 'ನಮಸ್ಕಾರ'),
        ('kannaDa', 'ಕನ್ನಡ'),
        ('amma', 'ಅಮ್ಮ'),
        ('beMgaLUru', 'ಬೆಂಗಳೂರು'),
        ('vishva', 'ವಿಶ್ವ'),
        ('oMdu', 'ಒಂದು'),
        ('nInu', 'ನೀನು'),
        ('shAlE', 'ಶಾಲೇ'),
        ('aidu', 'ಐದು'),
        ('hAgU', 'ಹಾಗೂ'),
        ('RuShigaLu', 'ಋಷಿಗಳು'),
        ('kRuShNa', 'ಕೃಷ್ಣ'),
        ('praj~jA', 'ಪ್ರಜ್ಞಾ'),
    ])
    def test_kannada_words(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected

    def test_complex_word(self, kannada_engine):
        """Long complex word with multiple conjuncts."""
        result = kannada_engine.transliterate('sha~gkaraacaaryaru')
        assert result == 'ಶಙ್ಕರಾಚಾರ್ಯರು'

    def test_words_with_space(self, kannada_engine):
        result = kannada_engine.transliterate('rAma sItA')
        assert result == 'ರಾಮ ಸೀತಾ'

    def test_word_boundary_virama(self, kannada_engine):
        """Final consonant without vowel gets virama."""
        result = kannada_engine.transliterate('ram')
        assert result == 'ರಮ್'

    def test_explicit_a_no_virama(self, kannada_engine):
        """Explicit 'a' at end = inherent vowel, no virama."""
        result = kannada_engine.transliterate('rama')
        assert result == 'ರಮ'

    def test_punctuation_preserved(self, kannada_engine):
        result = kannada_engine.transliterate('namO namaste!')
        assert result.endswith('!')


# ============================================================
# Hindi (Devanagari) Tests
# ============================================================

class TestHindiTransliteration:
    """Test Hindi transliteration (Devanagari output)."""

    @pytest.mark.parametrize("baraha,expected", [
        ('namaste', 'नमस्ते'),
        ('hindii', 'हिन्दी'),
        ('hindI', 'हिन्दी'),
        ('duniyaa', 'दुनिया'),
        ('kRuShNa', 'कृष्ण'),
        ('rAma', 'राम'),
    ])
    def test_hindi_words(self, hindi_engine, baraha, expected):
        assert hindi_engine.transliterate(baraha) == expected

    def test_hindi_final_virama(self, hindi_engine):
        """Hindi has implicit schwa — final consonant keeps inherent 'a', no virama."""
        result = hindi_engine.transliterate('bhaarat')
        assert result == 'भारत'

    def test_hindi_no_short_e_o(self, hindi_engine):
        """Hindi maps short e/o to long e/o."""
        # 'e' in standalone position should produce long ए in Hindi
        result = hindi_engine.transliterate('e')
        # Hindi's script_map maps short-e devanagari → long-e devanagari
        assert result == 'ए'

    def test_hindi_vowel_standalone(self, hindi_engine):
        assert hindi_engine.transliterate('a') == 'अ'
        assert hindi_engine.transliterate('i') == 'इ'
        assert hindi_engine.transliterate('u') == 'उ'

    def test_hindi_conjuncts(self, hindi_engine):
        assert hindi_engine.transliterate('strii') == 'स्त्री'


# ============================================================
# Telugu Tests
# ============================================================

class TestTeluguTransliteration:
    """Test Telugu transliteration."""

    @pytest.mark.parametrize("baraha,expected", [
        ('namaskaaraM', 'నమస్కారం'),
        ('telugu', 'తెలుగు'),
    ])
    def test_telugu_words(self, telugu_engine, baraha, expected):
        assert telugu_engine.transliterate(baraha) == expected

    def test_telugu_vowel(self, telugu_engine):
        assert telugu_engine.transliterate('a') == 'అ'

    def test_telugu_consonant(self, telugu_engine):
        assert telugu_engine.transliterate('ka') == 'క'

    def test_telugu_anusvara(self, telugu_engine):
        result = telugu_engine.transliterate('aM')
        assert result == 'అం'


# ============================================================
# Tamil Tests
# ============================================================

class TestTamilTransliteration:
    """Test Tamil transliteration — note Tamil merges many consonants."""

    def test_vanakkam(self, tamil_engine):
        result = tamil_engine.transliterate('vanakkam')
        assert result == 'வநக்கம்'

    def test_tamil_vowel(self, tamil_engine):
        assert tamil_engine.transliterate('a') == 'அ'

    def test_tamil_consonant_merge(self, tamil_engine):
        """Tamil merges ka-varga (k, kh, g, gh) into க."""
        ka = tamil_engine.transliterate('ka')
        kha = tamil_engine.transliterate('kha')
        ga = tamil_engine.transliterate('ga')
        assert ka == kha == ga  # All map to க

    def test_tamil_unique_consonants(self, tamil_engine):
        """Tamil retains distinct consonants like ண (Na) and ந (na)."""
        Na = tamil_engine.transliterate('Na')
        na = tamil_engine.transliterate('na')
        assert Na != na  # ண vs ந

    def test_tamil_lx_zha(self, tamil_engine):
        """Lx maps to ழ in Tamil (via Devanagari ऴ)."""
        result = tamil_engine.transliterate('tamiLx')
        assert 'ழ' in result


# ============================================================
# Digits, Symbols, and Special Characters
# ============================================================

class TestDigitsAndSymbols:
    """Test digit and symbol transliteration."""

    def test_digits_kannada(self, kannada_engine):
        result = kannada_engine.transliterate('123')
        assert result == '೧೨೩'

    def test_digits_hindi(self, hindi_engine):
        result = hindi_engine.transliterate('0123456789')
        assert result == '०१२३४५६७८९'

    def test_digit_triggers_flush(self, kannada_engine):
        """Digits should be recognized after text."""
        result = kannada_engine.transliterate('ka1')
        assert '೧' in result

    def test_danda_symbol(self, kannada_engine):
        """Pipe | maps to danda ।"""
        result = kannada_engine.transliterate('|')
        assert result == '।'

    def test_double_danda(self, kannada_engine):
        result = kannada_engine.transliterate('||')
        assert result == '॥'

    def test_om_symbol_parsing(self, hindi_engine):
        """OM in transliteration engine produces vowel O + anusvara M.
        The ॐ symbol is triggered by OM. in the IME layer, not here."""
        result = hindi_engine.transliterate('OM')
        assert result == 'ओं'


# ============================================================
# Edge Cases and Advanced
# ============================================================

class TestEdgeCases:
    """Test edge cases and advanced transliteration scenarios."""

    def test_underscore_skip(self, kannada_engine):
        """Underscore _ is a skip character in Baraha."""
        # Without underscore: 'ka' → ಕ
        # With underscore between k and a: k_a should skip underscore
        result = kannada_engine.transliterate('k_a')
        # k gets virama (since _ follows), then a is standalone vowel
        assert 'ಕ' in result or 'ಅ' in result

    def test_zwj_caret(self, kannada_engine):
        """Single caret ^ inserts ZWJ."""
        result = kannada_engine.transliterate('^')
        assert '\u200D' in result  # ZWJ

    def test_zwnj_double_caret(self, kannada_engine):
        """Double caret ^^ inserts ZWNJ."""
        result = kannada_engine.transliterate('^^')
        assert '\u200C' in result  # ZWNJ

    def test_multiple_vowels_standalone(self, kannada_engine):
        """Multiple standalone vowels in sequence.
        Note: 'ai' is a diphthong matched greedily, so use separated vowels."""
        # 'aiu' would be parsed as 'ai' + 'u' = ಐಉ
        result = kannada_engine.transliterate('aiu')
        assert result == 'ಐಉ'  # ai(diphthong) + u
        # Separated vowels each produce standalone forms
        result2 = kannada_engine.transliterate('a i u')
        assert 'ಅ' in result2
        assert 'ಇ' in result2
        assert 'ಉ' in result2

    def test_consonant_virama_end(self, kannada_engine):
        """Consonant at end of input gets virama."""
        result = kannada_engine.transliterate('k')
        # k alone at end → ಕ + virama
        assert result == 'ಕ್'

    def test_mixed_text_with_english(self, kannada_engine):
        """Non-Baraha characters pass through."""
        result = kannada_engine.transliterate('Hello World')
        # 'H' matches visarga yogavaaha, but standalone
        # This is testing that the engine handles mixed content
        assert isinstance(result, str)

    def test_long_conjunct_chain(self, kannada_engine):
        """Test a long complex word from the original test suite."""
        result = kannada_engine.transliterate(
            'jyOtsnaabhiraahatamahaddhRudayaandhakaaram'
        )
        expected = 'ಜ್ಯೋತ್ಸ್ನಾಭಿರಾಹತಮಹದ್ಧೃದಯಾನ್ಧಕಾರಮ್'
        assert result == expected

    def test_sutra_style(self, kannada_engine):
        """Test sutra-style text with visarga."""
        result = kannada_engine.transliterate(
            'DralOpE poorvasya dIrGO NaH'
        )
        expected = 'ಡ್ರಲೋಪೇ ಪೋರ್ವಸ್ಯ ದೀರ್ಘೋ ಣಃ'
        assert result == expected


# ============================================================
# ANSI Conversion Tests
# ============================================================

class TestAnsiConversion:
    """Test convert_to_ansi function."""

    def test_kannada_ansi(self):
        """Test Kannada Unicode → ANSI conversion."""
        from transliteration import unicode_to_ansi_kannada
        # ಕ = \u0C95 → 'k'
        assert unicode_to_ansi_kannada('\u0C95') == 'k'
        # ಮ = \u0CAE → 'm'
        assert unicode_to_ansi_kannada('\u0CAE') == 'm'

    def test_hindi_ansi(self):
        """Test Hindi Unicode → ANSI conversion."""
        from transliteration import unicode_to_ansi_hindi
        # क = \u0915 → 'k'
        assert unicode_to_ansi_hindi('\u0915') == 'k'

    def test_convert_to_ansi_wrapper(self):
        """Test the convert_to_ansi wrapper function."""
        result = convert_to_ansi('\u0C95', 'kannada')
        assert result == 'k'

    def test_convert_to_ansi_unsupported_lang(self):
        """Unsupported language returns text unchanged."""
        result = convert_to_ansi('test', 'telugu')
        assert result == 'test'


# ============================================================
# Data Table Integrity Tests
# ============================================================

class TestDataTables:
    """Verify the transliteration data tables are consistent."""

    def test_all_vowels_have_signs(self):
        """Every Baraha vowel key should have a corresponding vowel sign."""
        for key in BARAHA_VOWELS:
            assert key in BARAHA_VOWEL_SIGNS, f"Vowel '{key}' missing from BARAHA_VOWEL_SIGNS"

    def test_consonant_table_not_empty(self):
        assert len(BARAHA_CONSONANTS) > 30

    def test_vowel_table_not_empty(self):
        assert len(BARAHA_VOWELS) > 10

    def test_language_registry(self):
        """All four primary languages must be in LANGUAGES."""
        for lang in ['kannada', 'hindi', 'telugu', 'tamil']:
            assert lang in LANGUAGES
            assert 'script_map' in LANGUAGES[lang]
            assert 'name' in LANGUAGES[lang]
            assert 'code' in LANGUAGES[lang]

    def test_devanagari_virama_constant(self):
        assert DEVANAGARI_VIRAMA == '\u094D'


# ============================================================
# ITRANS SCHEME TESTS
# ============================================================

class TestITRANSScheme:
    """Test ITRANS scheme transliteration."""

    def _engine(self, lang='hindi'):
        return TransliterationEngine(lang, scheme='itrans')

    # --- Basic vowels ---
    def test_itrans_vowels_hindi(self):
        e = self._engine('hindi')
        assert e.transliterate('a') == 'अ'
        assert e.transliterate('aa') == 'आ'
        assert e.transliterate('i') == 'इ'
        assert e.transliterate('ii') == 'ई'
        assert e.transliterate('u') == 'उ'
        assert e.transliterate('uu') == 'ऊ'
        assert e.transliterate('e') == 'ए'
        assert e.transliterate('ai') == 'ऐ'
        assert e.transliterate('o') == 'ओ'
        assert e.transliterate('au') == 'औ'

    def test_itrans_vocalic_vowels(self):
        e = self._engine('sanskrit')
        assert e.transliterate('RRi') == 'ऋ'
        assert e.transliterate('RRI') == 'ॠ'
        assert e.transliterate('R^i') == 'ऋ'
        assert e.transliterate('LLi') == 'ऌ'
        assert e.transliterate('LLI') == 'ॡ'

    # --- Basic consonants ---
    def test_itrans_consonants_ka_varga(self):
        e = self._engine('hindi')
        assert e.transliterate('ka') == 'क'
        assert e.transliterate('kha') == 'ख'
        assert e.transliterate('ga') == 'ग'
        assert e.transliterate('gha') == 'घ'

    def test_itrans_consonants_cha_varga(self):
        e = self._engine('hindi')
        assert e.transliterate('cha') == 'च'
        assert e.transliterate('Cha') == 'छ'
        assert e.transliterate('chha') == 'छ'
        assert e.transliterate('ja') == 'ज'
        assert e.transliterate('jha') == 'झ'

    def test_itrans_retroflex(self):
        e = self._engine('hindi')
        assert e.transliterate('Ta') == 'ट'
        assert e.transliterate('Tha') == 'ठ'
        assert e.transliterate('Da') == 'ड'
        assert e.transliterate('Dha') == 'ढ'
        assert e.transliterate('Na') == 'ण'

    def test_itrans_dental(self):
        e = self._engine('hindi')
        assert e.transliterate('ta') == 'त'
        assert e.transliterate('tha') == 'थ'
        assert e.transliterate('da') == 'द'
        assert e.transliterate('dha') == 'ध'
        assert e.transliterate('na') == 'न'

    def test_itrans_labial(self):
        e = self._engine('hindi')
        assert e.transliterate('pa') == 'प'
        assert e.transliterate('pha') == 'फ'
        assert e.transliterate('ba') == 'ब'
        assert e.transliterate('bha') == 'भ'
        assert e.transliterate('ma') == 'म'

    def test_itrans_semivowels(self):
        e = self._engine('hindi')
        assert e.transliterate('ya') == 'य'
        assert e.transliterate('ra') == 'र'
        assert e.transliterate('la') == 'ल'
        assert e.transliterate('va') == 'व'

    def test_itrans_sibilants(self):
        e = self._engine('hindi')
        assert e.transliterate('sha') == 'श'
        assert e.transliterate('Sha') == 'ष'
        assert e.transliterate('shha') == 'ष'
        assert e.transliterate('sa') == 'स'
        assert e.transliterate('ha') == 'ह'

    # --- Conjuncts ---
    def test_itrans_conjuncts(self):
        e = self._engine('hindi')
        assert e.transliterate('kSha') == 'क्ष'
        assert e.transliterate('xa') == 'क्ष'
        assert e.transliterate('GYa') == 'ज्ञ'
        assert e.transliterate('dnya') == 'ज्ञ'

    def test_itrans_conjunct_cluster(self):
        e = self._engine('sanskrit')
        # namaste
        assert e.transliterate('namaste') == 'नमस्ते'

    # --- Yogavaahas ---
    def test_itrans_anusvara(self):
        e = self._engine('hindi')
        assert e.transliterate('naM') == 'नं'
        assert e.transliterate('na.m') == 'नं'

    def test_itrans_visarga(self):
        e = self._engine('hindi')
        assert e.transliterate('namaH') == 'नमः'
        assert e.transliterate('nama.h') == 'नमः'

    def test_itrans_chandrabindu(self):
        e = self._engine('hindi')
        assert e.transliterate('ha.N') == 'हँ'

    # --- Nukta consonants ---
    def test_itrans_nukta(self):
        e = self._engine('hindi')
        import unicodedata
        # Nukta consonants: precomposed (\u0958) or decomposed (क़) are equivalent
        assert unicodedata.normalize('NFC', e.transliterate('qa')) == unicodedata.normalize('NFC', 'क़')
        assert unicodedata.normalize('NFC', e.transliterate('za')) == unicodedata.normalize('NFC', 'ज़')
        assert unicodedata.normalize('NFC', e.transliterate('fa')) == unicodedata.normalize('NFC', 'फ़')

    # --- Symbols ---
    def test_itrans_danda(self):
        e = self._engine('hindi')
        assert e.transliterate('|') == '।'
        assert e.transliterate('||') == '॥'

    def test_itrans_avagraha(self):
        e = self._engine('sanskrit')
        assert e.transliterate('.a') == 'ऽ'

    def test_itrans_om(self):
        e = self._engine('hindi')
        # ITRANS: 'O' is not a vowel (only lowercase 'o' is)
        # so 'OM' matches the OM symbol → ॐ directly
        assert e.transliterate('OM') == 'ॐ'
        # AUM is also a direct ITRANS symbol → ॐ
        assert e.transliterate('AUM') == 'ॐ'

    # --- Vedic marks (same as Baraha) ---
    def test_itrans_vedic(self):
        e = self._engine('sanskrit')
        assert e.transliterate('#') == '॑'
        assert e.transliterate('$') == '॒'
        assert e.transliterate('##') == '᳚'

    # --- Velar nasal ---
    def test_itrans_velar_nasal(self):
        e = self._engine('hindi')
        assert e.transliterate('~Na') == 'ङ'

    # --- Palatal nasal ---
    def test_itrans_palatal_nasal(self):
        e = self._engine('hindi')
        assert e.transliterate('~na') == 'ञ'
        assert e.transliterate('JNa') == 'ञ'

    # --- Cross-language: ITRANS with Kannada ---
    def test_itrans_kannada(self):
        e = self._engine('kannada')
        assert e.transliterate('namaskAra') == 'ನಮಸ್ಕಾರ'

    def test_itrans_telugu(self):
        e = self._engine('telugu')
        assert e.transliterate('namaste') == 'నమస్తే'

    def test_itrans_tamil(self):
        e = self._engine('tamil')
        result = e.transliterate('tamizh')
        assert 'த' in result  # Tamil ta

    # --- Scheme switching ---
    def test_scheme_switch_runtime(self):
        """Engine can switch scheme at runtime."""
        e = TransliterationEngine('hindi', scheme='baraha')
        assert e.scheme == 'baraha'
        baraha_result = e.transliterate('Ru')
        assert baraha_result == 'ऋ'

        e.set_scheme('itrans')
        assert e.scheme == 'itrans'
        itrans_result = e.transliterate('RRi')
        assert itrans_result == 'ऋ'

    def test_scheme_invalid(self):
        """Invalid scheme raises ValueError."""
        import pytest
        with pytest.raises(ValueError):
            TransliterationEngine('hindi', scheme='inscript')

    def test_scheme_default_is_baraha(self):
        """Default scheme should be Baraha."""
        e = TransliterationEngine('hindi')
        assert e.scheme == 'baraha'

    # --- Full sentence tests ---
    def test_itrans_gayatri_mantra(self):
        e = self._engine('sanskrit')
        # oM bhUrbhuvaH svaH
        result = e.transliterate('bhuurbhuvaH')
        assert 'भू' in result
        assert 'भुवः' in result

    def test_itrans_hindi_schwa(self):
        """Hindi ITRANS should also handle implicit schwa."""
        e = self._engine('hindi')
        result = e.transliterate('bharat')
        assert result == 'भारत' or result == 'भरत'  # schwa deletion at end

    # --- ITRANS-specific aliases ---
    def test_itrans_double_aliases(self):
        """ITRANS double-letter aliases should work."""
        e = self._engine('hindi')
        assert e.transliterate('aa') == 'आ'
        assert e.transliterate('ii') == 'ई'
        assert e.transliterate('uu') == 'ऊ'

    # --- SCHEMES registry ---
    def test_schemes_registry(self):
        from transliteration import SCHEMES
        assert 'baraha' in SCHEMES
        assert 'itrans' in SCHEMES
        for scheme_name, tables in SCHEMES.items():
            assert 'vowels' in tables
            assert 'vowel_signs' in tables
            assert 'consonants' in tables
            assert 'yogavaahas' in tables
            assert 'symbols' in tables
            assert 'digits' in tables

    def test_itrans_vowel_sign_completeness(self):
        """Every ITRANS vowel key should have a corresponding vowel sign."""
        from transliteration import ITRANS_VOWELS, ITRANS_VOWEL_SIGNS
        for key in ITRANS_VOWELS:
            assert key in ITRANS_VOWEL_SIGNS, f"ITRANS vowel '{key}' missing from ITRANS_VOWEL_SIGNS"


# ============================================================
# CUSTOM MAPPINGS TESTS
# ============================================================

class TestCustomMappings:
    """Test custom user mapping overrides."""

    def test_custom_consonant_override(self):
        """Custom mapping can override an existing consonant key."""
        cm = {'consonants': {'ka': '\u0916'}}  # ka → kha instead of ka
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('ka') == '\u0916'  # kha

    def test_custom_new_consonant(self):
        """Custom mapping can add a brand new key."""
        cm = {'consonants': {'xx': '\u0915'}}  # xx → ka
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('xx') == '\u0915'  # ka with inherent a (Hindi schwa)

    def test_custom_vowel_override(self):
        cm = {'vowels': {'ee': '\u0908'}, 'vowel_signs': {'ee': '\u0940'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('ee') == '\u0908'  # ee → ī

    def test_custom_symbol(self):
        cm = {'symbols': {'@@': '\u0950'}}  # @@ → OM symbol
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('@@') == '\u0950'

    def test_custom_empty(self):
        """Empty custom mappings should not affect behavior."""
        e1 = TransliterationEngine('hindi', custom_mappings={})
        e2 = TransliterationEngine('hindi')
        assert e1.transliterate('namaste') == e2.transliterate('namaste')

    def test_custom_none(self):
        """None custom mappings should not affect behavior."""
        e1 = TransliterationEngine('hindi', custom_mappings=None)
        e2 = TransliterationEngine('hindi')
        assert e1.transliterate('ka') == e2.transliterate('ka')

    def test_custom_with_itrans(self):
        """Custom mappings work with ITRANS scheme too."""
        cm = {'consonants': {'zz': '\u0915'}}
        e = TransliterationEngine('hindi', scheme='itrans', custom_mappings=cm)
        assert e.transliterate('zz') == '\u0915'  # ka with inherent a

    def test_set_custom_mappings_runtime(self):
        """Engine can update custom mappings at runtime."""
        e = TransliterationEngine('hindi')
        base = e.transliterate('ka')
        assert base == '\u0915'

        e.set_custom_mappings({'consonants': {'ka': '\u0916'}})
        assert e.transliterate('ka') == '\u0916'

        # Clearing restores original
        e.set_custom_mappings({})
        assert e.transliterate('ka') == '\u0915'

    def test_custom_preserves_non_overridden(self):
        """Custom override of one key doesn't affect others."""
        cm = {'consonants': {'ka': '\u0916'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('ka') == '\u0916'
        assert e.transliterate('ga') == '\u0917'  # ga still works

    def test_custom_cross_language(self):
        """Custom mappings survive language switch."""
        cm = {'consonants': {'xx': '\u0915'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        e.set_language('kannada')
        result = e.transliterate('xx')
        # xx maps to Devanagari ka, then stage 2 converts to Kannada ka
        assert '\u0C95' in result  # Kannada ka
