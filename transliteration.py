"""
Transliteration engine for Indian languages using the Baraha scheme.

Architecture:
  1. Roman (Baraha) → Devanagari: canonical transliteration with greedy
     longest-match parsing, virama insertion for conjuncts, vowel sign
     attachment, and word-boundary halant.
  2. Devanagari → Target script: simple character mapping for Kannada,
     Telugu, Tamil.

Supports: Kannada, Hindi (Devanagari), Telugu, Tamil.
"""

# ============================================================
# STAGE 1: BARAHA (ROMAN) → DEVANAGARI MAPPING
# ============================================================

# --- Vowels (standalone forms) ---
BARAHA_VOWELS = {
    'a': '\u0905',    # अ
    'A': '\u0906',    # आ
    'aa': '\u0906',   # आ
    'i': '\u0907',    # इ
    'I': '\u0908',    # ई
    'ee': '\u090F',   # ए (long e — practical Baraha)
    'ii': '\u0908',   # ई (long i alias)
    'u': '\u0909',    # उ
    'U': '\u090A',    # ऊ
    'oo': '\u0913',   # ओ (long o — practical Baraha)
    'Ru': '\u090B',   # ऋ
    'RU': '\u0960',   # ॠ
    '~lu': '\u090C',  # ऌ
    '~lU': '\u0961',  # ॡ
    'e': '\u090E',    # ऎ (short e)
    'E': '\u090F',    # ए (long e)
    'ai': '\u0910',   # ऐ
    'o': '\u0912',    # ऒ (short o)
    'O': '\u0913',    # ओ (long o)
    'au': '\u0914',   # औ
    'ou': '\u0914',   # औ
    '~e': '\u090D',   # ऍ (candra e — English 'a' as in cat, used in Marathi/Hindi)
    '~o': '\u0911',   # ऑ (candra o — English 'o' as in ball, used in Hindi loanwords)
}

# --- Vowel signs (matras, used after consonants) ---
BARAHA_VOWEL_SIGNS = {
    'a': '',           # inherent vowel, no sign
    'A': '\u093E',     # ा
    'aa': '\u093E',    # ा
    'i': '\u093F',     # ि
    'I': '\u0940',     # ी
    'ee': '\u0947',    # े (long e sign — practical Baraha)
    'ii': '\u0940',    # ी (long i sign alias)
    'u': '\u0941',     # ु
    'U': '\u0942',     # ू
    'oo': '\u094B',    # ो (long o sign — practical Baraha)
    'Ru': '\u0943',    # ृ
    'RU': '\u0944',    # ॄ
    '~lu': '\u0962',   # ॢ
    '~lU': '\u0963',   # ॣ
    'e': '\u0946',     # ॆ (short e sign)
    'E': '\u0947',     # े (long e sign)
    'ai': '\u0948',    # ै
    'o': '\u094A',     # ॊ (short o sign)
    'O': '\u094B',     # ो (long o sign)
    'au': '\u094C',    # ौ
    'ou': '\u094C',    # ौ
    '~e': '\u0945',    # ॅ (candra e sign)
    '~o': '\u0949',    # ॉ (candra o sign)
}

# --- Consonants ---
BARAHA_CONSONANTS = {
    # Ka-varga
    'k': '\u0915',     # क
    'kh': '\u0916',    # ख
    'K': '\u0916',     # ख
    'g': '\u0917',     # ग
    'gh': '\u0918',    # घ
    'G': '\u0918',     # घ
    '~g': '\u0919',    # ङ
    # Cha-varga
    'ch': '\u091A',    # च
    'c': '\u091A',     # च
    'Ch': '\u091B',    # छ
    'C': '\u091B',     # छ
    'j': '\u091C',     # ज
    'jh': '\u091D',    # झ
    'J': '\u091D',     # झ
    '~j': '\u091E',    # ञ
    # Ta-varga (retroflex)
    'T': '\u091F',     # ट
    'Th': '\u0920',    # ठ
    'D': '\u0921',     # ड
    'Dh': '\u0922',    # ढ
    'N': '\u0923',     # ण
    # ta-varga (dental)
    't': '\u0924',     # त
    'th': '\u0925',    # थ
    'd': '\u0926',     # द
    'dh': '\u0927',    # ध
    'n': '\u0928',     # न
    # Pa-varga
    'p': '\u092A',     # प
    'ph': '\u092B',    # फ
    'P': '\u092B',     # फ
    'b': '\u092C',     # ब
    'bh': '\u092D',    # भ
    'B': '\u092D',     # भ
    'm': '\u092E',     # म
    # Antahstha (semivowels)
    'y': '\u092F',     # य
    'r': '\u0930',     # र
    'l': '\u0932',     # ल
    'v': '\u0935',     # व
    'w': '\u0935',     # व
    # Ushma (sibilants/fricatives)
    'sh': '\u0936',    # श
    'S': '\u0936',     # श
    'Sh': '\u0937',    # ष
    's': '\u0938',     # स
    'h': '\u0939',     # ह
    '~h': '\u0939',    # ह
    'L': '\u0933',     # ळ
    # Conjunct consonants
    'kSh': '\u0915\u094D\u0937',  # क्ष
    'j~j': '\u091C\u094D\u091E',  # ज्ञ
    # Extra consonants (with nukta)
    'kx': '\u0958',    # क़
    'Kx': '\u0959',    # ख़
    'gx': '\u095A',    # ग़
    'z': '\u095B',     # ज़
    'jx': '\u095B',    # ज़
    'Dx': '\u095C',    # ड़
    'Dhx': '\u095D',   # ढ़
    'f': '\u095E',     # फ़
    'Px': '\u095E',    # फ़
    'Y': '\u095F',     # य़
    'yx': '\u095F',    # य़
    'rx': '\u0931',    # ऱ
    'Lx': '\u0934',    # ऴ (ழ in Tamil, ഴ in Malayalam)
    'zh': '\u0934',    # ऴ — common alias for Tamil ழ (e.g. tamizh → தமிழ்)
    'nx': '\u0929',    # ऩ (ன in Tamil — alveolar n)
}

# --- Yogavaahas ---
BARAHA_YOGAVAAHAS = {
    'M': '\u0902',     # ं (anusvara)
    'H': '\u0903',     # ः (visarga)
    '~M': '\u0901',    # ँ (chandrabindu)
}

# --- Digits ---
BARAHA_DIGITS = {
    '0': '\u0966', '1': '\u0967', '2': '\u0968', '3': '\u0969', '4': '\u096A',
    '5': '\u096B', '6': '\u096C', '7': '\u096D', '8': '\u096E', '9': '\u096F',
}

# --- Symbols ---
BARAHA_SYMBOLS = {
    'OM': '\u0950',    # ॐ
    '&': '\u093D',     # ऽ (avagraha)
    '||': '\u0965',    # ॥ (double danda)
    '|': '\u0964',     # । (danda)
    '##': '\u1CDA',    # ᳚ dīrgha svarita (double vertical line above)
    '#': '\u0951',     # ॑ svarita (single vertical line above)
    '$': '\u0952',     # ॒ anudātta (horizontal line below)
}

DEVANAGARI_VIRAMA = '\u094D'  # ्

# ============================================================
# ITRANS SCHEME TABLES
# ============================================================
# ITRANS (Indian Languages TRANSliteration) by Avinash Chopde.
# Standard in Indology/academia. Same Devanagari output codepoints as Baraha —
# only the Roman input keys differ. Stage 2 (Deva→target script) is shared.

ITRANS_VOWELS = {
    'a': '\u0905',      # अ
    'A': '\u0906',      # आ
    'aa': '\u0906',     # आ
    'i': '\u0907',      # इ
    'I': '\u0908',      # ई
    'ii': '\u0908',     # ई
    'u': '\u0909',      # उ
    'U': '\u090A',      # ऊ
    'uu': '\u090A',     # ऊ
    'RRi': '\u090B',    # ऋ
    'R^i': '\u090B',    # ऋ
    'RRI': '\u0960',    # ॠ
    'R^I': '\u0960',    # ॠ
    'LLi': '\u090C',    # ऌ
    'L^i': '\u090C',    # ऌ
    'LLI': '\u0961',    # ॡ
    'L^I': '\u0961',    # ॡ
    'e': '\u090F',      # ए
    'ai': '\u0910',     # ऐ
    'o': '\u0913',      # ओ
    'au': '\u0914',     # औ
    '.c': '\u090D',     # ऍ (candra e)
    '.o': '\u0911',     # ऑ (candra o)
}

ITRANS_VOWEL_SIGNS = {
    'a': '',             # inherent vowel
    'A': '\u093E',      # ा
    'aa': '\u093E',     # ा
    'i': '\u093F',      # ि
    'I': '\u0940',      # ी
    'ii': '\u0940',     # ी
    'u': '\u0941',      # ु
    'U': '\u0942',      # ू
    'uu': '\u0942',     # ू
    'RRi': '\u0943',    # ृ
    'R^i': '\u0943',    # ृ
    'RRI': '\u0944',    # ॄ
    'R^I': '\u0944',    # ॄ
    'LLi': '\u0962',    # ॢ
    'L^i': '\u0962',    # ॢ
    'LLI': '\u0963',    # ॣ
    'L^I': '\u0963',    # ॣ
    'e': '\u0947',      # े
    'ai': '\u0948',     # ै
    'o': '\u094B',      # ो
    'au': '\u094C',     # ौ
    '.c': '\u0945',     # ॅ (candra e sign)
    '.o': '\u0949',     # ॉ (candra o sign)
}

