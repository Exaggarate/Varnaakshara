#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define N 4096
#define F 60
#define THRESHOLD 2
#define N_CHAR (256 - THRESHOLD + F + 1)
#define Q1 32768U
#define Q2 65536U
#define Q3 98304U
#define Q4 131072U
#define MAX_CUM (Q1 - 1)

static unsigned char text_buf[N];
static int char_to_sym[N_CHAR+1], sym_to_char[N_CHAR+1];
static unsigned int sym_freq[N_CHAR+1], sym_cum[N_CHAR+1];
static double position_cum[N+1];

static unsigned char *inbuf;
static int inpos, insize;
static unsigned long low, high, value;

static int GetBit(void) {
    static int gbuf = 0, glen = 0;
    if (glen <= 0) {
        gbuf = (inpos < insize) ? inbuf[inpos++] : 0;
        glen = 8;
    }
    glen--;
    int r = (gbuf >> 7) & 1;
    gbuf = (gbuf << 1) & 0xFF;
    return r;
}

static void StartModel(void) {
    sym_cum[N_CHAR] = 0;
    for (int sym = N_CHAR; sym >= 1; sym--) {
        char_to_sym[sym-1] = sym;
        sym_to_char[sym] = sym-1;
        sym_freq[sym] = 1;
        sym_cum[sym-1] = sym_cum[sym] + 1;
    }
    sym_freq[0] = 0;
    position_cum[N] = 0;
    for (int i = N; i >= 1; i--)
        position_cum[i-1] = position_cum[i] + 10000.0 / (i + 200);
}

static void UpdateModel(int sym) {
    if (sym_cum[0] >= MAX_CUM) {
        unsigned int c = 0;
        for (int i = N_CHAR; i > 0; i--) {
            sym_cum[i] = c;
            sym_freq[i] = (sym_freq[i] + 1) >> 1;
            c += sym_freq[i];
        }
        sym_cum[0] = c;
    }
    int i = sym;
    while (sym_freq[i] == sym_freq[i-1]) i--;
    if (i < sym) {
        int ci = sym_to_char[i], cs = sym_to_char[sym];
        sym_to_char[i] = cs; sym_to_char[sym] = ci;
        char_to_sym[ci] = sym; char_to_sym[cs] = i;
    }
    sym_freq[i]++;
    for (int j = i-1; j >= 0; j--) sym_cum[j]++;
}

static void Normalize(void) {
    for (;;) {
        if (low >= Q2) { value -= Q2; low -= Q2; high -= Q2; }
        else if (low >= Q1 && high <= Q3) { value -= Q1; low -= Q1; high -= Q1; }
        else if (high > Q2) break;
        low += low; high += high;
        value = 2 * value + GetBit();
    }
}

static int DecodeChar(void) {
    unsigned long range = high - low;
    double cum_d = (double)((value - low + 1) * sym_cum[0] - 1) / (double)range;
    int cum = (int)cum_d;
    int sym; for (sym = 1; sym_cum[sym] > (unsigned)cum; sym++);
    high = low + (unsigned long)((double)(range * sym_cum[sym-1]) / (double)sym_cum[0]);
    low += (unsigned long)((double)(range * sym_cum[sym]) / (double)sym_cum[0]) + 1;
    Normalize();
    int ch = sym_to_char[sym];
    UpdateModel(sym);
    return ch;
}

static int DecodePosition(void) {
    unsigned long range = high - low;
    double cum_d = (double)((value - low + 1) * position_cum[0] - 1.0) / (double)range;
    double cum = cum_d;
    int pos; for (pos = 1; position_cum[pos] > cum; pos++);
    high = low + (unsigned long)((double)range * position_cum[pos-1] / position_cum[0]);
    low += (unsigned long)((double)range * position_cum[pos] / position_cum[0]) + 1;
    Normalize();
    return pos - 1;
}

int main(int argc, char *argv[]) {
    if (argc < 3) { fprintf(stderr, "Usage: %s input.sl output.ttf [size]\n", argv[0]); return 1; }
    
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END); int fsize = ftell(f); rewind(f);
    
    unsigned char hdr[4];
    fread(hdr, 1, 4, f);
    unsigned long orig_size = hdr[0] | (hdr[1]<<8) | (hdr[2]<<16) | (hdr[3]<<24);
    
    if (argc >= 4) orig_size = strtoul(argv[3], NULL, 10);
    
    insize = fsize - 4;
    inbuf = malloc(insize);
    fread(inbuf, 1, insize, f);
    fclose(f);
    inpos = 0;
    
    fprintf(stderr, "Header: %02x%02x%02x%02x (=%lu), data: %d bytes, orig: %lu\n",
            hdr[0],hdr[1],hdr[2],hdr[3], 
            (unsigned long)(hdr[0]|(hdr[1]<<8)|(hdr[2]<<16)|(hdr[3]<<24)),
            insize, orig_size);
    
    StartModel();
    low = 0; high = Q4; value = 0;
    for (int i = 0; i < 17; i++) value = 2*value + GetBit();
    
    memset(text_buf, ' ', N - F);
    int r = N - F;
    
    unsigned char *out = malloc(orig_size + 1);
    unsigned long count = 0;
    
    while (count < orig_size) {
        int c = DecodeChar();
        if (c < 256) {
            out[count++] = c;
            text_buf[r++] = c; r &= (N-1);
        } else {
            int pos = DecodePosition();
            int src = (r - pos - 1) & (N-1);
            int len = c - 255 + THRESHOLD;
            for (int k = 0; k < len; k++) {
                c = text_buf[(src + k) & (N-1)];
                out[count++] = c;
                text_buf[r++] = c; r &= (N-1);
            }
        }
    }
    
    f = fopen(argv[2], "wb");
    fwrite(out, 1, orig_size, f);
    fclose(f);
    fprintf(stderr, "Decoded %lu bytes\n", count);
    
    unsigned char *hd = out;
    fprintf(stderr, "First 4 bytes: %02x %02x %02x %02x\n", hd[0],hd[1],hd[2],hd[3]);
    
    free(out); free(inbuf);
    return 0;
}
