"""
Varnaakshara - Multi-language Indian Script Typing Tool
Main application with system tray, GUI editor, and format conversion.
Supports phonetic transliteration with Unicode and ANSI output.

Phase 1 MVP: Desktop editor with transliteration + system tray.
"""

import sys
import os
import platform

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLabel, QPushButton, QComboBox, QMenuBar, QMenu,
    QAction, QActionGroup, QSystemTrayIcon, QFileDialog, QMessageBox,
    QStatusBar, QSplitter, QToolBar, QFontComboBox, QSpinBox, QGroupBox,
    QTabWidget, QPlainTextEdit, QShortcut, QDockWidget, QSlider,
    QColorDialog, QFrame, QSizePolicy, QInputDialog, QScrollArea,
    QGraphicsDropShadowEffect, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QSize, QMargins
from PyQt5.QtGui import (
    QIcon, QFont, QKeySequence, QTextCursor, QColor, QPalette, QPixmap,
    QTextCharFormat, QTextBlockFormat, QTextListFormat, QPageSize, QPainter
)
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog

# Import from new table-driven engine, fall back to old module
try:
    from core.engine.transliteration import TransliterationEngine, SUPPORTED_LANGUAGES as LANGUAGES
    _USE_NEW_ENGINE = True
except ImportError:
    from transliteration import TransliterationEngine, LANGUAGES
    _USE_NEW_ENGINE = False

# ANSI conversion: prefer new engine method, fall back to old function
def convert_to_ansi(text, language):
    """Convert Unicode text to ANSI encoding."""
    if _USE_NEW_ENGINE:
        engine = TransliterationEngine(language)
        return engine.to_ansi(text)
    else:
        from transliteration import convert_to_ansi as _old_convert
        return _old_convert(text, language)


# Import platform-specific IME from the ime package
_IME_CLASS = None
if platform.system() == 'Windows':
    try:
        from ime import WindowsIME
        _IME_CLASS = WindowsIME
    except (ImportError, OSError):
        pass
elif platform.system() == 'Darwin':
    try:
        from ime import MacOSIME
        _IME_CLASS = MacOSIME
    except (ImportError, OSError):
        pass


class TranslitEditor(QTextEdit):
    """Custom QTextEdit that intercepts keystrokes for transliteration."""

    transliteration_toggled = pyqtSignal(bool)

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.transliterate_enabled = True
        self.buffer = ''
        self.buffer_start_pos = -1

        # Styling
        self.setFont(QFont('Nirmala UI', 14))  # Windows Indic font
        self.setAcceptRichText(True)

        # Flush timer — commit buffer after short delay
        self.flush_timer = QTimer()
        self.flush_timer.setSingleShot(True)
        self.flush_timer.setInterval(500)  # 500ms
        self.flush_timer.timeout.connect(self._flush_buffer)

    def set_transliteration(self, enabled):
        self.transliterate_enabled = enabled
        if not enabled:
            self._flush_buffer()
        self.transliteration_toggled.emit(enabled)

    def toggle_transliteration(self):
        self.set_transliteration(not self.transliterate_enabled)

    def keyPressEvent(self, event):
        if not self.transliterate_enabled:
            super().keyPressEvent(event)
            return

        key = event.key()
        text = event.text()

        # Let control keys pass through
        if event.modifiers() & (Qt.ControlModifier | Qt.AltModifier):
            self._flush_buffer()
            super().keyPressEvent(event)
            return

        # Navigation / editing keys flush buffer and pass through
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down,
                   Qt.Key_Home, Qt.Key_End, Qt.Key_PageUp, Qt.Key_PageDown,
                   Qt.Key_Delete, Qt.Key_Escape, Qt.Key_Tab):
            self._flush_buffer()
            super().keyPressEvent(event)
            return

        # Backspace — remove from buffer if buffer exists
        if key == Qt.Key_Backspace:
            if self.buffer:
                self.buffer = self.buffer[:-1]
                # Remove the raw char we just added
                cursor = self.textCursor()
                if cursor.position() > 0:
                    cursor.deletePreviousChar()
                    self.setTextCursor(cursor)
                if not self.buffer:
                    self.buffer_start_pos = -1
                self.flush_timer.start()
                return
            else:
                super().keyPressEvent(event)
                return

        # Space / Enter / punctuation — flush buffer first, then insert
        if key in (Qt.Key_Space, Qt.Key_Return, Qt.Key_Enter) or \
           (text and text in '.,;:!?()-[]{}"\'/\\@#$%^&*+=<>|`~'):
            self._flush_buffer()
            super().keyPressEvent(event)
            return

        # Alphabetic / digit input — buffer it
        if text and (text.isalpha() or text.isdigit()):
            if not self.buffer:
                self.buffer_start_pos = self.textCursor().position()

            self.buffer += text
            self.flush_timer.start()

            # Insert raw char for now (will be replaced on flush)
            super().keyPressEvent(event)
            return

        # Anything else — flush and pass through
        self._flush_buffer()
        super().keyPressEvent(event)

    def _flush_buffer(self):
        """Convert buffered text and replace in editor."""
        self.flush_timer.stop()

        if not self.buffer or self.buffer_start_pos < 0:
            self.buffer = ''
            self.buffer_start_pos = -1
            return

        # Transliterate the buffer
        converted = self.engine.transliterate(self.buffer)

        # Replace the raw buffer text with converted text
        cursor = self.textCursor()
        current_pos = cursor.position()
        buffer_end = current_pos

        # Select the raw buffer region
        cursor.setPosition(self.buffer_start_pos)
        cursor.setPosition(buffer_end, QTextCursor.KeepAnchor)

        # Replace with transliterated text
        cursor.insertText(converted)

        self.buffer = ''
        self.buffer_start_pos = -1


class CollapsiblePanel(QWidget):
    """Collapsible panel section for InDesign-style inspector."""
    def __init__(self, title, icon='', parent=None):
        super().__init__(parent)
        self.setObjectName('collapsiblePanel')
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        self._title = title
        self._icon = icon
        self.header = QPushButton(f'▼  {icon}  {title}'.strip())
        self.header.setObjectName('panelHeader')
        self.header.setCheckable(True)
        self.header.setChecked(True)
        self.header.clicked.connect(self._toggle)
        lay.addWidget(self.header)
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(10, 8, 10, 10)
        self.content_layout.setSpacing(6)
        lay.addWidget(self.content)

    def _toggle(self):
        vis = self.header.isChecked()
        self.content.setVisible(vis)
        arrow = '▼' if vis else '▶'
        self.header.setText(f'{arrow}  {self._icon}  {self._title}'.strip())

    def addWidget(self, w):
        self.content_layout.addWidget(w)

    def addLayout(self, la):
        self.content_layout.addLayout(la)