ITRANS_CONSONANTS = {
    # Ka-varga
    'k': '\u0915',      # क
    'kh': '\u0916',     # ख
    'g': '\u0917',      # ग
    'gh': '\u0918',     # घ
    '~N': '\u0919',     # ङ
    'N^': '\u0919',     # ङ
    # Cha-varga
    'ch': '\u091A',     # च
    'chh': '\u091B',    # छ
    'Ch': '\u091B',     # छ
    'j': '\u091C',      # ज
    'jh': '\u091D',     # झ
    '~n': '\u091E',     # ञ
    'JN': '\u091E',     # ञ
    # Ta-varga (retroflex)
    'T': '\u091F',      # ट
    'Th': '\u0920',     # ठ
    'D': '\u0921',      # ड
    'Dh': '\u0922',     # ढ
    'N': '\u0923',      # ण
    # ta-varga (dental)
    't': '\u0924',      # त
    'th': '\u0925',     # थ
    'd': '\u0926',      # द
    'dh': '\u0927',     # ध
    'n': '\u0928',      # न
    # Pa-varga
    'p': '\u092A',      # प
    'ph': '\u092B',     # फ
    'b': '\u092C',      # ब
    'bh': '\u092D',     # भ
    'm': '\u092E',      # म
    # Antahstha (semivowels)
    'y': '\u092F',      # य
    'r': '\u0930',      # र
    'l': '\u0932',      # ल
    'v': '\u0935',      # व
    'w': '\u0935',      # व
    # Ushma (sibilants/fricatives)
    'sh': '\u0936',     # श
    'Sh': '\u0937',     # ष
    'shh': '\u0937',    # ष (ITRANS alt)
    's': '\u0938',      # स
    'h': '\u0939',      # ह
    'ld': '\u0933',     # ळ (ITRANS: ld for retroflex lateral)
    # Conjuncts
    'kSh': '\u0915\u094D\u0937',  # क्ष
    'x': '\u0915\u094D\u0937',    # क्ष (ITRANS shortcut)
    'GY': '\u091C\u094D\u091E',   # ज्ञ
    'dny': '\u091C\u094D\u091E',  # ज्ञ (Marathi style)
    'j~n': '\u091C\u094D\u091E',  # ज्ञ
    # Nukta consonants
    'q': '\u0958',      # क़
    '.kh': '\u0959',    # ख़
    '.g': '\u095A',     # ग़
    'z': '\u095B',      # ज़
    '.D': '\u095C',     # ड़
    '.Dh': '\u095D',    # ढ़
    'f': '\u095E',      # फ़
    '.y': '\u095F',     # य़
    '.r': '\u0931',     # ऱ
    'zh': '\u0934',     # ऴ
    '.n~': '\u0929',    # ऩ
}

ITRANS_YOGAVAAHAS = {
    'M': '\u0902',      # ं (anusvara)
    '.m': '\u0902',     # ं (ITRANS alt)
    '.n': '\u0902',     # ं (common ITRANS usage)
    'H': '\u0903',      # ः (visarga)
    '.h': '\u0903',     # ः (ITRANS alt)
    '.N': '\u0901',     # ँ (chandrabindu)
}

ITRANS_SYMBOLS = {
    'OM': '\u0950',     # ॐ
    'AUM': '\u0950',    # ॐ
    '.a': '\u093D',     # ऽ (avagraha)
    '||': '\u0965',     # ॥ (double danda)
    '|': '\u0964',      # । (danda)
    '##': '\u1CDA',     # ᳚ dīrgha svarita
    '#': '\u0951',      # ॑ svarita
    '$': '\u0952',      # ॒ anudātta
}

# Scheme registry: maps scheme name to its tables
SCHEMES = {
    'baraha': {
        'vowels': BARAHA_VOWELS,
        'vowel_signs': BARAHA_VOWEL_SIGNS,
        'consonants': BARAHA_CONSONANTS,
        'yogavaahas': BARAHA_YOGAVAAHAS,
        'symbols': BARAHA_SYMBOLS,
        'digits': BARAHA_DIGITS,
    },
    'itrans': {
        'vowels': ITRANS_VOWELS,
        'vowel_signs': ITRANS_VOWEL_SIGNS,
        'consonants': ITRANS_CONSONANTS,
        'yogavaahas': ITRANS_YOGAVAAHAS,
        'symbols': ITRANS_SYMBOLS,
        'digits': BARAHA_DIGITS,  # digits are same for both
    },
}

# ============================================================
# STAGE 2: DEVANAGARI → TARGET SCRIPT MAPPINGS
# ============================================================

# --- Devanagari → Kannada ---
DEVA_TO_KANNADA = {
    # Vowels
    '\u0905': '\u0C85',  # अ→ಅ
    '\u0906': '\u0C86',  # आ→ಆ
    '\u0907': '\u0C87',  # इ→ಇ
    '\u0908': '\u0C88',  # ई→ಈ
    '\u0909': '\u0C89',  # उ→ಉ
    '\u090A': '\u0C8A',  # ऊ→ಊ
    '\u090B': '\u0C8B',  # ऋ→ಋ
    '\u0960': '\u0CE0',  # ॠ→ೠ
    '\u090C': '\u0C8C',  # ऌ→ಌ
    '\u0961': '\u0CE1',  # ॡ→ೡ
    '\u090E': '\u0C8E',  # ऎ→ಎ
    '\u090F': '\u0C8F',  # ए→ಏ
    '\u0910': '\u0C90',  # ऐ→ಐ
    '\u0912': '\u0C92',  # ऒ→ಒ
    '\u0913': '\u0C93',  # ओ→ಓ
    '\u0914': '\u0C94',  # औ→ಔ
    # Vowel signs
    '\u093E': '\u0CBE',  # ा→ಾ
    '\u093F': '\u0CBF',  # ि→ಿ
    '\u0940': '\u0CC0',  # ी→ೀ
    '\u0941': '\u0CC1',  # ु→ು
    '\u0942': '\u0CC2',  # ू→ೂ
    '\u0943': '\u0CC3',  # ृ→ೃ
    '\u0944': '\u0CC4',  # ॄ→ೄ
    '\u0962': '\u0CE2',  # ॢ→ೢ
    '\u0963': '\u0CE3',  # ॣ→ೣ
    '\u0946': '\u0CC6',  # ॆ→ೆ
    '\u0947': '\u0CC7',  # े→ೇ
    '\u0948': '\u0CC8',  # ै→ೈ
    '\u094A': '\u0CCA',  # ॊ→ೊ
    '\u094B': '\u0CCB',  # ो→ೋ
    '\u094C': '\u0CCC',  # ौ→ೌ
    # Yogavaahas
    '\u0902': '\u0C82',  # ं→ಂ
    '\u0903': '\u0C83',  # ः→ಃ
    '\u0901': '\u0C81',  # ँ→ಁ
    # Virama
    '\u094D': '\u0CCD',  # ्→್
    # Consonants
    '\u0915': '\u0C95',  # क→ಕ
    '\u0916': '\u0C96',  # ख→ಖ
    '\u0917': '\u0C97',  # ग→ಗ
    '\u0918': '\u0C98',  # घ→ಘ
    '\u0919': '\u0C99',  # ङ→ಙ
    '\u091A': '\u0C9A',  # च→ಚ
    '\u091B': '\u0C9B',  # छ→ಛ
    '\u091C': '\u0C9C',  # ज→ಜ
    '\u091D': '\u0C9D',  # झ→ಝ
    '\u091E': '\u0C9E',  # ञ→ಞ
    '\u091F': '\u0C9F',  # ट→ಟ
    '\u0920': '\u0CA0',  # ठ→ಠ
    '\u0921': '\u0CA1',  # ड→ಡ
    '\u0922': '\u0CA2',  # ढ→ಢ
    '\u0923': '\u0CA3',  # ण→ಣ
    '\u0924': '\u0CA4',  # त→ತ
    '\u0925': '\u0CA5',  # थ→ಥ
    '\u0926': '\u0CA6',  # द→ದ
    '\u0927': '\u0CA7',  # ध→ಧ
    '\u0928': '\u0CA8',  # न→ನ
    '\u0929': '\u0CA9',  # ऩ→ೞ (approx)
    '\u092A': '\u0CAA',  # प→ಪ
    '\u092B': '\u0CAB',  # फ→ಫ
    '\u092C': '\u0CAC',  # ब→ಬ
    '\u092D': '\u0CAD',  # भ→ಭ
    '\u092E': '\u0CAE',  # म→ಮ
    '\u092F': '\u0CAF',  # य→ಯ
    '\u0930': '\u0CB0',  # र→ರ
    '\u0931': '\u0CB1',  # ऱ→ಱ
    '\u0932': '\u0CB2',  # ल→ಲ
    '\u0933': '\u0CB3',  # ळ→ಳ
    '\u0934': '\u0CB4',  # ऴ→ೞ
    '\u0935': '\u0CB5',  # व→ವ
    '\u0936': '\u0CB6',  # श→ಶ
    '\u0937': '\u0CB7',  # ष→ಷ
    '\u0938': '\u0CB8',  # स→ಸ
    '\u0939': '\u0CB9',  # ह→ಹ
    # Nukta consonants (map to base in Kannada)
    '\u0958': '\u0C95',  # क़→ಕ
    '\u0959': '\u0C96',  # ख़→ಖ
    '\u095A': '\u0C97',  # ग़→ಗ
    '\u095B': '\u0C9C',  # ज़→ಜ
    '\u095C': '\u0CA1',  # ड़→ಡ
    '\u095D': '\u0CA2',  # ढ़→ಢ
    '\u095E': '\u0CAB',  # फ़→ಫ
    '\u095F': '\u0CAF',  # य़→ಯ
    # Digits
    '\u0966': '\u0CE6',  # ०→೦
    '\u0967': '\u0CE7',  # १→೧
    '\u0968': '\u0CE8',  # २→೨
    '\u0969': '\u0CE9',  # ३→೩
    '\u096A': '\u0CEA',  # ४→೪
    '\u096B': '\u0CEB',  # ५→೫
    '\u096C': '\u0CEC',  # ६→೬
    '\u096D': '\u0CED',  # ७→೭
    '\u096E': '\u0CEE',  # ८→೮
    '\u096F': '\u0CEF',  # ९→೯
    # Symbols
    # \u0950 (ॐ) intentionally NOT mapped — it's universal across all Indic scripts
    '\u093D': '\u0CBD',  # ऽ→ಽ
    '\u0964': '\u0964',  # ।→। (shared)
    '\u0965': '\u0965',  # ॥→॥ (shared)
}

