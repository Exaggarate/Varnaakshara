import sys, os, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest

app = QApplication(sys.argv)

# Need to set path for imports
sys.path.insert(0, r'Z:\root\.openclaw\workspace\varnaakshara-ime')
from app import VarnaaksharaApp
w = VarnaaksharaApp()
w.show()
w.resize(1300, 850)
app.processEvents()
time.sleep(1)

ed = w.editor

# Set font size 14
for sp in w.findChildren(QSpinBox):
    sp.setValue(14); app.processEvents(); break

ed.clear(); app.processEvents()

# Type some content with transliteration
def typeit(txt, nl=True):
    QTest.keyClicks(ed, txt, delay=15)
    app.processEvents(); time.sleep(0.2)
    if nl:
        QTest.keyClick(ed, Qt.Key_Return); app.processEvents()
    QTest.keyClick(ed, Qt.Key_Space); app.processEvents(); time.sleep(0.1)

# Kannada (default)
typeit("varNAkshara - parichaya")
typeit("")
typeit("varNAkshara eMbudu bhAratIya bhAShegaLalli Taipu mADalu sahAya mADuva oMdu phOnetik")
typeit("inpuT methaDa eMjin Agide.")
typeit("")
typeit("namaskAra -> namaskAra (Kannada)")
typeit("namastE -> namastE (Hindi)")
typeit("shrI -> shrI (Telugu)")
typeit("vanakkam -> vanakkam (Tamil)")

app.processEvents(); time.sleep(0.5)

# Screenshot
px = w.grab()
px.save('C:\\hybrid_ui_test.png')
print("[1] Hybrid UI screenshot saved")

txt = ed.toPlainText()
print(f"\nContent ({len(txt)} chars):")
for i, ln in enumerate(txt.split('\n')[:10]):
    if ln.strip(): print(f"  {i+1}: {ln[:80]}")

print("\nDONE")
w.close()
app.processEvents()
