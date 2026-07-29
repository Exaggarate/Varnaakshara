import React, { useCallback, useState, useRef, useEffect } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import {
  $getSelection,
  $isRangeSelection,
  $createParagraphNode,
  FORMAT_TEXT_COMMAND,
  FORMAT_ELEMENT_COMMAND,
  UNDO_COMMAND,
  REDO_COMMAND,
  INDENT_CONTENT_COMMAND,
  OUTDENT_CONTENT_COMMAND,
} from 'lexical';
import {
  INSERT_ORDERED_LIST_COMMAND,
  INSERT_UNORDERED_LIST_COMMAND,
} from '@lexical/list';
import { INSERT_TABLE_COMMAND } from '@lexical/table';
import { TOGGLE_LINK_COMMAND } from '@lexical/link';
import { INSERT_HORIZONTAL_RULE_COMMAND } from '@lexical/react/LexicalHorizontalRuleNode';
import { $setBlocksType } from '@lexical/selection';
import { $createHeadingNode, $createQuoteNode } from '@lexical/rich-text';

import { INSERT_IMAGE_COMMAND } from '../nodes/ImageNode';
import { INSERT_PAGE_BREAK_COMMAND } from '../nodes/PageBreakNode';

const { ipcRenderer } = window.require ? window.require('electron') : { ipcRenderer: null };

const FONT_FAMILIES = [
  'Noto Sans Kannada', 'Noto Sans Devanagari', 'Noto Sans Telugu',
  'Noto Sans Tamil', 'Noto Sans Malayalam', 'Noto Sans Bengali',
  'Noto Sans Gujarati', 'Noto Sans Gurmukhi', 'Noto Sans Oriya',
  'Noto Serif Kannada', 'Noto Serif Devanagari', 'Noto Serif Telugu',
  'Noto Serif Tamil', 'Noto Serif', 'Noto Sans',
  'Arial', 'Calibri', 'Cambria', 'Georgia', 'Segoe UI',
  'Tahoma', 'Times New Roman', 'Trebuchet MS', 'Verdana',
  'Courier New', 'Consolas',
];

const FONT_SIZES = ['8','9','10','11','12','14','16','18','20','24','28','32','36','48','72'];

const LINE_SPACINGS = [
  { label: '1.0', value: '1.0' },
  { label: '1.15', value: '1.15' },
  { label: '1.5', value: '1.5' },
  { label: '2.0', value: '2.0' },
  { label: '2.5', value: '2.5' },
  { label: '3.0', value: '3.0' },
];

// ── Alignment SVG Icons ──────────────────────────────────────────────────────
const AlignLeftIcon = () => (
  <svg width="16" height="14" viewBox="0 0 16 14" fill="currentColor">
    <rect x="0" y="0" width="16" height="2" />
    <rect x="0" y="4" width="11" height="2" />
    <rect x="0" y="8" width="14" height="2" />
    <rect x="0" y="12" width="9" height="2" />
  </svg>
);
const AlignCenterIcon = () => (
  <svg width="16" height="14" viewBox="0 0 16 14" fill="currentColor">
    <rect x="0" y="0" width="16" height="2" />
    <rect x="2.5" y="4" width="11" height="2" />
    <rect x="1" y="8" width="14" height="2" />
    <rect x="3.5" y="12" width="9" height="2" />
  </svg>
);
const AlignRightIcon = () => (
  <svg width="16" height="14" viewBox="0 0 16 14" fill="currentColor">
    <rect x="0" y="0" width="16" height="2" />
    <rect x="5" y="4" width="11" height="2" />
    <rect x="2" y="8" width="14" height="2" />
    <rect x="7" y="12" width="9" height="2" />
  </svg>
);
const AlignJustifyIcon = () => (
  <svg width="16" height="14" viewBox="0 0 16 14" fill="currentColor">
    <rect x="0" y="0" width="16" height="2" />
    <rect x="0" y="4" width="16" height="2" />
    <rect x="0" y="8" width="16" height="2" />
    <rect x="0" y="12" width="16" height="2" />
  </svg>
);

