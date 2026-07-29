#!/usr/bin/env python3
"""
Varnaakshara Shreelipi Font Weight Generator
=============================================
Scans Shreelipi font directories, inventories all fonts, groups by script,
selects Regular-weight sources, and generates 5-weight families using the
same outline expansion technique as generate_font_weights.py.

Output naming: "Varnaakshara Shreelipi [Script] [NN]"
Output directory: core/fonts/generated/shreelipi/

Usage:
    python generate_shreelipi_weights.py [--inventory-only] [--dry-run]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Import core functions from the existing weight generator
sys.path.insert(0, os.path.dirname(__file__))
from generate_font_weights import (
    WEIGHT_CONFIGS,
    generate_weight,
    verify_font,
)
from fontTools.ttLib import TTFont


# Directory code → script name mapping
SCRIPT_MAP = {
    'ARA': 'Arabic',
    'ASS': 'Assamese',
    'BAN': 'Bengali',
    'DEV': 'Devanagari',
    'DIA': 'Diacritical',
    'GUJ': 'Gujarati',
    'KAN': 'Kannada',
    'MAL': 'Malayalam',
    'ORI': 'Odia',
    'PUN': 'Punjabi',
    'SAN': 'Sanskrit',
    'SND': 'Sindhi',
    'TAM': 'Tamil',
    'TEL': 'Telugu',
}

# Minimum glyph count to include a font (skip auxiliary/symbol fonts)
MIN_GLYPHS = 50

# Bold-indicating subfamily strings
BOLD_SUBFAMILIES = {'Bold', 'BoldItalic', 'Bold Italic'}
ITALIC_SUBFAMILIES = {'Italic', 'BoldItalic', 'Bold Italic'}
SKIP_SUBFAMILIES = BOLD_SUBFAMILIES | ITALIC_SUBFAMILIES


def get_font_info(font_path):
    """Extract font metadata. Returns dict or None on error."""
    try:
        font = TTFont(font_path)
    except Exception as e:
        return None

    try:
        nt = font['name']
        info = {}

        for nid, key in [(1, 'family'), (2, 'subfamily'), (4, 'full_name'),
                          (6, 'ps_name'), (16, 'typo_family'), (17, 'typo_subfamily')]:
            rec = nt.getName(nid, 3, 1, 0x409)
            if rec:
                info[key] = rec.toUnicode()
            else:
                rec = nt.getName(nid, 1, 0, 0)
                info[key] = rec.toUnicode() if rec else 'N/A'

        try:
            info['glyph_count'] = len(font.getGlyphOrder())
        except Exception:
            # Fallback: count from maxp table
            try:
                info['glyph_count'] = font['maxp'].numGlyphs
            except Exception:
                info['glyph_count'] = 0

        try:
            info['weight_class'] = font['OS/2'].usWeightClass
        except Exception:
            info['weight_class'] = 400

        # Check if font has glyf table (TrueType outlines)
        info['has_glyf'] = 'glyf' in font

        font.close()
        return info
    except Exception as e:
        try:
            font.close()
        except:
            pass
        return None


def determine_script_from_path(font_path, base_dir):
    """Determine script code from the font's directory path."""
    rel = os.path.relpath(font_path, base_dir)
    parts = rel.replace('\\', '/').split('/')

    # Check for LNGFONTS/XXX or DEFFONTS/XXX pattern
    for i, part in enumerate(parts):
        if part in ('LNGFONTS', 'DEFFONTS') and i + 1 < len(parts):
            code = parts[i + 1].upper()
            if code in SCRIPT_MAP:
                return code

    # Top-level ORI files
    fname = os.path.basename(font_path).upper()
    if 'ORI' in fname:
        return 'ORI'

    return None


def inventory_shreelipi_fonts(base_dir):
    """
    Scan all Shreelipi fonts and return inventory.
    Returns list of dicts with path, info, script_code, script_name.
    """
    inventory = []

    for root, dirs, files in sorted(os.walk(base_dir)):
        for f in sorted(files):
            if not f.lower().endswith('.ttf'):
                continue
            path = os.path.join(root, f)
            info = get_font_info(path)
            if info is None:
                print(f"  SKIP (error): {os.path.relpath(path, base_dir)}")
                continue

            script_code = determine_script_from_path(path, base_dir)
            script_name = SCRIPT_MAP.get(script_code, 'Unknown') if script_code else 'Unknown'

            inventory.append({
                'path': path,
                'rel_path': os.path.relpath(path, base_dir),
                'filename': f,
                'family': info['family'],
                'subfamily': info['subfamily'],
                'glyph_count': info['glyph_count'],
                'weight_class': info['weight_class'],
                'has_glyf': info['has_glyf'],
                'script_code': script_code,
                'script_name': script_name,
            })

    return inventory


