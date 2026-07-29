import React, { useCallback, useEffect, useState } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import {
  $getSelection,
  $isRangeSelection,
  FORMAT_TEXT_COMMAND,
  FORMAT_ELEMENT_COMMAND,
  UNDO_COMMAND,
  REDO_COMMAND,
  COMMAND_PRIORITY_CRITICAL,
  SELECTION_CHANGE_COMMAND,
} from 'lexical';
import { $isHeadingNode } from '@lexical/rich-text';
import {
  INSERT_ORDERED_LIST_COMMAND,
  INSERT_UNORDERED_LIST_COMMAND,
  $isListNode,
} from '@lexical/list';
import { INSERT_TABLE_COMMAND } from '@lexical/table';
import { $isLinkNode, TOGGLE_LINK_COMMAND } from '@lexical/link';
import { $getNearestNodeOfType, mergeRegister } from '@lexical/utils';

// ── Font Lists ───────────────────────────────────────────────────────────────
const FONT_FAMILIES = [
  // Varnaakshara / Indian language fonts
  'Noto Sans Kannada',
  'Noto Sans Devanagari',
  'Noto Sans Telugu',
  'Noto Sans Tamil',
  'Noto Sans Malayalam',
  'Noto Sans Bengali',
  'Noto Sans Gujarati',
  'Noto Sans Gurmukhi',
  'Noto Sans Oriya',
  'Noto Serif Kannada',
  'Noto Serif Devanagari',
  'Noto Serif Telugu',
  'Noto Serif Tamil',
  // General fonts
  'Noto Serif',
  'Noto Sans',
  'Arial',
  'Calibri',
  'Cambria',
  'Georgia',
  'Segoe UI',
  'Tahoma',
  'Times New Roman',
  'Trebuchet MS',
  'Verdana',
  'Courier New',
  'Consolas',
];

const FONT_SIZES = [
  '8', '9', '10', '11', '12', '14', '16', '18',
  '20', '24', '28', '32', '36', '48', '72',
];

