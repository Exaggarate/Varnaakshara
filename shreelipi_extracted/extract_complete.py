#!/usr/bin/env python3
"""
Shree-Lipi 7.4 Complete Keyboard Layout Extractor v2
Uses IDV files as primary ISCII source + cross-references DEV glyph codes.
"""
import os, json, struct

# ── ISCII → Unicode offset table (IS 13194:1991) ──
ISCII_TO_UNICODE_OFFSET = {
    0xA1: 0x01, 0xA2: 0x02, 0xA3: 0x03,
    0xA4: 0x05, 0xA5: 0x06, 0xA6: 0x07, 0xA7: 0x08,
    0xA8: 0x09, 0xA9: 0x0A, 0xAA: 0x0B,
    0xAB: 0x0E, 0xAC: 0x0F, 0xAD: 0x10,
    0xAE: 0x0D, 0xAF: 0x12, 0xB0: 0x13, 0xB1: 0x14,
    0xB2: 0x11,
    0xB3: 0x15, 0xB4: 0x16, 0xB5: 0x17, 0xB6: 0x18, 0xB7: 0x19,
    0xB8: 0x1A, 0xB9: 0x1B, 0xBA: 0x1C, 0xBB: 0x1D, 0xBC: 0x1E,
    0xBD: 0x1F, 0xBE: 0x20, 0xBF: 0x21, 0xC0: 0x22, 0xC1: 0x23,
    0xC2: 0x24, 0xC3: 0x25, 0xC4: 0x26, 0xC5: 0x27, 0xC6: 0x28,
    0xC7: 0x29, 0xC8: 0x2A, 0xC9: 0x2B, 0xCA: 0x2C, 0xCB: 0x2D,
    0xCC: 0x2E, 0xCD: 0x2F, 0xCE: 0x30, 0xCF: 0x32, 0xD0: 0x33,
    0xD1: 0x34, 0xD2: 0x35, 0xD3: 0x36, 0xD4: 0x37, 0xD5: 0x38,
    0xD6: 0x39,
    0xD8: 0x4D, 0xD9: 0x3C, 0xDA: 0x3D,
    0xE0: 0x3E, 0xE1: 0x3F, 0xE2: 0x40, 0xE3: 0x41, 0xE4: 0x42,
    0xE5: 0x43, 0xE6: 0x46, 0xE7: 0x47, 0xE8: 0x48, 0xE9: 0x45,
    0xEA: 0x4A, 0xEB: 0x4B, 0xEC: 0x4C, 0xED: 0x49,
    0xF0: 0x66, 0xF1: 0x67, 0xF2: 0x68, 0xF3: 0x69, 0xF4: 0x6A,
    0xF5: 0x6B, 0xF6: 0x6C, 0xF7: 0x6D, 0xF8: 0x6E, 0xF9: 0x6F,
}

ISCII_NAMES = {
    0xA1: "chandrabindu", 0xA2: "anusvara", 0xA3: "visarga",
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
    0xD7: "reserved", 0xD8: "halant", 0xD9: "nukta", 0xDA: "avagraha",
    0xDB: "ext", 0xDC: "DC", 0xDD: "DD", 0xDE: "DE", 0xDF: "DF",
    0xE0: "aa_matra", 0xE1: "i_matra", 0xE2: "ii_matra",
    0xE3: "u_matra", 0xE4: "uu_matra", 0xE5: "vocalic_r_matra",
    0xE6: "short_e_matra", 0xE7: "e_matra", 0xE8: "ai_matra",
    0xE9: "candra_e_matra", 0xEA: "short_o_matra",
    0xEB: "o_matra", 0xEC: "au_matra", 0xED: "candra_o_matra",
    0xF0: "digit_0", 0xF1: "digit_1", 0xF2: "digit_2",
    0xF3: "digit_3", 0xF4: "digit_4", 0xF5: "digit_5",
    0xF6: "digit_6", 0xF7: "digit_7", 0xF8: "digit_8", 0xF9: "digit_9",
}

