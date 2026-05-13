<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://github.com/divisionseven/artty/raw/main/docs/assets/brand/logo_white.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://github.com/divisionseven/artty/raw/main/docs/assets/brand/logo_black.svg">
    <img src="https://github.com/divisionseven/artty/raw/main/docs/assets/brand/logo_color.png" alt="artty color logo" width="500">
  </picture>

# arTTY Documentation Index

### Welcome to the arTTY technical documentation. Here you'll find in-depth information about the conversion algorithm, complete API references, and practical usage examples.

</div>

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
- [Join Discussions](https://github.com/divisionseven/artty/discussions)

---

## Features Overview

| Feature                       | Description                                                                          |
| ----------------------------- | ------------------------------------------------------------------------------------ |
| ⚡️  **Unicode Braille Output** | Uses braille characters (U+2800–U+28FF) for efficient 2×4 pixel cell representation  |
| 🎨  **24-bit ANSI Color**      | Embedded color codes sample only from lit pixels, preventing dark edge contamination |
| 🖥️  **Cross-Platform**         | Works on macOS, Linux, and Windows with VT support                                   |
| 📐  **Preserves Contrast**     | Advanced threshold and sharpness controls maintain image definition                  |
| ⚙️  **Fully Configurable**     | Adjustable width, threshold, contrast, sharpness, and padding                        |
| 🔧  **Python Library**         | Import `image_to_braille` directly in your own code                                  |

---

> Last updated: 2026-05-12
