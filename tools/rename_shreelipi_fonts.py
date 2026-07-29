#!/usr/bin/env python3
"""
Rename internal font names in Shreelipi-origin fonts.

Transforms: "Varnaakshara Shreelipi [Script] NN" → "Varnaakshara [Script] Lipi NN"
with new numbering that doesn't conflict with existing Baraha-origin Lipi fonts.

Updates name table entries: nameID 1, 2, 4, 6, 16, 17
on both platform 1 (Mac) and platform 3 (Windows).
"""

import os
import sys
import re
from fontTools.ttLib import TTFont

# ── Configuration ──────────────────────────────────────────────────────────

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "core", "fonts", "generated", "shreelipi")

# Script code → (Full script name, Lipi start number)
# Start numbers chosen to avoid conflict with existing Baraha-origin fonts
SCRIPT_CONFIG = {
    "ass": ("Assamese",    1),   # No existing Baraha → start at 01
    "ban": ("Bengali",     3),   # Baraha has Bengali Lipi 01–02 → start at 03
    "dev": ("Devanagari",  2),   # Baraha has Devanagari Lipi 01 → start at 02
    "dia": ("Diacritical", 1),   # No existing Baraha → start at 01
    "guj": ("Gujarati",    3),   # Baraha has Gujarati Lipi 01–02 → start at 03
    "kan": ("Kannada",    11),   # Baraha has Kannada Lipi 01–09, skip 10 (Kalidasa) → start at 11
    "mal": ("Malayalam",   4),   # Baraha has Malayalam Lipi 01–03 → start at 04
    "ori": ("Odia",        1),   # No existing Baraha → start at 01
    "pun": ("Punjabi",     1),   # No existing Baraha → start at 01
    "san": ("Sanskrit",    1),   # No existing Baraha → start at 01
    "snd": ("Sindhi",      1),   # No existing Baraha → start at 01
    "tam": ("Tamil",       4),   # Baraha has Tamil Lipi 01–03 → start at 04
    "tel": ("Telugu",      4),   # Baraha has Telugu Lipi 01–03 → start at 04
}

WEIGHTS = ["Regular", "Medium", "SemiBold", "Bold", "Black"]

# ── Helpers ────────────────────────────────────────────────────────────────

def build_numbering_map():
    """
    Build a mapping from (script_code, old_number) → new_lipi_number.
    Within each script, sort existing directories by their old number and assign
    sequential new Lipi numbers starting from the configured start.
    """
    mapping = {}  # (script_code, old_num) → new_num

    # Discover all directories
    by_script = {}
    for entry in sorted(os.listdir(BASE_DIR)):
        dirpath = os.path.join(BASE_DIR, entry)
        if not os.path.isdir(dirpath):
            continue
        parts = entry.split("-")
        if len(parts) != 3 or parts[0] != "shreelipi":
            continue
        code = parts[1]
        try:
            num = int(parts[2])
        except ValueError:
            continue
        by_script.setdefault(code, []).append(num)

    for code, nums in by_script.items():
        if code not in SCRIPT_CONFIG:
            print(f"WARNING: Unknown script code '{code}', skipping")
            continue
        _, start = SCRIPT_CONFIG[code]
        for i, old_num in enumerate(sorted(nums)):
            mapping[(code, old_num)] = start + i

    return mapping


