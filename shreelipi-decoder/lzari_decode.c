#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define N        4096
#define F        60
#define THRESHOLD 2
#define NIL      N
#define N_CHAR   (256 - THRESHOLD + F)
#define M        15
#define Q1       (1U << M)
#define Q2       (2 * Q1)
#define Q3       (3 * Q1)
#define Q4       (4 * Q1)
#define MAX_CUM  (Q1 - 1)

static unsigned char text_buf[N + F - 1];
static int match_position, match_length;
static int lson[N + 1], rson[N + 257], dad[N + 1];
static int char_to_sym[N_CHAR], sym_to_char[N_CHAR + 1];
static unsigned int sym_freq[N_CHAR + 1], sym_cum[N_CHAR + 1];
static unsigned int position_cum[N + 1];
static FILE *infile, *outfile;
static unsigned long low, high, value;
static int shifts;
static unsigned long textsize, codesize;

/* EXACT Okumura bit I/O */
static int getbuf = 0, getlen = 0;
static int putbuf = 0, putlen = 0;

static void PutBit(int bit) {
    if (bit) putbuf |= (0x80 >> putlen);
    if (++putlen >= 8) {
        fputc(putbuf, outfile); codesize++;
        putbuf = 0; putlen = 0;
    }
}

static void FlushBits(void) {
    int i;
    for (i = 0; i < 7; i++) PutBit(0);
}

static int GetBit(void) {
    int i;
    while (getlen <= 0) {
        getbuf = fgetc(infile);
        if (getbuf == EOF) getbuf = 0;
        getlen = 8;
    }
    getlen--;
    i = getbuf;
    getbuf <<= 1;
    return (i >> 7) & 1;
}

static void InitTree(void) {
    int i;
    for (i = N + 1; i <= N + 256; i++) rson[i] = NIL;
    for (i = 0; i < N; i++) dad[i] = NIL;
}

static void InsertNode(int r) {
    int i, p, cmp; unsigned char *key = &text_buf[r];
    cmp = 1; p = N + 1 + key[0];
    rson[r] = lson[r] = NIL; match_length = 0;
    for (;;) {
        if (cmp >= 0) { if (rson[p] != NIL) p = rson[p]; else { rson[p] = r; dad[r] = p; return; } }
        else          { if (lson[p] != NIL) p = lson[p]; else { lson[p] = r; dad[r] = p; return; } }
        for (i = 1; i < F; i++) if ((cmp = key[i] - text_buf[p + i]) != 0) break;
        if (i > THRESHOLD) {
            if (i > match_length) { match_position = ((r - p) & (N - 1)) - 1; if ((match_length = i) >= F) break; }
            if (i == match_length && (unsigned)((r - p) & (N - 1)) - 1 < (unsigned)match_position) match_position = ((r - p) & (N - 1)) - 1;
        }
    }
    dad[r] = dad[p]; lson[r] = lson[p]; rson[r] = rson[p];
    dad[lson[p]] = r; dad[rson[p]] = r;
    if (rson[dad[p]] == p) rson[dad[p]] = r; else lson[dad[p]] = r;
    dad[p] = NIL;
}

static void DeleteNode(int p) {
    int q;
    if (dad[p] == NIL) return;
    if (rson[p] == NIL) q = lson[p]; else if (lson[p] == NIL) q = rson[p];
    else { q = lson[p]; if (rson[q] != NIL) { do q = rson[q]; while (rson[q] != NIL);
        rson[dad[q]] = lson[q]; dad[lson[q]] = dad[q]; lson[q] = lson[p]; dad[lson[p]] = q; }
        rson[q] = rson[p]; dad[rson[p]] = q; }
    dad[q] = dad[p]; if (rson[dad[p]] == p) rson[dad[p]] = q; else lson[dad[p]] = q; dad[p] = NIL;
}

static void StartModel(void) {
    int ch, sym, i;
    sym_cum[N_CHAR] = 0;
    for (sym = N_CHAR; sym >= 1; sym--) { ch = sym - 1; char_to_sym[ch] = sym; sym_to_char[sym] = ch;
        sym_freq[sym] = 1; sym_cum[sym - 1] = sym_cum[sym] + sym_freq[sym]; }
    sym_freq[0] = 0;
    position_cum[N] = 0;
    for (i = N; i >= 1; i--) position_cum[i - 1] = position_cum[i] + 10000 / (i + 200);
}

static void UpdateModel(int sym) {
    int i, c, ch_i, ch_sym;
    if (sym_cum[0] >= MAX_CUM) { c = 0; for (i = N_CHAR; i > 0; i--) { sym_cum[i] = c; c += (sym_freq[i] = (sym_freq[i] + 1) >> 1); } sym_cum[0] = c; }
    for (i = sym; sym_freq[i] == sym_freq[i - 1]; i--);
    if (i < sym) { ch_i = sym_to_char[i]; ch_sym = sym_to_char[sym]; sym_to_char[i] = ch_sym; sym_to_char[sym] = ch_i; char_to_sym[ch_i] = sym; char_to_sym[ch_sym] = i; }
    sym_freq[i]++; while (--i >= 0) sym_cum[i]++;
}

static void Output(int bit) { PutBit(bit); for (; shifts > 0; shifts--) PutBit(!bit); }

static void EncodeChar(int ch) {
    unsigned long range; int sym = char_to_sym[ch];
    range = high - low; high = low + (range * sym_cum[sym - 1]) / sym_cum[0]; low += (range * sym_cum[sym]) / sym_cum[0];
    for (;;) { if (high <= Q2) Output(0); else if (low >= Q2) { Output(1); low -= Q2; high -= Q2; }
        else if (low >= Q1 && high <= Q3) { shifts++; low -= Q1; high -= Q1; } else break; low += low; high += high; }
    UpdateModel(sym);
}

