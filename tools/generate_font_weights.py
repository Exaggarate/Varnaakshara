#!/usr/bin/env python3
"""
Varnaakshara Font Weight Generator
===================================
Generates 5-weight font families from single-weight ANSI TrueType fonts
using fonttools + skia-pathops outline expansion.

Technique: For each heavier weight, the glyph outlines are stroked with
increasing width and unioned with the original filled shape. This expands
outer contours outward and shrinks inner counters, producing a natural
bolding effect.

Usage:
    python generate_font_weights.py [--source-dir DIR] [--output-dir DIR] [--font FILENAME]
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


# Weight configurations: (name, usWeightClass, stroke_expansion_units, is_bold)
WEIGHT_CONFIGS = [
    ("Regular",  400,  0,  False),
    ("Medium",   500,  10, False),
    ("SemiBold", 600,  20, False),
    ("Bold",     700,  35, True),
    ("Black",    900,  55, True),
]

# Default directories
DEFAULT_SOURCE_DIR = os.path.join(os.path.dirname(__file__), "..", "fonts", "ansi")
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "core", "fonts", "generated")


def expand_glyph_outlines(glyphset, glyph_name, expansion_units):
    """
    Expand a glyph's outlines by the given number of units using pathops stroke + union.

    For each glyph:
    1. Record drawing commands from the original glyph
    2. Build a pathops Path from those commands
    3. Create a stroked copy (stroke width = 2 * expansion for symmetric expansion)
    4. Union the original filled path with the stroked version
    5. Return the result as TTGlyphPen output

    Returns (new_glyph, success). On failure, returns (None, False).
    """
    if expansion_units <= 0:
        return None, True  # No expansion needed, use original

    try:
        # Record the original drawing commands
        rec = RecordingPen()
        glyphset[glyph_name].draw(rec)

        # Check if glyph has any drawing operations
        has_outlines = any(op in ('lineTo', 'qCurveTo', 'curveTo') for op, _ in rec.value)
        if not has_outlines:
            return None, True  # Empty glyph or space, skip

        # Build original pathops path
        original = SkiaPath()
        rec.replay(original.getPen())
        original.convertConicsToQuads()

        # Check if original has any area
        if not list(original.contours):
            return None, True

        # Build stroked copy for expansion
        # Stroke width is 2x the desired expansion (half goes each side)
        stroke_width = expansion_units * 2
        stroked = SkiaPath()
        rec.replay(stroked.getPen())
        stroked.stroke(stroke_width, LineCap.ROUND_CAP, LineJoin.ROUND_JOIN, 4.0)
        stroked.convertConicsToQuads()

        # Union original + stroked = expanded shape
        result = pathops.op(
            original, stroked,
            pathops.PathOp.UNION,
            fix_winding=True,
            keep_starting_points=False,
        )

        if result is None or not list(result.contours):
            # Fallback: return original unchanged
            return None, True

        # Convert result back to TrueType glyph
        ttpen = TTGlyphPen(None)
        result.draw(ttpen)
        new_glyph = ttpen.glyph()

        return new_glyph, True

    except Exception as e:
        # On any error, skip this glyph (use original)
        print(f"    Warning: Could not expand '{glyph_name}': {e}")
        return None, False


def get_family_name(font):
    """Extract the typographic family name from a font."""
    name_table = font['name']
    # Try nameID 16 (typographic family) first, then nameID 1 (family)
    for name_id in (16, 1):
        record = name_table.getName(name_id, 3, 1, 0x409)
        if record:
            return record.toUnicode()
    return "Unknown"


def get_postscript_family(family_name):
    """Convert family name to PostScript-compatible format (no spaces)."""
    return family_name.replace(" ", "-")


def update_name_table(font, family_name, weight_name):
    """
    Update the font's name table for proper family/weight identification.

    Sets:
    - nameID 1: Family name (same across all weights for RIBBI grouping)
    - nameID 2: Subfamily (Regular/Bold for RIBBI, or the actual weight)
    - nameID 4: Full name = "Family Name Weight"
    - nameID 6: PostScript name = "FamilyName-Weight"
    - nameID 16: Typographic family name
    - nameID 17: Typographic subfamily name
    """
    name_table = font['name']
    ps_family = get_postscript_family(family_name)

    # For Windows RIBBI model: nameID 1+2 define the family grouping
    # nameID 2 should be Regular/Bold/Italic/Bold Italic only
    # For non-RIBBI weights, we use nameID 16+17 (typographic)

    # Determine RIBBI subfamily
    if weight_name == "Regular":
        ribbi_subfamily = "Regular"
    elif weight_name == "Bold":
        ribbi_subfamily = "Bold"
    else:
        ribbi_subfamily = "Regular"  # Non-RIBBI weights fall back to Regular

    # For non-RIBBI weights, nameID 1 should include the weight to create
    # a separate RIBBI family, OR we use nameID 16/17 properly
    # The preferred approach for InDesign is to use nameID 16/17 for all
    # weights and keep nameID 1 the same across all weights.

    full_name = f"{family_name} {weight_name}" if weight_name != "Regular" else family_name
    ps_name = f"{ps_family}-{weight_name}"

    # Platform 3 (Windows), Encoding 1 (Unicode BMP), Language 0x409 (English US)
    entries = {
        1: family_name,         # Family name
        2: ribbi_subfamily,     # RIBBI subfamily
        4: full_name,           # Full name
        6: ps_name,             # PostScript name
        16: family_name,        # Typographic family
        17: weight_name,        # Typographic subfamily
    }

    for name_id, value in entries.items():
        name_table.setName(value, name_id, 3, 1, 0x409)  # Windows
        name_table.setName(value, name_id, 1, 0, 0)       # Mac

    # Update nameID 3 (Unique ID)
    unique_id = f"Varnaaksharam;{ps_name}"
    name_table.setName(unique_id, 3, 3, 1, 0x409)
    name_table.setName(unique_id, 3, 1, 0, 0)


def update_os2_table(font, weight_class, is_bold):
    """
    Update OS/2 table for weight class and style flags.

    - usWeightClass: 400, 500, 600, 700, 900
    - fsSelection: bit 5 (BOLD) for Bold/Black, bit 6 (REGULAR) for Regular
    """
    os2 = font['OS/2']
    os2.usWeightClass = weight_class

    # fsSelection flags
    REGULAR_BIT = 1 << 6   # bit 6
    BOLD_BIT = 1 << 5      # bit 5

    # Clear REGULAR and BOLD bits first
    os2.fsSelection &= ~(REGULAR_BIT | BOLD_BIT)

    if is_bold:
        os2.fsSelection |= BOLD_BIT
    elif weight_class == 400:
        os2.fsSelection |= REGULAR_BIT


def update_head_table(font, is_bold):
    """
    Update head table macStyle for bold flag.

    - macStyle bit 0: Bold
    """
    head = font['head']
    BOLD_BIT = 1 << 0

    if is_bold:
        head.macStyle |= BOLD_BIT
    else:
        head.macStyle &= ~BOLD_BIT


def generate_weight(source_path, output_path, family_name, weight_name, weight_class,
                    expansion_units, is_bold):
    """
    Generate a single weight variant of a font.

    Args:
        source_path: Path to source TTF file
        output_path: Path to write the generated TTF
        family_name: Font family name
        weight_name: Weight name (Regular, Medium, SemiBold, Bold, Black)
        weight_class: OS/2 usWeightClass value
        expansion_units: Outline expansion in font units
        is_bold: Whether this weight should have bold flags set
    """
    font = TTFont(source_path)
    glyphset = font.getGlyphSet()
    glyf_table = font['glyf']

    if expansion_units > 0:
        glyph_names = font.getGlyphOrder()
        total = len(glyph_names)
        expanded = 0
        failed = 0

        for i, glyph_name in enumerate(glyph_names):
            glyph = glyf_table[glyph_name]

            # Skip empty glyphs and composite glyphs
            if glyph.numberOfContours <= 0:
                continue

            new_glyph, success = expand_glyph_outlines(glyphset, glyph_name, expansion_units)

            if new_glyph is not None:
                # Preserve original metrics
                orig_width = font['hmtx'][glyph_name][0]

                # Calculate bounds for the new glyph
                new_glyph.recalcBounds(glyf_table)

                # Replace the glyph
                glyf_table[glyph_name] = new_glyph

                # Keep original advance width (don't change horizontal metrics)
                # but adjust LSB if the glyph expanded leftward
                font['hmtx'][glyph_name] = (orig_width, new_glyph.xMin)

                expanded += 1
            elif not success:
                failed += 1

        print(f"    Expanded {expanded}/{total} glyphs ({failed} failed)")

    # Update metadata
    update_name_table(font, family_name, weight_name)
    update_os2_table(font, weight_class, is_bold)
    update_head_table(font, is_bold)

    # Save
    font.save(output_path)
    return True


def process_font(source_path, output_dir, stats):
    """
    Process a single source font, generating all 5 weight variants.
    """
    basename = os.path.splitext(os.path.basename(source_path))[0]
    font = TTFont(source_path)
    family_name = get_family_name(font)
    font.close()

    print(f"\n{'='*60}")
    print(f"Processing: {os.path.basename(source_path)}")
    print(f"Family: {family_name}")
    print(f"{'='*60}")

    # Create family subdirectory
    family_dir = os.path.join(output_dir, basename)
    os.makedirs(family_dir, exist_ok=True)

    for weight_name, weight_class, expansion, is_bold in WEIGHT_CONFIGS:
        output_filename = f"{basename}-{weight_name}.ttf"
        output_path = os.path.join(family_dir, output_filename)

        print(f"  Generating {weight_name} (w{weight_class}, expansion={expansion})...")

        try:
            start = time.time()
            success = generate_weight(
                source_path, output_path, family_name,
                weight_name, weight_class, expansion, is_bold
            )
            elapsed = time.time() - start

            if success:
                size_kb = os.path.getsize(output_path) / 1024
                print(f"    -> {output_filename} ({size_kb:.1f} KB, {elapsed:.1f}s)")
                stats['generated'] += 1
            else:
                print(f"    -> FAILED")
                stats['failed'] += 1
        except Exception as e:
            print(f"    -> ERROR: {e}")
            stats['failed'] += 1

    stats['families'] += 1


def verify_font(font_path):
    """Verify a generated font has correct metadata."""
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
    return info


def main():
    parser = argparse.ArgumentParser(description="Generate multi-weight font families")
    parser.add_argument("--source-dir", default=DEFAULT_SOURCE_DIR,
                        help="Directory containing source TTF fonts")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR,
                        help="Output directory for generated fonts")
    parser.add_argument("--font", default=None,
                        help="Process a single font file (filename only)")
    parser.add_argument("--verify", action="store_true",
                        help="Verify generated fonts after processing")
    parser.add_argument("--skip", nargs="*", default=["brhkndb.ttf"],
                        help="Font files to skip (default: brhkndb.ttf)")
    args = parser.parse_args()

    source_dir = os.path.abspath(args.source_dir)
    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print("Varnaakshara Font Weight Generator")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print(f"Weights: {', '.join(f'{n} (w{w})' for n, w, _, _ in WEIGHT_CONFIGS)}")

    # Collect source fonts
    if args.font:
        source_fonts = [os.path.join(source_dir, args.font)]
    else:
        source_fonts = sorted([
            os.path.join(source_dir, f)
            for f in os.listdir(source_dir)
            if f.endswith('.ttf') and f not in (args.skip or [])
        ])

    print(f"\nFonts to process: {len(source_fonts)}")
    if args.skip:
        print(f"Skipping: {', '.join(args.skip)}")

    stats = {'families': 0, 'generated': 0, 'failed': 0}
    start_time = time.time()

    for source_path in source_fonts:
        process_font(source_path, output_dir, stats)

    total_time = time.time() - start_time

    print(f"\n{'='*60}")
    print(f"COMPLETE")
    print(f"{'='*60}")
    print(f"Families processed: {stats['families']}")
    print(f"Font files generated: {stats['generated']}")
    print(f"Failed: {stats['failed']}")
    print(f"Total time: {total_time:.1f}s")

    # Verify if requested
    if args.verify:
        print(f"\n{'='*60}")
        print("VERIFICATION")
        print(f"{'='*60}")
        for root, dirs, files in os.walk(output_dir):
            for f in sorted(files):
                if f.endswith('.ttf'):
                    info = verify_font(os.path.join(root, f))
                    print(f"\n  {info['file']}:")
                    print(f"    Family:     {info['family']}")
                    print(f"    Subfamily:  {info['subfamily']}")
                    print(f"    Full name:  {info['full_name']}")
                    print(f"    PS name:    {info['ps_name']}")
                    print(f"    Typo fam:   {info['typo_family']}")
                    print(f"    Typo sub:   {info['typo_subfamily']}")
                    print(f"    Weight:     {info['weight_class']}")
                    print(f"    fsSelect:   {info['fs_selection']}")
                    print(f"    macStyle:   {info['mac_style']}")


if __name__ == "__main__":
    main()
