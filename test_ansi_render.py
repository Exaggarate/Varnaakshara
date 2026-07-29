#!/usr/bin/env python3
"""
ANSI + Shreelipi Font Render Test
Tests whether ANSI-encoded fonts render their glyphs correctly
without any special backend/shaping engine.

For each font:
1. Read its cmap to find available glyphs
2. Build a sample string from high codepoints (0x80-0xFF range where Indic glyphs live)
3. Render with Pillow and check if pixels actually appear
4. Classify: RENDERS_OK, BLANK (no glyphs), PARTIAL (some glyphs missing)
"""

import os
import sys
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from collections import defaultdict

PROJECT = Path(__file__).parent
FONTS_ANSI = PROJECT / "fonts" / "ansi"
FONTS_BARAHA_EXTRA = PROJECT / "fonts" / "baraha-ansi-extra"
SHREELIPI_DEFFONTS = PROJECT / "shreelipi_extracted" / "fonts" / "DEFFONTS"
SHREELIPI_LNGFONTS = PROJECT / "shreelipi_extracted" / "fonts" / "LNGFONTS"
SHREELIPI_ROOT = PROJECT / "shreelipi_extracted" / "fonts"
OUTPUT_DIR = PROJECT / "test_results" / "ansi_render"

# Language dir mapping
LANG_MAP = {
    "KAN": "Kannada", "DEV": "Devanagari", "TAM": "Tamil",
    "TEL": "Telugu", "MAL": "Malayalam", "GUJ": "Gujarati",
    "BAN": "Bengali", "ASS": "Assamese", "ORI": "Odia",
    "PUN": "Punjabi", "SAN": "Sanskrit", "DIA": "Diacritical",
    "SND": "Sindhi", "ARA": "Arabic",
}

def get_font_cmap(font_path):
    """Extract cmap entries from a font file."""
    try:
        tt = TTFont(str(font_path))
        cmap = tt.getBestCmap()
        tt.close()
        if cmap:
            return cmap  # dict of {codepoint: glyph_name}
    except Exception as e:
        return None
    return None

def get_high_codepoints(cmap):
    """Get codepoints in the 0x80-0xFF range (where ANSI Indic glyphs typically live)."""
    high = [cp for cp in cmap.keys() if 0x80 <= cp <= 0xFF]
    # Also check 0x40-0x7F range (some fonts put glyphs here too)
    mid = [cp for cp in cmap.keys() if 0x40 <= cp < 0x80]
    # And full printable range
    printable = [cp for cp in cmap.keys() if 0x20 <= cp <= 0xFF]
    return high, mid, printable