LANGUAGES = {
    "devanagari": {"dir": "DEV", "compose_ext": ".DEV", "idv_exts": [".IDV"], "base": 0x0900, "name": "Devanagari"},
    "bengali":    {"dir": "BAN", "compose_ext": ".BAN", "idv_exts": [".IBA"], "base": 0x0980, "name": "Bengali"},
    "assamese":   {"dir": "ASS", "compose_ext": ".ASS", "idv_exts": [".IAS"], "base": 0x0980, "name": "Assamese"},
    "gujarati":   {"dir": "GUJ", "compose_ext": ".GUJ", "idv_exts": [".IGU", ".iGU"], "base": 0x0A80, "name": "Gujarati"},
    "gurmukhi":   {"dir": "PUN", "compose_ext": ".PUN", "idv_exts": [".IPU", ".iPU"], "base": 0x0A00, "name": "Gurmukhi"},
    "kannada":    {"dir": "KAN", "compose_ext": ".KAN", "idv_exts": [".IKA", ".iKA"], "base": 0x0C80, "name": "Kannada"},
    "malayalam":  {"dir": "MAL", "compose_ext": ".MAL", "idv_exts": [".IMA", ".iMA"], "base": 0x0D00, "name": "Malayalam"},
    "oriya":      {"dir": "ORI", "compose_ext": ".ORI", "idv_exts": [".IOR", ".iOR"], "base": 0x0B00, "name": "Oriya"},
    "tamil":      {"dir": "TAM", "compose_ext": ".TAM", "idv_exts": [".ITA", ".iTA"], "base": 0x0B80, "name": "Tamil"},
    "telugu":     {"dir": "TEL", "compose_ext": ".TEL", "idv_exts": [".ITE", ".iTE"], "base": 0x0C00, "name": "Telugu"},
}

COMPOSE_BASE = "/tmp/SL74DVD/COMMON/COMPOSE"
OUTPUT_DIR = "/root/.openclaw/workspace/varnaakshara-ime/shreelipi_extracted"

def iscii_to_unicode(iscii_byte, script_base):
    if iscii_byte in ISCII_TO_UNICODE_OFFSET:
        return chr(script_base + ISCII_TO_UNICODE_OFFSET[iscii_byte])
    return None

def find_idv_file(compose_dir, layout_name, idv_exts):
    """Find IDV file matching a compose file, case-insensitively."""
    for idv_ext in idv_exts:
        # Try various case combinations
        candidates = [
            layout_name + idv_ext,
            layout_name + idv_ext.upper(),
            layout_name + idv_ext.lower(),
            layout_name.upper() + idv_ext,
            layout_name.upper() + idv_ext.upper(),
            layout_name.upper() + idv_ext.lower(),
            layout_name.lower() + idv_ext,
            layout_name.lower() + idv_ext.upper(),
            layout_name.lower() + idv_ext.lower(),
        ]
        for candidate in candidates:
            path = os.path.join(compose_dir, candidate)
            if os.path.exists(path):
                return path
    
    # Fallback: case-insensitive directory scan
    name_upper = layout_name.upper()
    for f in os.listdir(compose_dir):
        f_name = os.path.splitext(f)[0].upper()
        f_ext = os.path.splitext(f)[1].upper()
        if f_name == name_upper and any(f_ext == ext.upper() for ext in idv_exts):
            return os.path.join(compose_dir, f)
    
    return None

def parse_layer(data, script_base, start=0x20, end=0x80):
    """Parse one layer of key mappings from binary data."""
    mappings = {}
    stats = {"iscii": 0, "glyph": 0, "passthrough": 0, "unmapped": 0, "special": 0}
    
    for pos in range(start, end):
        if pos >= len(data):
            break
        byte_val = data[pos]
        key = chr(pos) if pos < 0x7F else "DEL"
        
        if byte_val == 0xFF:
            stats["unmapped"] += 1
            continue
        
        if byte_val == pos:
            stats["passthrough"] += 1
            continue
        
        if byte_val in ISCII_TO_UNICODE_OFFSET:
            unicode_char = iscii_to_unicode(byte_val, script_base)
            if unicode_char:
                stats["iscii"] += 1
                mappings[key] = {
                    "iscii": f"0x{byte_val:02X}",
                    "iscii_name": ISCII_NAMES.get(byte_val, f"iscii_{byte_val:02X}"),
                    "unicode": unicode_char,
                    "unicode_hex": f"U+{ord(unicode_char):04X}",
                }
            else:
                stats["special"] += 1
                mappings[key] = {
                    "iscii": f"0x{byte_val:02X}",
                    "iscii_name": ISCII_NAMES.get(byte_val, f"unknown"),
                    "type": "unmappable_iscii"
                }
        elif 0x80 <= byte_val <= 0x9F:
            stats["special"] += 1
            mappings[key] = {
                "iscii": f"0x{byte_val:02X}",
                "type": "special_code"
            }
        elif 0x20 <= byte_val < 0x80:
            stats["glyph"] += 1
            mappings[key] = {
                "font_glyph": f"0x{byte_val:02X}",
                "font_glyph_char": chr(byte_val),
                "type": "font_glyph"
            }
        else:
            # Other ISCII range not in our table
            stats["special"] += 1
            name = ISCII_NAMES.get(byte_val, f"iscii_{byte_val:02X}")
            mappings[key] = {
                "iscii": f"0x{byte_val:02X}",
                "iscii_name": name,
                "type": "extended_iscii"
            }
    
    return mappings, stats

