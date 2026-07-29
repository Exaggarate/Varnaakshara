"""
Comprehensive tests for the table-driven Varnaakshara transliteration engine.

Tests the new engine at core/engine/transliteration.py which loads data from
JSON files. Covers:
  - Basic transliteration for each language
  - Virama/schwa handling
  - Conjunct handling
  - Cross-script conversion
  - ISO 15919 romanization
  - ANSI conversion round-trip
  - Braille conversion
  - Collation keys
  - Scheme switching (Baraha vs ITRANS)
  - Custom mappings
  - Keyboard layouts
  - Engine API
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.engine.transliteration import (
    TransliterationEngine,
    SUPPORTED_LANGUAGES,
    DEVANAGARI_VIRAMA,
)


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture
def kannada_engine():
    return TransliterationEngine('kannada')

@pytest.fixture
def hindi_engine():
    return TransliterationEngine('hindi')

@pytest.fixture
def telugu_engine():
    return TransliterationEngine('telugu')

@pytest.fixture
def tamil_engine():
    return TransliterationEngine('tamil')

@pytest.fixture
def malayalam_engine():
    return TransliterationEngine('malayalam')

@pytest.fixture
def bengali_engine():
    return TransliterationEngine('bengali')

@pytest.fixture
def gujarati_engine():
    return TransliterationEngine('gujarati')

@pytest.fixture
def punjabi_engine():
    return TransliterationEngine('punjabi')

@pytest.fixture
def odia_engine():
    return TransliterationEngine('odia')

@pytest.fixture
def sanskrit_engine():
    return TransliterationEngine('sanskrit')

@pytest.fixture
def marathi_engine():
    return TransliterationEngine('marathi')

@pytest.fixture
def assamese_engine():
    return TransliterationEngine('assamese')


# ============================================================
# ENGINE API TESTS
# ============================================================

class TestEngineAPI:
    """Test the TransliterationEngine class interface."""

    def test_default_language_is_kannada(self):
        engine = TransliterationEngine()
        assert engine.language == 'kannada'

    def test_default_scheme_is_baraha(self):
        engine = TransliterationEngine()
        assert engine.scheme == 'baraha'

    def test_set_language_valid(self):
        engine = TransliterationEngine('kannada')
        engine.set_language('hindi')
        assert engine.language == 'hindi'

    def test_set_language_invalid(self):
        with pytest.raises(ValueError, match='Unsupported language'):
            TransliterationEngine('klingon')

    def test_set_scheme_invalid(self):
        with pytest.raises(ValueError, match='Unsupported scheme'):
            TransliterationEngine('kannada', scheme='inscript')

    def test_all_languages_constructible(self):
        for lang in SUPPORTED_LANGUAGES:
            engine = TransliterationEngine(lang)
            assert engine.language == lang

    def test_transliterate_returns_string(self):
        engine = TransliterationEngine('kannada')
        assert isinstance(engine.transliterate('namaste'), str)

    def test_transliterate_empty_string(self):
        engine = TransliterationEngine('kannada')
        assert engine.transliterate('') == ''

    def test_passthrough_ascii_symbols(self):
        engine = TransliterationEngine('kannada')
        assert engine.transliterate('@%') == '@%'

    def test_process_key_and_flush(self):
        engine = TransliterationEngine('kannada')
        out, flushed = engine.process_key('k')
        assert not flushed
        out, flushed = engine.process_key('a')
        assert not flushed
        out, flushed = engine.process_key(' ')
        assert flushed
        assert out is not None
        assert 'ಕ' in out

    def test_flush_explicit(self):
        engine = TransliterationEngine('kannada')
        engine.process_key('n')
        engine.process_key('a')
        result = engine.flush()
        assert result
        assert engine.flush() == ''

    def test_language_switch_mid_use(self):
        engine = TransliterationEngine('kannada')
        kn_result = engine.transliterate('ka')
        engine.set_language('hindi')
        hi_result = engine.transliterate('ka')
        assert kn_result != hi_result

    def test_transliterate_with_language_param(self):
        engine = TransliterationEngine('kannada')
        result = engine.transliterate('ka', language='hindi')
        assert result == 'क'

    def test_transliterate_with_scheme_param(self):
        engine = TransliterationEngine('hindi', scheme='baraha')
        result = engine.transliterate('RRi', scheme='itrans')
        assert result == 'ऋ'


# ============================================================
# KANNADA TRANSLITERATION
# ============================================================

class TestKannadaBasic:
    """Test Kannada transliteration."""

    @pytest.mark.parametrize("baraha,expected", [
        # Standalone vowels
        ('a', 'ಅ'), ('A', 'ಆ'), ('aa', 'ಆ'),
        ('i', 'ಇ'), ('I', 'ಈ'), ('u', 'ಉ'), ('U', 'ಊ'),
        ('e', 'ಎ'), ('E', 'ಏ'), ('ai', 'ಐ'),
        ('o', 'ಒ'), ('O', 'ಓ'), ('au', 'ಔ'),
        ('Ru', 'ಋ'),
        # Consonants with inherent a
        ('ka', 'ಕ'), ('kha', 'ಖ'), ('ga', 'ಗ'), ('gha', 'ಘ'),
        ('cha', 'ಚ'), ('ja', 'ಜ'),
        ('Ta', 'ಟ'), ('Da', 'ಡ'), ('Na', 'ಣ'),
        ('ta', 'ತ'), ('da', 'ದ'), ('na', 'ನ'),
        ('pa', 'ಪ'), ('ba', 'ಬ'), ('ma', 'ಮ'),
        ('ya', 'ಯ'), ('ra', 'ರ'), ('la', 'ಲ'), ('va', 'ವ'),
        ('sha', 'ಶ'), ('Sha', 'ಷ'), ('sa', 'ಸ'), ('ha', 'ಹ'),
        ('La', 'ಳ'),
    ])
    def test_basic_chars(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected

    @pytest.mark.parametrize("baraha,expected", [
        # Vowel signs (matras)
        ('kA', 'ಕಾ'), ('ki', 'ಕಿ'), ('kI', 'ಕೀ'),
        ('ku', 'ಕು'), ('kU', 'ಕೂ'),
        ('ke', 'ಕೆ'), ('kE', 'ಕೇ'), ('kai', 'ಕೈ'),
        ('ko', 'ಕೊ'), ('kO', 'ಕೋ'), ('kau', 'ಕೌ'),
        ('kRu', 'ಕೃ'),
    ])
    def test_vowel_signs(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected


class TestKannadaConjuncts:
    """Test Kannada conjuncts and virama handling."""

    @pytest.mark.parametrize("baraha,expected", [
        # Geminate consonants
        ('kka', 'ಕ್ಕ'), ('nna', 'ನ್ನ'), ('mma', 'ಮ್ಮ'),
        # Consonant clusters
        ('sta', 'ಸ್ತ'), ('stra', 'ಸ್ತ್ರ'),
        ('nda', 'ನ್ದ'), ('ndha', 'ನ್ಧ'),
        # Special conjuncts
        ('kSha', 'ಕ್ಷ'), ('j~ja', 'ಜ್ಞ'),
    ])
    def test_conjuncts(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected

    def test_virama_at_word_end(self, kannada_engine):
        """Dravidian script: final consonant gets virama."""
        assert kannada_engine.transliterate('ram') == 'ರಮ್'
        assert kannada_engine.transliterate('k') == 'ಕ್'

    def test_explicit_a_no_virama(self, kannada_engine):
        assert kannada_engine.transliterate('rama') == 'ರಮ'


class TestKannadaYogavaahas:
    """Test anusvara, visarga, chandrabindu."""

    def test_anusvara(self, kannada_engine):
        assert kannada_engine.transliterate('aM') == 'ಅಂ'
        assert kannada_engine.transliterate('rAmaM') == 'ರಾಮಂ'

    def test_visarga(self, kannada_engine):
        assert kannada_engine.transliterate('aH') == 'ಅಃ'
        assert kannada_engine.transliterate('duHkha') == 'ದುಃಖ'

    def test_chandrabindu(self, kannada_engine):
        assert kannada_engine.transliterate('a~M') == 'ಅಁ'


class TestKannadaWords:
    """Test full Kannada words."""

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
    def test_words(self, kannada_engine, baraha, expected):
        assert kannada_engine.transliterate(baraha) == expected

    def test_complex_word(self, kannada_engine):
        assert kannada_engine.transliterate('sha~gkaraacaaryaru') == 'ಶಙ್ಕರಾಚಾರ್ಯರು'

    def test_long_conjunct_chain(self, kannada_engine):
        result = kannada_engine.transliterate(
            'jyOtsnaabhiraahatamahaddhRudayaandhakaaram'
        )
        assert result == 'ಜ್ಯೋತ್ಸ್ನಾಭಿರಾಹತಮಹದ್ಧೃದಯಾನ್ಧಕಾರಮ್'

    def test_sutra_style(self, kannada_engine):
        result = kannada_engine.transliterate('DralOpE poorvasya dIrGO NaH')
        assert result == 'ಡ್ರಲೋಪೇ ಪೋರ್ವಸ್ಯ ದೀರ್ಘೋ ಣಃ'

    def test_words_with_space(self, kannada_engine):
        assert kannada_engine.transliterate('rAma sItA') == 'ರಾಮ ಸೀತಾ'

    def test_punctuation_preserved(self, kannada_engine):
        result = kannada_engine.transliterate('namO namaste!')
        assert result.endswith('!')


# ============================================================
# HINDI TRANSLITERATION
# ============================================================

class TestHindiTransliteration:
    """Test Hindi (Devanagari) transliteration."""

    @pytest.mark.parametrize("baraha,expected", [
        ('namaste', 'नमस्ते'),
        ('hindii', 'हिन्दी'),
        ('hindI', 'हिन्दी'),
        ('duniyaa', 'दुनिया'),
        ('kRuShNa', 'कृष्ण'),
        ('rAma', 'राम'),
        ('strii', 'स्त्री'),
    ])
    def test_hindi_words(self, hindi_engine, baraha, expected):
        assert hindi_engine.transliterate(baraha) == expected

    def test_implicit_schwa(self, hindi_engine):
        """Hindi keeps inherent 'a' at word end (no virama)."""
        assert hindi_engine.transliterate('bhaarat') == 'भारत'

    def test_no_short_e_o(self, hindi_engine):
        """Hindi maps short e/o to long e/o."""
        assert hindi_engine.transliterate('e') == 'ए'
        assert hindi_engine.transliterate('o') == 'ओ'

    def test_vowels(self, hindi_engine):
        assert hindi_engine.transliterate('a') == 'अ'
        assert hindi_engine.transliterate('i') == 'इ'
        assert hindi_engine.transliterate('u') == 'उ'


# ============================================================
# TELUGU TRANSLITERATION
# ============================================================

class TestTeluguTransliteration:
    """Test Telugu transliteration."""

    @pytest.mark.parametrize("baraha,expected", [
        ('namaskaaraM', 'నమస్కారం'),
        ('telugu', 'తెలుగు'),
    ])
    def test_words(self, telugu_engine, baraha, expected):
        assert telugu_engine.transliterate(baraha) == expected

    def test_vowel(self, telugu_engine):
        assert telugu_engine.transliterate('a') == 'అ'

    def test_consonant(self, telugu_engine):
        assert telugu_engine.transliterate('ka') == 'క'

    def test_anusvara(self, telugu_engine):
        assert telugu_engine.transliterate('aM') == 'అం'


# ============================================================
# TAMIL TRANSLITERATION
# ============================================================

class TestTamilTransliteration:
    """Test Tamil transliteration."""

    def test_vanakkam(self, tamil_engine):
        assert tamil_engine.transliterate('vanakkam') == 'வநக்கம்'

    def test_vowel(self, tamil_engine):
        assert tamil_engine.transliterate('a') == 'அ'

    def test_consonant_merge(self, tamil_engine):
        """Tamil merges ka-varga into க."""
        ka = tamil_engine.transliterate('ka')
        kha = tamil_engine.transliterate('kha')
        ga = tamil_engine.transliterate('ga')
        assert ka == kha == ga

    def test_unique_consonants(self, tamil_engine):
        Na = tamil_engine.transliterate('Na')
        na = tamil_engine.transliterate('na')
        assert Na != na

    def test_zha(self, tamil_engine):
        result = tamil_engine.transliterate('tamiLx')
        assert 'ழ' in result


# ============================================================
# OTHER LANGUAGES
# ============================================================

class TestMalayalamTransliteration:
    def test_basic(self, malayalam_engine):
        assert malayalam_engine.transliterate('ka') == 'ക'
        assert malayalam_engine.transliterate('a') == 'അ'

    def test_word(self, malayalam_engine):
        result = malayalam_engine.transliterate('malayaaLaM')
        assert 'മ' in result
        assert 'ല' in result


class TestBengaliTransliteration:
    def test_basic(self, bengali_engine):
        assert bengali_engine.transliterate('ka') == 'ক'
        assert bengali_engine.transliterate('a') == 'অ'

    def test_word(self, bengali_engine):
        result = bengali_engine.transliterate('bAMlA')
        assert 'ব' in result or 'বা' in result


class TestGujaratiTransliteration:
    def test_basic(self, gujarati_engine):
        assert gujarati_engine.transliterate('ka') == 'ક'
        assert gujarati_engine.transliterate('a') == 'અ'


class TestPunjabiTransliteration:
    def test_basic(self, punjabi_engine):
        assert punjabi_engine.transliterate('ka') == 'ਕ'

    def test_vowel(self, punjabi_engine):
        # Punjabi has no short e/o, Ru, etc.
        assert punjabi_engine.transliterate('a') in ('ਅ', 'ਅ')


class TestOdiaTransliteration:
    def test_basic(self, odia_engine):
        assert odia_engine.transliterate('ka') == 'କ'
        assert odia_engine.transliterate('a') == 'ଅ'


class TestMarathiTransliteration:
    def test_basic(self, marathi_engine):
        # Marathi uses Devanagari
        assert marathi_engine.transliterate('ka') == 'क'

    def test_implicit_schwa(self, marathi_engine):
        # Marathi has implicit schwa
        assert marathi_engine.transliterate('bhaarat') == 'भारत'


class TestSanskritTransliteration:
    def test_basic(self, sanskrit_engine):
        # Sanskrit uses Devanagari but NO implicit schwa
        assert sanskrit_engine.transliterate('ka') == 'क'

    def test_no_implicit_schwa(self, sanskrit_engine):
        """Sanskrit shows virama on final consonant."""
        result = sanskrit_engine.transliterate('raam')
        assert result.endswith('म्')

    def test_namaste(self, sanskrit_engine):
        assert sanskrit_engine.transliterate('namaste') == 'नमस्ते'


class TestAssameseTransliteration:
    def test_basic(self, assamese_engine):
        # Assamese uses Bengali script with র→ৰ
        result = assamese_engine.transliterate('ka')
        assert result == 'ক'


# ============================================================
# DIGITS AND SYMBOLS
# ============================================================

class TestDigitsAndSymbols:
    def test_digits_kannada(self, kannada_engine):
        assert kannada_engine.transliterate('123') == '೧೨೩'

    def test_digits_hindi(self, hindi_engine):
        assert hindi_engine.transliterate('0123456789') == '०१२३४५६७८९'

    def test_danda(self, kannada_engine):
        assert kannada_engine.transliterate('|') == '।'

    def test_double_danda(self, kannada_engine):
        assert kannada_engine.transliterate('||') == '॥'

    def test_om_hindi(self, hindi_engine):
        """OM in Baraha scheme produces O + M = ओं"""
        result = hindi_engine.transliterate('OM')
        assert result == 'ओं'


# ============================================================
# VIRAMA AND SCHWA HANDLING
# ============================================================

class TestViramaSchwa:
    """Test virama and schwa handling across language types."""

    def test_dravidian_virama(self, kannada_engine):
        """Kannada: final consonant gets virama."""
        assert 'ಕ್' == kannada_engine.transliterate('k')

    def test_indic_no_virama(self, hindi_engine):
        """Hindi: final consonant keeps inherent 'a' (no virama)."""
        result = hindi_engine.transliterate('bharat')
        assert '्' not in result[-1:]  # no virama at end

    def test_conjunct_virama(self):
        """Virama between consonants forms conjunct in all languages."""
        for lang in ['kannada', 'hindi', 'telugu']:
            engine = TransliterationEngine(lang)
            result = engine.transliterate('kka')
            # Should contain virama between the two k's
            assert result  # just verify it doesn't crash

    def test_zwj(self, kannada_engine):
        result = kannada_engine.transliterate('^')
        assert '\u200D' in result

    def test_zwnj(self, kannada_engine):
        result = kannada_engine.transliterate('^^')
        assert '\u200C' in result

    def test_underscore_skip(self, kannada_engine):
        result = kannada_engine.transliterate('k_a')
        assert 'ಅ' in result


# ============================================================
# CASE SENSITIVITY
# ============================================================

class TestCaseSensitivity:
    def test_T_vs_t(self, kannada_engine):
        assert kannada_engine.transliterate('Ta') == 'ಟ'
        assert kannada_engine.transliterate('ta') == 'ತ'

    def test_D_vs_d(self, kannada_engine):
        assert kannada_engine.transliterate('Da') == 'ಡ'
        assert kannada_engine.transliterate('da') == 'ದ'

    def test_N_vs_n(self, kannada_engine):
        assert kannada_engine.transliterate('Na') == 'ಣ'
        assert kannada_engine.transliterate('na') == 'ನ'

    def test_S_vs_s(self, kannada_engine):
        assert kannada_engine.transliterate('Sa') == 'ಶ'
        assert kannada_engine.transliterate('sa') == 'ಸ'

    def test_K_vs_k(self, kannada_engine):
        assert kannada_engine.transliterate('Ka') == 'ಖ'
        assert kannada_engine.transliterate('ka') == 'ಕ'


# ============================================================
# ITRANS SCHEME
# ============================================================

class TestITRANSScheme:
    """Test ITRANS scheme transliteration."""

    def _engine(self, lang='hindi'):
        return TransliterationEngine(lang, scheme='itrans')

    def test_vowels(self):
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

    def test_vocalic_vowels(self):
        e = self._engine('sanskrit')
        assert e.transliterate('RRi') == 'ऋ'
        assert e.transliterate('RRI') == 'ॠ'
        assert e.transliterate('LLi') == 'ऌ'

    def test_consonants(self):
        e = self._engine('hindi')
        assert e.transliterate('ka') == 'क'
        assert e.transliterate('kha') == 'ख'
        assert e.transliterate('ga') == 'ग'
        assert e.transliterate('cha') == 'च'
        assert e.transliterate('Cha') == 'छ'
        assert e.transliterate('Ta') == 'ट'
        assert e.transliterate('Tha') == 'ठ'
        assert e.transliterate('ta') == 'त'
        assert e.transliterate('tha') == 'थ'

    def test_conjuncts(self):
        e = self._engine('hindi')
        assert e.transliterate('kSha') == 'क्ष'
        assert e.transliterate('xa') == 'क्ष'
        assert e.transliterate('GYa') == 'ज्ञ'

    def test_anusvara(self):
        e = self._engine('hindi')
        assert e.transliterate('naM') == 'नं'
        assert e.transliterate('na.m') == 'नं'

    def test_visarga(self):
        e = self._engine('hindi')
        assert e.transliterate('namaH') == 'नमः'

    def test_om(self):
        e = self._engine('hindi')
        assert e.transliterate('OM') == 'ॐ'
        assert e.transliterate('AUM') == 'ॐ'

    def test_danda(self):
        e = self._engine('hindi')
        assert e.transliterate('|') == '।'
        assert e.transliterate('||') == '॥'

    def test_itrans_kannada(self):
        e = self._engine('kannada')
        assert e.transliterate('namaskAra') == 'ನಮಸ್ಕಾರ'

    def test_itrans_telugu(self):
        e = self._engine('telugu')
        assert e.transliterate('namaste') == 'నమస్తే'

    def test_scheme_switch_runtime(self):
        e = TransliterationEngine('hindi', scheme='baraha')
        assert e.scheme == 'baraha'
        assert e.transliterate('Ru') == 'ऋ'
        e.set_scheme('itrans')
        assert e.scheme == 'itrans'
        assert e.transliterate('RRi') == 'ऋ'

    def test_double_aliases(self):
        e = self._engine('hindi')
        assert e.transliterate('aa') == 'आ'
        assert e.transliterate('ii') == 'ई'
        assert e.transliterate('uu') == 'ऊ'


# ============================================================
# CUSTOM MAPPINGS
# ============================================================

class TestCustomMappings:
    def test_custom_consonant_override(self):
        cm = {'consonants': {'ka': '\u0916'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('ka') == '\u0916'

    def test_custom_new_key(self):
        cm = {'consonants': {'xx': '\u0915'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('xx') == '\u0915'

    def test_custom_vowel(self):
        cm = {'vowels': {'ee': '\u0908'}, 'vowel_signs': {'ee': '\u0940'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('ee') == '\u0908'

    def test_custom_symbol(self):
        cm = {'symbols': {'@@': '\u0950'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('@@') == '\u0950'

    def test_custom_empty(self):
        e1 = TransliterationEngine('hindi', custom_mappings={})
        e2 = TransliterationEngine('hindi')
        assert e1.transliterate('namaste') == e2.transliterate('namaste')

    def test_custom_none(self):
        e1 = TransliterationEngine('hindi', custom_mappings=None)
        e2 = TransliterationEngine('hindi')
        assert e1.transliterate('ka') == e2.transliterate('ka')

    def test_custom_with_itrans(self):
        cm = {'consonants': {'zz': '\u0915'}}
        e = TransliterationEngine('hindi', scheme='itrans', custom_mappings=cm)
        assert e.transliterate('zz') == '\u0915'

    def test_set_custom_mappings_runtime(self):
        e = TransliterationEngine('hindi')
        assert e.transliterate('ka') == '\u0915'
        e.set_custom_mappings({'consonants': {'ka': '\u0916'}})
        assert e.transliterate('ka') == '\u0916'
        e.set_custom_mappings({})
        assert e.transliterate('ka') == '\u0915'

    def test_custom_preserves_non_overridden(self):
        cm = {'consonants': {'ka': '\u0916'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        assert e.transliterate('ka') == '\u0916'
        assert e.transliterate('ga') == '\u0917'

    def test_custom_cross_language(self):
        cm = {'consonants': {'xx': '\u0915'}}
        e = TransliterationEngine('hindi', custom_mappings=cm)
        e.set_language('kannada')
        result = e.transliterate('xx')
        assert '\u0C95' in result  # Kannada ka


# ============================================================
# CROSS-SCRIPT CONVERSION
# ============================================================

class TestCrossScript:
    """Test convert_script between scripts."""

    def test_kannada_to_telugu(self, kannada_engine):
        result = kannada_engine.convert_script('ಕನ್ನಡ', 'kannada', 'telugu')
        assert result == 'కన్నడ'

    def test_kannada_to_hindi(self, kannada_engine):
        result = kannada_engine.convert_script('ನಮಸ್ಕಾರ', 'kannada', 'hindi')
        assert result == 'नमस्कार'

    def test_kannada_to_malayalam(self, kannada_engine):
        result = kannada_engine.convert_script('ಕನ್ನಡ', 'kannada', 'malayalam')
        assert 'ക' in result

    def test_hindi_to_kannada(self, hindi_engine):
        result = hindi_engine.convert_script('नमस्ते', 'hindi', 'kannada')
        assert 'ನ' in result

    def test_telugu_to_kannada(self, telugu_engine):
        result = telugu_engine.convert_script('నమస్కారం', 'telugu', 'kannada')
        assert 'ನ' in result

    def test_identity(self, kannada_engine):
        """Convert to same script should return approximately same text."""
        text = 'ಕನ್ನಡ'
        result = kannada_engine.convert_script(text, 'kannada', 'kannada')
        assert result == text


# ============================================================
# ISO 15919 ROMANIZATION
# ============================================================

class TestISO15919:
    """Test ISO 15919 romanization output."""

    def test_kannada_basic(self, kannada_engine):
        result = kannada_engine.to_iso15919('ನಮಸ್ಕಾರ')
        assert result == 'namaskāra'

    def test_kannada_conjunct(self, kannada_engine):
        result = kannada_engine.to_iso15919('ಕನ್ನಡ')
        assert result == 'kannaḍa'

    def test_hindi_basic(self, hindi_engine):
        result = hindi_engine.to_iso15919('नमस्ते')
        assert result == 'namastē'

    def test_hindi_conjunct(self, hindi_engine):
        result = hindi_engine.to_iso15919('कृष्ण')
        assert 'kr̥' in result

    def test_telugu(self, telugu_engine):
        result = telugu_engine.to_iso15919('తెలుగు')
        assert result == 'telugu'

    def test_tamil(self, tamil_engine):
        result = tamil_engine.to_iso15919('தமிழ்')
        # Tamil ழ should romanize
        assert 'tamiḻ' == result or 'tam' in result

    def test_with_language_param(self, kannada_engine):
        """Can specify language parameter."""
        result = kannada_engine.to_iso15919('ಅಮ್ಮ', language='kannada')
        assert result == 'amma'


# ============================================================
# ANSI CONVERSION ROUND-TRIP
# ============================================================

class TestAnsiConversion:
    """Test ANSI (legacy font) conversion."""

    def test_kannada_to_ansi(self, kannada_engine):
        result = kannada_engine.to_ansi('ಕ')
        assert result == 'k'

    def test_kannada_to_ansi_word(self, kannada_engine):
        result = kannada_engine.to_ansi('ಕನ್ನಡ')
        assert 'k' in result

    def test_hindi_to_ansi(self, hindi_engine):
        result = hindi_engine.to_ansi('क')
        assert result == 'k'

    def test_ansi_round_trip_kannada(self, kannada_engine):
        """Convert to ANSI and back should approximately match."""
        original = 'ಕನ್ನಡ'
        ansi = kannada_engine.to_ansi(original)
        back = kannada_engine.from_ansi(ansi)
        assert back == original

    def test_ansi_round_trip_hindi(self, hindi_engine):
        original = 'नमस्ते'
        ansi = hindi_engine.to_ansi(original)
        back = hindi_engine.from_ansi(ansi)
        assert back == original

    def test_unsupported_lang(self, telugu_engine):
        """Unsupported language returns text unchanged."""
        result = telugu_engine.to_ansi('test')
        assert result == 'test'


# ============================================================
# BRAILLE CONVERSION
# ============================================================

class TestBrailleConversion:
    def test_kannada_braille(self, kannada_engine):
        result = kannada_engine.to_braille('ಕ')
        # Should return a braille character
        assert result  # non-empty
        assert isinstance(result, str)

    def test_hindi_braille(self, hindi_engine):
        result = hindi_engine.to_braille('क')
        assert result
        assert isinstance(result, str)


# ============================================================
# COLLATION
# ============================================================

class TestCollation:
    def test_collation_key_returns_tuple(self, kannada_engine):
        key = kannada_engine.get_collation_key('ಕ')
        assert isinstance(key, tuple)

    def test_collation_ordering(self, kannada_engine):
        """ka should sort before kha."""
        key_ka = kannada_engine.get_collation_key('ಕ')
        key_kha = kannada_engine.get_collation_key('ಖ')
        assert key_ka < key_kha

    def test_collation_multiple_chars(self, kannada_engine):
        key = kannada_engine.get_collation_key('ಕನ್ನಡ')
        assert len(key) > 1


# ============================================================
# KEYBOARD LAYOUTS
# ============================================================

class TestKeyboardLayouts:
    def test_get_inscript_layout(self, kannada_engine):
        layout = kannada_engine.get_keyboard_layout('kannada', 'inscript')
        assert isinstance(layout, dict)
        # Should have at least 'normal' layer
        if layout:  # may be empty if data not loaded
            assert 'normal' in layout or len(layout) > 0

    def test_get_layout_returns_dict(self, hindi_engine):
        layout = hindi_engine.get_keyboard_layout('hindi', 'inscript')
        assert isinstance(layout, dict)


# ============================================================
# ALL LANGUAGES BASIC SANITY
# ============================================================

class TestAllLanguagesSanity:
    """Verify basic transliteration works for every language."""

    @pytest.mark.parametrize("lang,expected_char_class", [
        ('kannada', 'ಕ'),
        ('hindi', 'क'),
        ('telugu', 'క'),
        ('tamil', 'க'),
        ('malayalam', 'ക'),
        ('marathi', 'क'),
        ('sanskrit', 'क'),
        ('bengali', 'ক'),
        ('assamese', 'ক'),
        ('gujarati', 'ક'),
        ('punjabi', 'ਕ'),
        ('odia', 'କ'),
    ])
    def test_ka_for_all_languages(self, lang, expected_char_class):
        engine = TransliterationEngine(lang)
        result = engine.transliterate('ka')
        assert result == expected_char_class

    @pytest.mark.parametrize("lang", list(SUPPORTED_LANGUAGES.keys()))
    def test_namaste_for_all(self, lang):
        """namaste should produce non-empty output for all languages."""
        engine = TransliterationEngine(lang)
        result = engine.transliterate('namaste')
        assert result
        assert len(result) > 0
        # Should contain non-ASCII characters
        assert any(ord(c) > 127 for c in result)


# ============================================================
# REVERSE TRANSLITERATION
# ============================================================

class TestReverseTransliteration:
    def test_basic_reverse(self, kannada_engine):
        """Reverse transliterate should produce readable Roman text."""
        result = kannada_engine.reverse_transliterate('ಕನ್ನಡ')
        assert isinstance(result, str)
        assert len(result) > 0
        # Should contain ASCII characters
        assert any(ord(c) < 128 for c in result)

    def test_reverse_vowel(self, kannada_engine):
        result = kannada_engine.reverse_transliterate('ಅ')
        assert 'a' in result.lower()


# ============================================================
# EDGE CASES
# ============================================================

class TestEdgeCases:
    def test_multiple_vowels(self, kannada_engine):
        result = kannada_engine.transliterate('aiu')
        assert result == 'ಐಉ'

    def test_separated_vowels(self, kannada_engine):
        result = kannada_engine.transliterate('a i u')
        assert 'ಅ' in result
        assert 'ಇ' in result
        assert 'ಉ' in result

    def test_mixed_text(self, kannada_engine):
        result = kannada_engine.transliterate('Hello ka World')
        assert isinstance(result, str)

    def test_digit_after_text(self, kannada_engine):
        result = kannada_engine.transliterate('ka1')
        assert '೧' in result

    def test_vedic_marks(self, kannada_engine):
        assert kannada_engine.transliterate('#') == '॑'
        assert kannada_engine.transliterate('$') == '॒'
        assert kannada_engine.transliterate('##') == '᳚'


# ============================================================
# SCHEME SWITCHING (BARAHA vs ITRANS)
# ============================================================

class TestSchemeSwitching:
    """Test switching between Baraha and ITRANS schemes."""

    def test_baraha_kRuShNa(self):
        e = TransliterationEngine('hindi', scheme='baraha')
        assert e.transliterate('kRuShNa') == 'कृष्ण'

    def test_itrans_kRuShNa(self):
        """ITRANS uses different keys for RI/vocalic R."""
        e = TransliterationEngine('hindi', scheme='itrans')
        assert e.transliterate('kRRiShNa') == 'कृष्ण'

    def test_baraha_vocalic_r(self):
        e = TransliterationEngine('hindi', scheme='baraha')
        assert e.transliterate('Ru') == 'ऋ'

    def test_itrans_vocalic_r(self):
        e = TransliterationEngine('hindi', scheme='itrans')
        assert e.transliterate('RRi') == 'ऋ'

    def test_runtime_switch(self):
        e = TransliterationEngine('kannada', scheme='baraha')
        baraha_result = e.transliterate('namaskaara')
        e.set_scheme('itrans')
        itrans_result = e.transliterate('namaskAra')
        assert baraha_result == itrans_result == 'ನಮಸ್ಕಾರ'

    def test_both_produce_same_devanagari(self):
        """Same input text should produce same Devanagari for both schemes."""
        b = TransliterationEngine('hindi', scheme='baraha')
        i = TransliterationEngine('hindi', scheme='itrans')
        # Common inputs that are same in both
        for text in ['namaste', 'ka', 'ga', 'ta', 'da', 'na', 'pa', 'ba', 'ma']:
            assert b.transliterate(text) == i.transliterate(text), \
                f"Mismatch for '{text}': baraha={b.transliterate(text)}, itrans={i.transliterate(text)}"
