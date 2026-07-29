#!/usr/bin/env python3
"""
Generate Unicode ↔ ANSI (Baraha BrhCode) conversion maps for all 12 Indian languages,
plus Shreelipi maps where conversion tables exist.

Strategy:
1. Build a canonical Devanagari → BrhCode map from the hardcoded _ANSI_HINDI + _ANSI_KANNADA
2. For each language, use unicode_maps/<lang>.json to map Devanagari → target script
3. Chain: Target Unicode ← Devanagari → BrhCode  ⟹  Target Unicode → BrhCode
4. For Shreelipi: reverse font_conversion tables, chain Unicode → BrhCode → Shreelipi bytes
"""

import json
import os
import sys
from collections import OrderedDict
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.dirname(BASE_DIR)  # core/data/
UNICODE_MAPS_DIR = os.path.join(DATA_DIR, "unicode_maps")
FONT_CONV_DIR = os.path.join(DATA_DIR, "font_conversion")
OUTPUT_DIR = BASE_DIR
SHREELIPI_DIR = os.path.join(OUTPUT_DIR, "shreelipi")

LANGUAGES = [
    "kannada", "hindi", "telugu", "tamil", "malayalam", "marathi",
    "sanskrit", "bengali", "assamese", "gujarati", "punjabi", "odia"
]

# ============================================================
# CANONICAL DEVANAGARI → BrhCode MAP
# ============================================================
# Built from the hardcoded maps in transliteration.py
# Hindi map is the primary source; Kannada fills in short vowels

