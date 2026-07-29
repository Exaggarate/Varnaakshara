#!/usr/bin/env python3
"""
Generate unified JSON data files for Varnaakshara IME from:
  1. Baraha RE extracted data files
  2. Existing hardcoded transliteration.py tables

Output goes to core/data/{phonetic_rules,unicode_maps,keyboard_layouts,collation,iso15919,braille,font_conversion}/
"""

import json
import os
import sys
import copy

BARAHA_RE_DIR = os.path.join(os.path.dirname(__file__), '..', 'baraha-re')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'core', 'data')

# ============================================================
# Language mapping: our names -> Baraha file names
# ============================================================
LANG_MAP = {
    'kannada':   {'phonetic': 'kannada_phonetic.json',   'brh': 'kannada.json',   'kb': 'kannada.json',   'coll': 'kannada_collcode.json',   'iso': 'brh_kannada_iso15919.json',   'braille': 'kannada_braille.json'},
    'hindi':     {'phonetic': 'devanagari_phonetic.json', 'brh': 'devanagari.json', 'kb': 'devanagari.json', 'coll': 'devanagari_collcode.json', 'iso': 'brh_devanagari_iso15919.json', 'braille': 'devanagari_braille.json'},
    'telugu':    {'phonetic': 'telugu_phonetic.json',    'brh': 'telugu.json',    'kb': 'telugu.json',    'coll': 'telugu_collcode.json',    'iso': 'brh_telugu_iso15919.json',    'braille': 'telugu_braille.json'},
    'tamil':     {'phonetic': 'tamil_phonetic.json',     'brh': 'tamil.json',     'kb': 'tamil.json',     'coll': 'tamil_collcode.json',     'iso': 'brh_tamil_iso15919.json',     'braille': 'tamil_braille.json'},
    'malayalam': {'phonetic': 'malayalam_phonetic.json', 'brh': 'malayalam.json', 'kb': 'malayalam.json', 'coll': 'malayalam_collcode.json', 'iso': 'brh_malayalam_iso15919.json', 'braille': 'malayalam_braille.json'},
    'bengali':   {'phonetic': 'bengali_phonetic.json',   'brh': 'bengali.json',   'kb': 'bengali.json',   'coll': 'bengali_collcode.json',   'iso': 'brh_bengali_iso15919.json',   'braille': 'bengali_braille.json'},
    'gujarati':  {'phonetic': 'gujarati_phonetic.json',  'brh': 'gujarati.json',  'kb': 'gujarati.json',  'coll': 'gujarati_collcode.json',  'iso': 'brh_gujarati_iso15919.json',  'braille': 'gujarati_braille.json'},
    'punjabi':   {'phonetic': 'gurumukhi_phonetic.json', 'brh': 'gurumukhi.json', 'kb': 'gurumukhi.json', 'coll': 'gurumukhi_collcode.json', 'iso': 'brh_gurmukhi_iso15919.json', 'braille': 'gurmukhi_braille.json'},
    'odia':      {'phonetic': 'oriya_phonetic.json',     'brh': 'oriya.json',     'kb': 'oriya.json',     'coll': 'oriya_collcode.json',     'iso': 'brh_oriya_iso15919.json',     'braille': 'oriya_braille.json'},
}

# Marathi, Sanskrit, Assamese share Devanagari/Bengali base
DERIVED_LANGS = {
    'marathi':  'hindi',
    'sanskrit': 'hindi',
    'assamese': 'bengali',
}

# ============================================================
# Unicode block ranges for scripts (for deriving Devanagari offsets)
# ============================================================
SCRIPT_BLOCKS = {
    'devanagari': 0x0900,
    'bengali':    0x0980,
    'gurmukhi':   0x0A00,
    'gujarati':   0x0A80,
    'odia':       0x0B00,
    'tamil':      0x0B80,
    'telugu':     0x0C00,
    'kannada':    0x0C80,
    'malayalam':  0x0D00,
}

def hex_to_chr(hex_str):
    """Convert '0x0C85' or 'U+0C85' to character."""
    s = hex_str.strip()
    if s.startswith('U+') or s.startswith('u+'):
        return chr(int(s[2:], 16))
    elif s.startswith('0x') or s.startswith('0X'):
        return chr(int(s[2:], 16))
    else:
        return chr(int(s, 16))