# --- Devanagari → Telugu ---
DEVA_TO_TELUGU = {
    # Vowels
    '\u0905': '\u0C05',  # అ
    '\u0906': '\u0C06',  # ఆ
    '\u0907': '\u0C07',  # ఇ
    '\u0908': '\u0C08',  # ఈ
    '\u0909': '\u0C09',  # ఉ
    '\u090A': '\u0C0A',  # ఊ
    '\u090B': '\u0C0B',  # ఋ
    '\u0960': '\u0C60',  # ౠ
    '\u090C': '\u0C0C',  # ఌ
    '\u0961': '\u0C61',  # ౡ
    '\u090E': '\u0C0E',  # ఎ
    '\u090F': '\u0C0F',  # ఏ
    '\u0910': '\u0C10',  # ఐ
    '\u0912': '\u0C12',  # ఒ
    '\u0913': '\u0C13',  # ఓ
    '\u0914': '\u0C14',  # ఔ
    # Vowel signs
    '\u093E': '\u0C3E',  # ా
    '\u093F': '\u0C3F',  # ి
    '\u0940': '\u0C40',  # ీ
    '\u0941': '\u0C41',  # ు
    '\u0942': '\u0C42',  # ూ
    '\u0943': '\u0C43',  # ృ
    '\u0944': '\u0C44',  # ౄ
    '\u0946': '\u0C46',  # ె
    '\u0947': '\u0C47',  # ే
    '\u0948': '\u0C48',  # ై
    '\u094A': '\u0C4A',  # ొ
    '\u094B': '\u0C4B',  # ో
    '\u094C': '\u0C4C',  # ౌ
    # Yogavaahas
    '\u0902': '\u0C02',  # ం
    '\u0903': '\u0C03',  # ః
    '\u0901': '\u0C01',  # ఁ
    # Virama
    '\u094D': '\u0C4D',  # ్
    # Consonants
    '\u0915': '\u0C15',  # క
    '\u0916': '\u0C16',  # ఖ
    '\u0917': '\u0C17',  # గ
    '\u0918': '\u0C18',  # ఘ
    '\u0919': '\u0C19',  # ఙ
    '\u091A': '\u0C1A',  # చ
    '\u091B': '\u0C1B',  # ఛ
    '\u091C': '\u0C1C',  # జ
    '\u091D': '\u0C1D',  # ఝ
    '\u091E': '\u0C1E',  # ఞ
    '\u091F': '\u0C1F',  # ట
    '\u0920': '\u0C20',  # ఠ
    '\u0921': '\u0C21',  # డ
    '\u0922': '\u0C22',  # ఢ
    '\u0923': '\u0C23',  # ణ
    '\u0924': '\u0C24',  # త
    '\u0925': '\u0C25',  # థ
    '\u0926': '\u0C26',  # ద
    '\u0927': '\u0C27',  # ధ
    '\u0928': '\u0C28',  # న
    '\u092A': '\u0C2A',  # ప
    '\u092B': '\u0C2B',  # ఫ
    '\u092C': '\u0C2C',  # బ
    '\u092D': '\u0C2D',  # భ
    '\u092E': '\u0C2E',  # మ
    '\u092F': '\u0C2F',  # య
    '\u0930': '\u0C30',  # ర
    '\u0931': '\u0C31',  # ఱ
    '\u0932': '\u0C32',  # ల
    '\u0933': '\u0C33',  # ళ
    '\u0934': '\u0C34',  # ఴ
    '\u0935': '\u0C35',  # వ
    '\u0936': '\u0C36',  # శ
    '\u0937': '\u0C37',  # ష
    '\u0938': '\u0C38',  # స
    '\u0939': '\u0C39',  # హ
    # Nukta consonants
    '\u0958': '\u0C15',  '\u0959': '\u0C16',  '\u095A': '\u0C17',
    '\u095B': '\u0C1C',  '\u095C': '\u0C21',  '\u095D': '\u0C22',
    '\u095E': '\u0C2B',  '\u095F': '\u0C2F',
    # Digits
    '\u0966': '\u0C66',  '\u0967': '\u0C67',  '\u0968': '\u0C68',
    '\u0969': '\u0C69',  '\u096A': '\u0C6A',  '\u096B': '\u0C6B',
    '\u096C': '\u0C6C',  '\u096D': '\u0C6D',  '\u096E': '\u0C6E',
    '\u096F': '\u0C6F',
    # Symbols
    '\u0964': '\u0964',  '\u0965': '\u0965',
    '\u093D': '\u0C3D',
}

# --- Devanagari → Tamil ---
# Tamil has fewer consonants; many Devanagari consonants merge.
DEVA_TO_TAMIL = {
    # Vowels
    '\u0905': '\u0B85',  # அ
    '\u0906': '\u0B86',  # ஆ
    '\u0907': '\u0B87',  # இ
    '\u0908': '\u0B88',  # ஈ
    '\u0909': '\u0B89',  # உ
    '\u090A': '\u0B8A',  # ஊ
    '\u090E': '\u0B8E',  # எ
    '\u090F': '\u0B8F',  # ஏ
    '\u0910': '\u0B90',  # ஐ
    '\u0912': '\u0B92',  # ஒ
    '\u0913': '\u0B93',  # ஓ
    '\u0914': '\u0B94',  # ஔ
    # Vowel signs
    '\u093E': '\u0BBE',  # ா
    '\u093F': '\u0BBF',  # ி
    '\u0940': '\u0BC0',  # ீ
    '\u0941': '\u0BC1',  # ு
    '\u0942': '\u0BC2',  # ூ
    '\u0946': '\u0BC6',  # ெ
    '\u0947': '\u0BC7',  # ே
    '\u0948': '\u0BC8',  # ை
    '\u094A': '\u0BCA',  # ொ
    '\u094B': '\u0BCB',  # ோ
    '\u094C': '\u0BCC',  # ௌ
    # Yogavaahas
    '\u0902': '\u0B82',  # ஂ
    '\u0903': '\u0B83',  # ஃ
    # Virama
    '\u094D': '\u0BCD',  # ்
    # Consonants — Tamil merges many
    '\u0915': '\u0B95',  # க (ka-varga all → க)
    '\u0916': '\u0B95',  # க
    '\u0917': '\u0B95',  # க
    '\u0918': '\u0B95',  # க
    '\u0919': '\u0B99',  # ங
    '\u091A': '\u0B9A',  # ச
    '\u091B': '\u0B9A',  # ச
    '\u091C': '\u0B9C',  # ஜ
    '\u091D': '\u0B9A',  # ச
    '\u091E': '\u0B9E',  # ஞ
    '\u091F': '\u0B9F',  # ட
    '\u0920': '\u0B9F',  # ட
    '\u0921': '\u0B9F',  # ட
    '\u0922': '\u0B9F',  # ட
    '\u0923': '\u0BA3',  # ண
    '\u0924': '\u0BA4',  # த
    '\u0925': '\u0BA4',  # த
    '\u0926': '\u0BA4',  # த
    '\u0927': '\u0BA4',  # த
    '\u0928': '\u0BA8',  # ந
    '\u0929': '\u0BA9',  # ன
    '\u092A': '\u0BAA',  # ப
    '\u092B': '\u0BAA',  # ப
    '\u092C': '\u0BAA',  # ப
    '\u092D': '\u0BAA',  # ப
    '\u092E': '\u0BAE',  # ம
    '\u092F': '\u0BAF',  # ய
    '\u0930': '\u0BB0',  # ர
    '\u0931': '\u0BB1',  # ற
    '\u0932': '\u0BB2',  # ல
    '\u0933': '\u0BB3',  # ள
    '\u0934': '\u0BB4',  # ழ
    '\u0935': '\u0BB5',  # வ
    '\u0936': '\u0BB6',  # ஶ
    '\u0937': '\u0BB7',  # ஷ
    '\u0938': '\u0BB8',  # ஸ
    '\u0939': '\u0BB9',  # ஹ
    # Digits
    '\u0966': '\u0BE6',  '\u0967': '\u0BE7',  '\u0968': '\u0BE8',
    '\u0969': '\u0BE9',  '\u096A': '\u0BEA',  '\u096B': '\u0BEB',
    '\u096C': '\u0BEC',  '\u096D': '\u0BED',  '\u096E': '\u0BEE',
    '\u096F': '\u0BEF',
    # Symbols
    '\u0964': '\u0964',  '\u0965': '\u0965',
}