# From _ANSI_HINDI (transliteration.py lines ~1148-1169)
_CANONICAL_DEVA_TO_BRH = {
    # Independent vowels
    '\u0905': 'A',    # अ
    '\u0906': 'Aa',   # आ
    '\u0907': 'I',    # इ
    '\u0908': 'Ii',   # ई
    '\u0909': 'U',    # उ
    '\u090A': 'Uu',   # ऊ
    '\u090B': 'Ru',   # ऋ
    '\u090E': 'E',    # ऎ (short e - from Kannada map, not in standard Hindi)
    '\u090F': 'Ee',   # ए
    '\u0910': 'Ai',   # ऐ
    '\u0912': 'O',    # ऒ (short o - from Kannada map, not in standard Hindi)
    '\u0913': 'Oo',   # ओ
    '\u0914': 'Au',   # औ

    # Consonants
    '\u0915': 'k',    # क
    '\u0916': 'K',    # ख
    '\u0917': 'g',    # ग
    '\u0918': 'G',    # घ
    '\u0919': '|',    # ङ
    '\u091A': 'c',    # च
    '\u091B': 'C',    # छ
    '\u091C': 'j',    # ज
    '\u091D': 'J',    # झ
    '\u091E': '~',    # ञ
    '\u091F': 'q',    # ट
    '\u0920': 'Q',    # ठ
    '\u0921': 'w',    # ड
    '\u0922': 'W',    # ढ
    '\u0923': 'N',    # ण
    '\u0924': 't',    # त
    '\u0925': 'T',    # थ
    '\u0926': 'd',    # द
    '\u0927': 'D',    # ध
    '\u0928': 'n',    # न
    '\u092A': 'p',    # प
    '\u092B': 'P',    # फ
    '\u092C': 'b',    # ब
    '\u092D': 'B',    # भ
    '\u092E': 'm',    # म
    '\u092F': 'y',    # य
    '\u0930': 'r',    # र
    '\u0932': 'l',    # ल
    '\u0933': 'L',    # ळ
    '\u0935': 'v',    # व
    '\u0936': 'S',    # श
    '\u0937': 'x',    # ष
    '\u0938': 's',    # स
    '\u0939': 'h',    # ह

    # Dependent vowel signs (matras)
    '\u093E': 'a',    # ा
    '\u093F': 'i',    # ि
    '\u0940': 'ii',   # ी
    '\u0941': 'u',    # ु
    '\u0942': 'uu',   # ू
    '\u0943': 'R',    # ृ
    '\u0946': 'e',    # ॆ (short e matra - from Kannada/Telugu/Tamil)
    '\u0947': 'ee',   # े
    '\u0948': 'Y',    # ै
    '\u094A': 'o',    # ॊ (short o matra - from Kannada/Telugu)
    '\u094B': 'oo',   # ो
    '\u094C': 'ou',   # ौ

    # Signs
    '\u094D': '\\',   # ् (virama/halant)
    '\u0902': 'M',    # ं (anusvara)
    '\u0903': 'H',    # ः (visarga)
    '\u0901': 'z',    # ँ (chandrabindu)

    # Vocalic R long
    '\u0960': 'RU',   # ॠ
    '\u0944': 'RR',   # ॄ (matra form)

    # Nukta consonants (map to base + nukta marker)
    '\u0958': 'k&',   # क़
    '\u0959': 'K&',   # ख़
    '\u095A': 'g&',   # ग़
    '\u095B': 'j&',   # ज़
    '\u095C': 'w&',   # ड़
    '\u095D': 'W&',   # ढ़
    '\u095E': 'P&',   # फ़
    '\u095F': 'y&',   # य़

    # Digits
    '\u0966': '0',    # ०
    '\u0967': '1',    # १
    '\u0968': '2',    # २
    '\u0969': '3',    # ३
    '\u096A': '4',    # ४
    '\u096B': '5',    # ५
    '\u096C': '6',    # ६
    '\u096D': '7',    # ७
    '\u096E': '8',    # ८
    '\u096F': '9',    # ९

    # Punctuation
    '\u0964': '.',    # । (danda)
    '\u0965': '..',   # ॥ (double danda)
    '\u093D': '&',    # ऽ (avagraha)

    # Additional vowels
    '\u090C': 'Lu',   # ऌ (vocalic L)
    '\u0961': 'LU',   # ॡ (vocalic L long)
    '\u0962': 'lR',   # ॢ (matra vocalic L)
    '\u0963': 'lRR',  # ॣ (matra vocalic L long)

    # Additional consonants
    '\u0929': 'nq',   # ऩ (na with nukta)
    '\u0931': 'rq',   # ऱ (ra with nukta)
    '\u0934': 'Lq',   # ऴ (retroflex L / zha)
}