def hex_to_int(hex_str):
    s = hex_str.strip()
    if s.startswith('U+') or s.startswith('u+'):
        return int(s[2:], 16)
    elif s.startswith('0x') or s.startswith('0X'):
        return int(s[2:], 16)
    else:
        return int(s, 16)

def normalize_brhcode(code):
    """Normalize brhcode key: preserve 0x prefix, uppercase hex digits."""
    s = code.strip()
    if s.startswith('0x') or s.startswith('0X'):
        return '0x' + s[2:].upper()
    return s

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'  Written: {path}')


# ============================================================
# HARDCODED TABLES FROM transliteration.py (imported directly)
# ============================================================
# We import these to merge with Baraha RE data
sys.path.insert(0, os.path.dirname(__file__))
from transliteration import (
    BARAHA_VOWELS, BARAHA_VOWEL_SIGNS, BARAHA_CONSONANTS,
    BARAHA_YOGAVAAHAS, BARAHA_SYMBOLS, BARAHA_DIGITS,
    ITRANS_VOWELS, ITRANS_VOWEL_SIGNS, ITRANS_CONSONANTS,
    ITRANS_YOGAVAAHAS, ITRANS_SYMBOLS,
    DEVA_TO_KANNADA, DEVA_TO_TELUGU, DEVA_TO_TAMIL,
    DEVA_TO_MALAYALAM, DEVA_TO_BENGALI, DEVA_TO_GUJARATI,
    DEVA_TO_GURMUKHI, DEVA_TO_ODIA,
    LANGUAGES,
)


def generate_phonetic_rules(lang, files):
    """Generate merged phonetic rules JSON for a language."""
    print(f'  Generating phonetic rules for {lang}...')

    # Load Baraha RE phonetic rules
    baraha_path = os.path.join(BARAHA_RE_DIR, 'phonetic_rules', files['phonetic'])
    baraha_data = load_json(baraha_path)

    # Extract clean rules from Baraha RE
    baraha_rules = {}
    for rule in baraha_data.get('rules', []):
        inp = rule.get('input', '')
        uni = rule.get('unicode', '')
        note = rule.get('note', '')
        if not inp or not uni or note not in ('vowel', 'consonant'):
            continue
        # Parse unicode codepoints (may be "U+0C85" or "U+0C95 U+0CCD")
        codepoints = uni.split()
        try:
            chars = ''.join(hex_to_chr(cp) for cp in codepoints)
        except (ValueError, OverflowError):
            continue
        baraha_rules[inp] = {
            'unicode': chars,
            'type': note,
        }

    # Build the output phonetic rules
    # For Devanagari-based scripts, we use the existing hardcoded Baraha tables as canonical
    # For non-Devanagari scripts, the Baraha RE rules give us direct script mappings

    # Determine if this is a Devanagari-based language
    is_devanagari = lang in ('hindi', 'marathi', 'sanskrit')

    # Build Baraha scheme tables from existing hardcoded data
    baraha_scheme = {
        'vowels': {k: _char_to_codepoints(v) for k, v in BARAHA_VOWELS.items()},
        'vowel_signs': {k: _char_to_codepoints(v) for k, v in BARAHA_VOWEL_SIGNS.items()},
        'consonants': {k: _char_to_codepoints(v) for k, v in BARAHA_CONSONANTS.items()},
        'yogavaahas': {k: _char_to_codepoints(v) for k, v in BARAHA_YOGAVAAHAS.items()},
        'symbols': {k: _char_to_codepoints(v) for k, v in BARAHA_SYMBOLS.items()},
        'digits': {k: _char_to_codepoints(v) for k, v in BARAHA_DIGITS.items()},
    }

    itrans_scheme = {
        'vowels': {k: _char_to_codepoints(v) for k, v in ITRANS_VOWELS.items()},
        'vowel_signs': {k: _char_to_codepoints(v) for k, v in ITRANS_VOWEL_SIGNS.items()},
        'consonants': {k: _char_to_codepoints(v) for k, v in ITRANS_CONSONANTS.items()},
        'yogavaahas': {k: _char_to_codepoints(v) for k, v in ITRANS_YOGAVAAHAS.items()},
        'symbols': {k: _char_to_codepoints(v) for k, v in ITRANS_SYMBOLS.items()},
        'digits': {k: _char_to_codepoints(v) for k, v in BARAHA_DIGITS.items()},
    }

    # Merge any additional rules from Baraha RE that we don't already have
    baraha_re_extra = {}
    for inp, info in baraha_rules.items():
        if info['type'] == 'vowel':
            if inp not in BARAHA_VOWELS and inp not in BARAHA_YOGAVAAHAS:
                baraha_re_extra[inp] = info
        elif info['type'] == 'consonant':
            if inp not in BARAHA_CONSONANTS:
                baraha_re_extra[inp] = info

    output = {
        'language': lang,
        'baraha_re_source': files['phonetic'],
        'schemes': {
            'baraha': baraha_scheme,
            'itrans': itrans_scheme,
        },
        'baraha_re_rules': {k: v['unicode'] for k, v in baraha_rules.items()},
    }

    if baraha_re_extra:
        output['baraha_re_extra'] = {k: v['unicode'] for k, v in baraha_re_extra.items()}

    return output


