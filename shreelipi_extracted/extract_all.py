#!/usr/bin/env python3
"""
Shree-Lipi 7.4 Keyboard Layout Extractor
Extracts ISCII compose files (.DEV, .BAN, .GUJ, etc.) and maps to Unicode.
"""
import os, json, struct, sys

# ── ISCII → Unicode offset table (IS 13194:1991) ──
# Maps ISCII code (0xA0-0xFF) to offset within Unicode script block
ISCII_TO_UNICODE_OFFSET = {
    0xA1: 0x01,  # candrabindu
    0xA2: 0x02,  # anusvara
    0xA3: 0x03,  # visarga
    0xA4: 0x05,  # a
    0xA5: 0x06,  # aa
    0xA6: 0x07,  # i
    0xA7: 0x08,  # ii
    0xA8: 0x09,  # u
    0xA9: 0x0A,  # uu
    0xAA: 0x0B,  # vocalic r
    0xAB: 0x0E,  # short e (Dravidian)
    0xAC: 0x0F,  # e
    0xAD: 0x10,  # ai
    0xAE: 0x0D,  # candra e
    0xAF: 0x12,  # short o (Dravidian)
    0xB0: 0x13,  # o
    0xB1: 0x14,  # au
    0xB2: 0x11,  # candra o
    0xB3: 0x15,  # ka
    0xB4: 0x16,  # kha
    0xB5: 0x17,  # ga
    0xB6: 0x18,  # gha
    0xB7: 0x19,  # nga
    0xB8: 0x1A,  # cha
    0xB9: 0x1B,  # chha
    0xBA: 0x1C,  # ja
    0xBB: 0x1D,  # jha
    0xBC: 0x1E,  # nya
    0xBD: 0x1F,  # tta
    0xBE: 0x20,  # ttha
    0xBF: 0x21,  # dda
    0xC0: 0x22,  # ddha
    0xC1: 0x23,  # nna
    0xC2: 0x24,  # ta
    0xC3: 0x25,  # tha
    0xC4: 0x26,  # da
    0xC5: 0x27,  # dha
    0xC6: 0x28,  # na
    0xC7: 0x29,  # nnna (used in some scripts)
    0xC8: 0x2A,  # pa
    0xC9: 0x2B,  # pha
    0xCA: 0x2C,  # ba
    0xCB: 0x2D,  # bha
    0xCC: 0x2E,  # ma
    0xCD: 0x2F,  # ya
    0xCE: 0x30,  # ra
    0xCF: 0x32,  # la
    0xD0: 0x33,  # lla
    0xD1: 0x34,  # llla (used in some scripts)
    0xD2: 0x35,  # va/wa
    0xD3: 0x36,  # sha
    0xD4: 0x37,  # ssa
    0xD5: 0x38,  # sa
    0xD6: 0x39,  # ha
    0xD8: 0x4D,  # virama/halant
    0xD9: 0x3C,  # nukta
    0xDA: 0x3D,  # avagraha (ATR marker in ISCII)
    0xE0: 0x3E,  # aa matra
    0xE1: 0x3F,  # i matra
    0xE2: 0x40,  # ii matra
    0xE3: 0x41,  # u matra
    0xE4: 0x42,  # uu matra
    0xE5: 0x43,  # vocalic r matra
    0xE6: 0x46,  # short e matra (Dravidian)
    0xE7: 0x47,  # e matra
    0xE8: 0x48,  # ai matra
    0xE9: 0x45,  # candra e matra
    0xEA: 0x4A,  # short o matra (Dravidian)
    0xEB: 0x4B,  # o matra
    0xEC: 0x4C,  # au matra
    0xED: 0x49,  # candra o matra
    0xF0: 0x66,  # digit 0
    0xF1: 0x67,  # digit 1
    0xF2: 0x68,  # digit 2
    0xF3: 0x69,  # digit 3
    0xF4: 0x6A,  # digit 4
    0xF5: 0x6B,  # digit 5
    0xF6: 0x6C,  # digit 6
    0xF7: 0x6D,  # digit 7
    0xF8: 0x6E,  # digit 8
    0xF9: 0x6F,  # digit 9
}

