import React from 'react';

export default function TitleBar({ filename = 'Untitled', dirty = false }) {
  const title = `${dirty ? '● ' : ''}${filename} — Varnaakshara Writer`;

  return (
    <div className="title-bar">
      <div className="title-bar-icon">✦</div>
      <div className="title-bar-text">{title}</div>
      <div className="title-bar-controls">
        <button title="Minimize">─</button>
        <button title="Maximize">□</button>
        <button className="close" title="Close">✕</button>
      </div>
    </div>
  );
}
