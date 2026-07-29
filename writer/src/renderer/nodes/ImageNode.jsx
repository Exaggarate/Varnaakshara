/**
 * ImageNode — A Lexical DecoratorNode for inline images with resize handles.
 */
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { DecoratorNode, createCommand, $getNodeByKey } from 'lexical';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';

export const INSERT_IMAGE_COMMAND = createCommand('INSERT_IMAGE_COMMAND');

/* ── React component rendered inside the decorator ────────────────────────── */
function ImageComponent({ src, altText, width, height, nodeKey }) {
  const [editor] = useLexicalComposerContext();
  const imgRef = useRef(null);
  const [isSelected, setIsSelected] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [dims, setDims] = useState({ w: width || 'auto', h: height || 'auto' });

  // Click to select
  const handleClick = useCallback((e) => {
    e.stopPropagation();
    setIsSelected(true);
  }, []);

  // Deselect on outside click
  useEffect(() => {
    const deselect = (e) => {
      if (imgRef.current && !imgRef.current.contains(e.target)) {
        setIsSelected(false);
      }
    };
    document.addEventListener('mousedown', deselect);
    return () => document.removeEventListener('mousedown', deselect);
  }, []);

  // Delete key removes selected image
  useEffect(() => {
    if (!isSelected) return;
    const handleKey = (e) => {
      if (e.key === 'Delete' || e.key === 'Backspace') {
        e.preventDefault();
        editor.update(() => {
          const node = $getNodeByKey(nodeKey);
          if (node) node.remove();
        });
      }
    };
    document.addEventListener('keydown', handleKey);
    return () => document.removeEventListener('keydown', handleKey);
  }, [isSelected, editor, nodeKey]);

  // Resize via corner drag
  const onResizeStart = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsResizing(true);
    const startX = e.clientX;
    const startW = imgRef.current ? imgRef.current.querySelector('img').offsetWidth : 200;
    const aspect = imgRef.current ? imgRef.current.querySelector('img').naturalHeight / imgRef.current.querySelector('img').naturalWidth : 1;

    const onMove = (ev) => {
      const delta = ev.clientX - startX;
      const newW = Math.max(50, startW + delta);
      const newH = Math.round(newW * aspect);
      setDims({ w: newW, h: newH });
    };
    const onUp = () => {
      setIsResizing(false);
      document.removeEventListener('mousemove', onMove);
      document.removeEventListener('mouseup', onUp);
      // Persist new size into the node
      editor.update(() => {
        const node = $getNodeByKey(nodeKey);
        if (node) {
          const el = imgRef.current ? imgRef.current.querySelector('img') : null;
          if (el) {
            node.__width = el.offsetWidth;
            node.__height = el.offsetHeight;
          }
        }
      });
    };
    document.addEventListener('mousemove', onMove);
    document.addEventListener('mouseup', onUp);
  }, [editor, nodeKey]);

  const style = {
    width: typeof dims.w === 'number' ? dims.w + 'px' : dims.w,
    height: typeof dims.h === 'number' ? dims.h + 'px' : dims.h,
    maxWidth: '100%',
    display: 'block',
  };

  return (
    <span
      ref={imgRef}
      onClick={handleClick}
      className={`editor-image-wrapper ${isSelected ? 'selected' : ''}`}
      style={{ position: 'relative', display: 'inline-block', cursor: 'default' }}
    >
      <img src={src} alt={altText} style={style} draggable={false} />
      {isSelected && (
        <>
          <span className="img-resize-handle corner-se" onMouseDown={onResizeStart} />
        </>
      )}
    </span>
  );
}

/* ── Lexical Node ─────────────────────────────────────────────────────────── */
export class ImageNode extends DecoratorNode {
  __src;
  __altText;
  __width;
  __height;

  static getType() {
    return 'image';
  }

  static clone(node) {
    return new ImageNode(node.__src, node.__altText, node.__width, node.__height, node.__key);
  }

  constructor(src, altText, width, height, key) {
    super(key);
    this.__src = src;
    this.__altText = altText || '';
    this.__width = width || undefined;
    this.__height = height || undefined;
  }

  createDOM() {
    const span = document.createElement('span');
    span.style.display = 'inline-block';
    return span;
  }

  updateDOM() {
    return false;
  }

  decorate() {
    return (
      <ImageComponent
        src={this.__src}
        altText={this.__altText}
        width={this.__width}
        height={this.__height}
        nodeKey={this.__key}
      />
    );
  }

  static importJSON(serializedNode) {
    return $createImageNode({
      src: serializedNode.src,
      altText: serializedNode.altText,
      width: serializedNode.width,
      height: serializedNode.height,
    });
  }

  exportJSON() {
    return {
      type: 'image',
      version: 1,
      src: this.__src,
      altText: this.__altText,
      width: this.__width,
      height: this.__height,
    };
  }

  isInline() {
    return true;
  }
}

export function $createImageNode({ src, altText, width, height }) {
  return new ImageNode(src, altText, width, height);
}

export function $isImageNode(node) {
  return node instanceof ImageNode;
}
