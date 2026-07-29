# Varnaakshara IME (वर्णाक्षरः)

A **system-wide phonetic transliteration Input Method Engine** for Windows that lets you type in 12 Indian languages using a standard English keyboard. Type in Roman letters (Baraha scheme) — see Indian script appear in real-time, in **any** application.

**Free. Not for sale.**

**Website:** [exaggarate.github.io/Varnaakshara](https://exaggarate.github.io/Varnaakshara/)
**Download:** [GitHub Releases](https://github.com/Exaggarate/clawdbot-railway/releases/tag/v1.2.0)

---

## Table of Contents

- [How It Works](#how-it-works)
- [Supported Languages](#supported-languages)
- [Installation](#installation)
- [Usage & Keyboard Shortcuts](#usage--keyboard-shortcuts)
- [Complete Typing Reference](#complete-typing-reference)
- [Features](#features)
- [Technical Architecture](#technical-architecture)
- [Project Structure](#project-structure)
- [Building from Source](#building-from-source)
- [Testing](#testing)
- [Changelog](#changelog)
- [Future Plans](#future-plans)

---

## How It Works

You type English letters on your regular keyboard. Varnaakshara intercepts the keystrokes at the OS level and converts them to Indian script in real-time, before any application sees them.

```
namaskAra  →  ನಮಸ್ಕಾರ (Kannada)
namastE    →  नमस्ते (Hindi)
shrI       →  శ్రీ (Telugu)
vanakkam   →  வணக்கம் (Tamil)
dhanyavAd  →  ধন্যবাদ (Bengali)
namaskAr   →  નમસ્કાર (Gujarati)
```

No special keyboard layout to learn. No IME panel to click through. If you can type English, you can type in any Indian language.

---

## Supported Languages

| # | Language | Script | Example | Hotkey |
|---|----------|--------|---------|--------|
| 1 | Kannada | ಕನ್ನಡ | ನಮಸ್ಕಾರ | Ctrl+1 |
| 2 | Hindi | हिन्दी | नमस्ते | Ctrl+2 |
| 3 | Telugu | తెలుగు | నమస్కారం | Ctrl+3 |
| 4 | Tamil | தமிழ் | வணக்கம் | Ctrl+4 |
| 5 | Malayalam | മലയാളം | നമസ്കാരം | Ctrl+5 |
| 6 | Marathi | मराठी | नमस्कार | Ctrl+6 |
| 7 | Sanskrit | संस्कृतम् | नमस्कारः | Ctrl+7 |
| 8 | Bengali | বাংলা | নমস্কার | Ctrl+8 |
| 9 | Assamese | অসমীয়া | নমস্কাৰ | Ctrl+9 |
| 10 | Gujarati | ગુજરાતી | નમસ્કાર | Ctrl+0 |
| 11 | Punjabi (Gurmukhi) | ਪੰਜਾਬੀ | ਨਮਸਕਾਰ | — |
| 12 | Odia | ଓଡ଼ିଆ | ନମସ୍କାର | — |

Each language has its own Unicode script mapping table. The transliteration engine converts Roman → Devanagari first, then maps Devanagari codepoints to the target script using Unicode offset tables.

---

## Installation

### Windows Installer (Recommended)

1. Download **`Varnaakshara_Setup_v1.2.0.exe`** from [GitHub Releases](https://github.com/Exaggarate/clawdbot-railway/releases/tag/v1.2.0)
2. Run the installer — follow the wizard
3. **No admin privileges required** — installs to `%LOCALAPPDATA%\Programs\Varnaakshara\`
4. Optional: create desktop shortcut, enable start-on-boot
5. Launch from Start Menu or Desktop
6. Press **F11** or **F12** to toggle Indian script mode

**Requirements:** Windows 10 or later, 64-bit

### What the Installer Does

- Copies `Varnaakshara.exe` (42.5 MB PyInstaller bundle) to install directory
- Installs **32 fonts** to `{app}\fonts\` (Unicode, ANSI legacy, and Vedic)
- Registers all fonts in `HKCU\Software\Microsoft\Windows NT\CurrentVersion\Fonts` (per-user, no admin)
- Calls `AddFontResourceEx` to make fonts immediately available without reboot
- Optionally adds startup registry entry at `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
- Sends `WM_FONTCHANGE` to notify all running applications about new fonts
- Creates Start Menu shortcuts and optional desktop shortcut
- Clean uninstall removes everything (fonts, registry entries, shortcuts)

### Running from Source (Development)

```bash
pip install PyQt5
python varnaakshara_ime.py
```

---

## Usage & Keyboard Shortcuts

### Core Controls

| Key | Action |
|-----|--------|
| **F11** or **F12** | Toggle IME on/off (English ↔ Indian script) |
| **Ctrl+1** through **Ctrl+0** | Switch language (1=Kannada, 2=Hindi, ..., 0=Gujarati) |
| **Space** | Commit current word + insert space |
| **Enter** | Commit current word + insert newline |
| **Backspace** | Remove one transliteration step (smart — doesn't erase whole word) |
| **Escape** | Dismiss suggestion popup |
| **Tab** | Accept first suggestion |
| **1–5** (when popup visible) | Accept numbered suggestion |
| **↑ / ↓** (when popup visible) | Navigate suggestions |

### How the Buffer Works

When IME is active, your keystrokes go into an internal Roman buffer. The engine transliterates this buffer in real-time and shows the Indian script on screen:

```
You press:  n → a → m → a → s → k → A → r → a
Buffer:     n   na  nam nama namas namask namaskA namaskAr namaskAra
Screen:     ನ   ನ   ನಮ  ನಮ  ನಮಸ  ನಮಸ್ಕ  ನಮಸ್ಕಾ  ನಮಸ್ಕಾರ್  ನಮಸ್ಕಾರ
```

When you press **Space**, **Enter**, or any punctuation, the current word is "committed" — the buffer clears and the Indian text stays on screen. You're ready for the next word.

When you press **Backspace**, one character is removed from the Roman buffer (not from the Indian text directly). The engine re-transliterates and uses a diff algorithm to minimally update the screen.

---

## Complete Typing Reference

### Vowels (23 mappings)

#### Standalone Vowels (used at word start or after another vowel)

| Type | Get | Name | Unicode |
|------|-----|------|---------|
| `a` | अ | Short a | U+0905 |
| `A` or `aa` | आ | Long aa | U+0906 |
| `i` | इ | Short i | U+0907 |
| `I` or `ii` | ई | Long ii | U+0908 |
| `u` | उ | Short u | U+0909 |
| `U` or `oo` | ऊ | Long uu | U+090A |
| `e` | ऎ | Short e | U+090E |
| `E` or `ee` | ए | Long e | U+090F |
| `ai` | ऐ | Ai | U+0910 |
| `o` | ऒ | Short o | U+0912 |
| `O` or `oo` | ओ | Long o | U+0913 |
| `au` or `ou` | औ | Au | U+0914 |
| `Ru` | ऋ | Vocalic r | U+090B |
| `RU` | ॠ | Long vocalic r | U+0960 |
| `~lu` | ऌ | Vocalic l | U+090C |
| `~lU` | ॡ | Long vocalic l | U+0961 |
| `~e` | ऍ | Candra e (English a) | U+090D |
| `~o` | ऑ | Candra o (English o) | U+0911 |

**Note:** Hindi and Marathi don't have short e/o — `e` maps to ए and `o` maps to ओ automatically.

#### Vowel Signs (used after a consonant)

When a vowel follows a consonant, the dependent (mātrā) form is used automatically:

| Type | Sign | Example |
|------|------|---------|
| `a` | (inherent, no mark) | `ka` → क |
| `A` / `aa` | ा | `kA` → का |
| `i` | ि | `ki` → कि |
| `I` / `ii` | ी | `kI` → की |
| `u` | ु | `ku` → कु |
| `U` / `oo` | ू | `kU` → कू |
| `e` | ॆ | `ke` → कॆ |
| `E` / `ee` | े | `kE` → के |
| `ai` | ै | `kai` → कै |
| `o` | ॊ | `ko` → कॊ |
| `O` | ो | `kO` → को |
| `au` / `ou` | ौ | `kau` → कौ |
| `Ru` | ृ | `kRu` → कृ |

### Consonants (61 mappings)

#### Basic Consonants (Varga — organized by mouth position)

**Velar (kaṇṭhya — throat):**
| Type | Get | Name |
|------|-----|------|
| `k` | क | ka |
| `K` or `kh` | ख | kha |
| `g` | ग | ga |
| `G` or `gh` | घ | gha |
| `~g` | ङ | ṅa (velar nasal) |

**Palatal (tālavya — palate):**
| Type | Get | Name |
|------|-----|------|
| `c` or `ch` | च | ca |
| `C` or `Ch` | छ | cha |
| `j` | ज | ja |
| `J` or `jh` | झ | jha |
| `~j` | ञ | ña (palatal nasal) |

**Retroflex (mūrdhanya — roof of mouth):**
| Type | Get | Name |
|------|-----|------|
| `T` | ट | ṭa |
| `Th` | ठ | ṭha |
| `D` | ड | ḍa |
| `Dh` | ढ | ḍha |
| `N` | ण | ṇa (retroflex nasal) |

**Dental (dantya — teeth):**
| Type | Get | Name |
|------|-----|------|
| `t` | त | ta |
| `th` | थ | tha |
| `d` | द | da |
| `dh` | ध | dha |
| `n` | न | na |

**Labial (oṣṭhya — lips):**
| Type | Get | Name |
|------|-----|------|
| `p` | प | pa |
| `P` or `ph` | फ | pha |
| `b` | ब | ba |
| `B` or `bh` | भ | bha |
| `m` | म | ma |

**Semi-vowels (antaḥstha):**
| Type | Get | Name |
|------|-----|------|
| `y` | य | ya |
| `r` | र | ra |
| `l` | ल | la |
| `v` or `w` | व | va |
| `L` | ळ | ḷa (Kannada/Marathi retroflex lateral) |

**Sibilants & Aspirate (ūṣma):**
| Type | Get | Name |
|------|-----|------|
| `S` or `sh` | श | śa (palatal sibilant) |
| `Sh` | ष | ṣa (retroflex sibilant) |
| `s` | स | sa (dental sibilant) |
| `h` or `~h` | ह | ha |

#### Nukta Consonants (Perso-Arabic borrowings)
| Type | Get | Name | Unicode |
|------|-----|------|---------|
| `kx` | क़ | qa | U+0958 |
| `Kx` | ख़ | ḵa | U+0959 |
| `gx` | ग़ | ġa | U+095A |
| `jx` or `z` | ज़ | za | U+095B |
| `Dx` | ड़ | ṛa | U+095C |
| `Dhx` | ढ़ | ṛha | U+095D |
| `Px` or `f` | फ़ | fa | U+095E |
| `yx` or `Y` | य़ | ẏa | U+095F |
| `rx` | ऱ | ṟa (Tamil/Malayalam) | U+0931 |
| `Lx` or `zh` | ऴ | ḻa (Tamil/Malayalam) | U+0934 |
| `nx` | ऩ | ṉa | U+0929 |

#### Special Conjuncts (multi-consonant ligatures)
| Type | Get | Name |
|------|-----|------|
| `kSh` | क्ष | kṣa (ksha) |
| `j~j` | ज्ञ | jña (gya/dnya) |

### Yogavāhas (Modifiers)

| Type | Get | Name | Unicode |
|------|-----|------|---------|
| `M` | ं | Anusvāra (nasal dot) | U+0902 |
| `H` | ः | Visarga (breath) | U+0903 |
| `~M` | ँ | Chandrabindu (nasal moon) | U+0901 |

**Usage:** These come after a vowel or consonant — `rAM` → राम (rām with anusvāra), `namaH` → नमः

### Conjunct Consonants (Samyuktākṣara)

When two consonants appear together without a vowel between them, a virama (halant ्) joins them into a conjunct:

```
kka  → क्क     tta  → त्त     nna  → न्न
shra → श्र     ksha → क्ष     nta  → न्त
sva  → स्व     tva  → त्व     dya  → द्य
pra  → प्र     sta  → स्त     ndha → न्ध
```

The engine handles this automatically — type the consonants in sequence and it inserts virama between them. When a vowel follows, it removes the virama and adds the vowel sign.

### Special Characters & Symbols (7 mappings)

| Type | Get | Name | Unicode | Notes |
|------|-----|------|---------|-------|
| `&` | ऽ | Avagraha (elision) | U+093D | Used in Sanskrit sandhi: `so&ham` → सोऽहम् |
| `\|` | । | Danda (full stop) | U+0964 | Indian sentence terminator |
| `\|\|` | ॥ | Double danda | U+0965 | Verse/shloka terminator |
| `OM` | ओं | Normal letters | — | Regular transliteration |
| `OM.` | ॐ | Om symbol | U+0950 | Period triggers the symbol and is consumed |
| `_` | (skip) | — | — | Underscore breaks a conjunct without visible virama |
| `^` | ZWJ | Zero-width joiner | U+200D | Forces conjunct form |
| `^^` | ZWNJ | Zero-width non-joiner | U+200C | Prevents conjunct form |

### Vedic Accent Marks

For Vedic Sanskrit chanting notation (Taittirīya tradition):

| Type | Get | Name | Unicode | Position |
|------|-----|------|---------|----------|
| `#` | ॑ | Svarita (rising tone) | U+0951 | Above the syllable |
| `$` | ॒ | Anudātta (low tone) | U+0952 | Below the syllable |
| `##` | ᳚ | Dīrgha svarita (prolonged rising) | U+1CDA | Above the syllable |

**Udātta** (high tone) is **unmarked** — this is standard Taittirīya convention where the default pitch is high.

**Example:** Puruṣa Sūkta opening:
```
sa$hasra#  shIrShA$  puru#ShaH
स॒हस्र॑   शीर्षा॒    पुरु॑षः
```

### Indian Numerals (Digits)

When numeral mode is enabled, digits are converted to the script's native numerals:

| Type | Devanagari | Kannada | Telugu | Tamil |
|------|-----------|---------|--------|-------|
| 0 | ० | ೦ | ౦ | ௦ |
| 1 | १ | ೧ | ౧ | ௧ |
| 2 | २ | ೨ | ౨ | ௨ |
| 3 | ३ | ೩ | ౩ | ௩ |
| 4 | ४ | ೪ | ౪ | ௪ |
| 5 | ५ | ೫ | ౫ | ௫ |
| 6 | ६ | ೬ | ౬ | ௬ |
| 7 | ७ | ೭ | ౭ | ௭ |
| 8 | ८ | ೮ | ౮ | ௮ |
| 9 | ९ | ೯ | ౯ | ௯ |

---

## Features

### Core IME Engine
- **System-wide keyboard hook** — `WH_KEYBOARD_LL` via Win32 `SetWindowsHookExW`. Intercepts ALL hardware keystrokes before any app processes them
- **Real-time transliteration** — see Indian script appear character-by-character as you type
- **Works in any application** — Notepad, Word, Chrome, VS Code, Photoshop, games, terminal, anything that accepts text input
- **Diff-based screen updates** — the `_update()` method finds the longest common prefix between old and new screen text, erases only the changed suffix, and types only the new suffix. All operations sent as ONE atomic `SendInput` call
- **Smart backspace** — removes one Roman character from the buffer, re-transliterates, diffs against current screen, sends minimal corrections. Pressing backspace on a 20-character word sends 2-4 events instead of 40+
- **Injected event filtering** — the hook checks `LLKHF_INJECTED` flag to skip its own `SendInput` output, preventing infinite recursion
- **Combining mark awareness** — when the diff boundary falls on a combining mark (Unicode category Mc/Mn), the engine backs up one position to include the base character, ensuring proper rendering

### Transliteration Engine (transliteration.py)
- **Two-stage pipeline:** Roman → Devanagari (canonical) → Target script
- **Greedy left-to-right matching** with longest-match priority (e.g., `sh` matches before `s` + `h`)
- **61 consonant mappings** including all standard, nukta, and special conjuncts
- **23 vowel mappings** with automatic standalone/dependent form selection
- **3 yogavāha mappings** (anusvāra, visarga, chandrabindu)
- **7 symbol mappings** (avagraha, danda, double danda, OM, svarita, anudātta, dīrgha svarita)
- **10 digit mappings** per script
- **Virama (halant) management** — automatically inserted between consecutive consonants, removed when a vowel follows
- **Implicit schwa handling** — Hindi and Marathi correctly drop the inherent 'a' at word-end (भारत not भारत्)
- **Script conversion tables:**
  - Kannada: 93 Devanagari→Kannada mappings
  - Telugu: 90 mappings
  - Tamil: 75 mappings (fewer because Tamil has fewer consonant distinctions)
  - Malayalam: 84 mappings
  - Bengali: 90 mappings
  - Assamese: 90 mappings (shares Bengali script with small differences)
  - Gujarati: 82 mappings
  - Punjabi (Gurmukhi): 86 mappings
  - Odia: 82 mappings
  - Hindi/Marathi/Sanskrit: direct Devanagari (no conversion needed, only post-processing)
- **ANSI font support** — `unicode_to_ansi_kannada()` and `unicode_to_ansi_hindi()` for legacy BRH font compatibility

### Word Suggestions (suggestions.py + suggestion_popup.py)
- **731,000+ word dictionary** spanning all 12 supported languages
- **Auto-completion popup** appears after 3+ characters typed
- **Up to 5 suggestions** shown at a time
- **Prefix matching** — matches the beginning of the transliterated text against the dictionary
- **Personal learning** — words you type and commit are stored in a per-user learned dictionary. Learned words are shown with a ★ marker and ranked higher
- **Learned dictionary persistence** — saved to `%APPDATA%\Varnaakshara\learned_{lang}.json`
- **Win32 popup window** — `suggestion_popup.py` creates a `STATIC` class window with `WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE` flags, so it floats above everything without stealing focus
- **14pt Nirmala UI font** — clear, large text for readability
- **Smart positioning** — 3-tier caret detection:
  1. `GetGUIThreadInfo` → screen coordinates from `rcCaret`
  2. `GetCaretPos` + `ClientToScreen` → fallback for simpler apps
  3. Mouse cursor position → final fallback when caret APIs fail
- **Keyboard navigation** — Tab or 1-5 to accept, Up/Down arrows to navigate, Esc to dismiss

### System Tray & UI
- **PyQt5 system tray icon** — sits in the Windows taskbar notification area
- **Dynamic tray icon** — shows the current language code (KA, HI, TE, etc.) with color indicating active (green) or inactive (gray) state
- **Icon generated in-memory** — uses `QPainter` to draw text on a colored circle, no static icon files per language
- **Right-click menu:**
  - Toggle active/inactive
  - Language submenu (all 12 languages)
  - Indian numerals toggle
  - Settings
  - Check for updates
  - About dialog
  - Exit
- **Settings dialog** (`settings_ui.py`, 533 lines) — PyQt5 window with:
  - Default language selector
  - Start active on launch toggle
  - Run at Windows startup toggle
  - Show indicator toggle
  - Indicator opacity slider
  - Suggestion count (1-9)
  - Config saved to `%APPDATA%\Varnaakshara\settings.json`

### Auto-Updater (updater.py)
- Checks `https://api.github.com/repos/Exaggarate/Varnaakshara/releases/latest` for new versions
- Compares semantic version (`major.minor.patch`) against `CURRENT_VERSION`
- Downloads installer to temp directory
- Shows progress in a Qt dialog
- Runs the downloaded installer silently to upgrade in-place
- Optional startup check (configurable in settings)

### Single Instance Guard
- Uses a named mutex (`VarnaaksharaIME_SingleInstance`) to prevent multiple instances
- If another instance is already running, new launch shows an error and exits

### Fonts (32 bundled)

**7 Unicode fonts (Noto Sans family):**
- NotoSansBengali.ttf
- NotoSansDevanagari.ttf
- NotoSansGujarati.ttf
- NotoSansKannada-Regular.ttf
- NotoSansMalayalam.ttf
- NotoSansTamil.ttf
- NotoSansTelugu.ttf

**2 Patched Vedic fonts:**
- NotoSansKannadaVedic.ttf — fixed dīrgha svarita (U+1CDA) glyph from quotation-mark shape to proper ∏-shaped double vertical line
- NotoSansDevanagariVedic.ttf — same fix
- Patched using `fontTools` library — modified `glyf` table contour coordinates in-place, renamed via `name` table records (nameID 1, 4, 6) to avoid system font conflicts

**23 BRH ANSI legacy fonts:**
brhaknd, brhben, brhbenrn, brhbglr, brhdevrn, brhguj, brhgujrn, brhkai, brhknd, brhkndb, brhknde, brhkndrn, brhmal, brhmale, brhmalrn, brhsknd, brhtab, brhtabe, brhtabrn, brhtel, brhtele, brhtelrn, brhvjy

---

## Technical Architecture

### Keyboard Hook Flow

```
Hardware Keyboard
       ↓
[WH_KEYBOARD_LL hook] ← varnaakshara_ime.py:_hook_callback()
       ↓
Is LLKHF_INJECTED set? → YES → pass through (our own SendInput output)
       ↓ NO
Is IME active? → NO → pass through (normal English typing)
       ↓ YES
Is it a special key (F11/F12/Ctrl+N/etc.)? → handle specially
       ↓ NO
Map VK code to ASCII character (respecting Shift state)
       ↓
Append character to self._buf (Roman buffer)
       ↓
Call self._update():
  1. new_text = engine.transliterate(self._buf)
  2. Find common prefix between self._screen and new_text
  3. If new suffix starts with combining mark (Mc/Mn), back up 1 position
  4. Build atomic SendInput batch:
     - Backspaces to erase changed suffix of old screen text
     - Unicode characters to type new suffix
  5. Send everything in ONE SendInput call
  6. Update self._screen = new_text
  7. Query suggestions → update popup
       ↓
Return 1 (suppress original keystroke)
```

### Transliteration Pipeline

```
Roman input: "namaskAra"
       ↓
[Greedy left-to-right scan]
  n → न (consonant)
  a → (vowel 'a' = inherent, no mark needed)
  m → म (consonant, virama after न → न्म... wait, 'a' came first → नम)
  ...full parse...
       ↓
Devanagari: नमस्कार (canonical)
       ↓
[Script conversion] (if target ≠ Devanagari)
  Devanagari U+0915 (क) → Kannada U+0C95 (ಕ)  [offset-based mapping]
       ↓
Kannada: ನಮಸ್ಕಾರ
       ↓
[Post-processing]
  Hindi: delete final schwa (भारत not भारत्)
  Tamil: apply special consonant rules
  Others: pass through
```

### Screen Diff Algorithm

```
Old screen: ನಮಸ್ಕಾರ  (from "namaskAra")
New screen: ನಮಸ್ಕಾ    (from "namaskA", after backspace removed 'r')

Common prefix: ನಮಸ್ಕಾ (6 chars)
Erase: ರ (1 backspace)
Type: (nothing)

Result: 2 SendInput events (1 backspace key down + up)
Instead of: 14 events (7 backspaces + 6 chars + their key-ups) if we erased everything
```

---

## Project Structure

```
varnaakshara-ime/
├── varnaakshara_ime.py       # Main IME: keyboard hook, tray app, event loop (1411 lines)
│                              #   - Win32 keyboard hook (WH_KEYBOARD_LL)
│                              #   - IMEEngine class: buffer management, transliteration, diff updates
│                              #   - System tray with PyQt5 (dynamic icon, right-click menu)
│                              #   - Single instance guard (named mutex)
│                              #   - Settings integration, update checking
│
├── transliteration.py         # Baraha → Unicode engine (1197 lines)
│                              #   - BARAHA_VOWELS (23), BARAHA_VOWEL_SIGNS (23)
│                              #   - BARAHA_CONSONANTS (61), BARAHA_YOGAVAAHAS (3)
│                              #   - BARAHA_SYMBOLS (7), BARAHA_DIGITS (10)
│                              #   - DEVA_TO_KANNADA (93), DEVA_TO_TELUGU (90)
│                              #   - DEVA_TO_TAMIL (75), DEVA_TO_MALAYALAM (84)
│                              #   - DEVA_TO_BENGALI (90), DEVA_TO_GUJARATI (82)
│                              #   - DEVA_TO_GURMUKHI (86), DEVA_TO_ODIA (82)
│                              #   - LANGUAGES dict (12 entries)
│                              #   - TransliterationEngine class
│                              #   - ANSI conversion functions
│
├── suggestions.py             # Dictionary lookup + personal learning (284 lines)
│                              #   - SuggestionEngine class
│                              #   - 731K+ word dictionary (embedded/loaded)
│                              #   - Prefix matching, frequency ranking
│                              #   - Learned word persistence (JSON)
│                              #   - LANG_CODES for all 12 languages
│
├── suggestion_popup.py        # Win32 popup window for suggestions (223 lines)
│                              #   - SuggestionPopup class
│                              #   - WS_EX_TOPMOST | WS_EX_TOOLWINDOW | WS_EX_NOACTIVATE
│                              #   - 14pt Nirmala UI font
│                              #   - 3-tier caret positioning
│                              #   - Keyboard selection support
│
├── suggestion_popup_qt.py     # Alternative Qt-based popup (200 lines)
│
├── settings_ui.py             # Settings dialog (533 lines)
│                              #   - PyQt5 widget with config persistence
│                              #   - Language, startup, indicator, suggestions
│
├── updater.py                 # Auto-update from GitHub releases (261 lines)
│                              #   - Version comparison, download, silent install
│                              #   - CURRENT_VERSION = "1.1.0"
│                              #   - GITHUB_REPO = "Exaggarate/Varnaakshara"
│
├── app.py                     # Standalone text editor (702 lines, future Varnaakshara App)
├── varnaakshara_ime_mac.py    # macOS port (1190 lines, in progress)
├── launcher.py                # Process launcher utility (42 lines)
├── font_installer.py          # Font installation utilities (264 lines)
│
├── build.bat                  # Windows build script (PyInstaller)
├── build_mac.sh               # macOS build script
├── icon.ico                   # Application icon
│
├── fonts/
│   ├── unicode/               # 7 Noto Sans TTF fonts
│   │   ├── NotoSansBengali.ttf
│   │   ├── NotoSansDevanagari.ttf
│   │   ├── NotoSansGujarati.ttf
│   │   ├── NotoSansKannada-Regular.ttf
│   │   ├── NotoSansMalayalam.ttf
│   │   ├── NotoSansTamil.ttf
│   │   └── NotoSansTelugu.ttf
│   ├── ansi/                  # 23 BRH legacy fonts (.ttf)
│   ├── NotoSansKannadaVedic.ttf     # Patched dīrgha svarita glyph
│   ├── NotoSansDevanagariVedic.ttf  # Patched dīrgha svarita glyph
│   └── VEDIC_FONTS.md              # Documentation of font patching approach
│
├── installer/
│   ├── varnaakshara_setup.iss  # Inno Setup script (full installer config)
│   ├── LICENSE.txt
│   ├── README_INSTALL.txt
│   ├── dmg_background.png      # macOS DMG background
│   ├── dmg_background.py       # macOS DMG background generator
│   └── output/                 # Built installers
│       ├── Varnaakshara_Setup_v1.0.0.exe
│       ├── Varnaakshara_Setup_v1.1.0.exe
│       ├── Varnaakshara_Setup_v1.1.3.exe
│       └── Varnaakshara_Setup_v1.2.0.exe  ← current
│
└── tests/
    └── test_transliteration.py  # 144 unit tests (70 test functions, many parametrized)
```

---

## Building from Source

### Prerequisites
- Python 3.8+
- PyQt5 (`pip install PyQt5`)
- PyInstaller (`pip install pyinstaller`) — for building .exe

### Windows Build

```bash
cd varnaakshara-ime

# Run directly from source
python varnaakshara_ime.py

# Or build standalone .exe
python build.bat
# Output: dist/Varnaakshara.exe (~42.5 MB)
```

### Building the Installer

1. Build `Varnaakshara.exe` (above)
2. Copy `dist/Varnaakshara.exe` to `installer/dist/`
3. Install [Inno Setup 6](https://jrsoftware.org/isinfo.php)
4. Run: `iscc.exe installer/varnaakshara_setup.iss`
5. Output: `installer/output/Varnaakshara_Setup_v1.2.0.exe`

### macOS (In Progress)
```bash
chmod +x build_mac.sh
./build_mac.sh
```

---

## Testing

```bash
cd varnaakshara-ime
python -m pytest tests/test_transliteration.py -v
```

**144 tests** across 70 test functions (many are parametrized), covering:

- **Engine basics:** default language, language switching, empty input, process_key/flush
- **All 12 scripts:** basic transliteration per language verified
- **Vowels:** all 23 standalone + dependent forms
- **Consonants:** all basic, retroflex, aspirated, nukta variants
- **Case sensitivity:** `T` vs `t`, `D` vs `d`, `N` vs `n`, `S` vs `s`, `K` vs `k`, `G` vs `g`
- **Conjuncts:** `ksha`, `jna`, arbitrary consonant clusters
- **Yogavāhas:** anusvāra, visarga, chandrabindu (standalone + after consonant)
- **Special characters:** avagraha, danda, double danda, OM symbol
- **Vedic marks:** svarita, anudātta, dīrgha svarita
- **Hindi-specific:** schwa deletion, no short e/o, conjunct formation
- **Tamil-specific:** unique consonants, retroflex zh/Lx
- **Digits:** Devanagari and Kannada numeral conversion
- **ZWJ/ZWNJ:** caret and double-caret handling
- **ANSI conversion:** Kannada and Hindi Unicode→ANSI font mapping
- **Edge cases:** long conjunct chains, mixed text, multiple standalone vowels, word boundaries
- **Meta:** vowel/consonant table completeness, language registry integrity, virama constant

---

## Changelog

### v1.2.0 (2026-06-16) — Current Release
- **Smart backspace** — diff-based removal, one transliteration step per press
- **Avagraha** (`&` → ऽ) — fixed routing through transliteration buffer
- **OM symbol** — `OM.` triggers ॐ (period consumed), `OM` stays as normal ओं
- **Danda fix** — `|`/`||` no longer cause spurious virama before the danda
- **Vedic swaras** — `#` (svarita), `$` (anudātta), `##` (dīrgha svarita)
- **Suggestion popup rewrite** — 14pt font, 3-tier caret positioning, keyboard nav
- **Multi-char symbol priority** — `||` and `##` checked before single `|`/`#`
- **Vedic fonts** — patched Noto Sans with corrected U+1CDA glyph
- **Project renamed** from `indic-type` to `varnaakshara-ime`

### v1.1.x (2026-06-14 – 2026-06-15)
- Inno Setup installer with font bundling (32 fonts)
- Auto-updater (GitHub releases API)
- Settings UI (PyQt5 dialog)
- Per-user font registration (HKCU, no admin)
- System tray with dynamic language icon
- Indian numerals toggle
- Suggestion engine with 731K+ dictionary
- Personal word learning (★ markers)

### v1.0.0 (2026-06-13 – 2026-06-14)
- Initial release
- 12-language transliteration engine (Baraha scheme)
- Low-level keyboard hook
- System tray application
- Basic word suggestions
- PyInstaller packaging

---

## Future Plans

- **macOS port** — `varnaakshara_ime_mac.py` (1190 lines) exists, uses CGEvent tap instead of Win32 hooks. Needs testing and packaging (.dmg)
- **Linux/IBus** — port the transliteration engine to IBus framework
- **Varnaakshara App** — standalone text editor with:
  - Script-to-script conversion (type in one script, convert to another)
  - ISO 15919 / IAST romanization output
  - Spell checker for Indian languages
  - Script-order sorting (alphabetical in Indic order)
  - Dictionary lookup
  - Google Translate integration
- **`q` and `Q` keys** — currently unused in Baraha scheme, available for future mapping

---

## License

Free software. Not for sale.

## Credits

- **Baraha phonetic scheme** — created by Sheshadrivasu Chandrasekharan
- **Noto Sans fonts** — Google Fonts (Apache License 2.0)
- **BRH ANSI fonts** — Baraha Software
- Built with Python, PyQt5, Win32 API, ctypes
