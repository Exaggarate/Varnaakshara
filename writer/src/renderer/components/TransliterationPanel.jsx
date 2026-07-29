import React, { useState, useCallback } from 'react';

const { ipcRenderer } = window.require ? window.require('electron') : { ipcRenderer: null };

// ── Language Options ─────────────────────────────────────────────────────────
const LANGUAGES = [
  { value: 'kannada', label: 'ಕನ್ನಡ (Kannada)' },
  { value: 'devanagari', label: 'देवनागरी (Devanagari / Hindi)' },
  { value: 'telugu', label: 'తెలుగు (Telugu)' },
  { value: 'tamil', label: 'தமிழ் (Tamil)' },
  { value: 'malayalam', label: 'മലയാളം (Malayalam)' },
  { value: 'bengali', label: 'বাংলা (Bengali)' },
  { value: 'gujarati', label: 'ગુજરાતી (Gujarati)' },
  { value: 'gurmukhi', label: 'ਗੁਰਮੁਖੀ (Gurmukhi / Punjabi)' },
  { value: 'oriya', label: 'ଓଡ଼ିଆ (Odia)' },
];

const TRANSLITERATION_SCHEMES = [
  { value: 'baraha', label: 'Baraha' },
  { value: 'itrans', label: 'ITRANS' },
  { value: 'harvard-kyoto', label: 'Harvard-Kyoto' },
  { value: 'iast', label: 'IAST' },
  { value: 'slp1', label: 'SLP1' },
];

const ANSI_FONT_FAMILIES = [
  { value: 'nudi', label: 'Nudi' },
  { value: 'baraha', label: 'Baraha' },
  { value: 'anu', label: 'Anu' },
  { value: 'shree', label: 'Shree' },
  { value: 'akruti', label: 'Akruti' },
];

// ── Bridge Request Helper ────────────────────────────────────────────────────
async function bridgeRequest(endpoint, data) {
  if (!ipcRenderer) {
    console.warn('IPC not available — running outside Electron');
    return { success: false, error: 'Not running in Electron' };
  }
  return ipcRenderer.invoke('bridge-request', { endpoint, data });
}

// ── Panel Modes ──────────────────────────────────────────────────────────────
const MODES = [
  { value: 'transliterate', label: 'Transliterate' },
  { value: 'convert-script', label: 'Convert Script' },
  { value: 'unicode-ansi', label: 'Unicode ↔ ANSI' },
  { value: 'panchama-varga', label: 'Panchama Varga' },
  { value: 'iso15919', label: 'ISO 15919' },
];

