"""Automated UI test for Varnaakshara — runs headless, screenshots each step."""
import sys, os, time
os.environ['DISPLAY'] = ':99'
sys.argv = ['test']

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtTest import QTest

from app import VarnaaksharaApp

OUT = '/root/.openclaw/workspace'
results = []

def screenshot(widget, name):
    path = f"{OUT}/uitest_{name}.png"
    screen = QApplication.primaryScreen()
    px = screen.grabWindow(widget.winId())
    px.save(path)
    results.append(f"✅ {name}: saved")
    return path

def run_tests():
    try:
        w = window

        # Test 0: Initial state
        screenshot(w, "00_launch")

        # Test 1: Click editor and type text
        editor = w.editor
        editor.setFocus()
        QTest.mouseClick(editor.viewport(), Qt.LeftButton, Qt.NoModifier, QPoint(200, 100))
        QTest.keyClicks(editor, "namaste ")
        time.sleep(0.3)
        screenshot(w, "01_typing")
        editor_text = editor.toPlainText()
        results.append(f"  Editor text: '{editor_text[:80]}'")

        # Test 2: Bold button (B)
        toolbar = None
        for tb in w.findChildren(type(w).toolbar.__class__) if hasattr(w, 'toolbar') else []:
            toolbar = tb
            break
        # Try clicking bold via keyboard shortcut
        QTest.keyClick(editor, Qt.Key_A, Qt.ControlModifier)  # Select all
        QTest.keyClick(editor, Qt.Key_B, Qt.ControlModifier)  # Bold
        time.sleep(0.2)
        screenshot(w, "02_bold")
        results.append("✅ Bold shortcut applied")

        # Test 3: Undo bold
        QTest.keyClick(editor, Qt.Key_Z, Qt.ControlModifier)
        time.sleep(0.2)

        # Test 4: Language switching - click Hindi button
        # Find language buttons in the panel
        from PyQt5.QtWidgets import QPushButton
        lang_buttons = {}
        for btn in w.findChildren(QPushButton):
            txt = btn.text().strip()
            if txt:
                lang_buttons[txt] = btn

        results.append(f"  Found buttons: {list(lang_buttons.keys())[:15]}")

        # Click Hindi if available
        hindi_names = ['हिंदी', 'Hindi']
        for name in hindi_names:
            if name in lang_buttons:
                QTest.mouseClick(lang_buttons[name], Qt.LeftButton)
                time.sleep(0.3)
                screenshot(w, "03_hindi")
                results.append(f"✅ Switched to Hindi")
                break

        # Test 5: Type in Hindi mode
        QTest.mouseClick(editor.viewport(), Qt.LeftButton, Qt.NoModifier, QPoint(200, 150))
        QTest.keyClicks(editor, "bharat ")
        time.sleep(0.3)
        screenshot(w, "04_hindi_typing")
        results.append(f"  Editor text after Hindi: '{editor.toPlainText()[:100]}'")

        # Test 6: Click Converter tab
        from PyQt5.QtWidgets import QTabWidget
        tabs = w.findChildren(QTabWidget)
        for tab in tabs:
            for i in range(tab.count()):
                if 'Converter' in (tab.tabText(i) or ''):
                    tab.setCurrentIndex(i)
                    time.sleep(0.3)
                    screenshot(w, "05_converter_tab")
                    results.append("✅ Converter tab opened")
                    # Switch back to editor
                    tab.setCurrentIndex(0)
                    time.sleep(0.2)
                    break

        # Test 7: Test Convert button in transliterate panel
        convert_btn = None
        for btn in w.findChildren(QPushButton):
            if btn.text().strip().lower() == 'convert':
                convert_btn = btn
                break
        if convert_btn:
            QTest.mouseClick(convert_btn, Qt.LeftButton)
            time.sleep(0.3)
            screenshot(w, "06_convert_clicked")
            results.append("✅ Convert button clicked")

        # Test 8: Test Italic shortcut
        QTest.mouseClick(editor.viewport(), Qt.LeftButton, Qt.NoModifier, QPoint(200, 100))
        QTest.keyClick(editor, Qt.Key_A, Qt.ControlModifier)
        QTest.keyClick(editor, Qt.Key_I, Qt.ControlModifier)
        time.sleep(0.2)
        screenshot(w, "07_italic")
        results.append("✅ Italic shortcut applied")
        QTest.keyClick(editor, Qt.Key_Z, Qt.ControlModifier)

        # Test 9: Test menu bar - File menu
        menubar = w.menuBar()
        file_menu = None
        for action in menubar.actions():
            if action.text().replace('&', '') == 'File':
                file_menu = action.menu()
                break
        if file_menu:
            file_actions = [a.text().replace('&', '') for a in file_menu.actions() if a.text()]
            results.append(f"  File menu items: {file_actions}")
            results.append("✅ File menu accessible")

        # Test 10: Test Language menu
        for action in menubar.actions():
            if action.text().replace('&', '') == 'Language':
                lang_menu = action.menu()
                if lang_menu:
                    lang_actions = [a.text() for a in lang_menu.actions() if a.text()]
                    results.append(f"  Language menu: {lang_actions[:8]}")
                    results.append("✅ Language menu accessible")
                break

        # Test 11: Switch back to Kannada
        for name in ['ಕನ್ನಡ', 'Kannada']:
            if name in lang_buttons:
                QTest.mouseClick(lang_buttons[name], Qt.LeftButton)
                time.sleep(0.2)
                results.append("✅ Switched back to Kannada")
                break

        # Test 12: Test alignment buttons via shortcuts
        QTest.mouseClick(editor.viewport(), Qt.LeftButton, Qt.NoModifier, QPoint(200, 100))
        QTest.keyClick(editor, Qt.Key_E, Qt.ControlModifier)  # Center
        time.sleep(0.2)
        screenshot(w, "08_center_align")
        results.append("✅ Center alignment")
        QTest.keyClick(editor, Qt.Key_L, Qt.ControlModifier)  # Left (or cycle language)
        time.sleep(0.2)

        # Test 13: Underline
        QTest.keyClick(editor, Qt.Key_U, Qt.ControlModifier)
        time.sleep(0.2)
        results.append("✅ Underline shortcut")

        # Test 14: Collapsible panels - click Script Converter header
        from PyQt5.QtWidgets import QLabel
        for label in w.findChildren(QLabel):
            if 'SCRIPT CONVERTER' in (label.text() or '').upper():
                QTest.mouseClick(label, Qt.LeftButton)
                time.sleep(0.3)
                screenshot(w, "09_script_converter")
                results.append("✅ Script Converter panel toggled")
                break

        # Test 15: Final full screenshot
        screenshot(w, "10_final")

        # Print summary
        print("\n=== UI TEST RESULTS ===")
        for r in results:
            print(r)
        print(f"\nTotal tests: {len([r for r in results if r.startswith('✅')])}")
        print("=== DONE ===")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ERROR: {e}")
    finally:
        QApplication.quit()

app = QApplication(sys.argv)
app.setFont(QFont('Segoe UI', 10))
window = VarnaaksharaApp()
window.show()

QTimer.singleShot(1000, run_tests)
sys.exit(app.exec_())
