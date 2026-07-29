"""
Shared pytest fixtures for Varnaakshara test suite.
"""

import os
import sys
import tempfile

import pytest

# Ensure the project root is on sys.path so we can import modules directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Force offscreen Qt platform for headless CI (Linux without display)
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')


@pytest.fixture
def kannada_engine():
    """TransliterationEngine configured for Kannada."""
    from transliteration import TransliterationEngine
    return TransliterationEngine('kannada')


@pytest.fixture
def hindi_engine():
    """TransliterationEngine configured for Hindi."""
    from transliteration import TransliterationEngine
    return TransliterationEngine('hindi')


@pytest.fixture
def telugu_engine():
    """TransliterationEngine configured for Telugu."""
    from transliteration import TransliterationEngine
    return TransliterationEngine('telugu')


@pytest.fixture
def tamil_engine():
    """TransliterationEngine configured for Tamil."""
    from transliteration import TransliterationEngine
    return TransliterationEngine('tamil')


@pytest.fixture
def suggestion_db(tmp_path):
    """SuggestionEngine with a fresh temporary SQLite database."""
    from suggestions import SuggestionEngine
    db_path = str(tmp_path / 'test_dictionary.db')
    engine = SuggestionEngine(db_path=db_path, min_prefix=2)
    yield engine
    engine.close()


@pytest.fixture
def suggestion_db_default_prefix(tmp_path):
    """SuggestionEngine with default min_prefix=3."""
    from suggestions import SuggestionEngine
    db_path = str(tmp_path / 'test_dictionary_default.db')
    engine = SuggestionEngine(db_path=db_path)
    yield engine
    engine.close()
