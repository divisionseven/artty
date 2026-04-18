"""ANSI terminal detection utilities.

This module provides shared functions for detecting terminal support
for ANSI escape codes across the artty package.
"""

import os
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
    # Explicit env var overrides (per https://no-color.org and https://force-color.org)
    # Check at runtime so env vars set after import are respected
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True

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


def get_terminal_width() -> int:
    """Get terminal width columns, with safe fallback for non-TTY environments.

    Called at help render time, not import time, to respect runtime env vars.
    """
    import shutil

    try:
        return shutil.get_terminal_size().columns
    except (OSError, AttributeError):
        # Not a TTY or doesn't support get_terminal_size
        return 80


LOGO_MIN_WIDTH = 105
LOGO_COLOR_PATH = "docs/assets/brand/logo_color_ascii_color_w100.txt"
LOGO_PLAIN_PATH = "docs/assets/brand/logo_color_ascii_plain_w100.txt"


def get_help_logo() -> str:
    """Get ASCII logo for help output.

    - Returns empty string if terminal < 105 chars (won't fit)
    - Returns color logo if color supported via _supports_ansi()
    - Returns plain logo if color not supported
    """
    # Check terminal width
    if get_terminal_width() < LOGO_MIN_WIDTH:
        return ""

    # Check color support (called at RUNTIME, not import time)
    use_color = _supports_ansi()

    # Choose logo based on color support
    logo_path = LOGO_COLOR_PATH if use_color else LOGO_PLAIN_PATH

    # Load and return logo content
    try:
        # logo files are in the project root, same as artty package
        base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), logo_path
        )
        with open(base_path) as f:
            return f.read()
    except (FileNotFoundError, OSError):
        return ""
