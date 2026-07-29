#!/usr/bin/env python3
"""
Extract keyboard layouts for ALL Indian languages from Shree-Lipi 7.4 compose files.

Compose files are 406 bytes:
  - Bytes 0x00-0x1F: Identity mapping (control codes)
  - Bytes 0x20-0x7F: Key-to-ISCII mapping (96 entries)
    Position = ASCII code of key pressed
    Value = ISCII code output (0xA0-0xFF range = Indian script chars)
  - Bytes 0x80-0x195: Extended data (IDV-like compose sequences, ignored here for base layout)
  
ISCII (IS 13194:1991) uses a shared layout across all Indian scripts.
Unicode blocks mirror this layout with different base offsets.
"""

import json
import os
import glob
import sys
from pathlib import Path

# ---- Configuration ----

COMPOSE_BASE = "/tmp/SL74DVD/COMMON/COMPOSE"
OUTPUT_DIR = "/root/.openclaw/workspace/varnaakshara-ime/shreelipi_extracted"

# Language definitions: (directory, compose extension, unicode_base, script_name)
LANGUAGES = {
    "devanagari": {
        "dir": "DEV",
        "compose_ext": ".DEV",
        "compose_ext_alt": ".dev",
        "unicode_base": 0x0900,
        "script_name": "Devanagari",
    },
    "assamese": {
        "dir": "ASS",
        "compose_ext": ".ASS",
        "compose_ext_alt": ".ass",
        "unicode_base": 0x0980,  # Same block as Bengali
        "script_name": "Assamese (Bengali script)",
    },
    "bengali": {
        "dir": "BAN",
        "compose_ext": ".BAN",
        "compose_ext_alt": ".ban",
        "unicode_base": 0x0980,
        "script_name": "Bengali",
    },
    "gujarati": {
        "dir": "GUJ",
        "compose_ext": ".GUJ",
        "compose_ext_alt": ".guj",
        "unicode_base": 0x0A80,
        "script_name": "Gujarati",
    },
    "gurmukhi": {
        "dir": "PUN",
        "compose_ext": ".PUN",
        "compose_ext_alt": ".pun",
        "unicode_base": 0x0A00,
        "script_name": "Gurmukhi (Punjabi)",
    },
    "kannada": {
        "dir": "KAN",
        "compose_ext": ".KAN",
        "compose_ext_alt": ".kan",
        "unicode_base": 0x0C80,
        "script_name": "Kannada",
    },
    "malayalam": {
        "dir": "MAL",
        "compose_ext": ".MAL",
        "compose_ext_alt": ".mal",
        "unicode_base": 0x0D00,
        "script_name": "Malayalam",
    },
    "oriya": {
        "dir": "ORI",
        "compose_ext": ".ORI",
        "compose_ext_alt": ".ori",
        "unicode_base": 0x0B00,
        "script_name": "Odia (Oriya)",
    },
    "tamil": {
        "dir": "TAM",
        "compose_ext": ".TAM",
        "compose_ext_alt": ".tam",
        "unicode_base": 0x0B80,
        "script_name": "Tamil",
    },
    "telugu": {
        "dir": "TEL",
        "compose_ext": ".TEL",
        "compose_ext_alt": ".tel",
        "unicode_base": 0x0C00,
        "script_name": "Telugu",
    },
}

