"""
Varnaakshara — Settings Panel
Opens from system tray. Configure language, hotkeys, startup, appearance.
No editor bloat — the IME works system-wide.
"""

import sys
import os
import json
import platform

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QCheckBox, QFrame, QScrollArea, QApplication,
    QGroupBox, QSlider, QSpinBox, QGridLayout, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QMessageBox, QAbstractItemView, QRadioButton, QButtonGroup
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap, QPainter

# Import LANGUAGES — prefer new engine, fall back to old
try:
    from core.engine.transliteration import SUPPORTED_LANGUAGES as LANGUAGES
except ImportError:
    from transliteration import LANGUAGES


# ── Config persistence ──

def _config_dir():
    if platform.system() == 'Windows':
        base = os.environ.get('APPDATA', os.path.expanduser('~'))
        return os.path.join(base, 'Varnaakshara')
    return os.path.join(os.path.expanduser('~'), '.varnaakshara')

def _config_path():
    return os.path.join(_config_dir(), 'settings.json')

def _custom_mappings_path():
    return os.path.join(_config_dir(), 'custom_mappings.json')

def load_custom_mappings():
    """Load user custom key mappings from custom_mappings.json."""
    path = _custom_mappings_path()
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def create_default_custom_mappings():
    """Create a template custom_mappings.json if it doesn't exist."""
    path = _custom_mappings_path()
    if os.path.exists(path):
        return path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    template = {
        "_comment": "Custom key mappings for Varnaakshara IME. Values are Unicode characters or escape sequences.",
        "_docs": "Add your own key->character mappings below. These override the active scheme (Baraha/ITRANS).",
        "_example": {
            "consonants": {"q": "\u0958"},
            "vowels": {},
            "vowel_signs": {},
            "symbols": {},
            "yogavaahas": {}
        },
        "consonants": {},
        "vowels": {},
        "vowel_signs": {},
        "symbols": {},
        "yogavaahas": {}
    }
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    return path


def load_config():
    path = _config_path()
    defaults = {
        'language': 'kannada',
        'scheme': 'baraha',
        'input_mode': 'phonetic_baraha',
        'output_mode': 'unicode',
        'ansi_font_family': 'baraha',
        'clipboard_hotkey': 'ctrl+shift+c',
        'start_active': False,
        'run_at_startup': False,
        'show_indicator': True,
        'indicator_opacity': 80,
        'suggestion_count': 5,
        'suggestions_enabled': False,
        'sound_on_toggle': False,
        'theme': 'dark',
    }
    try:
        if os.path.exists(path):
            with open(path, 'r') as f:
                saved = json.load(f)
            defaults.update(saved)
    except Exception:
        pass
    return defaults


def save_config(config):
    path = _config_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)


# ── Styles ──

