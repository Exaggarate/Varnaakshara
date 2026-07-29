#!/usr/bin/env python3
"""
Build complete Shree-Lipi font glyph → Unicode mapping from visual inspection
of rendered WDEV001.TTF and WDEV002.TTF contact sheets.

WDEV001 = Base consonants, vowels, matras, digits
WDEV002 = Conjuncts, half-forms, special ligatures
"""

# Shree-Lipi WDEV001 (Shree-Dev-001) font glyph mapping
# Visually identified from rendered contact sheet
WDEV001_MAP = {
    # Row 0x20-0x2F
    0x20: " ",          # space
    0x21: "!",          # exclamation (shown as Devanagari danda? looks like !)
    0x22: "\u093D",     # avagraha ऽ (looks like a quote mark shape)
    0x23: "\u0910",     # ai ऐ
    # 0x24: empty/space
    # 0x25: empty/% sign
    0x25: "\u0966",     # ० (shown as %, but actually Devanagari zero? No, looks like %)
    0x26: "\u0964",     # danda ।
    0x27: "\u0902",     # anusvara anusvara ं (shown as apostrophe-like dot)
    0x28: "(",          # parenleft
    0x29: ")",          # parenright
    0x2A: "\u0CD5",     # asterisk / special — looks like a flower ✻ ornament
    0x2B: "+",          # plus
    0x2C: ",",          # comma  
    0x2D: "-",          # hyphen
    0x2E: ".",          # period
    0x2F: "/",          # slash
    
    # Row 0x30-0x3F — Devanagari digits
    0x30: "\u0966",     # ० zero
    0x31: "\u0967",     # १ one
    0x32: "\u0968",     # २ two
    0x33: "\u0969",     # ३ three
    0x34: "\u096A",     # ४ four
    0x35: "\u096B",     # ५ five
    0x36: "\u096C",     # ६ six
    0x37: "\u096D",     # ७ seven
    0x38: "\u096E",     # ८ eight
    0x39: "\u096F",     # ९ nine
    0x3A: ":",          # colon (Devanagari visarga-like)
    0x3B: ";",          # semicolon
    0x3C: "\u0921",     # ड (shown as box shape — actually ड ḍa)
    # 0x3D: = sign
    0x3E: "?",          # question mark shape
    0x3F: "?",          # same
    
    # Row 0x40-0x4F — Devanagari consonants + vowels
    0x40: "\u0938",     # स sa (the S-like shape)
    0x41: "\u0905",     # अ a
    0x42: "\u0907",     # इ i (short i, shown as इ)
    0x43: "\u0909",     # उ u
    0x44: "\u090A",     # ऊ uu
    0x45: "\u090F",     # ए e
    0x46: "\u0910",     # ऐ ai — wait, 0x23 was also ai. Let me re-check
    # Actually looking more carefully at the image:
    # 0x45 = ऋ (vocalic r)  — the shape has the ri hook
    0x45: "\u090B",     # ऋ vocalic_r
    0x46: "\u090F",     # ए e
    0x47: "\u0910",     # ऐ ai  — no, the font image shows ऐ at 0x46
    # Let me re-read the image more carefully:
    # Row 0x40: स अ इ उ ऊ ए ऋ ऐ क ख ग घ ड च छ ज
    0x40: "\u0938",     # स sa
    0x41: "\u0905",     # अ a
    0x42: "\u0907",     # इ i
    0x43: "\u0909",     # उ u
    0x44: "\u090A",     # ऊ uu
    0x45: "\u090F",     # ए e
    0x46: "\u090B",     # ऋ vocalic_r
    0x47: "\u0910",     # ऐ ai
    0x48: "\u0915",     # क ka
    0x49: "\u0916",     # ख kha
    0x4A: "\u0917",     # ग ga
    0x4B: "\u0918",     # घ gha
    0x4C: "\u0919",     # ड wait — looking at image: ड = dda
    0x4C: "\u0921",     # ड dda — no wait, the chart shows ङ at 4C
    # Let me be very precise from the image grid:
    # 40=स 41=अ 42=इ 43=उ 44=ऊ 45=ए 46=ऋ 47=ऐ 48=क 49=ख 4A=ग 4B=घ 4C=ड 4D=च 4E=छ 4F=ज
    0x4C: "\u0921",     # ड dda  
    0x4D: "\u091A",     # च cha
    0x4E: "\u091B",     # छ chha
    0x4F: "\u091C",     # ज ja
    
    # Row 0x50-0x5F
    # 50=झ 51=ट 52=ठ 53=ड 54=ढ 55=ण 56=त 57=थ 58=द 59=ध 5A=न 5B=प(?) 5C=फ 5D=? 5E=भ 5F=म
    0x50: "\u091D",     # झ jha
    0x51: "\u091F",     # ट tta
    0x52: "\u0920",     # ठ ttha
    0x53: "\u0921",     # ड dda — duplicate? Let me re-check. Image shows ड at 53
    0x53: "\u0922",     # ढ ddha — actually it could be ढ
    0x54: "\u0922",     # ढ ddha  
    0x55: "\u0923",     # ण nna
    0x56: "\u0924",     # त ta
    0x57: "\u0925",     # थ tha
    0x58: "\u0926",     # द da
    0x59: "\u0927",     # ध dha
    0x5A: "\u0928",     # न na
    0x5B: "\u092A",     # प pa — actually looks like प with a curve = ि ?
    # From image: 5B shows "fi" shape which is प pa
    0x5B: "\u092A",     # प pa
    0x5C: "\u092B",     # फ pha
    0x5D: "\u093C",     # nukta ़ (dot below) — shown as a dot
    0x5E: "\u092D",     # भ bha
    0x5F: "\u092E",     # म ma
    
    # Row 0x60-0x6F
    # 60=य 61=र 62=ल 63=ल(lla?) 64=व 65=श 66=ष 67=स 68=ह 69=ळ 6A=क्ष 6B=ज्ञ 6C=श्र 6D=ऽ(danda?) 6E=प(?) 6F=^(chandrabindu?)
    0x60: "\u092F",     # य ya
    0x61: "\u0930",     # र ra
    0x62: "\u0932",     # ल la
    0x63: "\u0933",     # ळ lla
    0x64: "\u0935",     # व va
    0x65: "\u0936",     # श sha
    0x66: "\u0937",     # ष ssa
    0x67: "\u0938",     # स sa — wait, 0x40 was also स. Let me check.
    # Actually the image at 0x40 shows a different shape. Looking again:
    # 0x40 appears to be ऽ (avagraha) and 0x67 is स (sa)
    0x67: "\u0938",     # स sa
    0x68: "\u0939",     # ह ha
    0x69: "\u0933",     # ळ lla (again? or different variant)
    # Image shows: 69=ळ̣ (with dot?), 6A=क्ष, 6B=ज्ञ, 6C=श्र
    0x69: "\u0934",     # ळ (with nukta = ऴ)  
    0x6A: "\u0915\u094D\u0937",  # क्ष ksha (conjunct)
    0x6B: "\u091C\u094D\u091E",  # ज्ञ jnya (conjunct)
    0x6C: "\u0936\u094D\u0930",  # श्र shra (conjunct)
    0x6D: "\u0964",     # । danda (vertical bar)
    0x6E: "\u092A",     # प pa (alternate form?)
    0x6F: "\u0901",     # ँ chandrabindu (^-like shape)
    
    # Row 0x70-0x7F — Matras (vowel signs)
    # 70=ि 71=ी 72=ी(?) 73=ु 74=ू 75=ू(?) 76=ू(?) 77=? 78=ो 79=ौ 7A=? 7B=ि(?) 7C=? 7D=? 7E=ब 7F=□
    0x70: "\u093F",     # ि i_matra
    0x71: "\u0940",     # ी ii_matra
    0x72: "\u0940",     # ी ii_matra (variant)
    0x73: "\u0941",     # ु u_matra
    0x74: "\u0942",     # ू uu_matra
    0x75: "\u0942",     # ू uu_matra (variant)
    0x76: "\u0942",     # ू uu_matra (variant)
    # 77 appears blank
    0x78: "\u094B",     # ो o_matra (shown as two curves)
    0x79: "\u094C",     # ौ au_matra
    # 7A-7B look like matra variants
    0x7B: "\u093F",     # ि i_matra (post-form)
    0x7C: "\u0943",     # ृ vocalic_r_matra
    0x7D: "\u0930\u094D",  # र् (ra-halant, for reph)
    0x7E: "\u092C",     # ब ba
    # 0x7F = empty box
}