# ISCII character names
ISCII_NAMES = {
    0xA1: "candrabindu", 0xA2: "anusvara", 0xA3: "visarga",
    0xA4: "a", 0xA5: "aa", 0xA6: "i", 0xA7: "ii",
    0xA8: "u", 0xA9: "uu", 0xAA: "vocalic_r",
    0xAB: "short_e", 0xAC: "e", 0xAD: "ai",
    0xAE: "candra_e", 0xAF: "short_o", 0xB0: "o", 0xB1: "au",
    0xB2: "candra_o",
    0xB3: "ka", 0xB4: "kha", 0xB5: "ga", 0xB6: "gha", 0xB7: "nga",
    0xB8: "cha", 0xB9: "chha", 0xBA: "ja", 0xBB: "jha", 0xBC: "nya",
    0xBD: "tta", 0xBE: "ttha", 0xBF: "dda", 0xC0: "ddha", 0xC1: "nna",
    0xC2: "ta", 0xC3: "tha", 0xC4: "da", 0xC5: "dha", 0xC6: "na",
    0xC7: "nnna", 0xC8: "pa", 0xC9: "pha", 0xCA: "ba", 0xCB: "bha",
    0xCC: "ma", 0xCD: "ya", 0xCE: "ra", 0xCF: "la",
    0xD0: "lla", 0xD1: "llla", 0xD2: "va", 0xD3: "sha",
    0xD4: "ssa", 0xD5: "sa", 0xD6: "ha",
    0xD8: "halant", 0xD9: "nukta", 0xDA: "avagraha",
    0xE0: "aa_matra", 0xE1: "i_matra", 0xE2: "ii_matra",
    0xE3: "u_matra", 0xE4: "uu_matra", 0xE5: "vocalic_r_matra",
    0xE6: "short_e_matra", 0xE7: "e_matra", 0xE8: "ai_matra",
    0xE9: "candra_e_matra", 0xEA: "short_o_matra",
    0xEB: "o_matra", 0xEC: "au_matra", 0xED: "candra_o_matra",
    0xF0: "digit_0", 0xF1: "digit_1", 0xF2: "digit_2",
    0xF3: "digit_3", 0xF4: "digit_4", 0xF5: "digit_5",
    0xF6: "digit_6", 0xF7: "digit_7", 0xF8: "digit_8", 0xF9: "digit_9",
}

# Language configs
LANGUAGES = {
    "devanagari": {"dir": "DEV", "ext": ".DEV", "idv_ext": ".IDV", "base": 0x0900, "name": "Devanagari"},
    "bengali":    {"dir": "BAN", "ext": ".BAN", "idv_ext": ".IBA", "base": 0x0980, "name": "Bengali"},
    "assamese":   {"dir": "ASS", "ext": ".ASS", "idv_ext": ".IAS", "base": 0x0980, "name": "Assamese"},
    "gujarati":   {"dir": "GUJ", "ext": ".GUJ", "idv_ext": ".IGU", "base": 0x0A80, "name": "Gujarati"},
    "kannada":    {"dir": "KAN", "ext": ".KAN", "idv_ext": ".IKA", "base": 0x0C80, "name": "Kannada"},
    "malayalam":  {"dir": "MAL", "ext": ".MAL", "idv_ext": ".IMA", "base": 0x0D00, "name": "Malayalam"},
    "oriya":      {"dir": "ORI", "ext": ".ORI", "idv_ext": ".IOR", "base": 0x0B00, "name": "Oriya"},
    "punjabi":    {"dir": "PUN", "ext": ".PUN", "idv_ext": ".IPU", "base": 0x0A00, "name": "Punjabi"},
    "tamil":      {"dir": "TAM", "ext": ".TAM", "idv_ext": ".ITA", "base": 0x0B80, "name": "Tamil"},
    "telugu":     {"dir": "TEL", "ext": ".TEL", "idv_ext": ".ITE", "base": 0x0C00, "name": "Telugu"},
}

COMPOSE_BASE = "/tmp/SL74DVD/COMMON/COMPOSE"
OUTPUT_DIR = "/root/.openclaw/workspace/varnaakshara-ime/shreelipi_extracted"

def iscii_to_unicode(iscii_byte, script_base):
    """Convert an ISCII byte to a Unicode character."""
    if iscii_byte in ISCII_TO_UNICODE_OFFSET:
        offset = ISCII_TO_UNICODE_OFFSET[iscii_byte]
        return chr(script_base + offset)
    return None

def iscii_to_name(iscii_byte):
    """Get the name of an ISCII character."""
    return ISCII_NAMES.get(iscii_byte, f"iscii_0x{iscii_byte:02X}")

