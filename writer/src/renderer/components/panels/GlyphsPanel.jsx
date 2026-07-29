/**
 * GlyphsPanel — Unicode character map browser for Indian scripts.
 * Shows a selectable grid of glyphs with search, recently-used tracking,
 * and click-to-insert functionality.
 */
import React, { useState, useEffect, useMemo, useCallback } from 'react';

/* ── Script Definitions ───────────────────────────────────────────────────── */
const SCRIPTS = [
  { id: 'kannada',    name: 'Kannada',    range: [0x0C80, 0x0CFF] },
  { id: 'devanagari', name: 'Devanagari', range: [0x0900, 0x097F] },
  { id: 'telugu',     name: 'Telugu',     range: [0x0C00, 0x0C7F] },
  { id: 'tamil',      name: 'Tamil',      range: [0x0B80, 0x0BFF] },
  { id: 'malayalam',  name: 'Malayalam',   range: [0x0D00, 0x0D7F] },
  { id: 'bengali',    name: 'Bengali',    range: [0x0980, 0x09FF] },
  { id: 'gujarati',   name: 'Gujarati',   range: [0x0A80, 0x0AFF] },
  { id: 'gurmukhi',   name: 'Gurmukhi',   range: [0x0A00, 0x0A7F] },
  { id: 'odia',       name: 'Odia',       range: [0x0B00, 0x0B7F] },
];

/* ── Indic Unicode Offset → Name Table ────────────────────────────────────── */
const INDIC_OFFSETS = {
  0x01: 'SIGN CANDRABINDU', 0x02: 'SIGN ANUSVARA', 0x03: 'SIGN VISARGA',
  0x04: 'SIGN AVAGRAHA',
  0x05: 'LETTER A',  0x06: 'LETTER AA', 0x07: 'LETTER I',  0x08: 'LETTER II',
  0x09: 'LETTER U',  0x0A: 'LETTER UU', 0x0B: 'LETTER VOCALIC R',
  0x0C: 'LETTER VOCALIC L', 0x0D: 'LETTER CANDRA E',
  0x0E: 'LETTER SHORT E',   0x0F: 'LETTER E',  0x10: 'LETTER AI',
  0x11: 'LETTER CANDRA O',  0x12: 'LETTER SHORT O', 0x13: 'LETTER O',
  0x14: 'LETTER AU',
  0x15: 'LETTER KA', 0x16: 'LETTER KHA', 0x17: 'LETTER GA',
  0x18: 'LETTER GHA', 0x19: 'LETTER NGA',
  0x1A: 'LETTER CA', 0x1B: 'LETTER CHA', 0x1C: 'LETTER JA',
  0x1D: 'LETTER JHA', 0x1E: 'LETTER NYA',
  0x1F: 'LETTER TTA', 0x20: 'LETTER TTHA', 0x21: 'LETTER DDA',
  0x22: 'LETTER DDHA', 0x23: 'LETTER NNA',
  0x24: 'LETTER TA', 0x25: 'LETTER THA', 0x26: 'LETTER DA',
  0x27: 'LETTER DHA', 0x28: 'LETTER NA', 0x29: 'LETTER NNNA',
  0x2A: 'LETTER PA', 0x2B: 'LETTER PHA', 0x2C: 'LETTER BA',
  0x2D: 'LETTER BHA', 0x2E: 'LETTER MA',
  0x2F: 'LETTER YA', 0x30: 'LETTER RA', 0x31: 'LETTER RRA',
  0x32: 'LETTER LA', 0x33: 'LETTER LLA', 0x34: 'LETTER LLLA',
  0x35: 'LETTER VA', 0x36: 'LETTER SHA', 0x37: 'LETTER SSA',
  0x38: 'LETTER SA', 0x39: 'LETTER HA',
  0x3C: 'SIGN NUKTA', 0x3D: 'SIGN AVAGRAHA',
  0x3E: 'VOWEL SIGN AA', 0x3F: 'VOWEL SIGN I', 0x40: 'VOWEL SIGN II',
  0x41: 'VOWEL SIGN U', 0x42: 'VOWEL SIGN UU',
  0x43: 'VOWEL SIGN VOCALIC R', 0x44: 'VOWEL SIGN VOCALIC RR',
  0x46: 'VOWEL SIGN E', 0x47: 'VOWEL SIGN EE', 0x48: 'VOWEL SIGN AI',
  0x4A: 'VOWEL SIGN O', 0x4B: 'VOWEL SIGN OO', 0x4C: 'VOWEL SIGN AU',
  0x4D: 'SIGN VIRAMA',
  0x55: 'LENGTH MARK', 0x56: 'AI LENGTH MARK', 0x57: 'AU LENGTH MARK',
  0x60: 'LETTER VOCALIC RR', 0x61: 'LETTER VOCALIC LL',
  0x62: 'VOWEL SIGN VOCALIC L', 0x63: 'VOWEL SIGN VOCALIC LL',
  0x66: 'DIGIT ZERO', 0x67: 'DIGIT ONE', 0x68: 'DIGIT TWO',
  0x69: 'DIGIT THREE', 0x6A: 'DIGIT FOUR', 0x6B: 'DIGIT FIVE',
  0x6C: 'DIGIT SIX', 0x6D: 'DIGIT SEVEN', 0x6E: 'DIGIT EIGHT',
  0x6F: 'DIGIT NINE',
  0x70: 'ISSHAR', 0x71: 'SIGN AVAGRAHA',
};

