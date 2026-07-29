#!/usr/bin/env python3
"""
Shreelipi 7.4 License/Protection Removal Tool
Patches all protection mechanisms from Shreelipi executables.
Cracked by Clawd-X 🦞

Usage: python3 shreelipi_crack.py <input_binary> <output_binary>
   or: python3 shreelipi_crack.py --batch <directory>
"""

import struct
import sys
import os
import shutil

def patch_binary(data):
    """Apply all protection removal patches to a Shreelipi binary."""
    data = bytearray(data)
    patches = []
    
    # ============================================
    # PATCH 1: CRC/USIGN integrity check
    # Signature: 55 8B EC 81 C4 F4 FE FF FF (53 56 57)
    # Action: Return TRUE immediately (mov al,1; ret N)
    # ============================================
    crc_sig = bytes([0x55, 0x8B, 0xEC, 0x81, 0xC4, 0xF4, 0xFE, 0xFF, 0xFF])
    pos = data.find(crc_sig)
    if pos >= 0:
        # Find ret N to determine stack cleanup:
        for j in range(pos+10, min(pos+0x400, len(data))):
            if data[j] == 0xC2 and j+2 < len(data) and data[j+2] == 0x00 and data[j+1] <= 0x20:
                ret_n = data[j+1]
                data[pos:pos+5] = bytes([0xB0, 0x01, 0xC2, ret_n, 0x00])
                patches.append(f"CRC check -> return true (ret 0x{ret_n:X})")
                break
    
    # ============================================
    # PATCH 2: Virus/tamper dialog function
    # Signature: 55 8B EC 81 C4 2C FF FF FF near "infected"
    # Action: Return immediately (ret)
    # ============================================
    virus_sig = bytes([0x55, 0x8B, 0xEC, 0x81, 0xC4, 0x2C, 0xFF, 0xFF, 0xFF])
    pos = 0
    while True:
        pos = data.find(virus_sig, pos)
        if pos < 0: break
        if b'infected' in data[pos:pos+300]:
            data[pos] = 0xC3
            patches.append("Virus dialog -> ret")
        pos += 9
    
    # ============================================
    # PATCH 3: Demo flag writes (C6 05 XX XX XX XX 01)
    # Find common demo flag addresses and change 01 -> 00
    # ============================================
    # Known demo flag addresses:
    demo_addrs = set()
    for i in range(len(data) - 7):
        if data[i] == 0xC6 and data[i+1] == 0x05 and data[i+6] == 0x01:
            addr = struct.unpack('<I', data[i+2:i+6])[0]
            if 0x4C0000 <= addr <= 0x500000:
                # Check if this address is referenced as a demo flag:
                # Look for cmp byte [addr], 0/1 nearby
                addr_bytes = data[i+2:i+6]
                cmp_pat = b'\x80\x3D' + addr_bytes
                if cmp_pat in data:
                    demo_addrs.add(addr)
    
    for addr in demo_addrs:
        addr_bytes = struct.pack('<I', addr)
        set_pat = b'\xC6\x05' + addr_bytes + b'\x01'
        pos = 0
        while True:
            pos = data.find(set_pat, pos)
            if pos < 0: break
            data[pos+6] = 0x00
            patches.append(f"Demo flag [0x{addr:X}] = 1 -> 0")
            pos += 7
        
        # Also patch conditional jumps:
        cmp_pat = b'\x80\x3D' + addr_bytes
        pos = 0
        while True:
            pos = data.find(cmp_pat, pos)
            if pos < 0: break
            if pos + 8 < len(data):
                if data[pos+7] == 0x74:  # je -> jmp
                    data[pos+7] = 0xEB
                    patches.append(f"Demo check je -> jmp")
                elif data[pos+7] == 0x75:  # jne -> nop
                    data[pos+7] = 0x90
                    data[pos+8] = 0x90
                    patches.append(f"Demo check jne -> nop")
            pos += 7
    
    # ============================================
    # PATCH 4: SetTimer (5 min = 300000ms)
    # push 300000 = 68 E0 93 04 00
    # Action: NOP out the push
    # ============================================
    timer_pat = bytes([0x68, 0xE0, 0x93, 0x04, 0x00])
    pos = 0
    while True:
        pos = data.find(timer_pat, pos)
        if pos < 0: break
        data[pos:pos+5] = b'\x90' * 5
        patches.append("SetTimer 300000ms -> NOP")
        pos += 5
    
    # ============================================
    # PATCH 5: USIGN verification function
    # Near "USIGN:" strings
    # ============================================
    usign_pos = data.find(b'USIGN:')
    if usign_pos >= 0:
        for i in range(usign_pos, max(0, usign_pos-1500), -1):
            if data[i:i+3] == b'\x55\x8B\xEC' and data[i+3:i+5] == b'\x33\xC0':
                if b'USIGN' in data[i:i+1500]:
                    data[i] = 0xC3
                    patches.append("USIGN verification -> ret")
                    break
    
    # ============================================
    # PATCH 6: Hardware lock check 
    # Function that checks MLUtil6.DLL/USB dongle
    # ============================================
    mlutil_err = data.find(b'Error in MLUtil6.DLL')
    if mlutil_err >= 0:
        for i in range(mlutil_err, max(0, mlutil_err-500), -1):
            if data[i:i+3] == b'\x55\x8B\xEC':
                # Make it: mov byte [eax], 1; ret
                data[i:i+4] = b'\xC6\x00\x01\xC3'
                patches.append("Hardware lock check -> pass")
                break
    
    return bytes(data), patches

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    data = open(input_path, 'rb').read()
    patched, patches = patch_binary(data)
    
    print(f"Patches applied to {os.path.basename(input_path)}:")
    for p in patches:
        print(f"  ✅ {p}")
    print(f"\nTotal: {len(patches)} patches")
    
    open(output_path, 'wb').write(patched)
    print(f"Saved: {output_path} ({len(patched)} bytes)")
