/*
 * Shree-Lipi ._DL File Decompressor
 * 
 * Reverse-engineered from Shree-Lipi 7.4 Setup.exe (Delphi/LZARI variant)
 * Format: [4-byte LE original size][LZARI compressed data]
 * 
 * Algorithm: Modified LZARI (Okumura)
 *   - Ring buffer: 4096 bytes, init 0x20, start position 0xFC4 (N-60)
 *   - Character model: 314 symbols (1-based), 256 literals + 58 length codes
 *   - Position model: 4096 entries (0-based), logarithmic distribution
 *     p_cum_freq[i] = trunc(p_cum_freq[i+1] + 10000.0 / (i+1+200))
 *   - Arithmetic coder: 17-bit range [0, 0x20000)
 *   - FPU uses truncation mode (round toward zero) via CW 0x1F32
 *   - Rescaling threshold: cum_freq[0] >= 0x7FFF (32767)
 *
 * Build: gcc -O2 -o sl_decompress sl_decompress.c -lm
 * Usage: sl_decompress <input._DL> <output.dll>
 *        sl_decompress --batch <dir>  (extracts all ._DL files in directory tree)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <dirent.h>
#include <sys/stat.h>
#include <libgen.h>
#include <ctype.h>

#define N        4096
#define N_MASK   0xFFF
#define NC       314       /* 256 literals + 58 length codes (lengths 3..60) */
#define NP       4096      /* Position model entries */
#define MAX_FREQ 0x7FFF    /* Rescale when cum_freq[0] >= this */
#define Q1       0x8000
#define Q2       0x10000
#define Q3       0x18000
#define Q4       0x20000

/* ---- Bit Reader ---- */
static unsigned char *g_inbuf;
static size_t g_insize, g_inpos;
static unsigned int g_bitbuf, g_bitmask;

static void bitreader_init(unsigned char *data, size_t size) {
    g_inbuf = data; g_insize = size; g_inpos = 0;
    g_bitbuf = 0; g_bitmask = 0;
}

static int get_bit(void) {
    g_bitmask >>= 1;
    if (g_bitmask == 0) {
        g_bitbuf = (g_inpos < g_insize) ? g_inbuf[g_inpos++] : 0;
        g_bitmask = 0x80;
    }
    return (g_bitbuf & g_bitmask) ? 1 : 0;
}

/* ---- Arithmetic Coder ---- */
static int32_t ac_low, ac_high, ac_value;

static void start_decode(void) {
    ac_value = 0;
    for (int i = 0; i < 17; i++)
        ac_value = (ac_value << 1) | get_bit();
}

static void renorm(void) {
    for (;;) {
        if (ac_low < Q2) {
            if (ac_low < Q1 || ac_high > Q3) {
                if (ac_high > Q2) return;
            } else {
                ac_value -= Q1; ac_low -= Q1; ac_high -= Q1;
            }
        } else {
            ac_value -= Q2; ac_low -= Q2; ac_high -= Q2;
        }
        ac_low *= 2;
        ac_high *= 2;
        ac_value = ac_value * 2 + get_bit();
    }
}

/* ---- Character Model (adaptive, 1-based symbols) ---- */
static int32_t c_sym_to_char[NC + 2];
static int32_t c_char_to_sym[NC + 2];
static int32_t c_freq[NC + 2];
static int32_t c_cum_freq[NC + 2];

static void init_char_model(void) {
    c_cum_freq[NC] = 0;
    for (int i = NC; i >= 1; i--) {
        c_char_to_sym[i - 1] = i;
        c_sym_to_char[i] = i - 1;
        c_freq[i] = 1;
        c_cum_freq[i - 1] = c_cum_freq[i] + 1;
    }
    c_freq[0] = 0;  /* sentinel */
}

