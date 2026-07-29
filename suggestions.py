"""
Varnaakshara Word Suggestion Engine
================================
SQLite-backed dictionary with prefix matching and per-user learning.

Architecture:
- Base dictionary: AOSP + Leipzig word lists (731K words, 9 languages)
- Personal dictionary: per-user learning table (frequency bumps on word completion)
- Prefix matching via SQL LIKE with index optimization
- Returns top N suggestions sorted by frequency (personal > base)

Database: %APPDATA%\\Varnaakshara\\dictionary.db
"""

import sqlite3
import os
import sys
import time


LANG_CODES = {
    'kannada': 'kn', 'hindi': 'hi', 'telugu': 'te', 'tamil': 'ta',
    'malayalam': 'ml', 'marathi': 'mr', 'sanskrit': 'sa',
    'bengali': 'bn', 'gujarati': 'gu',
    'assamese': 'as', 'punjabi': 'pa', 'odia': 'or',
}


def get_db_path():
    """Get the database path. %APPDATA%\\Varnaakshara\\dictionary.db on Windows."""
    if sys.platform == 'win32':
        appdata = os.environ.get('APPDATA', os.path.expanduser('~'))
        db_dir = os.path.join(appdata, 'Varnaakshara')
    else:
        db_dir = os.path.join(os.path.expanduser('~'), '.varnaakshara')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'dictionary.db')


