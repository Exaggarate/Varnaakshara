/**
 * SymbolPickerPlugin — A modal character picker dialog with common symbols and Unicode blocks.
 */
import React, { useCallback, useState } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { $getSelection, $isRangeSelection, $createTextNode } from 'lexical';

const SYMBOL_CATEGORIES = {
  'Common': [
    '©', '®', '™', '°', '±', '×', '÷', '•', '…', '—', '–', '¶', '§', '†', '‡',
    '€', '£', '¥', '¢', '₹', '∞', '≈', '≠', '≤', '≥', '√', 'π', 'µ', 'Ω', 'α',
    'β', 'γ', 'δ', 'λ', 'σ', 'θ', 'φ', '←', '→', '↑', '↓', '↔', '⇐', '⇒', '⇑',
    '⇓', '♠', '♣', '♥', '♦', '★', '☆', '✓', '✗', '✦', '⚡', '☀', '☁', '☂', '☃',
  ],
  'Math': [
    '∑', '∏', '∫', '∂', '∇', '∈', '∉', '∋', '∅', '∩', '∪', '⊂', '⊃', '⊆', '⊇',
    '⊕', '⊗', '⊥', '∠', '∧', '∨', '¬', '∀', '∃', '∄', 'ℕ', 'ℤ', 'ℚ', 'ℝ', 'ℂ',
  ],
  'Arrows': [
    '←', '↑', '→', '↓', '↔', '↕', '↖', '↗', '↘', '↙', '⇐', '⇑', '⇒', '⇓', '⇔',
    '⇕', '⟵', '⟶', '⟷', '⟸', '⟹', '⟺', '➜', '➝', '➞', '➡', '⬅', '⬆', '⬇', '↩',
  ],
  'Sanskrit / Devanagari': [
    'ॐ', '।', '॥', '॰', 'ऽ', '₹', '꣸', '꣹', '꣺', 'ꣻ',
    '॑', '॒', '᳡', '᳢', '᳣', '᳤', '᳥',
    'ꣳ', 'ꣴ', 'ꣵ', 'ꣶ', 'ꣷ',
  ],
  'Kannada': [
    'ಅ', 'ಆ', 'ಇ', 'ಈ', 'ಉ', 'ಊ', 'ಋ', 'ಎ', 'ಏ', 'ಐ', 'ಒ', 'ಓ', 'ಔ',
    'ಕ', 'ಖ', 'ಗ', 'ಘ', 'ಙ', 'ಚ', 'ಛ', 'ಜ', 'ಝ', 'ಞ',
    'ಟ', 'ಠ', 'ಡ', 'ಢ', 'ಣ', 'ತ', 'ಥ', 'ದ', 'ಧ', 'ನ',
    'ಪ', 'ಫ', 'ಬ', 'ಭ', 'ಮ', 'ಯ', 'ರ', 'ಲ', 'ವ', 'ಶ', 'ಷ', 'ಸ', 'ಹ', 'ಳ',
  ],
  'Emoji': [
    '😀', '😂', '😍', '🤔', '😎', '🙏', '👍', '👎', '❤️', '💡',
    '🔥', '⭐', '🎉', '🎵', '📌', '📎', '✉️', '🔔', '⚠️', '🚀',
  ],
};

export default function SymbolPickerPlugin({ isOpen, onClose }) {
  const [editor] = useLexicalComposerContext();
  const [activeCategory, setActiveCategory] = useState('Common');

  const insertSymbol = useCallback((char) => {
    editor.update(() => {
      const selection = $getSelection();
      if ($isRangeSelection(selection)) {
        selection.insertText(char);
      }
    });
  }, [editor]);

  if (!isOpen) return null;

  return (
    <div className="symbol-picker-overlay" onClick={onClose}>
      <div className="symbol-picker-dialog" onClick={(e) => e.stopPropagation()}>
        <div className="symbol-picker-header">
          <span className="symbol-picker-title">Insert Symbol</span>
          <button className="symbol-picker-close" onClick={onClose}>✕</button>
        </div>
        <div className="symbol-picker-tabs">
          {Object.keys(SYMBOL_CATEGORIES).map((cat) => (
            <button
              key={cat}
              className={`symbol-picker-tab ${activeCategory === cat ? 'active' : ''}`}
              onClick={() => setActiveCategory(cat)}
            >{cat}</button>
          ))}
        </div>
        <div className="symbol-picker-grid">
          {SYMBOL_CATEGORIES[activeCategory].map((ch, i) => (
            <button
              key={i}
              className="symbol-picker-char"
              onClick={() => insertSymbol(ch)}
              title={`U+${ch.codePointAt(0).toString(16).toUpperCase().padStart(4, '0')}`}
            >{ch}</button>
          ))}
        </div>
      </div>
    </div>
  );
}
