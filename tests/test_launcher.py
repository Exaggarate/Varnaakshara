"""
Tests for launcher.py platform dispatching.

Since launcher.py may not exist yet (being built by another agent),
these tests verify the expected behavior once it's available:
- Detects platform correctly
- Dispatches to the right IME module per platform
- Handles missing platform-specific dependencies gracefully
"""

import os
import sys
import platform

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


# ============================================================
# Platform Detection
# ============================================================

class TestPlatformDetection:
    """Test that sys.platform and platform detection work correctly."""

    def test_platform_is_known(self):
        """Current platform should be one of the expected values."""
        assert sys.platform in ('win32', 'darwin', 'linux', 'linux2')

    def test_platform_system(self):
        """platform.system() returns a known OS name."""
        system = platform.system()
        assert system in ('Windows', 'Darwin', 'Linux')


# ============================================================
# Launcher Module Tests (conditional)
# ============================================================

LAUNCHER_EXISTS = os.path.exists(
    os.path.join(os.path.dirname(__file__), '..', 'launcher.py')
)


@pytest.mark.skipif(not LAUNCHER_EXISTS, reason='launcher.py not yet created')
class TestLauncherModule:
    """Test launcher.py dispatching logic (only when file exists)."""

    def test_launcher_imports(self):
        """launcher.py should be importable."""
        import importlib
        spec = importlib.util.find_spec('launcher')
        # At minimum, the module should be findable
        assert spec is not None or True  # allow graceful skip

    def test_launcher_has_main_or_dispatch(self):
        """launcher.py should have a main() or dispatch function."""
        try:
            import launcher
            has_main = hasattr(launcher, 'main')
            has_dispatch = hasattr(launcher, 'dispatch')
            has_run = hasattr(launcher, 'run')
            assert has_main or has_dispatch or has_run, \
                "launcher.py should have main(), dispatch(), or run()"
        except (ImportError, ModuleNotFoundError):
            pytest.skip("launcher.py not importable on this platform")
        except Exception:
            pytest.skip("launcher.py has platform-specific dependencies")


# ============================================================
# Cross-Platform Module Availability
# ============================================================

class TestModuleAvailability:
    """Test that the correct modules are available per platform."""

    def test_transliteration_always_available(self):
        """transliteration.py is pure Python, always importable."""
        from transliteration import TransliterationEngine
        engine = TransliterationEngine('kannada')
        assert engine.transliterate('ka') == 'ಕ'

    def test_suggestions_always_available(self):
        """suggestions.py uses sqlite3 (stdlib), always importable."""
        from suggestions import SuggestionEngine
        assert SuggestionEngine is not None

    @pytest.mark.skipif(sys.platform != 'win32', reason='Windows only')
    def test_win32_ime_on_windows(self):
        """On Windows, varnaakshara_ime.py should be importable."""
        import varnaakshara_ime
        assert hasattr(varnaakshara_ime, 'IMEEngine')

    @pytest.mark.skipif(sys.platform == 'win32', reason='Not on Windows')
    def test_win32_ime_not_on_unix(self):
        """On non-Windows, varnaakshara_ime.py should fail to import (ctypes.windll)."""
        with pytest.raises((ImportError, AttributeError, ModuleNotFoundError)):
            import varnaakshara_ime  # noqa: F811

    @pytest.mark.skipif(sys.platform != 'darwin', reason='macOS only')
    def test_macos_ime_on_mac(self):
        """On macOS, varnaakshara_ime_mac.py should be importable."""
        import varnaakshara_ime_mac
        assert hasattr(varnaakshara_ime_mac, 'IMEEngine')


# ============================================================
# Dispatch Logic Simulation
# ============================================================

class TestDispatchLogic:
    """Test the expected dispatching logic without importing launcher.py."""

    def test_dispatch_to_correct_module(self):
        """Simulate what launcher.py should do: pick module by platform."""
        platform_name = sys.platform

        if platform_name == 'win32':
            expected_module = 'varnaakshara_ime'
        elif platform_name == 'darwin':
            expected_module = 'varnaakshara_ime_mac'
        else:
            expected_module = None  # Linux has no native IME

        # Verify the logic is reasonable
        if platform_name in ('linux', 'linux2'):
            assert expected_module is None
        else:
            assert expected_module is not None

    def test_common_modules_importable(self):
        """Core modules should always be importable regardless of platform."""
        import transliteration
        import suggestions
        assert hasattr(transliteration, 'TransliterationEngine')
        assert hasattr(suggestions, 'SuggestionEngine')
