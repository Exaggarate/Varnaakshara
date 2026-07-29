#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int32_t s0, s1, s2;
static int mode;

static const int32_t mult_a[] = {0x2505, 0xB919, 0x4731, 0x76A7, 0x114DB,
                                  0x1CD6D, 0x22551, 0x39387, 0x5F5E1, 0x501BD};
static const int32_t mult_b[] = {0xB919, 0x4731, 0x76A7, 0x114DB, 0x1CD6D,
                                  0x22551, 0x39387, 0x5F5E1, 0x501BD, 0x2505};
static const int32_t mult_c[] = {0x4731, 0x76A7, 0x114DB, 0x1CD6D, 0x22551,
                                  0x39387, 0x5F5E1, 0x501BD, 0x2505, 0xB919};

static int32_t signed_byte(int32_t x) {
    // Delphi pattern: x & 0x800000FF then sign correction
    // This extracts sign bit + low byte, handling negative values
    x = x & (int32_t)0x800000FF;
    if (x < 0) {
        x = ((x - 1) | (int32_t)0xFFFFFF00) + 1;
    }
    return x;
}

void prng_init(int16_t seed) {
    int32_t iseed = (int32_t)seed;  // Sign-extend short to int
    s0 = signed_byte(iseed);
    s1 = signed_byte(s0 + 0x15);
    s2 = signed_byte(s0 - 0x15);
    
    for (int i = 0; i < 11; i++) {
        // Use 32-bit wrapping arithmetic
        int32_t val = (int32_t)((uint32_t)s0 * 0x483 + (uint32_t)s1 * 0x651 + 
                                (uint32_t)s2 * 0x55f + 0x40e6d);
        val = signed_byte(val);
        s2 = s1;
        s1 = s0;
        s0 = val;
    }
    
    // Delphi mod: seed mod 10 with sign of seed
    mode = iseed % 10;
    if (mode < 0) mode += 10;
}

int keystream_byte(void) {
    // Use 32-bit wrapping for the multiplication/addition
    int32_t val = (int32_t)((uint32_t)((uint32_t)s0 * (uint32_t)mult_a[mode]) + 
                            (uint32_t)((uint32_t)s1 * (uint32_t)mult_b[mode]) +
                            (uint32_t)((uint32_t)s2 * (uint32_t)mult_c[mode]) + 
                            0x40e6d);
    
    // Delphi mod: val mod 0x7D03, sign of val
    int32_t ks;
    if (val >= 0) {
        ks = val % 0x7D03;
    } else {
        ks = -((-val) % 0x7D03);
    }
    
    s2 = s1;
    s1 = s0;
    s0 = ks;
    
    int32_t result = ks & (int32_t)0x800000FF;
    if (result < 0) {
        result = ((result - 1) | (int32_t)0xFFFFFF00) + 1;
    }
    return (int)(result & 0xFF);
}

int main(int argc, char **argv) {
    if (argc < 4) {
        fprintf(stderr, "Usage: sl_decrypt2 bruteforce <input> <pattern> [check_len]\n");
        fprintf(stderr, "       sl_decrypt2 decrypt <seed> <input> <output>\n");
        fprintf(stderr, "       sl_decrypt2 dump <seed> <input> [num_bytes]\n");
        return 1;
    }
    
    if (strcmp(argv[1], "bruteforce") == 0) {
        FILE *f = fopen(argv[2], "rb");
        if (!f) { perror("open"); return 1; }
        
        fseek(f, 0, SEEK_END);
        long fsize = ftell(f);
        fseek(f, 0, SEEK_SET);
        
        uint8_t *data = malloc(fsize);
        fread(data, 1, fsize, f);
        fclose(f);
        
        const char *pattern = argv[3];
        int plen = strlen(pattern);
        int check_len = argc > 4 ? atoi(argv[4]) : 128;
        if (check_len > fsize) check_len = fsize;
        
        uint8_t *dec = malloc(check_len);
        
        for (int32_t seed = -32768; seed < 32768; seed++) {
            prng_init((int16_t)seed);
            
            uint8_t prev_cipher = 0xFF;
            uint8_t prev_plain = 0xFF;
            
            for (int i = 0; i < check_len; i++) {
                int ks = keystream_byte();
                dec[i] = (uint8_t)(ks ^ prev_cipher ^ data[i] ^ prev_plain);
                prev_cipher = data[i];
                prev_plain = dec[i];
            }
            
            for (int i = 0; i <= check_len - plen; i++) {
                if (memcmp(dec + i, pattern, plen) == 0) {
                    printf("FOUND seed=%d (0x%04X) offset=%d: ", (int)(int16_t)seed, 
                           (unsigned)(uint16_t)(int16_t)seed, i);
                    for (int j = 0; j < 40 && j < check_len; j++) {
                        if (dec[j] >= 0x20 && dec[j] <= 0x7E) printf("%c", dec[j]);
                        else printf("[%02X]", dec[j]);
                    }
                    printf("\n");
                }
            }
        }
        
        free(data);
        free(dec);
        
    } else if (strcmp(argv[1], "dump") == 0) {
        int seed = atoi(argv[2]);
        FILE *f = fopen(argv[3], "rb");
        if (!f) { perror("open"); return 1; }
        
        fseek(f, 0, SEEK_END);
        long fsize = ftell(f);
        fseek(f, 0, SEEK_SET);
        
        uint8_t *data = malloc(fsize);
        fread(data, 1, fsize, f);
        fclose(f);
        
        int num = argc > 4 ? atoi(argv[4]) : 64;
        if (num > fsize) num = fsize;
        
        prng_init((int16_t)seed);
        uint8_t prev_cipher = 0xFF;
        uint8_t prev_plain = 0xFF;
        
        for (int i = 0; i < num; i++) {
            int ks = keystream_byte();
            uint8_t plain = (uint8_t)(ks ^ prev_cipher ^ data[i] ^ prev_plain);
            prev_cipher = data[i];
            prev_plain = plain;
            
            if (i % 16 == 0) printf("%04X: ", i);
            printf("%02X ", plain);
            if (i % 16 == 15) {
                printf(" ");
                for (int j = i - 15; j <= i; j++) {
                    // recompute... just print hex for now
                }
                printf("\n");
            }
        }
        printf("\n");
        
        free(data);
        
    } else if (strcmp(argv[1], "decrypt") == 0 && argc >= 5) {
        int seed = atoi(argv[2]);
        FILE *fin = fopen(argv[3], "rb");
        if (!fin) { perror("open"); return 1; }
        
        fseek(fin, 0, SEEK_END);
        long fsize = ftell(fin);
        fseek(fin, 0, SEEK_SET);
        
        uint8_t *data = malloc(fsize);
        fread(data, 1, fsize, fin);
        fclose(fin);
        
        prng_init((int16_t)seed);
        uint8_t prev_cipher = 0xFF;
        uint8_t prev_plain = 0xFF;
        
        for (long i = 0; i < fsize; i++) {
            int ks = keystream_byte();
            uint8_t plain = (uint8_t)(ks ^ prev_cipher ^ data[i] ^ prev_plain);
            prev_cipher = data[i];
            data[i] = plain;
            prev_plain = plain;
        }
        
        FILE *fout = fopen(argv[4], "wb");
        fwrite(data, 1, fsize, fout);
        fclose(fout);
        
        printf("Decrypted %ld bytes with seed %d\n", fsize, seed);
        free(data);
    }
    
    return 0;
}
