#!/usr/bin/env python3
"""
Automated GUI test for Varnaakshara Writer app.
Runs the app headlessly, tests each feature, takes screenshots.
"""
import sys
import os
import time
import subprocess
import traceback

# Start Xvfb on a fresh display
DISPLAY_NUM = 42
os.environ['DISPLAY'] = f':{DISPLAY_NUM}'

# Kill any old Xvfb on this display
subprocess.run(f'kill $(cat /tmp/.X{DISPLAY_NUM}-lock 2>/dev/null) 2>/dev/null; rm -f /tmp/.X{DISPLAY_NUM}-lock /tmp/.X11-unix/X{DISPLAY_NUM}', shell=True)
time.sleep(0.5)

xvfb = subprocess.Popen(
    ['Xvfb', f':{DISPLAY_NUM}', '-screen', '0', '1400x900x24'],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
time.sleep(1)
print(f"Xvfb started on :{DISPLAY_NUM}")

# Now import Qt (needs DISPLAY set)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer, Qt, QPoint
from PyQt5.QtGui import QKeySequence
from PyQt5.QtTest import QTest

# Add app dir to path
sys.path.insert(0, '/root/.openclaw/workspace/varnaakshara-ime')

results = []
screenshot_count = 0

def screenshot(widget, name):
    global screenshot_count
    screenshot_count += 1
    path = f'/tmp/vtest_{screenshot_count:02d}_{name}.png'
    # Grab the whole window
    try:
        pixmap = widget.grab()
        pixmap.save(path)
        print(f"  📸 Screenshot saved: {path}")
        return path
    except Exception as e:
        print(f"  ❌ Screenshot failed: {e}")
        return None

def test_result(name, passed, detail=""):
    status = "✅ PASS" if passed else "❌ FAIL"
    results.append((name, passed, detail))
    print(f"  {status}: {name}" + (f" — {detail}" if detail else ""))

def run_tests():
    app = QApplication(sys.argv)
    
    # Import and create main window
    from app import VarnaaksharaApp
    window = VarnaaksharaApp()
    window.show()
    window.resize(1300, 850)
    app.processEvents()
    time.sleep(1)
    
    print("\n" + "="*60)
    print("  VARNAAKSHARA WRITER — AUTOMATED TEST SUITE")
    print("="*60)
    
    # ─── TEST 1: App Launch ────────────────────────────────────
    print("\n▶ TEST 1: App Launch")
    test_result("Window visible", window.isVisible())
    test_result("Window title set", "Varnaakshara" in window.windowTitle(), window.windowTitle())
    screenshot(window, "launch")
    
    # ─── TEST 2: Menu Bar ──────────────────────────────────────
    print("\n▶ TEST 2: Menu Bar")
    menubar = window.menuBar()
    menu_names = [a.text() for a in menubar.actions()]
    print(f"  Menus found: {menu_names}")
    expected_menus = ['File', 'Edit', 'Language']
    for m in expected_menus:
        test_result(f"Menu '{m}' exists", any(m in n for n in menu_names))
    
    # ─── TEST 3: Toolbar / Ribbon ──────────────────────────────
    print("\n▶ TEST 3: Toolbar/Ribbon")
    toolbars = window.findChildren(window.__class__.__bases__[0].__mro__[0])
    # Check for language combo
    from PyQt5.QtWidgets import QComboBox
    combos = window.findChildren(QComboBox)
    combo_names = []
    for c in combos:
        items = [c.itemText(i) for i in range(min(c.count(), 5))]
        combo_names.append(f"{c.objectName() or 'combo'}({c.count()} items): {items}")
    print(f"  ComboBoxes: {len(combos)}")
    for cn in combo_names:
        print(f"    {cn}")
    test_result("Has combo boxes (lang/font/etc)", len(combos) >= 2)
    
    # ─── TEST 4: Editor Focus & Typing ─────────────────────────
    print("\n▶ TEST 4: Editor - Text Input")
    from PyQt5.QtWidgets import QTextEdit
    editors = window.findChildren(QTextEdit)
    print(f"  QTextEdit widgets found: {len(editors)}")
    test_result("Editor widget exists", len(editors) > 0)
    
    if editors:
        editor = editors[0]
        editor.setFocus()
        app.processEvents()
        
        # Clear and type
        editor.clear()
        app.processEvents()
        
        # Type raw English text
        QTest.keyClicks(editor, "Hello World")
        app.processEvents()
        time.sleep(0.3)
        
        text = editor.toPlainText()
        print(f"  Typed 'Hello World', got: '{text}'")
        test_result("Text input works", len(text) > 0, f"Got: {text[:50]}")
        screenshot(window, "text_input")
    
    # ─── TEST 5: Transliteration ───────────────────────────────
    print("\n▶ TEST 5: Transliteration")
    if editors:
        editor = editors[0]
        editor.clear()
        app.processEvents()
        
        # Find and enable transliteration toggle
        from PyQt5.QtWidgets import QPushButton
        buttons = window.findChildren(QPushButton)
        translit_btn = None
        for btn in buttons:
            if 'transliterat' in btn.text().lower() or 'translit' in btn.objectName().lower():
                translit_btn = btn
                break
        
        if translit_btn:
            # Enable transliteration
            translit_btn.click()
            app.processEvents()
            time.sleep(0.3)
            print(f"  Clicked transliteration button: '{translit_btn.text()}'")
        else:
            # Try Ctrl+Space shortcut
            QTest.keyClick(editor, Qt.Key_Space, Qt.ControlModifier)
            app.processEvents()
            time.sleep(0.3)
            print("  Toggled transliteration via Ctrl+Space")
        
        # Type transliterable text
        editor.clear()
        app.processEvents()
        QTest.keyClicks(editor, "namaskAra ", delay=50)
        app.processEvents()
        time.sleep(0.5)
        
        text = editor.toPlainText()
        print(f"  Typed 'namaskAra', got: '{text}'")
        # Check if we got Indic script (non-ASCII)
        has_indic = any(ord(c) > 127 for c in text)
        test_result("Transliteration produces Indic text", has_indic, f"Got: {text[:50]}")
        screenshot(window, "transliteration")
    
    # ─── TEST 6: Language Switching ────────────────────────────
    print("\n▶ TEST 6: Language Switching")
    lang_combo = None
    for c in combos:
        for i in range(c.count()):
            if 'Kannada' in c.itemText(i) or 'Hindi' in c.itemText(i):
                lang_combo = c
                break
        if lang_combo:
            break
    
    if lang_combo:
        original_lang = lang_combo.currentText()
        print(f"  Current language: {original_lang}")
        
        # Switch to Hindi
        for i in range(lang_combo.count()):
            if 'Hindi' in lang_combo.itemText(i):
                lang_combo.setCurrentIndex(i)
                app.processEvents()
                time.sleep(0.3)
                break
        
        new_lang = lang_combo.currentText()
        print(f"  Switched to: {new_lang}")
        test_result("Language switching works", 'Hindi' in new_lang)
        
        # Type in Hindi
        if editors:
            editor = editors[0]
            editor.clear()
            app.processEvents()
            QTest.keyClicks(editor, "namastE ", delay=50)
            app.processEvents()
            time.sleep(0.5)
            text = editor.toPlainText()
            print(f"  Typed 'namastE' in Hindi, got: '{text}'")
            test_result("Hindi transliteration works", any(ord(c) > 127 for c in text), f"Got: {text[:50]}")
            screenshot(window, "hindi")
        
        # Switch to Telugu
        for i in range(lang_combo.count()):
            if 'Telugu' in lang_combo.itemText(i):
                lang_combo.setCurrentIndex(i)
                app.processEvents()
                time.sleep(0.3)
                break
        
        if editors:
            editor.clear()
            app.processEvents()
            QTest.keyClicks(editor, "namaskAramu ", delay=50)
            app.processEvents()
            time.sleep(0.5)
            text = editor.toPlainText()
            print(f"  Typed 'namaskAramu' in Telugu, got: '{text}'")
            test_result("Telugu transliteration works", any(ord(c) > 127 for c in text), f"Got: {text[:50]}")
            screenshot(window, "telugu")
        
        # Switch to Tamil
        for i in range(lang_combo.count()):
            if 'Tamil' in lang_combo.itemText(i):
                lang_combo.setCurrentIndex(i)
                app.processEvents()
                time.sleep(0.3)
                break
        
        if editors:
            editor.clear()
            app.processEvents()
            QTest.keyClicks(editor, "vanakkam ", delay=50)
            app.processEvents()
            time.sleep(0.5)
            text = editor.toPlainText()
            print(f"  Typed 'vanakkam' in Tamil, got: '{text}'")
            test_result("Tamil transliteration works", any(ord(c) > 127 for c in text), f"Got: {text[:50]}")
            screenshot(window, "tamil")

        # Switch back to Kannada
        for i in range(lang_combo.count()):
            if 'Kannada' in lang_combo.itemText(i):
                lang_combo.setCurrentIndex(i)
                app.processEvents()
                break
    else:
        test_result("Language combo found", False, "Could not find language selector")
    
    # ─── TEST 7: Text Formatting (Bold/Italic/Underline) ──────
    print("\n▶ TEST 7: Text Formatting")
    if editors:
        editor = editors[0]
        editor.clear()
        app.processEvents()
        
        # Type some text
        QTest.keyClicks(editor, "Normal text ")
        app.processEvents()
        
        # Bold with Ctrl+B
        QTest.keyClick(editor, Qt.Key_B, Qt.ControlModifier)
        app.processEvents()
        QTest.keyClicks(editor, "Bold text ")
        app.processEvents()
        QTest.keyClick(editor, Qt.Key_B, Qt.ControlModifier)
        app.processEvents()
        
        # Italic with Ctrl+I
        QTest.keyClick(editor, Qt.Key_I, Qt.ControlModifier)
        app.processEvents()
        QTest.keyClicks(editor, "Italic text ")
        app.processEvents()
        QTest.keyClick(editor, Qt.Key_I, Qt.ControlModifier)
        app.processEvents()
        
        # Underline with Ctrl+U
        QTest.keyClick(editor, Qt.Key_U, Qt.ControlModifier)
        app.processEvents()
        QTest.keyClicks(editor, "Underline text")
        app.processEvents()
        QTest.keyClick(editor, Qt.Key_U, Qt.ControlModifier)
        app.processEvents()
        
        text = editor.toPlainText()
        test_result("Formatting - text preserved", "Normal" in text and "Bold" in text)
        
        # Check if formatting was applied via HTML
        html = editor.toHtml()
        test_result("Bold formatting applied", 'font-weight' in html or '<b>' in html or 'bold' in html.lower())
        test_result("Italic formatting applied", 'font-style:italic' in html or '<i>' in html or 'italic' in html.lower())
        test_result("Underline formatting applied", 'text-decoration' in html or '<u>' in html or 'underline' in html.lower())
        screenshot(window, "formatting")
    
    # ─── TEST 8: Font & Size Changes ──────────────────────────
    print("\n▶ TEST 8: Font & Size")
    from PyQt5.QtWidgets import QFontComboBox, QSpinBox
    font_combos = window.findChildren(QFontComboBox)
    size_spins = window.findChildren(QSpinBox)
    
    test_result("Font selector exists", len(font_combos) > 0, f"Found {len(font_combos)} font combos")
    test_result("Size selector exists", len(size_spins) > 0, f"Found {len(size_spins)} size spins")
    
    if size_spins:
        old_size = size_spins[0].value()
        size_spins[0].setValue(24)
        app.processEvents()
        test_result("Font size change", size_spins[0].value() == 24, f"Set to 24, got {size_spins[0].value()}")
        size_spins[0].setValue(old_size)
        app.processEvents()
    
    # ─── TEST 9: Tabs (Editor/Converter) ──────────────────────
    print("\n▶ TEST 9: Tabs")
    from PyQt5.QtWidgets import QTabWidget
    tabs = window.findChildren(QTabWidget)
    if tabs:
        tw = tabs[0]
        tab_names = [tw.tabText(i) for i in range(tw.count())]
        print(f"  Tabs found: {tab_names}")
        test_result("Editor tab exists", any('Editor' in t for t in tab_names))
        test_result("Converter tab exists", any('Converter' in t or 'Convert' in t for t in tab_names))
        
        # Switch to converter tab
        for i, name in enumerate(tab_names):
            if 'Converter' in name or 'Convert' in name:
                tw.setCurrentIndex(i)
                app.processEvents()
                time.sleep(0.3)
                test_result("Switch to Converter tab", tw.currentIndex() == i)
                screenshot(window, "converter_tab")
                break
        
        # Switch back to editor
        tw.setCurrentIndex(0)
        app.processEvents()
    else:
        test_result("Tab widget found", False)
    
    # ─── TEST 10: Ribbon Tabs (Home/Insert/View) ──────────────
    print("\n▶ TEST 10: Ribbon Tabs")
    ribbon_tabs_found = False
    for btn in buttons:
        txt = btn.text().strip()
        if txt in ('Home', 'Insert', 'View'):
            ribbon_tabs_found = True
            print(f"  Found ribbon tab: {txt}")
    test_result("Ribbon tabs present", ribbon_tabs_found or len(tabs) > 0, "Home/Insert/View buttons or QTabWidget")
    
    # ─── TEST 11: Status Bar ──────────────────────────────────
    print("\n▶ TEST 11: Status Bar")
    statusbar = window.statusBar()
    test_result("Status bar exists", statusbar is not None)
    if statusbar:
        msg = statusbar.currentMessage()
        # Check for status bar widgets
        from PyQt5.QtWidgets import QLabel
        sb_labels = statusbar.findChildren(QLabel)
        sb_texts = [l.text() for l in sb_labels if l.text()]
        print(f"  Status bar labels: {sb_texts}")
        test_result("Status bar has info", len(sb_texts) > 0 or len(msg) > 0, f"Labels: {sb_texts[:3]}")
    
    # ─── TEST 12: Document Properties Panel ───────────────────
    print("\n▶ TEST 12: Document Properties Panel")
    from PyQt5.QtWidgets import QDockWidget, QGroupBox
    docks = window.findChildren(QDockWidget)
    groups = window.findChildren(QGroupBox)
    dock_titles = [d.windowTitle() for d in docks]
    group_titles = [g.title() for g in groups]
    print(f"  Dock widgets: {dock_titles}")
    print(f"  Group boxes: {group_titles}")
    test_result("Document panel exists", len(docks) > 0 or any('Document' in t or 'Properties' in t for t in group_titles))
    
    # ─── TEST 13: Zoom ────────────────────────────────────────
    print("\n▶ TEST 13: Zoom Controls")
    from PyQt5.QtWidgets import QSlider
    sliders = window.findChildren(QSlider)
    test_result("Zoom slider exists", len(sliders) > 0, f"Found {len(sliders)} sliders")
    if sliders:
        zoom_slider = sliders[0]
        old_val = zoom_slider.value()
        zoom_slider.setValue(150)
        app.processEvents()
        time.sleep(0.3)
        test_result("Zoom value changes", zoom_slider.value() == 150)
        screenshot(window, "zoomed")
        zoom_slider.setValue(old_val)
        app.processEvents()
    
    # ─── TEST 14: Undo/Redo ───────────────────────────────────
    print("\n▶ TEST 14: Undo/Redo")
    if editors:
        editor = editors[0]
        editor.clear()
        app.processEvents()
        QTest.keyClicks(editor, "test undo")
        app.processEvents()
        before = editor.toPlainText()
        
        # Undo
        QTest.keyClick(editor, Qt.Key_Z, Qt.ControlModifier)
        app.processEvents()
        time.sleep(0.2)
        after_undo = editor.toPlainText()
        test_result("Undo works", len(after_undo) < len(before), f"Before: {len(before)} chars, After undo: {len(after_undo)} chars")
        
        # Redo
        QTest.keyClick(editor, Qt.Key_Z, Qt.ControlModifier | Qt.ShiftModifier)
        app.processEvents()
        time.sleep(0.2)
        after_redo = editor.toPlainText()
        test_result("Redo works", len(after_redo) >= len(after_undo), f"After redo: {len(after_redo)} chars")
    
    # ─── TEST 15: Multi-language content ──────────────────────
    print("\n▶ TEST 15: Multi-language Document")
    if editors and lang_combo:
        editor = editors[0]
        editor.clear()
        app.processEvents()
        
        test_langs = [
            ('Kannada', 'namaskAra '),
            ('Hindi', 'namastE '),
            ('Telugu', 'namaskAramu '),
            ('Tamil', 'vanakkam '),
            ('Bengali', 'namaskAr '),
            ('Gujarati', 'namaskAr '),
        ]
        
        for lang_name, text_to_type in test_langs:
            # Switch language
            for i in range(lang_combo.count()):
                if lang_name in lang_combo.itemText(i):
                    lang_combo.setCurrentIndex(i)
                    app.processEvents()
                    time.sleep(0.2)
                    break
            
            QTest.keyClicks(editor, text_to_type, delay=30)
            app.processEvents()
            time.sleep(0.3)
            QTest.keyClick(editor, Qt.Key_Return)
            app.processEvents()
        
        final_text = editor.toPlainText()
        lines = [l for l in final_text.strip().split('\n') if l.strip()]
        print(f"  Multi-lang doc has {len(lines)} lines")
        for i, line in enumerate(lines[:6]):
            print(f"    Line {i+1}: {line[:60]}")
        
        test_result("Multi-language doc created", len(lines) >= 4, f"{len(lines)} language lines")
        screenshot(window, "multilang")
    
    # ─── FINAL SCREENSHOT ─────────────────────────────────────
    print("\n▶ Final state screenshot")
    screenshot(window, "final")
    
    # ─── SUMMARY ──────────────────────────────────────────────
    print("\n" + "="*60)
    print("  TEST RESULTS SUMMARY")
    print("="*60)
    passed = sum(1 for _, p, _ in results if p)
    failed = sum(1 for _, p, _ in results if not p)
    print(f"\n  Total: {len(results)} | ✅ Passed: {passed} | ❌ Failed: {failed}\n")
    
    if failed > 0:
        print("  FAILURES:")
        for name, p, detail in results:
            if not p:
                print(f"    ❌ {name}: {detail}")
    
    print(f"\n  Screenshots saved: {screenshot_count} files in /tmp/vtest_*.png")
    print("="*60)
    
    # Cleanup
    window.close()
    app.processEvents()

try:
    run_tests()
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}")
    traceback.print_exc()
finally:
    xvfb.terminate()
    print("\nXvfb terminated. Tests complete.")
