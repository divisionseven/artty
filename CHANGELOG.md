# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Release automation: tag-based trigger, Windows binary builds, automatic GitHub Release creation

### Changed

- Replace README image paths with absolute GitHub URLs

## [0.1.2] - 2026-04-14

### Added

- Shell completions for bash, zsh, and fish (`completions/`)
- FAQ documentation (`docs/faq.md`)
- Man page (`man/artty.1`)
- Documentation links to `--help` output
- Code of Conduct added to repository
- Security policy added to repository

### Fixed

- Windows ANSI detection tests now correctly mock ctypes using `sys.modules` patching instead of `builtins.__import__` (fixes sys.modules caching issue that bypassed import mocking)
- CLI now shows help menu when run with no arguments instead of a missing argument error
- README demo tables — equal column widths using GitHub-compatible pixel sizing
- Hardcoded path in test_main.py — now uses dynamic path resolution
- SECURITY.md version table to reflect 0.1.x releases
- Various lint issues (unused imports, type annotations, duplicate tests)

### Changed

- Badge styles to black background, white logos, plastic style
- Dynamic version in `__init__.py` using `importlib.metadata`

### Removed

- Removed stale `test_version_flag` test that hardcoded version number and would fail on every version bump

## [0.1.1] - 2026-04-13

### Added

- Complete documentation folder (`docs/`) with usage guide, algorithm explanation, examples, and API reference with demo images
- Transparency testing assets (`tests/assets/transparency_test/`) for RGBA and indexed PNG with transparency
- CI/CD workflows for automated testing and PyPI publishing (`.github/workflows/`)
- New `--hide-paths` CLI flag to show only filename instead of full path in console output

### Changed

- README updated with comprehensive usage examples, installation instructions, and documentation links
- CONTRIBUTING.md and SECURITY.md added to repository

### Removed

- Old test asset files (`test_ascii_color_*.txt`, `test_output.txt`) — replaced by programmatic tests

### Fixed

- Transparent pixels in RGBA images now correctly treated as background instead of rendered as dim green

## [0.1.0] - 2026-04-10

### Added

- Package rebuilt as proper Python package with `src/artty` layout
- New Click-based CLI with robust argument handling
- Core converter using Unicode braille patterns (U+2800–U+28FF)
- 24-bit ANSI color support with lit-pixel sampling
- Configuration dataclasses for programmatic use
- Unicode braille output (2×4 pixel cells)
- Optional 24-bit ANSI color text
- Adjustable width, threshold, contrast, sharpness
- Content-aware cropping with padding control
- Background color support
- Terminal preview with auto-detection
- Python API for programmatic use