// ── Style Gallery Data ───────────────────────────────────────────────────────
const STYLE_GALLERY = [
  { name: 'Normal', tag: 'paragraph', style: { fontSize: '12px' } },
  { name: 'No Spacing', tag: 'paragraph', style: { fontSize: '12px', lineHeight: '1.0' } },
  { name: 'Heading 1', tag: 'h1', style: { fontSize: '18px', fontWeight: 700 } },
  { name: 'Heading 2', tag: 'h2', style: { fontSize: '15px', fontWeight: 600 } },
  { name: 'Heading 3', tag: 'h3', style: { fontSize: '13px', fontWeight: 600 } },
  { name: 'Heading 4', tag: 'h4', style: { fontSize: '12px', fontWeight: 600, fontStyle: 'italic' } },
  { name: 'Title', tag: 'h1', style: { fontSize: '20px', fontWeight: 300, letterSpacing: '1px' } },
  { name: 'Subtitle', tag: 'h2', style: { fontSize: '14px', fontWeight: 400, color: '#666', fontStyle: 'italic' } },
  { name: 'Quote', tag: 'quote', style: { fontSize: '12px', fontStyle: 'italic', color: '#555', borderLeft: '3px solid #0078d4', paddingLeft: '8px' } },
];

const BLOCK_TYPES = [
  { label: 'Normal', value: 'paragraph' },
  { label: 'Heading 1', value: 'h1' },
  { label: 'Heading 2', value: 'h2' },
  { label: 'Heading 3', value: 'h3' },
  { label: 'Heading 4', value: 'h4' },
  { label: 'Quote', value: 'quote' },
  { label: 'Code', value: 'code' },
];

