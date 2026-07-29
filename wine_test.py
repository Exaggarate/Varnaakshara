#!/usr/bin/env python3
"""Wine visual test — runs the actual Varnaakshara Writer in Wine, types
multi-language content with transliteration ON, and takes screenshots."""

import sys, os, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

app = QApplication(sys.argv)
from app import VarnaaksharaApp
w = VarnaaksharaApp()
w.show()
w.resize(1300, 850)
app.processEvents()
time.sleep(1)

ed = w.editor
combos = w.findChildren(QComboBox)

# Find language combo
lc = None
for c in combos:
    for i in range(c.count()):
        if 'Kannada' in c.itemText(i):
            lc = c; break
    if lc: break

# Ensure transliteration is ON
for btn in w.findChildren(QPushButton):
    if 'transliterat' in btn.text().lower():
        if 'OFF' in btn.text():
            btn.click(); app.processEvents(); time.sleep(0.3)
        print(f"Translit: {btn.text()}")
        break

# Set font size 28
for sp in w.findChildren(QSpinBox):
    sp.setValue(28); app.processEvents(); break

def switch(name):
    if lc:
        for i in range(lc.count()):
            if name in lc.itemText(i):
                lc.setCurrentIndex(i); app.processEvents(); time.sleep(0.2); return

def typeit(txt, nl=True):
    QTest.keyClicks(ed, txt, delay=20)
    app.processEvents(); time.sleep(0.3)
    if nl:
        QTest.keyClick(ed, Qt.Key_Return); app.processEvents()
    QTest.keyClick(ed, Qt.Key_Space); app.processEvents(); time.sleep(0.1)

ed.clear(); app.processEvents()

# === Type multi-language content ===
switch('Kannada')
typeit("varNAkshara - bahubhAShA saMpAdaka")
typeit("")

switch('Kannada')
typeit("namaskAra lOkavE! idhu varNAkshara saMpAdaka.")

switch('Hindi')
typeit("namastE duniyA! yah varNAkshar saMpAdak hai.")

switch('Telugu')
typeit("namaskAramu! idi varNAkshara saMpAdakamu.")

switch('Tamil')
typeit("vanakkam! itu varNAkShara tokuppAn.")

switch('Bengali')
typeit("namaskAr! ei hala varNAkshar saMpAdak.")

switch('Gujarati')
typeit("namaskAr! A varNAkshara saMpAdak chhe.", nl=False)

app.processEvents(); time.sleep(0.5)

# Print content
txt = ed.toPlainText()
print("\n=== CONTENT ===")
for i, ln in enumerate(txt.split('\n')):
    if ln.strip(): print(f"  {i+1}: {ln[:80]}")

# Screenshot 1: Full document
px = w.grab()
px.save('C:\\wine_test_doc.png')
print("\n[1] Document screenshot saved")

# === Test formatting ===
ed.clear(); app.processEvents()
switch('Kannada')

# Normal
typeit("sAmAnya pATha - Normal text", nl=True)

# Bold
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()
typeit("dappavAda pATha - Bold text", nl=True)
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()

# Italic
QTest.keyClick(ed, Qt.Key_I, Qt.ControlModifier); app.processEvents()
typeit("iregulu pATha - Italic text", nl=True)
QTest.keyClick(ed, Qt.Key_I, Qt.ControlModifier); app.processEvents()

# Underline
QTest.keyClick(ed, Qt.Key_U, Qt.ControlModifier); app.processEvents()
typeit("addiTa rekhA pATha - Underline text", nl=False)

app.processEvents(); time.sleep(0.5)
px2 = w.grab()
px2.save('C:\\wine_test_format.png')
print("[2] Formatting screenshot saved")

# === Test Converter tab ===
from PyQt5.QtWidgets import QTabWidget
tabs = w.findChildren(QTabWidget)
for tw in tabs:
    for i in range(tw.count()):
        if 'Converter' in tw.tabText(i) or 'Convert' in tw.tabText(i):
            tw.setCurrentIndex(i); app.processEvents(); time.sleep(0.5)
            px3 = w.grab()
            px3.save('C:\\wine_test_converter.png')
            print("[3] Converter tab screenshot saved")
            tw.setCurrentIndex(0); app.processEvents()
            break

# === Zoom test ===
from PyQt5.QtWidgets import QSlider
sliders = w.findChildren(QSlider)
if sliders:
    sliders[0].setValue(150); app.processEvents(); time.sleep(0.3)
    px4 = w.grab()
    px4.save('C:\\wine_test_zoom.png')
    print("[4] Zoom 150% screenshot saved")
    sliders[0].setValue(100); app.processEvents()

# === Final with rich multi-lang content ===
ed.clear(); app.processEvents()
for sp in w.findChildren(QSpinBox):
    sp.setValue(32); app.processEvents(); break

switch('Kannada')
typeit("varNAkshara")
typeit("")
typeit("bahubhAShA bhAratIya lipi saMpAdaka")
typeit("")

switch('Hindi')
typeit("namastE! yah ek bhAratIya bhAShA saMpAdak hai.")

switch('Tamil')
typeit("vanakkam! tamizh mozhiyil ezhuthungkaL.")

switch('Telugu')
typeit("namaskAramu! telugu lO vrAyaNDi.")

switch('Bengali')
typeit("namaskAr! bAMlAy likho.")

switch('Gujarati')
typeit("namaskAr! gujarAtImAM lakho.", nl=False)

app.processEvents(); time.sleep(0.5)
px5 = w.grab()
px5.save('C:\\wine_test_final.png')
print("[5] Final multi-lang screenshot saved")

txt = ed.toPlainText()
print("\n=== FINAL CONTENT ===")
for i, ln in enumerate(txt.split('\n')):
    if ln.strip(): print(f"  {i+1}: {ln[:80]}")

print("\n=== ALL TESTS COMPLETE ===")
w.close()
app.processEvents()