# --- Devanagari → Malayalam ---
DEVA_TO_MALAYALAM = {
    # Vowels
    '\u0905': '\u0D05', '\u0906': '\u0D06', '\u0907': '\u0D07', '\u0908': '\u0D08',
    '\u0909': '\u0D09', '\u090A': '\u0D0A', '\u090B': '\u0D0B', '\u0960': '\u0D60',
    '\u090C': '\u0D0C', '\u0961': '\u0D61',
    '\u090E': '\u0D0E', '\u090F': '\u0D0F', '\u0910': '\u0D10',
    '\u0912': '\u0D12', '\u0913': '\u0D13', '\u0914': '\u0D14',
    # Vowel signs
    '\u093E': '\u0D3E', '\u093F': '\u0D3F', '\u0940': '\u0D40',
    '\u0941': '\u0D41', '\u0942': '\u0D42', '\u0943': '\u0D43', '\u0944': '\u0D44',
    '\u0962': '\u0D62', '\u0963': '\u0D63',
    '\u0946': '\u0D46', '\u0947': '\u0D47', '\u0948': '\u0D48',
    '\u094A': '\u0D4A', '\u094B': '\u0D4B', '\u094C': '\u0D4C',
    # Yogavaahas
    '\u0902': '\u0D02', '\u0903': '\u0D03', '\u0901': '\u0D01',
    # Virama
    '\u094D': '\u0D4D',
    # Consonants
    '\u0915': '\u0D15', '\u0916': '\u0D16', '\u0917': '\u0D17', '\u0918': '\u0D18', '\u0919': '\u0D19',
    '\u091A': '\u0D1A', '\u091B': '\u0D1B', '\u091C': '\u0D1C', '\u091D': '\u0D1D', '\u091E': '\u0D1E',
    '\u091F': '\u0D1F', '\u0920': '\u0D20', '\u0921': '\u0D21', '\u0922': '\u0D22', '\u0923': '\u0D23',
    '\u0924': '\u0D24', '\u0925': '\u0D25', '\u0926': '\u0D26', '\u0927': '\u0D27', '\u0928': '\u0D28',
    '\u092A': '\u0D2A', '\u092B': '\u0D2B', '\u092C': '\u0D2C', '\u092D': '\u0D2D', '\u092E': '\u0D2E',
    '\u092F': '\u0D2F', '\u0930': '\u0D30', '\u0932': '\u0D32', '\u0935': '\u0D35',
    '\u0936': '\u0D36', '\u0937': '\u0D37', '\u0938': '\u0D38', '\u0939': '\u0D39',
    '\u0933': '\u0D33',
    # Extra consonants
    '\u0931': '\u0D31',  # ऱ→റ
    '\u0934': '\u0D34',  # ऴ→ഴ
    # Digits
    '\u0966': '\u0D66', '\u0967': '\u0D67', '\u0968': '\u0D68',
    '\u0969': '\u0D69', '\u096A': '\u0D6A', '\u096B': '\u0D6B',
    '\u096C': '\u0D6C', '\u096D': '\u0D6D', '\u096E': '\u0D6E',
    '\u096F': '\u0D6F',
    # Symbols
    '\u0964': '\u0964', '\u0965': '\u0965',
    '\u093D': '\u0D3D',
}

# --- Devanagari → Bengali ---
DEVA_TO_BENGALI = {
    # Vowels
    '\u0905': '\u0985', '\u0906': '\u0986', '\u0907': '\u0987', '\u0908': '\u0988',
    '\u0909': '\u0989', '\u090A': '\u098A', '\u090B': '\u098B', '\u0960': '\u09E0',
    '\u090C': '\u098C', '\u0961': '\u09E1',
    '\u090F': '\u098F', '\u0910': '\u0990',
    '\u0913': '\u0993', '\u0914': '\u0994',
    # Bengali has no short e/o; map to long
    '\u090E': '\u098F', '\u0912': '\u0993',
    # Vowel signs
    '\u093E': '\u09BE', '\u093F': '\u09BF', '\u0940': '\u09C0',
    '\u0941': '\u09C1', '\u0942': '\u09C2', '\u0943': '\u09C3', '\u0944': '\u09C4',
    '\u0962': '\u09E2', '\u0963': '\u09E3',
    '\u0947': '\u09C7', '\u0948': '\u09C8',
    '\u094B': '\u09CB', '\u094C': '\u09CC',
    '\u0946': '\u09C7', '\u094A': '\u09CB',  # short e/o signs → long
    # Yogavaahas
    '\u0902': '\u0982', '\u0903': '\u0983', '\u0901': '\u0981',
    # Virama
    '\u094D': '\u09CD',
    # Consonants
    '\u0915': '\u0995', '\u0916': '\u0996', '\u0917': '\u0997', '\u0918': '\u0998', '\u0919': '\u0999',
    '\u091A': '\u099A', '\u091B': '\u099B', '\u091C': '\u099C', '\u091D': '\u099D', '\u091E': '\u099E',
    '\u091F': '\u09A0', '\u0920': '\u09A1', '\u0921': '\u09A2', '\u0922': '\u09A3', '\u0923': '\u09A3',
    '\u0924': '\u09A4', '\u0925': '\u09A5', '\u0926': '\u09A6', '\u0927': '\u09A7', '\u0928': '\u09A8',
    '\u092A': '\u09AA', '\u092B': '\u09AB', '\u092C': '\u09AC', '\u092D': '\u09AD', '\u092E': '\u09AE',
    '\u092F': '\u09AF', '\u0930': '\u09B0', '\u0932': '\u09B2', '\u0935': '\u09AC',  # व→ব
    '\u0936': '\u09B6', '\u0937': '\u09B7', '\u0938': '\u09B8', '\u0939': '\u09B9',
    '\u0933': '\u09B2\u09BC',  # ळ→ল়
    # Extra consonants
    '\u0958': '\u0995\u09BC',  # क़→ক়
    '\u0959': '\u0996\u09BC',  # ख़→খ়
    '\u095A': '\u0997\u09BC',  # ग़→গ়
    '\u095B': '\u099C\u09BC',  # ज़→জ়
    '\u095C': '\u09A1\u09BC',  # ड़→ড়
    '\u095D': '\u09A2\u09BC',  # ढ़→ঢ়
    '\u095E': '\u09AB\u09BC',  # फ़→ফ়
    '\u095F': '\u09AF\u09BC',  # य़→য়
    # Digits
    '\u0966': '\u09E6', '\u0967': '\u09E7', '\u0968': '\u09E8',
    '\u0969': '\u09E9', '\u096A': '\u09EA', '\u096B': '\u09EB',
    '\u096C': '\u09EC', '\u096D': '\u09ED', '\u096E': '\u09EE',
    '\u096F': '\u09EF',
    # Symbols
    '\u0964': '\u0964', '\u0965': '\u0965',
    '\u093D': '\u09BD',
}

