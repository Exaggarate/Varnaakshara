"""
Varnaakshara IME package.

Provides the unified IME base class and platform-specific implementations.
Uses the new table-driven transliteration engine from core.engine.

Usage:
    from ime.ime_base import VarnaaksharaIMEBase
    from ime.ime_windows import WindowsIME
    from ime.ime_macos import MacOSIME
"""

from .ime_base import VarnaaksharaIMEBase

__all__ = ['VarnaaksharaIMEBase']

# Platform-specific imports — fail gracefully on wrong OS
import sys as _sys

if _sys.platform == 'win32':
    try:
        from .ime_windows import WindowsIME
        __all__.append('WindowsIME')
    except (ImportError, OSError, AttributeError):
        pass

if _sys.platform == 'darwin':
    try:
        from .ime_macos import MacOSIME
        __all__.append('MacOSIME')
    except (ImportError, OSError, AttributeError):
        pass
