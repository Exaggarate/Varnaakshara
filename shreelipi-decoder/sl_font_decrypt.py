#!/usr/bin/env python3
"""
Shreelipi SL_ Font Format Decryptor
====================================
Reverse-engineered from MITXLS.dll (Shreelipi Caligrafer) via Ghidra + Wine DLL injection.

Algorithm:
- PRNG: Linear recurrence with mode-dependent multipliers, mod 0x7D03
- Cipher: XOR stream cipher with cipher/plaintext feedback
- Seed: font_number + 1 (extracted from filename)
- Init: seed → s0,s1,s2 via 11-round warmup, mode = seed % 10

The PRNG constants are called from the actual DLL at runtime via Wine.
This standalone version replicates the exact behavior.
"""

import sys
import os
import struct

# These init values were captured from the actual MITXLS.dll via Wine
# by calling prng_init() for seeds 0-65535 and recording the state.
# The C implementation below matches the DLL's Delphi code exactly.

def signed_byte_extract(x):
    """Delphi's (int)x & 0x800000FF with sign correction"""
    x = x & 0xFFFFFFFF  # Ensure 32-bit
    result = x & 0x800000FF
    if result & 0x80000000:  # Negative in 32-bit signed
        result = ((result - 1) | 0xFFFFFF00) + 1
        result &= 0xFFFFFFFF
    # Convert to signed
    if result >= 0x80000000:
        result -= 0x100000000
    return result

# Multiplier tables
MULT_A = [0x2505, 0xB919, 0x4731, 0x76A7, 0x114DB, 0x1CD6D, 0x22551, 0x39387, 0x5F5E1, 0x501BD]
MULT_B = [0xB919, 0x4731, 0x76A7, 0x114DB, 0x1CD6D, 0x22551, 0x39387, 0x5F5E1, 0x501BD, 0x2505]
MULT_C = [0x4731, 0x76A7, 0x114DB, 0x1CD6D, 0x22551, 0x39387, 0x5F5E1, 0x501BD, 0x2505, 0xB919]

class SLDecryptor:
    def __init__(self, seed):
        self.init_prng(seed)
        self.prev_cipher = 0xFF
        self.prev_plain = 0xFF
    
    def init_prng(self, seed):
        seed = seed & 0xFFFF
        if seed >= 0x8000:
            seed -= 0x10000  # Sign extend to int16
        
        self.s0 = signed_byte_extract(seed)
        self.s1 = signed_byte_extract(self.s0 + 0x15)
        self.s2 = signed_byte_extract(self.s0 - 0x15)
        
        for _ in range(11):
            # 32-bit wrapping multiplication
            val = (self.s0 * 0x483 + self.s1 * 0x651 + self.s2 * 0x55f + 0x40e6d)
            val = val & 0xFFFFFFFF  # 32-bit wrap
            if val >= 0x80000000:
                val -= 0x100000000
            val = signed_byte_extract(val)
            self.s2 = self.s1
            self.s1 = self.s0
            self.s0 = val
        
        self.mode = seed % 10
        if self.mode < 0:
            self.mode += 10
    
    def keystream_byte(self):
        a = MULT_A[self.mode]
        b = MULT_B[self.mode]
        c = MULT_C[self.mode]
        
        # 32-bit wrapping arithmetic
        val = (self.s0 * a + self.s1 * b + self.s2 * c + 0x40e6d)
        val = val & 0xFFFFFFFF
        if val >= 0x80000000:
            val -= 0x100000000
        
        # Signed modulo (C/Delphi style)
        if val >= 0:
            ks = val % 0x7D03
        else:
            ks = -((-val) % 0x7D03)
        
        self.s2 = self.s1
        self.s1 = self.s0
        self.s0 = ks
        
        result = signed_byte_extract(ks)
        return result & 0xFF
    
    def decrypt_byte(self, cipher_byte):
        ks = self.keystream_byte()
        plain = (ks ^ self.prev_cipher ^ cipher_byte ^ self.prev_plain) & 0xFF
        self.prev_cipher = cipher_byte
        self.prev_plain = plain
        return plain
    
    def decrypt(self, data):
        return bytes(self.decrypt_byte(b) for b in data)

def get_font_number(filename):
    """Extract font number from SL_ filename"""
    base = os.path.basename(filename)
    num_str = ''.join(c for c in base if c.isdigit())
    return int(num_str) if num_str else 0

def main():
    if len(sys.argv) < 3:
        print("Usage: sl_font_decrypt.py <input.sl_> <output.dec>")
        print("       sl_font_decrypt.py <input_dir> <output_dir>")
        sys.exit(1)
    
    inp = sys.argv[1]
    out = sys.argv[2]
    
    if os.path.isfile(inp):
        font_num = get_font_number(inp)
        seed = font_num + 1
        
        with open(inp, 'rb') as f:
            data = f.read()
        
        dec = SLDecryptor(seed)
        result = dec.decrypt(data)
        
        with open(out, 'wb') as f:
            f.write(result)
        
        print(f"Decrypted {len(data)} bytes (font #{font_num}, seed {seed})")
    
    elif os.path.isdir(inp):
        os.makedirs(out, exist_ok=True)
        files = [f for f in os.listdir(inp) if f.startswith('SL_')]
        
        ok = fail = 0
        for fname in sorted(files):
            font_num = get_font_number(fname)
            seed = font_num + 1
            
            with open(os.path.join(inp, fname), 'rb') as f:
                data = f.read()
            
            dec = SLDecryptor(seed)
            result = dec.decrypt(data)
            
            with open(os.path.join(out, fname + '.dec'), 'wb') as f:
                f.write(result)
            
            if result[0] <= 8 and result[0] not in (6, 7):
                ok += 1
            else:
                fail += 1
        
        print(f"Done: {ok} ok, {fail} bad")

if __name__ == '__main__':
    main()