# ISCII to Unicode offset table (IS 13194:1991)
# Maps ISCII code -> offset from Unicode script base
ISCII_TO_UNICODE_OFFSET = {
    0xA1: 0x01,  # Candrabindu
    0xA2: 0x02,  # Anusvara
    0xA3: 0x03,  # Visarga
    0xA4: 0x05,  # Vowel A
    0xA5: 0x06,  # Vowel AA
    0xA6: 0x07,  # Vowel I
    0xA7: 0x08,  # Vowel II
    0xA8: 0x09,  # Vowel U
    0xA9: 0x0A,  # Vowel UU
    0xAA: 0x0B,  # Vowel Vocalic R
    0xAB: 0x0E,  # Vowel Short E (scripts that have it)
    0xAC: 0x0F,  # Vowel E
    0xAD: 0x10,  # Vowel AI
    0xAE: 0x0D,  # Vowel Candra E (Devanagari-specific)
    0xAF: 0x12,  # Vowel Short O (scripts that have it)
    0xB0: 0x13,  # Vowel O
    0xB1: 0x14,  # Vowel AU
    0xB2: 0x11,  # Vowel Candra O (Devanagari-specific)
    0xB3: 0x15,  # Ka
    0xB4: 0x16,  # Kha
    0xB5: 0x17,  # Ga
    0xB6: 0x18,  # Gha
    0xB7: 0x19,  # Nga
    0xB8: 0x1A,  # Cha
    0xB9: 0x1B,  # Chha
    0xBA: 0x1C,  # Ja
    0xBB: 0x1D,  # Jha
    0xBC: 0x1E,  # Nya
    0xBD: 0x1F,  # Tta
    0xBE: 0x20,  # Ttha
    0xBF: 0x21,  # Dda
    0xC0: 0x22,  # Ddha
    0xC1: 0x23,  # Nna
    0xC2: 0x24,  # Ta
    0xC3: 0x25,  # Tha
    0xC4: 0x26,  # Da
    0xC5: 0x27,  # Dha
    0xC6: 0x28,  # Na
    0xC7: 0x29,  # Nnna (not used in some scripts)
    0xC8: 0x2A,  # Pa
    0xC9: 0x2B,  # Pha
    0xCA: 0x2C,  # Ba
    0xCB: 0x2D,  # Bha
    0xCC: 0x2E,  # Ma
    0xCD: 0x2F,  # Ya
    0xCE: 0x30,  # Ra
    0xCF: 0x32,  # La
    0xD0: 0x33,  # Lla
    0xD1: 0x34,  # Llla (not used in some scripts)
    0xD2: 0x35,  # Va/Wa
    0xD3: 0x36,  # Sha
    0xD4: 0x37,  # Ssa
    0xD5: 0x38,  # Sa
    0xD6: 0x39,  # Ha
    0xD7: 0x00,  # Undefined/reserved
    0xD8: 0x4D,  # Virama/Halant
    0xD9: 0x3C,  # Nukta
    # 0xDA: ATR (script-specific extension)
    # 0xDB: EXT (script-specific extension)
    # 0xDC-0xDF: reserved
    0xE0: 0x3E,  # AA matra (dependent vowel)
    0xE1: 0x3F,  # I matra
    0xE2: 0x40,  # II matra
    0xE3: 0x41,  # U matra
    0xE4: 0x42,  # UU matra
    0xE5: 0x43,  # Vocalic R matra
    0xE6: 0x46,  # Short E matra
    0xE7: 0x47,  # E matra
    0xE8: 0x48,  # AI matra
    0xE9: 0x45,  # Candra E matra
    0xEA: 0x4A,  # Short O matra
    0xEB: 0x4B,  # O matra
    0xEC: 0x4C,  # AU matra
    0xED: 0x49,  # Candra O matra
}

# ISCII character names for readable output
ISCII_NAMES = {
    0xA1: "candrabindu",
    0xA2: "anusvara",
    0xA3: "visarga",
    0xA4: "vowel_a",
    0xA5: "vowel_aa",
    0xA6: "vowel_i",
    0xA7: "vowel_ii",
    0xA8: "vowel_u",
    0xA9: "vowel_uu",
    0xAA: "vowel_vocalic_r",
    0xAB: "vowel_short_e",
    0xAC: "vowel_e",
    0xAD: "vowel_ai",
    0xAE: "vowel_candra_e",
    0xAF: "vowel_short_o",
    0xB0: "vowel_o",
    0xB1: "vowel_au",
    0xB2: "vowel_candra_o",
    0xB3: "ka",
    0xB4: "kha",
    0xB5: "ga",
    0xB6: "gha",
    0xB7: "nga",
    0xB8: "cha",
    0xB9: "chha",
    0xBA: "ja",
    0xBB: "jha",
    0xBC: "nya",
    0xBD: "tta",
    0xBE: "ttha",
    0xBF: "dda",
    0xC0: "ddha",
    0xC1: "nna",
    0xC2: "ta",
    0xC3: "tha",
    0xC4: "da",
    0xC5: "dha",
    0xC6: "na",
    0xC7: "nnna",
    0xC8: "pa",
    0xC9: "pha",
    0xCA: "ba",
    0xCB: "bha",
    0xCC: "ma",
    0xCD: "ya",
    0xCE: "ra",
    0xCF: "la",
    0xD0: "lla",
    0xD1: "llla",
    0xD2: "va",
    0xD3: "sha",
    0xD4: "ssa",
    0xD5: "sa",
    0xD6: "ha",
    0xD7: "reserved",
    0xD8: "halant",
    0xD9: "nukta",
    0xDA: "atr",
    0xDB: "ext",
    0xE0: "matra_aa",
    0xE1: "matra_i",
    0xE2: "matra_ii",
    0xE3: "matra_u",
    0xE4: "matra_uu",
    0xE5: "matra_vocalic_r",
    0xE6: "matra_short_e",
    0xE7: "matra_e",
    0xE8: "matra_ai",
    0xE9: "matra_candra_e",
    0xEA: "matra_short_o",
    0xEB: "matra_o",
    0xEC: "matra_au",
    0xED: "matra_candra_o",
}