// ── Home Tab Ribbon ──────────────────────────────────────────────────────────
function HomeRibbon({ formatState, onFontChange, onSizeChange, onColorChange, onBgColorChange, onLineSpacingChange }) {
  const [editor] = useLexicalComposerContext();
  const [lineSpacingOpen, setLineSpacingOpen] = useState(false);
  const fmt = (f) => () => editor.dispatchCommand(FORMAT_TEXT_COMMAND, f);
  const align = (a) => () => editor.dispatchCommand(FORMAT_ELEMENT_COMMAND, a);

  // Clipboard actions
  const handleCut = useCallback(() => {
    document.execCommand('cut');
  }, []);
  const handleCopy = useCallback(() => {
    document.execCommand('copy');
  }, []);
  const handlePaste = useCallback(() => {
    navigator.clipboard.readText().then((text) => {
      editor.update(() => {
        const selection = $getSelection();
        if ($isRangeSelection(selection)) {
          selection.insertText(text);
        }
      });
    }).catch(() => {
      document.execCommand('paste');
    });
  }, [editor]);

  // Format Painter
  const [formatPainterFormat, setFormatPainterFormat] = useState(null);
  const handleFormatPainter = useCallback(() => {
    if (formatPainterFormat) {
      // Apply stored format
      editor.update(() => {
        const selection = $getSelection();
        if ($isRangeSelection(selection)) {
          const fmt = formatPainterFormat;
          if (fmt.bold) selection.formatText('bold');
          if (fmt.italic) selection.formatText('italic');
          if (fmt.underline) selection.formatText('underline');
          if (fmt.strikethrough) selection.formatText('strikethrough');
          if (fmt.superscript) selection.formatText('superscript');
          if (fmt.subscript) selection.formatText('subscript');
        }
      });
      setFormatPainterFormat(null);
    } else {
      // Capture current format
      editor.getEditorState().read(() => {
        const selection = $getSelection();
        if ($isRangeSelection(selection)) {
          setFormatPainterFormat({
            bold: selection.hasFormat('bold'),
            italic: selection.hasFormat('italic'),
            underline: selection.hasFormat('underline'),
            strikethrough: selection.hasFormat('strikethrough'),
            superscript: selection.hasFormat('superscript'),
            subscript: selection.hasFormat('subscript'),
          });
        }
      });
    }
  }, [editor, formatPainterFormat]);

  // Clear Formatting
  const handleClearFormat = useCallback(() => {
    editor.update(() => {
      const selection = $getSelection();
      if ($isRangeSelection(selection)) {
        const formats = ['bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript', 'code'];
        formats.forEach((f) => {
          if (selection.hasFormat(f)) {
            selection.formatText(f);
          }
        });
      }
    });
  }, [editor]);

  // Block type change
  const handleBlockTypeChange = useCallback((e) => {
    const val = e.target.value;
    editor.update(() => {
      const selection = $getSelection();
      if (!$isRangeSelection(selection)) return;
      if (val === 'paragraph') {
        $setBlocksType(selection, () => $createParagraphNode());
      } else if (val === 'quote') {
        $setBlocksType(selection, () => $createQuoteNode());
      } else if (val.startsWith('h')) {
        $setBlocksType(selection, () => $createHeadingNode(val));
      }
    });
  }, [editor]);

  // Style Gallery click
  const handleStyleClick = useCallback((item) => {
    editor.update(() => {
      const selection = $getSelection();
      if (!$isRangeSelection(selection)) return;
      if (item.tag === 'paragraph') {
        $setBlocksType(selection, () => $createParagraphNode());
      } else if (item.tag === 'quote') {
        $setBlocksType(selection, () => $createQuoteNode());
      } else if (item.tag.startsWith('h')) {
        $setBlocksType(selection, () => $createHeadingNode(item.tag));
      }
    });
  }, [editor]);

  return (
    <div className="ribbon-strip">
      {/* Clipboard */}
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <div style={{ display: 'flex', gap: 2 }}>
              <button className="ribbon-btn ribbon-btn-inline" onClick={handleCut} title="Cut (Ctrl+X)">Cut</button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={handleCopy} title="Copy (Ctrl+C)">Copy</button>
            </div>
            <div style={{ display: 'flex', gap: 2 }}>
              <button className="ribbon-btn ribbon-btn-inline" onClick={handlePaste} title="Paste (Ctrl+V)">Paste</button>
              <button
                className={`ribbon-btn ribbon-btn-inline ${formatPainterFormat ? 'active' : ''}`}
                onClick={handleFormatPainter}
                title="Format Painter"
              >Painter</button>
            </div>
          </div>
        </div>
        <span className="ribbon-section-label">Clipboard</span>
      </div>

      {/* Font */}
      <div className="ribbon-section">
        <div className="ribbon-section-content" style={{ flexDirection: 'column', alignItems: 'stretch', gap: 3 }}>
          <div style={{ display: 'flex', gap: 4 }}>
            <select className="ribbon-select ribbon-select-font" value={formatState.fontFamily} onChange={onFontChange}>
              {FONT_FAMILIES.map(f => <option key={f} value={f}>{f}</option>)}
            </select>
            <select className="ribbon-select ribbon-select-size" value={formatState.fontSize} onChange={onSizeChange}>
              {FONT_SIZES.map(s => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div style={{ display: 'flex', gap: 2 }}>
            <button className={`ribbon-btn ribbon-btn-inline ${formatState.isBold ? 'active' : ''}`} onClick={fmt('bold')} title="Bold">
              <strong>B</strong>
            </button>
            <button className={`ribbon-btn ribbon-btn-inline ${formatState.isItalic ? 'active' : ''}`} onClick={fmt('italic')} title="Italic">
              <em>I</em>
            </button>
            <button className={`ribbon-btn ribbon-btn-inline ${formatState.isUnderline ? 'active' : ''}`} onClick={fmt('underline')} title="Underline">
              <span style={{ textDecoration: 'underline' }}>U</span>
            </button>
            <button className={`ribbon-btn ribbon-btn-inline ${formatState.isStrikethrough ? 'active' : ''}`} onClick={fmt('strikethrough')} title="Strikethrough">
              <span style={{ textDecoration: 'line-through' }}>S</span>
            </button>
            <button className={`ribbon-btn ribbon-btn-inline ${formatState.isSuperscript ? 'active' : ''}`} onClick={fmt('superscript')} title="Superscript">
              X<sup style={{ fontSize: '8px' }}>²</sup>
            </button>
            <button className={`ribbon-btn ribbon-btn-inline ${formatState.isSubscript ? 'active' : ''}`} onClick={fmt('subscript')} title="Subscript">
              X<sub style={{ fontSize: '8px' }}>₂</sub>
            </button>
            <button className="ribbon-btn ribbon-btn-inline" onClick={handleClearFormat} title="Clear Formatting">
              <span style={{ fontSize: 11 }}>Aa̶</span>
            </button>
            <div className="ribbon-btn ribbon-btn-inline ribbon-color-btn" title="Text Color">
              <span style={{ fontWeight: 700 }}>A</span>
              <div className="ribbon-color-indicator" style={{ backgroundColor: formatState.textColor }} />
              <input type="color" value={formatState.textColor} onChange={onColorChange} />
            </div>
            <div className="ribbon-btn ribbon-btn-inline ribbon-color-btn" title="Highlight">
              <span style={{ backgroundColor: formatState.bgColor, padding: '0 2px', fontSize: 11 }}>ab</span>
              <div className="ribbon-color-indicator" style={{ backgroundColor: formatState.bgColor }} />
              <input type="color" value={formatState.bgColor} onChange={onBgColorChange} />
            </div>
          </div>
        </div>
        <span className="ribbon-section-label">Font</span>
      </div>

      {/* Paragraph */}
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <div style={{ display: 'flex', gap: 2 }}>
              <button className="ribbon-btn ribbon-btn-inline" onClick={align('left')} title="Align Left"><AlignLeftIcon /></button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={align('center')} title="Center"><AlignCenterIcon /></button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={align('right')} title="Align Right"><AlignRightIcon /></button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={align('justify')} title="Justify"><AlignJustifyIcon /></button>
            </div>
            <div style={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              <button className="ribbon-btn ribbon-btn-inline" onClick={() => editor.dispatchCommand(INSERT_UNORDERED_LIST_COMMAND)} title="Bullet List">* List</button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={() => editor.dispatchCommand(INSERT_ORDERED_LIST_COMMAND)} title="Numbered List">1. List</button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={() => editor.dispatchCommand(OUTDENT_CONTENT_COMMAND)} title="Decrease Indent">&lt;&lt;</button>
              <button className="ribbon-btn ribbon-btn-inline" onClick={() => editor.dispatchCommand(INDENT_CONTENT_COMMAND)} title="Increase Indent">&gt;&gt;</button>
              <div style={{ position: 'relative' }}>
                <button className="ribbon-btn ribbon-btn-inline" onClick={() => setLineSpacingOpen(!lineSpacingOpen)} title="Line Spacing">LS</button>
                {lineSpacingOpen && (
                  <div className="ribbon-dropdown">
                    {LINE_SPACINGS.map((ls) => (
                      <button
                        key={ls.value}
                        className="ribbon-dropdown-item"
                        onClick={() => { onLineSpacingChange(ls.value); setLineSpacingOpen(false); }}
                      >{ls.label}</button>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
        <span className="ribbon-section-label">Paragraph</span>
      </div>

      {/* Block Type */}
      <div className="ribbon-section">
        <div className="ribbon-section-content" style={{ flexDirection: 'column', gap: 4 }}>
          <select className="ribbon-select" value={formatState.blockType || 'paragraph'} onChange={handleBlockTypeChange} style={{ width: 110 }}>
            {BLOCK_TYPES.map(bt => <option key={bt.value} value={bt.value}>{bt.label}</option>)}
          </select>
        </div>
        <span className="ribbon-section-label">Styles</span>
      </div>

      {/* Styles Gallery */}
      <div className="ribbon-section ribbon-section-gallery">
        <div className="ribbon-section-content styles-gallery-scroll">
          {STYLE_GALLERY.map((item) => (
            <button
              key={item.name}
              className={`style-gallery-card ${formatState.blockType === item.tag ? 'active' : ''}`}
              onClick={() => handleStyleClick(item)}
              title={item.name}
            >
              <span style={item.style}>{item.name}</span>
            </button>
          ))}
        </div>
        <span className="ribbon-section-label">Styles Gallery</span>
      </div>
    </div>
  );
}

// ── Insert Tab Ribbon ────────────────────────────────────────────────────────
function InsertRibbon({ onTableGridOpen, onSymbolPickerOpen, onImageInsert }) {
  const [editor] = useLexicalComposerContext();

  const handleImageInsert = useCallback(() => {
    if (onImageInsert) onImageInsert();
  }, [onImageInsert]);

  const handleHR = useCallback(() => {
    editor.dispatchCommand(INSERT_HORIZONTAL_RULE_COMMAND, undefined);
  }, [editor]);

  const handlePageBreak = useCallback(() => {
    editor.dispatchCommand(INSERT_PAGE_BREAK_COMMAND, undefined);
  }, [editor]);

  return (
    <div className="ribbon-strip">
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn" onClick={onTableGridOpen} title="Insert Table">
            <span className="ribbon-btn-icon">[T]</span>
            <span className="ribbon-btn-label">Table</span>
          </button>
          <button className="ribbon-btn" onClick={handleImageInsert} title="Insert Image">
            <span className="ribbon-btn-icon">[I]</span>
            <span className="ribbon-btn-label">Image</span>
          </button>
          <button className="ribbon-btn" onClick={() => { const url = prompt('Enter URL:'); if (url) editor.dispatchCommand(TOGGLE_LINK_COMMAND, url); }} title="Insert Link">
            <span className="ribbon-btn-icon">[L]</span>
            <span className="ribbon-btn-label">Link</span>
          </button>
        </div>
        <span className="ribbon-section-label">Elements</span>
      </div>
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn" onClick={handleHR} title="Insert Horizontal Rule">
            <span className="ribbon-btn-icon">HR</span>
            <span className="ribbon-btn-label">Horiz Rule</span>
          </button>
          <button className="ribbon-btn" onClick={handlePageBreak} title="Insert Page Break">
            <span className="ribbon-btn-icon">PB</span>
            <span className="ribbon-btn-label">Page Break</span>
          </button>
        </div>
        <span className="ribbon-section-label">Breaks</span>
      </div>
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn" onClick={onSymbolPickerOpen} title="Insert Special Character">
            <span className="ribbon-btn-icon">Sym</span>
            <span className="ribbon-btn-label">Special Char</span>
          </button>
        </div>
        <span className="ribbon-section-label">Symbols</span>
      </div>
    </div>
  );
}

// ── Layout Tab Ribbon ────────────────────────────────────────────────────────
const PAGE_SIZES = [
  { label: 'A4 (210×297mm)', width: 794, height: 1123 },
  { label: 'US Letter (8.5×11in)', width: 816, height: 1056 },
  { label: 'Legal (8.5×14in)', width: 816, height: 1344 },
  { label: 'A5 (148×210mm)', width: 559, height: 794 },
  { label: 'B5 (176×250mm)', width: 665, height: 945 },
];

const MARGIN_PRESETS = [
  { label: 'Normal (1 in)', value: 96 },
  { label: 'Narrow (0.5 in)', value: 48 },
  { label: 'Wide (1.25 in)', value: 120 },
  { label: 'Moderate (0.75 in)', value: 72 },
];

const COLUMN_OPTIONS = [1, 2, 3];

const PARA_SPACINGS = ['0', '6', '12', '24'];

function LayoutRibbon({ pageSetup, onPageSetupChange }) {
  const [pageSizeOpen, setPageSizeOpen] = useState(false);
  const [marginOpen, setMarginOpen] = useState(false);
  const [columnsOpen, setColumnsOpen] = useState(false);
  const [spacingOpen, setSpacingOpen] = useState(false);

  return (
    <div className="ribbon-strip">
      {/* Orientation */}
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button
            className={`ribbon-btn ${pageSetup.orientation === 'portrait' ? 'active' : ''}`}
            onClick={() => onPageSetupChange({ orientation: 'portrait' })}
            title="Portrait"
          >
            <span className="ribbon-btn-icon">||</span>
            <span className="ribbon-btn-label">Portrait</span>
          </button>
          <button
            className={`ribbon-btn ${pageSetup.orientation === 'landscape' ? 'active' : ''}`}
            onClick={() => onPageSetupChange({ orientation: 'landscape' })}
            title="Landscape"
          >
            <span className="ribbon-btn-icon">=</span>
            <span className="ribbon-btn-label">Landscape</span>
          </button>
        </div>
        <span className="ribbon-section-label">Orientation</span>
      </div>

      {/* Page Size */}
      <div className="ribbon-section">
        <div className="ribbon-section-content" style={{ position: 'relative' }}>
          <button className="ribbon-btn" onClick={() => setPageSizeOpen(!pageSizeOpen)} title="Page Size">
            <span className="ribbon-btn-icon" style={{ fontSize: 13 }}>
              {PAGE_SIZES.find(p => p.width === pageSetup.pageWidth && p.height === pageSetup.pageHeight)?.label.split(' ')[0] || 'A4'}
            </span>
            <span className="ribbon-btn-label">Page Size</span>
          </button>
          {pageSizeOpen && (
            <div className="ribbon-dropdown" style={{ left: 0 }}>
              {PAGE_SIZES.map((ps) => (
                <button
                  key={ps.label}
                  className={`ribbon-dropdown-item ${pageSetup.pageWidth === ps.width && pageSetup.pageHeight === ps.height ? 'active' : ''}`}
                  onClick={() => { onPageSetupChange({ pageWidth: ps.width, pageHeight: ps.height }); setPageSizeOpen(false); }}
                >{ps.label}</button>
              ))}
            </div>
          )}
        </div>
        <span className="ribbon-section-label">Size</span>
      </div>

      {/* Margins */}
      <div className="ribbon-section">
        <div className="ribbon-section-content" style={{ position: 'relative' }}>
          <button className="ribbon-btn" onClick={() => setMarginOpen(!marginOpen)} title="Margins">
            <span className="ribbon-btn-icon">[M]</span>
            <span className="ribbon-btn-label">Margins</span>
          </button>
          {marginOpen && (
            <div className="ribbon-dropdown" style={{ left: 0 }}>
              {MARGIN_PRESETS.map((mp) => (
                <button
                  key={mp.label}
                  className={`ribbon-dropdown-item ${pageSetup.margin === mp.value ? 'active' : ''}`}
                  onClick={() => { onPageSetupChange({ margin: mp.value }); setMarginOpen(false); }}
                >{mp.label}</button>
              ))}
            </div>
          )}
        </div>
        <span className="ribbon-section-label">Margins</span>
      </div>

      {/* Columns */}
      <div className="ribbon-section">
        <div className="ribbon-section-content" style={{ position: 'relative' }}>
          <button className="ribbon-btn" onClick={() => setColumnsOpen(!columnsOpen)} title="Columns">
            <span className="ribbon-btn-icon">Col</span>
            <span className="ribbon-btn-label">Columns</span>
          </button>
          {columnsOpen && (
            <div className="ribbon-dropdown" style={{ left: 0 }}>
              {COLUMN_OPTIONS.map((c) => (
                <button
                  key={c}
                  className={`ribbon-dropdown-item ${pageSetup.columns === c ? 'active' : ''}`}
                  onClick={() => { onPageSetupChange({ columns: c }); setColumnsOpen(false); }}
                >{c} Column{c > 1 ? 's' : ''}</button>
              ))}
            </div>
          )}
        </div>
        <span className="ribbon-section-label">Columns</span>
      </div>

      {/* Paragraph Spacing */}
      <div className="ribbon-section">
        <div className="ribbon-section-content" style={{ position: 'relative' }}>
          <button className="ribbon-btn" onClick={() => setSpacingOpen(!spacingOpen)} title="Paragraph Spacing">
            <span className="ribbon-btn-icon">Sp</span>
            <span className="ribbon-btn-label">Spacing</span>
          </button>
          {spacingOpen && (
            <div className="ribbon-dropdown" style={{ left: 0 }}>
              <div className="ribbon-dropdown-label">Before Paragraph</div>
              {PARA_SPACINGS.map((s) => (
                <button
                  key={'b' + s}
                  className={`ribbon-dropdown-item ${String(pageSetup.spacingBefore) === s ? 'active' : ''}`}
                  onClick={() => { onPageSetupChange({ spacingBefore: Number(s) }); }}
                >{s}pt before</button>
              ))}
              <div className="ribbon-dropdown-label" style={{ marginTop: 6 }}>After Paragraph</div>
              {PARA_SPACINGS.map((s) => (
                <button
                  key={'a' + s}
                  className={`ribbon-dropdown-item ${String(pageSetup.spacingAfter) === s ? 'active' : ''}`}
                  onClick={() => { onPageSetupChange({ spacingAfter: Number(s) }); setSpacingOpen(false); }}
                >{s}pt after</button>
              ))}
            </div>
          )}
        </div>
        <span className="ribbon-section-label">Spacing</span>
      </div>
    </div>
  );
}

// ── Review Tab Ribbon ────────────────────────────────────────────────────────
function ReviewRibbon({ onFindReplace, onWordCount, onSpellCheckToggle, spellCheck }) {
  return (
    <div className="ribbon-strip">
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className={`ribbon-btn ${spellCheck ? 'active' : ''}`} onClick={onSpellCheckToggle} title="Toggle Spell Check">
            <span className="ribbon-btn-icon">ABC</span>
            <span className="ribbon-btn-label">Spell Check</span>
          </button>
          <button className="ribbon-btn" onClick={onWordCount} title="Word Count">
            <span className="ribbon-btn-icon">#W</span>
            <span className="ribbon-btn-label">Word Count</span>
          </button>
        </div>
        <span className="ribbon-section-label">Proofing</span>
      </div>
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn" onClick={onFindReplace} title="Find & Replace (Ctrl+F)">
            <span className="ribbon-btn-icon">Find</span>
            <span className="ribbon-btn-label">Find & Replace</span>
          </button>
        </div>
        <span className="ribbon-section-label">Editing</span>
      </div>
    </div>
  );
}

// ── Tools Tab Ribbon ─────────────────────────────────────────────────────────
function ToolsRibbon({ onOpenPanel }) {
  return (
    <div className="ribbon-strip">
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn" onClick={() => onOpenPanel && onOpenPanel('transliterate')}>
            <span className="ribbon-btn-icon">Trl</span>
            <span className="ribbon-btn-label">Transliterate</span>
          </button>
          <button className="ribbon-btn" onClick={() => onOpenPanel && onOpenPanel('convert-script')}>
            <span className="ribbon-btn-icon">Cvt</span>
            <span className="ribbon-btn-label">Convert Script</span>
          </button>
        </div>
        <span className="ribbon-section-label">Transliteration</span>
      </div>
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn" onClick={() => onOpenPanel && onOpenPanel('unicode-ansi')}>
            <span className="ribbon-btn-icon">U/A</span>
            <span className="ribbon-btn-label">Unicode-ANSI</span>
          </button>
          <button className="ribbon-btn" onClick={() => onOpenPanel && onOpenPanel('panchama-varga')}>
            <span className="ribbon-btn-icon">PV</span>
            <span className="ribbon-btn-label">Panchama Varga</span>
          </button>
        </div>
        <span className="ribbon-section-label">Conversion</span>
      </div>
      <div className="ribbon-section">
        <div className="ribbon-section-content">
          <button className="ribbon-btn">
            <span className="ribbon-btn-icon">Cfg</span>
            <span className="ribbon-btn-label">Settings</span>
          </button>
        </div>
        <span className="ribbon-section-label">Options</span>
      </div>
    </div>
  );
}

// ── Main Ribbon Export ───────────────────────────────────────────────────────
export default function Ribbon({
  activeTab, formatState, onFontChange, onSizeChange, onColorChange, onBgColorChange,
  onOpenPanel, pageSetup, onPageSetupChange,
  onTableGridOpen, onSymbolPickerOpen, onImageInsert,
  onFindReplace, onWordCount, onSpellCheckToggle, spellCheck,
  onLineSpacingChange,
}) {
  switch (activeTab) {
    case 'Insert':
      return <InsertRibbon onTableGridOpen={onTableGridOpen} onSymbolPickerOpen={onSymbolPickerOpen} onImageInsert={onImageInsert} />;
    case 'Layout':
      return <LayoutRibbon pageSetup={pageSetup} onPageSetupChange={onPageSetupChange} />;
    case 'Review':
      return <ReviewRibbon onFindReplace={onFindReplace} onWordCount={onWordCount} onSpellCheckToggle={onSpellCheckToggle} spellCheck={spellCheck} />;
    case 'Tools':
      return <ToolsRibbon onOpenPanel={onOpenPanel} />;
    case 'Home':
    default:
      return (
        <HomeRibbon
          formatState={formatState}
          onFontChange={onFontChange}
          onSizeChange={onSizeChange}
          onColorChange={onColorChange}
          onBgColorChange={onBgColorChange}
          onLineSpacingChange={onLineSpacingChange}
        />
      );
  }
}
