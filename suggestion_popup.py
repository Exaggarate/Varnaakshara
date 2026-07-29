"""
Varnaakshara Suggestion Popup
==========================
Lightweight overlay window that shows word suggestions near the cursor.
Uses Win32 layered window for transparency and always-on-top.

The popup is controlled from the IME hook thread via a thread-safe queue.
The Qt thread owns the popup widget and processes queue commands.
"""

import threading
import os
import time
from collections import deque

def _popup_log(msg):
    """Debug log for popup (no-op in production)."""
    pass


class _Invoker:
    """Helper that uses QApplication.postEvent to safely run callables on the Qt thread.
    
    QTimer.singleShot(0, fn) from a non-Qt thread doesn't reliably wake the
    event loop on Windows.  postEvent always does.
    """
    _receiver = None  # QObject living on the Qt main thread

    @classmethod
    def init(cls):
        """Create the receiver QObject. Call from Qt thread only."""
        from PyQt5.QtCore import QObject, QEvent
        class _Receiver(QObject):
            def event(self, ev):
                if ev.type() == QEvent.Type(QEvent.User + 1):
                    fn = getattr(ev, '_fn', None)
                    if fn:
                        try:
                            fn()
                        except Exception as e:
                            _popup_log(f'Invoker exec error: {e}')
                    return True
                return super().event(ev)
        cls._receiver = _Receiver()
        _popup_log('Invoker initialized')

    @classmethod
    def invoke(cls, fn):
        """Schedule fn to run on the Qt thread. Safe from any thread."""
        if cls._receiver is None:
            _popup_log('Invoker: no receiver, skipping')
            return
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QEvent
        app = QApplication.instance()
        if app is None:
            _popup_log('Invoker: no QApplication, skipping')
            return
        ev = QEvent(QEvent.Type(QEvent.User + 1))
        ev._fn = fn
        app.postEvent(cls._receiver, ev)
        _popup_log(f'Invoker: posted event')


