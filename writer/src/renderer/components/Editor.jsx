import React, { useCallback, useEffect, useRef, useState } from 'react';
import { LexicalComposer } from '@lexical/react/LexicalComposer';
import { RichTextPlugin } from '@lexical/react/LexicalRichTextPlugin';
import { ContentEditable } from '@lexical/react/LexicalContentEditable';
import { HistoryPlugin } from '@lexical/react/LexicalHistoryPlugin';
import { ListPlugin } from '@lexical/react/LexicalListPlugin';
import { LinkPlugin } from '@lexical/react/LexicalLinkPlugin';
import { TablePlugin } from '@lexical/react/LexicalTablePlugin';
import { AutoFocusPlugin } from '@lexical/react/LexicalAutoFocusPlugin';
import { OnChangePlugin } from '@lexical/react/LexicalOnChangePlugin';
import { HorizontalRulePlugin } from '@lexical/react/LexicalHorizontalRulePlugin';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import LexicalErrorBoundary from '@lexical/react/LexicalErrorBoundary';
import { HeadingNode, QuoteNode, $isHeadingNode } from '@lexical/rich-text';
import { ListNode, ListItemNode, $isListNode } from '@lexical/list';
import { TableNode, TableCellNode, TableRowNode } from '@lexical/table';
import { LinkNode, AutoLinkNode } from '@lexical/link';
import { CodeNode, CodeHighlightNode } from '@lexical/code';
import { HorizontalRuleNode } from '@lexical/react/LexicalHorizontalRuleNode';
import {
  $getSelection,
  $isRangeSelection,
  $insertNodes,
  $createParagraphNode,
  SELECTION_CHANGE_COMMAND,
  COMMAND_PRIORITY_CRITICAL,
  COMMAND_PRIORITY_EDITOR,
  COMMAND_PRIORITY_LOW,
} from 'lexical';
import { $getNearestNodeOfType, mergeRegister } from '@lexical/utils';

import Ribbon from './Ribbon';
import EditorIntegrationPlugin from './panels/EditorIntegrationPlugin';
import StatusBar from './StatusBar';
import FindReplacePlugin from '../plugins/FindReplacePlugin';
import SymbolPickerPlugin from '../plugins/SymbolPickerPlugin';
import WordCountModal from '../plugins/WordCountModal';
import TableGridPlugin from '../plugins/TableGridPlugin';
import { ImageNode, $createImageNode, INSERT_IMAGE_COMMAND } from '../nodes/ImageNode';
import { PageBreakNode, $createPageBreakNode, INSERT_PAGE_BREAK_COMMAND } from '../nodes/PageBreakNode';
import {
  serializeDocument,
  deserializeDocument,
  exportToHtml,
  exportToDocxBlob,
  exportToRtfString,
  importDocxIntoEditor,
} from '../utils/fileOps';
import '../styles/editor.css';
import '../styles/app.css';

const { ipcRenderer } = window.require ? window.require('electron') : { ipcRenderer: null };

// ── Lexical Theme ────────────────────────────────────────────────────────────
const editorTheme = {
  root: 'editor-root',
  paragraph: 'editor-paragraph',
  heading: {
    h1: 'editor-heading-h1',
    h2: 'editor-heading-h2',
    h3: 'editor-heading-h3',
    h4: 'editor-heading-h4',
  },
  text: {
    bold: 'editor-text-bold',
    italic: 'editor-text-italic',
    underline: 'editor-text-underline',
    strikethrough: 'editor-text-strikethrough',
    code: 'editor-text-code',
    superscript: 'editor-text-superscript',
    subscript: 'editor-text-subscript',
  },
  list: {
    ul: 'editor-list-ul',
    ol: 'editor-list-ol',
    listitem: 'editor-listitem',
    nested: { listitem: 'editor-nested-listitem' },
  },
  table: 'editor-table',
  tableCell: 'editor-table-cell',
  tableCellHeader: 'editor-table-cell-header',
  tableRow: 'editor-table-row',
  link: 'editor-link',
  code: 'editor-code',
  quote: 'editor-quote',
  horizontalRule: 'editor-hr',
};

