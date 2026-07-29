# Varnaakshara — Master Project Specification

**Document status:** Master spec (authoritative)

**Repo:** `varnaakshara-ime/` (monorepo)

**Apps in scope:**
1. **Varnaakshara IME** — system-wide input method (Windows first; macOS later)
2. **Varnaakshara Writer** — free Microsoft Word alternative optimized for Indian languages

**Shared Core:** Table-driven transliteration + conversion engine, data tables, and Varnaakshara font families.

---

## 1) Vision

### 1.1 North Star
Make typing, editing, converting, and publishing Indian language content **fast, accurate, and compatible** across modern Unicode and legacy ANSI/“font-encoding” ecosystems.

### 1.2 Product principles (non-negotiable)
- **Accuracy first:** transliteration and conversions must be deterministic, testable, and language-aware.
- **Low friction:** IME works in any Windows app; Writer feels like Word.
- **Offline-first:** all core features (IME, editing, conversions) work without internet.
- **Interoperability:** import/export across DOCX/RTF/HTML/PDF; Unicode/ANSI conversions.
- **Free forever:** no paywalls; optional donations are allowed but must not degrade UX.

### 1.3 Primary user personas
- Students and professionals typing in Indian scripts across apps (IME).
- Publishers/typists maintaining legacy font documents (Writer + converters).
- Translators and multilingual writers working across scripts (script-to-script conversion).

### 1.4 Success metrics
- IME latency: **< 20 ms** per keystroke processing for common sequences.
- Suggestion quality: top-1 acceptance **> 35%** for common vocabulary (phase-based target).
- Import/export fidelity: round-trip DOCX → edit → DOCX retains formatting with **> 95%** parity on regression suites.
- Conversion correctness: Unicode↔ANSI and script conversion **100% deterministic**; errors measurable via golden tests.

---

## 2) Scope & Definitions

### 2.1 Supported languages (12)
“12 Indian languages” shall mean **12 writing systems/language groups** supported by the tables and fonts in this repo. Minimum initial set:
- Devanagari (Hindi/Marathi/Sanskrit)
- Kannada
- Telugu
- Tamil
- Malayalam
- Bengali
- Gujarati
- (plus remaining supported scripts per data availability; finalize in Open Questions)

All language support is implemented via **data tables**, not code forks.

### 2.2 Output modes
- **Unicode mode:** emits Unicode codepoints for the target script.
- **ANSI mode:** emits glyph-encoded text for legacy fonts (e.g., Shreelipi/Baraha-style encodings). Requires:
  - per-script ANSI encoding table
  - user-chosen font family mapping (Varnaakshara fonts or compatible legacy fonts)

### 2.3 Input schemes
- **Phonetic transliteration:** Baraha-like + ITRANS-like schemes.
- **INSCRIPT keyboard mode:** layout-driven mapping by script.

---

## 3) Repository Structure (authoritative)

```
varnaakshara-ime/
├── core/           # Shared engine + data
│   ├── engine/     # Table-driven transliteration engine
│   ├── data/       # JSON tables (phonetic, keyboard, unicode, collation, etc.)
│   └── fonts/      # Source + generated font files
├── ime/            # IME app (Windows/macOS)
├── writer/         # Writer app
│   └── src/
├── tools/          # CLI utilities (font converter, etc.)
├── docs/           # Documentation
└── tests/          # Test suite
```

Conventions:
- `core/` is a **library** consumed by IME, Writer, and tools.
- All behavior changes must be validated by **tests** and **golden fixtures**.

---

## 4) Architecture

### 4.1 High-level component diagram (logical)
- **Core Engine (`core/engine`)**
  - transliteration FSM / longest-match tokenizer
  - scheme loader + validator
  - per-language/script rules
  - suggestion interface hooks
- **Data Tables (`core/data`)**
  - phonetic mappings (Baraha + ITRANS)
  - INSCRIPT layouts
  - Unicode composition rules (matras, virama, conjuncts)
  - ANSI encoding tables (glyph mappings)
  - script-to-script conversion tables
  - collation tables
  - romanization (ISO 15919)
  - braille mapping
- **Fonts (`core/fonts`)**
  - Varnaakshara families and generated binaries
  - metadata manifests (family, weight, coverage)
- **IME App (`ime/`)**
  - OS integration (TSF on Windows)
  - UI: candidate list, settings, tray
  - hotkey toggles and per-app exclusions
- **Writer App (`writer/`)**
  - editor shell (tabs, ribbons/toolbars)
  - document model (HTML/JSON/Delta)
  - import/export services
  - language superpowers features
- **Tools (`tools/`)**
  - table compiler/validator
  - font encoder/decoder
  - doc converters and batch processors

### 4.2 Core transliteration engine design
**Goal:** Implement phonetic transliteration and keyboard layout mapping using a **data-driven deterministic engine**.

