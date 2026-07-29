/**
 * Varnaakshara Writer — File Operations
 *
 * Handles serialization/deserialization of the Lexical editor state,
 * the .vnk file format, and HTML export.
 */

import { $generateHtmlFromNodes } from '@lexical/html';
import { $getRoot, $insertNodes } from 'lexical';
import { $generateNodesFromDOM } from '@lexical/html';

import { exportToDocx } from './docxExport';
import { exportToPDF } from './pdfExport';
import { exportToRTF } from './rtfExport';
import { importFromDocx } from './docxImport';

// ── VNK File Format ──────────────────────────────────────────────────────────
// .vnk is a JSON wrapper around the Lexical editor state:
// {
//   "varnaakshara": true,
//   "version": "1.0",
//   "created": "2026-07-26T12:00:00.000Z",
//   "modified": "2026-07-26T12:00:00.000Z",
//   "metadata": {
//     "title": "Untitled",
//     "author": "",
//     "language": "en"
//   },
//   "content": { ... lexical editor state JSON ... }
// }

const VNK_VERSION = '1.0';

/**
 * Serialize the current editor state to a .vnk JSON string.
 */
export function serializeDocument(editorState, metadata = {}) {
  const now = new Date().toISOString();
  const stateJson = editorState.toJSON();

  const doc = {
    varnaakshara: true,
    version: VNK_VERSION,
    created: metadata.created || now,
    modified: now,
    metadata: {
      title: metadata.title || 'Untitled',
      author: metadata.author || '',
      language: metadata.language || 'en',
      ...metadata,
    },
    content: stateJson,
  };

  return JSON.stringify(doc, null, 2);
}

/**
 * Deserialize a .vnk file (or plain JSON state) into the editor.
 */
export function deserializeDocument(editor, fileContent) {
  try {
    let content;

    // Try parsing as JSON first (.vnk format)
    try {
      const parsed = JSON.parse(fileContent);

      if (parsed.varnaakshara && parsed.content) {
        // It's a .vnk file
        content = parsed.content;
      } else if (parsed.root) {
        // It's a raw Lexical state
        content = parsed;
      } else {
        throw new Error('Unrecognized JSON format');
      }
    } catch {
      // Not JSON — try as HTML or plain text
      importFromHtml(editor, fileContent);
      return;
    }

    // Parse the Lexical state
    const editorState = editor.parseEditorState(content);
    editor.setEditorState(editorState);
  } catch (err) {
    console.error('[fileOps] Failed to deserialize document:', err);
    // Fallback: insert as plain text
    importFromPlainText(editor, fileContent);
  }
}

/**
 * Export the current editor content as an HTML string.
 */
export function exportToHtml(editor) {
  let html = '';
  editor.getEditorState().read(() => {
    html = $generateHtmlFromNodes(editor, null);
  });

  // Wrap in a full HTML document with basic styling
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="generator" content="Varnaakshara Writer">
  <title>Exported Document</title>
  <style>
    body {
      font-family: 'Noto Serif', 'Noto Sans Kannada', Georgia, 'Times New Roman', serif;
      font-size: 12pt;
      line-height: 1.6;
      max-width: 816px;
      margin: 40px auto;
      padding: 0 40px;
      color: #1a1a1a;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 12px 0;
    }
    table td, table th {
      border: 1px solid #bbb;
      padding: 6px 10px;
    }
    table th {
      background: #f5f5f5;
      font-weight: 600;
    }
    blockquote {
      border-left: 4px solid #2b7de9;
      margin: 8px 0;
      padding: 8px 16px;
      color: #555;
      font-style: italic;
    }
    code {
      font-family: 'Consolas', monospace;
      background: #f4f4f4;
      padding: 1px 5px;
      border-radius: 3px;
    }
    pre {
      font-family: 'Consolas', monospace;
      background: #f8f8f8;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      padding: 12px 16px;
      overflow-x: auto;
    }
    a { color: #2b7de9; }
    img { max-width: 100%; height: auto; }
  </style>
</head>
<body>
${html}
</body>
</html>`;
}

/**
 * Import HTML content into the editor.
 */
export function importFromHtml(editor, htmlString) {
  editor.update(() => {
    const root = $getRoot();
    root.clear();

    const parser = new DOMParser();
    const dom = parser.parseFromString(htmlString, 'text/html');
    const nodes = $generateNodesFromDOM(editor, dom);

    if (nodes.length > 0) {
      root.selectEnd();
      $insertNodes(nodes);
    }
  });
}

/**
 * Import plain text into the editor.
 */
export function importFromPlainText(editor, text) {
  editor.update(() => {
    const root = $getRoot();
    root.clear();

    // Split by newlines and create paragraph nodes
    const { $createParagraphNode, $createTextNode } = require('lexical');
    const lines = text.split('\n');

    for (const line of lines) {
      const paragraph = $createParagraphNode();
      if (line.trim()) {
        paragraph.append($createTextNode(line));
      }
      root.append(paragraph);
    }
  });
}

/**
 * Get document metadata from a .vnk file.
 */
export function getDocumentMetadata(fileContent) {
  try {
    const parsed = JSON.parse(fileContent);
    if (parsed.varnaakshara) {
      return {
        version: parsed.version,
        created: parsed.created,
        modified: parsed.modified,
        ...parsed.metadata,
      };
    }
  } catch {
    // Not a .vnk file
  }
  return null;
}

// ── Additional Export/Import Formats ─────────────────────────────────────────

/**
 * Export editorState to DOCX Blob.
 */
export async function exportToDocxBlob(editorState, metadata = {}) {
  return exportToDocx(editorState, metadata);
}

/**
 * Export an editor DOM element to PDF Blob.
 */
export async function exportToPdfBlob(editorElement, options = {}) {
  return exportToPDF(editorElement, options);
}

/**
 * Export editorState to RTF string.
 */
export async function exportToRtfString(editorState) {
  return exportToRTF(editorState);
}

/**
 * Import DOCX ArrayBuffer into a Lexical editor.
 */
export async function importDocxIntoEditor(editor, arrayBuffer) {
  const editorState = await importFromDocx(arrayBuffer, editor);
  if (editorState) editor.setEditorState(editorState);
  return editorState;
}
