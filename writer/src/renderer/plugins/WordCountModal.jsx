/**
 * WordCountModal — Detailed word count statistics modal.
 */
import React, { useMemo } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';

export default function WordCountModal({ isOpen, onClose }) {
  const [editor] = useLexicalComposerContext();

  const stats = useMemo(() => {
    if (!isOpen) return null;
    const root = editor.getRootElement();
    const text = root ? root.textContent || '' : '';
    const trimmed = text.trim();
    const words = trimmed ? trimmed.split(/\s+/).length : 0;
    const charsWithSpaces = text.length;
    const charsNoSpaces = text.replace(/\s/g, '').length;
    const paragraphs = trimmed ? trimmed.split(/\n\s*\n/).length : 0;
    const lines = trimmed ? trimmed.split(/\n/).length : 0;
    const pages = Math.max(1, Math.ceil(words / 250));
    return { words, charsWithSpaces, charsNoSpaces, paragraphs, lines, pages };
  }, [isOpen, editor]);

  if (!isOpen || !stats) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-dialog modal-sm" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <span>Word Count</span>
          <button className="modal-close" onClick={onClose}>✕</button>
        </div>
        <div className="modal-body">
          <table className="stats-table">
            <tbody>
              <tr><td>Pages</td><td>{stats.pages}</td></tr>
              <tr><td>Words</td><td>{stats.words.toLocaleString()}</td></tr>
              <tr><td>Characters (with spaces)</td><td>{stats.charsWithSpaces.toLocaleString()}</td></tr>
              <tr><td>Characters (no spaces)</td><td>{stats.charsNoSpaces.toLocaleString()}</td></tr>
              <tr><td>Paragraphs</td><td>{stats.paragraphs.toLocaleString()}</td></tr>
              <tr><td>Lines</td><td>{stats.lines.toLocaleString()}</td></tr>
            </tbody>
          </table>
        </div>
        <div className="modal-footer">
          <button className="modal-btn" onClick={onClose}>Close</button>
        </div>
      </div>
    </div>
  );
}
