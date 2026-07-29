/**
 * PanelsSidebar — InDesign-style tabbed panel system.
 *
 * Layout:
 *   ┌──────────────────────────────┐
 *   │  [◀ Panels ▶] toggle        │
 *   ├──────────────────────────────┤
 *   │                              │
 *   │   Active Panel Content       │
 *   │   (scrollable)               │
 *   │                              │
 *   ├──────────────────────────────┤
 *   │  📄  🔤  ¶  🎨  🔠  अ      │  ← icon tab strip
 *   └──────────────────────────────┘
 */
import React, { useState, useCallback } from 'react';
import PagesPanel from './panels/PagesPanel';
import GlyphsPanel from './panels/GlyphsPanel';
import StylesPanel from './panels/StylesPanel';
import SwatchesPanel from './panels/SwatchesPanel';

const { ipcRenderer } = window.require ? window.require('electron') : { ipcRenderer: null };

/* ── Panel Definitions ────────────────────────────────────────────────────── */
const PANELS = [
  { id: 'pages',           icon: '📄', fallback: 'Pg', label: 'Pages' },
  { id: 'glyphs',          icon: '🔤', fallback: 'Gl', label: 'Glyphs' },
  { id: 'styles',          icon: '¶',  fallback: '¶',  label: 'Styles' },
  { id: 'swatches',        icon: '🎨', fallback: 'Sw', label: 'Swatches' },
  { id: 'languages',       icon: '🔠', fallback: 'La', label: 'Languages' },
  { id: 'transliteration', icon: 'अ',  fallback: 'अ',  label: 'Transliteration' },
];

/* ── Languages Data ───────────────────────────────────────────────────────── */
const LANGUAGES = [
  { code: 'kan', label: 'ಕನ್ನಡ', name: 'Kannada' },
  { code: 'hin', label: 'हिन्दी', name: 'Hindi' },
  { code: 'tel', label: 'తెలుగు', name: 'Telugu' },
  { code: 'tam', label: 'தமிழ்', name: 'Tamil' },
  { code: 'mal', label: 'മലയാളം', name: 'Malayalam' },
  { code: 'mar', label: 'मराठी', name: 'Marathi' },
  { code: 'san', label: 'संस्कृतम्', name: 'Sanskrit' },
  { code: 'ben', label: 'বাংলা', name: 'Bengali' },
  { code: 'asm', label: 'অসমীয়া', name: 'Assamese' },
  { code: 'guj', label: 'ગુજરાતી', name: 'Gujarati' },
  { code: 'pan', label: 'ਪੰਜਾਬੀ', name: 'Punjabi' },
  { code: 'ori', label: 'ଓଡ଼ିଆ', name: 'Odia' },
];

const INPUT_SCHEMES = [
  { value: 'baraha', label: 'Baraha' },
  { value: 'itrans', label: 'ITRANS' },
  { value: 'inscript', label: 'INSCRIPT' },
];

const OUTPUT_MODES = [
  { value: 'unicode', label: 'Unicode' },
  { value: 'ansi', label: 'ANSI (Baraha)' },
];

/* ── Transliteration Data ─────────────────────────────────────────────────── */
const TRANSLIT_LANGUAGES = [
  { value: 'kannada', label: 'ಕನ್ನಡ (Kannada)' },
  { value: 'devanagari', label: 'देवनागरी (Hindi)' },
  { value: 'telugu', label: 'తెలుగు (Telugu)' },
  { value: 'tamil', label: 'தமிழ் (Tamil)' },
  { value: 'malayalam', label: 'മലയാളം (Malayalam)' },
  { value: 'bengali', label: 'বাংলা (Bengali)' },
  { value: 'gujarati', label: 'ગુજરાતી (Gujarati)' },
  { value: 'gurmukhi', label: 'ਗੁਰਮੁਖੀ (Punjabi)' },
  { value: 'oriya', label: 'ଓଡ଼ିଆ (Odia)' },
];