# --- Devanagari → Gujarati ---
DEVA_TO_GUJARATI = {
    # Vowels
    '\u0905': '\u0A85', '\u0906': '\u0A86', '\u0907': '\u0A87', '\u0908': '\u0A88',
    '\u0909': '\u0A89', '\u090A': '\u0A8A', '\u090B': '\u0A8B', '\u0960': '\u0AE0',
    '\u090C': '\u0A8C', '\u0961': '\u0AE1',
    '\u090F': '\u0A8F', '\u0910': '\u0A90',
    '\u0913': '\u0A93', '\u0914': '\u0A94',
    # Gujarati has no short e/o
    '\u090E': '\u0A8F', '\u0912': '\u0A93',
    # Vowel signs
    '\u093E': '\u0ABE', '\u093F': '\u0ABF', '\u0940': '\u0AC0',
    '\u0941': '\u0AC1', '\u0942': '\u0AC2', '\u0943': '\u0AC3', '\u0944': '\u0AC4',
    '\u0962': '\u0AE2', '\u0963': '\u0AE3',
    '\u0947': '\u0AC7', '\u0948': '\u0AC8',
    '\u094B': '\u0ACB', '\u094C': '\u0ACC',
    '\u0946': '\u0AC7', '\u094A': '\u0ACB',  # short e/o → long
    # Yogavaahas
    '\u0902': '\u0A82', '\u0903': '\u0A83', '\u0901': '\u0A81',
    # Virama
    '\u094D': '\u0ACD',
    # Consonants
    '\u0915': '\u0A95', '\u0916': '\u0A96', '\u0917': '\u0A97', '\u0918': '\u0A98', '\u0919': '\u0A99',
    '\u091A': '\u0A9A', '\u091B': '\u0A9B', '\u091C': '\u0A9C', '\u091D': '\u0A9D', '\u091E': '\u0A9E',
    '\u091F': '\u0A9F', '\u0920': '\u0AA0', '\u0921': '\u0AA1', '\u0922': '\u0AA2', '\u0923': '\u0AA3',
    '\u0924': '\u0AA4', '\u0925': '\u0AA5', '\u0926': '\u0AA6', '\u0927': '\u0AA7', '\u0928': '\u0AA8',
    '\u092A': '\u0AAA', '\u092B': '\u0AAB', '\u092C': '\u0AAC', '\u092D': '\u0AAD', '\u092E': '\u0AAE',
    '\u092F': '\u0AAF', '\u0930': '\u0AB0', '\u0932': '\u0AB2', '\u0935': '\u0AB5',
    '\u0936': '\u0AB6', '\u0937': '\u0AB7', '\u0938': '\u0AB8', '\u0939': '\u0AB9',
    '\u0933': '\u0AB3',
    # Digits
    '\u0966': '\u0AE6', '\u0967': '\u0AE7', '\u0968': '\u0AE8',
    '\u0969': '\u0AE9', '\u096A': '\u0AEA', '\u096B': '\u0AEB',
    '\u096C': '\u0AEC', '\u096D': '\u0AED', '\u096E': '\u0AEE',
    '\u096F': '\u0AEF',
    # Symbols
    '\u0964': '\u0964', '\u0965': '\u0965',
    '\u093D': '\u0ABD',
}

# --- Devanagari → Gurmukhi (Punjabi) ---
DEVA_TO_GURMUKHI = {
    # Vowels
    '\u0905': '\u0A05', '\u0906': '\u0A06', '\u0907': '\u0A07', '\u0908': '\u0A08',
    '\u0909': '\u0A09', '\u090A': '\u0A0A',
    '\u090F': '\u0A0F', '\u0910': '\u0A10',
    '\u0913': '\u0A13', '\u0914': '\u0A14',
    # Gurmukhi has no short e/o, no Ru/RU/lu/lU
    '\u090E': '\u0A0F', '\u0912': '\u0A13',
    '\u090B': '', '\u0960': '', '\u090C': '', '\u0961': '',
    # Vowel signs
    '\u093E': '\u0A3E', '\u093F': '\u0A3F', '\u0940': '\u0A40',
    '\u0941': '\u0A41', '\u0942': '\u0A42',
    '\u0947': '\u0A47', '\u0948': '\u0A48',
    '\u094B': '\u0A4B', '\u094C': '\u0A4C',
    '\u0946': '\u0A47', '\u094A': '\u0A4B',  # short → long
    '\u0943': '', '\u0944': '',  # no Ru sign
    # Yogavaahas
    '\u0902': '\u0A02', '\u0903': '\u0A03', '\u0901': '\u0A01',
    # Virama
    '\u094D': '\u0A4D',
    # Consonants
    '\u0915': '\u0A15', '\u0916': '\u0A16', '\u0917': '\u0A17', '\u0918': '\u0A18', '\u0919': '\u0A19',
    '\u091A': '\u0A1A', '\u091B': '\u0A1B', '\u091C': '\u0A1C', '\u091D': '\u0A1D', '\u091E': '\u0A1E',
    '\u091F': '\u0A1F', '\u0920': '\u0A20', '\u0921': '\u0A21', '\u0922': '\u0A22', '\u0923': '\u0A23',
    '\u0924': '\u0A24', '\u0925': '\u0A25', '\u0926': '\u0A26', '\u0927': '\u0A27', '\u0928': '\u0A28',
    '\u092A': '\u0A2A', '\u092B': '\u0A2B', '\u092C': '\u0A2C', '\u092D': '\u0A2D', '\u092E': '\u0A2E',
    '\u092F': '\u0A2F', '\u0930': '\u0A30', '\u0932': '\u0A32', '\u0935': '\u0A35',
    '\u0936': '\u0A36', '\u0937': '\u0A36\u0A3C',  # ष→ਸ਼਼
    '\u0938': '\u0A38', '\u0939': '\u0A39',
    '\u0933': '\u0A32\u0A3C',  # ळ→ਲ਼
    # Extra consonants
    '\u0958': '\u0A15\u0A3C',  # क़→ਕ਼
    '\u0959': '\u0A16\u0A3C',  # ख़→ਖ਼
    '\u095A': '\u0A17\u0A3C',  # ग़→ਗ਼
    '\u095B': '\u0A1C\u0A3C',  # ज़→ਜ਼
    '\u095C': '\u0A5C',        # ड़→ੜ
    '\u095D': '\u0A5C\u0A4D\u0A39',  # ढ़→ੜ੍ਹ
    '\u095E': '\u0A2B\u0A3C',  # फ़→ਫ਼
    # Digits
    '\u0966': '\u0A66', '\u0967': '\u0A67', '\u0968': '\u0A68',
    '\u0969': '\u0A69', '\u096A': '\u0A6A', '\u096B': '\u0A6B',
    '\u096C': '\u0A6C', '\u096D': '\u0A6D', '\u096E': '\u0A6E',
    '\u096F': '\u0A6F',
    # Symbols
    '\u0964': '\u0964', '\u0965': '\u0965',
}

# --- Devanagari → Odia ---
DEVA_TO_ODIA = {
    # Vowels
    '\u0905': '\u0B05', '\u0906': '\u0B06', '\u0907': '\u0B07', '\u0908': '\u0B08',
    '\u0909': '\u0B09', '\u090A': '\u0B0A', '\u090B': '\u0B0B', '\u0960': '\u0B60',
    '\u090C': '\u0B0C', '\u0961': '\u0B61',
    '\u090F': '\u0B0F', '\u0910': '\u0B10',
    '\u0913': '\u0B13', '\u0914': '\u0B14',
    # Odia has no short e/o
    '\u090E': '\u0B0F', '\u0912': '\u0B13',
    # Vowel signs
    '\u093E': '\u0B3E', '\u093F': '\u0B3F', '\u0940': '\u0B40',
    '\u0941': '\u0B41', '\u0942': '\u0B42', '\u0943': '\u0B43', '\u0944': '\u0B44',
    '\u0962': '\u0B62', '\u0963': '\u0B63',
    '\u0947': '\u0B47', '\u0948': '\u0B48',
    '\u094B': '\u0B4B', '\u094C': '\u0B4C',
    '\u0946': '\u0B47', '\u094A': '\u0B4B',  # short → long
    # Yogavaahas
    '\u0902': '\u0B02', '\u0903': '\u0B03', '\u0901': '\u0B01',
    # Virama
    '\u094D': '\u0B4D',
    # Consonants
    '\u0915': '\u0B15', '\u0916': '\u0B16', '\u0917': '\u0B17', '\u0918': '\u0B18', '\u0919': '\u0B19',
    '\u091A': '\u0B1A', '\u091B': '\u0B1B', '\u091C': '\u0B1C', '\u091D': '\u0B1D', '\u091E': '\u0B1E',
    '\u091F': '\u0B1F', '\u0920': '\u0B20', '\u0921': '\u0B21', '\u0922': '\u0B22', '\u0923': '\u0B23',
    '\u0924': '\u0B24', '\u0925': '\u0B25', '\u0926': '\u0B26', '\u0927': '\u0B27', '\u0928': '\u0B28',
    '\u092A': '\u0B2A', '\u092B': '\u0B2B', '\u092C': '\u0B2C', '\u092D': '\u0B2D', '\u092E': '\u0B2E',
    '\u092F': '\u0B2F', '\u0930': '\u0B30', '\u0932': '\u0B32', '\u0935': '\u0B35',
    '\u0936': '\u0B36', '\u0937': '\u0B37', '\u0938': '\u0B38', '\u0939': '\u0B39',
    '\u0933': '\u0B33',
    # Digits
    '\u0966': '\u0B66', '\u0967': '\u0B67', '\u0968': '\u0B68',
    '\u0969': '\u0B69', '\u096A': '\u0B6A', '\u096B': '\u0B6B',
    '\u096C': '\u0B6C', '\u096D': '\u0B6D', '\u096E': '\u0B6E',
    '\u096F': '\u0B6F',
    # Symbols
    '\u0964': '\u0964', '\u0965': '\u0965',
    '\u093D': '\u0B3D',
}