def _char_to_codepoints(s):
    """Convert a string to a list of U+XXXX codepoint strings."""
    if not s:
        return ''
    return s  # Store as actual Unicode string


def generate_unicode_maps(lang, files):
    """Generate Devanagari → target script mapping table."""
    print(f'  Generating unicode maps for {lang}...')

    # Get the script map from existing hardcoded tables
    script_maps = {
        'kannada': DEVA_TO_KANNADA,
        'telugu': DEVA_TO_TELUGU,
        'tamil': DEVA_TO_TAMIL,
        'malayalam': DEVA_TO_MALAYALAM,
        'bengali': DEVA_TO_BENGALI,
        'gujarati': DEVA_TO_GUJARATI,
        'punjabi': DEVA_TO_GURMUKHI,
        'odia': DEVA_TO_ODIA,
    }

    lang_info = LANGUAGES.get(lang, {})
    script_map = lang_info.get('script_map', {})

    # Load Baraha RE BrhCode table for additional info
    brh_path = os.path.join(BARAHA_RE_DIR, 'brhcode_tables', files['brh'])
    brh_data = load_json(brh_path)

    # Build the unicode map with readable keys
    unicode_map = {}
    for deva_char, target_char in script_map.items():
        deva_cp = f'U+{ord(deva_char):04X}'
        if len(target_char) == 1:
            target_cp = f'U+{ord(target_char):04X}'
        else:
            target_cp = ' '.join(f'U+{ord(c):04X}' for c in target_char)
        unicode_map[deva_char] = target_char

    output = {
        'language': lang,
        'unicode_block': brh_data.get('unicode_block', ''),
        'devanagari_to_target': unicode_map,
    }

    return output


def generate_keyboard_layouts(lang, files):
    """Generate keyboard layout JSON from Baraha RE data."""
    print(f'  Generating keyboard layouts for {lang}...')

    kb_path = os.path.join(BARAHA_RE_DIR, 'keyboard_layouts', files['kb'])
    kb_data = load_json(kb_path)

    # Load brhcode table to resolve brhcode -> unicode
    brh_path = os.path.join(BARAHA_RE_DIR, 'brhcode_tables', files['brh'])
    brh_data = load_json(brh_path)
    brh_to_uni = brh_data.get('brhcode_to_unicode', {})

    def resolve_brh(brhcode):
        """Resolve a brhcode to Unicode character(s)."""
        brhcode_norm = normalize_brhcode(brhcode)
        if brhcode_norm in brh_to_uni:
            try:
                return ''.join(hex_to_chr(u) for u in brh_to_uni[brhcode_norm])
            except (ValueError, OverflowError):
                return None
        if brhcode in brh_to_uni:
            try:
                return ''.join(hex_to_chr(u) for u in brh_to_uni[brhcode])
            except (ValueError, OverflowError):
                return None
        return None

    # Process INSCRIPT layout
    inscript = {}
    for layer_name, layer_map in kb_data.get('inscript', {}).items():
        resolved = {}
        for key, brhcode in layer_map.items():
            uni = resolve_brh(brhcode)
            if uni:
                resolved[key] = uni
        inscript[layer_name] = resolved

    # Process Baraha keyboard layout if present
    baraha_kb = {}
    for layer_name in ('baraha', 'brhkbd'):
        if layer_name in kb_data:
            for sub_layer, layer_map in kb_data[layer_name].items():
                resolved = {}
                for key, brhcode in layer_map.items():
                    uni = resolve_brh(brhcode)
                    if uni:
                        resolved[key] = uni
                baraha_kb[sub_layer] = resolved

    output = {
        'language': lang,
        'source': files['kb'],
        'inscript': inscript,
    }
    if baraha_kb:
        output['baraha_keyboard'] = baraha_kb

    return output