def rename_font(font_path, script_name, old_num, new_num, weight):
    """
    Update name table entries in a single font file.
    Returns (old_family_name, new_family_name) or None on error.
    """
    old_num_str = f"{old_num:02d}"
    new_num_str = f"{new_num:02d}"

    old_family = f"Varnaakshara Shreelipi {script_name} {old_num_str}"
    new_family = f"Varnaakshara {script_name} Lipi {new_num_str}"

    tt = TTFont(font_path)
    name_table = tt["name"]
    modified = False

    for rec in name_table.names:
        if rec.nameID not in (1, 2, 4, 6, 16, 17):
            continue

        try:
            val = rec.toUnicode()
        except Exception:
            continue

        new_val = None

        if rec.nameID == 1:
            # Family name: "Varnaakshara Shreelipi Bengali 01" → "Varnaakshara Bengali Lipi 03"
            if old_family in val:
                new_val = val.replace(old_family, new_family)

        elif rec.nameID == 2:
            # Subfamily: keep as-is (Regular/Bold/etc.)
            pass

        elif rec.nameID == 4:
            # Full name: "Varnaakshara Shreelipi Bengali 01 Bold" → "Varnaakshara Bengali Lipi 03 Bold"
            if old_family in val:
                new_val = val.replace(old_family, new_family)

        elif rec.nameID == 6:
            # PostScript name: "Varnaakshara-Shreelipi-Bengali-01-Bold" → "Varnaakshara-Bengali-Lipi-03-Bold"
            old_ps_family = f"Varnaakshara-Shreelipi-{script_name}-{old_num_str}"
            new_ps_family = f"Varnaakshara-{script_name}-Lipi-{new_num_str}"
            if old_ps_family in val:
                new_val = val.replace(old_ps_family, new_ps_family)

        elif rec.nameID == 16:
            # Typographic family: same as nameID 1
            if old_family in val:
                new_val = val.replace(old_family, new_family)

        elif rec.nameID == 17:
            # Typographic subfamily: keep as-is (Black/Bold/etc.)
            pass

        if new_val is not None and new_val != val:
            name_table.setName(new_val, rec.nameID, rec.platformID, rec.platEncID, rec.langID)
            modified = True

    if modified:
        tt.save(font_path)
    tt.close()

    return (old_family, new_family) if modified else None


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if not os.path.isdir(BASE_DIR):
        print(f"ERROR: Directory not found: {BASE_DIR}")
        sys.exit(1)

    print(f"Base directory: {BASE_DIR}")
    print()

    numbering = build_numbering_map()

    # Collect results for summary
    results = []  # (old_family, new_family, dir_name, file_count)
    errors = []
    total_files = 0

    for entry in sorted(os.listdir(BASE_DIR)):
        dirpath = os.path.join(BASE_DIR, entry)
        if not os.path.isdir(dirpath):
            continue

        parts = entry.split("-")
        if len(parts) != 3 or parts[0] != "shreelipi":
            continue

        code = parts[1]
        try:
            old_num = int(parts[2])
        except ValueError:
            continue

        if code not in SCRIPT_CONFIG:
            continue

        script_name, _ = SCRIPT_CONFIG[code]
        new_num = numbering.get((code, old_num))
        if new_num is None:
            errors.append(f"No mapping for {entry}")
            continue

        ttf_files = sorted([f for f in os.listdir(dirpath) if f.endswith(".ttf")])
        if not ttf_files:
            errors.append(f"No .ttf files in {entry}")
            continue

        old_family = None
        new_family = None
        file_count = 0

        for ttf in ttf_files:
            fpath = os.path.join(dirpath, ttf)
            # Infer weight from filename
            weight = "Regular"
            for w in WEIGHTS:
                if w in ttf:
                    weight = w
                    break

            try:
                result = rename_font(fpath, script_name, old_num, new_num, weight)
                if result:
                    old_family, new_family = result
                    file_count += 1
                    total_files += 1
            except Exception as e:
                errors.append(f"Error processing {fpath}: {e}")

        if old_family and new_family:
            results.append((old_family, new_family, entry, file_count))
            print(f"  ✓ {entry}: {old_family} → {new_family} ({file_count} files)")

    # ── Summary ────────────────────────────────────────────────────────────
    print()
    print("=" * 90)
    print(f"RENAME SUMMARY: {len(results)} families renamed, {total_files} files modified")
    print("=" * 90)
    print()

    # Group by script for cleaner output
    by_script = {}
    for old_fam, new_fam, dirname, fc in results:
        # Extract script from new family name
        script = new_fam.replace("Varnaakshara ", "").rsplit(" Lipi ", 1)[0]
        by_script.setdefault(script, []).append((old_fam, new_fam, dirname, fc))

    print(f"{'Old Name':<48} {'New Name':<42} {'Files'}")
    print(f"{'-'*48} {'-'*42} {'-'*5}")

    for script in sorted(by_script):
        for old_fam, new_fam, dirname, fc in by_script[script]:
            print(f"{old_fam:<48} {new_fam:<42} {fc}")

    if errors:
        print()
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")

    print()
    print("New Lipi number ranges by script:")
    range_by_script = {}
    for (code, old_num), new_num in sorted(numbering.items()):
        script_name = SCRIPT_CONFIG[code][0]
        range_by_script.setdefault(script_name, []).append(new_num)

    for script in sorted(range_by_script):
        nums = sorted(range_by_script[script])
        print(f"  {script:<15} Lipi {nums[0]:02d}–{nums[-1]:02d} ({len(nums)} fonts)")


if __name__ == "__main__":
    main()