function getCharName(scriptName, codePoint, base) {
  const offset = codePoint - base;
  const suffix = INDIC_OFFSETS[offset];
  const hex = 'U+' + codePoint.toString(16).toUpperCase().padStart(4, '0');
  if (suffix) return `${scriptName.toUpperCase()} ${suffix}`;
  return `${scriptName.toUpperCase()} ${hex}`;
}

/* ── Font Options ─────────────────────────────────────────────────────────── */
const FONT_OPTIONS = [
  'Noto Sans',
  'Noto Serif',
  'Noto Sans Kannada',
  'Noto Sans Devanagari',
  'Arial Unicode MS',
  'Segoe UI',
  'sans-serif',
];

const RECENT_KEY = 'varnaakshara-recent-glyphs';
const MAX_RECENT = 20;

/* ── Component ────────────────────────────────────────────────────────────── */
export default function GlyphsPanel({ onInsertText }) {
  const [activeScript, setActiveScript] = useState('kannada');
  const [search, setSearch] = useState('');
  const [font, setFont] = useState('Noto Sans');
  const [recentGlyphs, setRecentGlyphs] = useState(() => {
    try {
      return JSON.parse(localStorage.getItem(RECENT_KEY) || '[]');
    } catch { return []; }
  });

  const script = SCRIPTS.find((s) => s.id === activeScript) || SCRIPTS[0];

  /* Build character list for selected script */
  const allChars = useMemo(() => {
    const [start, end] = script.range;
    const chars = [];
    for (let cp = start; cp <= end; cp++) {
      const char = String.fromCodePoint(cp);
      const name = getCharName(script.name, cp, start - (start % 0x80));
      const hex = 'U+' + cp.toString(16).toUpperCase().padStart(4, '0');
      chars.push({ char, codePoint: cp, hex, decimal: cp, name });
    }
    return chars;
  }, [script]);

  /* Filtered list */
  const filteredChars = useMemo(() => {
    if (!search.trim()) return allChars;
    const q = search.toLowerCase();
    return allChars.filter(
      (c) =>
        c.name.toLowerCase().includes(q) ||
        c.hex.toLowerCase().includes(q) ||
        c.char.includes(q),
    );
  }, [allChars, search]);

  /* Insert glyph */
  const handleInsert = useCallback(
    (char) => {
      /* Fire insert event */
      if (onInsertText) {
        onInsertText(char);
      }
      window.dispatchEvent(
        new CustomEvent('varnaakshara-insert-text', { detail: { text: char } }),
      );

      /* Update recent */
      setRecentGlyphs((prev) => {
        const next = [char, ...prev.filter((c) => c !== char)].slice(0, MAX_RECENT);
        try { localStorage.setItem(RECENT_KEY, JSON.stringify(next)); } catch {}
        return next;
      });
    },
    [onInsertText],
  );

  return (
    <div className="panel-glyphs">
      {/* Script selector */}
      <div className="panel-row">
        <select
          className="panel-select"
          value={activeScript}
          onChange={(e) => setActiveScript(e.target.value)}
          style={{ flex: 1 }}
        >
          {SCRIPTS.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
      </div>

      {/* Search */}
      <div className="panel-row">
        <input
          className="panel-input"
          type="text"
          placeholder="Search glyphs…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* Font selector */}
      <div className="panel-row">
        <span className="panel-label" style={{ minWidth: 32, fontSize: 10 }}>Font</span>
        <select
          className="panel-select"
          value={font}
          onChange={(e) => setFont(e.target.value)}
          style={{ flex: 1 }}
        >
          {FONT_OPTIONS.map((f) => (
            <option key={f} value={f}>{f}</option>
          ))}
        </select>
      </div>

      {/* Recently Used */}
      {recentGlyphs.length > 0 && !search && (
        <div className="panel-glyphs-section">
          <div className="panel-glyphs-section-title">Recently Used</div>
          <div className="glyph-grid">
            {recentGlyphs.map((char, i) => {
              const cp = char.codePointAt(0);
              const hex = 'U+' + cp.toString(16).toUpperCase().padStart(4, '0');
              return (
                <div
                  key={`recent-${i}`}
                  className="glyph-cell"
                  onClick={() => handleInsert(char)}
                  title={`${hex}  (${cp})`}
                  style={{ fontFamily: font }}
                >
                  {char}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Main glyph grid */}
      <div className="panel-glyphs-section">
        <div className="panel-glyphs-section-title">
          {script.name} — {filteredChars.length} glyphs
        </div>
        <div className="glyph-grid">
          {filteredChars.map((c) => (
            <div
              key={c.codePoint}
              className="glyph-cell"
              onClick={() => handleInsert(c.char)}
              title={`${c.name}\n${c.hex}  (${c.decimal})`}
              style={{ fontFamily: font }}
            >
              {c.char}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