DARK_STYLE = """
QWidget#settingsRoot {
    background-color: #0D0D12;
}
QLabel {
    color: #B8A9C9;
    background: transparent;
    border: none;
}
QLabel#sectionTitle {
    color: #C9973E;
    font-size: 13px;
    font-weight: bold;
    padding: 4px 0;
}
QLabel#headerTitle {
    color: #C9973E;
    font-size: 20px;
    font-weight: bold;
}
QLabel#headerSubtitle {
    color: #7A6B8A;
    font-size: 9px;
    letter-spacing: 2px;
}
QLabel#versionLabel {
    color: #4A3D5C;
    font-size: 10px;
}
QComboBox {
    background-color: #1E1828;
    color: #E8D5F5;
    border: 1px solid #3D2E50;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 12px;
    min-height: 20px;
}
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background-color: #1E1828;
    color: #E8D5F5;
    selection-background-color: #3D2E50;
    border: 1px solid #3D2E50;
}
QCheckBox {
    color: #B8A9C9;
    font-size: 12px;
    spacing: 8px;
    background: transparent;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid #3D2E50;
    background-color: #1E1828;
}
QCheckBox::indicator:checked {
    background-color: #C9973E;
    border-color: #C9973E;
}
QCheckBox::indicator:hover {
    border-color: #C9973E;
}
QRadioButton {
    color: #B8A9C9;
    font-size: 12px;
    spacing: 8px;
    background: transparent;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #3D2E50;
    background-color: #1E1828;
}
QRadioButton::indicator:checked {
    background-color: #C9973E;
    border-color: #C9973E;
}
QRadioButton::indicator:hover {
    border-color: #C9973E;
}
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #2E2240, stop:1 #231A35);
    color: #E8D5F5;
    border: 1px solid #3D2E50;
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 12px;
    font-weight: bold;
    min-height: 18px;
}
QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3D2E50, stop:1 #2E2240);
    border-color: #C9973E;
}
QPushButton#primaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #C9973E, stop:1 #A67B2E);
    color: #0D0D12;
    border: none;
}
QPushButton#primaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #D9A74E, stop:1 #C9973E);
}
QFrame#separator {
    background-color: #2A2035;
    max-height: 1px;
}
QFrame#card {
    background-color: #12101A;
    border: 1px solid #2A2035;
    border-radius: 10px;
}
QSlider::groove:horizontal {
    border: none;
    height: 4px;
    background: #2A2035;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #C9973E;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}
QSlider::sub-page:horizontal {
    background: #C9973E;
    border-radius: 2px;
}
QSpinBox {
    background-color: #1E1828;
    color: #E8D5F5;
    border: 1px solid #3D2E50;
    border-radius: 6px;
    padding: 4px 8px;
    font-size: 12px;
}
QScrollArea {
    border: none;
    background: transparent;
}
QScrollBar:vertical {
    background: #0D0D12;
    width: 8px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #2A2035;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background: #3D2E50;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""


class CustomMappingsDialog(QDialog):
    """In-app editor for custom key→character mappings."""

    CATEGORIES = ['consonants', 'vowels', 'vowel_signs', 'symbols', 'yogavaahas']
    CAT_LABELS = {
        'consonants': 'Consonant',
        'vowels': 'Vowel',
        'vowel_signs': 'Vowel Sign',
        'symbols': 'Symbol',
        'yogavaahas': 'Yogavaaha',
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Varnaakshara — Custom Mappings')
        self.setMinimumSize(560, 420)
        self.resize(620, 500)
        self._changed = False

        # Dark theme matching Typing Reference
        self.setStyleSheet("""
            QDialog { background: #1E1E2E; color: #CDD6F4; }
            QLabel { color: #CDD6F4; }
            QComboBox {
                background: #313244; color: #CDD6F4; border: 1px solid #45475A;
                border-radius: 4px; padding: 4px 8px;
            }
            QComboBox::drop-down { border: none; }
            QComboBox QAbstractItemView {
                background: #313244; color: #CDD6F4; selection-background-color: #45475A;
            }
            QLineEdit {
                background: #313244; color: #CDD6F4; border: 1px solid #45475A;
                border-radius: 4px; padding: 4px 8px;
            }
            QLineEdit:focus { border: 1px solid #89B4FA; }
            QPushButton {
                background: #45475A; color: #CDD6F4; border: none;
                border-radius: 4px; padding: 6px 16px; font-size: 12px;
            }
            QPushButton:hover { background: #585B70; }
        """)

        root = QVBoxLayout(self)
        root.setSpacing(12)

        # Header
        title = QLabel('Custom Key Mappings')
        title.setStyleSheet('font-size: 18px; font-weight: bold; color: #CDD6F4;')
        root.addWidget(title)

        desc = QLabel(
            'Add your own key\u2192character overrides. '
            'These are applied on top of the active scheme (Baraha / ITRANS).'
        )
        desc.setWordWrap(True)
        desc.setStyleSheet('color: #aaa; font-size: 11px; margin-bottom: 2px;')
        root.addWidget(desc)

        # Warning
        warning = QLabel(
            '\u26a0\ufe0f  Custom mappings can override built-in keys and may cause '
            'unexpected transliteration behavior. Use at your own risk.'
        )
        warning.setWordWrap(True)
        warning.setStyleSheet(
            'background: #3B2A1A; color: #FAB387; font-size: 11px; '
            'padding: 6px 10px; border-radius: 4px; border: 1px solid #5A3D20; '
            'margin-bottom: 4px;'
        )
        root.addWidget(warning)

        # Table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(['Category', 'Key', 'Character'])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet(
            'QTableWidget { background: #1E1E2E; color: #CDD6F4; gridline-color: #45475A; }'
            'QHeaderView::section { background: #313244; color: #CDD6F4; padding: 4px; border: 1px solid #45475A; }'
            'QTableWidget::item:selected { background: #45475A; }'
        )
        root.addWidget(self.table)

        # Add-row form
        form_row = QHBoxLayout()
        form_row.setSpacing(8)

        self.cat_combo = QComboBox()
        for cat in self.CATEGORIES:
            self.cat_combo.addItem(self.CAT_LABELS[cat], cat)
        self.cat_combo.setFixedWidth(120)
        form_row.addWidget(self.cat_combo)

        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText('Key (e.g. q, xx, f)')
        self.key_input.setFixedWidth(140)
        form_row.addWidget(self.key_input)

        self.char_input = QLineEdit()
        self.char_input.setPlaceholderText('Character (paste or \\uXXXX)')
        self.char_input.setFixedWidth(180)
        form_row.addWidget(self.char_input)

        add_btn = QPushButton('+ Add')
        add_btn.setFixedHeight(30)
        add_btn.setStyleSheet('background: #A6E3A1; color: #1E1E2E; font-weight: bold; border-radius: 4px;')
        add_btn.clicked.connect(self._add_mapping)
        form_row.addWidget(add_btn)

        root.addLayout(form_row)

        # Bottom buttons
        btn_row = QHBoxLayout()

        del_btn = QPushButton('🗑 Delete Selected')
        del_btn.setFixedHeight(32)
        del_btn.setStyleSheet('color: #F38BA8;')
        del_btn.clicked.connect(self._delete_selected)
        btn_row.addWidget(del_btn)

        btn_row.addStretch()

        save_btn = QPushButton('  Save  ')
        save_btn.setFixedHeight(32)
        save_btn.setStyleSheet('background: #89B4FA; color: #1E1E2E; font-weight: bold; border-radius: 4px; padding: 0 20px;')
        save_btn.clicked.connect(self._save)
        btn_row.addWidget(save_btn)

        cancel_btn = QPushButton('  Cancel  ')
        cancel_btn.setFixedHeight(32)
        cancel_btn.clicked.connect(self.close)
        btn_row.addWidget(cancel_btn)

        root.addLayout(btn_row)

        # Load existing
        self._load()

    def _load(self):
        """Load mappings from JSON into the table."""
        cm = load_custom_mappings()
        self.table.setRowCount(0)
        for cat in self.CATEGORIES:
            entries = cm.get(cat, {})
            if isinstance(entries, dict):
                for key, char in entries.items():
                    self._insert_row(cat, key, char)

    def _insert_row(self, category, key, char):
        row = self.table.rowCount()
        self.table.insertRow(row)

        cat_item = QTableWidgetItem(self.CAT_LABELS.get(category, category))
        cat_item.setData(Qt.UserRole, category)
        cat_item.setFlags(cat_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, 0, cat_item)

        key_item = QTableWidgetItem(key)
        key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)
        key_item.setFont(QFont('Consolas', 11))
        self.table.setItem(row, 1, key_item)

        char_item = QTableWidgetItem(char)
        char_item.setFlags(char_item.flags() & ~Qt.ItemIsEditable)
        char_item.setFont(QFont('Noto Sans Devanagari', 14))
        self.table.setItem(row, 2, char_item)

    def _add_mapping(self):
        key = self.key_input.text().strip()
        char_raw = self.char_input.text().strip()
        if not key or not char_raw:
            return

        # Parse \uXXXX escape sequences (user types literal backslash-u)
        import re
        char = re.sub(
            r'\\u([0-9A-Fa-f]{4})',
            lambda m: chr(int(m.group(1), 16)),
            char_raw
        )

        cat = self.cat_combo.currentData()

        # Check for duplicate key in same category
        for r in range(self.table.rowCount()):
            if (self.table.item(r, 0).data(Qt.UserRole) == cat and
                    self.table.item(r, 1).text() == key):
                self.table.item(r, 2).setText(char)
                self._changed = True
                self.key_input.clear()
                self.char_input.clear()
                return

        self._insert_row(cat, key, char)
        self._changed = True
        self.key_input.clear()
        self.char_input.clear()
        self.key_input.setFocus()

    def _delete_selected(self):
        row = self.table.currentRow()
        if row >= 0:
            self.table.removeRow(row)
            self._changed = True

    def _save(self):
        """Build the mappings dict from table and write to JSON."""
        cm = {cat: {} for cat in self.CATEGORIES}
        for r in range(self.table.rowCount()):
            cat = self.table.item(r, 0).data(Qt.UserRole)
            key = self.table.item(r, 1).text()
            char = self.table.item(r, 2).text()
            if cat in cm:
                cm[cat][key] = char

        path = _custom_mappings_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(cm, f, indent=2, ensure_ascii=False)

        self._changed = False
        self.accept()


class TypingReferenceDialog(QDialog):
    """In-app typing reference showing all key mappings."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Varnaakshara \u2014 Typing Reference')
        self.setMinimumSize(640, 520)
        self.resize(720, 640)

        # Dark theme for entire dialog
        self.setStyleSheet("""
            QDialog { background: #1E1E2E; color: #CDD6F4; }
            QScrollArea { border: none; background: #1E1E2E; }
            QWidget#refContent { background: #1E1E2E; }
            QPushButton {
                background: #45475A; color: #CDD6F4; border: none;
                border-radius: 4px; padding: 6px 20px; font-size: 12px;
            }
            QPushButton:hover { background: #585B70; }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)

        # Header
        title = QLabel('How to Type')
        title.setStyleSheet('font-size: 20px; font-weight: bold; color: #CDD6F4; margin-bottom: 4px;')
        layout.addWidget(title)

        subtitle = QLabel('Key mappings for the active transliteration scheme')
        subtitle.setStyleSheet('font-size: 11px; color: #6C7086; margin-bottom: 8px;')
        layout.addWidget(subtitle)

        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setObjectName('refContent')
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(6)

        # Add sections
        sections = [
            ('Vowels', [
                ('a', '\u0905'), ('A / aa', '\u0906'), ('i', '\u0907'), ('I / ii', '\u0908'),
                ('u', '\u0909'), ('U / oo', '\u090A'), ('e', '\u090F'), ('E / ee', '\u090F'),
                ('ai', '\u0910'), ('o', '\u0913'), ('O', '\u0913'), ('au', '\u0914'),
                ('Ru', '\u090B'), ('RU', '\u0960'),
            ]),
            ('Consonants \u2014 Ka to Ma varga', [
                ('k', '\u0915'), ('K / kh', '\u0916'), ('g', '\u0917'), ('G / gh', '\u0918'), ('~g', '\u0919'),
                ('c / ch', '\u091A'), ('C / Ch', '\u091B'), ('j', '\u091C'), ('J / jh', '\u091D'), ('~j', '\u091E'),
                ('T', '\u091F'), ('Th', '\u0920'), ('D', '\u0921'), ('Dh', '\u0922'), ('N', '\u0923'),
                ('t', '\u0924'), ('th', '\u0925'), ('d', '\u0926'), ('dh', '\u0927'), ('n', '\u0928'),
                ('p', '\u092A'), ('P / ph', '\u092B'), ('b', '\u092C'), ('B / bh', '\u092D'), ('m', '\u092E'),
            ]),
            ('Consonants \u2014 Semi-vowels & Sibilants', [
                ('y', '\u092F'), ('r', '\u0930'), ('l', '\u0932'), ('v / w', '\u0935'), ('L', '\u0933'),
                ('S / sh', '\u0936'), ('Sh', '\u0937'), ('s', '\u0938'), ('h', '\u0939'),
            ]),
            ('Special Conjuncts', [
                ('kSh', '\u0915\u094D\u0937'), ('j~j', '\u091C\u094D\u091E'),
            ]),
            ('Symbols & Marks', [
                ('M', '\u0902  anusvara'), ('H', '\u0903  visarga'), ('~M', '\u0901  chandrabindu'),
                ('&', '\u093D  avagraha'), ('|', '\u0964  danda'), ('||', '\u0965  double danda'),
                ('OM.', '\u0950  Om'), ('^', 'ZWJ'), ('^^', 'ZWNJ'),
            ]),
            ('Vedic Marks', [
                ('#', '\u0951  svarita'), ('$', '\u0952  anudatta'), ('##', '\u1CDA  dirgha svarita'),
            ]),
        ]

        for section_title, mappings in sections:
            # Section header
            header = QLabel(section_title)
            header.setStyleSheet('font-size: 14px; font-weight: bold; color: #F5C2E7; margin-top: 14px; margin-bottom: 6px;')
            content_layout.addWidget(header)

            # Grid of key\u2192char pairs
            grid = QGridLayout()
            grid.setSpacing(6)
            grid.setColumnMinimumWidth(1, 80)
            grid.setColumnMinimumWidth(3, 80)
            for idx, (key, char) in enumerate(mappings):
                row = idx // 2
                col_offset = (idx % 2) * 2

                key_lbl = QLabel(key)
                key_lbl.setStyleSheet(
                    'font-family: Consolas, monospace; font-size: 12px; '
                    'background: #313244; color: #CDD6F4; '
                    'padding: 4px 10px; border-radius: 4px;'
                )
                key_lbl.setFixedHeight(28)

                char_lbl = QLabel(f'\u2192 {char}')
                char_lbl.setStyleSheet(
                    'font-size: 16px; color: #A6E3A1; padding: 4px 6px;'
                )
                char_lbl.setFixedHeight(28)

                grid.addWidget(key_lbl, row, col_offset)
                grid.addWidget(char_lbl, row, col_offset + 1)

            content_layout.addLayout(grid)

        content_layout.addStretch()
        scroll.setWidget(content)
        layout.addWidget(scroll)

        # Close button
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignRight)


class SettingsPanel(QWidget):
    """Varnaakshara settings — opens from system tray."""

    settings_changed = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setObjectName('settingsRoot')
        self.setWindowTitle('Varnaakshara — Settings')
        self.setFixedSize(480, 640)
        self.setStyleSheet(DARK_STYLE)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ──
        header = QWidget()
        header.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1A0E28, stop:0.5 #201030, stop:1 #1A0E28);
            }
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(24, 20, 24, 16)
        header_layout.setSpacing(4)

        title = QLabel('वर्णाक्षर')
        title.setObjectName('headerTitle')
        title.setFont(QFont('Noto Sans Devanagari', 20, QFont.Bold))
        header_layout.addWidget(title)

        subtitle = QLabel('VARNAAKSHARA  ·  Settings')
        subtitle.setObjectName('headerSubtitle')
        header_layout.addWidget(subtitle)

        # Gold line
        gold_line = QFrame()
        gold_line.setFixedHeight(2)
        gold_line.setStyleSheet('background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop:0.2 #C9973E, stop:0.8 #C9973E, stop:1 transparent);')

        root.addWidget(header)
        root.addWidget(gold_line)

        # ── Scrollable content ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content = QWidget()
        content.setStyleSheet('background: #0D0D12;')
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(20)

        # ── Section: Language ──
        content_layout.addWidget(self._section_title('Language'))

        lang_card = self._card()
        lang_inner = QVBoxLayout(lang_card)
        lang_inner.setContentsMargins(16, 16, 16, 16)
        lang_inner.setSpacing(12)

        lang_row = QHBoxLayout()
        lang_row.addWidget(QLabel('Default language'))
        lang_row.addStretch()
        self.lang_combo = QComboBox()
        for key, lang in LANGUAGES.items():
            self.lang_combo.addItem(f"{lang['name']}", key)
        self._set_combo_value(self.lang_combo, self.config['language'])
        self.lang_combo.setMinimumWidth(160)
        lang_row.addWidget(self.lang_combo)
        lang_inner.addLayout(lang_row)

        # Input mode selector (replaces old scheme selector)
        input_mode_row = QHBoxLayout()
        input_mode_row.addWidget(QLabel('Input mode'))
        input_mode_row.addStretch()
        self.input_mode_combo = QComboBox()
        self.input_mode_combo.addItem('Phonetic (Baraha)', 'phonetic_baraha')
        self.input_mode_combo.addItem('Phonetic (ITRANS)', 'phonetic_itrans')
        self.input_mode_combo.addItem('INSCRIPT Keyboard', 'inscript')
        self._set_combo_value(self.input_mode_combo,
                              self.config.get('input_mode', 'phonetic_baraha'))
        self.input_mode_combo.setMinimumWidth(180)
        input_mode_row.addWidget(self.input_mode_combo)
        lang_inner.addLayout(input_mode_row)

        # Keep scheme_combo for backward compat (hidden, synced with input_mode)
        self.scheme_combo = QComboBox()
        self.scheme_combo.addItem('Baraha (default)', 'baraha')
        self.scheme_combo.addItem('ITRANS (academic)', 'itrans')
        self._set_combo_value(self.scheme_combo, self.config.get('scheme', 'baraha'))
        self.scheme_combo.setVisible(False)
        lang_inner.addWidget(self.scheme_combo)

        # Output mode selector
        output_mode_row = QHBoxLayout()
        output_mode_row.addWidget(QLabel('Output format'))
        output_mode_row.addStretch()
        self.output_mode_combo = QComboBox()
        self.output_mode_combo.addItem('Unicode (standard)', 'unicode')
        self.output_mode_combo.addItem('ANSI (legacy font)', 'ansi')
        self._set_combo_value(self.output_mode_combo,
                              self.config.get('output_mode', 'unicode'))
        self.output_mode_combo.setMinimumWidth(180)
        self.output_mode_combo.currentIndexChanged.connect(self._on_output_mode_changed)
        output_mode_row.addWidget(self.output_mode_combo)
        lang_inner.addLayout(output_mode_row)

        # ANSI font family (shown only when output=ANSI)
        self._ansi_font_row = QHBoxLayout()
        self._ansi_font_label = QLabel('ANSI font family')
        self._ansi_font_row.addWidget(self._ansi_font_label)
        self._ansi_font_row.addStretch()
        self.ansi_font_combo = QComboBox()
        self.ansi_font_combo.addItem('Baraha', 'baraha')
        self.ansi_font_combo.addItem('Shree', 'shree')
        self.ansi_font_combo.addItem('Kruti', 'kruti')
        self._set_combo_value(self.ansi_font_combo,
                              self.config.get('ansi_font_family', 'baraha'))
        self.ansi_font_combo.setMinimumWidth(180)
        self._ansi_font_row.addWidget(self.ansi_font_combo)
        lang_inner.addLayout(self._ansi_font_row)
        # Hide ANSI font row if output mode is not ANSI
        is_ansi = self.config.get('output_mode', 'unicode') == 'ansi'
        self._ansi_font_label.setVisible(is_ansi)
        self.ansi_font_combo.setVisible(is_ansi)

        self.start_active_cb = QCheckBox('Start with transliteration active')
        self.start_active_cb.setChecked(self.config['start_active'])
        lang_inner.addWidget(self.start_active_cb)

        content_layout.addWidget(lang_card)

        # ── Section: Input Mode ──
        content_layout.addWidget(self._section_title('Input Mode'))

        input_mode_card = self._card()
        im_inner = QVBoxLayout(input_mode_card)
        im_inner.setContentsMargins(16, 16, 16, 16)
        im_inner.setSpacing(10)

        self._input_mode_btn_group = QButtonGroup(self)
        self._input_mode_btn_group.setExclusive(True)

        self._radio_baraha = QRadioButton('Phonetic (Baraha)')
        self._radio_itrans = QRadioButton('Phonetic (ITRANS)')
        self._radio_inscript = QRadioButton('INSCRIPT')

        self._input_mode_btn_group.addButton(self._radio_baraha)
        self._input_mode_btn_group.addButton(self._radio_itrans)
        self._input_mode_btn_group.addButton(self._radio_inscript)

        current_input_mode = self.config.get('input_mode', 'phonetic_baraha')
        if current_input_mode == 'phonetic_itrans':
            self._radio_itrans.setChecked(True)
        elif current_input_mode == 'inscript':
            self._radio_inscript.setChecked(True)
        else:
            self._radio_baraha.setChecked(True)

        im_inner.addWidget(self._radio_baraha)
        im_inner.addWidget(self._radio_itrans)
        im_inner.addWidget(self._radio_inscript)

        content_layout.addWidget(input_mode_card)

        # ── Section: Output Mode ──
        content_layout.addWidget(self._section_title('Output Mode'))

        output_mode_card = self._card()
        om_inner = QVBoxLayout(output_mode_card)
        om_inner.setContentsMargins(16, 16, 16, 16)
        om_inner.setSpacing(10)

        self._output_mode_btn_group = QButtonGroup(self)
        self._output_mode_btn_group.setExclusive(True)

        self._radio_unicode = QRadioButton('Unicode')
        self._radio_ansi = QRadioButton('ANSI')

        self._output_mode_btn_group.addButton(self._radio_unicode)
        self._output_mode_btn_group.addButton(self._radio_ansi)

        current_output = self.config.get('output_mode', 'unicode')
        if current_output == 'ansi':
            self._radio_ansi.setChecked(True)
        else:
            self._radio_unicode.setChecked(True)

        om_inner.addWidget(self._radio_unicode)
        om_inner.addWidget(self._radio_ansi)

        # ANSI font family dropdown (enabled only when ANSI is selected)
        ansi_row = QHBoxLayout()
        ansi_row.addWidget(QLabel('ANSI Font Family'))
        ansi_row.addStretch()
        self._ansi_font_dropdown = QComboBox()
        self._ansi_font_dropdown.addItem('Baraha', 'baraha')
        self._ansi_font_dropdown.addItem('Shree', 'shree')
        self._ansi_font_dropdown.addItem('Kruti', 'kruti')
        self._set_combo_value(self._ansi_font_dropdown,
                              self.config.get('ansi_font_family', 'baraha'))
        self._ansi_font_dropdown.setMinimumWidth(160)
        self._ansi_font_dropdown.setEnabled(current_output == 'ansi')
        ansi_row.addWidget(self._ansi_font_dropdown)
        om_inner.addLayout(ansi_row)

        # Enable/disable font dropdown based on radio selection
        self._radio_unicode.toggled.connect(
            lambda checked: self._ansi_font_dropdown.setEnabled(not checked)
        )

        content_layout.addWidget(output_mode_card)

        # ── Section: Clipboard ──
        content_layout.addWidget(self._section_title('Clipboard'))

        clipboard_card = self._card()
        clip_inner = QVBoxLayout(clipboard_card)
        clip_inner.setContentsMargins(16, 16, 16, 16)
        clip_inner.setSpacing(10)

        clip_desc = QLabel(
            'Configure the hotkey for clipboard conversion between '
            'Unicode and ANSI formats.'
        )
        clip_desc.setWordWrap(True)
        clip_desc.setStyleSheet('color: #aaa; font-size: 11px;')
        clip_inner.addWidget(clip_desc)

        clip_row = QHBoxLayout()
        clip_row.addWidget(QLabel('Conversion hotkey'))
        clip_row.addStretch()
        self._clip_hotkey_input = QLineEdit()
        self._clip_hotkey_input.setText(
            self.config.get('clipboard_hotkey', 'ctrl+shift+c')
        )
        self._clip_hotkey_input.setFixedWidth(160)
        self._clip_hotkey_input.setPlaceholderText('e.g. ctrl+shift+c')
        self._clip_hotkey_input.setStyleSheet(
            'background-color: #1E1828; color: #E8D5F5; '
            'border: 1px solid #3D2E50; border-radius: 6px; '
            'padding: 6px 12px; font-size: 12px;'
        )
        clip_row.addWidget(self._clip_hotkey_input)
        clip_inner.addLayout(clip_row)

        content_layout.addWidget(clipboard_card)

        # ── Section: Behavior ──
        content_layout.addWidget(self._section_title('Behavior'))

        behavior_card = self._card()
        behavior_inner = QVBoxLayout(behavior_card)
        behavior_inner.setContentsMargins(16, 16, 16, 16)
        behavior_inner.setSpacing(12)

        self.startup_cb = QCheckBox('Launch at system startup')
        self.startup_cb.setChecked(self.config['run_at_startup'])
        behavior_inner.addWidget(self.startup_cb)

        self.sound_cb = QCheckBox('Play sound on toggle')
        self.sound_cb.setChecked(self.config['sound_on_toggle'])
        behavior_inner.addWidget(self.sound_cb)

        # Clipboard conversion hotkey
        clipboard_row = QHBoxLayout()
        clipboard_row.addWidget(QLabel('Clipboard convert hotkey'))
        clipboard_row.addStretch()
        self.clipboard_hotkey_edit = QLineEdit()
        self.clipboard_hotkey_edit.setText(self.config.get('clipboard_hotkey', 'ctrl+shift+c'))
        self.clipboard_hotkey_edit.setFixedWidth(160)
        self.clipboard_hotkey_edit.setPlaceholderText('e.g. ctrl+shift+c')
        self.clipboard_hotkey_edit.setStyleSheet(
            'background-color: #1E1828; color: #E8D5F5; '
            'border: 1px solid #3D2E50; border-radius: 6px; '
            'padding: 6px 12px; font-size: 12px;'
        )
        clipboard_row.addWidget(self.clipboard_hotkey_edit)
        behavior_inner.addLayout(clipboard_row)

        self.suggestions_cb = QCheckBox('Enable word suggestions (experimental)')
        self.suggestions_cb.setChecked(self.config.get('suggestions_enabled', False))
        behavior_inner.addWidget(self.suggestions_cb)

        suggestions_row = QHBoxLayout()
        suggestions_row.addWidget(QLabel('Max suggestions'))
        suggestions_row.addStretch()
        self.suggestion_spin = QSpinBox()
        self.suggestion_spin.setRange(1, 9)
        self.suggestion_spin.setValue(self.config['suggestion_count'])
        self.suggestion_spin.setFixedWidth(60)
        suggestions_row.addWidget(self.suggestion_spin)
        behavior_inner.addLayout(suggestions_row)

        content_layout.addWidget(behavior_card)

        # ── Section: Appearance ──
        content_layout.addWidget(self._section_title('Appearance'))

        appearance_card = self._card()
        appearance_inner = QVBoxLayout(appearance_card)
        appearance_inner.setContentsMargins(16, 16, 16, 16)
        appearance_inner.setSpacing(12)

        self.indicator_cb = QCheckBox('Show floating language indicator')
        self.indicator_cb.setChecked(self.config['show_indicator'])
        appearance_inner.addWidget(self.indicator_cb)

        opacity_row = QHBoxLayout()
        opacity_row.addWidget(QLabel('Indicator opacity'))
        opacity_row.addStretch()
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(20, 100)
        self.opacity_slider.setValue(self.config['indicator_opacity'])
        self.opacity_slider.setFixedWidth(140)
        opacity_row.addWidget(self.opacity_slider)
        self.opacity_label = QLabel(f'{self.config["indicator_opacity"]}%')
        self.opacity_label.setFixedWidth(36)
        opacity_row.addWidget(self.opacity_label)
        self.opacity_slider.valueChanged.connect(
            lambda v: self.opacity_label.setText(f'{v}%')
        )
        appearance_inner.addLayout(opacity_row)

        content_layout.addWidget(appearance_card)

        # ── Section: Custom Mappings ──
        content_layout.addWidget(self._section_title('Custom Mappings'))

        custom_card = self._card()
        custom_inner = QVBoxLayout(custom_card)
        custom_inner.setContentsMargins(16, 16, 16, 16)
        custom_inner.setSpacing(12)

        custom_desc = QLabel('Override or add key\u2192character mappings.\nEdits apply on next launch or scheme change.')
        custom_desc.setWordWrap(True)
        custom_desc.setStyleSheet('color: #aaa; font-size: 11px;')
        custom_inner.addWidget(custom_desc)

        custom_btn_row = QHBoxLayout()
        edit_mappings_btn = QPushButton('✏️ Edit Mappings')
        edit_mappings_btn.setFixedHeight(32)
        edit_mappings_btn.clicked.connect(self._open_mappings_editor)
        custom_btn_row.addWidget(edit_mappings_btn)

        raw_json_btn = QPushButton('📄 Open JSON file')
        raw_json_btn.setFixedHeight(32)
        raw_json_btn.setStyleSheet('color: #888;')
        raw_json_btn.clicked.connect(self._open_custom_mappings)
        custom_btn_row.addWidget(raw_json_btn)

        custom_btn_row.addStretch()
        custom_inner.addLayout(custom_btn_row)

        cm = load_custom_mappings()
        active_count = sum(len(v) for k, v in cm.items() if isinstance(v, dict) and not k.startswith('_'))
        status_text = f'{active_count} custom mapping(s) active' if active_count else 'No custom mappings defined'
        self._custom_status = QLabel(status_text)
        self._custom_status.setStyleSheet('color: #888; font-size: 10px;')
        custom_inner.addWidget(self._custom_status)

        content_layout.addWidget(custom_card)

        # ── Section: Keyboard Shortcuts ──
        content_layout.addWidget(self._section_title('Keyboard Shortcuts'))

        shortcuts_card = self._card()
        sc_inner = QVBoxLayout(shortcuts_card)
        sc_inner.setContentsMargins(16, 16, 16, 16)
        sc_inner.setSpacing(8)

        mod = 'Cmd' if platform.system() == 'Darwin' else 'Ctrl'
        shortcuts = [
            ('Toggle IME', 'F11 / F12'),
            ('Switch language', f'{mod}+1 through {mod}+0'),
            ('English mode', f'{mod}+`'),
            ('Pick suggestion', '1–5'),
            ('Clipboard convert', self.config.get('clipboard_hotkey', f'{mod}+Shift+C')),
        ]
        for label, keys in shortcuts:
            row = QHBoxLayout()
            row.addWidget(QLabel(label))
            row.addStretch()
            key_label = QLabel(keys)
            key_label.setStyleSheet(
                'color: #C9973E; background: rgba(201,151,62,0.10); '
                'border: 1px solid rgba(201,151,62,0.2); border-radius: 4px; '
                'padding: 3px 10px; font-size: 11px;'
            )
            row.addWidget(key_label)
            sc_inner.addLayout(row)

        content_layout.addWidget(shortcuts_card)

        # ── Typing Reference button ──
        ref_btn = QPushButton('\U0001F4D6 Typing Reference')
        ref_btn.setFixedHeight(36)
        ref_btn.clicked.connect(self._show_typing_reference)
        content_layout.addWidget(ref_btn)

        content_layout.addStretch()

        scroll.setWidget(content)
        root.addWidget(scroll)

        # ── Footer ──
        footer = QWidget()
        footer.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1A1520, stop:0.5 #201828, stop:1 #1A1520);
                border-top: 1px solid #2A2035;
            }
        """)
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(24, 12, 24, 12)

        version = QLabel('v1.3.0  ·  Windows')
        version.setObjectName('versionLabel')
        footer_layout.addWidget(version)

        footer_layout.addStretch()

        save_btn = QPushButton('  Save  ')
        save_btn.setObjectName('primaryBtn')
        save_btn.clicked.connect(self._save)
        footer_layout.addWidget(save_btn)

        cancel_btn = QPushButton('  Cancel  ')
        cancel_btn.clicked.connect(self.close)
        footer_layout.addWidget(cancel_btn)

        root.addWidget(footer)

    def _open_mappings_editor(self):
        """Open the in-app custom mappings editor."""
        dlg = CustomMappingsDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            # Refresh status label
            cm = load_custom_mappings()
            active_count = sum(len(v) for k, v in cm.items() if isinstance(v, dict) and not k.startswith('_'))
            status_text = f'{active_count} custom mapping(s) active' if active_count else 'No custom mappings defined'
            self._custom_status.setText(status_text)
            # Emit settings changed so engine reloads
            self._save()

    def _open_custom_mappings(self):
        """Open custom_mappings.json in the default text editor."""
        path = create_default_custom_mappings()
        try:
            import subprocess
            if platform.system() == 'Windows':
                subprocess.Popen(['notepad', path])
            elif platform.system() == 'Darwin':
                subprocess.Popen(['open', path])
            else:
                subprocess.Popen(['xdg-open', path])
        except Exception:
            pass

    def _section_title(self, text):
        lbl = QLabel(text)
        lbl.setObjectName('sectionTitle')
        return lbl

    def _card(self):
        card = QFrame()
        card.setObjectName('card')
        return card

    def _set_combo_value(self, combo, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i)
                return

    def _show_typing_reference(self):
        dlg = TypingReferenceDialog(self)
        dlg.exec_()

    def _on_output_mode_changed(self, index):
        """Show/hide ANSI font family dropdown based on output mode."""
        is_ansi = self.output_mode_combo.currentData() == 'ansi'
        self._ansi_font_label.setVisible(is_ansi)
        self.ansi_font_combo.setVisible(is_ansi)

    def _save(self):
        self.config['language'] = self.lang_combo.currentData()
        # Derive scheme from input_mode for backward compat
        input_mode = self.input_mode_combo.currentData()
        self.config['input_mode'] = input_mode
        if input_mode == 'phonetic_baraha':
            self.config['scheme'] = 'baraha'
        elif input_mode == 'phonetic_itrans':
            self.config['scheme'] = 'itrans'
        else:
            self.config['scheme'] = self.config.get('scheme', 'baraha')
        self.config['output_mode'] = self.output_mode_combo.currentData()
        self.config['ansi_font_family'] = self.ansi_font_combo.currentData()
        self.config['clipboard_hotkey'] = self.clipboard_hotkey_edit.text().strip() or 'ctrl+shift+c'
        self.config['start_active'] = self.start_active_cb.isChecked()
        self.config['run_at_startup'] = self.startup_cb.isChecked()
        self.config['sound_on_toggle'] = self.sound_cb.isChecked()
        self.config['suggestions_enabled'] = self.suggestions_cb.isChecked()
        self.config['suggestion_count'] = self.suggestion_spin.value()
        self.config['show_indicator'] = self.indicator_cb.isChecked()
        self.config['indicator_opacity'] = self.opacity_slider.value()

        # Override from new Input Mode / Output Mode / Clipboard controls
        if self._radio_itrans.isChecked():
            self.config['input_mode'] = 'phonetic_itrans'
            self.config['scheme'] = 'itrans'
        elif self._radio_inscript.isChecked():
            self.config['input_mode'] = 'inscript'
        else:
            self.config['input_mode'] = 'phonetic_baraha'
            self.config['scheme'] = 'baraha'
        self.config['output_mode'] = (
            'ansi' if self._radio_ansi.isChecked() else 'unicode'
        )
        if self._ansi_font_dropdown.currentData():
            self.config['ansi_font_family'] = (
                self._ansi_font_dropdown.currentData()
            )
        clip_hotkey = self._clip_hotkey_input.text().strip()
        if clip_hotkey:
            self.config['clipboard_hotkey'] = clip_hotkey

        save_config(self.config)
        self.settings_changed.emit(self.config)
        self.close()


class FloatingIndicator(QWidget):
    """Tiny floating pill showing active script — e.g. 'ಕ' or 'हि'."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(48, 32)

        self._script_char = 'ಕ'
        self._active = True
        self._opacity = 0.8

    def set_script(self, char, active=True):
        self._script_char = char
        self._active = active
        self.update()

    def set_opacity(self, opacity_pct):
        self._opacity = opacity_pct / 100.0
        self.setWindowOpacity(self._opacity)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        # Background pill
        if self._active:
            p.setBrush(QColor(201, 151, 62, 220))
        else:
            p.setBrush(QColor(42, 32, 53, 200))

        p.setPen(Qt.NoPen)
        p.drawRoundedRect(0, 0, self.width(), self.height(), 16, 16)

        # Script character
        p.setPen(QColor('#0D0D12') if self._active else QColor('#7A6B8A'))
        p.setFont(QFont('Noto Sans Kannada', 14, QFont.Bold))
        p.drawText(self.rect(), Qt.AlignCenter, self._script_char)

        p.end()

    def mousePressEvent(self, event):
        """Allow dragging."""
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()


# ── Script character mapping for indicator ──
SCRIPT_CHARS = {
    'kannada': 'ಕ', 'hindi': 'हि', 'tamil': 'த', 'telugu': 'తె',
    'bengali': 'ব', 'gujarati': 'ગ', 'malayalam': 'മ', 'marathi': 'म',
    'odia': 'ଓ', 'punjabi': 'ਪ', 'sanskrit': 'सं', 'assamese': 'অ',
}


def get_script_char(lang_key):
    return SCRIPT_CHARS.get(lang_key, lang_key[:2])


# ── Standalone test ──
if __name__ == '__main__':
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    app = QApplication(sys.argv)
    app.setFont(QFont('Sans', 10))

    panel = SettingsPanel()
    panel.show()

    # Screenshot
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(500, lambda: (
        panel.grab().save('/tmp/varnaakshara_settings.png', 'PNG'),
        print('Settings screenshot saved'),
        app.quit()
    ))
    app.exec_()
