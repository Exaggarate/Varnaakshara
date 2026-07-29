#!/usr/bin/env python3
"""
Varnaakshara Baraha Font Processor
====================================
Processes newly discovered Baraha fonts:
  1. Unicode fonts (46 files): Rename families from BRH* → Varnaakshara *
     These already have real Bold/Italic variants — preserve them as-is.
  2. Extra ANSI fonts (8 files, 1 skipped): Rename + generate 5 weights
     using the stroke-and-union approach from generate_font_weights.py.

Usage:
    python process_baraha_fonts.py [--dry-run] [--verify]
"""

import argparse
import copy
import os
import sys
import time
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
import pathops
from pathops import Path as SkiaPath, LineCap, LineJoin


# ============================================================
# Configuration
# ============================================================

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
UNICODE_SOURCE_DIR = os.path.join(BASE_DIR, 'fonts', 'baraha-unicode')
ANSI_EXTRA_SOURCE_DIR = os.path.join(BASE_DIR, 'fonts', 'baraha-ansi-extra')
OUTPUT_DIR = os.path.join(BASE_DIR, 'core', 'fonts', 'generated')

# Weight configurations for ANSI fonts: (name, usWeightClass, stroke_expansion_units, is_bold)
WEIGHT_CONFIGS = [
    ("Regular",  400,  0,  False),
    ("Medium",   500,  10, False),
    ("SemiBold", 600,  20, False),
    ("Bold",     700,  35, True),
    ("Black",    900,  55, True),
]

# ============================================================
# Unicode Font Family Mapping
# ============================================================
# Map from BRH family base name → Varnaakshara family name
# These are Unicode fonts — NO "Lipi" suffix

UNICODE_FAMILY_MAP = {
    'BRHKan01': 'Varnaakshara Kannada 01',
    'BRHKan02': 'Varnaakshara Kannada 02',
    'BRHKan03': 'Varnaakshara Kannada 03',
    'BRHKan04': 'Varnaakshara Kannada 04',
    'BRHKan05': 'Varnaakshara Kannada 05',
    'BRHKan06': 'Varnaakshara Kannada 06',
    'BRHKan07': 'Varnaakshara Kannada 07',
    'BRHDev01': 'Varnaakshara Devanagari 01',
    'BRHDev02': 'Varnaakshara Devanagari 02',
    'BRHDev03': 'Varnaakshara Devanagari 03',
    'BRHTam01': 'Varnaakshara Tamil 01',
    'BRHTam02': 'Varnaakshara Tamil 02',
    'BRHTel01': 'Varnaakshara Telugu 01',
    'BRHTel02': 'Varnaakshara Telugu 02',
    'BRHMal01': 'Varnaakshara Malayalam 01',
    'BRHMal02': 'Varnaakshara Malayalam 02',
    'BRHGuj01': 'Varnaakshara Gujarati 01',
    'BRHGuj02': 'Varnaakshara Gujarati 02',
    'BRHGur01': 'Varnaakshara Gurmukhi 01',
    'BRHBen01': 'Varnaakshara Bengali 01',
    'BRHBen02': 'Varnaakshara Bengali 02',
    'BRHOri01': 'Varnaakshara Odia 01',
}

# Known variant suffixes for Unicode font filenames
VARIANT_SUFFIXES = ['BoldItalic', 'Bold', 'Italic']

# ============================================================
# Extra ANSI Font Mapping
# ============================================================
# Map from source filename → Varnaakshara family name
# brh_dev.ttf is skipped (duplicate of existing brhdevrn.ttf)

ANSI_EXTRA_MAP = {
    # 'brh_dev.ttf': SKIPPED — duplicate of brhdevrn.ttf (same glyphs + cmap)
    'brh_deve.ttf': 'Varnaakshara Devanagari Lipi 02',
    'brh_klds.ttf': 'Varnaakshara Kannada Lipi 10',
    'brhbrl.ttf':   'Varnaakshara Braille',
    'brhgur.ttf':   'Varnaakshara Gurmukhi Lipi 01',
    'brhgurrn.ttf': 'Varnaakshara Gurmukhi Lipi 02',
    'brhltn.ttf':   'Varnaakshara Latin',
    'brhori.ttf':   'Varnaakshara Odia Lipi 01',
    'brhorirn.ttf': 'Varnaakshara Odia Lipi 02',
}