def parse_compose_sequences(idv_data, script_base):
    """Parse compose/dead-key sequences from IDV data (bytes 0xD8+)."""
    sequences = []
    i = 0xD8
    while i < len(idv_data):
        if idv_data[i] == 0x04:
            seq = []
            i += 1
            while i < len(idv_data) and idv_data[i] != 0xFF and idv_data[i] != 0x04:
                seq.append(idv_data[i])
                i += 1
            if seq:
                iscii_names = [ISCII_NAMES.get(b, f"0x{b:02X}") for b in seq]
                unicode_chars = []
                for b in seq:
                    uc = iscii_to_unicode(b, script_base)
                    unicode_chars.append(uc if uc else f"[0x{b:02X}]")
                sequences.append({
                    "iscii_bytes": [f"0x{b:02X}" for b in seq],
                    "iscii_names": iscii_names,
                    "unicode": "".join(unicode_chars),
                })
        else:
            i += 1
    return sequences

def build_glyph_crossref(compose_dir, lang_config):
    """Cross-reference DEV and IDV files to build font glyph → ISCII mapping."""
    glyph_map = {}
    compose_ext = lang_config["compose_ext"].upper()
    
    for fname in os.listdir(compose_dir):
        name_part = os.path.splitext(fname)[0]
        file_ext = os.path.splitext(fname)[1].upper()
        fpath = os.path.join(compose_dir, fname)
        
        if file_ext != compose_ext or os.path.getsize(fpath) != 406:
            continue
        
        # Find matching IDV
        idv_path = find_idv_file(compose_dir, name_part, lang_config["idv_exts"])
        if not idv_path or os.path.getsize(idv_path) != 501:
            continue
        
        with open(fpath, 'rb') as f:
            dev_data = f.read()
        with open(idv_path, 'rb') as f:
            idv_data = f.read()
        
        for pos in range(0x20, 0x80):
            dev_byte = dev_data[pos]
            idv_byte = idv_data[pos]
            
            if (0x20 <= dev_byte < 0x80 and dev_byte != pos and 
                idv_byte in ISCII_TO_UNICODE_OFFSET):
                if dev_byte not in glyph_map:
                    glyph_map[dev_byte] = idv_byte
                # Don't override existing - first match wins
    
    return glyph_map