// ── Toolbar Component ────────────────────────────────────────────────────────
export default function Toolbar() {
  const [editor] = useLexicalComposerContext();

  // Active format states
  const [isBold, setIsBold] = useState(false);
  const [isItalic, setIsItalic] = useState(false);
  const [isUnderline, setIsUnderline] = useState(false);
  const [isStrikethrough, setIsStrikethrough] = useState(false);
  const [fontFamily, setFontFamily] = useState('Noto Serif');
  const [fontSize, setFontSize] = useState('12');
  const [textColor, setTextColor] = useState('#000000');
  const [bgColor, setBgColor] = useState('#ffff00');
  const [textAlign, setTextAlign] = useState('left');
  const [blockType, setBlockType] = useState('paragraph');
  const [canUndo, setCanUndo] = useState(false);
  const [canRedo, setCanRedo] = useState(false);

  // ── Update toolbar state from selection ────────────────────────────────
  const updateToolbar = useCallback(() => {
    const selection = $getSelection();
    if (!$isRangeSelection(selection)) return;

    setIsBold(selection.hasFormat('bold'));
    setIsItalic(selection.hasFormat('italic'));
    setIsUnderline(selection.hasFormat('underline'));
    setIsStrikethrough(selection.hasFormat('strikethrough'));

    // Check block type
    const anchorNode = selection.anchor.getNode();
    const element = anchorNode.getKey() === 'root'
      ? anchorNode
      : anchorNode.getTopLevelElementOrThrow();

    if ($isHeadingNode(element)) {
      setBlockType(element.getTag());
    } else if ($isListNode(element)) {
      const parentList = $getNearestNodeOfType(anchorNode, element.constructor);
      setBlockType(parentList ? parentList.getListType() : 'paragraph');
    } else {
      setBlockType(element.getType());
    }

    // Read inline styles for font/size/color
    const style = selection.style || '';
    const fontMatch = style.match(/font-family:\s*([^;]+)/);
    if (fontMatch) setFontFamily(fontMatch[1].trim().replace(/['"]/g, ''));
    const sizeMatch = style.match(/font-size:\s*(\d+)/);
    if (sizeMatch) setFontSize(sizeMatch[1]);
  }, []);

  // ── Register selection change listener ─────────────────────────────────
  useEffect(() => {
    return mergeRegister(
      editor.registerCommand(
        SELECTION_CHANGE_COMMAND,
        () => {
          updateToolbar();
          return false;
        },
        COMMAND_PRIORITY_CRITICAL,
      ),
      editor.registerUpdateListener(({ editorState }) => {
        editorState.read(() => updateToolbar());
      }),
    );
  }, [editor, updateToolbar]);

  // Track undo/redo availability
  useEffect(() => {
    return mergeRegister(
      editor.registerCommand(
        UNDO_COMMAND,
        () => false,
        COMMAND_PRIORITY_CRITICAL,
      ),
      editor.registerCommand(
        REDO_COMMAND,
        () => false,
        COMMAND_PRIORITY_CRITICAL,
      ),
    );
  }, [editor]);

  // ── Format Handlers ────────────────────────────────────────────────────
  const formatText = (format) => () => {
    editor.dispatchCommand(FORMAT_TEXT_COMMAND, format);
  };

  const formatElement = (alignment) => () => {
    editor.dispatchCommand(FORMAT_ELEMENT_COMMAND, alignment);
  };

  const handleUndo = () => editor.dispatchCommand(UNDO_COMMAND, undefined);
  const handleRedo = () => editor.dispatchCommand(REDO_COMMAND, undefined);

  const handleFontFamilyChange = (e) => {
    const value = e.target.value;
    setFontFamily(value);
    editor.update(() => {
      const selection = $getSelection();
      if ($isRangeSelection(selection)) {
        selection.setStyle(`font-family: ${value}`);
      }
    });
  };

  const handleFontSizeChange = (e) => {
    const value = e.target.value;
    setFontSize(value);
    editor.update(() => {
      const selection = $getSelection();
      if ($isRangeSelection(selection)) {
        selection.setStyle(`font-size: ${value}pt`);
      }
    });
  };

  const handleTextColorChange = (e) => {
    const value = e.target.value;
    setTextColor(value);
    editor.update(() => {
      const selection = $getSelection();
      if ($isRangeSelection(selection)) {
        selection.setStyle(`color: ${value}`);
      }
    });
  };

  const handleBgColorChange = (e) => {
    const value = e.target.value;
    setBgColor(value);
    editor.update(() => {
      const selection = $getSelection();
      if ($isRangeSelection(selection)) {
        selection.setStyle(`background-color: ${value}`);
      }
    });
  };

  const handleBulletList = () => {
    editor.dispatchCommand(INSERT_UNORDERED_LIST_COMMAND, undefined);
  };

  const handleNumberedList = () => {
    editor.dispatchCommand(INSERT_ORDERED_LIST_COMMAND, undefined);
  };

  const handleInsertTable = () => {
    // Insert a default 3x3 table
    editor.dispatchCommand(INSERT_TABLE_COMMAND, { rows: '3', columns: '3' });
  };

  const handleInsertLink = () => {
    const url = prompt('Enter URL:');
    if (url) {
      editor.dispatchCommand(TOGGLE_LINK_COMMAND, url);
    }
  };

  const handleInsertImage = () => {
    // TODO: Implement image insertion via IPC dialog
    if (typeof window.require === 'function') {
      const { ipcRenderer } = window.require('electron');
      // The main process will send 'insert-image' with the file path
      // For now, trigger the menu command
      console.log('Insert image: use Insert > Image from the menu bar');
    }
  };

  // ── Render ─────────────────────────────────────────────────────────────
  return (
    <div className="toolbar" role="toolbar" aria-label="Formatting toolbar">
      {/* ── Clipboard Section ──────────────────────────────────────────── */}
      <div className="toolbar-section">
        <button
          className="toolbar-btn"
          onClick={handleUndo}
          title="Undo (Ctrl+Z)"
          aria-label="Undo"
        >
          ↶
        </button>
        <button
          className="toolbar-btn"
          onClick={handleRedo}
          title="Redo (Ctrl+Y)"
          aria-label="Redo"
        >
          ↷
        </button>
      </div>

      {/* ── Font Section ───────────────────────────────────────────────── */}
      <div className="toolbar-section">
        <select
          className="toolbar-select toolbar-select-font"
          value={fontFamily}
          onChange={handleFontFamilyChange}
          title="Font Family"
          aria-label="Font Family"
        >
          {FONT_FAMILIES.map((font) => (
            <option key={font} value={font} style={{ fontFamily: font }}>
              {font}
            </option>
          ))}
        </select>
        <select
          className="toolbar-select toolbar-select-size"
          value={fontSize}
          onChange={handleFontSizeChange}
          title="Font Size"
          aria-label="Font Size"
        >
          {FONT_SIZES.map((size) => (
            <option key={size} value={size}>
              {size}
            </option>
          ))}
        </select>
      </div>

      {/* ── Text Format Section ────────────────────────────────────────── */}
      <div className="toolbar-section">
        <button
          className={`toolbar-btn ${isBold ? 'active' : ''}`}
          onClick={formatText('bold')}
          title="Bold (Ctrl+B)"
          aria-label="Bold"
          aria-pressed={isBold}
        >
          <strong>B</strong>
        </button>
        <button
          className={`toolbar-btn ${isItalic ? 'active' : ''}`}
          onClick={formatText('italic')}
          title="Italic (Ctrl+I)"
          aria-label="Italic"
          aria-pressed={isItalic}
        >
          <em>I</em>
        </button>
        <button
          className={`toolbar-btn ${isUnderline ? 'active' : ''}`}
          onClick={formatText('underline')}
          title="Underline (Ctrl+U)"
          aria-label="Underline"
          aria-pressed={isUnderline}
        >
          <span style={{ textDecoration: 'underline' }}>U</span>
        </button>
        <button
          className={`toolbar-btn ${isStrikethrough ? 'active' : ''}`}
          onClick={formatText('strikethrough')}
          title="Strikethrough (Ctrl+Shift+X)"
          aria-label="Strikethrough"
          aria-pressed={isStrikethrough}
        >
          <span style={{ textDecoration: 'line-through' }}>S</span>
        </button>

        {/* Text Color */}
        <div className="toolbar-btn toolbar-color-btn" title="Text Color">
          <span style={{ fontWeight: 700, fontSize: '14px' }}>A</span>
          <div className="color-indicator" style={{ backgroundColor: textColor }} />
          <input type="color" value={textColor} onChange={handleTextColorChange} aria-label="Text Color" />
        </div>

        {/* Highlight Color */}
        <div className="toolbar-btn toolbar-color-btn" title="Highlight Color">
          <span style={{ fontWeight: 700, fontSize: '12px', backgroundColor: bgColor, padding: '0 2px' }}>ab</span>
          <div className="color-indicator" style={{ backgroundColor: bgColor }} />
          <input type="color" value={bgColor} onChange={handleBgColorChange} aria-label="Highlight Color" />
        </div>
      </div>

      {/* ── Paragraph Section ──────────────────────────────────────────── */}
      <div className="toolbar-section">
        <button
          className={`toolbar-btn ${textAlign === 'left' ? 'active' : ''}`}
          onClick={formatElement('left')}
          title="Align Left (Ctrl+L)"
          aria-label="Align Left"
        >
          ≡
        </button>
        <button
          className={`toolbar-btn ${textAlign === 'center' ? 'active' : ''}`}
          onClick={formatElement('center')}
          title="Center (Ctrl+E)"
          aria-label="Center"
        >
          ≡
        </button>
        <button
          className={`toolbar-btn ${textAlign === 'right' ? 'active' : ''}`}
          onClick={formatElement('right')}
          title="Align Right (Ctrl+R)"
          aria-label="Align Right"
        >
          ≡
        </button>
        <button
          className={`toolbar-btn ${textAlign === 'justify' ? 'active' : ''}`}
          onClick={formatElement('justify')}
          title="Justify (Ctrl+J)"
          aria-label="Justify"
        >
          ≡
        </button>
      </div>

      {/* ── List Section ───────────────────────────────────────────────── */}
      <div className="toolbar-section">
        <button
          className="toolbar-btn"
          onClick={handleBulletList}
          title="Bullet List"
          aria-label="Bullet List"
        >
          •≡
        </button>
        <button
          className="toolbar-btn"
          onClick={handleNumberedList}
          title="Numbered List"
          aria-label="Numbered List"
        >
          1.
        </button>
      </div>

      {/* ── Insert Section ─────────────────────────────────────────────── */}
      <div className="toolbar-section">
        <button
          className="toolbar-btn toolbar-btn-text"
          onClick={handleInsertTable}
          title="Insert Table"
          aria-label="Insert Table"
        >
          ⊞ Table
        </button>
        <button
          className="toolbar-btn toolbar-btn-text"
          onClick={handleInsertImage}
          title="Insert Image"
          aria-label="Insert Image"
        >
          🖼 Image
        </button>
        <button
          className="toolbar-btn toolbar-btn-text"
          onClick={handleInsertLink}
          title="Insert Link (Ctrl+K)"
          aria-label="Insert Link"
        >
          🔗 Link
        </button>
      </div>
    </div>
  );
}
