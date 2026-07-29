/**
 * Varnaakshara Writer — PDF Export (Renderer)
 *
 * Uses html2canvas + jsPDF to render the editor DOM to a PDF Blob.
 * For highest fidelity (and proper Indic font shaping), prefer Electron's
 * main-process printToPDF path when available.
 */

import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

function normalizePageSize(pageSize) {
  const ps = String(pageSize || 'a4').toLowerCase();
  if (ps === 'letter') return 'letter';
  return 'a4';
}

/**
 * exportToPDF(editorElement, options) -> Blob
 * options: { pageSize, orientation, margins, quality }
 */
export async function exportToPDF(editorElement, options = {}) {
  try {
    if (!editorElement) throw new Error('No editor element');

    const pageSize = normalizePageSize(options.pageSize);
    const orientation = (options.orientation || 'portrait').toLowerCase() === 'landscape' ? 'landscape' : 'portrait';
    const margins = {
      top: options.margins?.top ?? 12,
      right: options.margins?.right ?? 12,
      bottom: options.margins?.bottom ?? 12,
      left: options.margins?.left ?? 12,
    };
    const quality = Math.max(0.5, Math.min(2.0, options.quality ?? 1.5));

    // Render at higher scale for readability.
    const canvas = await html2canvas(editorElement, {
      scale: quality,
      useCORS: true,
      backgroundColor: '#ffffff',
      logging: false,
    });

    const pdf = new jsPDF({
      orientation,
      unit: 'mm',
      format: pageSize,
      compress: true,
    });

    const pageWidth = pdf.internal.pageSize.getWidth();
    const pageHeight = pdf.internal.pageSize.getHeight();

    const imgData = canvas.toDataURL('image/png');
    const imgWidth = pageWidth - margins.left - margins.right;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    let y = margins.top;
    let remaining = imgHeight;
    let position = 0;

    // First page
    pdf.addImage(imgData, 'PNG', margins.left, y, imgWidth, imgHeight);
    remaining -= pageHeight - margins.top - margins.bottom;
    position = -(pageHeight - margins.top - margins.bottom);

    while (remaining > 0) {
      pdf.addPage();
      pdf.addImage(imgData, 'PNG', margins.left, margins.top + position, imgWidth, imgHeight);
      remaining -= pageHeight - margins.top - margins.bottom;
      position -= pageHeight - margins.top - margins.bottom;
    }

    const arrayBuffer = pdf.output('arraybuffer');
    return new Blob([arrayBuffer], { type: 'application/pdf' });
  } catch (err) {
    console.error('[pdfExport] export failed:', err);
    throw new Error('Failed to export PDF.');
  }
}

