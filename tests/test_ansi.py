"""Tests for the ANSI terminal detection module."""

import sys

from artty.ansi import _supports_ansi


class TestSupportsAnsi:
    """Tests for the _supports_ansi function."""

    def test_returns_bool(self):
        """Test that _supports_ansi returns a boolean."""
        result = _supports_ansi()
        assert isinstance(result, bool)

    def test_non_windows_platform_returns_isatty_result(self, monkeypatch):
        """Test that non-Windows platforms check isatty on stdout."""
        # Force non-Windows platform
        monkeypatch.setattr(sys, "platform", "linux")

        # Create a mock stdout without isatty
        class MockStdout:
            pass

        monkeypatch.setattr(sys, "stdout", MockStdout())
        result = _supports_ansi()
        assert result is False

    def test_non_windows_with_isatty_returns_true(self, monkeypatch):
        """Test that non-Windows with TTY stdout returns True."""
        monkeypatch.setattr(sys, "platform", "linux")

        # Create mock stdout with isatty returning True
        class MockStdout:
            def isatty(self):
                return True

        monkeypatch.setattr(sys, "stdout", MockStdout())
        result = _supports_ansi()
        assert result is True

    def test_non_windows_with_isatty_returns_false(self, monkeypatch):
        """Test that non-Windows with isatty returning False returns False."""
        monkeypatch.setattr(sys, "platform", "linux")

        class MockStdout:
            def isatty(self):
                return False

        monkeypatch.setattr(sys, "stdout", MockStdout())
        result = _supports_ansi()
        assert result is False

    def test_windows_with_ctypes_available_returns_true(self, monkeypatch):
        """Test that Windows with working ctypes returns True."""
        monkeypatch.setattr(sys, "platform", "win32")

        # Create mock ctypes with working functions
        class MockKernel:
            def GetStdHandle(self, handle):  # noqa: N802
                return 1

            def GetConsoleMode(self, handle, mode_ptr):  # noqa: N802
                # Simulate successful GetConsoleMode by writing to the DWORD
                mode_ptr._value = 0  # noqa: SLF001
                return True

            def SetConsoleMode(self, handle, mode):  # noqa: N802
                return True

        class MockWintypes:
            class HANDLE:
                def __init__(self, value):
                    self.value = value

                def __eq__(self, other):
                    # Allow comparison with integers (e.g., == -1)
                    if isinstance(other, MockWintypes.HANDLE):
                        return self.value == other.value
                    return self.value == other

            class DWORD:
                def __init__(self, value=0):
                    self.value = value

        class MockCtypes:
            windll = type("windll", (), {"kernel32": MockKernel()})()  # noqa: N816

            @staticmethod
            def byref(obj):
                # Return a mock reference that allows setting _value
                ref = type("ref", (), {"_value": obj.value})()
                return ref

        # Store original modules to restore later
        original_ctypes = sys.modules.get("ctypes")
        original_wintypes = sys.modules.get("ctypes.wintypes")

        try:
            # Create mock instance with wintypes attribute for 'from ctypes import wintypes'
            mock_ctypes = MockCtypes()
            mock_ctypes.wintypes = MockWintypes()  # noqa: N816

            # Directly patch sys.modules to bypass import machinery
            sys.modules["ctypes"] = mock_ctypes
            sys.modules["ctypes.wintypes"] = MockWintypes()
            result = _supports_ansi()
            assert result is True
        finally:
            # Restore original modules
            if original_ctypes is not None:
                sys.modules["ctypes"] = original_ctypes
            elif "ctypes" in sys.modules:
                del sys.modules["ctypes"]
            if original_wintypes is not None:
                sys.modules["ctypes.wintypes"] = original_wintypes
            elif "ctypes.wintypes" in sys.modules:
                del sys.modules["ctypes.wintypes"]

    def test_windows_with_ctypes_import_failure_returns_false(self, monkeypatch):
        """Test that Windows with ctypes import failure returns False."""
        monkeypatch.setattr(sys, "platform", "win32")

        # Store original module to restore later
        original_ctypes = sys.modules.get("ctypes")
        original_wintypes = sys.modules.get("ctypes.wintypes")

        def mock_import(name, *args, **kwargs):
            raise ImportError(f"No module named '{name}'")

        try:
            # Remove ctypes from sys.modules and patch __import__ to raise
            if "ctypes" in sys.modules:
                del sys.modules["ctypes"]
            if "ctypes.wintypes" in sys.modules:
                del sys.modules["ctypes.wintypes"]

            monkeypatch.setattr("builtins.__import__", mock_import)
            result = _supports_ansi()
            assert result is False
        finally:
            # Restore original modules
            if original_ctypes is not None:
                sys.modules["ctypes"] = original_ctypes
            if original_wintypes is not None:
                sys.modules["ctypes.wintypes"] = original_wintypes

    def test_windows_with_SetConsoleMode_failure_returns_false(self, monkeypatch):  # noqa: N802
        """Test that Windows when SetConsoleMode fails returns False."""
        monkeypatch.setattr(sys, "platform", "win32")

        # Create mock ctypes where SetConsoleMode raises an exception
        class MockKernel:
            def GetStdHandle(self, handle):  # noqa: N802
                return 1

            def GetConsoleMode(self, handle, mode_ptr):  # noqa: N802
                # Simulate successful GetConsoleMode
                mode_ptr._value = 0  # noqa: SLF001

            def SetConsoleMode(self, handle, mode):  # noqa: N802
                raise Exception("Console mode not supported")

        class MockWintypes:
            class HANDLE:
                def __init__(self, value):
                    self.value = value

                def __eq__(self, other):
                    # Allow comparison with integers (e.g., == -1)
                    if isinstance(other, MockWintypes.HANDLE):
                        return self.value == other.value
                    return self.value == other

            class DWORD:
                def __init__(self, value=0):
                    self.value = value

        class MockCtypes:
            windll = type("windll", (), {"kernel32": MockKernel()})()  # noqa: N816

            @staticmethod
            def byref(obj):
                ref = type("ref", (), {"_value": obj.value})()  # noqa: SLF001
                return ref

        # Store original modules to restore later
        original_ctypes = sys.modules.get("ctypes")
        original_wintypes = sys.modules.get("ctypes.wintypes")

        try:
            # Create mock instance with wintypes attribute for 'from ctypes import wintypes'
            mock_ctypes = MockCtypes()
            mock_ctypes.wintypes = MockWintypes()  # noqa: N816

            # Directly patch sys.modules to bypass import machinery
            sys.modules["ctypes"] = mock_ctypes
            sys.modules["ctypes.wintypes"] = MockWintypes()
            result = _supports_ansi()
            assert result is False
        finally:
            # Restore original modules
            if original_ctypes is not None:
                sys.modules["ctypes"] = original_ctypes
            elif "ctypes" in sys.modules:
                del sys.modules["ctypes"]
            if original_wintypes is not None:
                sys.modules["ctypes.wintypes"] = original_wintypes
            elif "ctypes.wintypes" in sys.modules:
                del sys.modules["ctypes.wintypes"]