// ── Registered Nodes ─────────────────────────────────────────────────────────
const editorNodes = [
  HeadingNode, QuoteNode, ListNode, ListItemNode,
  TableNode, TableCellNode, TableRowNode,
  LinkNode, AutoLinkNode, CodeNode, CodeHighlightNode,
  HorizontalRuleNode, ImageNode, PageBreakNode,
];

function onError(error) {
  console.error('[Lexical Error]', error);
}

// ── Menu Command Listener Plugin ─────────────────────────────────────────────
function MenuCommandPlugin() {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    if (!ipcRenderer) return;

    const handlers = {
      'menu-new': () => {
        editor.update(() => {
          const root = editor._editorState._nodeMap.get('root');
          if (root) root.clear();
        });
        ipcRenderer.send('set-current-file', null);
        ipcRenderer.send('set-dirty', false);
      },
      'menu-save': () => {
        const state = editor.getEditorState();
        const content = serializeDocument(state);
        ipcRenderer.invoke('save-file', { content });
      },
      'menu-save-as': () => {
        const state = editor.getEditorState();
        const content = serializeDocument(state);
        ipcRenderer.invoke('save-file-as', { content });
      },
      'open-file': async (_e, filePath) => {
        const result = await ipcRenderer.invoke('open-file', filePath);
        if (result.success) {
          deserializeDocument(editor, result.content);
          ipcRenderer.send('set-dirty', false);
        }
      },
      'auto-save': () => {
        const state = editor.getEditorState();
        const content = serializeDocument(state);
        ipcRenderer.invoke('save-file', { content });
      },
      'menu-export': async (_e, format) => {
        const state = editor.getEditorState();
        try {
          if (format === 'html') {
            const content = exportToHtml(editor);
            await ipcRenderer.invoke('export-file', { format, content });
            return;
          }
          if (format === 'docx') {
            const blob = await exportToDocxBlob(state, { title: 'Untitled' });
            const arrayBuffer = await blob.arrayBuffer();
            const b64 = Buffer.from(arrayBuffer).toString('base64');
            await ipcRenderer.invoke('export-file', { format, content: b64 });
            return;
          }
          if (format === 'rtf') {
            const rtf = await exportToRtfString(state);
            await ipcRenderer.invoke('export-file', { format, content: rtf });
            return;
          }
          if (format === 'pdf') {
            await ipcRenderer.invoke('export-file', { format, content: '' });
            return;
          }
          const content = exportToHtml(editor);
          await ipcRenderer.invoke('export-file', { format, content });
        } catch (err) {
          console.error('[export] failed:', err);
          ipcRenderer.invoke('show-error', { title: 'Export failed', message: err.message || String(err) });
        }
      },
      'menu-import-docx': async (_e, filePath) => {
        try {
          const result = await ipcRenderer.invoke('open-docx', filePath);
          if (!result.success) return;
          await importDocxIntoEditor(editor, result.buffer);
          ipcRenderer.send('set-dirty', true);
        } catch (err) {
          console.error('[import-docx] failed:', err);
          ipcRenderer.invoke('show-error', { title: 'Import failed', message: err.message || String(err) });
        }
      },
      'menu-print': () => ipcRenderer.invoke('print'),
      'menu-undo': () => editor.dispatchCommand('UNDO_COMMAND', undefined),
      'menu-redo': () => editor.dispatchCommand('REDO_COMMAND', undefined),
    };

    Object.entries(handlers).forEach(([ch, h]) => ipcRenderer.on(ch, h));
    return () => Object.entries(handlers).forEach(([ch, h]) => ipcRenderer.removeListener(ch, h));
  }, [editor]);

  return null;
}

