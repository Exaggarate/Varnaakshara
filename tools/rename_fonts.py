#!/usr/bin/env python3
"""
Rename Varnaaksharam → Varnaakshara in all font name tables.

Targets:
  1. All 110 generated fonts in core/fonts/generated/
  2. All 23 source fonts in fonts/ansi/

Updates nameID 1, 4, 6, 16 (keeps 2, 17 unchanged).
Saves in-place.
"""

import os
import sys
from fontTools.ttLib import TTFont


def rename_font(font_path, dry_run=False):
    """Rename Varnaaksharam → Varnaakshara in a single font file."""
    try:
        font = TTFont(font_path)
    except Exception as e:
        print(f"  ERROR opening {font_path}: {e}")
        return False

    name_table = font['name']
    changed = False

    # Process nameIDs 1, 4, 6, 16 across all platforms
    target_name_ids = [1, 4, 6, 16]

    for record in name_table.names:
        if record.nameID in target_name_ids:
            try:
                value = record.toUnicode()
            except Exception:
                continue

            if 'Varnaaksharam' in value:
                new_value = value.replace('Varnaaksharam', 'Varnaakshara')
                name_table.setName(
                    new_value,
                    record.nameID,
                    record.platformID,
                    record.platEncID,
                    record.langID
                )
                changed = True
                if not dry_run:
                    print(f"    nameID {record.nameID} (plat {record.platformID}): "
                          f"'{value}' → '{new_value}'")

    # Also fix nameID 3 (unique ID) if it contains Varnaaksharam
    for record in name_table.names:
        if record.nameID == 3:
            try:
                value = record.toUnicode()
            except Exception:
                continue
            if 'Varnaaksharam' in value:
                new_value = value.replace('Varnaaksharam', 'Varnaakshara')
                name_table.setName(
                    new_value,
                    record.nameID,
                    record.platformID,
                    record.platEncID,
                    record.langID
                )
                changed = True

    if changed and not dry_run:
        font.save(font_path)
        print(f"  ✓ Saved: {os.path.basename(font_path)}")
    elif not changed:
        print(f"  - No change: {os.path.basename(font_path)}")

    font.close()
    return changed


def process_directory(directory, label):
    """Process all TTF files in a directory tree."""
    print(f"\n{'='*60}")
    print(f"Processing: {label}")
    print(f"Directory: {directory}")
    print(f"{'='*60}")

    total = 0
    renamed = 0

    for root, dirs, files in sorted(os.walk(directory)):
        for f in sorted(files):
            if f.lower().endswith('.ttf'):
                total += 1
                path = os.path.join(root, f)
                rel = os.path.relpath(path, directory)
                print(f"\n  [{total}] {rel}")
                if rename_font(path):
                    renamed += 1

    print(f"\n  Total: {total}, Renamed: {renamed}, Unchanged: {total - renamed}")
    return total, renamed


def verify_font(font_path):
    """Verify a font no longer contains 'Varnaaksharam'."""
    font = TTFont(font_path)
    name_table = font['name']
    for record in name_table.names:
        try:
            value = record.toUnicode()
        except Exception:
            continue
        if 'Varnaaksharam' in value:
            font.close()
            return False, record.nameID, value
    font.close()
    return True, None, None


def main():
    base = os.path.join(os.path.dirname(__file__), '..')

    generated_dir = os.path.abspath(os.path.join(base, 'core', 'fonts', 'generated'))
    source_dir = os.path.abspath(os.path.join(base, 'fonts', 'ansi'))

    # Process generated fonts
    gen_total, gen_renamed = process_directory(generated_dir, "Generated Fonts")

    # Process source fonts
    src_total, src_renamed = process_directory(source_dir, "Source ANSI Fonts")

    # Summary
    print(f"\n{'='*60}")
    print(f"RENAME COMPLETE")
    print(f"{'='*60}")
    print(f"Generated fonts: {gen_renamed}/{gen_total} renamed")
    print(f"Source fonts:     {src_renamed}/{src_total} renamed")
    print(f"Grand total:      {gen_renamed + src_renamed}/{gen_total + src_total} renamed")

    # Verification pass
    print(f"\n{'='*60}")
    print(f"VERIFICATION")
    print(f"{'='*60}")
    errors = 0
    for directory in [generated_dir, source_dir]:
        for root, dirs, files in os.walk(directory):
            for f in sorted(files):
                if f.lower().endswith('.ttf'):
                    path = os.path.join(root, f)
                    ok, name_id, value = verify_font(path)
                    if not ok:
                        print(f"  ✗ STILL HAS 'Varnaaksharam': {os.path.relpath(path, base)} "
                              f"(nameID {name_id}: {value})")
                        errors += 1

    if errors == 0:
        print(f"  ✓ All fonts verified — no 'Varnaaksharam' found anywhere")
    else:
        print(f"  ✗ {errors} fonts still contain 'Varnaaksharam'")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
