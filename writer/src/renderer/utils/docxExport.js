/**
 * Varnaakshara Writer — DOCX Export
 *
 * Converts Lexical editor state JSON to a DOCX Blob using the `docx` package.
 *
 * Notes:
 * - This is a best-effort mapping. Lexical nodes can be extended; unknown nodes
 *   degrade gracefully to plain paragraphs/text.
 * - Indian scripts are preserved as Unicode (DOCX is UTF-8/Unicode).
 */

import {
  AlignmentType,
  Document,
  ExternalHyperlink,
  HeadingLevel,
  HighlightColor,
  ImageRun,
  LevelFormat,
  Packer,
  Paragraph,
  Table,
  TableCell,
  TableRow,
  TextRun,
  WidthType,
} from 'docx';

function clamp(n, min, max) {
  return Math.max(min, Math.min(max, n));
}

function cssColorToHex(color) {
  if (!color) return undefined;
  const c = String(color).trim();
  if (!c) return undefined;
  if (c.startsWith('#')) {
    const hex = c.slice(1);
    if (hex.length === 3) {
      return (hex[0] + hex[0] + hex[1] + hex[1] + hex[2] + hex[2]).toUpperCase();
    }
    if (hex.length === 6) return hex.toUpperCase();
  }
  // rgb/rgba
  const m = c.match(/^rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)$/i);
  if (m) {
    const r = clamp(parseInt(m[1], 10), 0, 255);
    const g = clamp(parseInt(m[2], 10), 0, 255);
    const b = clamp(parseInt(m[3], 10), 0, 255);
    return [r, g, b].map((x) => x.toString(16).padStart(2, '0')).join('').toUpperCase();
  }
  return undefined;
}

function lexicalFormatToTextStyle(formatBitmask) {
  // Lexical TextNode format bitmask:
  // 1 bold, 2 italic, 4 underline, 8 strikethrough (common Lexical defaults)
  // We avoid importing internals; map by bit positions.
  const f = Number(formatBitmask || 0);
  return {
    bold: (f & 1) !== 0,
    italics: (f & 2) !== 0,
    underline: (f & 4) !== 0,
    strike: (f & 8) !== 0,
  };
}

function mapAlignment(format) {
  switch (format) {
    case 'center':
      return AlignmentType.CENTER;
    case 'right':
      return AlignmentType.RIGHT;
    case 'justify':
      return AlignmentType.JUSTIFIED;
    case 'left':
    default:
      return AlignmentType.LEFT;
  }
}

function mapHeading(tag) {
  switch (tag) {
    case 'h1':
      return HeadingLevel.HEADING_1;
    case 'h2':
      return HeadingLevel.HEADING_2;
    case 'h3':
      return HeadingLevel.HEADING_3;
    case 'h4':
      return HeadingLevel.HEADING_4;
    case 'h5':
      return HeadingLevel.HEADING_5;
    case 'h6':
      return HeadingLevel.HEADING_6;
    default:
      return undefined;
  }
}

function mapHighlight(color) {
  // docx HighlightColor is limited; fall back to YELLOW.
  if (!color) return undefined;
  const c = String(color).toLowerCase();
  if (c.includes('yellow')) return HighlightColor.YELLOW;
  if (c.includes('green')) return HighlightColor.GREEN;
  if (c.includes('cyan')) return HighlightColor.CYAN;
  if (c.includes('magenta') || c.includes('pink')) return HighlightColor.MAGENTA;
  if (c.includes('blue')) return HighlightColor.BLUE;
  if (c.includes('red')) return HighlightColor.RED;
  if (c.includes('gray') || c.includes('grey')) return HighlightColor.GRAY;
  if (c.includes('black')) return HighlightColor.BLACK;
  return HighlightColor.YELLOW;
}