# ============================================================
# TRANSLITERATION ENGINE
# ============================================================

# Characters that signal a word boundary (consonant gets virama)
WORD_BOUNDARY = set(' \n\t\r.,;:!?()-[]{}\"\'/\\<>@#$%^*+=~`')


class TransliterationEngine:
    """
    Converts phonetic English to Indian script Unicode.
    Supports multiple input schemes (Baraha, ITRANS).

    Usage:
        engine = TransliterationEngine('kannada')           # Baraha default
        engine = TransliterationEngine('sanskrit', scheme='itrans')  # ITRANS
        result = engine.transliterate('namaskaara')
        # → ನಮಸ್ಕಾರ
    """

    def __init__(self, language='kannada', scheme='baraha', custom_mappings=None):
        self._custom_mappings = custom_mappings or {}
        self.set_scheme(scheme)
        self.set_language(language)

    def set_scheme(self, scheme):
        """Set the input scheme (baraha or itrans). Rebuilds sorted key lists."""
        scheme = scheme.lower()
        if scheme not in SCHEMES:
            raise ValueError(f"Unsupported scheme: {scheme}. Available: {list(SCHEMES.keys())}")
        self.scheme = scheme
        tables = SCHEMES[scheme]
        self._consonants = dict(tables['consonants'])
        self._yogavaahas_table = dict(tables['yogavaahas'])
        self._symbols_table = dict(tables['symbols'])
        self._digits_table = dict(tables['digits'])
        # vowels/vowel_signs are set per-language in set_language()
        self._base_vowels = dict(tables['vowels'])
        self._base_vowel_signs = dict(tables['vowel_signs'])
        # Apply custom mappings overlay
        self._apply_custom_mappings()
        self._build_sorted_keys()
        # If language is already set, rebuild per-language vowel tables
        if hasattr(self, 'language'):
            self.set_language(self.language)

    def set_custom_mappings(self, custom_mappings):
        """Update custom mappings and rebuild tables."""
        self._custom_mappings = custom_mappings or {}
        # Re-apply scheme + custom overlay
        self.set_scheme(self.scheme)

    def _apply_custom_mappings(self):
        """Overlay custom user mappings on top of the active scheme tables.

        custom_mappings format:
        {
            "consonants": {"key": "\\u0915", ...},
            "vowels": {"key": "\\u0905", ...},
            "vowel_signs": {"key": "\\u093E", ...},
            "symbols": {"key": "\\u0950", ...},
            "yogavaahas": {"key": "\\u0902", ...}
        }
        """
        cm = self._custom_mappings
        if not cm:
            return
        if 'consonants' in cm:
            self._consonants.update(cm['consonants'])
        if 'vowels' in cm:
            self._base_vowels.update(cm['vowels'])
        if 'vowel_signs' in cm:
            self._base_vowel_signs.update(cm['vowel_signs'])
        if 'symbols' in cm:
            self._symbols_table.update(cm['symbols'])
        if 'yogavaahas' in cm:
            self._yogavaahas_table.update(cm['yogavaahas'])

    def _build_sorted_keys(self):
        """Pre-sort all token lists by length (longest first) for greedy matching."""
        self._sorted_consonants = sorted(self._consonants.keys(), key=len, reverse=True)
        self._sorted_vowels = sorted(self._base_vowels.keys(), key=len, reverse=True)
        self._sorted_vowel_signs = sorted(self._base_vowel_signs.keys(), key=len, reverse=True)
        self._sorted_yogavaahas = sorted(self._yogavaahas_table.keys(), key=len, reverse=True)
        self._sorted_symbols = sorted(self._symbols_table.keys(), key=len, reverse=True)

    # Languages that do NOT distinguish short e/o from long e/o.
    # For these, 'e' → standard ए/े and 'o' → standard ओ/ो (no ऎ/ॆ or ऒ/ॊ).
    _NO_SHORT_EO = {'sanskrit', 'hindi', 'marathi', 'bengali', 'assamese',
                    'gujarati', 'punjabi', 'odia'}

    # Languages with implicit schwa: word-final consonants keep inherent 'a'
    # (no halant). Sanskrit requires explicit 'a'; Dravidian scripts also
    # generally show the halant for bare consonants.
    _IMPLICIT_SCHWA = {'hindi', 'marathi', 'bengali', 'assamese',
                       'gujarati', 'punjabi', 'odia'}

    def set_language(self, language):
        """Set the target language for transliteration."""
        if language not in LANGUAGES:
            raise ValueError(f"Unsupported language: {language}. Available: {list(LANGUAGES.keys())}")
        self.language = language
        self._script_map = LANGUAGES[language]['script_map']
        self._implicit_schwa = language in self._IMPLICIT_SCHWA

        # Build per-language vowel/sign tables from the active scheme
        if language in self._NO_SHORT_EO:
            # Map 'e'→long ए, 'o'→long ओ (no short e/o distinction)
            self._vowels = {**self._base_vowels,
                           'e': '\u090F', 'o': '\u0913'}       # ए, ओ
            self._vowel_signs = {**self._base_vowel_signs,
                                'e': '\u0947', 'o': '\u094B'}  # े, ो
        else:
            # Kannada, Telugu, Tamil, Malayalam — keep short e/o
            self._vowels = self._base_vowels
            self._vowel_signs = self._base_vowel_signs
        # Rebuild sorted vowel keys for the adjusted tables
        self._sorted_vowels = sorted(self._vowels.keys(), key=len, reverse=True)
        self._sorted_vowel_signs = sorted(self._vowel_signs.keys(), key=len, reverse=True)

    def _match_token(self, text, pos, sorted_keys, table):
        """Try to match a token at position `pos` using greedy longest-match.
        Returns (key, devanagari_value) or (None, None)."""
        for key in sorted_keys:
            end = pos + len(key)
            if end <= len(text) and text[pos:end] == key:
                return key, table[key]
        return None, None

    def _is_consonant_start(self, text, pos):
        """Check if position `pos` starts a consonant token."""
        for key in self._sorted_consonants:
            end = pos + len(key)
            if end <= len(text) and text[pos:end] == key:
                return True
        return False

    def _transliterate_to_devanagari(self, text):
        """Parse Roman (Baraha) text and produce Devanagari Unicode string."""
        result = []
        i = 0
        n = len(text)

        while i < n:
            ch = text[i]

            # --- Skip character ---
            if ch == '_':
                i += 1
                continue

            # --- ZWJ / ZWNJ ---
            if ch == '^':
                if i + 1 < n and text[i + 1] == '^':
                    result.append('\u200C')  # ZWNJ
                    i += 2
                else:
                    result.append('\u200D')  # ZWJ
                    i += 1
                continue

            # --- Try conjunct consonants first (kSh, j~j, GY, etc.) ---
            # These are already in the consonant table with longest-match

            # --- Try multi-char symbols before single-char versions claim them ---
            if text[i] == '|' and i + 1 < n and text[i + 1] == '|':
                result.append(self._symbols_table['||'])
                i += 2
                continue
            if text[i] == '#' and i + 1 < n and text[i + 1] == '#':
                result.append(self._symbols_table['##'])
                i += 2
                continue
            # AUM (ITRANS only) — check before vowels consume A/U
            if text[i:i+3] == 'AUM' and 'AUM' in self._symbols_table:
                result.append(self._symbols_table['AUM'])
                i += 3
                continue

            # --- Try consonant ---
            cons_key, cons_deva = self._match_token(text, i, self._sorted_consonants, self._consonants)
            if cons_key is not None:
                i += len(cons_key)
                result.append(cons_deva)

                # After a consonant, look for a vowel sign
                vsign_key, vsign_deva = self._match_token(text, i, self._sorted_vowel_signs, self._vowel_signs)
                if vsign_key is not None:
                    if vsign_key == 'a':
                        # Explicit 'a' = inherent vowel, no sign needed, just consume
                        i += len(vsign_key)
                    else:
                        result.append(vsign_deva)
                        i += len(vsign_key)
                else:
                    # No vowel follows. Check what's next:
                    if i >= n or text[i] in WORD_BOUNDARY:
                        # End of input or word boundary
                        if self._implicit_schwa:
                            pass  # Hindi/Marathi etc.: keep inherent 'a'
                        else:
                            result.append(DEVANAGARI_VIRAMA)  # Sanskrit/Dravidian: halant
                    elif self._is_consonant_start(text, i):
                        # Next is another consonant → virama for conjunct
                        result.append(DEVANAGARI_VIRAMA)
                    elif text[i] == '_':
                        # Skip marker → virama
                        result.append(DEVANAGARI_VIRAMA)
                    else:
                        # Check for yogavaaha (M, H, ~M) - consonant keeps inherent 'a'
                        yog_key, _ = self._match_token(text, i, self._sorted_yogavaahas, self._yogavaahas_table)
                        if yog_key is not None:
                            # Yogavaaha follows — consonant has inherent 'a', yogavaaha appended by main loop
                            pass
                        elif text[i] == '^':
                            # ZWJ/ZWNJ → virama
                            result.append(DEVANAGARI_VIRAMA)
                        elif text[i] in self._symbols_table or self._match_token(text, i, self._sorted_symbols, self._symbols_table)[0] is not None:
                            # Symbol follows (danda, avagraha, etc.) — acts like word boundary
                            if self._implicit_schwa:
                                pass  # keep inherent 'a'
                            else:
                                result.append(DEVANAGARI_VIRAMA)
                        else:
                            # Something else (digit, etc.) → virama
                            result.append(DEVANAGARI_VIRAMA)
                continue

            # --- Try yogavaaha ---
            yog_key, yog_deva = self._match_token(text, i, self._sorted_yogavaahas, self._yogavaahas_table)
            if yog_key is not None:
                result.append(yog_deva)
                i += len(yog_key)
                continue

            # --- Try standalone vowel ---
            vow_key, vow_deva = self._match_token(text, i, self._sorted_vowels, self._vowels)
            if vow_key is not None:
                result.append(vow_deva)
                i += len(vow_key)
                continue

            # --- Try digit ---
            if ch in self._digits_table:
                result.append(self._digits_table[ch])
                i += 1
                continue

            # --- Try symbol ---
            sym_key, sym_deva = self._match_token(text, i, self._sorted_symbols, self._symbols_table)
            if sym_key is not None:
                result.append(sym_deva)
                i += len(sym_key)
                continue

            # --- Pass through unchanged ---
            result.append(ch)
            i += 1

        return ''.join(result)

    def _devanagari_to_target(self, deva_text):
        """Map Devanagari string to target script using character-level mapping."""
        if self._script_map is None:
            return deva_text
        result = []
        for ch in deva_text:
            result.append(self._script_map.get(ch, ch))
        return ''.join(result)

    def transliterate(self, text):
        """Convert phonetic English (Baraha) to target Indian script."""
        deva = self._transliterate_to_devanagari(text)
        return self._devanagari_to_target(deva)

    def process_key(self, char):
        """Process a single keypress for real-time transliteration.
        Returns (output_text, should_flush)."""
        if not hasattr(self, '_buffer'):
            self._buffer = ''
        self._buffer += char

        if char in ' \n\t.,;:!?()-[]{}\"\'/' or char.isdigit():
            output = self.transliterate(self._buffer)
            self._buffer = ''
            return output, True

        return None, False

    def flush(self):
        """Force flush the buffer."""
        if hasattr(self, '_buffer') and self._buffer:
            result = self.transliterate(self._buffer)
            self._buffer = ''
            return result
        return ''


