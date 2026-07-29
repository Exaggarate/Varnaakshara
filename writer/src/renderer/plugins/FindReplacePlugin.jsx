/**
 * FindReplacePlugin — Slide-down search bar with Ctrl+F / Ctrl+H support.
 * Highlights matches, navigates next/prev, supports replace/replace-all.
 */
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useLexicalComposerContext } from '@lexical/react/LexicalComposerContext';
import { $getRoot, $createTextNode, $getSelection, $isRangeSelection } from 'lexical';

export default function FindReplacePlugin({ isOpen, onClose }) {
  const [editor] = useLexicalComposerContext();
  const [findText, setFindText] = useState('');
  const [replaceText, setReplaceText] = useState('');
  const [matches, setMatches] = useState([]);
  const [currentMatch, setCurrentMatch] = useState(-1);
  const [showReplace, setShowReplace] = useState(false);
  const findInputRef = useRef(null);
  const highlightStyleId = useRef(null);

  // Focus find input when opened
  useEffect(() => {
    if (isOpen && findInputRef.current) {
      findInputRef.current.focus();
      findInputRef.current.select();
    }
    if (!isOpen) {
      clearHighlights();
      setFindText('');
      setReplaceText('');
      setMatches([]);
      setCurrentMatch(-1);
    }
  }, [isOpen]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        // This is handled by the parent via onOpen callback
      }
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  // Clear CSS-based highlights
  const clearHighlights = useCallback(() => {
    if (highlightStyleId.current) {
      const el = document.getElementById(highlightStyleId.current);
      if (el) el.remove();
      highlightStyleId.current = null;
    }
    // Remove highlight marks
    const root = editor.getRootElement();
    if (root) {
      const marks = root.querySelectorAll('mark[data-find-highlight]');
      marks.forEach((mark) => {
        const parent = mark.parentNode;
        while (mark.firstChild) {
          parent.insertBefore(mark.firstChild, mark);
        }
        parent.removeChild(mark);
        parent.normalize();
      });
    }
  }, [editor]);

  // Perform search — find all occurrences in DOM and highlight with <mark>
  const doSearch = useCallback((query) => {
    clearHighlights();
    if (!query) {
      setMatches([]);
      setCurrentMatch(-1);
      return;
    }

    const root = editor.getRootElement();
    if (!root) return;

    const treeWalker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    const textNodes = [];
    while (treeWalker.nextNode()) {
      textNodes.push(treeWalker.currentNode);
    }

    const found = [];
    const lowerQuery = query.toLowerCase();

    textNodes.forEach((textNode) => {
      const text = textNode.textContent;
      const lowerText = text.toLowerCase();
      let startIdx = 0;
      let idx;
      const splits = [];

      while ((idx = lowerText.indexOf(lowerQuery, startIdx)) !== -1) {
        splits.push({ start: idx, end: idx + query.length });
        startIdx = idx + 1;
      }

      if (splits.length === 0) return;

      // Split the text node and wrap matches in <mark>
      const parent = textNode.parentNode;
      if (!parent) return;

      const frag = document.createDocumentFragment();
      let lastEnd = 0;

      splits.forEach((s) => {
        // Text before match
        if (s.start > lastEnd) {
          frag.appendChild(document.createTextNode(text.slice(lastEnd, s.start)));
        }
        // The match
        const mark = document.createElement('mark');
        mark.setAttribute('data-find-highlight', 'true');
        mark.className = 'find-highlight';
        mark.textContent = text.slice(s.start, s.end);
        frag.appendChild(mark);
        found.push(mark);
        lastEnd = s.end;
      });

      // Text after last match
      if (lastEnd < text.length) {
        frag.appendChild(document.createTextNode(text.slice(lastEnd)));
      }

      parent.replaceChild(frag, textNode);
    });

    setMatches(found);
    if (found.length > 0) {
      setCurrentMatch(0);
      found[0].classList.add('find-highlight-active');
      found[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      setCurrentMatch(-1);
    }
  }, [editor, clearHighlights]);

  // Navigate matches
  const goToMatch = useCallback((index) => {
    if (matches.length === 0) return;
    // Remove active from old
    if (currentMatch >= 0 && currentMatch < matches.length) {
      matches[currentMatch].classList.remove('find-highlight-active');
    }
    const newIdx = ((index % matches.length) + matches.length) % matches.length;
    setCurrentMatch(newIdx);
    matches[newIdx].classList.add('find-highlight-active');
    matches[newIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [matches, currentMatch]);

  const findNext = useCallback(() => goToMatch(currentMatch + 1), [goToMatch, currentMatch]);
  const findPrev = useCallback(() => goToMatch(currentMatch - 1), [goToMatch, currentMatch]);

  // Replace current match
  const replaceCurrent = useCallback(() => {
    if (currentMatch < 0 || currentMatch >= matches.length) return;
    const mark = matches[currentMatch];
    if (!mark || !mark.parentNode) return;
    const textNode = document.createTextNode(replaceText);
    mark.parentNode.replaceChild(textNode, mark);
    textNode.parentNode.normalize();

    // Re-search to update matches list
    const newMatches = [...matches];
    newMatches.splice(currentMatch, 1);
    setMatches(newMatches);
    if (newMatches.length > 0) {
      const nextIdx = currentMatch >= newMatches.length ? 0 : currentMatch;
      setCurrentMatch(nextIdx);
      newMatches[nextIdx].classList.add('find-highlight-active');
      newMatches[nextIdx].scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
      setCurrentMatch(-1);
    }
  }, [matches, currentMatch, replaceText]);

  // Replace all
  const replaceAll = useCallback(() => {
    matches.forEach((mark) => {
      if (mark && mark.parentNode) {
        const textNode = document.createTextNode(replaceText);
        mark.parentNode.replaceChild(textNode, mark);
        textNode.parentNode.normalize();
      }
    });
    setMatches([]);
    setCurrentMatch(-1);
  }, [matches, replaceText]);

  // Handle find input changes
  const handleFindChange = useCallback((e) => {
    const v = e.target.value;
    setFindText(v);
    doSearch(v);
  }, [doSearch]);

  // Enter to find next
  const handleFindKeyDown = useCallback((e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (e.shiftKey) findPrev();
      else findNext();
    }
  }, [findNext, findPrev]);

  if (!isOpen) return null;

  return (
    <div className="find-replace-bar">
      <div className="find-replace-row">
        <input
          ref={findInputRef}
          type="text"
          className="find-replace-input"
          placeholder="Find…"
          value={findText}
          onChange={handleFindChange}
          onKeyDown={handleFindKeyDown}
        />
        <span className="find-replace-count">
          {matches.length > 0 ? `${currentMatch + 1}/${matches.length}` : findText ? '0 results' : ''}
        </span>
        <button className="find-replace-btn" onClick={findPrev} title="Previous (Shift+Enter)">▲</button>
        <button className="find-replace-btn" onClick={findNext} title="Next (Enter)">▼</button>
        <button
          className={`find-replace-btn ${showReplace ? 'active' : ''}`}
          onClick={() => setShowReplace((p) => !p)}
          title="Toggle Replace"
        >↔</button>
        <button className="find-replace-btn find-replace-close" onClick={onClose} title="Close (Esc)">✕</button>
      </div>
      {showReplace && (
        <div className="find-replace-row">
          <input
            type="text"
            className="find-replace-input"
            placeholder="Replace with…"
            value={replaceText}
            onChange={(e) => setReplaceText(e.target.value)}
          />
          <button className="find-replace-btn" onClick={replaceCurrent} title="Replace">Replace</button>
          <button className="find-replace-btn" onClick={replaceAll} title="Replace All">All</button>
        </div>
      )}
    </div>
  );
}
