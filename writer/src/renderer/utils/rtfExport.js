/**
 * Varnaakshara Writer — RTF Export
 *
 * Basic RTF generator from Lexical editor state JSON.
 * Supports: bold/italic/underline, font family/size, alignment.
 *
 * This is intended for legacy workflows; it is not a full RTF implementation.
 */

function escRtf(text) {
  return String(text || '')
    .replace(/\\/g, '\\\\')
    .replace(/{/g, '\\{')
    .replace(/}/g, '\\}')
    .replace(/\n/g, '\\par\n');
}

function lexicalFormat(formatBitmask) {
  const f = Number(formatBitmask || 0);
  return {
    b: (f & 1) !== 0,
    i: (f & 2) !== 0,
    u: (f & 4) !== 0,
    strike: (f & 8) !== 0,
  };
}

function alignCtrl(format) {
  switch (format) {
    case 'center':
      return '\\qc';
    case 'right':
      return '\\qr';
    case 'justify':
      return '\\qj';
    case 'left':
    default:
      return '\\ql';
  }
}

function runsFromNode(node, fontTbl) {
  if (!node) return '';
  if (node.type === 'text') {
    const fmt = lexicalFormat(node.format);
    const font = node.style?.fontFamily;
    const fontSizePt = node.style?.fontSize ? parseFloat(node.style.fontSize) : null;
    let fontIndex = 0;
    if (font) {
      if (!fontTbl.map.has(font)) {
        const idx = fontTbl.list.length;
        fontTbl.map.set(font, idx);
        fontTbl.list.push(font);
      }
      fontIndex = fontTbl.map.get(font);
    }
    const sizeHalfPoints = fontSizePt ? Math.round(fontSizePt * 2) : null;

    const ctrl = [
      fmt.b ? '\\b' : '\\b0',
      fmt.i ? '\\i' : '\\i0',
      fmt.u ? '\\ul' : '\\ul0',
      `\\f${fontIndex}`,
      sizeHalfPoints ? `\\fs${sizeHalfPoints}` : '',
    ].filter(Boolean);

    return `${ctrl.join(' ')} ${escRtf(node.text)}`;
  }
  if (node.type === 'linebreak') {
    return '\\line\n';
  }
  // Ignore images/tables/links for basic RTF.
  let out = '';
  for (const c of node.children || []) out += runsFromNode(c, fontTbl);
  return out;
}

/**
 * exportToRTF(editorState) -> string
 */
export async function exportToRTF(editorState) {
  try {
    const json = typeof editorState?.toJSON === 'function' ? editorState.toJSON() : editorState;
    const rootChildren = json?.root?.children || [];

    const fontTbl = { map: new Map(), list: ['Noto Serif'] };
    fontTbl.map.set('Noto Serif', 0);

    let body = '';
    for (const node of rootChildren) {
      if (node.type === 'paragraph' || node.type === 'heading' || node.type === 'quote') {
        body += `{${alignCtrl(node.format)} ${runsFromNode(node, fontTbl)}\\par}\n`;
      } else if (node.type === 'list') {
        for (const item of node.children || []) {
          body += `{\\ql \\bullet\tab ${runsFromNode(item, fontTbl)}\\par}\n`;
        }
      } else {
        body += `{\\ql ${runsFromNode(node, fontTbl)}\\par}\n`;
      }
    }

    const fontTableRtf = fontTbl.list
      .map((f, i) => `{\\f${i} ${escRtf(f)};}`)
      .join('');

    // \uc1 for unicode, \uN? escapes are not needed if consumer supports UTF-8 RTF;
    // Electron will save as UTF-8.
    return `{\\rtf1\\ansi\\deff0{\\fonttbl${fontTableRtf}}\\viewkind4\\uc1\n${body}}`;
  } catch (err) {
    console.error('[rtfExport] export failed:', err);
    throw new Error('Failed to export RTF.');
  }
}