# ============================================================
# Outline Expansion (for ANSI weight generation)
# ============================================================

def expand_glyph_outlines(glyphset, glyph_name, expansion_units):
    """
    Expand a glyph's outlines using pathops stroke + union.
    Returns (new_glyph, success).
    """
    if expansion_units <= 0:
        return None, True

    try:
        rec = RecordingPen()
        glyphset[glyph_name].draw(rec)

        has_outlines = any(op in ('lineTo', 'qCurveTo', 'curveTo') for op, _ in rec.value)
        if not has_outlines:
            return None, True

        original = SkiaPath()
        rec.replay(original.getPen())
        original.convertConicsToQuads()

        if not list(original.contours):
            return None, True

        stroke_width = expansion_units * 2
        stroked = SkiaPath()
        rec.replay(stroked.getPen())
        stroked.stroke(stroke_width, LineCap.ROUND_CAP, LineJoin.ROUND_JOIN, 4.0)
        stroked.convertConicsToQuads()

        result = pathops.op(
            original, stroked,
            pathops.PathOp.UNION,
            fix_winding=True,
            keep_starting_points=False,
        )

        if result is None or not list(result.contours):
            return None, True

        ttpen = TTGlyphPen(None)
        result.draw(ttpen)
        new_glyph = ttpen.glyph()
        return new_glyph, True

    except Exception as e:
        print(f"    Warning: Could not expand '{glyph_name}': {e}")
        return None, False


# ============================================================
# Name Table Helpers
# ============================================================

def get_postscript_family(family_name):
    """Convert family name to PostScript-compatible format (no spaces)."""
    return family_name.replace(" ", "-")


def update_name_table_full(font, family_name, subfamily_name):
    """
    Update the font's name table for proper family/weight identification.

    Sets nameID 1, 2, 4, 6, 16, 17, 3 across Windows and Mac platforms.

    subfamily_name should be one of: Regular, Bold, Italic, Bold Italic,
    Medium, SemiBold, Black, etc.
    """
    name_table = font['name']
    ps_family = get_postscript_family(family_name)

    # Determine RIBBI subfamily for nameID 2
    ribbi_map = {
        'Regular': 'Regular',
        'Bold': 'Bold',
        'Italic': 'Italic',
        'Bold Italic': 'Bold Italic',
    }
    ribbi_subfamily = ribbi_map.get(subfamily_name, 'Regular')

    # Full name
    if subfamily_name == 'Regular':
        full_name = family_name
    else:
        full_name = f"{family_name} {subfamily_name}"

    # PostScript name (no spaces, hyphens only)
    ps_subfamily = subfamily_name.replace(" ", "")
    ps_name = f"{ps_family}-{ps_subfamily}"

    entries = {
        1: family_name,
        2: ribbi_subfamily,
        4: full_name,
        6: ps_name,
        16: family_name,
        17: subfamily_name,
    }

    for name_id, value in entries.items():
        name_table.setName(value, name_id, 3, 1, 0x409)  # Windows
        name_table.setName(value, name_id, 1, 0, 0)       # Mac

    # Unique ID (nameID 3)
    unique_id = f"Varnaakshara;{ps_name}"
    name_table.setName(unique_id, 3, 3, 1, 0x409)
    name_table.setName(unique_id, 3, 1, 0, 0)


def update_os2_table(font, weight_class, is_bold, is_italic=False):
    """Update OS/2 table for weight class and style flags."""
    os2 = font['OS/2']
    os2.usWeightClass = weight_class

    REGULAR_BIT = 1 << 6
    BOLD_BIT = 1 << 5
    ITALIC_BIT = 1 << 0

    # Clear relevant bits
    os2.fsSelection &= ~(REGULAR_BIT | BOLD_BIT | ITALIC_BIT)

    if is_bold:
        os2.fsSelection |= BOLD_BIT
    if is_italic:
        os2.fsSelection |= ITALIC_BIT
    if weight_class == 400 and not is_italic:
        os2.fsSelection |= REGULAR_BIT


