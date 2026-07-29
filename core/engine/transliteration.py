"""
Table-driven transliteration engine for Indian languages.

Loads all transliteration rules, script mappings, ISO 15919 tables,
braille tables, font conversion tables, collation tables, and keyboard
layouts from JSON data files at runtime.

Architecture:
  Stage 1: Roman (Baraha/ITRANS) → Devanagari via greedy longest-match
  Stage 2: Devanagari → Target script via character-level mapping

Pure Python, no OS dependencies. Shared between IME and Writer.

Supported languages: kannada, hindi, telugu, tamil, malayalam, marathi,
                     sanskrit, bengali, assamese, gujarati, punjabi, odia

Supported schemes: baraha, itrans
"""

import json
import os
from functools import lru_cache


# ============================================================
# DATA DIRECTORY
# ============================================================

_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')


def _data_path(*parts):
    """Resolve a path under the data directory."""
    return os.path.join(_DATA_DIR, *parts)


@lru_cache(maxsize=64)
def _load_json(path):
    """Load and cache a JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _load_language_data(lang, category):
    """Load JSON data for a language from a category subdirectory."""
    path = _data_path(category, f'{lang}.json')
    if os.path.exists(path):
        return _load_json(path)
    return None


# ============================================================
# CONSTANTS
# ============================================================

DEVANAGARI_VIRAMA = '\u094D'  # ्

# Characters that signal a word boundary
WORD_BOUNDARY = frozenset(' \n\t\r.,;:!?()-[]{}\"\'/\\<>@#$%^*+=~`')

# Languages that do NOT distinguish short e/o from long e/o.
_NO_SHORT_EO = frozenset({
    'sanskrit', 'hindi', 'marathi', 'bengali', 'assamese',
    'gujarati', 'punjabi', 'odia',
})

# Languages with implicit schwa: word-final consonants keep inherent 'a'
_IMPLICIT_SCHWA = frozenset({
    'hindi', 'marathi', 'bengali', 'assamese',
    'gujarati', 'punjabi', 'odia',
})

# All supported languages
SUPPORTED_LANGUAGES = {
    'kannada':   {'name': 'Kannada',   'code': 'kn'},
    'hindi':     {'name': 'Hindi',     'code': 'hi'},
    'telugu':    {'name': 'Telugu',    'code': 'te'},
    'tamil':     {'name': 'Tamil',     'code': 'ta'},
    'malayalam': {'name': 'Malayalam', 'code': 'ml'},
    'marathi':   {'name': 'Marathi',   'code': 'mr'},
    'sanskrit':  {'name': 'Sanskrit',  'code': 'sa'},
    'bengali':   {'name': 'Bengali',   'code': 'bn'},
    'assamese':  {'name': 'Assamese',  'code': 'as'},
    'gujarati':  {'name': 'Gujarati',  'code': 'gu'},
    'punjabi':   {'name': 'Punjabi',   'code': 'pa'},
    'odia':      {'name': 'Odia',      'code': 'or'},
}


# ============================================================
# SCHEME DATA — loaded from JSON but with hardcoded fallbacks
# ============================================================

def _build_scheme_tables():
    """Build scheme tables from JSON data files.

    Returns dict: scheme_name -> {vowels, vowel_signs, consonants, yogavaahas, symbols, digits}
    Each value maps Roman input key -> Devanagari Unicode string.
    """
    # Load phonetic rules for hindi (Devanagari = canonical)
    data = _load_language_data('hindi', 'phonetic_rules')
    if data and 'schemes' in data:
        schemes = {}
        for scheme_name, tables in data['schemes'].items():
            schemes[scheme_name] = {
                'vowels': dict(tables.get('vowels', {})),
                'vowel_signs': dict(tables.get('vowel_signs', {})),
                'consonants': dict(tables.get('consonants', {})),
                'yogavaahas': dict(tables.get('yogavaahas', {})),
                'symbols': dict(tables.get('symbols', {})),
                'digits': dict(tables.get('digits', {})),
            }
        return schemes
    return None


def _build_script_map(lang):
    """Build Devanagari → target script mapping from JSON data."""
    data = _load_language_data(lang, 'unicode_maps')
    if data:
        return dict(data.get('devanagari_to_target', {}))
    return {}


# ============================================================
# TRANSLITERATION ENGINE
# ============================================================

class TransliterationEngine:
    """
    Table-driven transliteration engine for Indian languages.

    Converts phonetic English (Baraha/ITRANS) to Indian script Unicode.
    Loads rules from JSON data files under core/data/.

    Usage:
        engine = TransliterationEngine('kannada')
        result = engine.transliterate('namaskaara')
        # → ನಮಸ್ಕಾರ

        engine = TransliterationEngine('hindi', scheme='itrans')
        result = engine.transliterate('namaste')
        # → नमस्ते
    """

    def __init__(self, language='kannada', scheme='baraha', custom_mappings=None):
        self._custom_mappings = custom_mappings or {}
        self._schemes_cache = _build_scheme_tables()
        self._script_map_cache = {}
        self._iso_cache = {}
        self._braille_cache = {}
        self._collation_cache = {}
        self._keyboard_cache = {}
        self._font_conv_cache = {}
        self._ansi_map_cache = {}

        self.set_scheme(scheme)
        self.set_language(language)

    # ============================================================
    # SCHEME MANAGEMENT
    # ============================================================

    def set_scheme(self, scheme):
        """Set the input scheme (baraha or itrans). Rebuilds sorted key lists."""
        scheme = scheme.lower()

        if self._schemes_cache and scheme in self._schemes_cache:
            tables = self._schemes_cache[scheme]
        else:
            # Fallback: try to get scheme tables
            available = list(self._schemes_cache.keys()) if self._schemes_cache else []
            raise ValueError(
                f"Unsupported scheme: {scheme}. Available: {available or ['baraha', 'itrans']}"
            )

        self.scheme = scheme
        self._consonants = dict(tables['consonants'])
        self._yogavaahas_table = dict(tables['yogavaahas'])
        self._symbols_table = dict(tables['symbols'])
        self._digits_table = dict(tables['digits'])
        self._base_vowels = dict(tables['vowels'])
        self._base_vowel_signs = dict(tables['vowel_signs'])

        # Apply custom mappings overlay
        self._apply_custom_mappings()
        self._build_sorted_keys()

        # If language is already set, rebuild per-language vowel tables
        if hasattr(self, 'language'):
            self.set_language(self.language)

    def set_custom_mappings(self, custom_mappings):
        """Update custom mappings and rebuild tables."""
        self._custom_mappings = custom_mappings or {}
        self.set_scheme(self.scheme)

    def _apply_custom_mappings(self):
        """Overlay custom user mappings on top of the active scheme tables.

        custom_mappings format:
        {
            "consonants": {"key": "\\u0915", ...},
            "vowels": {"key": "\\u0905", ...},
            "vowel_signs": {"key": "\\u093E", ...},
            "symbols": {"key": "\\u0950", ...},
            "yogavaahas": {"key": "\\u0902", ...}
        }
        """
        cm = self._custom_mappings
        if not cm:
            return
        if 'consonants' in cm:
            self._consonants.update(cm['consonants'])
        if 'vowels' in cm:
            self._base_vowels.update(cm['vowels'])
        if 'vowel_signs' in cm:
            self._base_vowel_signs.update(cm['vowel_signs'])
        if 'symbols' in cm:
            self._symbols_table.update(cm['symbols'])
        if 'yogavaahas' in cm:
            self._yogavaahas_table.update(cm['yogavaahas'])

    def _build_sorted_keys(self):
        """Pre-sort all token lists by length (longest first) for greedy matching."""
        self._sorted_consonants = sorted(self._consonants.keys(), key=len, reverse=True)
        self._sorted_vowels = sorted(self._base_vowels.keys(), key=len, reverse=True)
        self._sorted_vowel_signs = sorted(self._base_vowel_signs.keys(), key=len, reverse=True)
        self._sorted_yogavaahas = sorted(self._yogavaahas_table.keys(), key=len, reverse=True)
        self._sorted_symbols = sorted(self._symbols_table.keys(), key=len, reverse=True)

    # ============================================================
    # LANGUAGE MANAGEMENT
    # ============================================================

    def set_language(self, language):
        """Set the target language for transliteration."""
        if language not in SUPPORTED_LANGUAGES:
            raise ValueError(
                f"Unsupported language: {language}. "
                f"Available: {list(SUPPORTED_LANGUAGES.keys())}"
            )
        self.language = language

        # Load script map from cache or JSON
        if language not in self._script_map_cache:
            self._script_map_cache[language] = _build_script_map(language)
        self._script_map = self._script_map_cache[language]

        self._implicit_schwa = language in _IMPLICIT_SCHWA

        # Build per-language vowel/sign tables from the active scheme
        if language in _NO_SHORT_EO:
            # Map 'e'→long ए, 'o'→long ओ (no short e/o distinction)
            self._vowels = {**self._base_vowels,
                            'e': '\u090F', 'o': '\u0913'}
            self._vowel_signs = {**self._base_vowel_signs,
                                 'e': '\u0947', 'o': '\u094B'}
        else:
            # Kannada, Telugu, Tamil, Malayalam — keep short e/o
            self._vowels = self._base_vowels
            self._vowel_signs = self._base_vowel_signs

        # Rebuild sorted vowel keys for the adjusted tables
        self._sorted_vowels = sorted(self._vowels.keys(), key=len, reverse=True)
        self._sorted_vowel_signs = sorted(self._vowel_signs.keys(), key=len, reverse=True)

    # ============================================================
    # CORE TRANSLITERATION
    # ============================================================

    def _match_token(self, text, pos, sorted_keys, table):
        """Try to match a token at position `pos` using greedy longest-match.
        Returns (key, value) or (None, None)."""
        for key in sorted_keys:
            end = pos + len(key)
            if end <= len(text) and text[pos:end] == key:
                return key, table[key]
        return None, None

    def _is_consonant_start(self, text, pos):
        """Check if position `pos` starts a consonant token."""
        for key in self._sorted_consonants:
            end = pos + len(key)
            if end <= len(text) and text[pos:end] == key:
                return True
        return False

    def _transliterate_to_devanagari(self, text):
        """Parse Roman text and produce Devanagari Unicode string."""
        result = []
        i = 0
        n = len(text)

        while i < n:
            ch = text[i]

            # --- Skip character ---
            if ch == '_':
                i += 1
                continue

            # --- ZWJ / ZWNJ ---
            if ch == '^':
                if i + 1 < n and text[i + 1] == '^':
                    result.append('\u200C')  # ZWNJ
                    i += 2
                else:
                    result.append('\u200D')  # ZWJ
                    i += 1
                continue

            # --- Multi-char symbols before single-char ---
            if text[i] == '|' and i + 1 < n and text[i + 1] == '|':
                result.append(self._symbols_table.get('||', '॥'))
                i += 2
                continue
            if text[i] == '#' and i + 1 < n and text[i + 1] == '#':
                result.append(self._symbols_table.get('##', '\u1CDA'))
                i += 2
                continue
            # AUM (ITRANS only) — check before vowels consume A/U
            if text[i:i + 3] == 'AUM' and 'AUM' in self._symbols_table:
                result.append(self._symbols_table['AUM'])
                i += 3
                continue

            # --- Try consonant ---
            cons_key, cons_deva = self._match_token(
                text, i, self._sorted_consonants, self._consonants
            )
            if cons_key is not None:
                i += len(cons_key)
                result.append(cons_deva)

                # After a consonant, look for a vowel sign
                vsign_key, vsign_deva = self._match_token(
                    text, i, self._sorted_vowel_signs, self._vowel_signs
                )
                if vsign_key is not None:
                    if vsign_key == 'a':
                        # Explicit 'a' = inherent vowel, just consume
                        i += len(vsign_key)
                    else:
                        result.append(vsign_deva)
                        i += len(vsign_key)
                else:
                    # No vowel follows. Check what's next:
                    if i >= n or text[i] in WORD_BOUNDARY:
                        # End of input or word boundary
                        if self._implicit_schwa:
                            pass  # Hindi/Marathi etc.: keep inherent 'a'
                        else:
                            result.append(DEVANAGARI_VIRAMA)
                    elif self._is_consonant_start(text, i):
                        # Next is another consonant → virama for conjunct
                        result.append(DEVANAGARI_VIRAMA)
                    elif text[i] == '_':
                        # Skip marker → virama
                        result.append(DEVANAGARI_VIRAMA)
                    else:
                        # Check for yogavaaha (M, H, ~M)
                        yog_key, _ = self._match_token(
                            text, i, self._sorted_yogavaahas, self._yogavaahas_table
                        )
                        if yog_key is not None:
                            # Yogavaaha follows — consonant has inherent 'a'
                            pass
                        elif text[i] == '^':
                            # ZWJ/ZWNJ → virama
                            result.append(DEVANAGARI_VIRAMA)
                        elif (text[i] in self._symbols_table or
                              self._match_token(
                                  text, i, self._sorted_symbols,
                                  self._symbols_table
                              )[0] is not None):
                            # Symbol follows — acts like word boundary
                            if self._implicit_schwa:
                                pass
                            else:
                                result.append(DEVANAGARI_VIRAMA)
                        else:
                            # Something else (digit, etc.) → virama
                            result.append(DEVANAGARI_VIRAMA)
                continue

            # --- Try yogavaaha ---
            yog_key, yog_deva = self._match_token(
                text, i, self._sorted_yogavaahas, self._yogavaahas_table
            )
            if yog_key is not None:
                result.append(yog_deva)
                i += len(yog_key)
                continue

            # --- Try standalone vowel ---
            vow_key, vow_deva = self._match_token(
                text, i, self._sorted_vowels, self._vowels
            )
            if vow_key is not None:
                result.append(vow_deva)
                i += len(vow_key)
                continue

            # --- Try digit ---
            if ch in self._digits_table:
                result.append(self._digits_table[ch])
                i += 1
                continue

            # --- Try symbol ---
            sym_key, sym_deva = self._match_token(
                text, i, self._sorted_symbols, self._symbols_table
            )
            if sym_key is not None:
                result.append(sym_deva)
                i += len(sym_key)
                continue

            # --- Pass through unchanged ---
            result.append(ch)
            i += 1

        return ''.join(result)

    def _devanagari_to_target(self, deva_text):
        """Map Devanagari string to target script using character-level mapping."""
        if not self._script_map:
            return deva_text
        result = []
        for ch in deva_text:
            result.append(self._script_map.get(ch, ch))
        return ''.join(result)

    def transliterate(self, text, language=None, scheme=None):
        """Convert phonetic English to target Indian script.

        Args:
            text: Roman phonetic input string
            language: Optional language override (default: current language)
            scheme: Optional scheme override (default: current scheme)

        Returns:
            Unicode string in the target script
        """
        if scheme and scheme != self.scheme:
            self.set_scheme(scheme)
        if language and language != self.language:
            self.set_language(language)

        deva = self._transliterate_to_devanagari(text)
        return self._devanagari_to_target(deva)

    # ============================================================
    # REVERSE TRANSLITERATION
    # ============================================================

    def reverse_transliterate(self, text, language=None):
        """Convert Indian script Unicode back to Roman (Baraha scheme).

        Args:
            text: Unicode string in an Indian script
            language: Optional language override

        Returns:
            Romanized string in Baraha scheme
        """
        if language and language != self.language:
            self.set_language(language)

        # Build reverse maps: Devanagari -> Roman
        # First, convert target script to Devanagari
        if self._script_map:
            reverse_script = {v: k for k, v in self._script_map.items() if v}
            deva_text = ''.join(reverse_script.get(ch, ch) for ch in text)
        else:
            deva_text = text

        # Now convert Devanagari to Roman using reverse vowel/consonant maps
        reverse_vowels = {v: k for k, v in sorted(
            self._base_vowels.items(), key=lambda x: len(x[0])
        ) if v}
        reverse_consonants = {v: k for k, v in sorted(
            self._consonants.items(), key=lambda x: len(x[0])
        ) if v}
        reverse_signs = {v: k for k, v in sorted(
            self._base_vowel_signs.items(), key=lambda x: len(x[0])
        ) if v and k != 'a'}
        reverse_yogavaahas = {v: k for k, v in self._yogavaahas_table.items() if v}
        reverse_symbols = {v: k for k, v in self._symbols_table.items() if v}
        reverse_digits = {v: k for k, v in self._digits_table.items() if v}

        result = []
        i = 0
        n = len(deva_text)

        while i < n:
            ch = deva_text[i]

            # Try vowel sign
            if ch in reverse_signs:
                result.append(reverse_signs[ch])
                i += 1
                continue

            # Try virama
            if ch == DEVANAGARI_VIRAMA:
                i += 1
                continue

            # Try consonant (adds 'a' unless followed by virama or vowel sign)
            if ch in reverse_consonants:
                result.append(reverse_consonants[ch])
                # Check if next char is virama or vowel sign
                if i + 1 < n:
                    next_ch = deva_text[i + 1]
                    if next_ch == DEVANAGARI_VIRAMA:
                        pass  # virama = no inherent 'a'
                    elif next_ch in reverse_signs:
                        pass  # vowel sign follows
                    elif next_ch in reverse_yogavaahas:
                        result.append('a')  # inherent 'a' before yogavaaha
                    else:
                        result.append('a')  # inherent 'a'
                else:
                    result.append('a')  # final consonant has inherent 'a'
                i += 1
                continue

            # Try standalone vowel
            if ch in reverse_vowels:
                result.append(reverse_vowels[ch])
                i += 1
                continue

            # Try yogavaaha
            if ch in reverse_yogavaahas:
                result.append(reverse_yogavaahas[ch])
                i += 1
                continue

            # Try digit
            if ch in reverse_digits:
                result.append(reverse_digits[ch])
                i += 1
                continue

            # Try symbol
            if ch in reverse_symbols:
                result.append(reverse_symbols[ch])
                i += 1
                continue

            # Pass through
            result.append(ch)
            i += 1

        return ''.join(result)

    # ============================================================
    # CROSS-SCRIPT CONVERSION
    # ============================================================

    def convert_script(self, text, from_lang, to_lang):
        """Convert text from one Indian script to another.

        Goes through Devanagari as pivot:
        Source script → Devanagari → Target script

        Args:
            text: Unicode text in the source script
            from_lang: Source language name
            to_lang: Target language name

        Returns:
            Unicode string in the target script
        """
        # Build source → Devanagari reverse map
        # Prefer primary (non-nukta) mappings by sorting source keys
        source_map = _build_script_map(from_lang)
        if source_map:
            reverse_source = {}
            # Sort by source key codepoint to prefer primary consonants
            for k, v in sorted(source_map.items(), key=lambda x: ord(x[0])):
                if v and v not in reverse_source:
                    reverse_source[v] = k
            deva_text = []
            for ch in text:
                deva_text.append(reverse_source.get(ch, ch))
            deva_text = ''.join(deva_text)
        else:
            deva_text = text

        # Build Devanagari → target map
        target_map = _build_script_map(to_lang)
        if target_map:
            result = []
            for ch in deva_text:
                result.append(target_map.get(ch, ch))
            return ''.join(result)
        return deva_text

    # ============================================================
    # ISO 15919 ROMANIZATION
    # ============================================================

    def to_iso15919(self, text, language=None):
        """Convert Indian script Unicode to ISO 15919 romanization.

        Args:
            text: Unicode text in an Indian script
            language: Language of the text (default: current language)

        Returns:
            ISO 15919 romanized string
        """
        lang = language or self.language

        # Load ISO 15919 data (with supplementary virama/sign mappings)
        if lang not in self._iso_cache:
            data = _load_language_data(lang, 'iso15919')
            base = dict(data.get('unicode_to_romanization', {})) if data else {}
            # Supplement with standard virama and common sign mappings
            base.update(_get_iso15919_supplements(lang))
            self._iso_cache[lang] = base

        iso_map = self._iso_cache[lang]
        if not iso_map:
            return text

        # Build set of consonant characters and virama/vowel-sign characters
        consonants_set = set()
        virama_set = set()
        vowel_signs_set = set()
        for ch, rom in iso_map.items():
            if len(ch) == 1:
                cp = ord(ch)
                # Detect character type by Unicode block position
                block_base = (cp // 0x80) * 0x80
                offset = cp - block_base
                if 0x15 <= offset <= 0x39:  # consonant range
                    consonants_set.add(ch)
                elif offset == 0x4D:  # virama
                    virama_set.add(ch)
                elif 0x3E <= offset <= 0x4C:  # vowel sign range
                    vowel_signs_set.add(ch)

        # Context-aware romanization
        result = []
        i = 0
        n = len(text)
        while i < n:
            ch = text[i]
            # Try 2-char sequences first (for composite vowel signs)
            if i + 1 < n:
                pair = ch + text[i + 1]
                if pair in iso_map:
                    result.append(iso_map[pair])
                    i += 2
                    continue
            if ch in iso_map:
                rom = iso_map[ch]
                result.append(rom)
                # Add inherent 'a' after consonants when appropriate
                if ch in consonants_set:
                    # Check next character
                    next_ch = text[i + 1] if i + 1 < n else None
                    # No inherent 'a' if followed by virama or vowel sign
                    if next_ch and (next_ch in virama_set or
                                    next_ch in vowel_signs_set):
                        pass  # virama/sign follows
                    else:
                        result.append('a')  # inherent vowel
            else:
                result.append(ch)
            i += 1
        return ''.join(result)

    # ============================================================
    # BRAILLE CONVERSION
    # ============================================================

    def to_braille(self, text, language=None):
        """Convert Indian script Unicode to Braille.

        Args:
            text: Unicode text in an Indian script
            language: Language of the text (default: current language)

        Returns:
            Braille string
        """
        lang = language or self.language

        # Load braille data
        if lang not in self._braille_cache:
            data = _load_language_data(lang, 'braille')
            if data:
                # Extract just the braille character mapping
                raw = data.get('unicode_to_braille', {})
                self._braille_cache[lang] = {
                    k: v['braille'] if isinstance(v, dict) else v
                    for k, v in raw.items()
                }
            else:
                self._braille_cache[lang] = {}

        braille_map = self._braille_cache[lang]
        if not braille_map:
            return text

        result = []
        for ch in text:
            if ch in braille_map:
                result.append(braille_map[ch])
            else:
                result.append(ch)
        return ''.join(result)

    # ============================================================
    # ANSI (LEGACY FONT) CONVERSION
    # ============================================================

    def _load_font_conv(self, font_family):
        """Load a font conversion table."""
        if font_family not in self._font_conv_cache:
            # Search for matching font conversion file
            fc_dir = _data_path('font_conversion')
            if os.path.exists(fc_dir):
                for fname in os.listdir(fc_dir):
                    if not fname.endswith('.json'):
                        continue
                    path = os.path.join(fc_dir, fname)
                    data = _load_json(path)
                    src = data.get('source_font', '').lower()
                    tgt = data.get('target_font', '').lower()
                    ff_lower = font_family.lower()
                    if ff_lower in src or ff_lower in tgt or ff_lower in fname.lower():
                        self._font_conv_cache[font_family] = data.get('mappings', {})
                        return self._font_conv_cache[font_family]
            self._font_conv_cache[font_family] = {}
        return self._font_conv_cache[font_family]

    def to_ansi(self, text, language=None, font_family='baraha'):
        """Convert Unicode Indian script text to ANSI (legacy font encoding).

        Uses the BrhCode-based font conversion tables from Baraha RE.

        Args:
            text: Unicode text in an Indian script
            language: Language of the text
            font_family: Font family name (e.g., 'baraha', 'shree', 'kruti')

        Returns:
            ANSI encoded string
        """
        lang = language or self.language

        # Load BrhCode table for this language
        brh_data = _load_language_data(lang, 'unicode_maps')
        if not brh_data:
            return text

        # For ANSI conversion, we need unicode → brhcode mapping
        # This is implicit in the phonetic rules data
        # For now, build from the unicode map's reverse direction
        # plus the brhcode tables loaded at generation time.

        # Use a simple built-in ANSI map for common cases
        ansi_map = self._get_builtin_ansi_map(lang, font_family=font_family)
        if not ansi_map:
            return text

        if font_family == 'shreelipi':
            # Check if map uses hex byte notation (e.g. "0x65+0xF3")
            sample_vals = list(ansi_map.values())[:5]
            uses_hex = any(v.startswith('0x') for v in sample_vals if v)
            if uses_hex:
                return self._encode_shreelipi(text, ansi_map)

        return ''.join(ansi_map.get(ch, ch) for ch in text)

    def _encode_shreelipi(self, text, ansi_map):
        """Encode Unicode text to Shreelipi ANSI byte string.

        Shreelipi maps use hex byte notation (e.g. '0x65', '0x65+0xF3').
        Multi-byte sequences are joined with '+' in the map and produce
        multiple raw bytes in the output.
        """
        result = []
        for ch in text:
            mapped = ansi_map.get(ch)
            if mapped is None:
                result.append(ch)
            else:
                # Convert hex notation to actual bytes/chars
                for byte_str in mapped.split('+'):
                    byte_str = byte_str.strip()
                    if byte_str.startswith('0x'):
                        try:
                            result.append(chr(int(byte_str, 16)))
                        except (ValueError, OverflowError):
                            result.append(byte_str)
                    else:
                        result.append(byte_str)
        return ''.join(result)

    def _decode_shreelipi(self, text, reverse_map):
        """Decode Shreelipi ANSI byte string to Unicode.

        The reverse_map keys are hex-byte sequences from the JSON file.
        We convert the input text to hex-byte sequences and do greedy matching.
        """
        # Build a lookup from actual byte sequences to Unicode
        byte_seq_map = {}
        for hex_key, unicode_ch in reverse_map.items():
            # Convert hex key like "0x65+0xF3" to actual character sequence
            chars = []
            for byte_str in hex_key.split('+'):
                byte_str = byte_str.strip()
                if byte_str.startswith('0x'):
                    try:
                        chars.append(chr(int(byte_str, 16)))
                    except (ValueError, OverflowError):
                        chars.append(byte_str)
                else:
                    chars.append(byte_str)
            byte_seq_map[''.join(chars)] = unicode_ch

        # Sort by key length descending for greedy matching
        sorted_keys = sorted(byte_seq_map.keys(), key=len, reverse=True)

        result = []
        i = 0
        n = len(text)
        while i < n:
            matched = False
            for key in sorted_keys:
                end = i + len(key)
                if end <= n and text[i:end] == key:
                    result.append(byte_seq_map[key])
                    i = end
                    matched = True
                    break
            if not matched:
                result.append(text[i])
                i += 1
        return ''.join(result)

    def from_ansi(self, text, language=None, font_family='baraha'):
        """Convert ANSI (legacy font encoding) to Unicode.

        Args:
            text: ANSI encoded text
            language: Target language
            font_family: Font family name

        Returns:
            Unicode string
        """
        lang = language or self.language

        # Load the reverse map from JSON
        cache_key = f'{font_family}:{lang}'
        reverse_cache_key = f'reverse:{cache_key}'

        if reverse_cache_key in self._ansi_map_cache:
            reverse = self._ansi_map_cache[reverse_cache_key]
        else:
            # Load reverse map from JSON data
            if font_family == 'shreelipi':
                json_path = _data_path('ansi_maps', 'shreelipi', f'{lang}.json')
            else:
                json_path = _data_path('ansi_maps', f'{lang}.json')

            # Fall back to hindi map for marathi/sanskrit
            if not os.path.exists(json_path) and lang in ('marathi', 'sanskrit'):
                if font_family == 'shreelipi':
                    json_path = _data_path('ansi_maps', 'shreelipi', 'hindi.json')
                else:
                    json_path = _data_path('ansi_maps', 'hindi.json')

            if os.path.exists(json_path):
                data = _load_json(json_path)
                # Support both key naming conventions
                reverse = (data.get('ansi_to_unicode') or
                           data.get('shreelipi_to_unicode') or
                           {})
                # If no explicit reverse map, build from forward map
                if not reverse:
                    fwd = (data.get('unicode_to_ansi') or
                           data.get('unicode_to_shreelipi') or
                           {})
                    reverse = {v: k for k, v in fwd.items() if v}
            else:
                reverse = {}
            self._ansi_map_cache[reverse_cache_key] = reverse

        if not reverse:
            return text

        # Shreelipi: check if map uses hex-byte notation in keys
        if font_family == 'shreelipi':
            sample_keys = list(reverse.keys())[:5]
            uses_hex = any(k.startswith('0x') for k in sample_keys if k)
            if uses_hex:
                return self._decode_shreelipi(text, reverse)

        # Standard (Baraha) ANSI — greedy matching on plain text keys
        sorted_keys = sorted(reverse.keys(), key=len, reverse=True)

        result = []
        i = 0
        n = len(text)
        while i < n:
            matched = False
            for key in sorted_keys:
                end = i + len(key)
                if end <= n and text[i:end] == key:
                    result.append(reverse[key])
                    i = end
                    matched = True
                    break
            if not matched:
                result.append(text[i])
                i += 1
        return ''.join(result)

    # ============================================================
    # ENCODING DETECTION
    # ============================================================

    def detect_encoding(self, text):
        """Detect whether text is Unicode, Baraha ANSI, or Shreelipi ANSI.

        Returns:
            Tuple of (encoding, language, confidence) where:
            - encoding: 'unicode' | 'baraha' | 'shreelipi'
            - language: detected language name or current language
            - confidence: float 0.0-1.0

        Strategy:
        - If text has codepoints in Indic Unicode blocks (0x0900-0x0DFF) → 'unicode'
        - If text is all ASCII/Latin1 range, try matching against known ANSI maps
        - Check which ANSI map has the best coverage match
        """
        if not text:
            return ('unicode', self.language, 0.0)

        # Check for Indic Unicode codepoints
        indic_count = 0
        ascii_count = 0
        high_latin_count = 0
        total = len(text)

        for ch in text:
            cp = ord(ch)
            if 0x0900 <= cp <= 0x0DFF:
                indic_count += 1
            elif cp <= 0x007F:
                ascii_count += 1
            elif 0x0080 <= cp <= 0x00FF:
                high_latin_count += 1

        # If significant Indic Unicode codepoints present, it's Unicode
        non_space = sum(1 for ch in text if not ch.isspace())
        if non_space == 0:
            return ('unicode', self.language, 0.0)

        indic_ratio = indic_count / non_space
        if indic_ratio > 0.3:
            # Detect which language based on Unicode block
            detected_lang = self._detect_unicode_language(text)
            return ('unicode', detected_lang, min(1.0, indic_ratio + 0.2))

        # All ASCII/Latin1 — could be Baraha or Shreelipi ANSI
        if high_latin_count > 0:
            # High-byte Latin characters suggest Shreelipi
            best_lang, best_score = self._match_ansi_maps(text, 'shreelipi')
            if best_score > 0.2:
                return ('shreelipi', best_lang, best_score)

        # Try Baraha ANSI matching
        best_lang, best_score = self._match_ansi_maps(text, 'baraha')
        if best_score > 0.3:
            return ('baraha', best_lang, best_score)

        # Try Shreelipi as fallback
        best_lang_sl, best_score_sl = self._match_ansi_maps(text, 'shreelipi')
        if best_score_sl > best_score:
            return ('shreelipi', best_lang_sl, best_score_sl)

        # Default: treat as unicode
        return ('unicode', self.language, 0.5)

    def _detect_unicode_language(self, text):
        """Detect language from Unicode codepoints based on script block."""
        block_counts = {}
        for ch in text:
            cp = ord(ch)
            if 0x0900 <= cp <= 0x097F:
                block_counts['hindi'] = block_counts.get('hindi', 0) + 1
            elif 0x0980 <= cp <= 0x09FF:
                block_counts['bengali'] = block_counts.get('bengali', 0) + 1
            elif 0x0A00 <= cp <= 0x0A7F:
                block_counts['punjabi'] = block_counts.get('punjabi', 0) + 1
            elif 0x0A80 <= cp <= 0x0AFF:
                block_counts['gujarati'] = block_counts.get('gujarati', 0) + 1
            elif 0x0B00 <= cp <= 0x0B7F:
                block_counts['odia'] = block_counts.get('odia', 0) + 1
            elif 0x0B80 <= cp <= 0x0BFF:
                block_counts['tamil'] = block_counts.get('tamil', 0) + 1
            elif 0x0C00 <= cp <= 0x0C7F:
                block_counts['telugu'] = block_counts.get('telugu', 0) + 1
            elif 0x0C80 <= cp <= 0x0CFF:
                block_counts['kannada'] = block_counts.get('kannada', 0) + 1
            elif 0x0D00 <= cp <= 0x0D7F:
                block_counts['malayalam'] = block_counts.get('malayalam', 0) + 1
        if block_counts:
            return max(block_counts, key=block_counts.get)
        return self.language

    def _match_ansi_maps(self, text, font_family):
        """Try matching text against known ANSI maps for all languages.

        Returns (best_language, best_score).
        """
        best_lang = self.language
        best_score = 0.0

        # Languages that have ANSI maps
        candidates = ['kannada', 'hindi']

        for lang in candidates:
            if font_family == 'shreelipi':
                json_path = _data_path('ansi_maps', 'shreelipi', f'{lang}.json')
            else:
                json_path = _data_path('ansi_maps', f'{lang}.json')

            if not os.path.exists(json_path):
                continue

            data = _load_json(json_path)
            ansi_to_unicode = data.get('ansi_to_unicode', {})
            if not ansi_to_unicode:
                continue

            if font_family == 'shreelipi':
                # For Shreelipi, check if text bytes match known hex patterns
                score = self._score_shreelipi_match(text, ansi_to_unicode)
            else:
                # For Baraha, check character coverage
                known_chars = set()
                for key in ansi_to_unicode:
                    known_chars.update(key)
                non_space = [ch for ch in text if not ch.isspace()]
                if non_space:
                    matches = sum(1 for ch in non_space if ch in known_chars)
                    score = matches / len(non_space)
                else:
                    score = 0.0

            if score > best_score:
                best_score = score
                best_lang = lang

        return best_lang, best_score

    def _score_shreelipi_match(self, text, ansi_to_unicode):
        """Score how well text matches a Shreelipi ANSI map."""
        # Build set of byte values that appear in the map
        known_bytes = set()
        for hex_key in ansi_to_unicode:
            for byte_str in hex_key.split('+'):
                byte_str = byte_str.strip()
                if byte_str.startswith('0x'):
                    try:
                        known_bytes.add(int(byte_str, 16))
                    except ValueError:
                        pass

        non_space = [ch for ch in text if not ch.isspace()]
        if not non_space:
            return 0.0

        matches = sum(1 for ch in non_space if ord(ch) in known_bytes)
        return matches / len(non_space)

    # ============================================================
    # CROSS-ENCODING CONVERSION
    # ============================================================

    def convert_encoding(self, text, from_encoding, to_encoding,
                         language=None, from_family='baraha', to_family='baraha'):
        """Convert between any encoding pair: unicode↔baraha, unicode↔shreelipi, baraha↔shreelipi.

        Args:
            text: Input text
            from_encoding: 'unicode', 'baraha', or 'shreelipi'
            to_encoding: 'unicode', 'baraha', or 'shreelipi'
            language: Language for the conversion (default: current)
            from_family: Font family hint for source (used when from_encoding is 'baraha'/'shreelipi')
            to_family: Font family hint for target (used when to_encoding is 'baraha'/'shreelipi')

        Returns:
            Converted text string
        """
        if from_encoding == to_encoding and from_family == to_family:
            return text

        lang = language or self.language

        # Normalize encoding names to font_family
        if from_encoding in ('baraha', 'shreelipi'):
            from_family = from_encoding
        if to_encoding in ('baraha', 'shreelipi'):
            to_family = to_encoding

        # Step 1: Convert source to Unicode if needed
        if from_encoding == 'unicode':
            unicode_text = text
        elif from_encoding in ('baraha', 'shreelipi'):
            unicode_text = self.from_ansi(text, language=lang, font_family=from_family)
        else:
            raise ValueError(f"Unknown source encoding: {from_encoding}")

        # Step 2: Convert Unicode to target encoding
        if to_encoding == 'unicode':
            return unicode_text
        elif to_encoding in ('baraha', 'shreelipi'):
            return self.to_ansi(unicode_text, language=lang, font_family=to_family)
        else:
            raise ValueError(f"Unknown target encoding: {to_encoding}")

    def _get_builtin_ansi_map(self, lang, font_family='baraha'):
        """Get ANSI conversion map for a language, loaded from JSON data files.

        Args:
            lang: Language name
            font_family: 'baraha' or 'shreelipi'

        Returns:
            Dict mapping Unicode char → ANSI string, or None if not available.
        """
        cache_key = f'{font_family}:{lang}'
        if cache_key in self._ansi_map_cache:
            return self._ansi_map_cache[cache_key]

        # Determine JSON path based on font family
        if font_family == 'shreelipi':
            json_path = _data_path('ansi_maps', 'shreelipi', f'{lang}.json')
        else:
            json_path = _data_path('ansi_maps', f'{lang}.json')

        # Fall back to hindi map for marathi/sanskrit
        if not os.path.exists(json_path) and lang in ('marathi', 'sanskrit'):
            if font_family == 'shreelipi':
                json_path = _data_path('ansi_maps', 'shreelipi', 'hindi.json')
            else:
                json_path = _data_path('ansi_maps', 'hindi.json')

        if os.path.exists(json_path):
            data = _load_json(json_path)
            # Support both key naming conventions:
            # Baraha files: 'unicode_to_ansi' / 'ansi_to_unicode'
            # Shreelipi files: 'unicode_to_shreelipi' / 'shreelipi_to_unicode'
            ansi_map = (data.get('unicode_to_ansi') or
                        data.get('unicode_to_shreelipi') or
                        {})
            self._ansi_map_cache[cache_key] = ansi_map
            return ansi_map

        self._ansi_map_cache[cache_key] = None
        return None

    # ============================================================
    # COLLATION
    # ============================================================

    def get_collation_key(self, text, language=None):
        """Get a sortable collation key for text.

        Uses the Baraha-derived collation tables to produce
        a key suitable for sorting Indian language text in
        proper linguistic order.

        Args:
            text: Unicode text to generate collation key for
            language: Language (default: current)

        Returns:
            Tuple of integers suitable for sorting comparison
        """
        lang = language or self.language

        if lang not in self._collation_cache:
            data = _load_language_data(lang, 'collation')
            if data:
                self._collation_cache[lang] = data.get('unicode_to_collcode', {})
            else:
                self._collation_cache[lang] = {}

        coll_map = self._collation_cache[lang]
        if not coll_map:
            # Fallback: use Unicode codepoint order
            return tuple(ord(c) for c in text)

        keys = []
        for ch in text:
            if ch in coll_map:
                keys.append(coll_map[ch])
            else:
                # Unmapped chars get high values to sort last
                keys.append(0xFFFF + ord(ch))
        return tuple(keys)

    # ============================================================
    # KEYBOARD LAYOUT SUPPORT
    # ============================================================

    def get_keyboard_layout(self, language=None, layout_type='inscript'):
        """Get keyboard layout mapping for a language.

        Args:
            language: Language (default: current)
            layout_type: 'inscript' or 'baraha_keyboard'

        Returns:
            Dict of layer_name -> {key -> unicode_char} mappings
        """
        lang = language or self.language

        cache_key = f'{lang}:{layout_type}'
        if cache_key not in self._keyboard_cache:
            data = _load_language_data(lang, 'keyboard_layouts')
            if data:
                self._keyboard_cache[cache_key] = data.get(layout_type, {})
            else:
                self._keyboard_cache[cache_key] = {}

        return self._keyboard_cache[cache_key]

    def transliterate_inscript(self, text, language=None):
        """Transliterate text using INSCRIPT keyboard layout.

        Args:
            text: Key sequence from INSCRIPT keyboard
            language: Language (default: current)

        Returns:
            Unicode string
        """
        layout = self.get_keyboard_layout(language, 'inscript')
        if not layout:
            return text

        # Merge all layers, with shift layers taking precedence
        merged = {}
        for layer_name in ('normal', 'shift_a', 'shift_b'):
            if layer_name in layout:
                merged.update(layout[layer_name])

        result = []
        for ch in text:
            result.append(merged.get(ch, ch))
        return ''.join(result)

    # ============================================================
    # INCREMENTAL INPUT (IME)
    # ============================================================

    def process_key(self, char):
        """Process a single keypress for real-time transliteration.

        Returns:
            (output_text, should_flush) tuple
        """
        if not hasattr(self, '_buffer'):
            self._buffer = ''
        self._buffer += char

        if char in ' \n\t.,;:!?()-[]{}\"\'/' or char.isdigit():
            output = self.transliterate(self._buffer)
            self._buffer = ''
            return output, True

        return None, False

    def flush(self):
        """Force flush the buffer."""
        if hasattr(self, '_buffer') and self._buffer:
            result = self.transliterate(self._buffer)
            self._buffer = ''
            return result
        return ''


# ============================================================
# ISO 15919 SUPPLEMENTS
# ============================================================

# Standard ISO 15919 romanization for characters often missing from
# BrhCode-derived tables (virama, composed vowel signs, etc.)
_ISO15919_SUPPLEMENTS = {
    # Devanagari supplements
    'devanagari': {
        '\u094D': '',      # virama = empty (implicit in romanization)
        '\u093E': 'ā',     # aa sign
        '\u093F': 'i',     # i sign
        '\u0940': 'ī',     # ii sign
        '\u0941': 'u',     # u sign
        '\u0942': 'ū',     # uu sign
        '\u0943': 'r̥',    # Ru sign
        '\u0944': 'r̥̄',   # RU sign
        '\u0945': 'ê',     # candra e sign
        '\u0946': 'e',     # short e sign
        '\u0947': 'ē',     # long e sign
        '\u0948': 'ai',    # ai sign
        '\u0949': 'ô',     # candra o sign
        '\u094A': 'o',     # short o sign
        '\u094B': 'ō',     # long o sign
        '\u094C': 'au',    # au sign
        '\u0905': 'a', '\u0906': 'ā', '\u0907': 'i', '\u0908': 'ī',
        '\u0909': 'u', '\u090A': 'ū', '\u090B': 'r̥', '\u0960': 'r̥̄',
        '\u090C': 'l̥', '\u0961': 'l̥̄',
        '\u090D': 'ê', '\u090E': 'e', '\u090F': 'ē', '\u0910': 'ai',
        '\u0911': 'ô', '\u0912': 'o', '\u0913': 'ō', '\u0914': 'au',
        '\u0902': 'ṁ', '\u0903': 'ḥ', '\u0901': 'm̐',
        '\u0915': 'k', '\u0916': 'kh', '\u0917': 'g', '\u0918': 'gh', '\u0919': 'ṅ',
        '\u091A': 'c', '\u091B': 'ch', '\u091C': 'j', '\u091D': 'jh', '\u091E': 'ñ',
        '\u091F': 'ṭ', '\u0920': 'ṭh', '\u0921': 'ḍ', '\u0922': 'ḍh', '\u0923': 'ṇ',
        '\u0924': 't', '\u0925': 'th', '\u0926': 'd', '\u0927': 'dh', '\u0928': 'n',
        '\u092A': 'p', '\u092B': 'ph', '\u092C': 'b', '\u092D': 'bh', '\u092E': 'm',
        '\u092F': 'y', '\u0930': 'r', '\u0932': 'l', '\u0935': 'v',
        '\u0936': 'ś', '\u0937': 'ṣ', '\u0938': 's', '\u0939': 'h',
        '\u0933': 'ḷ', '\u0934': 'ḻ', '\u0931': 'ṟ',
        '\u0964': '.', '\u0965': '..',
        '\u0950': 'ōṁ',
    },
    # Kannada supplements
    'kannada': {
        '\u0CCD': '',      # virama
        '\u0CBE': 'ā', '\u0CBF': 'i', '\u0CC0': 'ī',
        '\u0CC1': 'u', '\u0CC2': 'ū', '\u0CC3': 'r̥', '\u0CC4': 'r̥̄',
        '\u0CC6': 'e', '\u0CC7': 'ē', '\u0CC8': 'ai',
        '\u0CCA': 'o', '\u0CCB': 'ō', '\u0CCC': 'au',
        '\u0C85': 'a', '\u0C86': 'ā', '\u0C87': 'i', '\u0C88': 'ī',
        '\u0C89': 'u', '\u0C8A': 'ū', '\u0C8B': 'r̥', '\u0CE0': 'r̥̄',
        '\u0C8C': 'l̥', '\u0CE1': 'l̥̄',
        '\u0C8E': 'e', '\u0C8F': 'ē', '\u0C90': 'ai',
        '\u0C92': 'o', '\u0C93': 'ō', '\u0C94': 'au',
        '\u0C82': 'ṁ', '\u0C83': 'ḥ', '\u0C81': 'm̐',
        '\u0C95': 'k', '\u0C96': 'kh', '\u0C97': 'g', '\u0C98': 'gh', '\u0C99': 'ṅ',
        '\u0C9A': 'c', '\u0C9B': 'ch', '\u0C9C': 'j', '\u0C9D': 'jh', '\u0C9E': 'ñ',
        '\u0C9F': 'ṭ', '\u0CA0': 'ṭh', '\u0CA1': 'ḍ', '\u0CA2': 'ḍh', '\u0CA3': 'ṇ',
        '\u0CA4': 't', '\u0CA5': 'th', '\u0CA6': 'd', '\u0CA7': 'dh', '\u0CA8': 'n',
        '\u0CAA': 'p', '\u0CAB': 'ph', '\u0CAC': 'b', '\u0CAD': 'bh', '\u0CAE': 'm',
        '\u0CAF': 'y', '\u0CB0': 'r', '\u0CB2': 'l', '\u0CB5': 'v',
        '\u0CB6': 'ś', '\u0CB7': 'ṣ', '\u0CB8': 's', '\u0CB9': 'h',
        '\u0CB3': 'ḷ', '\u0CB4': 'ḻ', '\u0CB1': 'ṟ',
    },
    # Telugu supplements
    'telugu': {
        '\u0C4D': '',
        '\u0C3E': 'ā', '\u0C3F': 'i', '\u0C40': 'ī',
        '\u0C41': 'u', '\u0C42': 'ū', '\u0C43': 'r̥', '\u0C44': 'r̥̄',
        '\u0C46': 'e', '\u0C47': 'ē', '\u0C48': 'ai',
        '\u0C4A': 'o', '\u0C4B': 'ō', '\u0C4C': 'au',
        '\u0C05': 'a', '\u0C06': 'ā', '\u0C07': 'i', '\u0C08': 'ī',
        '\u0C09': 'u', '\u0C0A': 'ū', '\u0C0B': 'r̥', '\u0C60': 'r̥̄',
        '\u0C0E': 'e', '\u0C0F': 'ē', '\u0C10': 'ai',
        '\u0C12': 'o', '\u0C13': 'ō', '\u0C14': 'au',
        '\u0C02': 'ṁ', '\u0C03': 'ḥ', '\u0C01': 'm̐',
        '\u0C15': 'k', '\u0C16': 'kh', '\u0C17': 'g', '\u0C18': 'gh', '\u0C19': 'ṅ',
        '\u0C1A': 'c', '\u0C1B': 'ch', '\u0C1C': 'j', '\u0C1D': 'jh', '\u0C1E': 'ñ',
        '\u0C1F': 'ṭ', '\u0C20': 'ṭh', '\u0C21': 'ḍ', '\u0C22': 'ḍh', '\u0C23': 'ṇ',
        '\u0C24': 't', '\u0C25': 'th', '\u0C26': 'd', '\u0C27': 'dh', '\u0C28': 'n',
        '\u0C2A': 'p', '\u0C2B': 'ph', '\u0C2C': 'b', '\u0C2D': 'bh', '\u0C2E': 'm',
        '\u0C2F': 'y', '\u0C30': 'r', '\u0C32': 'l', '\u0C35': 'v',
        '\u0C36': 'ś', '\u0C37': 'ṣ', '\u0C38': 's', '\u0C39': 'h',
        '\u0C33': 'ḷ',
    },
    # Tamil supplements
    'tamil': {
        '\u0BCD': '',
        '\u0BBE': 'ā', '\u0BBF': 'i', '\u0BC0': 'ī',
        '\u0BC1': 'u', '\u0BC2': 'ū',
        '\u0BC6': 'e', '\u0BC7': 'ē', '\u0BC8': 'ai',
        '\u0BCA': 'o', '\u0BCB': 'ō', '\u0BCC': 'au',
        '\u0B85': 'a', '\u0B86': 'ā', '\u0B87': 'i', '\u0B88': 'ī',
        '\u0B89': 'u', '\u0B8A': 'ū',
        '\u0B8E': 'e', '\u0B8F': 'ē', '\u0B90': 'ai',
        '\u0B92': 'o', '\u0B93': 'ō', '\u0B94': 'au',
        '\u0B82': 'ṁ', '\u0B83': 'ḥ',
        '\u0B95': 'k', '\u0B99': 'ṅ', '\u0B9A': 'c', '\u0B9C': 'j', '\u0B9E': 'ñ',
        '\u0B9F': 'ṭ', '\u0BA3': 'ṇ', '\u0BA4': 't', '\u0BA8': 'n', '\u0BA9': 'ṉ',
        '\u0BAA': 'p', '\u0BAE': 'm',
        '\u0BAF': 'y', '\u0BB0': 'r', '\u0BB2': 'l', '\u0BB5': 'v',
        '\u0BB6': 'ś', '\u0BB7': 'ṣ', '\u0BB8': 's', '\u0BB9': 'h',
        '\u0BB3': 'ḷ', '\u0BB4': 'ḻ', '\u0BB1': 'ṟ',
    },
}

# Add similar supplements for other scripts (offset-based from Devanagari)
_SCRIPT_OFFSETS = {
    'malayalam': 0x0D00 - 0x0900,
    'bengali':   0x0980 - 0x0900,
    'gujarati':  0x0A80 - 0x0900,
    'punjabi':   0x0A00 - 0x0900,
    'odia':      0x0B00 - 0x0900,
}


def _get_iso15919_supplements(lang):
    """Get ISO 15919 supplement mappings for a language."""
    if lang in _ISO15919_SUPPLEMENTS:
        return _ISO15919_SUPPLEMENTS[lang]
    # For Hindi/Marathi/Sanskrit, use Devanagari
    if lang in ('hindi', 'marathi', 'sanskrit'):
        return _ISO15919_SUPPLEMENTS['devanagari']
    # For Assamese, use Bengali
    if lang == 'assamese':
        base = _ISO15919_SUPPLEMENTS.get('bengali')
        if not base:
            base = _generate_offset_supplements('bengali')
        return base
    # For scripts with known offset, generate from Devanagari
    if lang in _SCRIPT_OFFSETS:
        return _generate_offset_supplements(lang)
    return {}


def _generate_offset_supplements(lang):
    """Generate ISO 15919 supplements by offsetting from Devanagari."""
    offset = _SCRIPT_OFFSETS.get(lang, 0)
    if not offset:
        return {}
    deva = _ISO15919_SUPPLEMENTS['devanagari']
    result = {}
    for ch, rom in deva.items():
        cp = ord(ch)
        if 0x0900 <= cp <= 0x097F:
            target_cp = cp + offset
            try:
                target_ch = chr(target_cp)
                result[target_ch] = rom
            except (ValueError, OverflowError):
                pass
    return result


# Pre-generate for offset-based scripts
for _lang in _SCRIPT_OFFSETS:
    _ISO15919_SUPPLEMENTS[_lang] = _generate_offset_supplements(_lang)


# ============================================================
# ANSI MAP LOADING (data-driven, from core/data/ansi_maps/)
# ============================================================

# Backward-compatible module-level references.
# These are lazy-loaded on first access so that the old test
# imports (e.g. ``from transliteration import _ANSI_KANNADA``)
# and any legacy code continue to work.

def _load_compat_ansi_map(lang):
    """Load an ANSI map from JSON for backward compatibility."""
    path = _data_path('ansi_maps', f'{lang}.json')
    if os.path.exists(path):
        data = _load_json(path)
        return data.get('unicode_to_ansi', {})
    return {}


class _LazyAnsiMap:
    """Descriptor that loads the ANSI map on first access."""
    def __init__(self, lang):
        self._lang = lang
        self._data = None

    def _load(self):
        if self._data is None:
            self._data = _load_compat_ansi_map(self._lang)
        return self._data

    # dict-like interface used by existing code / tests
    def get(self, key, default=None):
        return self._load().get(key, default)

    def items(self):
        return self._load().items()

    def keys(self):
        return self._load().keys()

    def values(self):
        return self._load().values()

    def __contains__(self, key):
        return key in self._load()

    def __getitem__(self, key):
        return self._load()[key]

    def __iter__(self):
        return iter(self._load())

    def __len__(self):
        return len(self._load())

    def __bool__(self):
        return bool(self._load())

    def __eq__(self, other):
        if isinstance(other, dict):
            return self._load() == other
        return NotImplemented


_ANSI_KANNADA = _LazyAnsiMap('kannada')
_ANSI_HINDI = _LazyAnsiMap('hindi')


# ============================================================
# MODULE-LEVEL CONVENIENCE
# ============================================================

# Alias for backward compatibility with old transliteration.py
LANGUAGES = SUPPORTED_LANGUAGES