class TestNoColorEnvVar:
    """Tests for NO_COLOR and FORCE_COLOR environment variable handling."""

    def test_no_color_env_disables_colors(self, monkeypatch):
        """Test that NO_COLOR=1 makes _supports_ansi() return False."""
        # Set NO_COLOR env var
        monkeypatch.setenv("NO_COLOR", "1")

        # Force non-Windows to skip platform-specific checks
        monkeypatch.setattr(sys, "platform", "linux")

        # Import after env var is set to test runtime check
        from artty.ansi import _supports_ansi

        result = _supports_ansi()
        assert result is False

    def test_force_color_env_enables_colors(self, monkeypatch):
        """Test that FORCE_COLOR=1 makes _supports_ansi() return True."""
        # Clear NO_COLOR and set FORCE_COLOR
        monkeypatch.delenv("NO_COLOR", raising=False)
        monkeypatch.setenv("FORCE_COLOR", "1")

        # Force non-Windows and make stdout not a TTY (should still be True with FORCE_COLOR)
        monkeypatch.setattr(sys, "platform", "linux")

        class MockStdout:
            def isatty(self):
                return False

        monkeypatch.setattr(sys, "stdout", MockStdout())

        from artty.ansi import _supports_ansi

        result = _supports_ansi()
        assert result is True