def iscii_to_unicode(iscii_byte: int, unicode_base: int) -> str | None:
    """Convert an ISCII byte to a Unicode character for the given script base.
    
    Returns the Unicode character string, or None if unmapped/reserved.
    """
    if iscii_byte in ISCII_TO_UNICODE_OFFSET:
        offset = ISCII_TO_UNICODE_OFFSET[iscii_byte]
        if offset == 0x00 and iscii_byte == 0xD7:
            # Reserved/undefined
            return None
        code_point = unicode_base + offset
        try:
            char = chr(code_point)
            return char
        except (ValueError, OverflowError):
            return None
    # Check if it's in the Devanagari digits range or other ISCII specials
    if 0xF1 <= iscii_byte <= 0xFA:
        # ISCII digits (Devanagari digits mapped to script-specific digits)
        # 0xF1=1, 0xF2=2, ... 0xFA=0 (or 0xF1-0xF9 = 1-9, 0xFA = 0)
        digit_offset = iscii_byte - 0xF1  # 0-9
        code_point = unicode_base + 0x66 + digit_offset  # Script digits start at base+0x66
        try:
            return chr(code_point)
        except (ValueError, OverflowError):
            return None
    return None


def get_key_label(ascii_code: int) -> str:
    """Get a human-readable label for an ASCII key code."""
    if ascii_code == 0x20:
        return "Space"
    elif 0x21 <= ascii_code <= 0x7E:
        return chr(ascii_code)
    elif ascii_code == 0x7F:
        return "DEL"
    else:
        return f"0x{ascii_code:02X}"


def is_shifted(ascii_code: int) -> bool:
    """Determine if a key requires Shift based on its ASCII code."""
    # Shifted keys: A-Z (0x41-0x5A) and the symbols: ! " # $ % & ( ) * + < > ? @ ^ _ { | } ~
    if 0x41 <= ascii_code <= 0x5A:
        return True
    shifted_symbols = set('!"#$%&()*+<>?@^_{}|~')
    if 0x21 <= ascii_code <= 0x7E and chr(ascii_code) in shifted_symbols:
        return True
    return False


