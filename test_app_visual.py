#!/usr/bin/env python3
"""
Visual test: Launch Varnaakshara Writer, type multi-language content
with transliteration ON (matching the old Wine screenshot), and screenshot.
"""
import sys, os, time, subprocess

DISPLAY_NUM = 43
os.environ['DISPLAY'] = f':{DISPLAY_NUM}'

subprocess.run(f'kill $(cat /tmp/.X{DISPLAY_NUM}-lock 2>/dev/null) 2>/dev/null; rm -f /tmp/.X{DISPLAY_NUM}-lock /tmp/.X11-unix/X{DISPLAY_NUM}', shell=True)
time.sleep(0.5)

xvfb = subprocess.Popen(['Xvfb', f':{DISPLAY_NUM}', '-screen', '0', '1400x900x24'],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor, QTextCharFormat
from PyQt5.QtTest import QTest

sys.path.insert(0, '/root/.openclaw/workspace/varnaakshara-ime')

app = QApplication(sys.argv)
from app import VarnaaksharaApp
window = VarnaaksharaApp()
window.show()
window.resize(1300, 850)
app.processEvents()
time.sleep(1)

editor = window.editor
combos = None

# Find language combo
from PyQt5.QtWidgets import QComboBox
all_combos = window.findChildren(QComboBox)
lang_combo = None
for c in all_combos:
    for i in range(c.count()):
        if 'Kannada' in c.itemText(i):
            lang_combo = c
            break
    if lang_combo:
        break

# Find transliteration toggle button
from PyQt5.QtWidgets import QPushButton
translit_btn = None
for btn in window.findChildren(QPushButton):
    if 'transliterat' in btn.text().lower() or 'translit' in btn.objectName().lower():
        translit_btn = btn
        break

print(f"Lang combo: {lang_combo is not None}")
print(f"Translit btn: {translit_btn.text() if translit_btn else 'NOT FOUND'}")

# Make sure transliteration is ON
if translit_btn:
    if 'OFF' in translit_btn.text():
        translit_btn.click()
        app.processEvents()
        time.sleep(0.3)
        print(f"Toggled ON: {translit_btn.text()}")
    else:
        print(f"Already ON: {translit_btn.text()}")

# Set font size to 32 like the old screenshot
from PyQt5.QtWidgets import QSpinBox
size_spins = window.findChildren(QSpinBox)
if size_spins:
    size_spins[0].setValue(32)
    app.processEvents()

# Clear editor
editor.clear()
app.processEvents()

def switch_lang(name):
    if lang_combo:
        for i in range(lang_combo.count()):
            if name in lang_combo.itemText(i):
                lang_combo.setCurrentIndex(i)
                app.processEvents()
                time.sleep(0.2)
                return True
    return False

def type_text(text, newline=True):
    QTest.keyClicks(editor, text, delay=30)
    app.processEvents()
    time.sleep(0.3)
    if newline:
        QTest.keyClick(editor, Qt.Key_Return)
        app.processEvents()
        time.sleep(0.1)
    # Flush transliteration by pressing space
    QTest.keyClick(editor, Qt.Key_Space)
    app.processEvents()
    time.sleep(0.2)

print("\n=== Typing multi-language content ===")

# 1. Kannada header
switch_lang('Kannada')
print("Language: Kannada")
type_text("varNAkshara")

# Add a blank line
QTest.keyClick(editor, Qt.Key_Return)
app.processEvents()

# 2. Kannada sentence
type_text("bahubhAShA bhAratIya lipi saMpAdaka")

# 3. Hindi
switch_lang('Hindi')
print("Language: Hindi")
type_text("namaskAr yah ek bahubhAShI saMpAdak hai jo bArah bhAratIya bhAShAoM meiN likhane ke suvidha pradAna karata hai")

# 4. Tamil  
switch_lang('Tamil')
print("Language: Tamil")
type_text("vanakkam ulakam tamizhil ezhuthungka")

# 5. Telugu
switch_lang('Telugu')
print("Language: Telugu")
type_text("namaskAramu telugu bhAShalo rAyaNDi")

# 6. Bengali
switch_lang('Bengali')
print("Language: Bengali")
type_text("namaskAr bAMlA bhAShAy likho")

# 7. Gujarati
switch_lang('Gujarati')
print("Language: Gujarati")
type_text("namaskAr gujarAtI bhAShAmAM", newline=False)

app.processEvents()
time.sleep(0.5)

# Print what we got
text = editor.toPlainText()
print(f"\n=== Editor content ===")
for i, line in enumerate(text.split('\n')):
    if line.strip():
        print(f"  Line {i+1}: {line[:80]}")

# Screenshot
pixmap = window.grab()
out = '/tmp/vtest_visual_final.png'
pixmap.save(out)
print(f"\n📸 Saved: {out}")

# Copy to workspace
import shutil
shutil.copy(out, '/root/.openclaw/workspace/vtest_visual_final.png')
print("📸 Copied to workspace")

window.close()
app.processEvents()
xvfb.terminate()
print("Done.")
