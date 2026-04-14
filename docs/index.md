# artty Documentation

<p align="center">
  <a href="https://pypi.org/project/artty/"><img src="https://img.shields.io/pypi/pyversions/artty?style=plastic&bg=black&logoColor=white" alt="Python Version"></a>
  <a href="https://github.com/divisionseven/artty/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/divisionseven/artty/ci.yml?style=plastic&bg=black&logoColor=white" alt="Build Status"></a>
  <a href="https://pypi.org/project/artty/"><img src="https://img.shields.io/pypi/v/artty?style=plastic&bg=black&logoColor=white" alt="PyPI Version"></a>
</p>

Welcome to the artty technical documentation. Here you'll find in-depth information about the conversion algorithm, complete API references, and practical usage examples.

---

## Documentation Sections

### [Algorithm](algorithm.md)

How Unicode Braille rendering works, the 8-step conversion pipeline, threshold-based pixel mapping, color extraction, and key technical decisions.

- Braille character encoding (2×4 pixel cells)
- Input validation and size limits
- Image pre-processing (contrast, sharpness)
- Luminance threshold mapping
- Color sampling from lit pixels
- Braille dot pattern generation
- ANSI color embedding

### [CLI & API Reference](reference.md)

Complete command-line options, Python API functions, parameters, return types, constants, and error handling.

- CLI flags and options (`-w`, `-t`, `--boost`, `--bg`, etc.)
- Python API (`image_to_braille` function)
- Configuration constants
- Error codes and exceptions

### [Examples](examples.md)

Practical usage examples from basic conversion to advanced techniques.

- Basic image conversion
- Threshold tuning
- Color boosting
- Batch processing
- Background color handling
- Output to file vs. terminal preview

---

## Quick Links

- [Homepage](../README.md)
- [GitHub Repository](https://github.com/divisionseven/artty)
- [PyPI Package](https://pypi.org/project/artty/)
- [Report Bugs](https://github.com/divisionseven/artty/issues)
- [Request Features](https://github.com/divisionseven/artty/discussions)

---

## Overview

| Feature | Description |
|---------|-------------|
| **Unicode Braille** | Uses U+2800–U+28FF for 8 dots per character (4× detail vs traditional ASCII) |
| **24-bit ANSI Color** | Embedded color codes sample only from lit pixels |
| **Cross-Platform** | Works on macOS, Linux, and Windows with VT support |
| **Configurable** | Width, threshold, contrast, sharpness, padding, color boost |

---

> Last updated: 2026-04-11