const TRANSLIT_SCHEMES = [
  { value: 'baraha', label: 'Baraha' },
  { value: 'itrans', label: 'ITRANS' },
  { value: 'harvard-kyoto', label: 'Harvard-Kyoto' },
  { value: 'iast', label: 'IAST' },
];

const ANSI_FONTS = [
  { value: 'nudi', label: 'Nudi' },
  { value: 'baraha', label: 'Baraha' },
  { value: 'anu', label: 'Anu' },
  { value: 'shree', label: 'Shree' },
];

const TRANSLIT_MODES = [
  { value: 'transliterate', label: 'Transliterate' },
  { value: 'convert-script', label: 'Script Converter' },
  { value: 'unicode-ansi', label: 'Unicode ↔ ANSI' },
  { value: 'panchama-varga', label: 'Panchama Varga' },
];

/* ── Bridge helper ────────────────────────────────────────────────────────── */
async function bridgeRequest(endpoint, data) {
  if (!ipcRenderer) return { success: false, error: 'Not in Electron' };
  return ipcRenderer.invoke('bridge-request', { endpoint, data });
}

/* ── Collapsible Section ──────────────────────────────────────────────────── */
function PanelSection({ title, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className="panel">
      <div className="panel-header" onClick={() => setOpen(!open)}>
        <span className="panel-header-title">{title}</span>
        <span className={`panel-header-icon ${open ? '' : 'collapsed'}`}>▾</span>
      </div>
      <div className={`panel-body ${open ? '' : 'collapsed'}`}>{children}</div>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════════
   Languages Panel Content
   ═══════════════════════════════════════════════════════════════════════════ */
function LanguagesContent({ activeLang, onLangChange }) {
  const [inputScheme, setInputScheme] = useState('baraha');
  const [outputMode, setOutputMode] = useState('unicode');

  return (
    <div className="panel-languages">
      <PanelSection title="Active Language" defaultOpen={true}>
        <div className="lang-grid">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              className={`lang-btn ${activeLang === lang.code ? 'active' : ''}`}
              onClick={() => onLangChange && onLangChange(lang.code)}
              title={lang.name}
            >
              {lang.label}
            </button>
          ))}
        </div>
      </PanelSection>

      <PanelSection title="Input Scheme" defaultOpen={true}>
        <div className="panel-row">
          <select
            className="panel-select"
            value={inputScheme}
            onChange={(e) => setInputScheme(e.target.value)}
            style={{ flex: 1 }}
          >
            {INPUT_SCHEMES.map((s) => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>
        </div>
        <div className="panel-row" style={{ marginTop: 4 }}>
          <span className="panel-label" style={{ fontSize: 10, opacity: 0.7, minWidth: 0 }}>
            Phonetic input scheme for typing Indian languages
          </span>
        </div>
      </PanelSection>

      <PanelSection title="Output Mode" defaultOpen={true}>
        <div className="panel-row">
          <select
            className="panel-select"
            value={outputMode}
            onChange={(e) => setOutputMode(e.target.value)}
            style={{ flex: 1 }}
          >
            {OUTPUT_MODES.map((m) => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>
        </div>
      </PanelSection>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════════
   Transliteration Panel Content
   ═══════════════════════════════════════════════════════════════════════════ */
function TransliterationContent() {
  const [mode, setMode] = useState('transliterate');
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Mode-specific state
  const [language, setLanguage] = useState('kannada');
  const [scheme, setScheme] = useState('baraha');
  const [fromLang, setFromLang] = useState('kannada');
  const [toLang, setToLang] = useState('devanagari');
  const [ansiDir, setAnsiDir] = useState('to-ansi');
  const [ansiFont, setAnsiFont] = useState('nudi');

  const handleConvert = useCallback(async () => {
    if (!inputText.trim()) return;
    setIsLoading(true);
    setError('');
    setOutputText('');
    try {
      let result;
      switch (mode) {
        case 'transliterate':
          result = await bridgeRequest('/transliterate', { text: inputText, language, scheme });
          break;
        case 'convert-script':
          result = await bridgeRequest('/convert-script', { text: inputText, from_lang: fromLang, to_lang: toLang });
          break;
        case 'unicode-ansi':
          result = await bridgeRequest(
            ansiDir === 'to-ansi' ? '/to-ansi' : '/from-ansi',
            { text: inputText, language, font_family: ansiFont },
          );
          break;
        case 'panchama-varga':
          result = await bridgeRequest('/transliterate', { text: inputText, language, scheme: 'panchama-varga' });
          break;
        default:
          setError('Unknown mode');
          return;
      }
      if (result && result.success && result.data?.result) {
        setOutputText(typeof result.data.result === 'string' ? result.data.result : JSON.stringify(result.data.result, null, 2));
      } else {
        setError(result?.error || result?.data?.error || 'Conversion failed');
      }
    } catch (err) {
      setError(err.message || 'Error');
    } finally {
      setIsLoading(false);
    }
  }, [inputText, mode, language, scheme, fromLang, toLang, ansiDir, ansiFont]);

  const handleSwap = useCallback(() => {
    setInputText(outputText);
    setOutputText(inputText);
  }, [inputText, outputText]);

  const handleCopy = useCallback(() => {
    if (outputText) navigator.clipboard.writeText(outputText);
  }, [outputText]);

  const handleInsert = useCallback(() => {
    if (outputText) {
      window.dispatchEvent(
        new CustomEvent('varnaakshara-insert-text', { detail: { text: outputText } }),
      );
    }
  }, [outputText]);

  return (
    <div className="panel-transliteration">
      {/* Mode selector */}
      <PanelSection title="Tool" defaultOpen={true}>
        <div className="panel-row">
          <select className="panel-select" value={mode} onChange={(e) => setMode(e.target.value)} style={{ flex: 1 }}>
            {TRANSLIT_MODES.map((m) => <option key={m.value} value={m.value}>{m.label}</option>)}
          </select>
        </div>
      </PanelSection>

      {/* Mode-specific options */}
      <PanelSection title="Options" defaultOpen={true}>
        {mode === 'transliterate' && (
          <>
            <div className="panel-row">
              <span className="panel-label">Lang</span>
              <select className="panel-select" value={language} onChange={(e) => setLanguage(e.target.value)}>
                {TRANSLIT_LANGUAGES.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
              </select>
            </div>
            <div className="panel-row">
              <span className="panel-label">Scheme</span>
              <select className="panel-select" value={scheme} onChange={(e) => setScheme(e.target.value)}>
                {TRANSLIT_SCHEMES.map((s) => <option key={s.value} value={s.value}>{s.label}</option>)}
              </select>
            </div>
          </>
        )}
        {mode === 'convert-script' && (
          <>
            <div className="panel-row">
              <span className="panel-label">From</span>
              <select className="panel-select" value={fromLang} onChange={(e) => setFromLang(e.target.value)}>
                {TRANSLIT_LANGUAGES.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
              </select>
            </div>
            <div className="panel-row">
              <span className="panel-label">To</span>
              <select className="panel-select" value={toLang} onChange={(e) => setToLang(e.target.value)}>
                {TRANSLIT_LANGUAGES.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
              </select>
            </div>
          </>
        )}
        {mode === 'unicode-ansi' && (
          <>
            <div className="panel-row">
              <span className="panel-label">Dir</span>
              <select className="panel-select" value={ansiDir} onChange={(e) => setAnsiDir(e.target.value)}>
                <option value="to-ansi">Unicode → ANSI</option>
                <option value="from-ansi">ANSI → Unicode</option>
              </select>
            </div>
            <div className="panel-row">
              <span className="panel-label">Lang</span>
              <select className="panel-select" value={language} onChange={(e) => setLanguage(e.target.value)}>
                {TRANSLIT_LANGUAGES.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
              </select>
            </div>
            <div className="panel-row">
              <span className="panel-label">Font</span>
              <select className="panel-select" value={ansiFont} onChange={(e) => setAnsiFont(e.target.value)}>
                {ANSI_FONTS.map((f) => <option key={f.value} value={f.value}>{f.label}</option>)}
              </select>
            </div>
          </>
        )}
        {mode === 'panchama-varga' && (
          <div className="panel-row">
            <span className="panel-label">Lang</span>
            <select className="panel-select" value={language} onChange={(e) => setLanguage(e.target.value)}>
              {TRANSLIT_LANGUAGES.map((l) => <option key={l.value} value={l.value}>{l.label}</option>)}
            </select>
          </div>
        )}
      </PanelSection>

      {/* Input / Output */}
      <PanelSection title="Convert" defaultOpen={true}>
        <div className="panel-row">
          <textarea
            className="panel-textarea"
            placeholder="Type or paste text…"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            rows={3}
          />
        </div>
        <div className="panel-row" style={{ justifyContent: 'flex-end', gap: 4 }}>
          <button className="panel-btn" onClick={handleSwap} title="Swap">⇅</button>
          <button
            className="panel-btn primary"
            onClick={handleConvert}
            disabled={isLoading || !inputText.trim()}
          >
            {isLoading ? '…' : 'Convert'}
          </button>
        </div>

        {error && (
          <div style={{
            padding: '4px 8px', marginBottom: 6, background: '#4a2020',
            border: '1px solid #6a3030', borderRadius: 3, color: '#ff8888', fontSize: 10,
          }}>
            ⚠ {error}
          </div>
        )}

        <div className="panel-row">
          <textarea
            className="panel-textarea"
            placeholder="Output…"
            readOnly
            value={outputText}
            rows={3}
          />
        </div>

        {outputText && (
          <div className="panel-row" style={{ gap: 4 }}>
            <button className="panel-btn" onClick={handleCopy} style={{ flex: 1 }}>📋 Copy</button>
            <button className="panel-btn primary" onClick={handleInsert} style={{ flex: 1 }}>Insert ↵</button>
          </div>
        )}

        {mode === 'panchama-varga' && (
          <div className="panel-row" style={{ marginTop: 4 }}>
            <span className="panel-label" style={{ fontSize: 10, opacity: 0.6, minWidth: 0 }}>
              Replaces anusvara with appropriate nasal consonant based on following consonant class
            </span>
          </div>
        )}
      </PanelSection>
    </div>
  );
}

/* ═══════════════════════════════════════════════════════════════════════════
   Main PanelsSidebar Component
   ═══════════════════════════════════════════════════════════════════════════ */
export default function PanelsSidebar({ collapsed, onToggle, activeLang, onLangChange, onInsertText }) {
  const [activePanel, setActivePanel] = useState('languages');

  const renderPanel = () => {
    switch (activePanel) {
      case 'pages':
        return <PagesPanel />;
      case 'glyphs':
        return <GlyphsPanel onInsertText={onInsertText} />;
      case 'styles':
        return <StylesPanel />;
      case 'swatches':
        return <SwatchesPanel />;
      case 'languages':
        return <LanguagesContent activeLang={activeLang} onLangChange={onLangChange} />;
      case 'transliteration':
        return <TransliterationContent />;
      default:
        return null;
    }
  };

  return (
    <div className={`panels-container ${collapsed ? 'collapsed' : ''}`}>
      {/* Toggle bar */}
      <div className="panel-toggle-bar" onClick={onToggle}>
        <span className="toggle-label">{collapsed ? '◀' : 'Panels'}</span>
        <span className="toggle-icon">{collapsed ? '◀' : '▶'}</span>
      </div>

      {!collapsed && (
        <>
          {/* Panel title */}
          <div className="panels-active-title">
            {PANELS.find((p) => p.id === activePanel)?.label || 'Panel'}
          </div>

          {/* Scrollable panel content */}
          <div className="panels-content">{renderPanel()}</div>

          {/* Icon tab strip at bottom */}
          <div className="panels-tab-strip">
            {PANELS.map((p) => (
              <button
                key={p.id}
                className={`panels-tab-icon ${activePanel === p.id ? 'active' : ''}`}
                onClick={() => setActivePanel(p.id)}
                title={p.label}
                data-label={p.fallback}
              >
                <span className="tab-icon-emoji">{p.icon}</span>
                <span className="tab-icon-fallback">{p.fallback}</span>
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
