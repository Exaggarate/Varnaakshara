/**
 * Varnaakshara Writer — DOCX Import
 *
 * Uses `mammoth` to convert DOCX ArrayBuffer -> HTML, then converts HTML ->
 * Lexical nodes using @lexical/html.
 */

import * as mammoth from 'mammoth/mammoth.browser';
import { $generateNodesFromDOM } from '@lexical/html';
import { $getRoot, $insertNodes } from 'lexical';

/**
 * importFromDocx(arrayBuffer, editor) -> LexicalEditorState
 *
 * Returns a parsed Lexical EditorState if an editor instance is provided,
 * otherwise returns { html } as a fallback.
 */
export async function importFromDocx(arrayBuffer, editor) {
  try {
    const { value: html } = await mammoth.convertToHtml({ arrayBuffer }, {
      // Keep images as data URIs so we can embed them.
      convertImage: mammoth.images.inline(async (image) => {
        const buffer = await image.read('base64');
        return { src: `data:${image.contentType};base64,${buffer}` };
      }),
    });

    if (!editor) {
      // In case caller wants to handle insertion itself.
      return { html };
    }

    const editorState = editor.parseEditorState(() => {
      const parser = new DOMParser();
      const dom = parser.parseFromString(html, 'text/html');
      const nodes = $generateNodesFromDOM(editor, dom);
      const root = $getRoot();
      root.clear();
      root.selectEnd();
      $insertNodes(nodes);
    });

    return editorState;
  } catch (err) {
    console.error('[docxImport] import failed:', err);
    throw new Error('Failed to import DOCX.');
  }
}