def parse_compose_file(filepath: str, unicode_base: int) -> dict:
    """Parse a single Shree-Lipi compose file and extract the keyboard layout.
    
    Returns a dict with layout name and key mappings.
    """
    with open(filepath, "rb") as f:
        data = f.read()
    
    if len(data) < 128:
        return None
    
    layout_name = Path(filepath).stem
    
    mappings = {}
    normal_keys = {}  # unshifted
    shift_keys = {}   # shifted
    
    # Process bytes 0x20 to 0x7F (96 key positions)
    for pos in range(0x20, min(0x80, len(data))):
        byte_val = data[pos]
        ascii_key = pos
        key_char = get_key_label(ascii_key)
        
        # Skip if passthrough (value == position) or unmapped (0xFF)
        if byte_val == pos:
            continue
        if byte_val == 0xFF:
            continue
        
        # Check if it's an ISCII character (0xA0-0xFF range)
        if byte_val >= 0xA0:
            unicode_char = iscii_to_unicode(byte_val, unicode_base)
            iscii_name = ISCII_NAMES.get(byte_val, f"iscii_0x{byte_val:02X}")
            
            entry = {
                "key": key_char,
                "ascii_code": ascii_key,
                "iscii_code": f"0x{byte_val:02X}",
                "iscii_name": iscii_name,
                "unicode_char": unicode_char,
                "unicode_codepoint": f"U+{ord(unicode_char):04X}" if unicode_char else None,
                "shifted": is_shifted(ascii_key),
            }
            mappings[key_char] = entry
            
            if is_shifted(ascii_key):
                shift_keys[key_char] = entry
            else:
                normal_keys[key_char] = entry
        else:
            # Maps to another ASCII character (remapping)
            target_char = chr(byte_val) if 0x20 <= byte_val <= 0x7E else f"0x{byte_val:02X}"
            entry = {
                "key": key_char,
                "ascii_code": ascii_key,
                "maps_to_ascii": target_char,
                "maps_to_code": f"0x{byte_val:02X}",
                "shifted": is_shifted(ascii_key),
                "type": "ascii_remap",
            }
            mappings[key_char] = entry
            if is_shifted(ascii_key):
                shift_keys[key_char] = entry
            else:
                normal_keys[key_char] = entry
    
    return {
        "layout_name": layout_name,
        "file": os.path.basename(filepath),
        "file_size": len(data),
        "total_mappings": len(mappings),
        "iscii_mappings": sum(1 for m in mappings.values() if "iscii_code" in m),
        "ascii_remaps": sum(1 for m in mappings.values() if m.get("type") == "ascii_remap"),
        "normal_keys": normal_keys,
        "shift_keys": shift_keys,
        "all_mappings": mappings,
    }


def process_language(lang_key: str, lang_config: dict) -> dict:
    """Process all compose files for a single language."""
    lang_dir = os.path.join(COMPOSE_BASE, lang_config["dir"])
    unicode_base = lang_config["unicode_base"]
    
    # Find compose files with both case variants
    compose_files = []
    for ext in [lang_config["compose_ext"], lang_config["compose_ext_alt"]]:
        pattern = os.path.join(lang_dir, f"*{ext}")
        compose_files.extend(glob.glob(pattern))
    
    # Also try case-insensitive matching
    if os.path.isdir(lang_dir):
        target_ext = lang_config["compose_ext"].upper()
        for f in os.listdir(lang_dir):
            full_path = os.path.join(lang_dir, f)
            if os.path.isfile(full_path) and f.upper().endswith(target_ext):
                if full_path not in compose_files:
                    compose_files.append(full_path)
    
    # Deduplicate and sort
    compose_files = sorted(set(compose_files))
    
    # Filter to only 406-byte files (proper compose files)
    compose_files = [f for f in compose_files if os.path.getsize(f) == 406]
    
    layouts = []
    for filepath in compose_files:
        layout = parse_compose_file(filepath, unicode_base)
        if layout:
            layouts.append(layout)
    
    return {
        "language": lang_key,
        "script_name": lang_config["script_name"],
        "unicode_base": f"U+{unicode_base:04X}",
        "compose_directory": lang_dir,
        "total_layouts": len(layouts),
        "layouts": layouts,
    }


