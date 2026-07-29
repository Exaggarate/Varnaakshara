"""
Tests for Varnaakshara suggestion engine (SQLite-backed dictionary).

Covers database creation, schema, learn_word, suggest, prefix matching,
user dictionary priority, min_prefix filtering, empty results, and stats.
"""

import os
import sys
import time
import sqlite3
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from suggestions import SuggestionEngine, LANG_CODES, get_db_path


# ============================================================
# Database Creation and Schema
# ============================================================

class TestDatabaseCreation:
    """Test database initialization and schema."""

    def test_db_file_created(self, tmp_path):
        """SuggestionEngine creates the database file."""
        db_path = str(tmp_path / 'test.db')
        engine = SuggestionEngine(db_path=db_path)
        assert os.path.exists(db_path)
        engine.close()

    def test_schema_tables_exist(self, suggestion_db):
        """Both base_dict and user_dict tables should exist."""
        cursor = suggestion_db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = {row[0] for row in cursor}
        assert 'base_dict' in tables
        assert 'user_dict' in tables

    def test_schema_base_dict_columns(self, suggestion_db):
        """base_dict should have word, lang, freq columns."""
        cursor = suggestion_db.conn.execute("PRAGMA table_info(base_dict)")
        columns = {row[1] for row in cursor}
        assert 'word' in columns
        assert 'lang' in columns
        assert 'freq' in columns

    def test_schema_user_dict_columns(self, suggestion_db):
        """user_dict should have word, lang, freq, last_used columns."""
        cursor = suggestion_db.conn.execute("PRAGMA table_info(user_dict)")
        columns = {row[1] for row in cursor}
        assert 'word' in columns
        assert 'lang' in columns
        assert 'freq' in columns
        assert 'last_used' in columns

    def test_indexes_created(self, suggestion_db):
        """Indexes should be present for performance."""
        cursor = suggestion_db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='index'"
        )
        index_names = {row[0] for row in cursor}
        assert 'idx_base_lang_word' in index_names
        assert 'idx_user_lang_word' in index_names

    def test_wal_mode(self, suggestion_db):
        """Database should use WAL journal mode."""
        cursor = suggestion_db.conn.execute("PRAGMA journal_mode")
        mode = cursor.fetchone()[0]
        assert mode.lower() == 'wal'

    def test_close_and_reopen(self, tmp_path):
        """Database can be closed and reopened."""
        db_path = str(tmp_path / 'test.db')
        engine = SuggestionEngine(db_path=db_path)
        engine.learn_word('ನಮಸ್ಕಾರ', 'kn')
        engine.close()

        # Reopen
        engine2 = SuggestionEngine(db_path=db_path, min_prefix=2)
        results = engine2.suggest('ನಮಸ', 'kn')
        assert len(results) > 0
        engine2.close()


# ============================================================
# Learn Word
# ============================================================

class TestLearnWord:
    """Test word learning functionality."""

    def test_learn_new_word(self, suggestion_db):
        """Learning a new word adds it to user_dict."""
        suggestion_db.learn_word('ನಮಸ್ಕಾರ', 'kn')
        cursor = suggestion_db.conn.execute(
            "SELECT word, freq FROM user_dict WHERE word=? AND lang=?",
            ('ನಮಸ್ಕಾರ', 'kn')
        )
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == 'ನಮಸ್ಕಾರ'
        assert row[1] >= 1

    def test_learn_word_increments_frequency(self, suggestion_db):
        """Repeated learning increments frequency."""
        suggestion_db.learn_word('ನಮಸ್ಕಾರ', 'kn')
        suggestion_db.learn_word('ನಮಸ್ಕಾರ', 'kn')
        suggestion_db.learn_word('ನಮಸ್ಕಾರ', 'kn')

        cursor = suggestion_db.conn.execute(
            "SELECT freq FROM user_dict WHERE word=? AND lang=?",
            ('ನಮಸ್ಕಾರ', 'kn')
        )
        freq = cursor.fetchone()[0]
        assert freq >= 3  # At least 3 from learning 3 times

    def test_learn_word_updates_last_used(self, suggestion_db):
        """Learning updates the last_used timestamp."""
        suggestion_db.learn_word('ಹೊಸ', 'kn')
        cursor = suggestion_db.conn.execute(
            "SELECT last_used FROM user_dict WHERE word=? AND lang=?",
            ('ಹೊಸ', 'kn')
        )
        ts = cursor.fetchone()[0]
        assert ts > 0
        assert abs(ts - time.time()) < 5  # within 5 seconds of now

    def test_learn_word_different_languages(self, suggestion_db):
        """Same word in different languages creates separate entries."""
        suggestion_db.learn_word('test', 'kn')
        suggestion_db.learn_word('test', 'hi')

        cursor = suggestion_db.conn.execute(
            "SELECT lang FROM user_dict WHERE word=?", ('test',)
        )
        langs = {row[0] for row in cursor}
        assert 'kn' in langs
        assert 'hi' in langs

    def test_add_user_word(self, suggestion_db):
        """add_user_word inserts with specified frequency."""
        suggestion_db.add_user_word('ಕನ್ನಡ', 'kn', freq=500)
        cursor = suggestion_db.conn.execute(
            "SELECT freq FROM user_dict WHERE word=? AND lang=?",
            ('ಕನ್ನಡ', 'kn')
        )
        assert cursor.fetchone()[0] == 500


