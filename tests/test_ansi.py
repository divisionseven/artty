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
            def GetStdHandle(self, handle):
                return 1

            def SetConsoleMode(self, handle, mode):
                return True

        class MockCtypes:
            windll = type("windll", (), {"kernel32": MockKernel()})()

        # We need to make ctypes import work with mock
        import builtins

        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "ctypes":
                return MockCtypes()
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        result = _supports_ansi()
        assert result is True

    def test_windows_with_ctypes_import_failure_returns_false(self, monkeypatch):
        """Test that Windows with ctypes import failure returns False."""
        monkeypatch.setattr(sys, "platform", "win32")

        # Mock ctypes import to raise an exception
        import builtins

        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "ctypes":
                raise ImportError("No module named 'ctypes'")
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        result = _supports_ansi()
        assert result is False

    def test_windows_with_SetConsoleMode_failure_returns_false(self, monkeypatch):
        """Test that Windows when SetConsoleMode fails returns False."""
        monkeypatch.setattr(sys, "platform", "win32")

        # Create mock ctypes where SetConsoleMode raises an exception
        class MockKernel:
            def GetStdHandle(self, handle):
                return 1

            def SetConsoleMode(self, handle, mode):
                raise Exception("Console mode not supported")

        class MockCtypes:
            windll = type("windll", (), {"kernel32": MockKernel()})()

        import builtins

        original_import = builtins.__import__

        def mock_import(name, *args, **kwargs):
            if name == "ctypes":
                return MockCtypes()
            return original_import(name, *args, **kwargs)

        monkeypatch.setattr(builtins, "__import__", mock_import)
        result = _supports_ansi()
        assert result is False
