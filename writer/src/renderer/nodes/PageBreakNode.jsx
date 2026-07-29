/**
 * PageBreakNode — A visual page-break separator that prints as page-break-before: always.
 */
import React from 'react';
import { DecoratorNode, createCommand } from 'lexical';

export const INSERT_PAGE_BREAK_COMMAND = createCommand('INSERT_PAGE_BREAK_COMMAND');

/* ── React component ──────────────────────────────────────────────────────── */
function PageBreakComponent() {
  return (
    <div className="editor-page-break" contentEditable={false}>
      <span className="editor-page-break-label">Page Break</span>
    </div>
  );
}

/* ── Lexical Node ─────────────────────────────────────────────────────────── */
export class PageBreakNode extends DecoratorNode {
  static getType() {
    return 'page-break';
  }

  static clone(node) {
    return new PageBreakNode(node.__key);
  }

  constructor(key) {
    super(key);
  }

  createDOM() {
    const div = document.createElement('div');
    div.style.pageBreakBefore = 'always';
    return div;
  }

  updateDOM() {
    return false;
  }

  decorate() {
    return <PageBreakComponent />;
  }

  static importJSON() {
    return $createPageBreakNode();
  }

  exportJSON() {
    return {
      type: 'page-break',
      version: 1,
    };
  }

  isInline() {
    return false;
  }

  getTextContent() {
    return '\n';
  }
}

export function $createPageBreakNode() {
  return new PageBreakNode();
}

export function $isPageBreakNode(node) {
  return node instanceof PageBreakNode;
}