def select_source_fonts(inventory):
    """
    Select source fonts for weight generation.
    Rules:
    - Skip fonts with < MIN_GLYPHS glyphs (auxiliary fonts)
    - Skip fonts without glyf table (can't do outline expansion)
    - For families with Bold/Italic variants, use only Regular
    - Group by (family_name, script_code) to avoid duplicates
    """
    # Group fonts by family name
    families = {}
    for item in inventory:
        fam = item['family']
        if fam not in families:
            families[fam] = []
        families[fam].append(item)

    sources = []
    skipped_bold = []
    skipped_small = []
    skipped_no_glyf = []

    for fam_name, members in sorted(families.items()):
        # Check if family has Bold/Italic variants
        subfamilies = {m['subfamily'] for m in members}
        has_bold = bool(subfamilies & BOLD_SUBFAMILIES)

        for m in members:
            # Skip small auxiliary fonts
            if m['glyph_count'] < MIN_GLYPHS:
                skipped_small.append(m)
                continue

            # Skip fonts without glyf table
            if not m['has_glyf']:
                skipped_no_glyf.append(m)
                continue

            # If family has Bold, skip Bold/Italic variants
            if has_bold and m['subfamily'] in SKIP_SUBFAMILIES:
                skipped_bold.append(m)
                continue

            # For "A" subfamily (e.g., Shreelipi Bangla LekhaT), treat as Regular
            sources.append(m)

    return sources, skipped_bold, skipped_small, skipped_no_glyf


def generate_shreelipi_families(sources, output_base):
    """
    Generate 5-weight families for each source font.
    Names: "Varnaakshara Shreelipi [Script] [NN]"
    """
    # Group by script for numbering
    by_script = {}
    for src in sources:
        sc = src['script_code'] or 'UNK'
        if sc not in by_script:
            by_script[sc] = []
        by_script[sc].append(src)

    stats = {'families': 0, 'generated': 0, 'failed': 0}
    generated_families = []

    for script_code in sorted(by_script.keys()):
        script_fonts = by_script[script_code]
        script_name = SCRIPT_MAP.get(script_code, 'Unknown')

        print(f"\n{'='*60}")
        print(f"Script: {script_name} ({script_code}) — {len(script_fonts)} source fonts")
        print(f"{'='*60}")

        for idx, src in enumerate(script_fonts, 1):
            number = f"{idx:02d}"
            family_name = f"Varnaakshara Shreelipi {script_name} {number}"
            dir_name = f"shreelipi-{script_code.lower()}-{number}"
            family_dir = os.path.join(output_base, dir_name)
            os.makedirs(family_dir, exist_ok=True)

            print(f"\n  [{script_code}-{number}] {src['filename']}")
            print(f"    Original: {src['family']} ({src['subfamily']})")
            print(f"    New name: {family_name}")
            print(f"    Glyphs:   {src['glyph_count']}")

            family_info = {
                'family_name': family_name,
                'dir_name': dir_name,
                'source_file': src['filename'],
                'source_family': src['family'],
                'script_code': script_code,
                'script_name': script_name,
                'glyph_count': src['glyph_count'],
                'weights': [],
            }

            for weight_name, weight_class, expansion, is_bold in WEIGHT_CONFIGS:
                output_filename = f"{dir_name}-{weight_name}.ttf"
                output_path = os.path.join(family_dir, output_filename)

                print(f"    Generating {weight_name} (w{weight_class})...", end='', flush=True)

                try:
                    start = time.time()
                    success = generate_weight(
                        src['path'], output_path, family_name,
                        weight_name, weight_class, expansion, is_bold
                    )
                    elapsed = time.time() - start

                    if success:
                        size_kb = os.path.getsize(output_path) / 1024
                        print(f" ✓ ({size_kb:.0f}KB, {elapsed:.1f}s)")
                        stats['generated'] += 1
                        family_info['weights'].append({
                            'weight': weight_name,
                            'file': output_filename,
                            'size_kb': round(size_kb, 1),
                        })
                    else:
                        print(f" ✗ FAILED")
                        stats['failed'] += 1
                except Exception as e:
                    print(f" ✗ ERROR: {e}")
                    stats['failed'] += 1

            stats['families'] += 1
            generated_families.append(family_info)

    return stats, generated_families