# Actually let me be more systematic. I'll use the cross-reference data we already built
# and fill in the gaps from the font image
import json

with open('/root/.openclaw/workspace/varnaakshara-ime/shreelipi_extracted/font_glyph_crossref.json') as f:
    xref = json.load(f)

print("Existing cross-reference for Devanagari:")
dev_xref = xref.get('devanagari', {})
for glyph_hex, info in sorted(dev_xref.items()):
    print(f"  Glyph {glyph_hex} ({info['glyph_char']}) → {info['iscii_name']} = {info['unicode']} ({info['unicode_hex']})")

print(f"\nTotal existing entries: {len(dev_xref)}")

# These are the unresolved ones from Inscript:
# 0x41 (A), 0x45 (E), 0x47 (G), 0x67 (g), 0x62 (b), 0x26 (&), 0x68 (h), 0x6E (n)
# From the font image:
# 0x41 = अ (a vowel)
# 0x45 = ए or ऋ  
# 0x47 = ऐ
# 0x67 = स (sa) — but we have 0x73 → ka already... wait
# Let me check what 0x67 renders as

print("\nUnresolved glyph codes to map from font image:")
unresolved = [0x26, 0x41, 0x45, 0x47, 0x62, 0x67, 0x68, 0x6E]
for code in unresolved:
    hex_key = f"0x{code:02X}"
    if hex_key in dev_xref:
        print(f"  0x{code:02X} ({chr(code)}) — ALREADY RESOLVED: {dev_xref[hex_key]['iscii_name']}")
    else:
        print(f"  0x{code:02X} ({chr(code)}) — NEEDS MAPPING")