def render_test(font_path, test_string, font_size=36):
    """Render a string with the font and check if pixels appear."""
    try:
        font = ImageFont.truetype(str(font_path), font_size)
    except Exception as e:
        return None, f"LOAD_FAIL: {e}"
    
    # Create image
    img = Image.new('RGB', (800, 80), 'white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), test_string, font=font, fill='black')
    
    # Check if any non-white pixels exist (excluding the very edges)
    pixels = img.load()
    non_white = 0
    for x in range(10, 790):
        for y in range(10, 70):
            r, g, b = pixels[x, y]
            if r < 250 or g < 250 or b < 250:
                non_white += 1
    
    return img, non_white

def render_full_atlas(font_path, font_size=28):
    """Render ALL glyphs from the font's cmap as an atlas image."""
    cmap = get_font_cmap(font_path)
    if not cmap:
        return None, "NO_CMAP"
    
    try:
        font = ImageFont.truetype(str(font_path), font_size)
    except:
        return None, "LOAD_FAIL"
    
    # Get all codepoints
    cps = sorted([cp for cp in cmap.keys() if 0x20 <= cp <= 0xFFFF])
    if not cps:
        return None, "NO_GLYPHS"
    
    # Render in rows of 16
    cols = 16
    rows = (len(cps) + cols - 1) // cols
    cell_w, cell_h = 50, 50
    img = Image.new('RGB', (cols * cell_w, rows * cell_h + 30), 'white')
    draw = ImageDraw.Draw(img)
    
    # Title
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    except:
        title_font = ImageFont.load_default()
    draw.text((5, 5), f"{font_path.name} — {len(cps)} glyphs", font=title_font, fill='black')
    
    rendered_count = 0
    for i, cp in enumerate(cps):
        row = i // cols
        col = i % cols
        x = col * cell_w
        y = row * cell_h + 30
        
        char = chr(cp)
        # Draw cell border
        draw.rectangle([x, y, x + cell_w - 1, y + cell_h - 1], outline='#ddd')
        
        # Draw the glyph
        draw.text((x + 5, y + 5), char, font=font, fill='black')
        
        # Draw codepoint label
        draw.text((x + 2, y + cell_h - 14), f"{cp:02X}", font=title_font, fill='#999')
        
        # Check if pixels appeared
        has_pixels = False
        for px in range(x + 5, min(x + cell_w - 5, img.width)):
            for py in range(y + 5, min(y + 35, img.height)):
                r, g, b = img.getpixel((px, py))
                if r < 200 or g < 200 or b < 200:
                    has_pixels = True
                    break
            if has_pixels:
                break
        if has_pixels:
            rendered_count += 1
    
    return img, f"{rendered_count}/{len(cps)}"

def classify_font(font_path):
    """Classify a single font: does it render with just Pillow or needs backend?"""
    result = {
        "file": font_path.name,
        "path": str(font_path),
        "status": "UNKNOWN",
        "total_glyphs": 0,
        "high_glyphs": 0,
        "rendered_pixels": 0,
        "details": "",
    }
    
    cmap = get_font_cmap(font_path)
    if cmap is None:
        result["status"] = "NO_CMAP"
        result["details"] = "Could not read font cmap table"
        return result
    
    high, mid, printable = get_high_codepoints(cmap)
    result["total_glyphs"] = len(cmap)
    result["high_glyphs"] = len(high)
    
    # Build test strings
    # Test 1: High codepoints (0x80-0xFF) - where most ANSI Indic glyphs are
    if high:
        test_str = ''.join(chr(cp) for cp in sorted(high)[:30])
        img, pixels = render_test(font_path, test_str)
        if img is None:
            result["status"] = "LOAD_FAIL"
            result["details"] = str(pixels)
            return result
        result["rendered_pixels"] = pixels
        
        if pixels > 50:
            result["status"] = "RENDERS_OK"
            result["details"] = f"High range renders: {pixels} pixels, {len(high)} high glyphs"
        else:
            # Try mid range
            test_str2 = ''.join(chr(cp) for cp in sorted(mid)[:30])
            img2, pixels2 = render_test(font_path, test_str2)
            if pixels2 and pixels2 > 50:
                result["status"] = "RENDERS_MID_ONLY"
                result["details"] = f"High range blank ({pixels}px), mid range renders ({pixels2}px)"
                result["rendered_pixels"] = pixels2
            else:
                result["status"] = "BLANK"
                result["details"] = f"No pixels rendered. High: {pixels}px, Mid: {pixels2}px"
    elif mid:
        test_str = ''.join(chr(cp) for cp in sorted(mid)[:30])
        img, pixels = render_test(font_path, test_str)
        if img is None:
            result["status"] = "LOAD_FAIL"
            result["details"] = str(pixels)
            return result
        result["rendered_pixels"] = pixels if isinstance(pixels, int) else 0
        if isinstance(pixels, int) and pixels > 50:
            result["status"] = "RENDERS_OK"
            result["details"] = f"Mid range only, renders: {pixels} pixels"
        else:
            result["status"] = "BLANK"
            result["details"] = f"Mid range only, {pixels} pixels"
    else:
        result["status"] = "NO_HIGH_GLYPHS"
        result["details"] = f"No glyphs in 0x40-0xFF range, total cmap: {len(cmap)}"
    
    return result

def collect_all_fonts():
    """Collect all ANSI source fonts from all locations."""
    fonts = []
    
    # Baraha ANSI fonts
    if FONTS_ANSI.exists():
        for f in sorted(FONTS_ANSI.glob("*.ttf")):
            fonts.append(("Baraha-ANSI", "mixed", f))
    
    # Baraha ANSI extra
    if FONTS_BARAHA_EXTRA.exists():
        for f in sorted(FONTS_BARAHA_EXTRA.glob("*.ttf")):
            fonts.append(("Baraha-ANSI-Extra", "mixed", f))
    
    # Shreelipi DEFFONTS (per language)
    if SHREELIPI_DEFFONTS.exists():
        for lang_dir in sorted(SHREELIPI_DEFFONTS.iterdir()):
            if lang_dir.is_dir():
                lang = LANG_MAP.get(lang_dir.name, lang_dir.name)
                for f in sorted(lang_dir.glob("*.[tT][tT][fF]")):
                    fonts.append(("Shreelipi-DEF", lang, f))
    
    # Shreelipi LNGFONTS (per language)
    if SHREELIPI_LNGFONTS.exists():
        for lang_dir in sorted(SHREELIPI_LNGFONTS.iterdir()):
            if lang_dir.is_dir():
                lang = LANG_MAP.get(lang_dir.name, lang_dir.name)
                for f in sorted(lang_dir.glob("*.[tT][tT][fF]")):
                    fonts.append(("Shreelipi-LNG", lang, f))
    
    # Root-level Shreelipi fonts
    if SHREELIPI_ROOT.exists():
        for f in sorted(SHREELIPI_ROOT.glob("*.TTF")):
            fonts.append(("Shreelipi-OTF", "Odia", f))
    
    return fonts

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    fonts = collect_all_fonts()
    print(f"Found {len(fonts)} ANSI/Shreelipi source fonts to test\n")
    
    results = {
        "summary": {},
        "by_source": defaultdict(list),
        "by_status": defaultdict(list),
        "by_language": defaultdict(lambda: defaultdict(list)),
    }
    
    renders_ok = 0
    blank = 0
    needs_backend = 0
    
    for i, (source, lang, font_path) in enumerate(fonts):
        print(f"[{i+1}/{len(fonts)}] Testing {font_path.name} ({source}/{lang})...", end=" ")
        
        r = classify_font(font_path)
        r["source"] = source
        r["language"] = lang
        
        results["by_source"][source].append(r)
        results["by_status"][r["status"]].append(r)
        results["by_language"][lang][r["status"]].append(r)
        
        if r["status"] == "RENDERS_OK":
            renders_ok += 1
            print(f"✅ {r['details']}")
        elif r["status"] == "BLANK":
            blank += 1
            needs_backend += 1
            print(f"❌ BLANK — {r['details']}")
        elif r["status"] == "RENDERS_MID_ONLY":
            renders_ok += 1
            print(f"⚠️  {r['details']}")
        else:
            print(f"⚠️  {r['status']}: {r['details']}")
        
        # Generate atlas for interesting cases
        if r["status"] in ("RENDERS_OK", "RENDERS_MID_ONLY", "BLANK"):
            atlas_img, atlas_info = render_full_atlas(font_path)
            if atlas_img:
                safe_name = font_path.stem.replace(" ", "_")
                atlas_path = OUTPUT_DIR / f"atlas_{source}_{lang}_{safe_name}.png"
                atlas_img.save(str(atlas_path))
                r["atlas"] = str(atlas_path)
                r["atlas_info"] = atlas_info
    
    # Generate summary
    print(f"\n{'='*60}")
    print(f"RESULTS SUMMARY")
    print(f"{'='*60}")
    print(f"Total fonts tested: {len(fonts)}")
    print(f"✅ Renders OK: {renders_ok}")
    print(f"❌ Blank/Needs Backend: {blank}")
    print(f"Other: {len(fonts) - renders_ok - blank}")
    
    print(f"\nBy Source:")
    for source in sorted(results["by_source"].keys()):
        items = results["by_source"][source]
        ok = sum(1 for r in items if r["status"] in ("RENDERS_OK", "RENDERS_MID_ONLY"))
        fail = sum(1 for r in items if r["status"] == "BLANK")
        print(f"  {source}: {len(items)} total, {ok} render, {fail} blank")
    
    print(f"\nBy Language:")
    for lang in sorted(results["by_language"].keys()):
        statuses = results["by_language"][lang]
        total = sum(len(v) for v in statuses.values())
        ok = len(statuses.get("RENDERS_OK", [])) + len(statuses.get("RENDERS_MID_ONLY", []))
        fail = len(statuses.get("BLANK", []))
        print(f"  {lang}: {total} total, {ok} render, {fail} blank")
    
    print(f"\n❌ FONTS THAT NEED BACKEND (blank render):")
    for r in results["by_status"].get("BLANK", []):
        print(f"  {r['file']} ({r['source']}/{r['language']}) — {r['total_glyphs']} glyphs, {r['high_glyphs']} high")
    
    # Save JSON report
    report = {
        "total": len(fonts),
        "renders_ok": renders_ok,
        "blank_needs_backend": blank,
        "by_source": {},
        "by_language": {},
        "blank_fonts": [],
        "all_results": [],
    }
    
    for source, items in results["by_source"].items():
        report["by_source"][source] = {
            "total": len(items),
            "ok": sum(1 for r in items if r["status"] in ("RENDERS_OK", "RENDERS_MID_ONLY")),
            "blank": sum(1 for r in items if r["status"] == "BLANK"),
        }
    
    for lang, statuses in results["by_language"].items():
        total = sum(len(v) for v in statuses.values())
        ok = len(statuses.get("RENDERS_OK", [])) + len(statuses.get("RENDERS_MID_ONLY", []))
        fail = len(statuses.get("BLANK", []))
        report["by_language"][lang] = {"total": total, "ok": ok, "blank": fail}
    
    for r in results["by_status"].get("BLANK", []):
        report["blank_fonts"].append({
            "file": r["file"],
            "source": r["source"],
            "language": r["language"],
            "total_glyphs": r["total_glyphs"],
            "high_glyphs": r["high_glyphs"],
        })
    
    for source_items in results["by_source"].values():
        for r in source_items:
            report["all_results"].append({
                k: v for k, v in r.items() if k != "atlas"
            })
    
    report_path = OUTPUT_DIR / "ansi_render_report.json"
    with open(str(report_path), 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved to: {report_path}")
    
    # Generate combined comparison images per language
    print("\nGenerating per-language comparison images...")
    for lang in sorted(results["by_language"].keys()):
        statuses = results["by_language"][lang]
        all_fonts_for_lang = []
        for status_list in statuses.values():
            all_fonts_for_lang.extend(status_list)
        
        if not all_fonts_for_lang:
            continue
        
        # Create comparison image
        row_height = 60
        img_height = len(all_fonts_for_lang) * row_height + 40
        img = Image.new('RGB', (900, img_height), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
        except:
            label_font = ImageFont.load_default()
        
        draw.text((10, 5), f"ANSI Font Render Test — {lang} ({len(all_fonts_for_lang)} fonts)", font=label_font, fill='black')
        draw.line([(0, 30), (900, 30)], fill='#ccc')
        
        for idx, r in enumerate(sorted(all_fonts_for_lang, key=lambda x: x["file"])):
            y = idx * row_height + 35
            status_emoji = "✅" if r["status"] in ("RENDERS_OK", "RENDERS_MID_ONLY") else "❌"
            
            # Status + filename label
            label = f"{status_emoji} {r['file']} [{r['source']}] — {r['total_glyphs']} glyphs"
            draw.text((10, y), label, font=label_font, fill='black' if "OK" in r["status"] else 'red')
            
            # Try to render sample text with this font
            font_path = Path(r["path"])
            if font_path.exists():
                cmap = get_font_cmap(font_path)
                if cmap:
                    high_cps = sorted([cp for cp in cmap.keys() if 0x40 <= cp <= 0xFF])[:40]
                    if high_cps:
                        test_str = ''.join(chr(cp) for cp in high_cps)
                        try:
                            test_font = ImageFont.truetype(str(font_path), 24)
                            draw.text((10, y + 16), test_str, font=test_font, fill='#333')
                        except:
                            pass
            
            draw.line([(0, y + row_height - 2), (900, y + row_height - 2)], fill='#eee')
        
        comp_path = OUTPUT_DIR / f"comparison_{lang.lower()}.png"
        img.save(str(comp_path))
        print(f"  Saved {comp_path.name}")

if __name__ == "__main__":
    main()
