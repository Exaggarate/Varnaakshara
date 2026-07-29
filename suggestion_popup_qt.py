"""
Varnaakshara Suggestion Popup (Cross-platform Qt)
===============================================
Pure PyQt5 overlay window for word suggestions.
Works on macOS and Linux (no Win32 dependencies).

Same interface as suggestion_popup.py:
  - SuggestionPopup class
  - show(suggestions, x, y), hide(), accept(index)
  - init_widget() for Qt thread initialization
  - is_visible, count properties
  - Dark theme (Catppuccin Mocha colors)

Thread-safe: can be called from the hook thread; Qt operations
are marshalled to the main Qt thread via signals.
"""

import threading
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication
from PyQt5.QtCore import Qt, QMetaObject, Q_ARG, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtGui import QFont, QColor, QCursor


# ============================================================
# Catppuccin Mocha palette
# ============================================================
_MOCHA_BASE = '#1E1E2E'
_MOCHA_SURFACE0 = '#313244'
_MOCHA_OVERLAY0 = '#6C7086'
_MOCHA_TEXT = '#CDD6F4'
_MOCHA_SUBTEXT0 = '#A6ADC8'
_MOCHA_BORDER = '#45475A'
_MOCHA_BLUE = '#89B4FA'
_MOCHA_YELLOW = '#F9E2AF'


# ============================================================
# Popup Widget
# ============================================================
class _PopupWidget(QWidget):
    """Frameless overlay widget showing up to 5 suggestions."""

    # Signals for thread-safe updates from hook thread
    sig_update = pyqtSignal(list)     # list of (word, source)
    sig_move = pyqtSignal(int, int)   # x, y
    sig_show = pyqtSignal()
    sig_hide = pyqtSignal()

    def __init__(self):
        super().__init__(None)
        self.setWindowFlags(
            Qt.ToolTip | Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WA_TranslucentBackground, False)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {_MOCHA_BASE};
                border: 1px solid {_MOCHA_BORDER};
                border-radius: 6px;
            }}
            QLabel {{
                color: {_MOCHA_TEXT};
                padding: 3px 8px;
                font-size: 13px;
                border: none;
            }}
            QLabel[selected="true"] {{
                background-color: {_MOCHA_SURFACE0};
                border-radius: 4px;
            }}
        """)

        self._layout = QVBoxLayout()
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.setSpacing(1)
        self.setLayout(self._layout)

        # Pre-create 5 label slots
        self.labels = []
        for i in range(5):
            lbl = QLabel()
            # Use a cross-platform font
            lbl.setFont(QFont('Helvetica Neue', 12))
            self._layout.addWidget(lbl)
            self.labels.append(lbl)
            lbl.hide()

        # Connect signals to slots
        self.sig_update.connect(self._on_update)
        self.sig_move.connect(self._on_move)
        self.sig_show.connect(self._on_show)
        self.sig_hide.connect(self._on_hide)

    @pyqtSlot(list)
    def _on_update(self, suggestions):
        for i, lbl in enumerate(self.labels):
            if i < len(suggestions):
                word, source = suggestions[i]
                src_icon = '⭐' if source == 'user' else ''
                # Number key hint (1-5)
                lbl.setText(f'{i + 1}. {word} {src_icon}')
                lbl.show()
            else:
                lbl.hide()
        self.adjustSize()

    @pyqtSlot(int, int)
    def _on_move(self, x, y):
        self.move(x, y + 25)  # offset below cursor

    @pyqtSlot()
    def _on_show(self):
        self.show()
        self.raise_()

    @pyqtSlot()
    def _on_hide(self):
        self.hide()


# ============================================================
# Public API (thread-safe)
# ============================================================
class SuggestionPopup:
    """Thread-safe suggestion popup controller.

    Call from ANY thread:
      show(suggestions, x, y)  — display/update suggestions
      hide()                   — hide popup
      accept(index)            — accept suggestion at index (0-based)

    Must be initialized from the Qt thread via init_widget().
    """

    def __init__(self):
        self._widget = None       # type: _PopupWidget | None
        self._suggestions = []    # current list of (word, source) tuples
        self._visible = False
        self._on_accept = None    # callback(word, lang_code)

    def set_accept_callback(self, cb):
        """Set callback for when user accepts a suggestion."""
        self._on_accept = cb

    def init_widget(self, parent=None):
        """Create the popup widget. Must be called from the Qt thread."""
        self._widget = _PopupWidget()

    def show(self, suggestions, x=None, y=None):
        """Show popup with suggestions. Thread-safe."""
        if not self._widget or not suggestions:
            self.hide()
            return

        self._suggestions = list(suggestions)
        self._visible = True

        try:
            self._widget.sig_update.emit(self._suggestions)
            if x is not None and y is not None:
                self._widget.sig_move.emit(x, y)
            else:
                # Fall back to cursor position
                try:
                    pos = QCursor.pos()
                    self._widget.sig_move.emit(pos.x(), pos.y())
                except Exception:
                    pass
            self._widget.sig_show.emit()
        except RuntimeError:
            pass

    def hide(self):
        """Hide the popup. Thread-safe."""
        self._suggestions = []
        self._visible = False
        if self._widget:
            try:
                self._widget.sig_hide.emit()
            except RuntimeError:
                pass

    def accept(self, index):
        """Accept suggestion at index (0-based). Returns the word or None."""
        if 0 <= index < len(self._suggestions):
            word, source = self._suggestions[index]
            self.hide()
            return word
        return None

    @property
    def is_visible(self):
        return self._visible and bool(self._suggestions)

    @property
    def count(self):
        return len(self._suggestions)
