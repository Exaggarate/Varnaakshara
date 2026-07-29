/**
 * StylesPanel — InDesign-style paragraph & character styles panel.
 * Click a style to apply it to the current selection in the editor.
 */
import React, { useState, useCallback } from 'react';

/* ── Built-in Paragraph Styles ────────────────────────────────────────────── */
const PARAGRAPH_STYLES = [
  {
    id: 'normal', name: 'Normal',
    fontFamily: 'Noto Serif', fontSize: '12pt', fontWeight: 'normal',
    fontStyle: 'normal', desc: 'Noto Serif, 12pt',
  },
  {
    id: 'h1', name: 'Heading 1',
    fontFamily: 'Noto Sans', fontSize: '24pt', fontWeight: 'bold',
    fontStyle: 'normal', desc: 'Noto Sans, 24pt Bold',
  },
  {
    id: 'h2', name: 'Heading 2',
    fontFamily: 'Noto Sans', fontSize: '18pt', fontWeight: 'bold',
    fontStyle: 'normal', desc: 'Noto Sans, 18pt Bold',
  },
  {
    id: 'h3', name: 'Heading 3',
    fontFamily: 'Noto Sans', fontSize: '14pt', fontWeight: 'bold',
    fontStyle: 'normal', desc: 'Noto Sans, 14pt Bold',
  },
  {
    id: 'h4', name: 'Heading 4',
    fontFamily: 'Noto Sans', fontSize: '12pt', fontWeight: 'bold',
    fontStyle: 'normal', desc: 'Noto Sans, 12pt Bold',
  },
  {
    id: 'title', name: 'Title',
    fontFamily: 'Noto Serif', fontSize: '28pt', fontWeight: 'bold',
    fontStyle: 'normal', desc: 'Noto Serif, 28pt Bold',
  },
  {
    id: 'subtitle', name: 'Subtitle',
    fontFamily: 'Noto Serif', fontSize: '16pt', fontWeight: 'normal',
    fontStyle: 'italic', desc: 'Noto Serif, 16pt Italic',
  },
  {
    id: 'quote', name: 'Quote',
    fontFamily: 'Noto Serif', fontSize: '12pt', fontWeight: 'normal',
    fontStyle: 'italic', desc: 'Noto Serif, 12pt Italic',
  },
  {
    id: 'code', name: 'Code Block',
    fontFamily: 'Consolas, monospace', fontSize: '11pt', fontWeight: 'normal',
    fontStyle: 'normal', desc: 'Consolas, 11pt',
  },
  {
    id: 'list', name: 'List Paragraph',
    fontFamily: 'Noto Serif', fontSize: '12pt', fontWeight: 'normal',
    fontStyle: 'normal', desc: 'Noto Serif, 12pt',
  },
];

/* ── Built-in Character Styles ────────────────────────────────────────────── */
const CHARACTER_STYLES = [
  {
    id: 'default', name: 'Default',
    fontWeight: 'normal', fontStyle: 'normal',
    textDecoration: 'none', desc: 'Regular',
  },
  {
    id: 'bold', name: 'Bold',
    fontWeight: 'bold', fontStyle: 'normal',
    textDecoration: 'none', desc: 'Bold',
  },
  {
    id: 'italic', name: 'Italic',
    fontWeight: 'normal', fontStyle: 'italic',
    textDecoration: 'none', desc: 'Italic',
  },
  {
    id: 'strong', name: 'Strong Emphasis',
    fontWeight: 'bold', fontStyle: 'italic',
    textDecoration: 'none', desc: 'Bold Italic',
  },
  {
    id: 'subtle', name: 'Subtle Emphasis',
    fontWeight: 'normal', fontStyle: 'italic',
    textDecoration: 'none', desc: 'Italic, muted', opacity: 0.7,
  },
  {
    id: 'book-title', name: 'Book Title',
    fontWeight: 'bold', fontStyle: 'italic',
    textDecoration: 'underline', desc: 'Bold Italic Underline',
  },
];

/* ── Component ────────────────────────────────────────────────────────────── */
export default function StylesPanel() {
  const [subTab, setSubTab] = useState('paragraph'); // 'paragraph' | 'character'

  const applyParagraphStyle = useCallback((styleId) => {
    window.dispatchEvent(
      new CustomEvent('varnaakshara-apply-style', {
        detail: { type: 'paragraph', styleId },
      }),
    );
  }, []);

  const applyCharacterStyle = useCallback((styleId) => {
    window.dispatchEvent(
      new CustomEvent('varnaakshara-apply-style', {
        detail: { type: 'character', styleId },
      }),
    );
  }, []);

  return (
    <div className="panel-styles">
      {/* Sub-tab selector */}
      <div className="panel-styles-tabs">
        <button
          className={`panel-styles-tab ${subTab === 'paragraph' ? 'active' : ''}`}
          onClick={() => setSubTab('paragraph')}
        >
          ¶ Paragraph
        </button>
        <button
          className={`panel-styles-tab ${subTab === 'character' ? 'active' : ''}`}
          onClick={() => setSubTab('character')}
        >
          A Character
        </button>
      </div>

      {/* Paragraph Styles */}
      {subTab === 'paragraph' && (
        <div className="panel-styles-list">
          {PARAGRAPH_STYLES.map((style) => (
            <div
              key={style.id}
              className="panel-style-item"
              onClick={() => applyParagraphStyle(style.id)}
              title={`Apply "${style.name}" — ${style.desc}`}
            >
              <div className="panel-style-preview">
                <span
                  style={{
                    fontFamily: style.fontFamily,
                    fontSize: Math.min(parseInt(style.fontSize), 16) + 'px',
                    fontWeight: style.fontWeight,
                    fontStyle: style.fontStyle || 'normal',
                  }}
                >
                  {style.name}
                </span>
              </div>
              <div className="panel-style-meta">{style.desc}</div>
            </div>
          ))}

          <div className="panel-styles-footer">
            <button className="panel-btn" style={{ flex: 1, opacity: 0.5, cursor: 'default' }} disabled>
              + New Style
            </button>
          </div>
        </div>
      )}

      {/* Character Styles */}
      {subTab === 'character' && (
        <div className="panel-styles-list">
          {CHARACTER_STYLES.map((style) => (
            <div
              key={style.id}
              className="panel-style-item"
              onClick={() => applyCharacterStyle(style.id)}
              title={`Apply "${style.name}" — ${style.desc}`}
            >
              <div className="panel-style-preview">
                <span
                  style={{
                    fontWeight: style.fontWeight,
                    fontStyle: style.fontStyle || 'normal',
                    textDecoration: style.textDecoration || 'none',
                    opacity: style.opacity || 1,
                  }}
                >
                  Aa {style.name}
                </span>
              </div>
              <div className="panel-style-meta">{style.desc}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