static void update_char_model(int sym) {
    int i, j;
    
    if (c_cum_freq[0] >= MAX_FREQ) {
        /* Rescale: halve all frequencies (round up), rebuild cumulative */
        c_cum_freq[NC] = 0;
        for (j = NC; j >= 1; j--) {
            c_freq[j] = (c_freq[j] + 1) >> 1;
            c_cum_freq[j - 1] = c_cum_freq[j] + c_freq[j];
        }
    }
    
    /* Move symbol toward front to maintain frequency-sorted order */
    for (i = sym; i > 1 && c_freq[i] == c_freq[i - 1]; i--)
        ;
    
    if (i < sym) {
        int ch_i = c_sym_to_char[i];
        int ch_sym = c_sym_to_char[sym];
        c_sym_to_char[i] = ch_sym;
        c_sym_to_char[sym] = ch_i;
        c_char_to_sym[ch_i] = sym;
        c_char_to_sym[ch_sym] = i;
    }
    
    c_freq[i]++;
    for (j = i - 1; j >= 0; j--)
        c_cum_freq[j]++;
}

/* ---- Position Model (static, logarithmic distribution) ---- */
static int32_t p_cum_freq[NP + 2];

static void init_pos_model(void) {
    p_cum_freq[NP] = 0;
    for (int i = NP - 1; i >= 0; i--) {
        long double val = 10000.0L / (long double)(i + 1 + 200);
        p_cum_freq[i] = (int32_t)((long double)p_cum_freq[i + 1] + val);
    }
}

/* ---- Decode Functions ---- */

static int decode_char_sym(void) {
    int32_t range = ac_high - ac_low;
    int32_t total = c_cum_freq[0];
    int sym;
    
    int64_t temp = (int64_t)(ac_value - ac_low + 1) * total - 1;
    int32_t cum = (int32_t)(temp / range);
    
    /* Binary search for symbol */
    int lo = 1, hi = NC;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (cum < c_cum_freq[mid]) lo = mid + 1;
        else hi = mid;
    }
    sym = lo;
    
    /* Update arithmetic coder range */
    temp = (int64_t)c_cum_freq[sym - 1] * range;
    ac_high = ac_low + (int32_t)(temp / total);
    temp = (int64_t)c_cum_freq[sym] * range;
    ac_low = ac_low + (int32_t)(temp / total);
    
    renorm();
    
    int ch = c_sym_to_char[sym];
    update_char_model(sym);
    return ch;
}

static int decode_position_sym(void) {
    int32_t range = ac_high - ac_low;
    int32_t total = p_cum_freq[0];
    int sym;
    
    int64_t temp = (int64_t)(ac_value - ac_low + 1) * total - 1;
    int32_t cum = (int32_t)(temp / range);
    
    /* Binary search, returns 0-based position */
    int lo = 1, hi = NP;
    while (lo < hi) {
        int mid = (lo + hi) / 2;
        if (cum < p_cum_freq[mid]) lo = mid + 1;
        else hi = mid;
    }
    sym = lo - 1;
    
    /* Update range: position uses cum_freq[sym] and cum_freq[sym+1] */
    temp = (int64_t)p_cum_freq[sym] * range;
    ac_high = ac_low + (int32_t)(temp / total);
    temp = (int64_t)p_cum_freq[sym + 1] * range;
    ac_low = ac_low + (int32_t)(temp / total);
    
    renorm();
    return sym;
}

/* ---- Main Decompress Function ---- */