def generate_summary(all_results: dict) -> str:
    """Generate a markdown summary of all extracted layouts."""
    lines = []
    lines.append("# Shree-Lipi 7.4 - All Indian Language Keyboard Layouts Summary")
    lines.append("")
    lines.append(f"**Source:** `/tmp/SL74DVD/COMMON/COMPOSE/`")
    lines.append(f"**Total languages:** {len(all_results)}")
    total_layouts = sum(r["total_layouts"] for r in all_results.values())
    lines.append(f"**Total keyboard layouts extracted:** {total_layouts}")
    lines.append("")
    
    lines.append("## Overview")
    lines.append("")
    lines.append("| Language | Script | Unicode Base | Layouts | Compose Dir |")
    lines.append("|----------|--------|-------------|---------|-------------|")
    for lang_key, result in sorted(all_results.items()):
        lines.append(f"| {lang_key.title()} | {result['script_name']} | {result['unicode_base']} | {result['total_layouts']} | {result['compose_directory'].split('/')[-1]} |")
    lines.append("")
    
    # Per-language details
    for lang_key, result in sorted(all_results.items()):
        lines.append(f"## {result['script_name']} ({lang_key.title()})")
        lines.append("")
        lines.append(f"- **Unicode base:** {result['unicode_base']}")
        lines.append(f"- **Total layouts:** {result['total_layouts']}")
        lines.append("")
        
        if result["layouts"]:
            lines.append("### Layout List")
            lines.append("")
            lines.append("| Layout | File | ISCII Mappings | ASCII Remaps | Total |")
            lines.append("|--------|------|---------------|-------------|-------|")
            for layout in result["layouts"]:
                lines.append(f"| {layout['layout_name']} | {layout['file']} | {layout['iscii_mappings']} | {layout['ascii_remaps']} | {layout['total_mappings']} |")
            lines.append("")
            
            # Show INSCRIPT layout detail if available (it's the standard)
            inscript = None
            for layout in result["layouts"]:
                if "INSCRIPT" in layout["layout_name"].upper():
                    inscript = layout
                    break
            
            if inscript:
                lines.append(f"### INSCRIPT Layout Detail ({lang_key.title()})")
                lines.append("")
                lines.append("#### Normal (Unshifted) Keys")
                lines.append("")
                lines.append("| Key | ISCII | Character Name | Unicode | Char |")
                lines.append("|-----|-------|---------------|---------|------|")
                for key, m in sorted(inscript["normal_keys"].items(), key=lambda x: x[1]["ascii_code"]):
                    if "iscii_code" in m:
                        char_display = m.get("unicode_char", "")
                        lines.append(f"| `{key}` | {m['iscii_code']} | {m.get('iscii_name', '')} | {m.get('unicode_codepoint', '')} | {char_display} |")
                    else:
                        lines.append(f"| `{key}` | - | ASCII remap → `{m.get('maps_to_ascii', '')}` | - | - |")
                lines.append("")
                
                lines.append("#### Shifted Keys")
                lines.append("")
                lines.append("| Key | ISCII | Character Name | Unicode | Char |")
                lines.append("|-----|-------|---------------|---------|------|")
                for key, m in sorted(inscript["shift_keys"].items(), key=lambda x: x[1]["ascii_code"]):
                    if "iscii_code" in m:
                        char_display = m.get("unicode_char", "")
                        lines.append(f"| `{key}` | {m['iscii_code']} | {m.get('iscii_name', '')} | {m.get('unicode_codepoint', '')} | {char_display} |")
                    else:
                        lines.append(f"| `{key}` | - | ASCII remap → `{m.get('maps_to_ascii', '')}` | - | - |")
                lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_results = {}
    
    for lang_key, lang_config in sorted(LANGUAGES.items()):
        print(f"Processing {lang_key} ({lang_config['script_name']})...")
        result = process_language(lang_key, lang_config)
        all_results[lang_key] = result
        
        # Save per-language JSON
        output_file = os.path.join(OUTPUT_DIR, f"keyboard_layouts_{lang_key}.json")
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"  → {result['total_layouts']} layouts saved to {output_file}")
    
    # Save combined summary JSON
    combined_file = os.path.join(OUTPUT_DIR, "keyboard_layouts_all.json")
    with open(combined_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\nCombined JSON saved to {combined_file}")
    
    # Generate markdown summary
    summary = generate_summary(all_results)
    summary_file = os.path.join(OUTPUT_DIR, "all_languages_summary.md")
    with open(summary_file, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"Summary saved to {summary_file}")
    
    # Print quick stats
    print("\n=== Extraction Summary ===")
    total = 0
    for lang_key, result in sorted(all_results.items()):
        print(f"  {lang_key:12s}: {result['total_layouts']:3d} layouts")
        total += result['total_layouts']
    print(f"  {'TOTAL':12s}: {total:3d} layouts")


if __name__ == "__main__":
    main()