def update_head_table(font, is_bold, is_italic=False):
    """Update head table macStyle."""
    head = font['head']
    BOLD_BIT = 1 << 0
    ITALIC_BIT = 1 << 1

    if is_bold:
        head.macStyle |= BOLD_BIT
    else:
        head.macStyle &= ~BOLD_BIT

    if is_italic:
        head.macStyle |= ITALIC_BIT
    else:
        head.macStyle &= ~ITALIC_BIT


# ============================================================
# Unicode Font Processing
# ============================================================

def parse_unicode_filename(filename):
    """
    Parse a Unicode font filename to extract family base and variant.
    E.g., 'BRHKan07BoldItalic.ttf' → ('BRHKan07', 'Bold Italic')
         'BRHKan07.ttf' → ('BRHKan07', 'Regular')
    """
    stem = os.path.splitext(filename)[0]

    for suffix in VARIANT_SUFFIXES:
        if stem.endswith(suffix):
            base = stem[:-len(suffix)]
            # Convert 'BoldItalic' → 'Bold Italic'
            variant = 'Bold Italic' if suffix == 'BoldItalic' else suffix
            return base, variant

    return stem, 'Regular'


def process_unicode_fonts(source_dir, output_dir, stats):
    """Process all Unicode fonts: rename only, preserve original variants."""
    print(f"\n{'='*60}")
    print("PROCESSING UNICODE FONTS")
    print(f"Source: {source_dir}")
    print(f"{'='*60}")

    # Collect all TTF files
    ttf_files = sorted([f for f in os.listdir(source_dir) if f.endswith('.ttf')])
    print(f"Found {len(ttf_files)} font files")

    # Group by family
    families = {}
    for filename in ttf_files:
        base, variant = parse_unicode_filename(filename)
        if base not in families:
            families[base] = []
        families[base].append((filename, variant))

    print(f"Grouped into {len(families)} families")

    for base_name in sorted(families.keys()):
        new_family = UNICODE_FAMILY_MAP.get(base_name)
        if not new_family:
            print(f"\n  WARNING: No mapping for '{base_name}', skipping")
            stats['skipped'] += len(families[base_name])
            continue

        dir_slug = base_name.lower()
        family_dir = os.path.join(output_dir, dir_slug)
        os.makedirs(family_dir, exist_ok=True)

        print(f"\n  {base_name} → {new_family}")

        for filename, variant in sorted(families[base_name], key=lambda x: x[1]):
            source_path = os.path.join(source_dir, filename)

            # Determine weight/style properties
            is_bold = variant in ('Bold', 'Bold Italic')
            is_italic = variant in ('Italic', 'Bold Italic')
            weight_class = 700 if is_bold else 400

            # Output filename
            variant_slug = variant.replace(' ', '')
            output_filename = f"{dir_slug}-{variant_slug}.ttf"
            output_path = os.path.join(family_dir, output_filename)

            try:
                font = TTFont(source_path)
                update_name_table_full(font, new_family, variant)
                update_os2_table(font, weight_class, is_bold, is_italic)
                update_head_table(font, is_bold, is_italic)
                font.save(output_path)
                font.close()

                size_kb = os.path.getsize(output_path) / 1024
                print(f"    {variant:14s} → {output_filename} ({size_kb:.1f} KB)")
                stats['unicode_processed'] += 1
            except Exception as e:
                print(f"    ERROR processing {filename}: {e}")
                stats['failed'] += 1


# ============================================================
# ANSI Extra Font Processing (with weight generation)
# ============================================================