#### 4.2.1 Input processing pipeline
1. **Keystroke buffer** (per active context)
2. **Tokenizer / matcher**
   - longest-match over roman tokens (phonetic)
   - layout-based mapping for INSCRIPT
3. **Rule application**
   - context-sensitive rules: vowel signs, consonant conjunct behavior, implicit ‘a’, virama insertion, nukta handling
   - language-specific exception rules loaded from data
4. **Output composition**
   - Unicode: emits codepoints and combining marks per script
   - ANSI: emits legacy glyph codes + inserts zero-width / placeholders if required by legacy encoding
5. **Suggestion generation (optional in pipeline)**
   - dictionary lookup based on current composed word
   - ranked candidates
6. **Commit behavior**
   - commit on whitespace/punctuation or explicit key
   - backspace behavior: reverses buffer and recomposes

#### 4.2.2 Determinism
- Given (scheme, language/script, buffer) the engine output must be **pure and deterministic**.
- No hidden state beyond explicitly modeled context.

#### 4.2.3 Data contracts
- All JSON schemas are versioned.
- Engine must validate tables at startup (or during build) and fail with actionable errors.

### 4.3 Varnaakshara IME (Windows)

#### 4.3.1 Windows integration
- Implement IME using **Text Services Framework (TSF)**.
- Requirements:
  - composition string support
  - candidate list UI integration
  - per-app compatibility (Win32, UWP where possible)
  - 32/64-bit compatibility

#### 4.3.2 Tray + hotkeys
- System tray icon with:
  - language/script selection
  - input mode selection (phonetic/INSCRIPT)
  - scheme selection (Baraha/ITRANS)
  - output mode toggle (Unicode/ANSI)
  - ANSI font family selection
  - settings + diagnostics
- Global hotkey:
  - toggle IME on/off
  - optional cycle language

#### 4.3.3 Suggestion UI
- Candidate window near caret.
- Keyboard navigation (↑/↓, Tab, Enter, number keys).
- Must not steal focus.

### 4.4 Varnaakshara Writer

#### 4.4.1 Document model
- Internal representation must support rich formatting and round-trippable exports.
- Recommended internal model:
  - Editor engine stores a structured JSON (Lexical) or ProseMirror/TipTap document.
  - Export pipelines generate DOCX/RTF/HTML/PDF.

#### 4.4.2 UI model
- Word-like UI: ribbon or toolbar groups; rulers; status bar; tabbed docs.
- Offline spellcheck and find/replace.

#### 4.4.3 Shared engine embedding
- Writer must embed the same core engine for:
  - transliteration typing mode
  - transliteration-aware search
  - script conversion
  - Unicode↔ANSI conversion

---

## 5) Feature Matrix (deliverable-level)

Legend: **MVP** (first public usable), **V1** (strong release), **V2** (advanced)

### 5.1 IME features
- Phonetic transliteration (Baraha scheme): MVP
- Phonetic transliteration (ITRANS scheme): MVP
- INSCRIPT keyboard mode: MVP
- 12 languages/scripts via data: MVP (expand table coverage iteratively)
- Unicode output mode: MVP
- ANSI output mode + font family selection: V1
- System tray UI: MVP
- Global hotkey toggle: MVP
- Suggestions/autocomplete:
  - basic dictionary suggestions: V1
  - next-word prediction: V2
- Per-app enable/disable and profiles: V2
- User custom dictionary + learning: V2
- macOS IME port: V2/V3

### 5.2 Writer features (Word parity)
**Core editor**
- Rich text formatting (bold/italic/underline/strike/super/sub): MVP
- Font family/size: MVP
- Paragraph formatting: MVP
- Bullets/numbering: MVP
- Tables (insert/merge/borders/styling): V1
- Headers/footers: V1
- Page numbers: V1
- Find & replace (transliteration-aware): V1
- Spell check Indian languages: V1 (start with 1–2 languages, expand)
- Word/character count: MVP
- Undo/redo unlimited: MVP
- Copy/paste with formatting: MVP
- Drag & drop: MVP
- Insert images/shapes: V1
- Page setup: V1
- Print + print preview: V1
- Zoom: MVP
- Multiple document tabs: MVP
- Rulers (horizontal + vertical): V1
- Style sheets/presets: V1
- Table of contents generation: V1
- Bookmarks/hyperlinks: V1
- Comments/annotations: V2
- Track changes: V2
- Mail merge: V2
- Columns layout: V2
- Word art/decorative text: V2
- Borders and shading: V1
- Auto-save + recovery: V1

**Import/Export**
- Export PDF: V1
- Export DOCX/RTF/plain/HTML: V1
- Import DOCX/RTF/plain/HTML: V1

