/**
 * TableGridPlugin — A hover grid picker for table insertion (like Word).
 */
import React, { useCallback, useState } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { INSERT_TABLE_COMMAND } from '@lexical/table';

const MAX_ROWS = 8;
const MAX_COLS = 8;

export default function TableGridPlugin({ isOpen, onClose }) {
  const [editor] = useLexicalComposerContext();
  const [hoverRow, setHoverRow] = useState(0);
  const [hoverCol, setHoverCol] = useState(0);

  const handleInsert = useCallback((r, c) => {
    editor.dispatchCommand(INSERT_TABLE_COMMAND, { rows: String(r), columns: String(c) });
    onClose();
  }, [editor, onClose]);

  if (!isOpen) return null;

  return (
    <div className="table-grid-overlay" onClick={onClose}>
      <div className="table-grid-popup" onClick={(e) => e.stopPropagation()}>
        <div className="table-grid-label">{hoverRow > 0 ? `${hoverRow} × ${hoverCol} Table` : 'Insert Table'}</div>
        <div className="table-grid">
          {Array.from({ length: MAX_ROWS }, (_, r) => (
            <div key={r} className="table-grid-row">
              {Array.from({ length: MAX_COLS }, (_, c) => (
                <div
                  key={c}
                  className={`table-grid-cell ${r < hoverRow && c < hoverCol ? 'highlighted' : ''}`}
                  onMouseEnter={() => { setHoverRow(r + 1); setHoverCol(c + 1); }}
                  onClick={() => handleInsert(r + 1, c + 1)}
                />
              ))}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