def extract_language(lang_key, lang_config):
    """Extract all keyboard layouts for a language using IDV as primary source."""
    compose_dir = os.path.join(COMPOSE_BASE, lang_config["dir"])
    if not os.path.isdir(compose_dir):
        return None, {}
    
    compose_ext = lang_config["compose_ext"].upper()
    script_base = lang_config["base"]
    
    # First, build the glyph cross-reference for this language
    glyph_map = build_glyph_crossref(compose_dir, lang_config)
    
    layouts = {}
    
    for fname in sorted(os.listdir(compose_dir)):
        name_part = os.path.splitext(fname)[0]
        file_ext = os.path.splitext(fname)[1].upper()
        fpath = os.path.join(compose_dir, fname)
        
        if file_ext != compose_ext or os.path.getsize(fpath) != 406:
            continue
        
        with open(fpath, 'rb') as f:
            dev_data = f.read()
        
        # Find matching IDV file
        idv_path = find_idv_file(compose_dir, name_part, lang_config["idv_exts"])
        idv_data = None
        if idv_path and os.path.getsize(idv_path) == 501:
            with open(idv_path, 'rb') as f:
                idv_data = f.read()
        
        layout = {"file": fname, "normal": {}, "shifted": {}, "compose_sequences": []}
        
        if idv_data:
            # IDV provides clean ISCII mapping for the shifted layer
            shifted_mappings, shifted_stats = parse_layer(idv_data, script_base)
            layout["shifted"] = shifted_mappings
            layout["shifted_stats"] = shifted_stats
            
            # Parse compose sequences
            layout["compose_sequences"] = parse_compose_sequences(idv_data, script_base)
        
        # DEV provides the normal layer - resolve glyph codes using cross-reference
        normal_mappings, normal_stats = parse_layer(dev_data, script_base)
        
        # Now resolve font glyph codes using the cross-reference
        resolved_count = 0
        for key, info in normal_mappings.items():
            if info.get("type") == "font_glyph":
                glyph_code = int(info["font_glyph"], 16)
                if glyph_code in glyph_map:
                    iscii_code = glyph_map[glyph_code]
                    unicode_char = iscii_to_unicode(iscii_code, script_base)
                    if unicode_char:
                        info["resolved_iscii"] = f"0x{iscii_code:02X}"
                        info["resolved_name"] = ISCII_NAMES.get(iscii_code, f"iscii_{iscii_code:02X}")
                        info["unicode"] = unicode_char
                        info["unicode_hex"] = f"U+{ord(unicode_char):04X}"
                        info["type"] = "resolved_glyph"
                        resolved_count += 1
        
        normal_stats["resolved_glyphs"] = resolved_count
        normal_stats["unresolved_glyphs"] = normal_stats["glyph"] - resolved_count
        layout["normal"] = normal_mappings
        layout["normal_stats"] = normal_stats
        layouts[name_part] = layout
    
    return layouts, glyph_map

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    all_glyph_maps = {}
    summary_lines = ["# Shree-Lipi 7.4 Complete Extraction (v2)\n"]
    summary_lines.append("Uses IDV files for ISCII mapping + DEV/IDV cross-reference for glyph code resolution.\n")
    
    total_layouts = 0
    
    for lang_key, lang_config in sorted(LANGUAGES.items()):
        print(f"Extracting {lang_config['name']}...")
        layouts, glyph_map = extract_language(lang_key, lang_config)
        
        if not layouts:
            print(f"  No layouts found")
            continue
        
        all_glyph_maps[lang_key] = {
            f"0x{k:02X}": {
                "glyph_char": chr(k),
                "iscii": f"0x{v:02X}",
                "iscii_name": ISCII_NAMES.get(v, f"iscii_{v:02X}"),
                "unicode": iscii_to_unicode(v, lang_config["base"]),
                "unicode_hex": f"U+{ord(iscii_to_unicode(v, lang_config['base'])):04X}" if iscii_to_unicode(v, lang_config["base"]) else None,
            }
            for k, v in sorted(glyph_map.items())
        }
        
        # Save JSON
        output = {
            "language": lang_config["name"],
            "script_unicode_base": f"U+{lang_config['base']:04X}",
            "total_layouts": len(layouts),
            "glyph_crossref_entries": len(glyph_map),
            "layouts": layouts,
        }
        
        out_path = os.path.join(OUTPUT_DIR, f"layouts_v2_{lang_key}.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        total_layouts += len(layouts)
        
        # Summary stats
        total_iscii = 0
        total_resolved = 0
        total_unresolved = 0
        for name, data in layouts.items():
            ns = data.get("normal_stats", {})
            total_iscii += ns.get("iscii", 0)
            total_resolved += ns.get("resolved_glyphs", 0)
            total_unresolved += ns.get("unresolved_glyphs", 0)
        
        summary_lines.append(f"\n## {lang_config['name']}")
        summary_lines.append(f"- Layouts: **{len(layouts)}**")
        summary_lines.append(f"- Glyph crossref entries: **{len(glyph_map)}**")
        summary_lines.append(f"- Normal layer: {total_iscii} direct ISCII + {total_resolved} resolved glyphs + {total_unresolved} unresolved")
        summary_lines.append(f"- Output: `layouts_v2_{lang_key}.json`\n")
        
        # Layout table
        summary_lines.append(f"| Layout | Normal ISCII | Resolved Glyphs | Unresolved | Shifted ISCII | Compose Seqs |")
        summary_lines.append(f"|--------|-------------|-----------------|------------|--------------|-------------|")
        for name, data in sorted(layouts.items()):
            ns = data.get("normal_stats", {})
            ss = data.get("shifted_stats", {})
            cs = len(data.get("compose_sequences", []))
            summary_lines.append(f"| {name} | {ns.get('iscii',0)} | {ns.get('resolved_glyphs',0)} | {ns.get('unresolved_glyphs',0)} | {ss.get('iscii',0)} | {cs} |")
        
        print(f"  {len(layouts)} layouts, {len(glyph_map)} glyph mappings")
    
    # Save glyph cross-reference
    glyph_path = os.path.join(OUTPUT_DIR, "font_glyph_crossref.json")
    with open(glyph_path, 'w', encoding='utf-8') as f:
        json.dump(all_glyph_maps, f, indent=2, ensure_ascii=False)
    
    summary_lines.insert(1, f"\n**Total: {total_layouts} layouts extracted**\n")
    
    summary_path = os.path.join(OUTPUT_DIR, "extraction_v2_summary.md")
    with open(summary_path, 'w') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"\nDone! {total_layouts} layouts. Glyph crossref: {glyph_path}")

if __name__ == "__main__":
    main()