// ── Image Command Plugin ─────────────────────────────────────────────────────
function ImagePlugin() {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    return editor.registerCommand(
      INSERT_IMAGE_COMMAND,
      (payload) => {
        const imageNode = $createImageNode(payload);
        $insertNodes([imageNode]);
        return true;
      },
      COMMAND_PRIORITY_EDITOR,
    );
  }, [editor]);

  return null;
}

// ── Page Break Command Plugin ────────────────────────────────────────────────
function PageBreakPlugin() {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    return editor.registerCommand(
      INSERT_PAGE_BREAK_COMMAND,
      () => {
        const pageBreakNode = $createPageBreakNode();
        $insertNodes([pageBreakNode]);
        // Insert a paragraph after page break so user can type
        const paragraphNode = $createParagraphNode();
        pageBreakNode.insertAfter(paragraphNode);
        paragraphNode.selectStart();
        return true;
      },
      COMMAND_PRIORITY_EDITOR,
    );
  }, [editor]);

  return null;
}

// ── Format State Tracker Plugin ──────────────────────────────────────────────
function FormatStatePlugin({ onUpdate }) {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    return mergeRegister(
      editor.registerCommand(
        SELECTION_CHANGE_COMMAND,
        () => {
          const selection = $getSelection();
          if (!$isRangeSelection(selection)) return false;

          const anchorNode = selection.anchor.getNode();
          const topLevelElement = anchorNode.getTopLevelElementOrThrow();
          let blockType = 'paragraph';
          if ($isHeadingNode(topLevelElement)) {
            blockType = topLevelElement.getTag();
          } else if ($isListNode(topLevelElement)) {
            const parentList = $getNearestNodeOfType(anchorNode, ListNode);
            blockType = parentList ? parentList.getListType() : 'paragraph';
          } else if (topLevelElement.getType() === 'quote') {
            blockType = 'quote';
          } else if (topLevelElement.getType() === 'code') {
            blockType = 'code';
          }

          onUpdate({
            isBold: selection.hasFormat('bold'),
            isItalic: selection.hasFormat('italic'),
            isUnderline: selection.hasFormat('underline'),
            isStrikethrough: selection.hasFormat('strikethrough'),
            isSuperscript: selection.hasFormat('superscript'),
            isSubscript: selection.hasFormat('subscript'),
            blockType,
          });
          return false;
        },
        COMMAND_PRIORITY_CRITICAL,
      ),
    );
  }, [editor, onUpdate]);

  return null;
}

// ── Word Count Plugin ────────────────────────────────────────────────────────
function WordCountPlugin({ onUpdate }) {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    return editor.registerUpdateListener(({ editorState }) => {
      editorState.read(() => {
        const text = editor.getRootElement()?.textContent || '';
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        const chars = text.length;
        const counts = { words, chars, pages: Math.max(1, Math.ceil(words / 250)) };
        onUpdate(counts);
        window.dispatchEvent(new CustomEvent('varnaakshara-counts', { detail: counts }));
      });
    });
  }, [editor, onUpdate]);

  return null;
}

// ── Keyboard Shortcuts Plugin ────────────────────────────────────────────────
function KeyboardShortcutsPlugin({ onCtrlF }) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === 'f' || e.key === 'h')) {
        e.preventDefault();
        onCtrlF();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onCtrlF]);

  return null;
}