class SuggestionEngine:
    """Word suggestion engine with base + personal dictionary."""

    def __init__(self, db_path=None, min_prefix=3):
        self.db_path = db_path or get_db_path()
        self.min_prefix = min_prefix
        self.conn = None
        self._connect()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA cache_size=-4000")
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS base_dict (
                word TEXT NOT NULL,
                lang TEXT NOT NULL,
                freq INTEGER NOT NULL DEFAULT 128,
                PRIMARY KEY (word, lang)
            );
            CREATE TABLE IF NOT EXISTS user_dict (
                word TEXT NOT NULL,
                lang TEXT NOT NULL,
                freq INTEGER NOT NULL DEFAULT 1,
                last_used REAL NOT NULL,
                PRIMARY KEY (word, lang)
            );
            CREATE INDEX IF NOT EXISTS idx_base_lang_word ON base_dict(lang, word);
            CREATE INDEX IF NOT EXISTS idx_user_lang_word ON user_dict(lang, word);
        """)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def is_loaded(self, lang_code):
        cur = self.conn.execute(
            "SELECT COUNT(*) FROM base_dict WHERE lang = ?", (lang_code,)
        )
        return cur.fetchone()[0] > 0

    def load_wordlist(self, filepath, lang_code, batch_size=5000):
        """Load AOSP/Leipzig wordlist. Format: ' word=X,f=N'"""
        if self.is_loaded(lang_code):
            return

        words = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line.startswith('word='):
                    continue
                parts = line.split(',')
                if len(parts) < 2:
                    continue
                word_part = parts[0]
                freq_part = parts[1]
                if '=' not in word_part or '=' not in freq_part:
                    continue
                word = word_part.split('=', 1)[1].strip()
                try:
                    freq = int(freq_part.split('=', 1)[1].strip())
                except ValueError:
                    freq = 128
                if word and len(word) >= 2:
                    words.append((word, lang_code, freq))
                if len(words) >= batch_size:
                    self.conn.executemany(
                        "INSERT OR IGNORE INTO base_dict (word, lang, freq) VALUES (?, ?, ?)",
                        words
                    )
                    words.clear()
        if words:
            self.conn.executemany(
                "INSERT OR IGNORE INTO base_dict (word, lang, freq) VALUES (?, ?, ?)",
                words
            )
        self.conn.commit()

    def suggest(self, prefix, lang_code, limit=5):
        """
        Get word suggestions for a Unicode prefix.
        Returns list of (word, source) tuples sorted by relevance.
        """
        if len(prefix) < self.min_prefix:
            return []

        results = []

        # User dictionary first (higher priority)
        cur = self.conn.execute(
            """SELECT word, freq FROM user_dict
               WHERE lang = ? AND word LIKE ? || '%'
               ORDER BY freq DESC, last_used DESC
               LIMIT ?""",
            (lang_code, prefix, limit)
        )
        for word, freq in cur:
            results.append((word, 'user', freq + 10000))

        # Base dictionary (fill remaining)
        remaining = limit - len(results)
        if remaining > 0:
            existing = {r[0] for r in results}
            cur = self.conn.execute(
                """SELECT word, freq FROM base_dict
                   WHERE lang = ? AND word LIKE ? || '%'
                   ORDER BY freq DESC
                   LIMIT ?""",
                (lang_code, prefix, remaining + len(existing))
            )
            for word, freq in cur:
                if word not in existing and len(results) < limit:
                    results.append((word, 'base', freq))

        results.sort(key=lambda x: -x[2])
        return [(word, source) for word, source, _ in results]

    def learn_word(self, word, lang_code):
        """Record word completion. Bumps freq in user_dict."""
        now = time.time()
        cur = self.conn.execute(
            "UPDATE user_dict SET freq = freq + 1, last_used = ? WHERE word = ? AND lang = ?",
            (now, word, lang_code)
        )
        if cur.rowcount == 0:
            cur2 = self.conn.execute(
                "SELECT freq FROM base_dict WHERE word = ? AND lang = ?",
                (word, lang_code)
            )
            row = cur2.fetchone()
            base_freq = row[0] if row else 0
            self.conn.execute(
                "INSERT INTO user_dict (word, lang, freq, last_used) VALUES (?, ?, ?, ?)",
                (word, lang_code, base_freq + 1, now)
            )
        self.conn.commit()

    def add_user_word(self, word, lang_code, freq=128):
        now = time.time()
        self.conn.execute(
            "INSERT OR REPLACE INTO user_dict (word, lang, freq, last_used) VALUES (?, ?, ?, ?)",
            (word, lang_code, freq, now)
        )
        self.conn.commit()

    def get_stats(self):
        stats = {}
        cur = self.conn.execute(
            "SELECT lang, COUNT(*) FROM base_dict GROUP BY lang ORDER BY lang"
        )
        stats['base'] = {lang: count for lang, count in cur}
        cur = self.conn.execute(
            "SELECT lang, COUNT(*) FROM user_dict GROUP BY lang ORDER BY lang"
        )
        stats['user'] = {lang: count for lang, count in cur}
        return stats


def build_database(dict_dir, db_path=None):
    """Build SQLite database from wordlist files."""
    engine = SuggestionEngine(db_path=db_path)
    lang_files = {
        'kn': 'kn_wordlist.combined', 'hi': 'hi_wordlist.combined',
        'te': 'te_wordlist.combined', 'ta': 'ta_wordlist.combined',
        'ml': 'ml_wordlist.combined', 'mr': 'mr_wordlist.combined',
        'sa': 'sa_wordlist.combined', 'bn': 'bn_wordlist.combined',
        'gu': 'gu_wordlist.combined',
    }
    total = 0
    for lang_code, filename in lang_files.items():
        filepath = os.path.join(dict_dir, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP {lang_code}: {filename} not found")
            continue
        if engine.is_loaded(lang_code):
            cur = engine.conn.execute(
                "SELECT COUNT(*) FROM base_dict WHERE lang = ?", (lang_code,)
            )
            count = cur.fetchone()[0]
            print(f"  SKIP {lang_code}: already loaded ({count:,} words)")
            total += count
            continue
        print(f"  Loading {lang_code} from {filename}...", end='', flush=True)
        engine.load_wordlist(filepath, lang_code)
        cur = engine.conn.execute(
            "SELECT COUNT(*) FROM base_dict WHERE lang = ?", (lang_code,)
        )
        count = cur.fetchone()[0]
        print(f" {count:,} words")
        total += count
    print(f"\nTotal: {total:,} words across {len(lang_files)} languages")
    engine.close()
    return db_path or get_db_path()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Varnaakshara Suggestion Engine')
    parser.add_argument('--build', metavar='DICT_DIR',
                        help='Build database from wordlist directory')
    parser.add_argument('--db', metavar='DB_PATH',
                        help='Database path (default: auto)')
    parser.add_argument('--test', action='store_true',
                        help='Run suggestion tests')
    parser.add_argument('--stats', action='store_true',
                        help='Show database statistics')
    args = parser.parse_args()

    if args.build:
        print("Building suggestion database...")
        db = build_database(args.build, args.db)
        print(f"Database: {db}")

    if args.test:
        engine = SuggestionEngine(db_path=args.db)
        tests = [
            ('kn', '\u0cae\u0ca4\u0ccd\u0ca4'),      # ಮತ್ತ
            ('kn', '\u0c95\u0cb0\u0ccd\u0ca8\u0cbe'),  # ಕರ್ನಾ
            ('hi', '\u092d\u093e\u0930'),               # भार
            ('hi', '\u0939\u093f\u0928\u094d\u0926'),   # हिन्द
            ('mr', '\u092e\u0930\u093e'),               # मरा
            ('ta', '\u0ba4\u0bae\u0bbf'),               # தமி
        ]
        for lang, prefix in tests:
            results = engine.suggest(prefix, lang, limit=5)
            words = [w for w, _ in results]
            print(f"  {lang} '{prefix}' -> {words}")
        engine.close()

    if args.stats:
        engine = SuggestionEngine(db_path=args.db)
        stats = engine.get_stats()
        print("\nBase dictionary:")
        for lang, count in sorted(stats['base'].items()):
            print(f"  {lang}: {count:,} words")
        print(f"  Total: {sum(stats['base'].values()):,}")
        if stats['user']:
            print("\nUser dictionary:")
            for lang, count in sorted(stats['user'].items()):
                print(f"  {lang}: {count:,} words")
        engine.close()
