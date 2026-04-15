"""ANSI terminal detection utilities.

This module provides shared functions for detecting terminal support
for ANSI escape codes across the artty package.
"""

import sys


def _supports_ansi() -> bool:
    """
    Return True if the current terminal is likely to support ANSI codes.

    On Windows, this function attempts to enable virtual terminal processing
    (a side effect that persists for the lifetime of the process).
    On other platforms, it simply checks whether stdout is a TTY.

    Returns:
        bool: True if ANSI codes should work in the current terminal.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            kernel32 = ctypes.windll.kernel32

            # STD_OUTPUT_HANDLE = -11
            stdout_handle = kernel32.GetStdHandle(-11)
            if stdout_handle == wintypes.HANDLE(-1):  # INVALID_HANDLE_VALUE
                return False

            # Get current console mode
            mode = wintypes.DWORD()
            if not kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode)):
                return False

            # Enable virtual terminal processing while preserving existing flags
            enable_virtual_terminal_processing = 0x0004
            new_mode = mode.value | enable_virtual_terminal_processing

            if not kernel32.SetConsoleMode(stdout_handle, new_mode):
                return False

            return True

        except Exception:
            # Fall back gracefully on any ctypes / permission / old Windows issues
            return False
    else:
        return bool(hasattr(sys.stdout, "isatty") and sys.stdout.isatty())