# ============================================================
# Suggest (Prefix Matching)
# ============================================================

class TestSuggest:
    """Test word suggestion / prefix matching."""

    def test_suggest_basic_prefix(self, suggestion_db):
        """Learned words are suggested by prefix."""
        suggestion_db.learn_word('ನಮಸ್ಕಾರ', 'kn')
        suggestion_db.learn_word('ನಮಸ್ತೆ', 'kn')
        results = suggestion_db.suggest('ನಮ', 'kn', limit=5)
        words = [w for w, _ in results]
        assert 'ನಮಸ್ಕಾರ' in words
        assert 'ನಮಸ್ತೆ' in words

    def test_suggest_respects_limit(self, suggestion_db):
        """Suggestions respect the limit parameter."""
        for i in range(10):
            suggestion_db.learn_word(f'word{i:03d}', 'en')
        results = suggestion_db.suggest('wor', 'en', limit=3)
        assert len(results) <= 3

    def test_suggest_lang_filter(self, suggestion_db):
        """Suggestions are filtered by language."""
        suggestion_db.learn_word('ನಮಸ್ಕಾರ', 'kn')
        suggestion_db.learn_word('नमस्ते', 'hi')

        kn_results = suggestion_db.suggest('ನಮ', 'kn')
        hi_results = suggestion_db.suggest('नम', 'hi')

        kn_words = [w for w, _ in kn_results]
        hi_words = [w for w, _ in hi_results]

        assert 'ನಮಸ್ಕಾರ' in kn_words
        assert 'नमस्ते' not in kn_words
        assert 'नमस्ते' in hi_words

    def test_suggest_sorted_by_frequency(self, suggestion_db):
        """Higher frequency words should appear first."""
        suggestion_db.add_user_word('ಕನ್ನಡ', 'kn', freq=100)
        suggestion_db.add_user_word('ಕನ್ನಡಿಗ', 'kn', freq=500)
        suggestion_db.add_user_word('ಕನ್ನ', 'kn', freq=50)

        results = suggestion_db.suggest('ಕನ', 'kn', limit=5)
        words = [w for w, _ in results]
        # ಕನ್ನಡಿಗ (freq 500) should come before ಕನ್ನಡ (freq 100)
        if 'ಕನ್ನಡಿಗ' in words and 'ಕನ್ನಡ' in words:
            assert words.index('ಕನ್ನಡಿಗ') < words.index('ಕನ್ನಡ')

    def test_suggest_no_match(self, suggestion_db):
        """No results when prefix doesn't match anything."""
        suggestion_db.learn_word('ಕನ್ನಡ', 'kn')
        results = suggestion_db.suggest('ತೆ', 'kn')
        assert len(results) == 0

    def test_suggest_exact_match(self, suggestion_db):
        """Exact match should still return the word."""
        suggestion_db.learn_word('ಹಲೋ', 'kn')
        results = suggestion_db.suggest('ಹಲೋ', 'kn')
        words = [w for w, _ in results]
        assert 'ಹಲೋ' in words


# ============================================================
# User Dictionary Priority
# ============================================================

class TestUserDictPriority:
    """Test that user dictionary has higher priority than base."""

    def test_user_words_come_first(self, suggestion_db):
        """User dict entries should appear before base dict for same prefix."""
        # Add base dict entry directly
        suggestion_db.conn.execute(
            "INSERT INTO base_dict (word, lang, freq) VALUES (?, ?, ?)",
            ('ಪದ_base', 'kn', 1000)
        )
        suggestion_db.conn.commit()

        # Add user dict entry
        suggestion_db.add_user_word('ಪದ_user', 'kn', freq=1)

        results = suggestion_db.suggest('ಪದ', 'kn', limit=5)
        sources = [source for _, source in results]
        words = [w for w, _ in results]

        # User entry should be present
        assert 'ಪದ_user' in words
        assert 'ಪದ_base' in words

        # User source should come before base source
        user_idx = words.index('ಪದ_user')
        base_idx = words.index('ಪದ_base')
        assert user_idx < base_idx

    def test_user_words_source_tag(self, suggestion_db):
        """User dict entries tagged with 'user' source."""
        suggestion_db.learn_word('ಟೆಸ್ಟ್', 'kn')
        results = suggestion_db.suggest('ಟೆ', 'kn')
        assert any(source == 'user' for _, source in results)

    def test_base_words_source_tag(self, suggestion_db):
        """Base dict entries tagged with 'base' source."""
        suggestion_db.conn.execute(
            "INSERT INTO base_dict (word, lang, freq) VALUES (?, ?, ?)",
            ('ಟೆಸ್ಟ್_base', 'kn', 128)
        )
        suggestion_db.conn.commit()
        results = suggestion_db.suggest('ಟೆ', 'kn')
        assert any(source == 'base' for _, source in results)