def generate_collation(lang, files):
    """Generate collation/sorting table JSON."""
    print(f'  Generating collation for {lang}...')

    coll_path = os.path.join(BARAHA_RE_DIR, 'collcode_tables', files['coll'])
    coll_data = load_json(coll_path)

    # Load brhcode table to resolve to Unicode
    brh_path = os.path.join(BARAHA_RE_DIR, 'brhcode_tables', files['brh'])
    brh_data = load_json(brh_path)
    brh_to_uni = brh_data.get('brhcode_to_unicode', {})

    # Build unicode -> collation_key map
    brh_to_coll = coll_data.get('brhcode_to_collcode', {})
    unicode_collation = {}

    for brhcode, collcode in brh_to_coll.items():
        brhcode_norm = normalize_brhcode(brhcode)
        if brhcode_norm in brh_to_uni:
            unis = brh_to_uni[brhcode_norm]
            try:
                uni_str = ''.join(hex_to_chr(u) for u in unis)
                coll_val = hex_to_int(collcode)
                unicode_collation[uni_str] = coll_val
            except (ValueError, OverflowError):
                continue

    output = {
        'language': lang,
        'source': files['coll'],
        'collcode_prefix': coll_data.get('collcode_prefix', ''),
        'unicode_to_collcode': unicode_collation,
        'brhcode_to_collcode': brh_to_coll,  # Keep raw too
    }

    return output


def generate_iso15919(lang, files):
    """Generate ISO 15919 romanization table."""
    print(f'  Generating ISO 15919 for {lang}...')

    iso_path = os.path.join(BARAHA_RE_DIR, 'iso15919_tables', files['iso'])
    iso_data = load_json(iso_path)

    brh_path = os.path.join(BARAHA_RE_DIR, 'brhcode_tables', files['brh'])
    brh_data = load_json(brh_path)
    brh_to_uni = brh_data.get('brhcode_to_unicode', {})

    brh_to_rom = iso_data.get('brhcode_to_romanization', {})

    # Build unicode -> romanization map
    unicode_to_iso = {}
    for brhcode, rom in brh_to_rom.items():
        if rom is None:
            continue
        brhcode_norm = normalize_brhcode(brhcode)
        if brhcode_norm in brh_to_uni:
            unis = brh_to_uni[brhcode_norm]
            try:
                uni_str = ''.join(hex_to_chr(u) for u in unis)
                unicode_to_iso[uni_str] = rom
            except (ValueError, OverflowError):
                continue

    output = {
        'language': lang,
        'standard': 'ISO 15919',
        'source': files['iso'],
        'unicode_to_romanization': unicode_to_iso,
    }

    return output


def generate_braille(lang, files):
    """Generate Braille table JSON."""
    print(f'  Generating braille for {lang}...')

    br_path = os.path.join(BARAHA_RE_DIR, 'braille_tables', files['braille'])
    br_data = load_json(br_path)

    brh_path = os.path.join(BARAHA_RE_DIR, 'brhcode_tables', files['brh'])
    brh_data = load_json(brh_path)
    brh_to_uni = brh_data.get('brhcode_to_unicode', {})

    # Build unicode -> braille mapping
    unicode_to_braille = {}
    tables = br_data.get('tables', {})

    for section_name, section in tables.items():
        for brhcode, info in section.items():
            braille_uni = info.get('braille_unicode', '')
            if not braille_uni:
                continue
            # Resolve brhcode to unicode
            brhcode_norm = normalize_brhcode(brhcode)
            if brhcode_norm in brh_to_uni:
                unis = brh_to_uni[brhcode_norm]
                try:
                    uni_str = ''.join(hex_to_chr(u) for u in unis)
                except (ValueError, OverflowError):
                    continue
                unicode_to_braille[uni_str] = {
                    'braille': braille_uni,
                    'dots': info.get('braille_dots', ''),
                    'name': info.get('name', ''),
                }

    output = {
        'language': lang,
        'type': br_data.get('type', 'Bharati Braille'),
        'source': files['braille'],
        'unicode_to_braille': unicode_to_braille,
    }

    return output


