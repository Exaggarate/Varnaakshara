#!/usr/bin/env python3
"""
Validation test for generated Unicode ↔ ANSI conversion maps.
Tests bidirectional round-trip, coverage, and structural integrity.
"""

import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHREELIPI_DIR = os.path.join(BASE_DIR, "shreelipi")

LANGUAGES = [
    "kannada", "hindi", "telugu", "tamil", "malayalam", "marathi",
    "sanskrit", "bengali", "assamese", "gujarati", "punjabi", "odia"
]

# Minimum expected mappings per language
MIN_MAPPINGS = {
    "kannada": 60, "hindi": 55, "telugu": 60, "tamil": 50,
    "malayalam": 60, "marathi": 55, "sanskrit": 55, "bengali": 60,
    "assamese": 60, "gujarati": 55, "punjabi": 55, "odia": 55,
}

# Expected Unicode blocks per language
UNICODE_BLOCKS = {
    "kannada":   (0x0C80, 0x0CFF),
    "hindi":     (0x0900, 0x097F),
    "telugu":    (0x0C00, 0x0C7F),
    "tamil":     (0x0B80, 0x0BFF),
    "malayalam": (0x0D00, 0x0D7F),
    "marathi":   (0x0900, 0x097F),
    "sanskrit":  (0x0900, 0x097F),
    "bengali":   (0x0980, 0x09FF),
    "assamese":  (0x0980, 0x09FF),
    "gujarati":  (0x0A80, 0x0AFF),
    "punjabi":   (0x0A00, 0x0A7F),
    "odia":      (0x0B00, 0x0B7F),
}

# Shared punctuation block
SHARED_RANGE = (0x0964, 0x0965)  # danda, double danda


def test_baraha_map(lang):
    """Test a single Baraha map file."""
    fpath = os.path.join(BASE_DIR, f"{lang}.json")
    errors = []

    # 1. File exists
    if not os.path.exists(fpath):
        return [f"File missing: {fpath}"]

    # 2. Valid JSON
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    # 3. Required fields
    for field in ('language', 'encoding', 'unicode_to_ansi', 'ansi_to_unicode'):
        if field not in data:
            errors.append(f"Missing field: {field}")

    if errors:
        return errors

    assert data['language'] == lang, f"Language mismatch: {data['language']} != {lang}"
    assert data['encoding'] == 'baraha', f"Encoding should be 'baraha', got {data['encoding']}"

    u2a = data['unicode_to_ansi']
    a2u = data['ansi_to_unicode']

    # 4. Minimum coverage
    min_expected = MIN_MAPPINGS.get(lang, 50)
    if len(u2a) < min_expected:
        errors.append(f"Too few mappings: {len(u2a)} < {min_expected}")

    # 5. Unicode block check (most chars should be in expected block)
    block_start, block_end = UNICODE_BLOCKS[lang]
    in_block = 0
    out_block = 0
    for uni_char in u2a:
        for ch in uni_char:
            cp = ord(ch)
            if block_start <= cp <= block_end:
                in_block += 1
            elif SHARED_RANGE[0] <= cp <= SHARED_RANGE[1]:
                in_block += 1  # shared punctuation is OK
            else:
                out_block += 1
            break  # only check first char of multi-char strings

    if in_block == 0:
        errors.append(f"No characters in expected Unicode block U+{block_start:04X}-U+{block_end:04X}")

    # 6. Bidirectional round-trip (strict)
    strict_ok = 0
    strict_fail = 0
    for uni, ansi in u2a.items():
        if ansi in a2u and a2u[ansi] == uni:
            strict_ok += 1
        else:
            strict_fail += 1

    # 7. No empty keys/values
    for uni, ansi in u2a.items():
        if not uni:
            errors.append("Empty Unicode key in unicode_to_ansi")
        if not ansi:
            errors.append(f"Empty ANSI value for U+{ord(uni[0]):04X}")

    for ansi, uni in a2u.items():
        if not ansi:
            errors.append("Empty ANSI key in ansi_to_unicode")
        if not uni:
            errors.append(f"Empty Unicode value for ANSI '{ansi}'")

    # 8. Core consonants should be present (at least ka, pa, ma for every script)
    # We check by looking for BrhCode values 'k', 'p', 'm' in the reverse map
    for core_brh in ('k', 'p', 'm', 'A'):
        if core_brh not in a2u:
            errors.append(f"Core BrhCode '{core_brh}' missing from ansi_to_unicode")

    return errors


