import React, { useState, useEffect, useCallback } from 'react';
import Editor from './Editor';
import TitleBar from './TitleBar';
import RibbonTabs from './RibbonTabs';
import PanelsSidebar from './PanelsSidebar';

const { ipcRenderer } = window.require ? window.require('electron') : { ipcRenderer: null };

const DEFAULT_PAGE_SETUP = {
  orientation: 'portrait',
  pageWidth: 816,     // US Letter width at 96 dpi
  pageHeight: 1056,   // US Letter height at 96 dpi
  margin: 96,         // 1 inch
  columns: 1,
  spacingBefore: 0,
  spacingAfter: 8,
};

export default function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [zoom, setZoom] = useState(1.0);
  const [activeTab, setActiveTab] = useState('Home');
  const [panelsCollapsed, setPanelsCollapsed] = useState(false);
  const [focusMode, setFocusMode] = useState(false);
  const [activeLang, setActiveLang] = useState('kan');
  const [filename, setFilename] = useState('Untitled');
  const [dirty, setDirty] = useState(false);
  const [pageSetup, setPageSetup] = useState(DEFAULT_PAGE_SETUP);

  // Listen for main process commands
  useEffect(() => {
    if (!ipcRenderer) return;

    const handlers = {
      'set-dark-mode': (_e, val) => setDarkMode(val),
      'set-zoom': (_e, val) => setZoom(val),
      'set-filename': (_e, val) => setFilename(val || 'Untitled'),
      'set-dirty': (_e, val) => setDirty(val),
      'tools-transliterate': () => { setActiveTab('Tools'); setPanelsCollapsed(false); },
      'tools-convert-script': () => { setActiveTab('Tools'); setPanelsCollapsed(false); },
      'tools-unicode-ansi': () => { setActiveTab('Tools'); setPanelsCollapsed(false); },
      'tools-panchama-varga': () => { setActiveTab('Tools'); setPanelsCollapsed(false); },
    };

    Object.entries(handlers).forEach(([channel, handler]) => {
      ipcRenderer.on(channel, handler);
    });

    return () => {
      Object.entries(handlers).forEach(([channel, handler]) => {
        ipcRenderer.removeListener(channel, handler);
      });
    };
  }, []);

  // Apply theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', darkMode ? 'dark' : 'light');
  }, [darkMode]);

  // F11 focus mode toggle
  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === 'F11') {
        e.preventDefault();
        setFocusMode((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  const handleOpenPanel = useCallback((panelMode) => {
    setPanelsCollapsed(false);
  }, []);

  const handleInsertText = useCallback((text) => {
    window.dispatchEvent(
      new CustomEvent('varnaakshara-insert-text', { detail: { text } }),
    );
  }, []);

  const handlePageSetupChange = useCallback((updates) => {
    setPageSetup((prev) => ({ ...prev, ...updates }));
  }, []);

  return (
    <div className={`app-container ${focusMode ? 'focus-mode' : ''}`}>
      <TitleBar filename={filename} dirty={dirty} />
      <RibbonTabs activeTab={activeTab} onTabChange={setActiveTab} />

      <div className="app-main">
        <Editor
          zoom={zoom}
          activeTab={activeTab}
          onOpenPanel={handleOpenPanel}
          pageSetup={pageSetup}
          onPageSetupChange={handlePageSetupChange}
        />
        <PanelsSidebar
          collapsed={panelsCollapsed}
          onToggle={() => setPanelsCollapsed((c) => !c)}
          activeLang={activeLang}
          onLangChange={setActiveLang}
          onInsertText={handleInsertText}
        />
      </div>
    </div>
  );
}