def generate_font_conversion():
    """Generate font conversion JSON files."""
    print('  Generating font conversion tables...')

    fc_dir = os.path.join(BARAHA_RE_DIR, 'font_conversion_tables')
    output_dir = os.path.join(OUTPUT_DIR, 'font_conversion')
    os.makedirs(output_dir, exist_ok=True)

    for fname in sorted(os.listdir(fc_dir)):
        if not fname.endswith('.json') or fname == 'summary.json':
            continue
        fc_path = os.path.join(fc_dir, fname)
        fc_data = load_json(fc_path)

        source_font = fc_data.get('source_font', '')
        target_font = fc_data.get('target_font', '')

        # Build clean mapping
        mappings = {}
        for entry in fc_data.get('mappings', []):
            src = entry.get('source', '')
            tgt = entry.get('target', '')
            if src and tgt:
                mappings[src] = tgt

        output = {
            'source_font': source_font,
            'target_font': target_font,
            'source_file': fname,
            'mappings': mappings,
        }

        # Name the output file from the source/target pair
        out_name = fname
        save_json(os.path.join(output_dir, out_name), output)


def generate_derived_lang(lang, base_lang):
    """Generate data files for derived languages (marathi, sanskrit, assamese)."""
    print(f'  Generating derived language data for {lang} (based on {base_lang})...')

    base_dir = os.path.join(OUTPUT_DIR, 'phonetic_rules')
    base_path = os.path.join(base_dir, f'{base_lang}.json')
    if os.path.exists(base_path):
        data = load_json(base_path)
        data['language'] = lang
        data['derived_from'] = base_lang
        save_json(os.path.join(base_dir, f'{lang}.json'), data)

    # Unicode maps
    lang_info = LANGUAGES.get(lang, {})
    script_map = lang_info.get('script_map', {})
    output = {
        'language': lang,
        'derived_from': base_lang,
        'devanagari_to_target': {k: v for k, v in script_map.items()},
    }
    save_json(os.path.join(OUTPUT_DIR, 'unicode_maps', f'{lang}.json'), output)

    # For collation, iso15919, braille, keyboard - copy from base
    for subdir in ('collation', 'iso15919', 'braille', 'keyboard_layouts'):
        base_file = os.path.join(OUTPUT_DIR, subdir, f'{base_lang}.json')
        if os.path.exists(base_file):
            data = load_json(base_file)
            data['language'] = lang
            data['derived_from'] = base_lang
            save_json(os.path.join(OUTPUT_DIR, subdir, f'{lang}.json'), data)


def main():
    print('=== Generating Varnaakshara IME Data Files ===\n')

    # Ensure output directories exist
    for subdir in ('phonetic_rules', 'unicode_maps', 'keyboard_layouts',
                   'collation', 'iso15919', 'braille', 'font_conversion'):
        os.makedirs(os.path.join(OUTPUT_DIR, subdir), exist_ok=True)

    # Generate data for each primary language
    for lang, files in LANG_MAP.items():
        print(f'\n--- {lang.upper()} ---')

        # Phonetic rules
        data = generate_phonetic_rules(lang, files)
        save_json(os.path.join(OUTPUT_DIR, 'phonetic_rules', f'{lang}.json'), data)

        # Unicode maps
        data = generate_unicode_maps(lang, files)
        save_json(os.path.join(OUTPUT_DIR, 'unicode_maps', f'{lang}.json'), data)

        # Keyboard layouts
        data = generate_keyboard_layouts(lang, files)
        save_json(os.path.join(OUTPUT_DIR, 'keyboard_layouts', f'{lang}.json'), data)

        # Collation
        data = generate_collation(lang, files)
        save_json(os.path.join(OUTPUT_DIR, 'collation', f'{lang}.json'), data)

        # ISO 15919
        data = generate_iso15919(lang, files)
        save_json(os.path.join(OUTPUT_DIR, 'iso15919', f'{lang}.json'), data)

        # Braille
        data = generate_braille(lang, files)
        save_json(os.path.join(OUTPUT_DIR, 'braille', f'{lang}.json'), data)

    # Generate derived languages
    print('\n--- DERIVED LANGUAGES ---')
    for lang, base in DERIVED_LANGS.items():
        generate_derived_lang(lang, base)

    # Font conversion tables
    print('\n--- FONT CONVERSION ---')
    generate_font_conversion()

    print('\n=== Done! ===')


if __name__ == '__main__':
    main()