static void EncodePosition(int position) {
    unsigned long range = high - low;
    high = low + (range * position_cum[position]) / position_cum[0]; low += (range * position_cum[position + 1]) / position_cum[0];
    for (;;) { if (high <= Q2) Output(0); else if (low >= Q2) { Output(1); low -= Q2; high -= Q2; }
        else if (low >= Q1 && high <= Q3) { shifts++; low -= Q1; high -= Q1; } else break; low += low; high += high; }
}

static void EncodeEnd(void) { shifts++; Output(low < Q1 ? 0 : 1); FlushBits(); }

static int DecodeChar(void) {
    unsigned long range = high - low;
    unsigned long cum = ((value - low + 1) * sym_cum[0] - 1) / range;
    int sym; for (sym = 1; sym_cum[sym] > cum; sym++);
    high = low + (range * sym_cum[sym - 1]) / sym_cum[0]; low += (range * sym_cum[sym]) / sym_cum[0];
    for (;;) { if (low >= Q2) { value -= Q2; low -= Q2; high -= Q2; }
        else if (low >= Q1 && high <= Q3) { value -= Q1; low -= Q1; high -= Q1; } else if (high > Q2) break;
        low += low; high += high; value = 2 * value + GetBit(); }
    int ch = sym_to_char[sym]; UpdateModel(sym); return ch;
}

static int DecodePosition(void) {
    unsigned long range = high - low;
    unsigned long cum = ((value - low + 1) * position_cum[0] - 1) / range;
    int pos; for (pos = 1; position_cum[pos] > cum; pos++);
    high = low + (range * position_cum[pos - 1]) / position_cum[0]; low += (range * position_cum[pos]) / position_cum[0];
    for (;;) { if (low >= Q2) { value -= Q2; low -= Q2; high -= Q2; }
        else if (low >= Q1 && high <= Q3) { value -= Q1; low -= Q1; high -= Q1; } else if (high > Q2) break;
        low += low; high += high; value = 2 * value + GetBit(); }
    return pos - 1;
}

static void Encode(void) {
    int i, c, len, r, s, last_match_length;
    fseek(infile, 0, SEEK_END); textsize = ftell(infile); rewind(infile);
    fputc(textsize & 0xff, outfile); fputc((textsize >> 8) & 0xff, outfile);
    fputc((textsize >> 16) & 0xff, outfile); fputc((textsize >> 24) & 0xff, outfile);
    codesize = 4; if (textsize == 0) return;
    StartModel(); InitTree(); low = 0; high = Q4; shifts = 0;
    putbuf = 0; putlen = 0;
    s = 0; r = N - F; memset(text_buf, ' ', r);
    for (len = 0; len < F && (c = fgetc(infile)) != EOF; len++) text_buf[r + len] = c;
    textsize = len;
    for (i = 1; i <= F; i++) InsertNode(r - i);
    InsertNode(r);
    do {
        if (match_length > len) match_length = len;
        if (match_length <= THRESHOLD) { match_length = 1; EncodeChar(text_buf[r]); }
        else { EncodeChar(255 - THRESHOLD + match_length); EncodePosition(match_position); }
        last_match_length = match_length;
        for (i = 0; i < last_match_length && (c = fgetc(infile)) != EOF; i++) {
            DeleteNode(s); text_buf[s] = c; if (s < F - 1) text_buf[s + N] = c;
            s = (s + 1) & (N - 1); r = (r + 1) & (N - 1); InsertNode(r); }
        textsize += i;
        while (i++ < last_match_length) { DeleteNode(s); s = (s + 1) & (N - 1); r = (r + 1) & (N - 1); if (--len) InsertNode(r); }
    } while (len > 0);
    EncodeEnd();
    fprintf(stderr, "In: %lu, Out: %lu\n", textsize, codesize);
}

static void Decode(void) {
    int i, j, k, r, c; unsigned long count;
    textsize = fgetc(infile); textsize |= (unsigned long)fgetc(infile) << 8;
    textsize |= (unsigned long)fgetc(infile) << 16; textsize |= (unsigned long)fgetc(infile) << 24;
    fprintf(stderr, "Size: %lu\n", textsize); if (textsize == 0) return;
    StartModel(); getbuf = 0; getlen = 0;
    low = 0; high = Q4; value = 0;
    memset(text_buf, ' ', N - F); r = N - F;
    for (i = 0; i <= M + 1; i++) value = 2 * value + GetBit();
    for (count = 0; count < textsize;) {
        c = DecodeChar();
        if (c < 256) { fputc(c, outfile); text_buf[r++] = c; r &= (N - 1); count++; }
        else { i = (r - DecodePosition() - 1) & (N - 1); j = c - 255 + THRESHOLD;
            for (k = 0; k < j; k++) { c = text_buf[(i + k) & (N - 1)]; fputc(c, outfile); text_buf[r++] = c; r &= (N - 1); count++; } }
    }
}

int main(int argc, char *argv[]) {
    if (argc != 4 || (argv[1][0] != 'e' && argv[1][0] != 'd')) { fprintf(stderr, "Usage: %s e|d in out\n", argv[0]); return 1; }
    infile = fopen(argv[2], "rb"); outfile = fopen(argv[3], "wb");
    if (!infile || !outfile) { perror("fopen"); return 1; }
    if (argv[1][0] == 'e') Encode(); else Decode();
    fclose(infile); fclose(outfile); return 0;
}