class VarnaaksharaApp(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.engine = TransliterationEngine('kannada')
        self.current_language = 'kannada'
        self.current_file = None

        # Create platform IME instance if available
        self.ime = None
        if _IME_CLASS:
            try:
                self.ime = _IME_CLASS(language='kannada', scheme='baraha')
            except Exception:
                pass

        self.init_ui()
        self.setup_shortcuts()

    def init_ui(self):
        """Build a pro Word/InDesign style UI: ribbon + page canvas + inspector."""
        self.setWindowTitle('Varnaakshara — Document Editor')
        self.setMinimumSize(1400, 900)
        self.setStyleSheet(self._get_stylesheet())
        self.showMaximized()

        # ── Central Widget ──
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Ribbon (tabs + groups) ──
        self.ribbon = QTabWidget()
        self.ribbon.setObjectName('ribbon')
        self.ribbon.setDocumentMode(True)
        self.ribbon.setMovable(False)
        self.ribbon.setElideMode(Qt.ElideNone)
        main_layout.addWidget(self.ribbon, 0)

        def _ribbon_group(title: str) -> QWidget:
            box = QFrame()
            box.setObjectName('ribbonGroup')
            box_layout = QVBoxLayout(box)
            box_layout.setContentsMargins(8, 6, 8, 6)
            box_layout.setSpacing(4)

            row = QWidget()
            row_layout = QHBoxLayout(row)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(6)
            box_layout.addWidget(row, 1)

            label = QLabel(title)
            label.setObjectName('ribbonGroupTitle')
            label.setAlignment(Qt.AlignHCenter)
            box_layout.addWidget(label, 0)

            box._row_layout = row_layout  # type: ignore[attr-defined]
            return box

        def _add_to_group(group: QWidget, w: QWidget):
            group._row_layout.addWidget(w)  # type: ignore[attr-defined]

        # HOME TAB
        home = QWidget()
        home_layout = QHBoxLayout(home)
        home_layout.setContentsMargins(10, 6, 10, 6)
        home_layout.setSpacing(10)

        # Group: Clipboard
        grp_clip = _ribbon_group('CLIPBOARD')
        undo_btn = QPushButton('↩\nUndo')
        undo_btn.setObjectName('ribbonLargeBtn')
        undo_btn.clicked.connect(lambda: self.editor.undo())
        _add_to_group(grp_clip, undo_btn)
        redo_btn = QPushButton('↪\nRedo')
        redo_btn.setObjectName('ribbonLargeBtn')
        redo_btn.clicked.connect(lambda: self.editor.redo())
        _add_to_group(grp_clip, redo_btn)
        home_layout.addWidget(grp_clip)

        # Hidden lang/toggle/format — used by panel + menus
        self.lang_combo = QComboBox()
        for key, lang in LANGUAGES.items():
            self.lang_combo.addItem(lang['name'], key)
        self.lang_combo.currentIndexChanged.connect(self._on_language_changed)
        self.lang_combo.setVisible(False)

        self.toggle_btn = QPushButton('Transliteration ON')
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setChecked(True)
        self.toggle_btn.clicked.connect(self._on_toggle_clicked)
        self.toggle_btn.setVisible(False)

        self.format_combo = QComboBox()
        self.format_combo.addItem('Unicode', 'unicode')
        self.format_combo.addItem('Baraha ANSI', 'baraha')
        self.format_combo.addItem('Shreelipi ANSI', 'shreelipi')
        self.format_combo.currentIndexChanged.connect(self._on_format_combo_changed)
        self.format_combo.setVisible(False)

        # Group: Font
        grp_font = _ribbon_group('Font')
        self.font_family_combo = QFontComboBox()
        # Try Noto Serif Kannada first, fall back to Nirmala UI
        for _fn in ['Noto Serif Kannada', 'Nirmala UI', 'Noto Sans']:
            if QFont(_fn).family():
                self.font_family_combo.setCurrentFont(QFont(_fn))
                break
        self.font_family_combo.setMinimumWidth(220)
        self.font_family_combo.currentFontChanged.connect(self._on_font_family_changed)
        _add_to_group(grp_font, self.font_family_combo)

        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(6, 144)
        self.font_size_spin.setValue(14)
        self.font_size_spin.valueChanged.connect(self._on_font_size_changed)
        self.font_size_spin.setFixedWidth(70)
        _add_to_group(grp_font, self.font_size_spin)

        # Icon-like buttons (still text, but styled)
        self.bold_btn = QPushButton('B')
        self.bold_btn.setObjectName('ribbonIconBtn')
        self.bold_btn.setCheckable(True)
        self.bold_btn.clicked.connect(self._toggle_bold)
        _add_to_group(grp_font, self.bold_btn)

        self.italic_btn = QPushButton('I')
        self.italic_btn.setObjectName('ribbonIconBtn')
        self.italic_btn.setCheckable(True)
        self.italic_btn.clicked.connect(self._toggle_italic)
        _add_to_group(grp_font, self.italic_btn)

        self.underline_btn = QPushButton('U')
        self.underline_btn.setObjectName('ribbonIconBtn')
        self.underline_btn.setCheckable(True)
        self.underline_btn.clicked.connect(self._toggle_underline)
        _add_to_group(grp_font, self.underline_btn)

        self.strike_btn = QPushButton('S')
        self.strike_btn.setObjectName('ribbonIconBtn')
        self.strike_btn.setCheckable(True)
        self.strike_btn.setToolTip('Strikethrough')
        self.strike_btn.clicked.connect(self._toggle_strikethrough)
        _add_to_group(grp_font, self.strike_btn)

        self.text_color_btn = QPushButton('A')
        self.text_color_btn.setObjectName('ribbonIconBtn')
        self.text_color_btn.clicked.connect(self._pick_text_color)
        _add_to_group(grp_font, self.text_color_btn)

        self.highlight_btn = QPushButton('▇')
        self.highlight_btn.setObjectName('ribbonIconBtn')
        self.highlight_btn.clicked.connect(self._pick_highlight_color)
        _add_to_group(grp_font, self.highlight_btn)

        home_layout.addWidget(grp_font)

        # Group: Paragraph
        grp_para = _ribbon_group('Paragraph')
        self.align_left_btn = QPushButton('≡L')
        self.align_left_btn.setObjectName('ribbonIconBtn')
        self.align_left_btn.setCheckable(True)
        self.align_left_btn.setChecked(True)
        self.align_left_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignLeft))
        _add_to_group(grp_para, self.align_left_btn)

        self.align_center_btn = QPushButton('≡C')
        self.align_center_btn.setObjectName('ribbonIconBtn')
        self.align_center_btn.setCheckable(True)
        self.align_center_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignCenter))
        _add_to_group(grp_para, self.align_center_btn)

        self.align_right_btn = QPushButton('≡R')
        self.align_right_btn.setObjectName('ribbonIconBtn')
        self.align_right_btn.setCheckable(True)
        self.align_right_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignRight))
        _add_to_group(grp_para, self.align_right_btn)

        self.align_justify_btn = QPushButton('≡J')
        self.align_justify_btn.setObjectName('ribbonIconBtn')
        self.align_justify_btn.setCheckable(True)
        self.align_justify_btn.clicked.connect(lambda: self._set_alignment(Qt.AlignJustify))
        _add_to_group(grp_para, self.align_justify_btn)

        self._align_buttons = [self.align_left_btn, self.align_center_btn,
                               self.align_right_btn, self.align_justify_btn]

        self.line_spacing_combo = QComboBox()
        self.line_spacing_combo.addItems(['1.0', '1.15', '1.5', '2.0', '2.5', '3.0'])
        self.line_spacing_combo.setCurrentIndex(1)
        self.line_spacing_combo.setFixedWidth(80)
        self.line_spacing_combo.currentTextChanged.connect(self._on_line_spacing_changed)
        _add_to_group(grp_para, QLabel('Spacing'))
        _add_to_group(grp_para, self.line_spacing_combo)

        home_layout.addWidget(grp_para)

        # Group: Styles
        grp_styles = _ribbon_group('Styles')
        self.style_combo = QComboBox()
        self.style_combo.addItems([
            'Normal', 'Title', 'Heading 1', 'Heading 2', 'Heading 3',
            'Subtitle', 'Quote', 'Code'
        ])
        self.style_combo.setMinimumWidth(170)
        self.style_combo.currentTextChanged.connect(self._apply_paragraph_style)
        _add_to_group(grp_styles, self.style_combo)
        home_layout.addWidget(grp_styles)

        home_layout.addStretch(1)
        self.ribbon.addTab(home, 'HOME')

        # INSERT TAB
        insert = QWidget()
        insert_layout = QHBoxLayout(insert)
        insert_layout.setContentsMargins(10, 6, 10, 6)
        insert_layout.setSpacing(10)

        grp_insert = _ribbon_group('Insert')
        btn_hr = QPushButton('Horizontal Rule')
        btn_hr.clicked.connect(self._insert_horizontal_rule)
        _add_to_group(grp_insert, btn_hr)

        btn_pb = QPushButton('Page Break')
        btn_pb.clicked.connect(self._insert_page_break)
        _add_to_group(grp_insert, btn_pb)

        btn_dt = QPushButton('Date/Time')
        btn_dt.clicked.connect(self._insert_datetime)
        _add_to_group(grp_insert, btn_dt)

        btn_sc = QPushButton('Special Char')
        btn_sc.clicked.connect(self._insert_special_char)
        _add_to_group(grp_insert, btn_sc)

        insert_layout.addWidget(grp_insert)
        insert_layout.addStretch(1)
        self.ribbon.addTab(insert, 'INSERT')

        # LAYOUT TAB
        layout_tab = QWidget()
        layout_tab_l = QHBoxLayout(layout_tab)
        layout_tab_l.setContentsMargins(10, 6, 10, 6)
        layout_tab_l.setSpacing(10)

        grp_page = _ribbon_group('PAGE SETUP')
        btn_orient = QPushButton('Orientation')
        btn_orient.setToolTip('Toggle Portrait/Landscape')
        _add_to_group(grp_page, btn_orient)
        btn_margins = QPushButton('Margins')
        _add_to_group(grp_page, btn_margins)
        btn_cols = QPushButton('Columns')
        _add_to_group(grp_page, btn_cols)
        layout_tab_l.addWidget(grp_page)
        layout_tab_l.addStretch(1)
        self.ribbon.addTab(layout_tab, 'LAYOUT')

        # REVIEW TAB
        review_tab = QWidget()
        review_tab_l = QHBoxLayout(review_tab)
        review_tab_l.setContentsMargins(10, 6, 10, 6)
        review_tab_l.setSpacing(10)

        grp_proofing = _ribbon_group('PROOFING')
        btn_wc = QPushButton('Word Count')
        btn_wc.clicked.connect(lambda: QMessageBox.information(self, 'Word Count', self.word_count_label.text()))
        _add_to_group(grp_proofing, btn_wc)
        review_tab_l.addWidget(grp_proofing)
        review_tab_l.addStretch(1)
        self.ribbon.addTab(review_tab, 'REVIEW')

        # TOOLS TAB
        tools_tab = QWidget()
        tools_tab_l = QHBoxLayout(tools_tab)
        tools_tab_l.setContentsMargins(10, 6, 10, 6)
        tools_tab_l.setSpacing(10)

        grp_tools = _ribbon_group('VIEW')
        btn_panel = QPushButton('Toggle Panel')
        btn_panel.clicked.connect(self._toggle_side_panel)
        _add_to_group(grp_tools, btn_panel)
        tools_tab_l.addWidget(grp_tools)
        tools_tab_l.addStretch(1)
        self.ribbon.addTab(tools_tab, 'TOOLS')

        # ── Main content: Editor/Converter + Inspector ──
        content_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(content_splitter, 1)

        # Left: tabs
        self.tabs = QTabWidget()
        self.tabs.setObjectName('mainTabs')
        content_splitter.addWidget(self.tabs)

        # Editor tab with page canvas
        editor_widget = QWidget()
        editor_v = QVBoxLayout(editor_widget)
        editor_v.setContentsMargins(0, 0, 0, 0)
        editor_v.setSpacing(0)

        # Canvas scroll
        self.canvas_scroll = QScrollArea()
        self.canvas_scroll.setWidgetResizable(True)
        self.canvas_scroll.setObjectName('canvasScroll')
        editor_v.addWidget(self.canvas_scroll, 1)

        canvas = QWidget()
        canvas.setObjectName('pasteboard')
        canvas_layout = QVBoxLayout(canvas)
        canvas_layout.setContentsMargins(60, 40, 60, 40)
        canvas_layout.setSpacing(0)
        canvas_layout.addStretch(1)

        # Center holder
        holder = QWidget()
        holder_layout = QHBoxLayout(holder)
        holder_layout.setContentsMargins(0, 0, 0, 0)
        holder_layout.addStretch(1)

        # Page (white) with shadow
        self.page_frame = QFrame()
        self.page_frame.setObjectName('docPage')
        self.page_frame.setFixedWidth(900)

        shadow = QGraphicsDropShadowEffect(self.page_frame)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.page_frame.setGraphicsEffect(shadow)

        page_layout = QVBoxLayout(self.page_frame)
        page_layout.setContentsMargins(70, 70, 70, 70)
        page_layout.setSpacing(0)

        self.editor = TranslitEditor(self.engine)
        self.editor.setPlaceholderText(
            'Start typing in English...\n'
            'Example: namaskaara → ನಮಸ್ಕಾರ\n\n'
            'Ctrl+Space: toggle transliteration\n'
            'Ctrl+L: cycle language'
        )
        self.editor.cursorPositionChanged.connect(self._on_cursor_position_changed)
        self.editor.textChanged.connect(self._update_word_count)
        page_layout.addWidget(self.editor)

        holder_layout.addWidget(self.page_frame)
        holder_layout.addStretch(1)
        canvas_layout.addWidget(holder, 0)
        canvas_layout.addStretch(1)

        self.canvas_scroll.setWidget(canvas)

        self.tabs.addTab(editor_widget, 'Editor')

        # Converter tab (keep existing)
        converter_widget = QWidget()
        conv_layout = QHBoxLayout(converter_widget)

        input_group = QGroupBox('English (Phonetic Input)')
        input_layout = QVBoxLayout(input_group)
        self.conv_input = QPlainTextEdit()
        self.conv_input.setFont(QFont('Consolas', 13))
        self.conv_input.setPlaceholderText('Type or paste English text here...')
        input_layout.addWidget(self.conv_input)
        conv_layout.addWidget(input_group)

        btn_layout = QVBoxLayout()
        btn_layout.addStretch()
        convert_btn = QPushButton('Convert → Unicode')
        convert_btn.setMinimumHeight(46)
        convert_btn.clicked.connect(lambda: self._convert('unicode'))
        btn_layout.addWidget(convert_btn)

        convert_baraha_btn = QPushButton('Convert → Baraha ANSI')
        convert_baraha_btn.setMinimumHeight(46)
        convert_baraha_btn.clicked.connect(lambda: self._convert('baraha'))
        btn_layout.addWidget(convert_baraha_btn)

        convert_shreelipi_btn = QPushButton('Convert → Shreelipi ANSI')
        convert_shreelipi_btn.setMinimumHeight(46)
        convert_shreelipi_btn.clicked.connect(lambda: self._convert('shreelipi'))
        btn_layout.addWidget(convert_shreelipi_btn)

        swap_btn = QPushButton('Swap')
        swap_btn.clicked.connect(self._swap_converter)
        btn_layout.addWidget(swap_btn)
        btn_layout.addStretch()
        conv_layout.addLayout(btn_layout)

        output_group = QGroupBox('Converted Output')
        output_layout = QVBoxLayout(output_group)
        self.conv_output = QPlainTextEdit()
        self.conv_output.setFont(QFont('Nirmala UI', 14))
        self.conv_output.setReadOnly(True)
        self.conv_output.setPlaceholderText('Converted text will appear here...')
        output_layout.addWidget(self.conv_output)

        copy_btn = QPushButton('Copy to Clipboard')
        copy_btn.clicked.connect(self._copy_output)
        output_layout.addWidget(copy_btn)
        conv_layout.addWidget(output_group)

        self.tabs.addTab(converter_widget, 'Converter')

        # Right: InDesign-style dark panels
        self.side_panel = QWidget()
        self.side_panel.setObjectName('sidePanel')
        self.side_panel.setMinimumWidth(280)
        self.side_panel.setMaximumWidth(340)
        panel_scroll = QScrollArea()
        panel_scroll.setObjectName('panelScroll')
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        panel_inner = QWidget()
        panel_inner.setObjectName('sidePanel')
        side_layout = QVBoxLayout(panel_inner)
        side_layout.setContentsMargins(0, 0, 0, 0)
        side_layout.setSpacing(1)

        # Panel header
        panels_hdr = QLabel('PANELS')
        panels_hdr.setObjectName('panelsHeader')
        panels_hdr.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        side_layout.addWidget(panels_hdr)

        # ── ACTIVE LANGUAGE ── (4x3 grid)
        lang_panel = CollapsiblePanel('ACTIVE LANGUAGE', '\U0001f310')
        lang_grid_layout = QGridLayout()
        lang_grid_layout.setSpacing(4)
        self._lang_buttons = {}
        _native = {
            'kannada': '\u0c95\u0ca8\u0ccd\u0ca8\u0ca1', 'hindi': '\u0939\u093f\u0902\u0926\u0940',
            'telugu': '\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41', 'tamil': '\u0ba4\u0bae\u0bbf\u0bb4\u0bcd',
            'malayalam': '\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02', 'marathi': '\u092e\u0930\u093e\u0920\u0940',
            'sanskrit': '\u0938\u0902\u0938\u094d\u0915\u0943\u0924', 'bengali': '\u09ac\u09be\u0982\u09b2\u09be',
            'gujarati': '\u0a97\u0ac1\u0a9c\u0ab0\u0abe\u0aa4\u0ac0', 'punjabi': '\u0a2a\u0a70\u0a1c\u0a3e\u0a2c\u0a40',
            'odia': '\u0b13\u0b21\u0b3c\u0b3f\u0b06'
        }
        _ri, _ci = 0, 0
        for lk in _native:
            lb = QPushButton(_native[lk])
            lb.setObjectName('langGridBtn')
            lb.setCheckable(True)
            lb.setChecked(lk == 'kannada')
            lb.clicked.connect(lambda ch, k=lk: self._switch_language_from_grid(k))
            lang_grid_layout.addWidget(lb, _ri, _ci)
            self._lang_buttons[lk] = lb
            _ci += 1
            if _ci > 2: _ci = 0; _ri += 1
        lang_panel.addLayout(lang_grid_layout)
        side_layout.addWidget(lang_panel)

        # ── TRANSLITERATE ──
        tl_panel = CollapsiblePanel('TRANSLITERATE', '\u0c85')
        self.translit_input = QPlainTextEdit()
        self.translit_input.setObjectName('translitInput')
        self.translit_input.setMaximumHeight(55)
        self.translit_input.setPlaceholderText('namaskAra lOkavE')
        tl_panel.addWidget(self.translit_input)
        _tl_row = QHBoxLayout()
        _tl_cv = QPushButton('Convert')
        _tl_cv.setObjectName('accentBtn')
        _tl_cv.clicked.connect(self._panel_transliterate)
        _tl_ins = QPushButton('Insert \u2193')
        _tl_ins.clicked.connect(self._panel_insert)
        _tl_row.addWidget(_tl_cv); _tl_row.addWidget(_tl_ins)
        tl_panel.addLayout(_tl_row)
        self.translit_preview = QLabel('')
        self.translit_preview.setObjectName('translitPreview')
        self.translit_preview.setWordWrap(True)
        tl_panel.addWidget(self.translit_preview)
        side_layout.addWidget(tl_panel)

        # ── SCRIPT CONVERTER (collapsed) ──
        _sc = CollapsiblePanel('SCRIPT CONVERTER', '\u2194')
        _sc.header.setChecked(False); _sc.content.setVisible(False)
        _sc.header.setText('\u25b6  \u2194  SCRIPT CONVERTER')
        side_layout.addWidget(_sc)

        # ── UNICODE \u2194 ANSI (collapsed) ──
        _ua = CollapsiblePanel('UNICODE \u2194 ANSI', 'U\u21a4A')
        _ua.header.setChecked(False); _ua.content.setVisible(False)
        _ua.header.setText('\u25b6  U\u21a4A  UNICODE \u2194 ANSI')
        side_layout.addWidget(_ua)

        # ── PANCHAMA VARGA (collapsed) ──
        _pv = CollapsiblePanel('PANCHAMA VARGA', '\u2698')
        _pv.header.setChecked(False); _pv.content.setVisible(False)
        _pv.header.setText('\u25b6  \u2698  PANCHAMA VARGA')
        side_layout.addWidget(_pv)

        # ── DOCUMENT ──
        doc_panel = CollapsiblePanel('DOCUMENT', '\U0001f4c4')
        doc_grid = QGridLayout()
        doc_grid.setHorizontalSpacing(8)
        doc_grid.setVerticalSpacing(6)

        self.page_size_combo = QComboBox(); self.page_size_combo.addItems(['A4', 'Letter', 'Legal', 'A3', 'A5'])
        self.orientation_combo = QComboBox(); self.orientation_combo.addItems(['Portrait', 'Landscape'])
        self.margin_combo = QComboBox(); self.margin_combo.addItems(['Normal (1")', 'Narrow (0.5")', 'Wide (1.5")', 'Custom...'])
        self.columns_combo = QComboBox(); self.columns_combo.addItems(['1', '2', '3'])
        doc_grid.addWidget(QLabel('Page'), 0, 0); doc_grid.addWidget(self.page_size_combo, 0, 1)
        doc_grid.addWidget(QLabel('Orient'), 1, 0); doc_grid.addWidget(self.orientation_combo, 1, 1)
        doc_grid.addWidget(QLabel('Margins'), 2, 0); doc_grid.addWidget(self.margin_combo, 2, 1)
        doc_grid.addWidget(QLabel('Columns'), 3, 0); doc_grid.addWidget(self.columns_combo, 3, 1)
        doc_panel.addLayout(doc_grid)

        self.char_info_label = QLabel('Position: 0 | Line: 1 | Col: 1')
        self.char_info_label.setWordWrap(True)
        doc_panel.addWidget(self.char_info_label)
        side_layout.addWidget(doc_panel)

        side_layout.addStretch(1)
        panel_scroll.setWidget(panel_inner)
        sp_layout = QVBoxLayout(self.side_panel)
        sp_layout.setContentsMargins(0, 0, 0, 0)
        sp_layout.addWidget(panel_scroll)
        content_splitter.addWidget(self.side_panel)

        content_splitter.setSizes([1600, 320])
        content_splitter.setCollapsible(1, True)

        # ── Menu Bar ──
        self._create_menus()

        # ── Status Bar (blue, like design) ──
        status = self.statusBar()
        status.setObjectName('blueStatusBar')
        self.status_page = QLabel('Page 1')
        status.addWidget(self.status_page)
        self.word_count_label = QLabel('0 words')
        status.addWidget(self.word_count_label)
        self.char_count_label = QLabel('0 chars')
        status.addWidget(self.char_count_label)

        # Spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        status.addWidget(spacer)

        # Right side: language indicator + scheme + zoom
        self.status_lang_dot = QLabel('\u25cf')
        self.status_lang_dot.setObjectName('langDot')
        status.addPermanentWidget(self.status_lang_dot)
        self.status_lang = QLabel('Kannada')
        status.addPermanentWidget(self.status_lang)
        self.status_scheme = QLabel('Phonetic')
        status.addPermanentWidget(self.status_scheme)

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(50, 300)
        self.zoom_slider.setValue(100)
        self.zoom_slider.setFixedWidth(120)
        self.zoom_slider.valueChanged.connect(self._on_zoom_changed)
        status.addPermanentWidget(self.zoom_slider)
        self.zoom_label = QLabel('100%')
        self.zoom_label.setFixedWidth(45)
        status.addPermanentWidget(self.zoom_label)

    def _create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('&File')

        new_action = QAction('&New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)

        open_action = QAction('&Open...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)

        save_action = QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)

        save_as_action = QAction('Save &As...', self)
        save_as_action.setShortcut('Ctrl+Shift+S')
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        # Export submenu
        export_menu = file_menu.addMenu('&Export')

        export_unicode = QAction('Export as Unicode (.txt)', self)
        export_unicode.triggered.connect(lambda: self._export('unicode'))
        export_menu.addAction(export_unicode)

        export_baraha = QAction('Export as Baraha ANSI (.txt)', self)
        export_baraha.triggered.connect(lambda: self._export('baraha'))
        export_menu.addAction(export_baraha)

        export_shreelipi = QAction('Export as Shreelipi ANSI (.txt)', self)
        export_shreelipi.triggered.connect(lambda: self._export('shreelipi'))
        export_menu.addAction(export_shreelipi)

        file_menu.addSeparator()

        # Print
        print_action = QAction('&Print...', self)
        print_action.setShortcut('Ctrl+P')
        print_action.triggered.connect(self._print_document)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Alt+F4')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu('&Edit')

        undo_action = QAction('&Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.editor.undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction('&Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.editor.redo)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction('Cu&t', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.editor.cut)
        edit_menu.addAction(cut_action)

        copy_action = QAction('&Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.editor.copy)
        edit_menu.addAction(copy_action)

        paste_action = QAction('&Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.editor.paste)
        edit_menu.addAction(paste_action)

        select_all_action = QAction('Select &All', self)
        select_all_action.setShortcut('Ctrl+A')
        select_all_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_all_action)

        # Language menu
        lang_menu = menubar.addMenu('&Language')
        for key, lang in LANGUAGES.items():
            action = QAction(f'{lang["name"]}', self)
            action.triggered.connect(lambda checked, k=key: self._switch_language(k))
            lang_menu.addAction(action)

        # Input Scheme menu
        scheme_menu = menubar.addMenu('&Input Scheme')
        self._scheme_action_group = QActionGroup(self)
        self._scheme_action_group.setExclusive(True)

        baraha_action = QAction('Baraha', self, checkable=True, checked=True)
        baraha_action.triggered.connect(lambda: self._set_input_scheme('phonetic_baraha'))
        self._scheme_action_group.addAction(baraha_action)
        scheme_menu.addAction(baraha_action)

        itrans_action = QAction('ITRANS', self, checkable=True)
        itrans_action.triggered.connect(lambda: self._set_input_scheme('phonetic_itrans'))
        self._scheme_action_group.addAction(itrans_action)
        scheme_menu.addAction(itrans_action)

        inscript_action = QAction('INSCRIPT', self, checkable=True)
        inscript_action.triggered.connect(lambda: self._set_input_scheme('inscript'))
        self._scheme_action_group.addAction(inscript_action)
        scheme_menu.addAction(inscript_action)

        # Output Mode menu
        output_menu = menubar.addMenu('&Output Mode')
        self._output_action_group = QActionGroup(self)
        self._output_action_group.setExclusive(True)

        unicode_action = QAction('Unicode', self, checkable=True, checked=True)
        unicode_action.triggered.connect(lambda: self._set_output_mode('unicode'))
        self._output_action_group.addAction(unicode_action)
        output_menu.addAction(unicode_action)

        baraha_action = QAction('Baraha ANSI', self, checkable=True)
        baraha_action.triggered.connect(lambda: self._set_output_mode('baraha'))
        self._output_action_group.addAction(baraha_action)
        output_menu.addAction(baraha_action)

        shreelipi_action = QAction('Shreelipi ANSI', self, checkable=True)
        shreelipi_action.triggered.connect(lambda: self._set_output_mode('shreelipi'))
        self._output_action_group.addAction(shreelipi_action)
        output_menu.addAction(shreelipi_action)

        # Clipboard Conversion menu
        clipboard_menu = menubar.addMenu('&Clipboard')

        clip_u2b = QAction('Convert Clipboard Unicode\u2192Baraha', self)
        clip_u2b.triggered.connect(lambda: self._convert_clipboard('unicode_to_baraha'))
        clipboard_menu.addAction(clip_u2b)

        clip_b2u = QAction('Convert Clipboard Baraha\u2192Unicode', self)
        clip_b2u.triggered.connect(lambda: self._convert_clipboard('baraha_to_unicode'))
        clipboard_menu.addAction(clip_b2u)

        clipboard_menu.addSeparator()

        clip_u2s = QAction('Convert Clipboard Unicode\u2192Shreelipi', self)
        clip_u2s.triggered.connect(lambda: self._convert_clipboard('unicode_to_shreelipi'))
        clipboard_menu.addAction(clip_u2s)

        clip_s2u = QAction('Convert Clipboard Shreelipi\u2192Unicode', self)
        clip_s2u.triggered.connect(lambda: self._convert_clipboard('shreelipi_to_unicode'))
        clipboard_menu.addAction(clip_s2u)

        clipboard_menu.addSeparator()

        clip_b2s = QAction('Convert Clipboard Baraha\u2192Shreelipi', self)
        clip_b2s.triggered.connect(lambda: self._convert_clipboard('baraha_to_shreelipi'))
        clipboard_menu.addAction(clip_b2s)

        clip_s2b = QAction('Convert Clipboard Shreelipi\u2192Baraha', self)
        clip_s2b.triggered.connect(lambda: self._convert_clipboard('shreelipi_to_baraha'))
        clipboard_menu.addAction(clip_s2b)

        clipboard_menu.addSeparator()

        clip_auto = QAction('Auto-detect \u2192 Unicode', self)
        clip_auto.triggered.connect(lambda: self._convert_clipboard('auto_to_unicode'))
        clipboard_menu.addAction(clip_auto)

        # View menu
        view_menu = menubar.addMenu('&View')

        toggle_panel_action = QAction('Toggle Side &Panel', self)
        toggle_panel_action.setShortcut('F9')
        toggle_panel_action.triggered.connect(self._toggle_side_panel)
        view_menu.addAction(toggle_panel_action)

        view_menu.addSeparator()

        zoom_in_action = QAction('Zoom &In', self)
        zoom_in_action.setShortcut('Ctrl+=')
        zoom_in_action.triggered.connect(lambda: self.zoom_slider.setValue(self.zoom_slider.value() + 10))
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction('Zoom &Out', self)
        zoom_out_action.setShortcut('Ctrl+-')
        zoom_out_action.triggered.connect(lambda: self.zoom_slider.setValue(self.zoom_slider.value() - 10))
        view_menu.addAction(zoom_out_action)

        zoom_reset_action = QAction('&Reset Zoom', self)
        zoom_reset_action.setShortcut('Ctrl+0')
        zoom_reset_action.triggered.connect(lambda: self.zoom_slider.setValue(100))
        view_menu.addAction(zoom_reset_action)

        # Insert menu
        insert_menu = menubar.addMenu('&Insert')

        insert_hr = QAction('Horizontal &Rule', self)
        insert_hr.triggered.connect(self._insert_horizontal_rule)
        insert_menu.addAction(insert_hr)

        insert_pagebreak = QAction('&Page Break', self)
        insert_pagebreak.triggered.connect(self._insert_page_break)
        insert_menu.addAction(insert_pagebreak)

        insert_datetime = QAction('&Date/Time', self)
        insert_datetime.triggered.connect(self._insert_datetime)
        insert_menu.addAction(insert_datetime)

        insert_special = QAction('&Special Character...', self)
        insert_special.triggered.connect(self._insert_special_char)
        insert_menu.addAction(insert_special)

        # Format menu
        format_menu = menubar.addMenu('Forma&t')

        fmt_bold = QAction('&Bold', self)
        fmt_bold.setShortcut('Ctrl+B')
        fmt_bold.triggered.connect(lambda: self.bold_btn.click())
        format_menu.addAction(fmt_bold)

        fmt_italic = QAction('&Italic', self)
        fmt_italic.setShortcut('Ctrl+I')
        fmt_italic.triggered.connect(lambda: self.italic_btn.click())
        format_menu.addAction(fmt_italic)

        fmt_underline = QAction('&Underline', self)
        fmt_underline.setShortcut('Ctrl+U')
        fmt_underline.triggered.connect(lambda: self.underline_btn.click())
        format_menu.addAction(fmt_underline)

        format_menu.addSeparator()

        fmt_left = QAction('Align &Left', self)
        fmt_left.triggered.connect(lambda: self._set_alignment(Qt.AlignLeft))
        format_menu.addAction(fmt_left)

        fmt_center = QAction('Align &Center', self)
        fmt_center.setShortcut('Ctrl+E')
        fmt_center.triggered.connect(lambda: self._set_alignment(Qt.AlignCenter))
        format_menu.addAction(fmt_center)

        fmt_right = QAction('Align &Right', self)
        fmt_right.setShortcut('Ctrl+R')
        fmt_right.triggered.connect(lambda: self._set_alignment(Qt.AlignRight))
        format_menu.addAction(fmt_right)

        fmt_justify = QAction('&Justify', self)
        fmt_justify.setShortcut('Ctrl+J')
        fmt_justify.triggered.connect(lambda: self._set_alignment(Qt.AlignJustify))
        format_menu.addAction(fmt_justify)

        # Help menu
        help_menu = menubar.addMenu('&Help')

        about_action = QAction('&About Varnaakshara', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

        shortcuts_action = QAction('&Keyboard Shortcuts', self)
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)

    def setup_shortcuts(self):
        # Ctrl+Space: Toggle transliteration
        toggle_shortcut = QShortcut(QKeySequence('Ctrl+Space'), self)
        toggle_shortcut.activated.connect(self._toggle_transliteration)

        # Ctrl+L: Cycle language
        lang_shortcut = QShortcut(QKeySequence('Ctrl+L'), self)
        lang_shortcut.activated.connect(self._cycle_language)

    def _toggle_transliteration(self):
        self.editor.toggle_transliteration()
        enabled = self.editor.transliterate_enabled
        self.toggle_btn.setChecked(enabled)
        state = 'ON' if enabled else 'OFF'
        self.toggle_btn.setText(f'🔤 Transliteration: {state}')
        self.statusBar().showMessage(
            f'Transliteration {state} — {LANGUAGES[self.current_language]["name"]}'
        )

    def _on_toggle_clicked(self):
        enabled = self.toggle_btn.isChecked()
        self.editor.set_transliteration(enabled)
        state = 'ON' if enabled else 'OFF'
        self.toggle_btn.setText(f'🔤 Transliteration: {state}')

    def _on_language_changed(self, index):
        lang_key = self.lang_combo.itemData(index)
        self._switch_language(lang_key)

    def _switch_language(self, lang_key):
        self.current_language = lang_key
        self.engine.set_language(lang_key)
        self.editor.engine = self.engine
        if self.ime:
            self.ime.set_language(lang_key)

        # Update combo box without triggering signal
        self.lang_combo.blockSignals(True)
        for i in range(self.lang_combo.count()):
            if self.lang_combo.itemData(i) == lang_key:
                self.lang_combo.setCurrentIndex(i)
                break
        self.lang_combo.blockSignals(False)

        lang_name = LANGUAGES[lang_key]['name']
        # Update grid buttons
        if hasattr(self, '_lang_buttons'):
            for k, b in self._lang_buttons.items():
                b.setChecked(k == lang_key)
        # Update status bar
        if hasattr(self, 'status_lang'):
            self.status_lang.setText(lang_name)

    def _switch_language_from_grid(self, lang_key):
        """Called by panel language grid buttons."""
        self._switch_language(lang_key)

    def _panel_transliterate(self):
        """Convert text in the panel transliteration input."""
        text = self.translit_input.toPlainText().strip()
        if text:
            result = self.engine.transliterate(text)
            self.translit_preview.setText(result)

    def _panel_insert(self):
        """Insert panel transliteration result into the editor."""
        preview = self.translit_preview.text()
        if preview:
            self.editor.insertPlainText(preview)
            self.translit_input.clear()
            self.translit_preview.clear()

    def _cycle_language(self):
        keys = list(LANGUAGES.keys())
        current_idx = keys.index(self.current_language)
        next_idx = (current_idx + 1) % len(keys)
        self._switch_language(keys[next_idx])

    # ══════════════════════════════════════════════
    # FORMATTING METHODS (Word-style)
    # ══════════════════════════════════════════════

    def _on_font_family_changed(self, font):
        """Apply font family to selection or cursor."""
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self._merge_format_on_selection(fmt)

    def _on_font_size_changed(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self._merge_format_on_selection(fmt)

    def _toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.bold_btn.isChecked() else QFont.Normal)
        self._merge_format_on_selection(fmt)

    def _toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self._merge_format_on_selection(fmt)

    def _toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self._merge_format_on_selection(fmt)

    def _toggle_strikethrough(self):
        fmt = QTextCharFormat()
        fmt.setFontStrikeOut(self.strike_btn.isChecked())
        self._merge_format_on_selection(fmt)

    def _pick_text_color(self):
        color = QColorDialog.getColor(Qt.white, self, 'Text Color')
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self._merge_format_on_selection(fmt)

    def _pick_highlight_color(self):
        color = QColorDialog.getColor(Qt.yellow, self, 'Highlight Color')
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setBackground(color)
            self._merge_format_on_selection(fmt)

    def _set_alignment(self, alignment):
        self.editor.setAlignment(alignment)
        # Update button states
        aligns = {
            Qt.AlignLeft: 0, Qt.AlignCenter: 1,
            Qt.AlignRight: 2, Qt.AlignJustify: 3
        }
        for i, btn in enumerate(self._align_buttons):
            btn.setChecked(i == aligns.get(alignment, 0))

    def _on_line_spacing_changed(self, text):
        try:
            spacing = float(text)
        except ValueError:
            return
        cursor = self.editor.textCursor()
        block_fmt = QTextBlockFormat()
        block_fmt.setLineHeight(spacing * 100, 1)  # ProportionalHeight
        cursor.mergeBlockFormat(block_fmt)

    def _merge_format_on_selection(self, fmt):
        """Apply a QTextCharFormat to the current selection or word."""
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(fmt)
        self.editor.mergeCurrentCharFormat(fmt)

    def _on_cursor_position_changed(self):
        """Sync toolbar buttons with cursor's current format."""
        cursor = self.editor.textCursor()
        char_fmt = cursor.charFormat()

        # Sync bold/italic/underline/strike buttons
        self.bold_btn.setChecked(char_fmt.fontWeight() >= QFont.Bold)
        self.italic_btn.setChecked(char_fmt.fontItalic())
        self.underline_btn.setChecked(char_fmt.fontUnderline())
        self.strike_btn.setChecked(char_fmt.fontStrikeOut())

        # Sync font family & size
        self.font_family_combo.blockSignals(True)
        self.font_family_combo.setCurrentFont(QFont(char_fmt.fontFamily()))
        self.font_family_combo.blockSignals(False)

        ps = int(char_fmt.fontPointSize()) if char_fmt.fontPointSize() > 0 else 14
        self.font_size_spin.blockSignals(True)
        self.font_size_spin.setValue(ps)
        self.font_size_spin.blockSignals(False)

        # Sync alignment
        align = self.editor.alignment()
        aligns = {Qt.AlignLeft: 0, Qt.AlignCenter: 1, Qt.AlignRight: 2, Qt.AlignJustify: 3}
        for i, btn in enumerate(self._align_buttons):
            btn.setChecked(i == aligns.get(align, 0))

        # Update char info
        pos = cursor.position()
        block = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self.char_info_label.setText(f'Position: {pos} | Line: {block} | Col: {col}')

    def _update_word_count(self):
        text = self.editor.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        self.word_count_label.setText(f'{words} words')
        if hasattr(self, 'char_count_label'):
            self.char_count_label.setText(f'{chars} chars')

    def _on_zoom_changed(self, value):
        self.zoom_label.setText(f'{value}%')
        # Scale the editor font relative to base size
        scale = value / 100.0
        base_size = self.font_size_spin.value()
        font = self.editor.font()
        font.setPointSizeF(base_size * scale)
        self.editor.document().setDefaultFont(font)

    def _apply_paragraph_style(self, style_name):
        """Apply predefined paragraph styles."""
        cursor = self.editor.textCursor()
        char_fmt = QTextCharFormat()
        block_fmt = QTextBlockFormat()

        styles = {
            'Normal': (14, QFont.Normal, False, 0),
            'Title': (28, QFont.Bold, False, 0),
            'Heading 1': (24, QFont.Bold, False, 0),
            'Heading 2': (20, QFont.Bold, False, 0),
            'Heading 3': (16, QFont.Bold, True, 0),
            'Subtitle': (18, QFont.Normal, True, 0),
            'Quote': (14, QFont.Normal, True, 40),
            'Code': (13, QFont.Normal, False, 20),
        }
        size, weight, italic, indent = styles.get(style_name, (14, QFont.Normal, False, 0))
        char_fmt.setFontPointSize(size)
        char_fmt.setFontWeight(weight)
        char_fmt.setFontItalic(italic)
        if style_name == 'Code':
            char_fmt.setFontFamily('Consolas')
        block_fmt.setLeftMargin(indent)

        cursor.select(QTextCursor.BlockUnderCursor)
        cursor.mergeCharFormat(char_fmt)
        cursor.mergeBlockFormat(block_fmt)

    def _convert(self, fmt):
        text = self.conv_input.toPlainText()
        if not text.strip():
            return

        unicode_result = self.engine.transliterate(text)

        if fmt == 'baraha' or fmt == 'ansi':
            result = self.engine.to_ansi(unicode_result, font_family='baraha')
        elif fmt == 'shreelipi':
            result = self.engine.to_ansi(unicode_result, font_family='shreelipi')
        else:
            result = unicode_result

        self.conv_output.setPlainText(result)

    def _swap_converter(self):
        input_text = self.conv_input.toPlainText()
        output_text = self.conv_output.toPlainText()
        self.conv_input.setPlainText(output_text)
        self.conv_output.setPlainText(input_text)

    def _copy_output(self):
        text = self.conv_output.toPlainText()
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage('Copied to clipboard!')

    def _new_file(self):
        self.editor.clear()
        self.current_file = None
        self.setWindowTitle('Varnaakshara — New File')

    def _open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 'Open File', '',
            'Text Files (*.txt);;All Files (*)'
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    self.editor.setPlainText(f.read())
                self.current_file = path
                self.setWindowTitle(f'Varnaakshara — {os.path.basename(path)}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to open file:\n{e}')

    def _save_file(self):
        if self.current_file:
            self._do_save(self.current_file)
        else:
            self._save_file_as()

    def _save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, 'Save File', '',
            'Text Files (*.txt);;All Files (*)'
        )
        if path:
            self._do_save(path)

    def _do_save(self, path):
        try:
            text = self.editor.toPlainText()
            fmt = self.format_combo.currentData()
            if fmt == 'ansi':
                text = convert_to_ansi(text, self.current_language)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(text)
            self.current_file = path
            self.setWindowTitle(f'Varnaakshara — {os.path.basename(path)}')
            self.statusBar().showMessage(f'Saved: {path}')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save file:\n{e}')

    def _export(self, fmt):
        fmt_names = {'unicode': 'Unicode', 'baraha': 'Baraha ANSI', 'shreelipi': 'Shreelipi ANSI'}
        path, _ = QFileDialog.getSaveFileName(
            self, f'Export as {fmt_names.get(fmt, fmt)}', '',
            'Text Files (*.txt);;All Files (*)'
        )
        if path:
            try:
                text = self.editor.toPlainText()
                if fmt in ('baraha', 'ansi'):
                    text = self.engine.to_ansi(text, font_family='baraha')
                elif fmt == 'shreelipi':
                    text = self.engine.to_ansi(text, font_family='shreelipi')
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.statusBar().showMessage(f'Exported ({fmt_names.get(fmt, fmt)}): {path}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to export:\n{e}')

    def _show_about(self):
        QMessageBox.about(
            self, 'About Varnaakshara',
            '<h2>ವರ್ಣಾಕ್ಷರ Varnaakshara</h2>'
            '<p><b>Professional Indian Script Document Editor</b></p>'
            '<p>12 languages: Kannada, Hindi, Telugu, Tamil, Malayalam, '
            'Marathi, Sanskrit, Bengali, Assamese, Gujarati, Punjabi, Odia</p>'
            '<p>3 input schemes: Baraha, ITRANS, INSCRIPT</p>'
            '<p>3 output encodings: Unicode, Baraha ANSI, Shreelipi ANSI</p>'
            '<hr>'
            '<p><b>Version:</b> 2.0.0</p>'
            '<p><b>License:</b> Free for personal use</p>'
        )

    def _show_shortcuts(self):
        QMessageBox.information(
            self, 'Keyboard Shortcuts',
            '<h3>Shortcuts</h3>'
            '<table>'
            '<tr><td><b>Ctrl+Space</b></td><td>Toggle transliteration on/off</td></tr>'
            '<tr><td><b>Ctrl+L</b></td><td>Cycle through languages</td></tr>'
            '<tr><td><b>Ctrl+N</b></td><td>New file</td></tr>'
            '<tr><td><b>Ctrl+O</b></td><td>Open file</td></tr>'
            '<tr><td><b>Ctrl+S</b></td><td>Save file</td></tr>'
            '<tr><td><b>Ctrl+Shift+S</b></td><td>Save as...</td></tr>'
            '</table>'
            '<h3>Typing Tips</h3>'
            '<ul>'
            '<li><b>aa</b> = long A (ā)</li>'
            '<li><b>ii</b> = long I (ī)</li>'
            '<li><b>uu</b> = long U (ū)</li>'
            '<li><b>T, D, N</b> (uppercase) = retroflex</li>'
            '<li><b>sh</b> = palatal sh, <b>Sh</b> = retroflex sh</li>'
            '<li><b>M</b> = anusvara (ಂ/ं)</li>'
            '<li><b>H</b> = visarga (ಃ/ः)</li>'
            '</ul>'
        )

    def _set_input_scheme(self, mode):
        """Set input scheme via IME and/or editor engine."""
        if self.ime:
            self.ime.set_input_mode(mode)
        # Also update the editor's engine scheme
        if mode == 'phonetic_baraha' and hasattr(self.engine, 'set_scheme'):
            self.engine.set_scheme('baraha')
        elif mode == 'phonetic_itrans' and hasattr(self.engine, 'set_scheme'):
            self.engine.set_scheme('itrans')
        scheme_name = {
            'phonetic_baraha': 'Baraha',
            'phonetic_itrans': 'ITRANS',
            'inscript': 'INSCRIPT',
        }.get(mode, mode)
        self.statusBar().showMessage(f'Input scheme: {scheme_name}')

    def _on_format_combo_changed(self, index):
        """Handle format dropdown change."""
        mode = self.format_combo.currentData()
        if mode:
            self._set_output_mode(mode, from_combo=True)

    def _set_output_mode(self, mode, from_combo=False):
        """Set output mode via IME."""
        if self.ime:
            font_family = mode if mode in ('baraha', 'shreelipi') else None
            self.ime.set_output_mode(
                'ansi' if mode in ('baraha', 'shreelipi') else 'unicode',
                font_family=font_family
            )
        # Also update the editor's engine output preference
        self._current_output_mode = mode
        mode_names = {'unicode': 'Unicode', 'baraha': 'Baraha ANSI', 'shreelipi': 'Shreelipi ANSI'}
        mode_name = mode_names.get(mode, mode)
        self.statusBar().showMessage(f'Output mode: {mode_name}')
        # Sync toolbar combo if change came from menu
        if not from_combo:
            for i in range(self.format_combo.count()):
                if self.format_combo.itemData(i) == mode:
                    self.format_combo.blockSignals(True)
                    self.format_combo.setCurrentIndex(i)
                    self.format_combo.blockSignals(False)
                    break

    def _toggle_side_panel(self):
        """Toggle the right side panel visibility."""
        self.side_panel.setVisible(not self.side_panel.isVisible())

    def _print_document(self):
        """Open print dialog."""
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.editor.print_(printer)

    def _insert_horizontal_rule(self):
        cursor = self.editor.textCursor()
        cursor.insertHtml('<hr>')

    def _insert_page_break(self):
        cursor = self.editor.textCursor()
        cursor.insertText('\n')
        block_fmt = QTextBlockFormat()
        block_fmt.setPageBreakPolicy(QTextBlockFormat.PageBreak_AlwaysBefore)
        cursor.mergeBlockFormat(block_fmt)

    def _insert_datetime(self):
        import datetime
        cursor = self.editor.textCursor()
        cursor.insertText(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

    def _insert_special_char(self):
        """Show special character picker for Indic scripts."""
        chars = ('ಅಆಇಈಉಊಎಏಐಒಓಔ  '
                 'ಕಖಗಘಙಚಛಜಝಞ  '
                 'ಾಿೀುೂೃೆೇೈೊೋೌ  '
                 '್ಂಃಽ  '
                 '೦೧೨೩೪೫೬೭೮೯  '
                 '।॥ ॐ ₹')
        text, ok = QInputDialog.getText(
            self, 'Insert Special Character',
            f'Available ({LANGUAGES[self.current_language]["name"]}):\n{chars}\n\nPaste or type character:'
        )
        if ok and text:
            self.editor.textCursor().insertText(text)

    def _convert_clipboard(self, conversion):
        """Convert clipboard text between Unicode, Baraha, and Shreelipi."""
        # Try IME first
        if self.ime and hasattr(self.ime, 'handle_clipboard_convert'):
            if self.ime.handle_clipboard_convert(conversion):
                self.statusBar().showMessage('Clipboard converted!')
                return

        # Fallback: use engine directly
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        if not text:
            self.statusBar().showMessage('Clipboard is empty')
            return
        try:
            if conversion == 'auto_to_unicode':
                enc, lang, conf = self.engine.detect_encoding(text)
                if enc == 'unicode':
                    self.statusBar().showMessage('Text is already Unicode')
                    return
                result = self.engine.from_ansi(text, font_family=enc)
            elif conversion == 'unicode_to_baraha' or conversion == 'unicode_to_ansi':
                result = self.engine.to_ansi(text, font_family='baraha')
            elif conversion == 'baraha_to_unicode' or conversion == 'ansi_to_unicode':
                result = self.engine.from_ansi(text, font_family='baraha')
            elif conversion == 'unicode_to_shreelipi':
                result = self.engine.to_ansi(text, font_family='shreelipi')
            elif conversion == 'shreelipi_to_unicode':
                result = self.engine.from_ansi(text, font_family='shreelipi')
            elif conversion == 'baraha_to_shreelipi':
                unicode_text = self.engine.from_ansi(text, font_family='baraha')
                result = self.engine.to_ansi(unicode_text, font_family='shreelipi')
            elif conversion == 'shreelipi_to_baraha':
                unicode_text = self.engine.from_ansi(text, font_family='shreelipi')
                result = self.engine.to_ansi(unicode_text, font_family='baraha')
            else:
                result = text
            clipboard.setText(result)
            self.statusBar().showMessage('Clipboard converted!')
        except Exception as e:
            self.statusBar().showMessage(f'Conversion error: {e}')

    def _get_stylesheet(self):
        return """
            /* ═══════════════════════════════════════════
               Varnaakshara Writer — Hybrid Theme
               Word Ribbon + InDesign Dark Panels
               ═══════════════════════════════════════════ */

            QMainWindow {
                background-color: #535353;
            }

            /* ── Menu Bar (dark) ── */
            QMenuBar {
                background-color: #2b2b2b;
                color: #e0e0e0;
                font-size: 12px;
                padding: 2px 0;
                border-bottom: 1px solid #1a1a1a;
            }
            QMenuBar::item {
                padding: 5px 12px;
                border-radius: 2px;
            }
            QMenuBar::item:selected {
                background-color: #505050;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #555;
                padding: 4px 0;
            }
            QMenu::item {
                padding: 5px 30px 5px 20px;
            }
            QMenu::item:selected {
                background-color: #2a6fdb;
            }
            QMenu::separator {
                height: 1px;
                background: #555;
                margin: 4px 10px;
            }

            /* ── Ribbon (Word-style, light) ── */
            QTabWidget#ribbon::pane {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f2f5, stop:1 #e4e8ec);
                border: none;
                border-bottom: 1px solid #b0b8c0;
            }
            QTabWidget#ribbon > QTabBar::tab {
                background: transparent;
                color: #555;
                padding: 6px 16px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                border: none;
                border-bottom: 3px solid transparent;
                margin: 0 2px;
            }
            QTabWidget#ribbon > QTabBar::tab:selected {
                color: #1a73e8;
                border-bottom: 3px solid #1a73e8;
            }
            QTabWidget#ribbon > QTabBar::tab:hover {
                color: #333;
                background: rgba(0,0,0,0.04);
            }

            /* ── Ribbon Groups ── */
            QFrame#ribbonGroup {
                background: transparent;
                border-right: 1px solid #c8cdd2;
                margin: 2px 0;
            }
            QLabel#ribbonGroupTitle {
                color: #888;
                font-size: 10px;
                font-weight: normal;
                padding-top: 2px;
            }

            /* ── Ribbon Buttons ── */
            QPushButton#ribbonIconBtn {
                background-color: transparent;
                color: #333;
                border: 1px solid transparent;
                border-radius: 3px;
                padding: 3px 8px;
                font-size: 13px;
                font-weight: bold;
                min-height: 24px;
                min-width: 28px;
            }
            QPushButton#ribbonIconBtn:hover {
                background-color: rgba(0, 0, 0, 0.08);
                border: 1px solid #b0b8c0;
            }
            QPushButton#ribbonIconBtn:checked {
                background-color: #2a6fdb;
                color: #fff;
                border: 1px solid #1a5fc0;
            }
            QPushButton#ribbonLargeBtn {
                background: transparent;
                color: #555;
                border: 1px solid transparent;
                border-radius: 3px;
                padding: 6px 10px;
                font-size: 11px;
                min-height: 36px;
            }
            QPushButton#ribbonLargeBtn:hover {
                background-color: rgba(0,0,0,0.06);
                border: 1px solid #c0c8d0;
            }

            /* ── Document Canvas (white page on dark pasteboard) ── */
            QTextEdit {
                background-color: #ffffff;
                color: #1a1a1a;
                border: none;
                padding: 20px;
                selection-background-color: #2a6fdb;
                selection-color: #ffffff;
                font-size: 14px;
            }
            QFrame#docPage {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
            }
            QWidget#pasteboard {
                background-color: #535353;
            }
            QScrollArea#canvasScroll {
                background-color: #535353;
                border: none;
            }

            /* ── Converter text areas ── */
            QPlainTextEdit {
                background-color: #fff;
                color: #1a1a1a;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                padding: 8px;
                selection-background-color: #2a6fdb;
                selection-color: #fff;
            }

            /* ── Side Panel (InDesign-style dark) ── */
            QWidget#sidePanel {
                background-color: #2b2b2b;
                border-left: 1px solid #1a1a1a;
            }
            QScrollArea#panelScroll {
                background-color: #2b2b2b;
                border: none;
            }
            QLabel#panelsHeader {
                background-color: #333;
                color: #aaa;
                font-size: 11px;
                font-weight: bold;
                padding: 6px 12px;
                border-bottom: 1px solid #444;
            }
            /* Panel headers */
            QPushButton#panelHeader {
                background-color: #383838;
                color: #ccc;
                border: none;
                border-bottom: 1px solid #222;
                padding: 7px 12px;
                text-align: left;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton#panelHeader:hover {
                background-color: #404040;
            }
            /* Language grid buttons */
            QPushButton#langGridBtn {
                background-color: #444;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px 4px;
                font-size: 12px;
                min-height: 22px;
            }
            QPushButton#langGridBtn:hover {
                background-color: #505050;
                border-color: #777;
            }
            QPushButton#langGridBtn:checked {
                background-color: #1a73e8;
                color: #fff;
                border-color: #1a73e8;
            }
            /* Panel labels & combos */
            QWidget#sidePanel QLabel {
                color: #bbb;
                font-size: 11px;
            }
            QWidget#sidePanel QComboBox {
                background-color: #444;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 3px 8px;
                font-size: 11px;
            }
            QWidget#sidePanel QComboBox::drop-down { border: none; }
            QWidget#sidePanel QComboBox QAbstractItemView {
                background-color: #333;
                color: #ddd;
                selection-background-color: #1a73e8;
            }
            /* Transliterate panel */
            QPlainTextEdit#translitInput {
                background-color: #3a3a3a;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 3px;
                font-size: 12px;
                padding: 4px;
            }
            QLabel#translitPreview {
                background-color: #3a3a3a;
                color: #ffcc00;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 6px;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton#accentBtn {
                background-color: #1a73e8;
                color: #fff;
                border: none;
                border-radius: 3px;
                padding: 6px 14px;
                font-weight: bold;
            }
            QPushButton#accentBtn:hover {
                background-color: #1565c0;
            }

            /* ── Main Tabs (Editor/Converter) ── */
            QTabWidget#mainTabs::pane {
                border: none;
                background-color: #535353;
            }
            QTabWidget#mainTabs > QTabBar::tab {
                background-color: #3a3a3a;
                color: #aaa;
                padding: 7px 18px;
                margin-right: 1px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                border: 1px solid #444;
                border-bottom: none;
            }
            QTabWidget#mainTabs > QTabBar::tab:selected {
                background-color: #535353;
                color: #fff;
            }
            QTabWidget#mainTabs > QTabBar::tab:hover {
                background-color: #454545;
                color: #ddd;
            }

            /* ── Converter GroupBoxes ── */
            QGroupBox {
                color: #222;
                border: 1px solid #c0c0c0;
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 18px;
                font-weight: bold;
                font-size: 12px;
                background-color: #f5f5f5;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 6px;
            }

            /* ── Converter Buttons ── */
            QPushButton {
                background-color: #e8ecf0;
                color: #222;
                border: 1px solid #b0b8c0;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #d4dae0;
                border: 1px solid #8890a0;
            }
            QPushButton:pressed {
                background-color: #c0c8d0;
            }

            /* ── Status Bar (blue) ── */
            QStatusBar#blueStatusBar {
                background-color: #1a73e8;
                color: #fff;
                font-size: 11px;
                border: none;
                padding: 2px 8px;
            }
            QStatusBar#blueStatusBar QLabel {
                color: #fff;
                font-size: 11px;
                padding: 0 8px;
            }
            QLabel#langDot {
                color: #4caf50;
                font-size: 14px;
                padding: 0 2px;
            }

            /* ── Zoom Slider (on blue bar) ── */
            QSlider::groove:horizontal {
                border: none;
                height: 4px;
                background: rgba(255,255,255,0.3);
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: none;
                width: 12px;
                margin: -4px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:hover {
                background: #e0e0e0;
            }

            /* ── Splitter ── */
            QSplitter::handle {
                background-color: #1a1a1a;
                width: 2px;
            }

            /* ── Ribbon combos & spins ── */
            QTabWidget#ribbon QComboBox {
                background-color: #fff;
                color: #222;
                border: 1px solid #b0b8c0;
                border-radius: 3px;
                padding: 3px 8px;
                font-size: 12px;
            }
            QTabWidget#ribbon QComboBox::drop-down { border: none; width: 18px; }
            QTabWidget#ribbon QComboBox QAbstractItemView {
                background: #fff; color: #222;
                selection-background-color: #1a73e8; selection-color: #fff;
            }
            QTabWidget#ribbon QSpinBox {
                background: #fff; color: #222;
                border: 1px solid #b0b8c0; border-radius: 3px;
                padding: 2px 6px; min-height: 22px;
            }
            QTabWidget#ribbon QFontComboBox {
                background: #fff; color: #222;
                border: 1px solid #b0b8c0; border-radius: 3px;
                padding: 3px 8px; font-size: 12px;
            }
        """


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Varnaakshara')
    app.setOrganizationName('Varnaakshara')

    # Set app-wide font
    app.setFont(QFont('Segoe UI', 10))

    window = VarnaaksharaApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