function base64ToUint8Array(base64) {
  const b64 = base64.includes(',') ? base64.split(',')[1] : base64;
  const binary = atob(b64);
  const len = binary.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

function nodeTextRuns(node, inherited = {}) {
  if (!node) return [];
  const runs = [];

  if (node.type === 'text') {
    const styleFromFormat = lexicalFormatToTextStyle(node.format);
    const style = {
      ...inherited,
      ...styleFromFormat,
    };

    const color = cssColorToHex(node.style?.color || inherited.color);
    const highlight = mapHighlight(node.style?.backgroundColor || inherited.highlight);

    runs.push(
      new TextRun({
        text: node.text || '',
        bold: style.bold,
        italics: style.italics,
        underline: style.underline ? {} : undefined,
        strike: style.strike,
        font: node.style?.fontFamily || inherited.font,
        size: node.style?.fontSize ? Math.round(parseFloat(node.style.fontSize) * 2) : inherited.size,
        color,
        highlight,
      })
    );
    return runs;
  }

  if (node.type === 'link') {
    const url = node.url || node.fields?.url;
    const childRuns = [];
    for (const child of node.children || []) {
      childRuns.push(...nodeTextRuns(child, inherited));
    }
    if (url) {
      return [new ExternalHyperlink({ link: url, children: childRuns.length ? childRuns : [new TextRun(url)] })];
    }
    return childRuns;
  }

  if (node.type === 'linebreak') {
    runs.push(new TextRun({ text: '', break: 1 }));
    return runs;
  }

  if (node.type === 'image') {
    try {
      const src = node.src || node.data?.src || node.url;
      if (!src) return [];
      const data = base64ToUint8Array(src);
      const width = clamp(parseInt(node.width || 480, 10) || 480, 32, 1200);
      const height = clamp(parseInt(node.height || 320, 10) || 320, 32, 1200);
      return [
        new ImageRun({
          data,
          transformation: { width, height },
        }),
      ];
    } catch {
      return [];
    }
  }

  // Fallback: traverse children.
  for (const child of node.children || []) {
    runs.push(...nodeTextRuns(child, inherited));
  }
  return runs;
}

function paragraphFromNode(node, numbering, inheritedParagraph = {}) {
  const alignment = mapAlignment(node.format || inheritedParagraph.alignment);
  const heading = node.type === 'heading' ? mapHeading(node.tag) : undefined;
  const lineHeight = node.lineHeight || inheritedParagraph.lineHeight;

  const childrenRuns = [];
  for (const child of node.children || []) {
    // Lexical uses text nodes mostly; link/image handled above
    childrenRuns.push(...nodeTextRuns(child, inheritedParagraph.textStyle));
  }

  // Page break support: Lexical doesn't ship a default page-break node; handle common custom types.
  const isPageBreak = node.type === 'pagebreak' || node.type === 'page-break';
  if (isPageBreak) {
    return new Paragraph({ children: [new TextRun({ text: '', break: 1 })], pageBreakBefore: true });
  }

  const paraOpts = {
    children: childrenRuns.length ? childrenRuns : [new TextRun({ text: '' })],
    alignment,
    heading,
  };

  if (lineHeight) {
    // docx line spacing is in twentieths of a point; approximate.
    // If lineHeight is like 1.5, map to 240 * 1.5 (roughly 12pt default).
    const lh = parseFloat(lineHeight);
    if (!Number.isNaN(lh) && lh > 0) {
      paraOpts.spacing = { line: Math.round(240 * lh) };
    }
  }

  if (numbering) {
    paraOpts.numbering = numbering;
  }

  return new Paragraph(paraOpts);
}

function tableFromNode(node) {
  const rows = (node.children || []).filter((n) => n.type === 'tablerow' || n.type === 'table-row');
  const tableRows = rows.map((row) => {
    const cells = (row.children || []).filter((n) => n.type === 'tablecell' || n.type === 'table-cell');
    return new TableRow({
      children: cells.map((cell) => {
        const cellParas = [];
        for (const child of cell.children || []) {
          if (child.type === 'paragraph' || child.type === 'heading') {
            cellParas.push(paragraphFromNode(child));
          } else {
            // Wrap stray content in a paragraph
            cellParas.push(new Paragraph({ children: nodeTextRuns(child) }));
          }
        }
        return new TableCell({
          children: cellParas.length ? cellParas : [new Paragraph('')],
          margins: { top: 100, bottom: 100, left: 120, right: 120 },
        });
      }),
    });
  });

  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows: tableRows,
  });
}