def load_unicode_map(lang):
    """Load devanagari_to_target mapping for a language."""
    fpath = os.path.join(UNICODE_MAPS_DIR, f"{lang}.json")
    if not os.path.exists(fpath):
        return {}, None
    with open(fpath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('devanagari_to_target', {}), data.get('derived_from')


def build_baraha_map(lang):
    """Build Unicode ↔ BrhCode map for a given language."""
    deva_to_target, derived_from = load_unicode_map(lang)

    # For Hindi: Devanagari IS the target, use canonical map directly
    if lang == 'hindi':
        unicode_to_ansi = dict(_CANONICAL_DEVA_TO_BRH)
        ansi_to_unicode = {}
        for uni, ansi in unicode_to_ansi.items():
            if ansi not in ansi_to_unicode:  # first mapping wins
                ansi_to_unicode[ansi] = uni
        return unicode_to_ansi, ansi_to_unicode

    # For Marathi/Sanskrit: Devanagari-based, same as Hindi but may have
    # overrides from unicode_maps
    if lang in ('marathi', 'sanskrit'):
        # Start with full Hindi/Devanagari map
        unicode_to_ansi = dict(_CANONICAL_DEVA_TO_BRH)
        # Apply any overrides from the lang's unicode_map
        # (e.g., marathi maps short-e to standard-e)
        if deva_to_target:
            for deva, target in deva_to_target.items():
                if deva in _CANONICAL_DEVA_TO_BRH:
                    brh = _CANONICAL_DEVA_TO_BRH[deva]
                    # The target IS the Unicode char to use for this language
                    # If target differs from deva, add target mapping too
                    if target != deva:
                        unicode_to_ansi[target] = brh
        ansi_to_unicode = {}
        for uni, ansi in unicode_to_ansi.items():
            if ansi not in ansi_to_unicode:
                ansi_to_unicode[ansi] = uni
        return unicode_to_ansi, ansi_to_unicode

    # For all other languages: map via Devanagari
    # Reverse the deva_to_target to get target_to_deva
    target_to_deva = {}
    for deva, target in deva_to_target.items():
        # Skip empty target values (some scripts lack certain chars)
        if not target:
            continue
        # Prefer non-nukta forms (simpler Devanagari) when multiple map to same target
        if target not in target_to_deva:
            target_to_deva[target] = deva

    unicode_to_ansi = {}
    for target_char, deva_char in target_to_deva.items():
        if deva_char in _CANONICAL_DEVA_TO_BRH:
            brh = _CANONICAL_DEVA_TO_BRH[deva_char]
            unicode_to_ansi[target_char] = brh

    # Also do forward: for each Devanagari in canonical, find the target
    for deva_char, brh in _CANONICAL_DEVA_TO_BRH.items():
        if deva_char in deva_to_target:
            target = deva_to_target[deva_char]
            if target and target not in unicode_to_ansi:
                unicode_to_ansi[target] = brh

    # Build reverse
    ansi_to_unicode = {}
    for uni, ansi in unicode_to_ansi.items():
        if ansi not in ansi_to_unicode:
            ansi_to_unicode[ansi] = uni

    return unicode_to_ansi, ansi_to_unicode


def save_baraha_map(lang, unicode_to_ansi, ansi_to_unicode):
    """Save Baraha map as JSON."""
    data = OrderedDict([
        ("language", lang),
        ("encoding", "baraha"),
        ("description", f"Unicode ↔ Baraha BrhCode map for {lang.title()}"),
        ("generated", datetime.now(timezone.utc).isoformat()),
        ("total_mappings", len(unicode_to_ansi)),
        ("unicode_to_ansi", OrderedDict(
            sorted(unicode_to_ansi.items(),
                   key=lambda x: tuple(ord(c) for c in x[0]) if x[0] else (0,))
        )),
        ("ansi_to_unicode", OrderedDict(sorted(ansi_to_unicode.items()))),
    ])
    outpath = os.path.join(OUTPUT_DIR, f"{lang}.json")
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return outpath


# ============================================================
# SHREELIPI GENERATION
# ============================================================

# Font conversion tables that contain Shreelipi or similar ANSI font mappings
SHREELIPI_TABLES = {
    "kannada": [
        ("01_shree_kan_0850_to_brh_kannada.json", "Shree-Kan-0850", "BRH Kannada"),
    ],
    "devanagari": [
        ("05_shree_dev_0709_to_brh_devanagari.json", "Shree-Dev-0709", "BRH Devanagari"),
    ],
}

# Languages that use each font system
FONT_LANG_MAP = {
    "kannada": "kannada",
    "hindi": "devanagari",
    "marathi": "devanagari",
    "sanskrit": "devanagari",
}


def load_font_conversion(filename):
    """Load a font conversion table."""
    fpath = os.path.join(FONT_CONV_DIR, filename)
    if not os.path.exists(fpath):
        return None
    with open(fpath, 'r', encoding='utf-8') as f:
        return json.load(f)


def parse_hex_val(hex_str):
    """Parse '0xHH' or '0xHH+0xHH' into a string of chars."""
    parts = hex_str.split('+')
    chars = []
    for p in parts:
        p = p.strip()
        if p.startswith('0x') or p.startswith('0X'):
            val = int(p, 16)
            if val == 0:
                continue  # skip null
            chars.append(chr(val))
        else:
            chars.append(p)
    return ''.join(chars)


def build_shreelipi_map(lang, baraha_unicode_to_ansi):
    """
    Build Unicode ↔ Shreelipi map.

    Chain: Unicode → BrhCode → Shreelipi byte
    The font_conversion tables map: Shreelipi_byte → BrhCode_byte
    We reverse that to get: BrhCode_byte → Shreelipi_byte
    Then chain with our baraha map: Unicode → BrhCode → Shreelipi
    """
    font_system = FONT_LANG_MAP.get(lang)
    if not font_system:
        return None, None, None, True

    tables = SHREELIPI_TABLES.get(font_system)
    if not tables:
        return None, None, None, True

    filename, source_font, target_font = tables[0]
    conv_data = load_font_conversion(filename)
    if not conv_data:
        return None, None, None, True

    # The conversion table maps: source_hex → target_hex (Shreelipi → BrhCode)
    # We need reverse: BrhCode → Shreelipi
    brh_to_shreelipi = {}
    for src_hex, tgt_hex in conv_data.get('mappings', {}).items():
        try:
            src_chars = parse_hex_val(src_hex)
            tgt_chars = parse_hex_val(tgt_hex)
            if tgt_chars and src_chars:
                # Only use single-char or simple mappings for clean reversal
                if '+' not in tgt_hex:
                    brh_to_shreelipi[tgt_chars] = src_chars
                elif '+' not in src_hex:
                    # Multi-byte BrhCode target, single Shreelipi source
                    brh_to_shreelipi[tgt_chars] = src_chars
        except (ValueError, OverflowError):
            continue

    # Now chain: Unicode → BrhCode(string) → match to BrhCode byte → Shreelipi byte
    # The BrhCode in baraha map is ASCII strings like 'k', 'K', 'Aa'
    # The BrhCode in font table is byte positions in the BRH font
    # These are DIFFERENT representations!
    #
    # The font conversion maps byte positions (0x41='A', 0x6B='k', etc.)
    # The baraha map uses ASCII representations ('k', 'K', 'Aa', etc.)
    # They align when the BrhCode string IS the ASCII character at that byte position
    #
    # For single-char BrhCode values, the ASCII char IS the byte
    # For multi-char values like 'Aa', 'Ii', etc., we need the BRH font byte sequence

    unicode_to_shreelipi = {}
    for uni_char, brh_code in baraha_unicode_to_ansi.items():
        # Try to find Shreelipi equivalent for this BrhCode
        # Single char BrhCode: direct byte lookup
        if len(brh_code) == 1:
            brh_byte = brh_code  # ASCII char
            if brh_byte in brh_to_shreelipi:
                unicode_to_shreelipi[uni_char] = brh_to_shreelipi[brh_byte]
        else:
            # Multi-char BrhCode: try to find matching multi-byte sequence
            brh_bytes = brh_code
            if brh_bytes in brh_to_shreelipi:
                unicode_to_shreelipi[uni_char] = brh_to_shreelipi[brh_bytes]

    shreelipi_to_unicode = {}
    for uni, shree in unicode_to_shreelipi.items():
        if shree not in shreelipi_to_unicode:
            shreelipi_to_unicode[shree] = uni

    return unicode_to_shreelipi, shreelipi_to_unicode, filename, False


def save_shreelipi_map(lang, unicode_to_shreelipi, shreelipi_to_unicode,
                        source_table, needs_table):
    """Save Shreelipi map as JSON."""
    os.makedirs(SHREELIPI_DIR, exist_ok=True)

    data = OrderedDict([
        ("language", lang),
        ("encoding", "shreelipi"),
        ("description", f"Unicode ↔ Shreelipi map for {lang.title()}"),
        ("generated", datetime.now(timezone.utc).isoformat()),
        ("needs_table", needs_table),
    ])

    if needs_table:
        data["note"] = (
            f"No Shreelipi font conversion table available for {lang.title()}. "
            "Requires a Shreelipi→BrhCode conversion table to generate mappings."
        )
        data["unicode_to_shreelipi"] = {}
        data["shreelipi_to_unicode"] = {}
    else:
        data["source_table"] = source_table
        data["total_mappings"] = len(unicode_to_shreelipi)
        data["unicode_to_shreelipi"] = OrderedDict(
            sorted(unicode_to_shreelipi.items(), key=lambda x: ord(x[0][0]))
        )
        data["shreelipi_to_unicode"] = OrderedDict(
            sorted(shreelipi_to_unicode.items(), key=lambda x: ord(x[0][0]))
        )

    outpath = os.path.join(SHREELIPI_DIR, f"{lang}.json")
    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return outpath


# ============================================================
# VALIDATION
# ============================================================

def validate_map(lang, unicode_to_ansi, ansi_to_unicode):
    """Validate bidirectional round-trip and report coverage."""
    issues = []
    round_trip_ok = 0
    round_trip_fail = 0

    # Check: every unicode_to_ansi key should round-trip through ansi_to_unicode
    for uni, ansi in unicode_to_ansi.items():
        if ansi in ansi_to_unicode:
            recovered = ansi_to_unicode[ansi]
            if recovered == uni:
                round_trip_ok += 1
            else:
                # This is expected for many-to-one mappings (e.g., nukta variants)
                round_trip_fail += 1
                issues.append(
                    f"  Round-trip mismatch: U+{ord(uni):04X} ({uni}) → '{ansi}' → "
                    f"U+{ord(recovered):04X} ({recovered})"
                )
        else:
            round_trip_fail += 1
            issues.append(f"  Missing reverse: '{ansi}' not in ansi_to_unicode")

    # Count character categories
    vowels = sum(1 for u in unicode_to_ansi if '\u0900' <= u <= '\u097F' and
                 (('\u0905' <= u <= '\u0914') or ('\u093E' <= u <= '\u094C')))
    consonants = sum(1 for u in unicode_to_ansi if '\u0900' <= u <= '\u097F' and
                     '\u0915' <= u <= '\u0939')

    return {
        'total': len(unicode_to_ansi),
        'reverse_total': len(ansi_to_unicode),
        'round_trip_ok': round_trip_ok,
        'round_trip_fail': round_trip_fail,
        'issues': issues[:10],  # cap at 10
    }


# ============================================================
# MAIN
# ============================================================

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(SHREELIPI_DIR, exist_ok=True)

    report_lines = []
    report_lines.append("# ANSI Map Generation Report")
    report_lines.append(f"\nGenerated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    report_lines.append(f"\nLanguages: {len(LANGUAGES)}")
    report_lines.append("")

    # Summary table
    report_lines.append("## Baraha BrhCode Maps\n")
    report_lines.append("| Language | Unicode→ANSI | ANSI→Unicode | Round-trip OK | Issues |")
    report_lines.append("|----------|-------------|-------------|---------------|--------|")

    all_results = {}
    shreelipi_results = {}

    for lang in LANGUAGES:
        print(f"Generating Baraha map for {lang}...")
        u2a, a2u = build_baraha_map(lang)
        save_baraha_map(lang, u2a, a2u)

        val = validate_map(lang, u2a, a2u)
        all_results[lang] = val
        issue_count = val['round_trip_fail']
        report_lines.append(
            f"| {lang.title():12s} | {val['total']:11d} | {val['reverse_total']:11d} | "
            f"{val['round_trip_ok']:13d} | {issue_count:6d} |"
        )

        # Shreelipi
        print(f"  Generating Shreelipi map for {lang}...")
        u2s, s2u, src_table, needs = build_shreelipi_map(lang, u2a)
        save_shreelipi_map(lang, u2s, s2u, src_table, needs)
        shreelipi_results[lang] = {
            'needs_table': needs,
            'total': len(u2s) if u2s else 0,
            'source': src_table,
        }

    # Shreelipi summary
    report_lines.append("\n## Shreelipi Maps\n")
    report_lines.append("| Language | Status | Mappings | Source Table |")
    report_lines.append("|----------|--------|----------|-------------|")
    for lang in LANGUAGES:
        sr = shreelipi_results[lang]
        if sr['needs_table']:
            report_lines.append(f"| {lang.title():12s} | ⚠️ needs_table | 0 | N/A |")
        else:
            report_lines.append(
                f"| {lang.title():12s} | ✅ generated | {sr['total']} | {sr['source']} |"
            )

    # Detail sections
    report_lines.append("\n## Detailed Validation\n")
    for lang in LANGUAGES:
        val = all_results[lang]
        report_lines.append(f"### {lang.title()}\n")
        report_lines.append(f"- Forward mappings (Unicode→ANSI): {val['total']}")
        report_lines.append(f"- Reverse mappings (ANSI→Unicode): {val['reverse_total']}")
        report_lines.append(f"- Round-trip successes: {val['round_trip_ok']}")
        report_lines.append(f"- Round-trip mismatches: {val['round_trip_fail']}")
        if val['issues']:
            report_lines.append(f"- Issues (showing up to 10):")
            for issue in val['issues']:
                report_lines.append(issue)
        report_lines.append("")

    # Character coverage info
    report_lines.append("## BrhCode Reference\n")
    report_lines.append("The Baraha BrhCode scheme uses ASCII characters to represent")
    report_lines.append("Indian script characters. The same ASCII codes are used across")
    report_lines.append("all languages - only the Unicode codepoints differ per script.\n")
    report_lines.append("### Core mappings:\n")
    report_lines.append("| Category | Example (Devanagari) | BrhCode |")
    report_lines.append("|----------|---------------------|---------|")
    examples = [
        ("Vowel", "अ (U+0905)", "A"),
        ("Vowel", "आ (U+0906)", "Aa"),
        ("Consonant", "क (U+0915)", "k"),
        ("Consonant", "ख (U+0916)", "K"),
        ("Matra", "ा (U+093E)", "a"),
        ("Matra", "ि (U+093F)", "i"),
        ("Sign", "ं (U+0902)", "M"),
        ("Sign", "् (U+094D)", "\\\\"),
    ]
    for cat, ex, brh in examples:
        report_lines.append(f"| {cat} | {ex} | {brh} |")

    report_lines.append("\n## File Manifest\n")
    report_lines.append("### Baraha maps (`core/data/ansi_maps/`)\n")
    for lang in LANGUAGES:
        report_lines.append(f"- `{lang}.json`")
    report_lines.append("\n### Shreelipi maps (`core/data/ansi_maps/shreelipi/`)\n")
    for lang in LANGUAGES:
        sr = shreelipi_results[lang]
        status = "✅" if not sr['needs_table'] else "⚠️ placeholder"
        report_lines.append(f"- `shreelipi/{lang}.json` {status}")

    report_lines.append("\n---\n*Auto-generated by `generate_all.py`*\n")

    # Write report
    report_path = os.path.join(OUTPUT_DIR, "GENERATION_REPORT.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"\nReport written to: {report_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    total_baraha = sum(r['total'] for r in all_results.values())
    total_shreelipi = sum(r['total'] for r in shreelipi_results.values())
    shreelipi_generated = sum(1 for r in shreelipi_results.values() if not r['needs_table'])
    shreelipi_needed = sum(1 for r in shreelipi_results.values() if r['needs_table'])
    print(f"  Baraha maps:    {len(LANGUAGES)} languages, {total_baraha} total mappings")
    print(f"  Shreelipi maps: {shreelipi_generated} generated, {shreelipi_needed} need tables")
    print(f"  Total Shreelipi mappings: {total_shreelipi}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