// ── Main Component ───────────────────────────────────────────────────────────
export default function TransliterationPanel({ mode, onModeChange, onClose }) {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Transliterate mode state
  const [language, setLanguage] = useState('kannada');
  const [scheme, setScheme] = useState('baraha');

  // Convert script mode state
  const [fromLang, setFromLang] = useState('kannada');
  const [toLang, setToLang] = useState('devanagari');

  // ANSI mode state
  const [ansiDirection, setAnsiDirection] = useState('to-ansi');
  const [ansiFont, setAnsiFont] = useState('nudi');

  // ── Execute Conversion ─────────────────────────────────────────────────
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
            ansiDirection === 'to-ansi' ? '/to-ansi' : '/from-ansi',
            { text: inputText, language, font_family: ansiFont }
          );
          break;

        case 'panchama-varga':
          // Panchama varga conversion uses the transliteration engine
          result = await bridgeRequest('/transliterate', {
            text: inputText,
            language,
            scheme: 'panchama-varga',
          });
          break;

        case 'iso15919':
          result = await bridgeRequest('/to-iso15919', { text: inputText, language });
          break;

        default:
          setError('Unknown mode');
          return;
      }

      if (result.success && result.data?.result) {
        setOutputText(typeof result.data.result === 'string' ? result.data.result : JSON.stringify(result.data.result, null, 2));
      } else {
        setError(result.error || result.data?.error || 'Conversion failed');
      }
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  }, [inputText, mode, language, scheme, fromLang, toLang, ansiDirection, ansiFont]);

  // ── Copy to Clipboard ──────────────────────────────────────────────────
  const handleCopy = useCallback(() => {
    if (outputText) {
      navigator.clipboard.writeText(outputText);
    }
  }, [outputText]);

  // ── Swap Input/Output ──────────────────────────────────────────────────
  const handleSwap = useCallback(() => {
    setInputText(outputText);
    setOutputText(inputText);
  }, [inputText, outputText]);

  // ── Render Mode-Specific Options ───────────────────────────────────────
  const renderOptions = () => {
    switch (mode) {
      case 'transliterate':
        return (
          <>
            <div className="form-group">
              <label>Target Language</label>
              <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                {LANGUAGES.map((l) => (
                  <option key={l.value} value={l.value}>{l.label}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Input Scheme</label>
              <select value={scheme} onChange={(e) => setScheme(e.target.value)}>
                {TRANSLITERATION_SCHEMES.map((s) => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>
          </>
        );

      case 'convert-script':
        return (
          <>
            <div className="form-group">
              <label>From Script</label>
              <select value={fromLang} onChange={(e) => setFromLang(e.target.value)}>
                {LANGUAGES.map((l) => (
                  <option key={l.value} value={l.value}>{l.label}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>To Script</label>
              <select value={toLang} onChange={(e) => setToLang(e.target.value)}>
                {LANGUAGES.map((l) => (
                  <option key={l.value} value={l.value}>{l.label}</option>
                ))}
              </select>
            </div>
          </>
        );

      case 'unicode-ansi':
        return (
          <>
            <div className="form-group">
              <label>Direction</label>
              <select value={ansiDirection} onChange={(e) => setAnsiDirection(e.target.value)}>
                <option value="to-ansi">Unicode → ANSI</option>
                <option value="from-ansi">ANSI → Unicode</option>
              </select>
            </div>
            <div className="form-group">
              <label>Language</label>
              <select value={language} onChange={(e) => setLanguage(e.target.value)}>
                {LANGUAGES.map((l) => (
                  <option key={l.value} value={l.value}>{l.label}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Font Family</label>
              <select value={ansiFont} onChange={(e) => setAnsiFont(e.target.value)}>
                {ANSI_FONT_FAMILIES.map((f) => (
                  <option key={f.value} value={f.value}>{f.label}</option>
                ))}
              </select>
            </div>
          </>
        );

      case 'panchama-varga':
        return (
          <div className="form-group">
            <label>Language</label>
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              {LANGUAGES.map((l) => (
                <option key={l.value} value={l.value}>{l.label}</option>
              ))}
            </select>
          </div>
        );

      case 'iso15919':
        return (
          <div className="form-group">
            <label>Source Language</label>
            <select value={language} onChange={(e) => setLanguage(e.target.value)}>
              {LANGUAGES.map((l) => (
                <option key={l.value} value={l.value}>{l.label}</option>
              ))}
            </select>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="side-panel">
      <div className="side-panel-header">
        <span>🔤 Transliteration Tools</span>
        <button className="side-panel-close" onClick={onClose} title="Close panel" aria-label="Close">
          ✕
        </button>
      </div>
      <div className="side-panel-body">
        {/* Mode Selector */}
        <div className="form-group">
          <label>Tool</label>
          <select value={mode} onChange={(e) => onModeChange(e.target.value)}>
            {MODES.map((m) => (
              <option key={m.value} value={m.value}>{m.label}</option>
            ))}
          </select>
        </div>

        {/* Mode-specific options */}
        {renderOptions()}

        {/* Input */}
        <div className="form-group">
          <label>Input Text</label>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Paste or type text here…"
            rows={4}
          />
        </div>

        {/* Action Buttons */}
        <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
          <button
            className="btn btn-primary"
            onClick={handleConvert}
            disabled={isLoading || !inputText.trim()}
            style={{ flex: 1 }}
          >
            {isLoading ? 'Converting…' : 'Convert'}
          </button>
          <button className="btn" onClick={handleSwap} title="Swap input and output">
            ⇅
          </button>
        </div>

        {/* Error */}
        {error && (
          <div style={{
            padding: '8px 12px',
            marginBottom: '12px',
            background: '#fff0f0',
            border: '1px solid #ffcccc',
            borderRadius: '4px',
            color: '#cc0000',
            fontSize: '12px',
          }}>
            ⚠ {error}
          </div>
        )}

        {/* Output */}
        <div className="form-group">
          <label>Output</label>
          <textarea
            value={outputText}
            readOnly
            rows={4}
            placeholder="Converted text will appear here…"
            style={{ background: 'var(--panel-bg)' }}
          />
        </div>

        {outputText && (
          <button className="btn" onClick={handleCopy} style={{ width: '100%' }}>
            📋 Copy to Clipboard
          </button>
        )}

        {/* Info */}
        <div style={{
          marginTop: '16px',
          padding: '10px',
          background: 'var(--toolbar-bg)',
          borderRadius: '4px',
          fontSize: '11px',
          color: 'var(--text-secondary)',
          lineHeight: '1.5',
        }}>
          <strong>Tip:</strong> Select text in the document first, then use
          Tools → Transliterate Selection to convert in-place.
          <br /><br />
          The Python bridge must be running for transliteration features.
          It starts automatically with the app.
        </div>
      </div>
    </div>
  );
}
