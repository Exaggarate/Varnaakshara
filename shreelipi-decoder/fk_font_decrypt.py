#!/usr/bin/env python3
"""
Shreelipi FK_ Font Decryptor
=============================
Decrypts FK_ (FKFONTS) bitmap font files from Shreelipi 7.4 DVD.

FK_ Cipher Algorithm:
- 24-bit LFSR state initialized from seed via PRNG warmup
- PRNG warmup uses constant 0x668b7 (differs from SL_ which uses 0x40e6d)
- 5 bitmask positions: bits 1, 4, 6, 30, (overflow=0)
- Keystream: 8 rounds per byte of parity-feedback LFSR
- CBC-like XOR feedback: plain = ks ^ prev_cipher ^ cipher ^ prev_plain
- Seed = font_number (extracted from filename FK_NNNN)

Reverse-engineered from SL7_32.EXE (Shreelipi 7.4 main application):
- FUN_00452d30: FK init (mode=8, constant 0x668b7)
- FUN_00453020: FK keystream byte generator (8-round LFSR)
- FUN_00452fb4: Bitmask popcount helper
- FUN_0046e4a8: FK file decryption loop

Author: Clawd-X (RE from SL7_32.EXE via Ghidra headless decompilation)
Date: 2026-07-09
"""

import os
import sys
import argparse
from pathlib import Path


def signed_byte_extract(x):
    """Delphi signed byte extraction: x & 0x800000FF with sign correction"""
    x = x & 0xFFFFFFFF
    r = x & 0x800000FF
    if r & 0x80000000:
        r = ((r - 1) | 0xFFFFFF00) + 1
        r &= 0xFFFFFFFF
    if r >= 0x80000000:
        r -= 0x100000000
    return r


def make_mask(val):
    """FUN_00452d1c: Create bitmask (1 << val if val < 32, else 0)"""
    val = val & 0xFF
    if val < 32:
        return 1 << val
    return 0


class FKDecryptor:
    """FK_ font file decryptor"""
    
    # Bitmask parameters for mode 8 (standard FK_)
    MASK_PARAMS = [1, 4, 6, 0x1E, 0xFF]
    
    def __init__(self, seed):
        self.masks = [make_mask(p) for p in self.MASK_PARAMS]
        self.state = self._init_state(seed)
        self.prev_cipher = 0xFF
        self.prev_plain = 0xFF
    
    def _init_state(self, seed):
        """FUN_00452d30: Initialize 24-bit LFSR state"""
        # signed_byte then (short) cast
        s0 = signed_byte_extract(seed)
        s0 = s0 & 0xFFFF
        if s0 >= 0x8000:
            s0 = (s0 - 0x10000) & 0xFFFFFFFF
        
        s1 = (s0 + 0x15) & 0xFFFFFFFF
        s2 = (s0 - 0x15) & 0xFFFFFFFF
        
        # Warmup loop (11 iterations) with FK-specific constant 0x668b7
        for i in range(11):
            prev_s1 = s1
            prev_s0 = s0
            val = (s0 * 0x483 + s1 * 0x651 + s2 * 0x55f + 0x668b7) & 0xFFFFFFFF
            val = signed_byte_extract(val)
            s2 = s1
            s1 = s0
            s0 = val
        
        # State = [s1_prev, s0_prev, s0] packed into 24-bit value
        state = ((prev_s1 & 0xFF) * 0x100 + (prev_s0 & 0xFF)) * 0x100 + (s0 & 0xFF)
        return state & 0xFFFFFFFF
    
    def keystream_byte(self):
        """FUN_00453020: Generate one keystream byte via 8-round LFSR"""
        output = 0
        for _ in range(8):
            output = (output << 1) & 0xFF
            # Popcount: count masks that overlap with state
            pc = sum(1 for mask in self.masks if mask and (self.state & mask))
            # Shift state left
            self.state = (self.state << 1) & 0xFFFFFFFF
            # If parity is odd, feed back
            if pc & 1:
                output |= 1
                self.state |= 1
        return output
    
    def decrypt_byte(self, cipher_byte):
        """Decrypt one byte with CBC-like feedback"""
        ks = self.keystream_byte()
        feedback = self.prev_cipher ^ cipher_byte ^ self.prev_plain
        plain = ks ^ feedback
        self.prev_plain = plain
        self.prev_cipher = cipher_byte
        return plain
    
    def decrypt(self, data):
        """Decrypt entire data buffer"""
        return bytearray(self.decrypt_byte(b) for b in data)


def extract_font_number(filename):
    """Extract font number from FK_NNNN filename"""
    base = os.path.basename(filename)
    parts = base.split('_')
    if len(parts) >= 2:
        try:
            return int(parts[1].split('.')[0])
        except ValueError:
            pass
    return None


def decrypt_file(inpath, outpath, seed=None):
    """Decrypt a single FK_ file"""
    if seed is None:
        seed = extract_font_number(inpath)
        if seed is None:
            raise ValueError(f"Cannot determine seed from filename: {inpath}")
    
    data = open(inpath, 'rb').read()
    dec = FKDecryptor(seed)
    result = dec.decrypt(data)
    
    os.makedirs(os.path.dirname(outpath) or '.', exist_ok=True)
    open(outpath, 'wb').write(result)
    return len(result)


def main():
    parser = argparse.ArgumentParser(description='Shreelipi FK_ Font Decryptor')
    parser.add_argument('input', help='Input FK_ file or directory')
    parser.add_argument('output', help='Output file or directory')
    parser.add_argument('--seed', type=int, help='Override seed (default: extract from filename)')
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        # Batch mode
        total = 0
        for root, dirs, files in os.walk(args.input):
            for fn in sorted(files):
                if fn.startswith('FK_') and not fn.endswith('.MAP'):
                    inpath = os.path.join(root, fn)
                    relpath = os.path.relpath(inpath, args.input)
                    outpath = os.path.join(args.output, relpath)
                    try:
                        n = decrypt_file(inpath, outpath, args.seed)
                        total += 1
                    except Exception as e:
                        print(f"FAIL: {fn}: {e}", file=sys.stderr)
        print(f"Decrypted {total} files")
    else:
        n = decrypt_file(args.input, args.output, args.seed)
        print(f"Decrypted {n} bytes → {args.output}")


if __name__ == '__main__':
    main()