# ============================================================
# Min Prefix Filtering
# ============================================================

class TestMinPrefix:
    """Test min_prefix filtering behavior."""

    def test_prefix_too_short_returns_empty(self, suggestion_db_default_prefix):
        """Prefix shorter than min_prefix returns no results (default min_prefix=3)."""
        engine = suggestion_db_default_prefix
        engine.learn_word('ನಮಸ್ಕಾರ', 'kn')

        # Prefix of length 1 (single Unicode char)
        results = engine.suggest('ನ', 'kn')
        assert results == []

        # Prefix of length 2
        results = engine.suggest('ನಮ', 'kn')
        assert results == []

    def test_prefix_at_min_returns_results(self, suggestion_db_default_prefix):
        """Prefix at exactly min_prefix should return results."""
        engine = suggestion_db_default_prefix
        engine.learn_word('ನಮಸ್ಕಾರ', 'kn')

        results = engine.suggest('ನಮಸ', 'kn')
        assert len(results) > 0

    def test_custom_min_prefix(self, tmp_path):
        """Custom min_prefix value is respected."""
        db_path = str(tmp_path / 'min_prefix_test.db')
        engine = SuggestionEngine(db_path=db_path, min_prefix=1)
        engine.learn_word('abc', 'en')

        results = engine.suggest('a', 'en')
        assert len(results) > 0
        engine.close()


# ============================================================
# Empty Results
# ============================================================

class TestEmptyResults:
    """Test edge cases that should return empty results."""

    def test_empty_prefix(self, suggestion_db):
        results = suggestion_db.suggest('', 'kn')
        assert results == []

    def test_wrong_language(self, suggestion_db):
        suggestion_db.learn_word('test', 'kn')
        results = suggestion_db.suggest('tes', 'hi')
        assert results == []

    def test_empty_database(self, suggestion_db):
        results = suggestion_db.suggest('any', 'kn')
        assert results == []


# ============================================================
# Stats
# ============================================================

class TestStats:
    """Test statistics reporting."""

    def test_stats_structure(self, suggestion_db):
        """Stats returns dict with base and user keys."""
        stats = suggestion_db.get_stats()
        assert 'base' in stats
        assert 'user' in stats
        assert isinstance(stats['base'], dict)
        assert isinstance(stats['user'], dict)

    def test_stats_counts(self, suggestion_db):
        """Stats reflect actual word counts."""
        suggestion_db.learn_word('word1', 'kn')
        suggestion_db.learn_word('word2', 'kn')
        suggestion_db.learn_word('word3', 'hi')

        stats = suggestion_db.get_stats()
        assert stats['user'].get('kn', 0) == 2
        assert stats['user'].get('hi', 0) == 1

    def test_stats_base_empty_initially(self, suggestion_db):
        """Base dict stats empty when no wordlists loaded."""
        stats = suggestion_db.get_stats()
        assert len(stats['base']) == 0

    def test_stats_base_after_insert(self, suggestion_db):
        """Base dict stats reflect inserted entries."""
        suggestion_db.conn.execute(
            "INSERT INTO base_dict (word, lang, freq) VALUES (?, ?, ?)",
            ('test', 'kn', 128)
        )
        suggestion_db.conn.commit()
        stats = suggestion_db.get_stats()
        assert stats['base'].get('kn', 0) == 1


# ============================================================
# is_loaded
# ============================================================

class TestIsLoaded:
    """Test is_loaded method."""

    def test_not_loaded_initially(self, suggestion_db):
        assert not suggestion_db.is_loaded('kn')

    def test_loaded_after_insert(self, suggestion_db):
        suggestion_db.conn.execute(
            "INSERT INTO base_dict (word, lang, freq) VALUES (?, ?, ?)",
            ('ಟೆಸ್ಟ್', 'kn', 128)
        )
        suggestion_db.conn.commit()
        assert suggestion_db.is_loaded('kn')


# ============================================================
# LANG_CODES
# ============================================================

class TestLangCodes:
    """Test language code mapping."""

    def test_primary_languages(self):
        assert LANG_CODES['kannada'] == 'kn'
        assert LANG_CODES['hindi'] == 'hi'
        assert LANG_CODES['telugu'] == 'te'
        assert LANG_CODES['tamil'] == 'ta'

    def test_all_codes_are_two_letter(self):
        for lang, code in LANG_CODES.items():
            assert len(code) == 2, f"Lang code for {lang} is not 2-letter: {code}"