# ============================================================
# LANGUAGE REGISTRY
# ============================================================

LANGUAGES = {
    'kannada': {
        'name': 'Kannada',
        'code': 'kn',
        'script_map': DEVA_TO_KANNADA,
    },
    'hindi': {
        'name': 'Hindi',
        'code': 'hi',
        # Hindi is Devanagari but doesn't have short e/o;
        # map them to their long equivalents.
        'script_map': {
            '\u090E': '\u090F',  # ऎ (short e) → ए (long e)
            '\u0912': '\u0913',  # ऒ (short o) → ओ (long o)
            '\u0946': '\u0947',  # ॆ (short e sign) → े (long e sign)
            '\u094A': '\u094B',  # ॊ (short o sign) → ो (long o sign)
        },
    },
    'telugu': {
        'name': 'Telugu',
        'code': 'te',
        'script_map': DEVA_TO_TELUGU,
    },
    'tamil': {
        'name': 'Tamil',
        'code': 'ta',
        'script_map': DEVA_TO_TAMIL,
    },
    'malayalam': {
        'name': 'Malayalam',
        'code': 'ml',
        'script_map': DEVA_TO_MALAYALAM,
    },
    'marathi': {
        'name': 'Marathi',
        'code': 'mr',
        # Marathi uses Devanagari, same as Hindi (no short e/o)
        'script_map': {
            '\u090E': '\u090F',  '\u0912': '\u0913',
            '\u0946': '\u0947',  '\u094A': '\u094B',
        },
    },
    'sanskrit': {
        'name': 'Sanskrit',
        'code': 'sa',
        # Sanskrit uses Devanagari; has all vowels including short e/o
        'script_map': {},
    },
    'bengali': {
        'name': 'Bengali',
        'code': 'bn',
        'script_map': DEVA_TO_BENGALI,
    },
    'assamese': {
        'name': 'Assamese',
        'code': 'as',
        # Assamese uses Bengali script with one difference: র→ৰ
        'script_map': {**DEVA_TO_BENGALI, '\u0930': '\u09F0'},  # র→ৰ
    },
    'gujarati': {
        'name': 'Gujarati',
        'code': 'gu',
        'script_map': DEVA_TO_GUJARATI,
    },
    'punjabi': {
        'name': 'Punjabi',
        'code': 'pa',
        'script_map': DEVA_TO_GURMUKHI,
    },
    'odia': {
        'name': 'Odia',
        'code': 'or',
        'script_map': DEVA_TO_ODIA,
    },
}


# ============================================================
# ANSI ENCODING SUPPORT
# ============================================================

def unicode_to_ansi_kannada(unicode_text):
    """Convert Unicode Kannada to ANSI (Baraha-compatible font encoding)."""
    UNICODE_TO_ANSI = {
        '\u0C85': 'A', '\u0C86': 'Aa', '\u0C87': 'I', '\u0C88': 'Ii',
        '\u0C89': 'U', '\u0C8A': 'Uu', '\u0C8B': 'Ru',
        '\u0C8E': 'E', '\u0C8F': 'Ee', '\u0C90': 'Ai',
        '\u0C92': 'O', '\u0C93': 'Oo', '\u0C94': 'Au',
        '\u0C95': 'k', '\u0C96': 'K', '\u0C97': 'g', '\u0C98': 'G',
        '\u0C99': '|',
        '\u0C9A': 'c', '\u0C9B': 'C', '\u0C9C': 'j', '\u0C9D': 'J',
        '\u0C9E': '~',
        '\u0C9F': 'q', '\u0CA0': 'Q', '\u0CA1': 'w', '\u0CA2': 'W',
        '\u0CA3': 'N',
        '\u0CA4': 't', '\u0CA5': 'T', '\u0CA6': 'd', '\u0CA7': 'D',
        '\u0CA8': 'n',
        '\u0CAA': 'p', '\u0CAB': 'P', '\u0CAC': 'b', '\u0CAD': 'B',
        '\u0CAE': 'm',
        '\u0CAF': 'y', '\u0CB0': 'r', '\u0CB2': 'l', '\u0CB3': 'L',
        '\u0CB5': 'v', '\u0CB6': 'S', '\u0CB7': 'x', '\u0CB8': 's',
        '\u0CB9': 'h',
        '\u0CBE': 'a', '\u0CBF': 'i', '\u0CC0': 'ii',
        '\u0CC1': 'u', '\u0CC2': 'uu',
        '\u0CC3': 'R',   # ृ sign
        '\u0CC6': 'e', '\u0CC7': 'ee', '\u0CC8': 'Y',
        '\u0CCA': 'o', '\u0CCB': 'oo', '\u0CCC': 'ou',
        '\u0CCD': '\\',  # virama/halant
        '\u0C82': 'M',   # anusvara
        '\u0C83': 'H',   # visarga
    }
    return ''.join(UNICODE_TO_ANSI.get(ch, ch) for ch in unicode_text)


def unicode_to_ansi_hindi(unicode_text):
    """Convert Unicode Hindi to ANSI (legacy font encoding)."""
    UNICODE_TO_ANSI = {
        '\u0905': 'A', '\u0906': 'Aa', '\u0907': 'I', '\u0908': 'Ii',
        '\u0909': 'U', '\u090A': 'Uu', '\u090B': 'Ru',
        '\u090F': 'Ee', '\u0910': 'Ai', '\u0913': 'Oo', '\u0914': 'Au',
        '\u0915': 'k', '\u0916': 'K', '\u0917': 'g', '\u0918': 'G',
        '\u0919': '|',
        '\u091A': 'c', '\u091B': 'C', '\u091C': 'j', '\u091D': 'J',
        '\u091E': '~',
        '\u091F': 'q', '\u0920': 'Q', '\u0921': 'w', '\u0922': 'W',
        '\u0923': 'N',
        '\u0924': 't', '\u0925': 'T', '\u0926': 'd', '\u0927': 'D',
        '\u0928': 'n',
        '\u092A': 'p', '\u092B': 'P', '\u092C': 'b', '\u092D': 'B',
        '\u092E': 'm',
        '\u092F': 'y', '\u0930': 'r', '\u0932': 'l', '\u0933': 'L',
        '\u0935': 'v', '\u0936': 'S', '\u0937': 'x', '\u0938': 's',
        '\u0939': 'h',
        '\u093E': 'a', '\u093F': 'i', '\u0940': 'ii',
        '\u0941': 'u', '\u0942': 'uu',
        '\u0943': 'R',   # ृ sign
        '\u0947': 'ee', '\u0948': 'Y',
        '\u094B': 'oo', '\u094C': 'ou',
        '\u094D': '\\',
        '\u0902': 'M',
        '\u0903': 'H',
        '\u0901': 'z',  # chandrabindu
    }
    return ''.join(UNICODE_TO_ANSI.get(ch, ch) for ch in unicode_text)


