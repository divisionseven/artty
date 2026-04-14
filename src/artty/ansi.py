"""ANSI terminal detection utilities.

This module provides shared functions for detecting terminal support
for ANSI escape codes across the artty package.
"""

import sys


def _supports_ansi() -> bool:
    """
    Return True if the current terminal is likely to support ANSI codes.

    On Windows, attempts to enable virtual terminal processing.
    On other platforms, checks if stdout is a TTY.

    Returns:
        bool: True if ANSI codes should work in the current terminal.
    """
    if sys.platform == "win32":
        try:
            import ctypes

            kernel = ctypes.windll.kernel32  # type: ignore[attr-defined]
            # Enable VIRTUAL_TERMINAL_PROCESSING on Windows 10+
            kernel.SetConsoleMode(kernel.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
