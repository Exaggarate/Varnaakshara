/**
 * EditorIntegrationPlugin — Minimal Lexical plugin that listens for custom
 * DOM events dispatched by the Panels sidebar and translates them into
 * Lexical editor commands.  Keeps Editor.jsx changes to a single import +
 * one JSX element.
 */
import { useEffect } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import {
  $getSelection,
  $isRangeSelection,
  $createParagraphNode,
  FORMAT_TEXT_COMMAND,
} from 'lexical';
import { $createHeadingNode, $createQuoteNode } from '@lexical/rich-text';
import { $setBlocksType } from '@lexical/selection';

export default function EditorIntegrationPlugin() {
  const [editor] = useLexicalComposerContext();

  useEffect(() => {
    /* ── Insert arbitrary text at cursor ───────────────────────────────── */
    const handleInsertText = (e) => {
      const text = e.detail?.text;
      if (!text) return;
      editor.focus();
      editor.update(() => {
        const selection = $getSelection();
        if ($isRangeSelection(selection)) {
          selection.insertText(text);
        }
      });
    };

    /* ── Apply paragraph / character style ─────────────────────────────── */
    const handleApplyStyle = (e) => {
      const { type, styleId } = e.detail || {};

      if (type === 'paragraph') {
        editor.focus();
        editor.update(() => {
          const selection = $getSelection();
          if (!$isRangeSelection(selection)) return;

          switch (styleId) {
            case 'h1':
              $setBlocksType(selection, () => $createHeadingNode('h1'));
              break;
            case 'h2':
              $setBlocksType(selection, () => $createHeadingNode('h2'));
              break;
            case 'h3':
              $setBlocksType(selection, () => $createHeadingNode('h3'));
              break;
            case 'h4':
              $setBlocksType(selection, () => $createHeadingNode('h4'));
              break;
            case 'quote':
              $setBlocksType(selection, () => $createQuoteNode());
              break;
            case 'title':
              $setBlocksType(selection, () => $createHeadingNode('h1'));
              break;
            case 'subtitle':
              $setBlocksType(selection, () => $createHeadingNode('h2'));
              break;
            case 'normal':
            case 'list':
            default:
              $setBlocksType(selection, () => $createParagraphNode());
              break;
          }
        });
      } else if (type === 'character') {
        editor.focus();
        switch (styleId) {
          case 'bold':
            editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'bold');
            break;
          case 'italic':
            editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'italic');
            break;
          case 'strong':
            editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'bold');
            setTimeout(() => editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'italic'), 0);
            break;
          case 'subtle':
            editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'italic');
            break;
          case 'book-title':
            editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'bold');
            setTimeout(() => {
              editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'italic');
              setTimeout(() => editor.dispatchCommand(FORMAT_TEXT_COMMAND, 'underline'), 0);
            }, 0);
            break;
          default:
            break;
        }
      }
    };

    /* ── Apply text / background color ─────────────────────────────────── */
    const handleApplyColor = (e) => {
      const { color, target } = e.detail || {};
      if (!color) return;
      editor.focus();
      editor.update(() => {
        const selection = $getSelection();
        if (!$isRangeSelection(selection)) return;
        // Use style text for color application
        const nodes = selection.getNodes();
        nodes.forEach((node) => {
          if (node.setStyle) {
            const existing = node.getStyle() || '';
            const prop = target === 'background' ? 'background-color' : 'color';
            // Simple style merge
            const regex = new RegExp(`${prop}\\s*:[^;]+;?`, 'g');
            const cleaned = existing.replace(regex, '').trim();
            node.setStyle(`${cleaned} ${prop}: ${color};`.trim());
          }
        });
      });
    };

    /* ── Scroll to page ────────────────────────────────────────────────── */
    const handleScrollToPage = (e) => {
      const { page } = e.detail || {};
      if (page == null) return;
      const pasteboard = document.querySelector('.editor-pasteboard');
      if (!pasteboard) return;
      const editorPage = document.querySelector('.editor-page');
      if (!editorPage) return;
      const pageHeight = editorPage.offsetHeight || 1056;
      const linesPerPage = 250; // approx words per page
      // Estimate scroll position
      const scrollTarget = (page - 1) * (pageHeight * 0.8);
      pasteboard.scrollTo({ top: scrollTarget, behavior: 'smooth' });
    };

    window.addEventListener('varnaakshara-insert-text', handleInsertText);
    window.addEventListener('varnaakshara-apply-style', handleApplyStyle);
    window.addEventListener('varnaakshara-apply-color', handleApplyColor);
    window.addEventListener('varnaakshara-scroll-to-page', handleScrollToPage);

    return () => {
      window.removeEventListener('varnaakshara-insert-text', handleInsertText);
      window.removeEventListener('varnaakshara-apply-style', handleApplyStyle);
      window.removeEventListener('varnaakshara-apply-color', handleApplyColor);
      window.removeEventListener('varnaakshara-scroll-to-page', handleScrollToPage);
    };
  }, [editor]);

  return null;
}