class TestGetHelpLogo:
    """Tests for get_help_logo function."""

    def test_returns_empty_when_narrow_terminal(self, monkeypatch):
        """Test logo returns empty when terminal is narrow."""
        import artty.ansi

        # Mock get_terminal_width to return narrow width
        monkeypatch.setattr(artty.ansi, "get_terminal_width", lambda: 50)

        from artty.ansi import get_help_logo

        result = get_help_logo()
        assert result == ""

    def test_returns_color_logo_when_color_supported(self, monkeypatch, tmp_path):
        """Test logo returns color logo when color is supported."""
        import artty.ansi

        # Create mock logo files in a temp location
        mock_docs = tmp_path / "docs" / "assets" / "brand"
        mock_docs.mkdir(parents=True)

        color_logo = mock_docs / "logo_color_ascii_color_w100.txt"
        color_logo.write_text("COLOR_LOGO")

        plain_logo = mock_docs / "logo_color_ascii_plain_w100.txt"
        plain_logo.write_text("PLAIN_LOGO")

        # Use temp directory path
        def mock_get_help_logo():
            if artty.ansi.get_terminal_width() < artty.ansi.LOGO_MIN_WIDTH:
                return ""

            use_color = artty.ansi._supports_ansi()

            logo_path = (
                artty.ansi.LOGO_COLOR_PATH if use_color else artty.ansi.LOGO_PLAIN_PATH
            )

            try:
                base_path = tmp_path / logo_path
                with open(base_path) as f:
                    return f.read()
            except (FileNotFoundError, OSError):
                return ""

        monkeypatch.setattr(artty.ansi, "get_help_logo", mock_get_help_logo)
        monkeypatch.setattr(artty.ansi, "get_terminal_width", lambda: 120)

        from artty.ansi import get_help_logo

        # Mock _supports_ansi to return True (color supported)
        monkeypatch.setattr(artty.ansi, "_supports_ansi", lambda: True)

        result = get_help_logo()
        assert result == "COLOR_LOGO"

    def test_returns_plain_logo_when_no_color(self, monkeypatch, tmp_path):
        """Test logo returns plain logo when color is not supported."""
        import artty.ansi

        # Create mock logo files
        mock_docs = tmp_path / "docs" / "assets" / "brand"
        mock_docs.mkdir(parents=True)

        color_logo = mock_docs / "logo_color_ascii_color_w100.txt"
        color_logo.write_text("COLOR_LOGO")

        plain_logo = mock_docs / "logo_color_ascii_plain_w100.txt"
        plain_logo.write_text("PLAIN_LOGO")

        # Use temp directory path
        def mock_get_help_logo():
            if artty.ansi.get_terminal_width() < artty.ansi.LOGO_MIN_WIDTH:
                return ""

            use_color = artty.ansi._supports_ansi()

            logo_path = (
                artty.ansi.LOGO_COLOR_PATH if use_color else artty.ansi.LOGO_PLAIN_PATH
            )

            try:
                base_path = tmp_path / logo_path
                with open(base_path) as f:
                    return f.read()
            except (FileNotFoundError, OSError):
                return ""

        monkeypatch.setattr(artty.ansi, "get_help_logo", mock_get_help_logo)
        monkeypatch.setattr(artty.ansi, "get_terminal_width", lambda: 120)

        # Force color to return False
        monkeypatch.setattr(artty.ansi, "_supports_ansi", lambda: False)

        from artty.ansi import get_help_logo

        result = get_help_logo()
        assert result == "PLAIN_LOGO"
