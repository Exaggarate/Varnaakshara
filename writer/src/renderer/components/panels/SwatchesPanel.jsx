/**
 * SwatchesPanel — InDesign-style color swatches panel.
 * Click to set text color, Shift+Click for background/highlight color.
 * Custom swatches persist in localStorage.
 */
import React, { useState, useCallback, useRef } from 'react';

/* ── Default Swatches ─────────────────────────────────────────────────────── */
const BUILT_IN_SWATCHES = [
  { name: 'Black',        hex: '#000000', builtin: true },
  { name: 'White',        hex: '#FFFFFF', builtin: true },
  { name: 'Registration', hex: '#100000', builtin: true, icon: '⊕' },
  { name: 'Paper',        hex: '#FAFAFA', builtin: true, icon: '□' },
  { name: 'Red',          hex: '#FF0000', builtin: true },
  { name: 'Dark Red',     hex: '#8B0000', builtin: true },
  { name: 'Blue',         hex: '#0000FF', builtin: true },
  { name: 'Dark Blue',    hex: '#00008B', builtin: true },
  { name: 'Green',        hex: '#008000', builtin: true },
  { name: 'Dark Green',   hex: '#006400', builtin: true },
  { name: 'Yellow',       hex: '#FFFF00', builtin: true },
  { name: 'Orange',       hex: '#FF8C00', builtin: true },
  { name: 'Purple',       hex: '#800080', builtin: true },
  { name: 'Cyan',         hex: '#00FFFF', builtin: true },
  { name: 'Magenta',      hex: '#FF00FF', builtin: true },
  { name: 'Gray 80%',     hex: '#333333', builtin: true },
  { name: 'Gray 60%',     hex: '#666666', builtin: true },
  { name: 'Gray 40%',     hex: '#999999', builtin: true },
  { name: 'Gray 20%',     hex: '#CCCCCC', builtin: true },
  /* Indian theme */
  { name: 'Saffron',      hex: '#FF9933', builtin: true },
  { name: 'India White',  hex: '#FFFFFF', builtin: true },
  { name: 'India Green',  hex: '#138808', builtin: true },
  { name: 'Navy Blue',    hex: '#000080', builtin: true },
  { name: 'Ashoka Blue',  hex: '#06038D', builtin: true },
];

const CUSTOM_SWATCHES_KEY = 'varnaakshara-custom-swatches';

function loadCustomSwatches() {
  try {
    return JSON.parse(localStorage.getItem(CUSTOM_SWATCHES_KEY) || '[]');
  } catch { return []; }
}

/* ── Component ────────────────────────────────────────────────────────────── */
export default function SwatchesPanel() {
  const [viewMode, setViewMode] = useState('small'); // 'small' | 'large'
  const [customSwatches, setCustomSwatches] = useState(loadCustomSwatches);
  const colorInputRef = useRef(null);
  const [newColorName, setNewColorName] = useState('');

  const allSwatches = [...BUILT_IN_SWATCHES, ...customSwatches];

  /* Apply color — Click for text, Shift+Click for background */
  const handleSwatchClick = useCallback((hex, e) => {
    const target = e.shiftKey ? 'background' : 'text';
    window.dispatchEvent(
      new CustomEvent('varnaakshara-apply-color', {
        detail: { color: hex, target },
      }),
    );
  }, []);

  /* Add custom swatch */
  const handleAddSwatch = useCallback(() => {
    if (!colorInputRef.current) return;
    const hex = colorInputRef.current.value;
    const name = newColorName.trim() || hex;
    const newSwatch = { name, hex, builtin: false };
    const updated = [...customSwatches, newSwatch];
    setCustomSwatches(updated);
    setNewColorName('');
    try { localStorage.setItem(CUSTOM_SWATCHES_KEY, JSON.stringify(updated)); } catch {}
  }, [customSwatches, newColorName]);

  /* Remove custom swatch */
  const handleRemoveSwatch = useCallback(
    (index) => {
      const updated = customSwatches.filter((_, i) => i !== index);
      setCustomSwatches(updated);
      try { localStorage.setItem(CUSTOM_SWATCHES_KEY, JSON.stringify(updated)); } catch {}
    },
    [customSwatches],
  );

  const cellSize = viewMode === 'large' ? 36 : 20;

  return (
    <div className="panel-swatches">
      {/* View toggle */}
      <div className="panel-row" style={{ justifyContent: 'space-between' }}>
        <span className="panel-label" style={{ fontSize: 10 }}>
          Click = text color · Shift+Click = highlight
        </span>
        <div style={{ display: 'flex', gap: 2 }}>
          <button
            className={`panel-btn ${viewMode === 'small' ? 'active-view' : ''}`}
            onClick={() => setViewMode('small')}
            title="Small swatches"
            style={{ padding: '2px 6px', fontSize: 10 }}
          >
            ▪▪
          </button>
          <button
            className={`panel-btn ${viewMode === 'large' ? 'active-view' : ''}`}
            onClick={() => setViewMode('large')}
            title="Large swatches"
            style={{ padding: '2px 6px', fontSize: 10 }}
          >
            ■
          </button>
        </div>
      </div>

      {/* Swatch grid */}
      <div className="swatch-grid" style={{ gridTemplateColumns: `repeat(auto-fill, minmax(${cellSize}px, 1fr))` }}>
        {allSwatches.map((swatch, i) => (
          <div
            key={`${swatch.name}-${i}`}
            className="swatch-cell"
            onClick={(e) => handleSwatchClick(swatch.hex, e)}
            onContextMenu={(e) => {
              e.preventDefault();
              if (!swatch.builtin) {
                const customIdx = i - BUILT_IN_SWATCHES.length;
                if (customIdx >= 0) handleRemoveSwatch(customIdx);
              }
            }}
            title={`${swatch.name}\n${swatch.hex}${!swatch.builtin ? '\nRight-click to remove' : ''}`}
            style={{
              width: cellSize,
              height: cellSize,
              background: swatch.hex,
              border: swatch.hex.toUpperCase() === '#FFFFFF' || swatch.hex.toUpperCase() === '#FAFAFA'
                ? '1px solid var(--panel-input-border)'
                : '1px solid transparent',
            }}
          >
            {swatch.icon && (
              <span style={{ fontSize: cellSize * 0.4, color: '#fff', mixBlendMode: 'difference' }}>
                {swatch.icon}
              </span>
            )}
          </div>
        ))}
      </div>

      {/* Add custom swatch */}
      <div className="panel-swatches-add">
        <div className="panel-row" style={{ gap: 4 }}>
          <input
            className="panel-input"
            type="text"
            placeholder="Name"
            value={newColorName}
            onChange={(e) => setNewColorName(e.target.value)}
            style={{ flex: 1, fontSize: 10, padding: '3px 6px' }}
          />
          <input
            ref={colorInputRef}
            type="color"
            defaultValue="#FF6600"
            style={{ width: 28, height: 24, padding: 0, border: 'none', cursor: 'pointer', background: 'transparent' }}
          />
          <button
            className="panel-btn"
            onClick={handleAddSwatch}
            style={{ padding: '3px 8px', fontSize: 10 }}
          >
            + Add
          </button>
        </div>
      </div>

      {/* Custom swatches count */}
      {customSwatches.length > 0 && (
        <div style={{ padding: '4px 0', fontSize: 9, color: 'var(--panel-text)', opacity: 0.6 }}>
          {customSwatches.length} custom swatch{customSwatches.length !== 1 ? 'es' : ''}
        </div>
      )}
    </div>
  );
}
