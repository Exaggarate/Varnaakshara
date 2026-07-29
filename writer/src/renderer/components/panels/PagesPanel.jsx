/**
 * PagesPanel — InDesign-style page thumbnails panel.
 * Estimates pages from word count (≈250 words / page) and shows
 * clickable thumbnails in a 2-column grid.
 */
import React, { useState, useEffect, useCallback } from 'react';

export default function PagesPanel() {
  const [counts, setCounts] = useState({ words: 0, chars: 0, pages: 1 });
  const [currentPage, setCurrentPage] = useState(1);

  /* Listen for counts broadcast from WordCountPlugin */
  useEffect(() => {
    const handler = (e) => {
      if (e.detail) setCounts(e.detail);
    };
    window.addEventListener('varnaakshara-counts', handler);
    return () => window.removeEventListener('varnaakshara-counts', handler);
  }, []);

  const totalPages = Math.max(1, counts.pages || 1);

  const handlePageClick = useCallback(
    (page) => {
      setCurrentPage(page);
      window.dispatchEvent(
        new CustomEvent('varnaakshara-scroll-to-page', { detail: { page } }),
      );
    },
    [],
  );

  /* Generate thumbnail "lines" pattern — we render tiny bars to simulate text */
  const renderPageLines = (page) => {
    const lineCount = page < totalPages ? 14 : Math.max(3, Math.ceil(14 * ((counts.words % 250) / 250)) || 14);
    const lines = [];
    for (let i = 0; i < lineCount; i++) {
      const width = i === 0 ? '55%' : i === lineCount - 1 ? '40%' : `${65 + Math.sin(i * 7) * 20}%`;
      lines.push(
        <div
          key={i}
          style={{
            height: 2,
            marginBottom: 2,
            background: 'rgba(0,0,0,0.15)',
            width,
            borderRadius: 1,
          }}
        />,
      );
    }
    return lines;
  };

  return (
    <div className="panel-pages">
      {/* Header info */}
      <div className="panel-pages-info">
        <span className="panel-label" style={{ fontSize: 10 }}>
          {totalPages} {totalPages === 1 ? 'Page' : 'Pages'} · {counts.words} Words
        </span>
      </div>

      {/* Thumbnail grid */}
      <div className="panel-pages-grid">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <div
            key={page}
            className={`panel-page-thumb ${currentPage === page ? 'active' : ''}`}
            onClick={() => handlePageClick(page)}
            title={`Page ${page}`}
          >
            <div className="panel-page-thumb-inner">
              {renderPageLines(page)}
            </div>
            <span className="panel-page-thumb-label">{page}</span>
          </div>
        ))}
      </div>

      {/* Footer */}
      <div className="panel-pages-footer">
        <button
          className="panel-btn"
          style={{ flex: 1, opacity: 0.5, cursor: 'default' }}
          disabled
          title="Page management coming soon"
        >
          + Add Page
        </button>
      </div>
    </div>
  );
}