**Indian language superpowers**
- Built-in transliteration typing: MVP
- Script-to-script conversion: V1
- Unicode↔ANSI conversion: V1
- Panchama varga nasal conversion: V1
- OCR (image→text): V2 (offline optional; may use local OCR models)
- Legacy font document import + auto convert (Shreelipi/Baraha): V1/V2 (phase by font)
- ISO 15919 romanization: V1
- Braille output: V2
- Collation-aware sorting: V1

### 5.3 Shared Core features
- Table-driven transliteration engine: MVP
- JSON schema validation + compiler: MVP
- Test fixtures + golden tests: MVP
- Font families integration: V1 (as fonts become available)
- CLI tools for conversion/batch processing: V1

---

## 6) Tech Stack Decision

### 6.1 Decision record goals
- Maximize delivery speed for Writer (complex UI)
- Ensure strong Windows IME integration (native required)
- Maintain shared core in a single language when possible

### 6.2 Options

#### Option A — Electron + Web Editor (Lexical/TipTap)
- **Writer:** Electron + Lexical (React) or TipTap (ProseMirror)
- **IME:** separate native Windows TSF component; may expose a local IPC bridge for shared core
- **Core engine:** TypeScript (shared with Writer), with native bindings for IME (Node-API) or a small embedded runtime

Pros:
- Fastest for Word-like UI
- Mature editor ecosystem
- Easier DOCX/HTML tooling

Cons:
- IME still needs native; sharing TS engine with TSF adds complexity
- Electron footprint

#### Option B — Tauri + Web Editor
- **Writer:** Tauri (Rust) + web editor
- **IME:** TSF native; core could be Rust and reused

Pros:
- Smaller footprint than Electron
- Rust core can be shared between IME and Writer

Cons:
- Slightly higher integration complexity; editor stack similar

### 6.3 Recommendation (initial)
**Writer:** Electron + Lexical (or TipTap) for maximum speed and fidelity.

**IME:** Native Windows TSF in C++ or Rust.

**Core Engine:** Implement core engine as **Rust library** with:
- WASM build for Writer (or a TS wrapper calling Rust via wasm)
- Native build for IME and tools

Rationale:
- One deterministic engine implementation for all apps
- Performance and correctness advantages
- Easier to test and ship as a single crate/library

If Rust is rejected, fallback is TypeScript core + native wrapper for TSF (higher risk).

**Action item:** create ADR `docs/adr/ADR-0001-tech-stack.md` after prototype spike.

---

## 7) Data Pipeline (Tables, Reverse Engineering, Validation)

### 7.1 Source data
- Reverse-engineered mappings from **Baraha** and **Shreelipi**.

### 7.2 Data formats
All tables in `core/data/`.

Required table types (minimum):
- `phonetic/<scheme>/<script>.json`
  - roman token → target script output (Unicode sequence) and/or ANSI glyph sequence
  - metadata: token class (vowel/consonant), precedence
- `keyboard/inscript/<script>.json`
  - key + modifiers → output sequence
- `unicode/rules/<script>.json`
  - composition rules, virama behavior, special cases
- `ansi/encodings/<fontFamily>/<script>.json`
  - Unicode sequence ↔ ANSI glyph code sequence mapping
- `script-conversion/<from>-to-<to>.json`
  - mapping tables including normalization rules
- `collation/<script>.json`
  - sort weights and normalization
- `romanization/iso15919/<script>.json`
- `braille/<script>.json`

### 7.3 Build-time compilation
Create a `tools/tablec` compiler that:
- Validates JSON against schema
- Produces optimized binary/packed JSON artifacts for runtime
- Emits reports:
  - coverage stats (glyphs, aksharas)
  - conflict detection (same token maps to multiple outputs)
  - unreachable tokens

### 7.4 Versioning
- Tables have `schemaVersion`.
- Engine has compatibility matrix: supports last N versions.

### 7.5 Golden tests
- For each script and scheme: `tests/golden/<script>/<scheme>.yaml`
- Include:
  - input roman strings → expected Unicode
  - input roman strings → expected ANSI (when enabled)
  - backspace behavior
  - edge cases (conjuncts, anusvara, visarga, nukta)

---

## 8) Font Engineering

### 8.1 Font families
Include these Varnaakshara families:
- Kannada: `Varnaakshara Kan01` … `Kan09`
- Devanagari: `Dev01`
- Telugu: `Tel01` … `Tel03`
- Tamil: `Tam01` … `Tam03`
- Malayalam: `Mal01` … `Mal03`
- Bengali: `Ben01` … `Ben02`
- Gujarati: `Guj01` … `Guj02`

Each family has **5 weights**:
- Regular, Medium, SemiBold, Bold, Black

### 8.2 Font deliverables
For each family + weight:
- TTF/OTF binaries for Unicode usage
- If ANSI mode requires special encoding fonts, provide:
  - ANSI-encoded font binaries OR
  - Unicode font + encoding table that maps to legacy glyph codes (preferred when feasible)