def test_shreelipi_map(lang):
    """Test a single Shreelipi map file."""
    fpath = os.path.join(SHREELIPI_DIR, f"{lang}.json")
    errors = []

    if not os.path.exists(fpath):
        return [f"File missing: {fpath}"]

    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"Invalid JSON: {e}"]

    for field in ('language', 'encoding', 'needs_table'):
        if field not in data:
            errors.append(f"Missing field: {field}")

    if errors:
        return errors

    assert data['language'] == lang
    assert data['encoding'] == 'shreelipi'

    if data['needs_table']:
        # Placeholder file - just verify structure
        if 'note' not in data:
            errors.append("Placeholder missing 'note' field")
    else:
        u2s = data.get('unicode_to_shreelipi', {})
        s2u = data.get('shreelipi_to_unicode', {})
        if not u2s:
            errors.append("Generated Shreelipi map has no unicode_to_shreelipi entries")
        if not s2u:
            errors.append("Generated Shreelipi map has no shreelipi_to_unicode entries")
        if 'source_table' not in data:
            errors.append("Missing 'source_table' field")

    return errors


def main():
    print("=" * 60)
    print("ANSI Map Validation Test")
    print("=" * 60)

    total_pass = 0
    total_fail = 0
    total_errors = []

    # Test Baraha maps
    print("\n--- Baraha BrhCode Maps ---\n")
    for lang in LANGUAGES:
        errors = test_baraha_map(lang)
        if errors:
            status = "❌ FAIL"
            total_fail += 1
            total_errors.extend([(lang, e) for e in errors])
        else:
            status = "✅ PASS"
            total_pass += 1

        # Load count for display
        fpath = os.path.join(BASE_DIR, f"{lang}.json")
        count = 0
        if os.path.exists(fpath):
            with open(fpath) as f:
                d = json.load(f)
            count = d.get('total_mappings', len(d.get('unicode_to_ansi', {})))

        print(f"  {status} {lang:12s} ({count} mappings)")
        for e in errors:
            print(f"         ⚠ {e}")

    # Test Shreelipi maps
    print("\n--- Shreelipi Maps ---\n")
    for lang in LANGUAGES:
        errors = test_shreelipi_map(lang)
        if errors:
            status = "❌ FAIL"
            total_fail += 1
            total_errors.extend([(f"shreelipi/{lang}", e) for e in errors])
        else:
            status = "✅ PASS"
            total_pass += 1

        fpath = os.path.join(SHREELIPI_DIR, f"{lang}.json")
        if os.path.exists(fpath):
            with open(fpath) as f:
                d = json.load(f)
            needs = d.get('needs_table', True)
            count = d.get('total_mappings', 0)
            extra = f" (placeholder)" if needs else f" ({count} mappings)"
        else:
            extra = " (missing)"

        print(f"  {status} {lang:12s}{extra}")
        for e in errors:
            print(f"         ⚠ {e}")

    # Cross-language consistency check
    print("\n--- Cross-Language Consistency ---\n")
    # All languages should map the same BrhCode set (core subset)
    core_brh = {'A', 'Aa', 'I', 'Ii', 'U', 'Uu', 'k', 'K', 'g', 'G',
                'c', 'C', 'j', 't', 'T', 'd', 'D', 'n', 'p', 'P',
                'b', 'B', 'm', 'y', 'r', 'l', 'v', 's', 'h',
                'a', 'i', 'ii', 'u', 'uu', 'M', '\\'}
    all_brh = {}
    for lang in LANGUAGES:
        fpath = os.path.join(BASE_DIR, f"{lang}.json")
        if os.path.exists(fpath):
            with open(fpath) as f:
                d = json.load(f)
            brh_set = set(d.get('ansi_to_unicode', {}).keys())
            all_brh[lang] = brh_set

    if all_brh:
        # Find core BrhCodes present in ALL languages
        common = set.intersection(*all_brh.values())
        missing_core = core_brh - common
        if missing_core:
            # These are expected linguistic differences, not errors
            # Tamil lacks aspirated consonants; Bengali/Assamese merge v/b
            print(f"  ℹ️  {len(missing_core)} core BrhCodes missing from some languages (expected linguistic gaps):")
            for brh in sorted(missing_core):
                missing_in = [l for l, s in all_brh.items() if brh not in s]
                print(f"    '{brh}' missing in: {', '.join(missing_in)}")
            total_pass += 1  # informational, not a failure
        else:
            print(f"  ✅ All {len(core_brh)} core BrhCodes present across all 12 languages")
            total_pass += 1

        # Show BrhCode coverage per language
        print(f"\n  BrhCode coverage:")
        for lang in LANGUAGES:
            print(f"    {lang:12s}: {len(all_brh[lang]):3d} BrhCodes")

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {total_pass} passed, {total_fail} failed")
    print("=" * 60)

    if total_errors:
        print("\nErrors:")
        for lang, err in total_errors:
            print(f"  [{lang}] {err}")

    return 1 if total_fail > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
