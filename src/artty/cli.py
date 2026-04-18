"""Click CLI wrapper for ArTTY.

This module provides the command-line interface for the artty tool.
It uses Click for argument parsing and provides colored terminal output with
progress feedback.

Functions
---------
main : click.Command
    The main CLI entry point, registered as the 'artty' console script.
resolve_output_path : Resolve output file path from CLI arguments.
info, success, warn, error, header, dim : Terminal output helpers.
"""

import os
import sys
import time
import types
from typing import Any

import click

from artty import __version__
from artty.ansi import _supports_ansi, get_help_logo
from artty.converter import image_to_braille

# ANSI escape codes for colored output
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_GREEN = "\033[32m"
ANSI_CYAN = "\033[36m"
ANSI_YELLOW = "\033[33m"
ANSI_RED = "\033[31m"


USE_ANSI = _supports_ansi()


def _c(text: str, *codes: str) -> str:
    """Wrap text in ANSI codes if the terminal supports them."""
    if not USE_ANSI:
        return text
    return "".join(codes) + text + ANSI_RESET


def info(msg: str) -> None:
    print(_c("  " + msg, ANSI_CYAN))


def success(msg: str) -> None:
    print(_c("  ✓ " + msg, ANSI_GREEN))


def warn(msg: str) -> None:
    print(_c("  ⚠ " + msg, ANSI_YELLOW))


def error(msg: str) -> None:
    print(_c("  ✗ " + msg, ANSI_RED), file=sys.stderr)


def header(msg: str) -> None:
    print(_c(msg, ANSI_BOLD))


def dim(msg: str) -> None:
    print(_c(msg, ANSI_DIM))


def _format_path(path: str, hide: bool) -> str:
    """Format a path for display.

    Args:
        path: Full file path to format.
        hide: If True, return only the filename; otherwise return full path.

    Returns:
        Formatted path string.
    """
    if hide:
        return os.path.basename(path)
    return path


def resolve_output_path(
    input_path: str, output: str | None, width: int, color: bool
) -> str | None:
    """
    Resolve the output file path based on input and CLI options.

    Args:
        input_path: Path to the input image.
        output: CLI-provided output path or None.
        width: Output width in characters.
        color: Whether color mode is enabled.

    Returns:
        Resolved output path, or None if --no-save was passed.

    Raises:
        ValueError: If the output path escapes the input directory (path traversal).
    """
    input_stem = os.path.splitext(os.path.basename(input_path))[0]
    mode_tag = "color" if color else "plain"
    auto_name = f"{input_stem}_ascii_{mode_tag}_w{width}.txt"

    if output is None:
        return os.path.join(os.path.dirname(os.path.abspath(input_path)), auto_name)

    expanded = os.path.expanduser(output)

    if os.path.isdir(expanded):
        return os.path.join(expanded, auto_name)

    # Treat it as a full file path; create parent dirs if needed
    parent = os.path.dirname(expanded)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # Security check: prevent path traversal attacks
    input_dir = os.path.dirname(os.path.abspath(input_path))

    # If output has no directory component (just a filename), place in input directory
    if not os.path.dirname(output):
        final_path = os.path.join(input_dir, output)
        return os.path.abspath(final_path)

    # Otherwise check the output directory
    output_dir = os.path.dirname(os.path.abspath(expanded))

    # Must be same directory or subdirectory
    if not output_dir.startswith(input_dir + os.sep) and output_dir != input_dir:
        raise ValueError(f"Output path must be in same directory as input: {input_dir}")

    return os.path.abspath(expanded)


# ---------------------------------------------------------------------------
# Custom Help Formatter (exact pattern from pkg-defender)
# ---------------------------------------------------------------------------