function buildNumbering() {
  // Simple numbering config for bullets and decimal.
  return {
    config: [
      {
        reference: 'varnaakshara-bullets',
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: '•',
            alignment: AlignmentType.LEFT,
          },
          {
            level: 1,
            format: LevelFormat.BULLET,
            text: '◦',
            alignment: AlignmentType.LEFT,
          },
        ],
      },
      {
        reference: 'varnaakshara-numbering',
        levels: [
          {
            level: 0,
            format: LevelFormat.DECIMAL,
            text: '%1.',
            alignment: AlignmentType.LEFT,
          },
          {
            level: 1,
            format: LevelFormat.LOWER_LETTER,
            text: '%2)',
            alignment: AlignmentType.LEFT,
          },
        ],
      },
    ],
  };
}

function walkRootChildrenToBlocks(rootChildren) {
  const blocks = [];

  // Very small list handling: Lexical list nodes contain listitem children.
  for (const node of rootChildren || []) {
    if (node.type === 'paragraph' || node.type === 'heading' || node.type === 'quote') {
      blocks.push({ kind: 'paragraph', node });
      continue;
    }
    if (node.type === 'list') {
      const listType = node.listType || node.tag; // 'bullet' | 'number'
      const ref = listType === 'number' ? 'varnaakshara-numbering' : 'varnaakshara-bullets';
      const items = node.children || [];
      for (const item of items) {
        // listitem contains paragraphs
        if (item.type === 'listitem') {
          const pChildren = item.children || [];
          if (pChildren.length === 0) {
            blocks.push({ kind: 'paragraph', node: { type: 'paragraph', children: [] }, numbering: { reference: ref, level: item.indent || 0 } });
          }
          for (const child of pChildren) {
            blocks.push({ kind: 'paragraph', node: child.type ? child : { type: 'paragraph', children: [child] }, numbering: { reference: ref, level: item.indent || 0 } });
          }
        }
      }
      continue;
    }
    if (node.type === 'table') {
      blocks.push({ kind: 'table', node });
      continue;
    }
    if (node.type === 'image') {
      // stand-alone image -> paragraph with image run
      blocks.push({ kind: 'paragraph', node: { type: 'paragraph', children: [node] } });
      continue;
    }
    if (node.type === 'horizontalrule') {
      blocks.push({ kind: 'paragraph', node: { type: 'paragraph', children: [{ type: 'text', text: '──────────', format: 0 }] } });
      continue;
    }
    // Fallback: wrap unknown node content into paragraph
    blocks.push({ kind: 'paragraph', node: { type: 'paragraph', children: node.children || [] } });
  }

  return blocks;
}

/**
 * exportToDocx(editorState, metadata) -> Blob
 */
export async function exportToDocx(editorState, metadata = {}) {
  try {
    const json = typeof editorState?.toJSON === 'function' ? editorState.toJSON() : editorState;
    const rootChildren = json?.root?.children || [];

    const numbering = buildNumbering();
    const blocks = walkRootChildrenToBlocks(rootChildren);

    const docChildren = [];
    for (const b of blocks) {
      if (b.kind === 'table') {
        docChildren.push(tableFromNode(b.node));
      } else {
        docChildren.push(paragraphFromNode(b.node, b.numbering));
      }
    }

    const doc = new Document({
      creator: metadata.author || 'Varnaakshara Writer',
      title: metadata.title || 'Document',
      description: metadata.description || '',
      numbering,
      sections: [
        {
          properties: {},
          children: docChildren,
        },
      ],
    });

    const arrayBuffer = await Packer.toArrayBuffer(doc);
    return new Blob([arrayBuffer], {
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    });
  } catch (err) {
    console.error('[docxExport] export failed:', err);
    throw new Error('Failed to export DOCX.');
  }
}