static int decompress(const char *infile, const char *outfile) {
    FILE *fin = fopen(infile, "rb");
    if (!fin) { fprintf(stderr, "Cannot open: %s\n", infile); return -1; }
    
    fseek(fin, 0, SEEK_END);
    long fsize = ftell(fin);
    fseek(fin, 0, SEEK_SET);
    
    uint32_t orig_size;
    if (fread(&orig_size, 4, 1, fin) != 1) { fclose(fin); return -1; }
    
    size_t comp_size = fsize - 4;
    unsigned char *comp_data = malloc(comp_size);
    if (fread(comp_data, 1, comp_size, fin) != comp_size) {
        free(comp_data); fclose(fin); return -1;
    }
    fclose(fin);
    
    unsigned char *outbuf = malloc(orig_size + 256);
    unsigned char ring_buf[N];
    memset(ring_buf, 0x20, N);
    int r = N - 60;  /* 0xFC4 */
    
    bitreader_init(comp_data, comp_size);
    init_char_model();
    init_pos_model();
    ac_low = 0;
    ac_high = Q4;
    start_decode();
    
    size_t count = 0;
    while (count < orig_size) {
        int c = decode_char_sym();
        
        if (c < 256) {
            /* Literal byte */
            outbuf[count++] = (unsigned char)c;
            ring_buf[r] = (unsigned char)c;
            r = (r + 1) & N_MASK;
        } else {
            /* Back-reference: length = c - 253 (3..60) */
            int length = c - 253;
            int pos = decode_position_sym();
            int src = (r - pos - 1) & N_MASK;
            
            for (int i = 0; i < length && count < orig_size; i++) {
                unsigned char ch = ring_buf[(src + i) & N_MASK];
                outbuf[count++] = ch;
                ring_buf[r] = ch;
                r = (r + 1) & N_MASK;
            }
        }
    }
    
    FILE *fout = fopen(outfile, "wb");
    if (!fout) { free(comp_data); free(outbuf); return -1; }
    fwrite(outbuf, 1, count, fout);
    fclose(fout);
    
    free(comp_data);
    free(outbuf);
    return 0;
}

/* ---- Batch Mode ---- */

static int process_dir(const char *dirpath, const char *outdir, int *total, int *success) {
    DIR *d = opendir(dirpath);
    if (!d) return -1;
    
    struct dirent *ent;
    while ((ent = readdir(d)) != NULL) {
        if (ent->d_name[0] == '.') continue;
        
        char fullpath[4096];
        snprintf(fullpath, sizeof(fullpath), "%s/%s", dirpath, ent->d_name);
        
        struct stat st;
        if (stat(fullpath, &st) != 0) continue;
        
        if (S_ISDIR(st.st_mode)) {
            process_dir(fullpath, outdir, total, success);
            continue;
        }
        
        /* Check for ._DL extension */
        size_t len = strlen(ent->d_name);
        if (len < 4) continue;
        const char *ext = ent->d_name + len - 4;
        if (strcasecmp(ext, "._DL") != 0 && strcasecmp(ext, "._dl") != 0) continue;
        
        /* Build output filename: replace ._DL with .dll */
        char outname[256];
        strncpy(outname, ent->d_name, len - 4);
        outname[len - 4] = '\0';
        strcat(outname, ".dll");
        
        /* Build relative path for output */
        char outpath[4096];
        snprintf(outpath, sizeof(outpath), "%s/%s", outdir, outname);
        
        (*total)++;
        fprintf(stderr, "[%d] %s -> %s ... ", *total, fullpath, outpath);
        
        if (decompress(fullpath, outpath) == 0) {
            (*success)++;
            
            /* Report size */
            struct stat ost;
            if (stat(outpath, &ost) == 0) {
                fprintf(stderr, "OK (%ld -> %ld bytes)\n", st.st_size, ost.st_size);
            } else {
                fprintf(stderr, "OK\n");
            }
        } else {
            fprintf(stderr, "FAILED\n");
        }
    }
    
    closedir(d);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Shree-Lipi ._DL Decompressor\n");
        fprintf(stderr, "Usage:\n");
        fprintf(stderr, "  %s <input._DL> <output.dll>        Single file\n", argv[0]);
        fprintf(stderr, "  %s --batch <dir> [outdir]           Batch extract\n", argv[0]);
        return 1;
    }
    
    if (strcmp(argv[1], "--batch") == 0) {
        if (argc < 3) {
            fprintf(stderr, "Usage: %s --batch <dir> [outdir]\n", argv[0]);
            return 1;
        }
        const char *dir = argv[2];
        const char *outdir = (argc >= 4) ? argv[3] : "/tmp/sl_extracted";
        
        mkdir(outdir, 0755);
        
        int total = 0, success = 0;
        process_dir(dir, outdir, &total, &success);
        fprintf(stderr, "\nDone: %d/%d files extracted to %s\n", success, total, outdir);
        return (success == total) ? 0 : 1;
    }
    
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <input._DL> <output.dll>\n", argv[0]);
        return 1;
    }
    
    return decompress(argv[1], argv[2]);
}