def parse_compose_file(filepath, script_base):
    """Parse a 406-byte Shree-Lipi compose file."""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    if len(data) != 406:
        return None, f"Unexpected size: {len(data)} (expected 406)"
    
    # Key labels for ASCII 0x20-0x7F
    key_labels = {}
    for i in range(0x20, 0x80):
        if i == 0x7F:
            key_labels[i] = "DEL"
        else:
            key_labels[i] = chr(i)
    
    mappings = {}
    stats = {"total_keys": 0, "iscii_mapped": 0, "passthrough": 0, "unmapped": 0}
    
    for pos in range(0x20, 0x80):
        byte_val = data[pos]
        key = key_labels[pos]
        stats["total_keys"] += 1
        
        if byte_val == 0xFF:
            stats["unmapped"] += 1
            continue
        
        if byte_val == pos:
            # Passthrough - key produces itself
            stats["passthrough"] += 1
            mappings[key] = {
                "iscii": f"0x{byte_val:02X}",
                "type": "passthrough",
                "output": chr(byte_val),
                "unicode_hex": f"U+{byte_val:04X}"
            }
            continue
        
        # ISCII character mapping
        unicode_char = iscii_to_unicode(byte_val, script_base)
        if unicode_char:
            stats["iscii_mapped"] += 1
            mappings[key] = {
                "iscii": f"0x{byte_val:02X}",
                "iscii_name": iscii_to_name(byte_val),
                "type": "iscii",
                "output": unicode_char,
                "unicode_hex": f"U+{ord(unicode_char):04X}",
                "unicode_name": iscii_to_name(byte_val)
            }
        elif byte_val < 0x80:
            # Maps to a different ASCII character
            stats["passthrough"] += 1
            mappings[key] = {
                "iscii": f"0x{byte_val:02X}",
                "type": "ascii_remap",
                "output": chr(byte_val),
                "unicode_hex": f"U+{byte_val:04X}"
            }
        else:
            # Unknown ISCII code
            stats["iscii_mapped"] += 1
            mappings[key] = {
                "iscii": f"0x{byte_val:02X}",
                "type": "unknown_iscii",
                "output": f"[ISCII 0x{byte_val:02X}]",
                "note": "ISCII code not in standard mapping table"
            }
    
    return mappings, stats

def parse_idv_file(filepath, script_base):
    """Parse a 501-byte Shree-Lipi IDV (compose sequence) file."""
    with open(filepath, 'rb') as f:
        data = f.read()
    
    if len(data) < 256:
        return None
    
    # First 128 bytes: same as compose file (key mapping)
    # Bytes 128-255: modifier/shift layer
    # Bytes 256+: compose sequences (dead key rules)
    
    compose_sequences = []
    
    # Parse compose sequence area (bytes 0x80 onward)
    # Format appears to be: length, seq_byte1, seq_byte2, ..., result_byte
    pos = 0x80
    while pos < len(data):
        if data[pos] == 0xFF:
            pos += 1
            continue
        
        # Look for compose sequence markers (0x04 prefix based on hexdump analysis)
        if pos < len(data) - 2 and data[pos] == 0x04:
            # Read sequence until 0xFF or 0x04
            seq_start = pos + 1
            seq_end = seq_start
            while seq_end < len(data) and data[seq_end] != 0xFF and data[seq_end] != 0x04:
                seq_end += 1
            
            if seq_end > seq_start:
                seq_bytes = data[seq_start:seq_end]
                # Convert ISCII bytes to Unicode
                unicode_seq = []
                for b in seq_bytes:
                    uc = iscii_to_unicode(b, script_base)
                    if uc:
                        unicode_seq.append(uc)
                    elif 0x20 <= b < 0x80:
                        unicode_seq.append(chr(b))
                    else:
                        unicode_seq.append(f"[0x{b:02X}]")
                
                compose_sequences.append({
                    "raw_bytes": [f"0x{b:02X}" for b in seq_bytes],
                    "iscii_names": [iscii_to_name(b) if b in ISCII_NAMES else f"0x{b:02X}" for b in seq_bytes],
                    "unicode": "".join(unicode_seq)
                })
            
            pos = seq_end
        else:
            pos += 1
    
    return compose_sequences