ANSI_CONVERTERS = {
    'kannada': unicode_to_ansi_kannada,
    'hindi': unicode_to_ansi_hindi,
}


def convert_to_ansi(unicode_text, language):
    """Convert Unicode Indian script text to ANSI encoding."""
    converter = ANSI_CONVERTERS.get(language)
    if converter:
        return converter(unicode_text)
    return unicode_text


# ============================================================
# TESTS
# ============================================================

if __name__ == '__main__':
    import sys

    passed = 0
    failed = 0
    errors = []

    def test(input_text, expected, language='kannada', label=None):
        global passed, failed
        engine = TransliterationEngine(language)
        result = engine.transliterate(input_text)
        status = '✅' if result == expected else '❌'
        desc = label or input_text
        if result == expected:
            passed += 1
        else:
            failed += 1
            errors.append((desc, language, input_text, expected, result))
        # Show hex for debugging on failure
        extra = ''
        if result != expected:
            extra = f'\n     expected hex: {" ".join(f"U+{ord(c):04X}" for c in expected)}'
            extra += f'\n     got hex:      {" ".join(f"U+{ord(c):04X}" for c in result)}'
        print(f'  {status} {desc:50s} → {result:20s} (expected: {expected}){extra}')

    # ===================== KANNADA =====================
    print('=== KANNADA TESTS ===')

    # Required test cases from spec
    test('nAnu', 'ನಾನು', 'kannada', 'nAnu → ನಾನು')
    test('namaskaara', 'ನಮಸ್ಕಾರ', 'kannada', 'namaskaara → ನಮಸ್ಕಾರ')
    test('namaskAra', 'ನಮಸ್ಕಾರ', 'kannada', 'namaskAra → ನಮಸ್ಕಾರ')
    test('kannaDa', 'ಕನ್ನಡ', 'kannada', 'kannaDa → ಕನ್ನಡ')
    test('amma', 'ಅಮ್ಮ', 'kannada', 'amma → ಅಮ್ಮ')
    test('ga~ggA', 'ಗಙ್ಗಾ', 'kannada', 'ga~ggA → ಗಙ್ಗಾ')
    test('ga~ggEti', 'ಗಙ್ಗೇತಿ', 'kannada', 'ga~ggEti → ಗಙ್ಗೇತಿ')
    test('brUyaat', 'ಬ್ರೂಯಾತ್', 'kannada', 'brUyaat → ಬ್ರೂಯಾತ್')
    test('sha~gkaraacaaryaru', 'ಶಙ್ಕರಾಚಾರ್ಯರು', 'kannada', 'sha~gkaraacaaryaru → ಶಙ್ಕರಾಚಾರ್ಯರು')
    test('RuShigaLu', 'ಋಷಿಗಳು', 'kannada', 'RuShigaLu → ಋಷಿಗಳು')
    test('kRuShNa', 'ಕೃಷ್ಣ', 'kannada', 'kRuShNa → ಕೃಷ್ಣ')
    test('jyOtsnaabhiraahatamahaddhRudayaandhakaaram',
         'ಜ್ಯೋತ್ಸ್ನಾಭಿರಾಹತಮಹದ್ಧೃದಯಾನ್ಧಕಾರಮ್',
         'kannada', 'jyOtsnaabhiraahatamahaddhRudayaandhakaaram')
    test('DralOpE poorvasya dIrGO NaH',
         'ಡ್ರಲೋಪೇ ಪೋರ್ವಸ್ಯ ದೀರ್ಘೋ ಣಃ',
         'kannada', 'DralOpE poorvasya dIrGO NaH')

    # Additional Kannada tests
    test('beMgaLUru', 'ಬೆಂಗಳೂರು', 'kannada', 'beMgaLUru → ಬೆಂಗಳೂರು')
    test('hAgU', 'ಹಾಗೂ', 'kannada', 'hAgU → ಹಾಗೂ')
    test('vishva', 'ವಿಶ್ವ', 'kannada', 'vishva → ವಿಶ್ವ')
    test('oMdu', 'ಒಂದು', 'kannada', 'oMdu → ಒಂದು')
    test('nInu', 'ನೀನು', 'kannada', 'nInu → ನೀನು')
    test('shAlE', 'ಶಾಲೇ', 'kannada', 'shAlE → ಶಾಲೇ')
    test('aidu', 'ಐದು', 'kannada', 'aidu → ಐದು')

    # ===================== HINDI =====================
    print('\n=== HINDI TESTS ===')

    test('namaste', 'नमस्ते', 'hindi', 'namaste → नमस्ते')
    test('bhaarat', 'भारत्', 'hindi', 'bhaarat → भारत् (virama on final t)')
    test('hindii', 'हिन्दी', 'hindi', 'hindii → हिन्दी')
    test('hindI', 'हिन्दी', 'hindi', 'hindI → हिन्दी')
    test('duniyaa', 'दुनिया', 'hindi', 'duniyaa → दुनिया')

    # ===================== TELUGU =====================
    print('\n=== TELUGU TESTS ===')

    test('namaskaaraM', 'నమస్కారం', 'telugu', 'namaskaaraM → నమస్కారం')
    test('telugu', 'తెలుగు', 'telugu', 'telugu → తెలుగు')

    # ===================== TAMIL =====================
    print('\n=== TAMIL TESTS ===')

    test('vanakkam', 'வநக்கம்', 'tamil', 'vanakkam → வநக்கம்')
    test('tamiLx', 'தமிழ்', 'tamil', 'tamiLx → தமிழ் (tamil with Lx=ழ)')

    # ===================== ADDITIONAL COVERAGE =====================
    print('\n=== ADDITIONAL COVERAGE ===')

    # Vowel forms
    test('aidu', 'ಐದು', 'kannada', 'ai vowel → ಐ')
    test('auShada', 'ಔಷದ', 'kannada', 'au vowel → ಔ')
    test('Uru', 'ಊರು', 'kannada', 'U vowel → ಊ')

    # Conjuncts and clusters
    test('kShama', 'ಕ್ಷಮ', 'kannada', 'kSh conjunct → ಕ್ಷ')
    test('j~ja', 'ಜ್ಞ', 'kannada', 'j~j conjunct → ಜ್ಞ')
    test('praj~jA', 'ಪ್ರಜ್ಞಾ', 'kannada', 'praj~jA → ಪ್ರಜ್ಞಾ')
    test('stra', 'ಸ್ತ್ರ', 'kannada', 'triple cluster stra')
    test('strii', 'ಸ್ತ್ರೀ', 'kannada', 'strii → ಸ್ತ್ರೀ')

    # Yogavaahas
    test('rAmaM', 'ರಾಮಂ', 'kannada', 'anusvara M')
    test('duHkha', 'ದುಃಖ', 'kannada', 'visarga H')

    # Digits
    test('123', '೧೨೩', 'kannada', 'digits')

    # Mixed text with spaces and punctuation
    test('rAma sItA', 'ರಾಮ ಸೀತಾ', 'kannada', 'words with space')
    test('namO namaste!', 'ನಮೋ ನಮಸ್ತೆ!', 'kannada', 'punctuation preserved')

    # Explicit 'a' at word end
    test('rama', 'ರಮ', 'kannada', 'rama → ರಮ (explicit a)')
    test('ram', 'ರಮ್', 'kannada', 'ram → ರಮ್ (virama on final m)')

    # Hindi additional
    test('raam', 'राम्', 'hindi', 'raam → राम् (no inherent a on final m)')
    test('rAma', 'राम', 'hindi', 'rAma → राम (explicit a on final m)')
    test('kRuShNa', 'कृष्ण', 'hindi', 'kRuShNa → कृष्ण')
    test('~ga~gA', 'ङङा', 'hindi', '~ga~gA → ङङा (double ~g with vowel)')

    # ===================== SUMMARY =====================
    print(f'\n{"=" * 60}')
    print(f'RESULTS: {passed} passed, {failed} failed, {passed + failed} total')
    if errors:
        print(f'\nFAILURES:')
        for desc, lang, inp, exp, got in errors:
            print(f'  [{lang}] {desc}')
            print(f'    input:    {inp}')
            print(f'    expected: {exp} ({" ".join(f"U+{ord(c):04X}" for c in exp)})')
            print(f'    got:      {got} ({" ".join(f"U+{ord(c):04X}" for c in got)})')
    print(f'{"=" * 60}')

    sys.exit(1 if failed else 0)
