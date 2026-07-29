import React from 'react';

export default function StatusBar({
  pageCount = 1,
  wordCount = 0,
  charCount = 0,
  language = 'Kannada',
  inputMode = 'Phonetic',
  zoom = 1.0,
}) {
  const zoomPercent = Math.round(zoom * 100);

  return (
    <div className="status-bar" role="status" aria-live="polite">
      <div className="status-bar-left">
        <span className="status-bar-item">
          Page {pageCount}
        </span>
        <span className="status-bar-separator" />
        <span className="status-bar-item">
          {wordCount} {wordCount === 1 ? 'word' : 'words'}
        </span>
        <span className="status-bar-separator" />
        <span className="status-bar-item">
          {charCount.toLocaleString()} chars
        </span>
      </div>
      <div className="status-bar-right">
        <div className="status-bar-lang" title="Active language">
          <span className="lang-dot" />
          <span style={{ fontSize: 11, color: '#fff' }}>{language}</span>
        </div>
        <span className="status-bar-separator" />
        <span className="status-bar-item" title="Input mode">
          {inputMode}
        </span>
        <span className="status-bar-separator" />
        <div className="zoom-controls">
          <span style={{ fontSize: 11, color: '#fff', minWidth: 32, textAlign: 'right' }}>{zoomPercent}%</span>
          <input
            type="range"
            min="50"
            max="200"
            value={zoomPercent}
            readOnly
            title={`Zoom: ${zoomPercent}%`}
          />
        </div>
      </div>
    </div>
  );
}