### 8.3 Font metadata manifest
Create `core/fonts/manifest.json` listing:
- family name
- weights available
- scripts covered
- supported output modes (Unicode/ANSI)
- recommended fallback fonts

### 8.4 Build tooling
- Use `fonttools` (Python) or Rust font tooling to:
  - subset
  - generate weight instances if variable fonts exist
  - normalize naming
  - validate glyph coverage

### 8.5 ANSI font family selection
IME and Writer must:
- list ANSI-capable font families for the selected script
- persist user selection per script
- ensure emitted ANSI codes match the chosen family’s encoding table

---

## 9) Build, Packaging, and Distribution

### 9.1 Monorepo build orchestration
- Root build uses a single orchestrator (recommended: `pnpm` + `turbo` or `nx`, plus Rust workspace if used).
- CI must build:
  - core engine + tables
  - IME installer
  - Writer installer
  - CLI tools
  - run tests

### 9.2 Windows IME packaging
Deliverables:
- Signed installer (MSI or EXE) installing TSF text service
- Uninstaller
- System tray app (if separate process)

Requirements:
- Auto-update optional (V2); must be user-consented.

### 9.3 Writer packaging
- Windows installer
- App data directory for:
  - dictionaries
  - user settings
  - recovery/autosave files

### 9.4 CLI tools packaging
- Provide `tools/` binaries for:
  - batch conversion (Unicode↔ANSI)
  - script conversion
  - document conversion pipeline

### 9.5 Licensing
- Code license: choose permissive (MIT/Apache-2) or copyleft (GPL) — open question.
- Fonts: ensure redistributable licensing.

---

## 10) Milestones (phased plan)

### Milestone 0 — Foundations (2–4 weeks)
- Set up repo skeleton with `core/`, `ime/`, `writer/`, `tools/`, `tests/`.
- Define JSON schemas for key tables.
- Implement `core/engine` minimal transliteration (one script + one scheme).
- Golden test harness.

### Milestone 1 — IME MVP (4–8 weeks)
- TSF integration with composition.
- Phonetic transliteration (Baraha + ITRANS) for at least 2 scripts.
- INSCRIPT mapping for at least 2 scripts.
- Tray UI + hotkey.
- Unicode output.

### Milestone 2 — Writer MVP (4–8 weeks)
- Electron/Tauri shell with tabbed editor.
- Core formatting features (MVP list above).
- Embedded transliteration typing.
- Basic import/export: HTML + plain text.

### Milestone 3 — V1 Feature Completion (8–16 weeks)
- Expand to all 12 scripts.
- ANSI mode + font selection.
- DOCX/RTF import/export.
- Print + preview.
- Spellcheck initial languages.
- Script conversion + ISO 15919.

### Milestone 4 — Advanced “Superpowers” (ongoing)
- OCR pipeline.
- Track changes, comments.
- Legacy font document import automation.
- Braille output.

---

## 11) Open Questions (must resolve early)

1. **Exact list of 12 languages/scripts**: confirm which 12 and prioritize order.
2. **Core engine language**: Rust vs TypeScript. Decision affects IME and Writer integration.
3. **Windows IME architecture**: single process vs TSF service + tray companion.
4. **ANSI scope**:
   - Which legacy encodings must be supported first? (Shreelipi variants, Baraha fonts, others)
   - Are we shipping our own ANSI fonts or only conversion tables?
5. **Dictionary sources** for suggestions and spellcheck:
   - open lexicons per language
   - licensing constraints
6. **OCR approach**:
   - offline-only vs optional online
   - acceptable model sizes
7. **DOCX fidelity target**:
   - exact compatibility with Word features vs subset
   - how to handle unsupported constructs
8. **Licensing** for code and fonts.
9. **macOS IME plan**:
   - InputMethodKit vs other approach
   - timeline
10. **Backward compatibility guarantees** for table versions and documents.

---

## 12) Implementation Notes (actionable defaults)

- Every mapping change requires:
  - schema validation pass
  - updated golden tests
  - changelog entry
- Add a `docs/decisions/` folder for ADRs.
- Add `tools/diagnostics` to dump current engine state (active scheme, buffer, outputs) for bug reports.
- Add a `tests/corpus/` for real-world text corpora and regression outputs.

---

## 13) Immediate Next Actions

1. Create schemas for `phonetic`, `inscript`, `ansi-encoding`, and `unicode-rules`.
2. Implement engine MVP for one script (recommended: Devanagari) + Baraha scheme.
3. Build minimal TSF IME prototype that calls engine and displays composition.
4. Choose Writer stack via 1-week spike:
   - Lexical vs TipTap
   - DOCX import/export library evaluation
5. Start font manifest and decide how ANSI mapping will be represented.
