import sys, os, time, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, r'Z:\root\.openclaw\workspace\varnaakshara-ime')

from PyQt5.QtWidgets import QApplication, QComboBox, QPushButton, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtTest import QTest

app = QApplication(sys.argv)
from app import VarnaaksharaApp
w = VarnaaksharaApp()
w.show()
w.resize(1300, 850)
app.processEvents()
time.sleep(1)

ed = w.editor

# Set font size 12 like the design
for sp in w.findChildren(QSpinBox):
    sp.setValue(12); app.processEvents(); break

ed.clear(); app.processEvents()

def switch_lang(name):
    if hasattr(w, '_lang_buttons'):
        for k, btn in w._lang_buttons.items():
            if name.lower() in k:
                btn.click(); app.processEvents(); time.sleep(0.2)
                return

def typeit(txt, nl=True):
    QTest.keyClicks(ed, txt, delay=12)
    app.processEvents(); time.sleep(0.15)
    if nl:
        QTest.keyClick(ed, Qt.Key_Return); app.processEvents()
    QTest.keyClick(ed, Qt.Key_Space); app.processEvents(); time.sleep(0.1)

# --- Type the same content as the design screenshot ---
# Title (bold, larger)
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()
typeit("varNAkshara - parichaya")
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()

typeit("")

# Subtitle
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()
typeit("Varnaakshara - Introduction")
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()

typeit("")

# Kannada paragraph
typeit("varNAkshara eMbudu bhAratIya bhAShegaLalli Taipu mADalu sahAya mADuva oMdu phOnetik")
typeit("inpuT methaDa eMjin Agide. idu baraha sAphTvEr na muMduvarike yAgi, Adhunika")
typeit("taMtraj~jAna doMdige nirmisalpattiDE.")

typeit("")

# English paragraph
typeit("Varnaakshara is a phonetic transliteration Input Method Engine for Windows")
typeit("that lets you type in 12 Indian languages using a standard English keyboard. Type")
typeit("in Roman letters - see Indian script appear in real-time.")

typeit("")

# Examples
typeit("namaskAra -> namaskAra (Kannada)")

switch_lang('hindi')
typeit("namastE -> namastE (Hindi)")

switch_lang('telugu')
typeit("shrI -> shrI (Telugu)")

switch_lang('tamil')
typeit("vanakkam -> vanakkam (Tamil)")

switch_lang('kannada')

app.processEvents(); time.sleep(0.5)

# Type in panel transliterate input
if hasattr(w, 'translit_input'):
    w.translit_input.setPlainText('namaskAra lOkavE')
    app.processEvents()
    if hasattr(w, '_panel_transliterate'):
        w._panel_transliterate()
        app.processEvents()

time.sleep(0.5)

# Screenshot 1 - full hybrid UI
px = w.grab()
px.save('C:\\hybrid_final.png')
print("[1] Full hybrid UI saved")

# Screenshot 2 - multi-language with features
ed.clear(); app.processEvents()

typeit("")

# Bold heading
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()
typeit("vaishiShTyagaLu - Features")
QTest.keyClick(ed, Qt.Key_B, Qt.ControlModifier); app.processEvents()
typeit("")

switch_lang('kannada')
typeit("12 bhAratIya bhAShegaLa beMbala - kannaDa, hiMdI, telugu, tamiLu, malayALaM, marAThI, saMskRta,")
typeit("beMgALI, asamI, gujarAtI, paMjAbI, oDiyA")

typeit("")

switch_lang('hindi')
typeit("namastE! yah ek bhAratIya bhAShA saMpAdak hai.")

switch_lang('tamil')
typeit("vanakkam! tamizh mozhiyil ezhuthungkaL.")

switch_lang('telugu')
typeit("namaskAramu! telugu lO vrAyaNDi.")

switch_lang('bengali')
typeit("namaskAr! bAMlAy likho.")

switch_lang('gujarati')
typeit("namaskAr! gujarAtImAM lakho.", nl=False)

app.processEvents(); time.sleep(0.5)
px2 = w.grab()
px2.save('C:\\hybrid_multilang.png')
print("[2] Multi-language saved")

txt = ed.toPlainText()
print(f"\nContent: {len(txt)} chars")
for i, ln in enumerate(txt.split('\n')[:12]):
    if ln.strip(): print(f"  {i+1}: {ln[:80]}")

print("\nDONE")
w.close(); app.processEvents()