// ── Main Editor Component ────────────────────────────────────────────────────
export default function Editor({ zoom = 1.0, activeTab = 'Home', onOpenPanel, pageSetup, onPageSetupChange }) {
  const [counts, setCounts] = useState({ words: 0, chars: 0, pages: 1 });
  const [formatState, setFormatState] = useState({
    isBold: false,
    isItalic: false,
    isUnderline: false,
    isStrikethrough: false,
    isSuperscript: false,
    isSubscript: false,
    fontFamily: 'Noto Serif',
    fontSize: '12',
    textColor: '#000000',
    bgColor: '#ffff00',
    blockType: 'paragraph',
  });

  // UI state for modals/popups
  const [findReplaceOpen, setFindReplaceOpen] = useState(false);
  const [symbolPickerOpen, setSymbolPickerOpen] = useState(false);
  const [wordCountOpen, setWordCountOpen] = useState(false);
  const [tableGridOpen, setTableGridOpen] = useState(false);
  const [spellCheck, setSpellCheck] = useState(false);
  const [lineSpacing, setLineSpacing] = useState('1.6');

  const initialConfig = {
    namespace: 'VarnaaksharaWriter',
    theme: editorTheme,
    nodes: editorNodes,
    onError,
  };

  const handleChange = useCallback(() => {
    if (ipcRenderer) ipcRenderer.send('set-dirty', true);
  }, []);

  const handleCountUpdate = useCallback((c) => setCounts(c), []);

  const handleFormatUpdate = useCallback((fmt) => {
    setFormatState((prev) => ({ ...prev, ...fmt }));
  }, []);

  const handleFontChange = useCallback((e) => {
    setFormatState((prev) => ({ ...prev, fontFamily: e.target.value }));
  }, []);

  const handleSizeChange = useCallback((e) => {
    setFormatState((prev) => ({ ...prev, fontSize: e.target.value }));
  }, []);

  const handleColorChange = useCallback((e) => {
    setFormatState((prev) => ({ ...prev, textColor: e.target.value }));
  }, []);

  const handleBgColorChange = useCallback((e) => {
    setFormatState((prev) => ({ ...prev, bgColor: e.target.value }));
  }, []);

  const handleLineSpacingChange = useCallback((val) => {
    setLineSpacing(val);
  }, []);

  // Image insert handler — uses IPC for file dialog
  const handleImageInsert = useCallback(() => {
    if (!ipcRenderer) {
      // Fallback for dev: use a file input
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          // Dispatch via custom event — will be picked up in a plugin
          window.__lexicalInsertImage?.({ src: reader.result, altText: file.name });
        };
        reader.readAsDataURL(file);
      };
      input.click();
      return;
    }
    ipcRenderer.invoke('dialog-open-image').then((result) => {
      if (result && result.src) {
        window.__lexicalInsertImage?.({ src: result.src, altText: result.altText || 'Image' });
      }
    }).catch(() => {
      // Fallback: use native file input
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = () => {
          window.__lexicalInsertImage?.({ src: reader.result, altText: file.name });
        };
        reader.readAsDataURL(file);
      };
      input.click();
    });
  }, []);

  // Page style computation
  const pageStyle = {
    width: pageSetup.orientation === 'landscape' ? pageSetup.pageHeight : pageSetup.pageWidth,
    minHeight: pageSetup.orientation === 'landscape' ? pageSetup.pageWidth : pageSetup.pageHeight,
    padding: pageSetup.margin,
    transform: `scale(${zoom})`,
    transformOrigin: 'top center',
  };

  const contentStyle = {};
  if (pageSetup.columns > 1) {
    contentStyle.columnCount = pageSetup.columns;
    contentStyle.columnGap = '24px';
  }
  if (pageSetup.spacingBefore > 0 || pageSetup.spacingAfter > 0) {
    contentStyle['--para-spacing-before'] = `${pageSetup.spacingBefore}pt`;
    contentStyle['--para-spacing-after'] = `${pageSetup.spacingAfter}pt`;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1, overflow: 'hidden' }}>
      <LexicalComposer initialConfig={initialConfig}>
        <Ribbon
          activeTab={activeTab}
          formatState={formatState}
          onFontChange={handleFontChange}
          onSizeChange={handleSizeChange}
          onColorChange={handleColorChange}
          onBgColorChange={handleBgColorChange}
          onOpenPanel={onOpenPanel}
          pageSetup={pageSetup}
          onPageSetupChange={onPageSetupChange}
          onTableGridOpen={() => setTableGridOpen(true)}
          onSymbolPickerOpen={() => setSymbolPickerOpen(true)}
          onImageInsert={handleImageInsert}
          onFindReplace={() => setFindReplaceOpen(true)}
          onWordCount={() => setWordCountOpen(true)}
          onSpellCheckToggle={() => setSpellCheck((p) => !p)}
          spellCheck={spellCheck}
          onLineSpacingChange={handleLineSpacingChange}
        />

        {/* Find & Replace Bar */}
        <FindReplacePlugin isOpen={findReplaceOpen} onClose={() => setFindReplaceOpen(false)} />

        {/* Ruler */}
        <div className="ruler">
          <div className="ruler-inner" style={{ width: pageSetup.orientation === 'landscape' ? pageSetup.pageHeight : pageSetup.pageWidth }} />
        </div>

        {/* Pasteboard + Page */}
        <div className="editor-pasteboard">
          <div className="editor-area">
            <div className="editor-page" style={pageStyle}>
              <div style={contentStyle}>
                <RichTextPlugin
                  contentEditable={
                    <ContentEditable
                      className="editor-root"
                      spellCheck={spellCheck}
                      style={{ lineHeight: lineSpacing }}
                    />
                  }
                  placeholder={
                    <div className="editor-placeholder">
                      Start typing here… or press Ctrl+O to open a document.
                    </div>
                  }
                  ErrorBoundary={LexicalErrorBoundary}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Plugins */}
        <HistoryPlugin />
        <ListPlugin />
        <LinkPlugin />
        <TablePlugin />
        <HorizontalRulePlugin />
        <AutoFocusPlugin />
        <OnChangePlugin onChange={handleChange} ignoreSelectionChange />
        <MenuCommandPlugin />
        <ImagePlugin />
        <PageBreakPlugin />
        <ImageInsertBridge />
        <FormatStatePlugin onUpdate={handleFormatUpdate} />
        <WordCountPlugin onUpdate={handleCountUpdate} />
        <EditorIntegrationPlugin />
        <KeyboardShortcutsPlugin onCtrlF={() => setFindReplaceOpen(true)} />
        <ParagraphSpacingPlugin spacingBefore={pageSetup.spacingBefore} spacingAfter={pageSetup.spacingAfter} />

        {/* Modals */}
        <SymbolPickerPlugin isOpen={symbolPickerOpen} onClose={() => setSymbolPickerOpen(false)} />
        <WordCountModal isOpen={wordCountOpen} onClose={() => setWordCountOpen(false)} />
        <TableGridPlugin isOpen={tableGridOpen} onClose={() => setTableGridOpen(false)} />

        <StatusBar
          pageCount={counts.pages}
          wordCount={counts.words}
          charCount={counts.chars}
          zoom={zoom}
        />
      </LexicalComposer>
    </div>
  );
}

// ── ImageInsertBridge — bridges window.__lexicalInsertImage to Lexical command ──
function ImageInsertBridge() {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    window.__lexicalInsertImage = (payload) => {
      editor.dispatchCommand(INSERT_IMAGE_COMMAND, payload);
    };
    return () => { window.__lexicalInsertImage = null; };
  }, [editor]);

  return null;
}

// ── Paragraph Spacing Plugin — Injects CSS for paragraph spacing ─────────────
function ParagraphSpacingPlugin({ spacingBefore, spacingAfter }) {
  useEffect(() => {
    const id = 'para-spacing-style';
    let style = document.getElementById(id);
    if (!style) {
      style = document.createElement('style');
      style.id = id;
      document.head.appendChild(style);
    }
    style.textContent = `
      .editor-root p,
      .editor-root h1,
      .editor-root h2,
      .editor-root h3,
      .editor-root h4 {
        margin-top: ${spacingBefore || 0}pt;
        margin-bottom: ${spacingAfter || 8}px;
      }
    `;
    return () => {
      const el = document.getElementById(id);
      if (el) el.remove();
    };
  }, [spacingBefore, spacingAfter]);

  return null;
}