def print_inventory_table(inventory):
    """Print a formatted inventory table."""
    print(f"\n{'='*100}")
    print(f"SHREELIPI FONT INVENTORY")
    print(f"{'='*100}")
    print(f"{'File':<40} {'Family':<30} {'Weight':<12} {'Glyphs':>6} {'Script':<10}")
    print(f"{'-'*40} {'-'*30} {'-'*12} {'-'*6} {'-'*10}")

    for item in inventory:
        print(f"{item['rel_path']:<40} {item['family']:<30} "
              f"{item['subfamily']:<12} {item['glyph_count']:>6} {item['script_name']:<10}")

    print(f"\nTotal fonts: {len(inventory)}")

    # Group summary by script
    by_script = {}
    for item in inventory:
        sn = item['script_name']
        if sn not in by_script:
            by_script[sn] = 0
        by_script[sn] += 1

    print(f"\nBy script:")
    for sn in sorted(by_script.keys()):
        print(f"  {sn}: {by_script[sn]}")


def main():
    parser = argparse.ArgumentParser(description="Generate Shreelipi font weight families")
    parser.add_argument("--inventory-only", action="store_true",
                        help="Only inventory fonts, don't generate weights")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be generated without doing it")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..', 'shreelipi_extracted', 'fonts'))
    output_base = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                '..', 'core', 'fonts', 'generated', 'shreelipi'))

    print("Varnaakshara Shreelipi Font Weight Generator")
    print(f"Source: {base_dir}")
    print(f"Output: {output_base}")

    # Step 1: Inventory all fonts
    print("\n--- INVENTORYING ALL SHREELIPI FONTS ---")
    inventory = inventory_shreelipi_fonts(base_dir)
    print_inventory_table(inventory)

    if args.inventory_only:
        return 0

    # Step 2: Select source fonts
    print("\n--- SELECTING SOURCE FONTS ---")
    sources, skipped_bold, skipped_small, skipped_no_glyf = select_source_fonts(inventory)

    print(f"\nSelected: {len(sources)} source fonts")
    print(f"Skipped (Bold/Italic variants): {len(skipped_bold)}")
    print(f"Skipped (< {MIN_GLYPHS} glyphs): {len(skipped_small)}")
    print(f"Skipped (no glyf table): {len(skipped_no_glyf)}")

    if skipped_bold:
        print("\n  Bold/Italic skipped:")
        for s in skipped_bold:
            print(f"    {s['rel_path']} ({s['family']} {s['subfamily']})")

    if skipped_small:
        print(f"\n  Small fonts skipped (< {MIN_GLYPHS} glyphs):")
        for s in skipped_small:
            print(f"    {s['rel_path']} ({s['glyph_count']} glyphs)")

    print("\n  Source fonts to process:")
    for s in sources:
        print(f"    {s['rel_path']} → {s['family']} [{s['script_name']}] ({s['glyph_count']} glyphs)")

    if args.dry_run:
        print("\n--- DRY RUN — not generating ---")
        for s in sources:
            print(f"  Would generate: Varnaakshara Shreelipi {s['script_name']} XX")
        return 0

    # Step 3: Generate weights
    print("\n--- GENERATING WEIGHT FAMILIES ---")
    os.makedirs(output_base, exist_ok=True)

    start_time = time.time()
    stats, generated_families = generate_shreelipi_families(sources, output_base)
    total_time = time.time() - start_time

    # Summary
    print(f"\n{'='*60}")
    print(f"GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Families generated: {stats['families']}")
    print(f"Font files generated: {stats['generated']}")
    print(f"Failed: {stats['failed']}")
    print(f"Total time: {total_time:.1f}s")

    # Save inventory JSON for the report
    inventory_path = os.path.join(output_base, 'shreelipi_inventory.json')
    with open(inventory_path, 'w') as f:
        json.dump({
            'inventory': [{k: v for k, v in item.items() if k != 'path'} for item in inventory],
            'generated_families': generated_families,
            'stats': stats,
        }, f, indent=2)
    print(f"\nInventory saved: {inventory_path}")

    # Quick verification of a few generated fonts
    print(f"\n--- VERIFICATION SAMPLE ---")
    verified = 0
    for fam in generated_families[:3]:
        dir_path = os.path.join(output_base, fam['dir_name'])
        for wt in fam['weights'][:2]:
            fp = os.path.join(dir_path, wt['file'])
            if os.path.exists(fp):
                info = verify_font(fp)
                print(f"  {wt['file']}: family={info['family']}, weight={info['weight_class']}")
                verified += 1
    print(f"  Verified {verified} sample fonts")

    return 0 if stats['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
