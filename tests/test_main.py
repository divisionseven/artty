"""Tests for the __main__ entry point module."""

import pathlib
import subprocess
import sys

from click.testing import CliRunner

from artty.cli import main


class TestMainEntryPoint:
    """Tests for the python -m artty entry point."""

    def test_main_module_can_be_imported(self):
        """Test that the __main__ module can be imported without errors."""
        # This imports the module to verify syntax and imports are correct
        from artty import __main__  # noqa: F401

    def test_main_function_is_callable(self):
        """Test that the main function from cli is callable."""
        # Verify main is the CLI main function
        assert callable(main)

    def test_main_invoked_directly_calls_cli(self):
        """Test that calling main via __main__ works as entry point."""
        # Test that main can be invoked with --help
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        # Should not crash - exit code 0 means --help worked
        assert result.exit_code == 0
        # Should contain expected CLI content
        assert "Usage:" in result.output

    def test_main_when_run_as_script(self):
        """Test that __main__ can be executed."""
        # This simulates: python -m artty
        # The __main__ module should call main() when __name__ == "__main__"
        # We verify the behavior by checking the module structure
        import artty.__main__ as main_module

        # Check that main is accessible through the module
        assert hasattr(main_module, "main")
        assert main_module.main is main

    def test_python_m_runs_successfully(self):
        """Test that python -m artty executes without errors."""
        # This runs the module as a script and covers the __main__ guard
        result = subprocess.run(
            [sys.executable, "-m", "artty", "--help"],
            capture_output=True,
            text=True,
            cwd=pathlib.Path(__file__).parent.parent,
        )
        # Should not crash
        assert result.returncode == 0
        # Should output help
        assert "Usage:" in result.stdout