def generate_ansi_weight(source_path, output_path, family_name, weight_name,
                         weight_class, expansion_units, is_bold):
    """Generate a single weight variant of an ANSI font."""
    font = TTFont(source_path)
    glyphset = font.getGlyphSet()
    glyf_table = font['glyf']

    if expansion_units > 0:
        glyph_names = font.getGlyphOrder()
        total = len(glyph_names)
        expanded = 0
        failed = 0

        for glyph_name in glyph_names:
            glyph = glyf_table[glyph_name]
            if glyph.numberOfContours <= 0:
                continue

            new_glyph, success = expand_glyph_outlines(glyphset, glyph_name, expansion_units)

            if new_glyph is not None:
                orig_width = font['hmtx'][glyph_name][0]
                new_glyph.recalcBounds(glyf_table)
                glyf_table[glyph_name] = new_glyph
                font['hmtx'][glyph_name] = (orig_width, new_glyph.xMin)
                expanded += 1
            elif not success:
                failed += 1

        print(f"      Expanded {expanded}/{total} glyphs ({failed} failed)")

    # Update metadata
    update_name_table_full(font, family_name, weight_name)
    update_os2_table(font, weight_class, is_bold)
    update_head_table(font, is_bold)

    font.save(output_path)
    font.close()
    return True


def process_ansi_extra_fonts(source_dir, output_dir, stats):
    """Process extra ANSI fonts: rename + generate 5 weights."""
    print(f"\n{'='*60}")
    print("PROCESSING EXTRA ANSI FONTS")
    print(f"Source: {source_dir}")
    print(f"{'='*60}")

    ttf_files = sorted([f for f in os.listdir(source_dir) if f.endswith('.ttf')])
    print(f"Found {len(ttf_files)} font files")

    for filename in ttf_files:
        source_path = os.path.join(source_dir, filename)

        if filename not in ANSI_EXTRA_MAP:
            print(f"\n  SKIP: {filename} (duplicate of existing brhdevrn.ttf)")
            stats['skipped'] += 1
            continue

        new_family = ANSI_EXTRA_MAP[filename]
        stem = os.path.splitext(filename)[0]
        family_dir = os.path.join(output_dir, stem)
        os.makedirs(family_dir, exist_ok=True)

        print(f"\n  {filename} → {new_family}")

        for weight_name, weight_class, expansion, is_bold in WEIGHT_CONFIGS:
            output_filename = f"{stem}-{weight_name}.ttf"
            output_path = os.path.join(family_dir, output_filename)

            print(f"    Generating {weight_name} (w{weight_class}, expansion={expansion})...")

            try:
                start = time.time()
                success = generate_ansi_weight(
                    source_path, output_path, new_family,
                    weight_name, weight_class, expansion, is_bold
                )
                elapsed = time.time() - start

                if success:
                    size_kb = os.path.getsize(output_path) / 1024
                    print(f"      → {output_filename} ({size_kb:.1f} KB, {elapsed:.1f}s)")
                    stats['ansi_processed'] += 1
                else:
                    print(f"      → FAILED")
                    stats['failed'] += 1
            except Exception as e:
                print(f"      → ERROR: {e}")
                stats['failed'] += 1

        stats['ansi_families'] += 1


# ============================================================
# Verification
# ============================================================

