# Varnaakshara Writer

A free, open-source word processor built for Indian languages. Think Microsoft Word, but with built-in transliteration, script conversion, Unicode↔ANSI conversion, and support for all major Indian scripts out of the box.

Part of the **Varnaakshara IME** suite.

---

## Features

- **Rich text editing** — Bold, italic, underline, strikethrough, headings, lists, tables, links, images
- **Word-like UI** — Familiar ribbon toolbar, status bar, menu bar, page layout
- **Indian language support** — Noto fonts for Kannada, Devanagari, Telugu, Tamil, Malayalam, Bengali, Gujarati, Gurmukhi, Odia
- **Transliteration tools** — Convert between input schemes (Baraha, ITRANS, Harvard-Kyoto, IAST, SLP1)
- **Script conversion** — Convert text between any two Indian scripts
- **Unicode ↔ ANSI** — Convert between Unicode and legacy ANSI fonts (Nudi, Baraha, Anu, Shree, Akruti)
- **Panchama Varga conversion** — Nasal consonant normalization
- **ISO 15919 romanization** — Standard transliteration to Latin
- **File format** — `.vnk` (JSON-based), with HTML import/export
- **Export** — PDF, HTML (DOCX planned)
- **Dark mode** — Full dark theme support
- **Auto-save** — Automatic saving every 60 seconds

---

## Architecture

```
writer/
├── package.json              # Dependencies & scripts
├── webpack.config.js         # Webpack bundler config
├── src/
│   ├── main.js               # Electron main process (window, menus, IPC, file I/O)
│   ├── bridge.py             # Python HTTP server wrapping TransliterationEngine
│   └── renderer/
│       ├── index.html        # HTML shell
│       ├── index.jsx         # React entry point
│       ├── components/
│       │   ├── App.jsx               # Root app component
│       │   ├── Editor.jsx            # Lexical editor with all plugins
│       │   ├── Toolbar.jsx           # Word-style ribbon toolbar
│       │   ├── StatusBar.jsx         # Bottom status bar
│       │   └── TransliterationPanel.jsx  # Side panel for transliteration tools
│       ├── styles/
│       │   ├── app.css       # App layout, theming, CSS variables
│       │   ├── editor.css    # Document page styling
│       │   └── toolbar.css   # Toolbar/ribbon styling
│       └── utils/
│           └── fileOps.js    # File serialization, .vnk format, HTML export
└── dist/                     # Built packages (generated)
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Desktop shell | Electron |
| Editor engine | Lexical (by Meta) |
| UI framework | React 18 |
| Bundler | Webpack 5 |
| Transliteration | Python (TransliterationEngine via HTTP bridge) |
| Packaging | electron-builder |

### Data Flow

```
User types → Lexical Editor → React state → OnChangePlugin → dirty flag
                                                    ↓
                                          Auto-save timer (IPC)
                                                    ↓
                                          main.js → fs.writeFile(.vnk)

Tools menu → IPC → Python bridge (HTTP :5111) → TransliterationEngine
                                                    ↓
                                          Response → Side panel
```

---

## Development Setup

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+ (for the transliteration bridge)
- The Varnaakshara core engine at `../core/engine/`

### Install Dependencies

```bash
cd writer
npm install
```

### Run in Development Mode

```bash
npm run dev
```

This starts:
1. Webpack dev server on `http://localhost:9000` (hot reload)
2. Electron window loading from the dev server

### Build for Production

```bash
npm run build
```

This bundles the React app into `build/`.

### Package for Distribution

```bash
# Windows
npm run package

# Linux
npm run package:linux

# macOS
npm run package:mac
```

Output goes to `dist/`.

---

## File Format (.vnk)

The `.vnk` format is a JSON file with this structure:

```json
{
  "varnaakshara": true,
  "version": "1.0",
  "created": "2026-07-26T12:00:00.000Z",
  "modified": "2026-07-26T14:30:00.000Z",
  "metadata": {
    "title": "My Document",
    "author": "User",
    "language": "kn"
  },
  "content": {
    "root": {
      "children": [...],
      "type": "root"
    }
  }
}
```

The `content` field is a standard Lexical editor state JSON object.

---

## Python Bridge

The bridge server (`src/bridge.py`) starts automatically with the Electron app and runs on `http://127.0.0.1:5111`. It wraps the `TransliterationEngine` from `../../core/engine/transliteration.py`.

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/transliterate` | Transliterate text using a scheme |
| POST | `/convert-script` | Convert between Indian scripts |
| POST | `/to-ansi` | Unicode → ANSI conversion |
| POST | `/from-ansi` | ANSI → Unicode conversion |
| POST | `/to-iso15919` | ISO 15919 romanization |
| POST | `/reverse` | Reverse transliteration |
| POST | `/spell-check` | Spell check (stub) |
| POST | `/word-count` | Word/char/sentence/paragraph count |

### Testing the Bridge

```bash
python3 src/bridge.py

# In another terminal:
curl http://localhost:5111/health
curl -X POST http://localhost:5111/word-count \
  -H "Content-Type: application/json" \
  -d '{"text": "ನಮಸ್ಕಾರ ವಿಶ್ವ"}'
```

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New | Ctrl+N |
| Open | Ctrl+O |
| Save | Ctrl+S |
| Save As | Ctrl+Shift+S |
| Print | Ctrl+P |
| Undo | Ctrl+Z |
| Redo | Ctrl+Y |
| Bold | Ctrl+B |
| Italic | Ctrl+I |
| Underline | Ctrl+U |
| Strikethrough | Ctrl+Shift+X |
| Find & Replace | Ctrl+H |
| Insert Link | Ctrl+K |
| Align Left | Ctrl+L |
| Center | Ctrl+E |
| Align Right | Ctrl+R |
| Justify | Ctrl+J |
| Zoom In | Ctrl+= |
| Zoom Out | Ctrl+- |
| Reset Zoom | Ctrl+0 |
| Full Screen | F11 |

---

## Roadmap

- [ ] DOCX export (via `docx` npm library)
- [ ] Spell check with Indian language dictionaries
- [ ] OCR integration (scan image → text)
- [ ] Find & Replace dialog
- [ ] Ruler / margin controls
- [ ] Header & Footer support
- [ ] Page numbering
- [ ] Columns layout
- [ ] Image resize handles
- [ ] Drag & drop file opening
- [ ] Template system
- [ ] Multi-tab / multi-document support

---

## License

MIT