class SuggestionPopup:
    """Thread-safe suggestion popup controller.
    
    Call from ANY thread:
      show(suggestions, x, y)  — display/update suggestions
      hide()                   — hide popup
      accept(index)            — accept suggestion at index (0-based)
    
    Must be initialized from the Qt thread via init_widget().
    """

    def __init__(self):
        self._widget = None
        self._suggestions = []  # current list of (word, source) tuples
        self._visible = False
        self._on_accept = None  # callback(word, lang_code)

    def set_accept_callback(self, cb):
        """Set callback for when user accepts a suggestion."""
        self._on_accept = cb

    def init_widget(self, parent=None):
        """Create the popup widget. Must be called from Qt thread."""
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QFont, QColor, QPalette

        class PopupWidget(QWidget):
            def __init__(self):
                super().__init__(None)
                self.setWindowFlags(
                    Qt.ToolTip | Qt.FramelessWindowHint |
                    Qt.WindowStaysOnTopHint | Qt.WindowDoesNotAcceptFocus
                )
                self.setAttribute(Qt.WA_ShowWithoutActivating)
                self.setAttribute(Qt.WA_TranslucentBackground, False)

                self.setStyleSheet("""
                    QWidget#popup_main {
                        background-color: #1E1E2E;
                        border: 1.5px solid #585B70;
                        border-radius: 8px;
                    }
                    QLabel#header {
                        color: #7F849C;
                        padding: 2px 10px;
                        font-size: 11px;
                    }
                    QLabel.suggestion {
                        color: #CDD6F4;
                        padding: 5px 12px;
                        font-size: 16px;
                        border-radius: 5px;
                    }
                    QLabel.suggestion:hover {
                        background-color: #313244;
                    }
                    QLabel#shortcut {
                        color: #6C7086;
                        font-size: 13px;
                        padding: 0px 4px;
                    }
                    QLabel#star {
                        color: #F9E2AF;
                        font-size: 13px;
                        padding: 0px 4px;
                    }
                """)

                self.setObjectName('popup_main')
                self.setMinimumWidth(180)

                self.layout = QVBoxLayout()
                self.layout.setContentsMargins(6, 5, 6, 6)
                self.layout.setSpacing(2)
                self.setLayout(self.layout)

                # Header hint
                self.header = QLabel('Tab / 1-5 to select')
                self.header.setObjectName('header')
                self.layout.addWidget(self.header)

                self.rows = []  # list of (row_widget, num_label, word_label, star_label)
                for i in range(5):
                    row = QWidget()
                    row.setStyleSheet('background: transparent; border: none;')
                    hl = QHBoxLayout()
                    hl.setContentsMargins(0, 0, 0, 0)
                    hl.setSpacing(4)
                    row.setLayout(hl)

                    num_lbl = QLabel(f'{i+1}')
                    num_lbl.setObjectName('shortcut')
                    num_lbl.setFont(QFont('Segoe UI', 10))
                    num_lbl.setFixedWidth(18)
                    hl.addWidget(num_lbl)

                    word_lbl = QLabel()
                    word_lbl.setProperty('class', 'suggestion')
                    word_lbl.setFont(QFont('Nirmala UI', 14))
                    hl.addWidget(word_lbl, 1)

                    star_lbl = QLabel()
                    star_lbl.setObjectName('star')
                    star_lbl.setFont(QFont('Segoe UI', 10))
                    star_lbl.setFixedWidth(20)
                    hl.addWidget(star_lbl)

                    self.layout.addWidget(row)
                    self.rows.append((row, num_lbl, word_lbl, star_lbl))
                    row.hide()

            def update_suggestions(self, suggestions, selected=0):
                for i, (row, num_lbl, word_lbl, star_lbl) in enumerate(self.rows):
                    if i < len(suggestions):
                        word, source = suggestions[i]
                        word_lbl.setText(word)
                        star_lbl.setText('★' if source == 'user' else '')
                        # Highlight selected row
                        if i == selected:
                            word_lbl.setStyleSheet(
                                'background-color: #313244; color: #CDD6F4; '
                                'padding: 5px 12px; font-size: 16px; border-radius: 5px;'
                            )
                        else:
                            word_lbl.setStyleSheet(
                                'background: transparent; color: #CDD6F4; '
                                'padding: 5px 12px; font-size: 16px; border-radius: 5px;'
                            )
                        row.show()
                    else:
                        row.hide()
                self.adjustSize()

        self._widget = PopupWidget()
        self._selected = 0
        # Initialize the cross-thread invoker on the Qt thread
        _Invoker.init()

    @staticmethod
    def _run_on_qt(fn):
        """Marshal a callable onto the Qt main thread via postEvent.
        
        This is safe to call from ANY thread.  postEvent always wakes
        the Qt event loop, unlike QTimer.singleShot which can fail
        from non-Qt threads on Windows.
        """
        _Invoker.invoke(fn)

    def show(self, suggestions, x=None, y=None, dpi_scale=1.0):
        """Show popup with suggestions. Thread-safe (marshals to Qt)."""
        if not self._widget or not suggestions:
            self.hide()
            return

        self._suggestions = list(suggestions)
        self._selected = 0
        self._visible = True

        # Capture values for the closure
        _suggestions = self._suggestions
        _selected = self._selected
        _widget = self._widget
        _x, _y = x, y
        _scale = dpi_scale

        def _do():
            try:
                _widget.update_suggestions(_suggestions, _selected)
                if _x is not None and _y is not None:
                    px, py = _x, _y
                    offset = int(24 * _scale)
                    try:
                        from PyQt5.QtWidgets import QApplication
                        from PyQt5.QtCore import QPoint
                        screen = QApplication.screenAt(QPoint(px, py))
                        if screen:
                            geom = screen.availableGeometry()
                            popup_w = _widget.sizeHint().width()
                            popup_h = _widget.sizeHint().height()
                            if px + popup_w > geom.right():
                                px = geom.right() - popup_w
                            if py + offset + popup_h > geom.bottom():
                                py = py - popup_h - 5
                            else:
                                py = py + offset
                            px = max(px, geom.left())
                    except Exception:
                        py = py + offset
                    _widget.move(px, py)
                _widget.show()
                _widget.raise_()
                _popup_log(f'show OK at ({_x},{_y}) count={len(_suggestions)}')
            except Exception as e:
                _popup_log(f'show error: {e}')

        self._run_on_qt(_do)

    def hide(self):
        """Hide the popup. Thread-safe."""
        self._suggestions = []
        self._selected = 0
        self._visible = False
        if self._widget:
            _widget = self._widget
            def _do():
                try:
                    _widget.hide()
                except RuntimeError:
                    pass
            self._run_on_qt(_do)

    def select_next(self):
        """Move selection down. Thread-safe."""
        if self._suggestions:
            self._selected = (self._selected + 1) % len(self._suggestions)
            if self._widget:
                _suggestions = self._suggestions
                _selected = self._selected
                _widget = self._widget
                def _do():
                    try:
                        _widget.update_suggestions(_suggestions, _selected)
                    except RuntimeError:
                        pass
                self._run_on_qt(_do)

    def select_prev(self):
        """Move selection up. Thread-safe."""
        if self._suggestions:
            self._selected = (self._selected - 1) % len(self._suggestions)
            if self._widget:
                _suggestions = self._suggestions
                _selected = self._selected
                _widget = self._widget
                def _do():
                    try:
                        _widget.update_suggestions(_suggestions, _selected)
                    except RuntimeError:
                        pass
                self._run_on_qt(_do)

    def accept(self, index=None):
        """Accept suggestion at index (0-based), or current selection if None. Returns the word or None."""
        if index is None:
            index = self._selected
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

    @property
    def selected_index(self):
        return self._selected