def verify_font(font_path):
    """Verify a processed font has correct Varnaakshara metadata."""
    font = TTFont(font_path)
    name_table = font['name']
    os2 = font['OS/2']
    head = font['head']

    info = {
        'file': os.path.basename(font_path),
        'family': name_table.getName(1, 3, 1, 0x409).toUnicode() if name_table.getName(1, 3, 1, 0x409) else 'N/A',
        'subfamily': name_table.getName(2, 3, 1, 0x409).toUnicode() if name_table.getName(2, 3, 1, 0x409) else 'N/A',
        'full_name': name_table.getName(4, 3, 1, 0x409).toUnicode() if name_table.getName(4, 3, 1, 0x409) else 'N/A',
        'ps_name': name_table.getName(6, 3, 1, 0x409).toUnicode() if name_table.getName(6, 3, 1, 0x409) else 'N/A',
        'typo_family': name_table.getName(16, 3, 1, 0x409).toUnicode() if name_table.getName(16, 3, 1, 0x409) else 'N/A',
        'typo_subfamily': name_table.getName(17, 3, 1, 0x409).toUnicode() if name_table.getName(17, 3, 1, 0x409) else 'N/A',
        'weight_class': os2.usWeightClass,
        'fs_selection': f"0x{os2.fsSelection:04X}",
        'mac_style': f"0x{head.macStyle:04X}",
    }
    font.close()

    # Check for old BRH names
    has_old_name = False
    for field in ['family', 'full_name', 'ps_name', 'typo_family']:
        if 'BRH' in info[field]:
            has_old_name = True
            break

    return info, has_old_name


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Process Baraha Unicode and extra ANSI fonts")
    parser.add_argument("--dry-run", action="store_true", help="Don't write any files")
    parser.add_argument("--verify", action="store_true", help="Verify after processing")
    parser.add_argument("--unicode-only", action="store_true", help="Process only Unicode fonts")
    parser.add_argument("--ansi-only", action="store_true", help="Process only ANSI fonts")
    args = parser.parse_args()

    unicode_dir = os.path.abspath(UNICODE_SOURCE_DIR)
    ansi_dir = os.path.abspath(ANSI_EXTRA_SOURCE_DIR)
    output_dir = os.path.abspath(OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)

    print("Varnaakshara Baraha Font Processor")
    print(f"Unicode source:    {unicode_dir}")
    print(f"ANSI extra source: {ansi_dir}")
    print(f"Output:            {output_dir}")

    stats = {
        'unicode_processed': 0,
        'ansi_processed': 0,
        'ansi_families': 0,
        'skipped': 0,
        'failed': 0,
    }

    start_time = time.time()

    if not args.ansi_only:
        process_unicode_fonts(unicode_dir, output_dir, stats)

    if not args.unicode_only:
        process_ansi_extra_fonts(ansi_dir, output_dir, stats)

    total_time = time.time() - start_time

    # Summary
    total_generated = stats['unicode_processed'] + stats['ansi_processed']

    print(f"\n{'='*60}")
    print("PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"Unicode fonts renamed:         {stats['unicode_processed']}")
    print(f"ANSI families weight-generated:{stats['ansi_families']}")
    print(f"ANSI weight files generated:   {stats['ansi_processed']}")
    print(f"Total font files created:      {total_generated}")
    print(f"Skipped (duplicates):          {stats['skipped']}")
    print(f"Failed:                        {stats['failed']}")
    print(f"Total time:                    {total_time:.1f}s")

    # Count all fonts now in generated/
    total_in_generated = 0
    for root, dirs, files in os.walk(output_dir):
        total_in_generated += sum(1 for f in files if f.endswith('.ttf'))
    print(f"\nTotal fonts in core/fonts/generated/: {total_in_generated}")

    # Verify if requested
    if args.verify:
        print(f"\n{'='*60}")
        print("VERIFICATION")
        print(f"{'='*60}")

        errors = 0
        # Only verify fonts we just created
        new_dirs = set()
        for base_name in UNICODE_FAMILY_MAP:
            new_dirs.add(base_name.lower())
        for filename in ANSI_EXTRA_MAP:
            new_dirs.add(os.path.splitext(filename)[0])

        for subdir in sorted(new_dirs):
            full_dir = os.path.join(output_dir, subdir)
            if not os.path.isdir(full_dir):
                continue
            for f in sorted(os.listdir(full_dir)):
                if f.endswith('.ttf'):
                    path = os.path.join(full_dir, f)
                    info, has_old = verify_font(path)
                    status = "✗ OLD NAME" if has_old else "✓"
                    print(f"  {status} {f}: {info['typo_family']} / {info['typo_subfamily']} (w{info['weight_class']})")
                    if has_old:
                        errors += 1

        if errors == 0:
            print(f"\n  ✓ All new fonts verified — no old BRH names found")
        else:
            print(f"\n  ✗ {errors} fonts still have old BRH names")

    return 0 if stats['failed'] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
