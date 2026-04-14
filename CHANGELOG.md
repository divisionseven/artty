# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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