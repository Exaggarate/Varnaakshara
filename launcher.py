"""
Varnaakshara Launcher
==================
Cross-platform launcher that auto-detects the OS and launches
the appropriate IME module.

Usage:
    python launcher.py
    python -m launcher
"""

import sys
import os
import platform
import traceback


def _get_version():
    """Best-effort version string."""
    # Prefer a single source of truth if present.
    try:
        from core import __version__  # type: ignore
        return __version__
    except Exception:
        pass
    # Fallback: env or unknown
    return os.environ.get('VARNAAKSHARA_VERSION', 'dev')


def main():
    version = _get_version()
    os_name = platform.system()
    print(f"Varnaakshara IME launcher — v{version}")
    print(f"Platform: {os_name} ({platform.machine()}) Python {platform.python_version()}")

    try:
        if os_name == 'Windows':
            from ime.ime_windows import WindowsIME, check_single_instance
            if not check_single_instance():
                raise RuntimeError('Another instance of Varnaakshara is already running.')
            ime = WindowsIME()
            ime.start()
            ime.run_event_loop()

        elif os_name == 'Darwin':
            from ime.ime_macos import (
                MacOSIME, check_single_instance,
                check_accessibility, show_accessibility_dialog,
            )
            if not check_single_instance():
                raise RuntimeError('Another instance of Varnaakshara is already running.')
            if not check_accessibility():
                show_accessibility_dialog()
                raise RuntimeError('Accessibility permission not granted.')
            ime = MacOSIME()
            ime.start()
            ime.run_event_loop()

        else:
            raise RuntimeError(
                f"Unsupported OS: {os_name}. Varnaakshara currently supports Windows and macOS."
            )

    except Exception as e:
        # Prefer GUI dialog if PyQt5 is available; else print.
        msg = (
            "Varnaakshara failed to start.\n\n"
            f"Error: {e}\n\n"
            "If this is the first run on macOS, ensure Accessibility permissions are enabled."
        )
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(None, 'Varnaakshara — Startup Error', msg)
        except Exception:
            print(msg)
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