class GroupedHelpFormatter(click.HelpFormatter):
    """Custom formatter matching standard CLI help style.

    Displays usage, description, options, and examples in a clean format.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._colmargin = 2  # 2-space leading indent for options

    def write_options(self, rows: list[tuple[str, str] | tuple[str]]) -> None:
        """Write options with 2-space indentation."""
        # Prepend 2-space indentation to each term
        indented_rows: list[tuple[str, str] | tuple[str]] = []
        for row in rows:
            term = "  " + row[0]  # Add 2-space indent
            if len(row) > 1:
                indented_rows.append((term, row[1]))
            else:
                indented_rows.append((term,))

        # Calculate the maximum width of all terms to ensure proper alignment
        # This fixes alignment issues when long options like --threshold exceed default col_max=30
        max_term_width = 0
        for row in indented_rows:
            term_width = len(row[0])
            if term_width > max_term_width:
                max_term_width = term_width

        # Use standard write_dl with explicit col_max
        # Add col_spacing (default 2) to ensure spacing between columns
        self.write_dl(indented_rows, col_max=max_term_width)  # type: ignore[arg-type]

    def write_examples_indented(self, ctx: click.Context) -> None:
        """Write Examples section - heading no indent, content 2-space indent."""
        examples = [
            "artty logo.png",
            "artty logo.png -o ~/Desktop/logo.txt -w 120",
            "artty logo.png --no-color --width 80",
            "artty logo.png --bg 0 0 0 --boost 1.4",
        ]

        self.write_heading("Examples")

        # Write each example with 2-space indentation
        for ex in examples:
            self.write_text("  " + ex)

    def write_examples(self, ctx: click.Context) -> None:
        """Write Examples section at the END (after options)."""
        examples = [
            "artty logo.png",
            "artty logo.png -o ~/Desktop/logo.txt -w 120",
            "artty logo.png --no-color --width 80",
            "artty logo.png --bg 0 0 0 --boost 1.4",
        ]

        self.write_heading("  Examples")

        # Use write_options for proper 2-space indentation
        # Convert to list of single-element tuples for options-style output
        rows: list[tuple[str, str] | tuple[str]] = [(ex,) for ex in examples]
        self.write_options(rows)


# Store reference to original format_help
_original_format_help = click.Command.format_help


def _custom_format_help(
    self: click.Command, ctx: click.Context, formatter: click.HelpFormatter
) -> None:
    """Custom format_help that adds Examples section using GroupedHelpFormatter."""
    # Use the formatter passed in if it's already GroupedHelpFormatter, otherwise wrap it
    if not isinstance(formatter, GroupedHelpFormatter):
        # Try to get terminal width with error handling
        try:
            term_width = os.get_terminal_size().columns or None
        except OSError:
            term_width = None

        # Get Click's formatter width (may be 78 default or actual terminal width)
        width = getattr(formatter, "width", None)

        # If terminal detected, use it; otherwise use 100 (wider than Click's 78 default)
        if term_width is not None:
            width = term_width
        elif width is None or width == 0 or width == 78:
            # Click defaults to 78 when it can't detect terminal - use wider 100
            width = 100
        custom_formatter = GroupedHelpFormatter(width=width)

        # Write blank line at top for breathing room
        custom_formatter.write_text("")

        # Add ASCII logo at top of help output
        # Use sys.stdout.write() directly to bypass Click's formatter wrapping
        # which would distort the 100-character logo
        logo = get_help_logo()
        if logo:
            sys.stdout.write("\n" + logo)
            sys.stdout.flush()
            custom_formatter.write_text("")

        # Write usage (no extra indentation - matches pkg-defender format)
        usage_output = self.get_usage(ctx)
        custom_formatter.write_text(usage_output)
        custom_formatter.write_text("")

        # Write description (hardcoded to match exact format like pkg-defender)
        # NO leading indent - matches pkg-defender format
        custom_formatter.write_text(
            "artty — Convert images to detailed braille ASCII art."
        )
        custom_formatter.write_text("")
        custom_formatter.write_text(
            "A CLI tool that converts images to detailed braille ASCII art with"
        )
        custom_formatter.write_text("accurate color embedding or plain text output.")
        custom_formatter.write_text("")
        custom_formatter.write_text("Features:")
        custom_formatter.write_text("  - Unicode braille characters")
        custom_formatter.write_text("  - 24-bit ANSI color support")
        custom_formatter.write_text("  - Cross-platform (macOS, Windows, Linux)")
        custom_formatter.write_text("  - Configurable output options")
        custom_formatter.write_text("")

        # Get options properly using get_params and get_help_record
        option_rows: list[tuple[str, str] | tuple[str]] = []
        for param in self.get_params(ctx):
            help_record = param.get_help_record(ctx)
            if help_record is not None:
                option_rows.append(help_record)

        if option_rows:
            custom_formatter.write_heading("Options")

            # Write options directly - let write_dl handle wrapping naturally
            custom_formatter.write_options(option_rows)
            custom_formatter.write_text("")

        # Write Examples section
        custom_formatter.write_examples_indented(ctx)

        # Write epilog if present
        if self.epilog:
            custom_formatter.write_text("")
            click.Command.format_epilog(self, ctx, custom_formatter)

        # Write the output to stdout
        output = "\n" + custom_formatter.getvalue()
        # Force color output even when piped
        click.echo(output, color=True)


# Apply the custom formatter by patching the format_help method on the main command
# This will be applied after the main function is defined


@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog="Full documentation: https://github.com/divisionseven/artty#readme\nReport bugs: https://github.com/divisionseven/artty/issues",
)
@click.argument("input", type=click.Path(exists=True), required=True)
@click.option(
    "-o",
    "--output",
    type=click.STRING,
    default=None,
    help=(
        "Where to save the .txt file. Accepts a full file path or a directory. "
        "If a directory is given, the filename is derived from the input image name. "
        "Defaults to the same directory as the input image."
    ),
)
@click.option(
    "--preview/--no-preview",
    default=True,
    help="Print the result to the terminal after saving (default: on).",
)
@click.option(
    "--no-save",
    is_flag=True,
    default=False,
    help="Do not write a .txt file — only print to stdout.",
)
@click.option(
    "-w",
    "--width",
    type=click.IntRange(min=10, max=500),
    default=100,
    help="Output width in braille characters. Height is auto-calculated. (default: 100)",
)
@click.option(
    "-t",
    "--threshold",
    type=click.IntRange(min=0, max=255),
    default=50,
    help=(
        "Luminance threshold (0-255). Pixels brighter than this become braille dots. "
        "Lower = denser, higher = sparser. (default: 50)"
    ),
)
@click.option(
    "--padding",
    type=int,
    default=30,
    help="Pixels of padding around auto-detected content. (default: 30)",
)
@click.option(
    "--contrast",
    type=float,
    default=1.0,
    help="Contrast enhancement factor. 1.0 = unchanged. (default: 1.0)",
)
@click.option(
    "--sharpness",
    type=float,
    default=1.0,
    help="Sharpness enhancement factor. 1.0 = unchanged. (default: 1.0)",
)
@click.option(
    "--color/--no-color",
    default=True,
    help="Enable/disable 24-bit ANSI color output. (default: on)",
)
@click.option(
    "--boost",
    "color_boost",
    type=float,
    default=1.2,
    help="Color brightness multiplier. 1.0-1.4 typical. (default: 1.2)",
)
@click.option(
    "--bg",
    nargs=3,
    type=click.IntRange(min=0, max=255),
    default=None,
    metavar="R G B",
    help="Solid ANSI background color as three integers (0-255).",
)
@click.option(
    "--hide-paths",
    is_flag=True,
    default=False,
    help="Show only filenames in output (hide full paths).",
)
@click.pass_context
@click.version_option(version=__version__, prog_name="artty")
def main(
    ctx: click.Context,
    input: str,
    output: str | None,
    preview: bool,
    no_save: bool,
    width: int,
    threshold: int,
    padding: int,
    contrast: float,
    sharpness: float,
    color: bool,
    color_boost: float,
    bg: tuple[int, int, int] | None,
    hide_paths: bool,
) -> None:
    """artty — Convert images to detailed braille ASCII art.

    A CLI tool that converts images to detailed braille ASCII art with
    accurate color embedding or plain text output.

    Features:
      - Unicode braille characters
      - 24-bit ANSI color support
      - Cross-platform (macOS, Windows, Linux)
      - Configurable output options
    """
    # Validate positive values
    if contrast <= 0:
        error("--contrast must be a positive number.")
        sys.exit(1)
    if sharpness <= 0:
        error("--sharpness must be a positive number.")
        sys.exit(1)
    if color_boost <= 0:
        error("--boost must be a positive number.")
        sys.exit(1)
    if padding < 0:
        error("--padding cannot be negative.")
        sys.exit(1)

    bg_color: tuple[int, int, int] | None = None
    if bg:
        bg_color = (int(bg[0]), int(bg[1]), int(bg[2]))
    output_path = resolve_output_path(
        input, output if not no_save else None, width, color
    )

    # Print run summary
    print()
    header("  artty  ─────────────────────────────────────")
    print()
    info(f"Input    : {_format_path(os.path.abspath(input), hide_paths)}")
    info(f"Mode     : {'color (24-bit ANSI)' if color else 'plain text'}")
    info(f"Width    : {width} chars")
    info(f"Threshold: {threshold}")
    if contrast != 1.0:
        info(f"Contrast : {contrast}")
    if sharpness != 1.0:
        info(f"Sharpness: {sharpness}")
    if color:
        info(f"Boost    : {color_boost}")
        if bg_color:
            info(f"BG color : rgb{bg_color}")
    if output_path:
        info(f"Output   : {_format_path(output_path, hide_paths)}")
    else:
        info("Output   : stdout only (--no-save)")
    print()

    # Convert
    start = time.time()

    try:
        result = image_to_braille(
            path=input,
            width=width,
            threshold=threshold,
            contrast=contrast,
            sharpness=sharpness,
            crop_padding=padding,
            color=color,
            bg_color=bg_color,
            color_boost=color_boost,
        )
    except FileNotFoundError as e:
        error(f"Could not open image: {e}")
        sys.exit(1)
    except ImportError as e:
        error(str(e))
        sys.exit(1)
    except Exception as e:
        error(f"Conversion failed: {e}")
        raise

    elapsed = time.time() - start
    line_count = result.count("\n") + 1

    success(f"Converted in {elapsed:.2f}s  ({line_count} lines)")

    # Save
    if output_path:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)
            success(f"Saved → {_format_path(output_path, hide_paths)}")
        except OSError as e:
            error(f"Could not write file: {e}")
            sys.exit(1)

    # Preview
    if preview:
        print()
        dim("  ─── Preview ───────────────────────────────────────")
        print()
        print(result)
        print()

    elif not output_path:
        # --no-save --no-preview: still write to stdout so the tool is pipeable
        print(result)


# Apply custom formatter - MUST come after main is defined
main.format_help = types.MethodType(_custom_format_help, main)  # type: ignore[method-assign]


if __name__ == "__main__":
    main()