def extract_language(lang_key, lang_config):
    """Extract all keyboard layouts for a language."""
    compose_dir = os.path.join(COMPOSE_BASE, lang_config["dir"])
    if not os.path.isdir(compose_dir):
        return None
    
    ext_upper = lang_config["ext"].upper()
    ext_lower = lang_config["ext"].lower()
    idv_upper = lang_config["idv_ext"].upper()
    idv_lower = lang_config["idv_ext"].lower()
    
    layouts = {}
    
    for fname in sorted(os.listdir(compose_dir)):
        fpath = os.path.join(compose_dir, fname)
        
        # Check if it's a compose file (406 bytes, correct extension)
        fname_upper = fname.upper()
        name_part = os.path.splitext(fname)[0]
        file_ext = os.path.splitext(fname)[1]
        
        if file_ext.upper() == ext_upper and os.path.getsize(fpath) == 406:
            mappings, stats = parse_compose_file(fpath, lang_config["base"])
            if mappings:
                layout_name = name_part
                
                # Also try to find matching IDV file
                idv_candidates = [
                    name_part + idv_upper,
                    name_part + idv_lower,
                    name_part.upper() + idv_upper,
                    name_part.lower() + idv_lower,
                    name_part.upper() + idv_lower,
                    name_part.lower() + idv_upper,
                ]
                
                compose_seqs = None
                for idv_name in idv_candidates:
                    idv_path = os.path.join(compose_dir, idv_name)
                    if os.path.exists(idv_path):
                        compose_seqs = parse_idv_file(idv_path, lang_config["base"])
                        break
                
                # Also try case-insensitive search
                if compose_seqs is None:
                    for f2 in os.listdir(compose_dir):
                        f2_name = os.path.splitext(f2)[0]
                        f2_ext = os.path.splitext(f2)[1]
                        if f2_name.upper() == name_part.upper() and f2_ext.upper() in (idv_upper, idv_lower.upper()):
                            idv_path = os.path.join(compose_dir, f2)
                            if os.path.getsize(idv_path) == 501:
                                compose_seqs = parse_idv_file(idv_path, lang_config["base"])
                                break
                
                layouts[layout_name] = {
                    "file": fname,
                    "stats": stats,
                    "key_mappings": mappings,
                }
                if compose_seqs:
                    layouts[layout_name]["compose_sequences"] = compose_seqs
    
    return layouts

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    summary_lines = ["# Shree-Lipi 7.4 Keyboard Layout Extraction Summary\n"]
    summary_lines.append(f"Extracted from: `/tmp/SL74DVD/COMMON/COMPOSE/`\n")
    
    total_layouts = 0
    
    for lang_key, lang_config in sorted(LANGUAGES.items()):
        print(f"Extracting {lang_config['name']}...")
        layouts = extract_language(lang_key, lang_config)
        
        if not layouts:
            print(f"  No layouts found for {lang_config['name']}")
            summary_lines.append(f"\n## {lang_config['name']}\nNo layouts found.\n")
            continue
        
        # Save JSON
        output = {
            "language": lang_config["name"],
            "script_unicode_base": f"U+{lang_config['base']:04X}",
            "total_layouts": len(layouts),
            "layouts": layouts
        }
        
        out_path = os.path.join(OUTPUT_DIR, f"keyboard_layouts_{lang_key}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        total_layouts += len(layouts)
        
        # Summary
        summary_lines.append(f"\n## {lang_config['name']} ({lang_config['dir']})")
        summary_lines.append(f"- Unicode block base: U+{lang_config['base']:04X}")
        summary_lines.append(f"- Layouts extracted: **{len(layouts)}**")
        summary_lines.append(f"- Output: `keyboard_layouts_{lang_key}.json`")
        summary_lines.append(f"\n| Layout Name | ISCII Keys | Passthrough | Unmapped |")
        summary_lines.append(f"|-------------|-----------|-------------|----------|")
        
        for name, data in sorted(layouts.items()):
            s = data["stats"]
            summary_lines.append(f"| {name} | {s['iscii_mapped']} | {s['passthrough']} | {s['unmapped']} |")
        
        print(f"  {len(layouts)} layouts extracted")
    
    summary_lines.insert(1, f"\n**Total layouts extracted: {total_layouts}**\n")
    
    # Write summary
    summary_path = os.path.join(OUTPUT_DIR, "all_languages_summary.md")
    with open(summary_path, 'w') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"\nDone! {total_layouts} total layouts extracted.")
    print(f"Summary: {summary_path}")

if __name__ == "__main__":
    main()
