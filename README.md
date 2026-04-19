<div align="center">
  <a href="docs/assets/brand/logo_color.png">
    <img src="https://github.com/divisionseven/artty/raw/main/docs/assets/brand/logo_color.png" alt="artty color logo" width="550"/>
  </a>

# arTTY

### Convert any image into detailed, full-color ASCII art directly in your terminal

[![PyPI Version][pypi-badge-badge]][pypi-badge-link]
[![Python Versions][python-badge-badge]][python-badge-link]
[![License: MIT][license-badge-badge]][license-badge-link]
[![Codecov][codecov-badge-badge]][codecov-badge-link]
[![CI Build][ci-badge-badge]][ci-badge-link]

<p>
  <a href="docs/index.md">Documentation</a> &nbsp;·&nbsp; <a href="#-demo">Demo</a> &nbsp;·&nbsp; <a href="#-installation">Install</a> &nbsp;·&nbsp; <a href="https://github.com/divisionseven/artty/issues">Open an Issue</a> &nbsp;·&nbsp; <a href="https://github.com/divisionseven/artty/discussions">Join the Conversation</a>

</div>

## What is arTTY?

`artty` is a command-line tool and Python library that converts images to Unicode braille ASCII art with 24-bit ANSI color support. It preserves image contrast and sharpness while producing detailed, scanable output that works in any modern terminal on macOS, Linux, or Windows.

Whether you're building a terminal-based dashboard, creating visual presentations, or just having fun with ASCII art, `artty` gives you professional results with minimal configuration.

Bring some art to your TTY with arTTY.

## Features

| Feature                       | Description                                                                          |
|-------------------------------|--------------------------------------------------------------------------------------|
| ⚡  **Unicode Braille Output** | Uses braille characters (U+2800–U+28FF) for efficient 2×4 pixel cell representation  |
| 🎨  **24-bit ANSI Color**     | Embedded color codes sample only from lit pixels, preventing dark edge contamination |
| 🖥️  **Cross-Platform**        | Works on macOS, Linux, and Windows with VT support                                   |
| 📐  **Preserves Contrast**    | Advanced threshold and sharpness controls maintain image definition                  |
| ⚙️  **Fully Configurable**    | Adjustable width, threshold, contrast, sharpness, and padding                        |
| 🔧  **Python API**            | Import `image_to_braille` directly in your own code                                  |

---

## Installation

**Prerequisites:** Python 3.10+

### From PyPI

```bash
# Using uv (recommended)
uv pip install artty

# or using pip
pip install artty
```

### From Source

```bash
git clone https://github.com/divisionseven/artty.git
cd artty

# Using uv (recommended)
uv sync
uv run artty --version

# Or using pip
pip install -e .
```

### Verify

```bash
artty --version
# Output: artty, version <version>
```
---

## Usage

### Basic Conversion

```bash
# Convert an image to braille ASCII art with default settings (default 100-character width)
artty input.png
```

### Specify Output Width (Characters)

```bash
# Convert an image to braille ASCII art with 80-character width (using defaults for all other settings)
artty input.png -w 80
```

### Plain Text Output (No ANSI Color Embedding)

```bash
# Convert an image to plain text using default settings (no ANSI color codes embedded)
artty input.png --no-color
```

### Full Example

```bash
# Convert with custom width, black background, contrast boost, and save to file with custom name/path
artty photo.jpg -w 120 --bg 0 0 0 --boost 1.4 -o output.txt
```
**Expected output:** A detailed braille ASCII representation of your image, preview displayed in your terminal and saved to `output.txt`.

### Commands List

```bash
# Show help screen
artty -h
artty --help
```

<div align="center">
  <a href="docs/assets/demo_images/outputs/screenshots/artty_demo_help_v2.png">
    <img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/artty_demo_help_v2.png" alt="artty help screen" width="100%"/>
  </a>
</div>

#### `artty --help` Output

```bash
Usage: artty [OPTIONS] INPUT

artty — Convert images to detailed braille ASCII art.

A CLI tool that converts images to detailed braille ASCII art with
accurate color embedding or plain text output.

Features:
  - Unicode braille characters
  - 24-bit ANSI color support
  - Cross-platform (macOS, Windows, Linux)
  - Configurable output options

Options:
  -o, --output TEXT              Where to save the .txt file. Accepts a full file path or a directory. If a directory is
                                 given, the filename is derived from the input image name. Defaults to the same directory as
                                 the input image.
  --preview / --no-preview       Print the result to the terminal after saving (default: on).
  --no-save                      Do not write a .txt file — only print to stdout.
  -w, --width INTEGER RANGE      Output width in braille characters. Height is auto-calculated. (default: 100)  [10<=x<=500]
  -t, --threshold INTEGER RANGE  Luminance threshold (0-255). Pixels brighter than this become braille dots. Lower = denser,
                                 higher = sparser. (default: 50)  [0<=x<=255]
  --padding INTEGER              Pixels of padding around auto-detected content. (default: 30)
  --contrast FLOAT               Contrast enhancement factor. 1.0 = unchanged. (default: 1.0)
  --sharpness FLOAT              Sharpness enhancement factor. 1.0 = unchanged. (default: 1.0)
  --color / --no-color           Enable/disable 24-bit ANSI color output. (default: on)
  --boost FLOAT                  Color brightness multiplier. 1.0-1.4 typical. (default: 1.2)
  --bg R G B                     Solid ANSI background color as three integers (0-255).  [0<=x<=255]
  --hide-paths                   Show only filenames in output (hide full paths).
  --version                      Show the version and exit.
  -h, --help                     Show this message and exit.

Examples:
  artty logo.png
  artty logo.png -o ~/Desktop/logo.txt -w 120
  artty logo.png --no-color --width 80
  artty logo.png --bg 0 0 0 --boost 1.4
```

---

## Demo Images

> [!Note]
> All demo screenshots were captured using the [Ghostty][ghostty-link] Terminal, which supports full TrueColor (24-bit) color output. Other terminal emulators that support TrueColor include [iTerm2][iterm2-link], [Kitty][kitty-link], [Alacritty][alacritty-link], and [WezTerm][wezterm-link], and various others. arTTY has currently been tested with both the [Ghostty][ghostty-link] and the [Visual Studio Code][vscode-link] integrated terminal.
>
> If you use arTTY with another terminal emulator, please [open an issue][issues-link] to report its performance.

### Full-Color JPEG Conversions

#### NASA 2026 Artemis II Crew Photo

```bash
# Convert a JPEG image to braille art using default settings
# with input/output paths hidden from the output message
artty nasa.jpeg --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/nasa.jpeg"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/nasa.jpeg" alt="nasa" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/nasa_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/nasa_color_demo.png" alt="nasa output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://www.nasa.gov" target="_blank">NASA</a> | Brand logos shown for demonstration purposes only. All trademarks are property of their respective owners.</sub></p>

#### Large Color JPEG Photograph

```bash
# Convert a JPEG image to 150-character width braille art
# with input/output paths hidden from the output message
artty JB1.jpeg -w 150 --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/JB1.jpeg"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/JB1.jpeg" alt="JB1" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/jb1_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/jb1_color_demo.png" alt="JB1 output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: © Division 7 | All trademarks are property of their respective owners.</sub></p>

#### Large Color JEPG Photograph

```bash
# Convert a JPEG image to 175-character width braille art
# with input/output paths hidden from the output message
artty JB3.jpeg -w 175 --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/JB3.jpeg"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/JB3.jpeg" alt="JB3" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/jb3_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/jb3_color_demo.png" alt="JB3 output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: © Division 7 | All trademarks are property of their respective owners.</sub></p>

### PNG Logos (with transparency)

#### arTTY Logo

```bash
# Convert the arTTY logo to 200-character width ASCII art
# with input/output paths hidden from the output message
artty logo.png -w 200 --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/logo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/logo.png" alt="logo" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/logo_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/logo_demo.png" alt="logo output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://github.com/divisionseven/artty" target="_blank">artty GitHub</a></sub></p>

#### Visual Studio Code Logo

```bash
# Convert the VS Code PNG image to braille art
# with input/output paths hidden from the output message
artty vscode.png --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/vscode.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/vscode.png" alt="vscode" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/vscode_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/vscode_color_demo.png" alt="vscode output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://code.visualstudio.com" target="_blank">Microsoft/VSCode</a> | Brand logos shown for demonstration purposes only. All trademarks are property of their respective owners.</sub></p>

#### Linux "Tux" Logo

```bash
# Convert the Linux logo to braille art
# with input/output paths hidden from the output message
artty linux.png --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/linux.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/linux.png" alt="linux" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/linux_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/linux_color_demo.png" alt="linux output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://www.linux.org" target="_blank">Linux</a> | Brand logos shown for demonstration purposes only. All trademarks are property of their respective owners.</sub></p>

#### GitHub White Logo

```bash
# Convert GitHub logo to 200-character width plain text (no color)
# with input/output paths hidden from the output message
artty github_full.png -w 200 --no-color --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Plain TXT Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/github_full.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/github_full.png" alt="github" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/github_full_plain_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/github_full_plain_demo.png" alt="github output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://github.com" target="_blank">GitHub</a> | Brand logos shown for demonstration purposes only. All trademarks are property of their respective owners.</sub></p>

#### PKG-Defender Repo PNG Logo

```bash
# Convert pkg-defender logo to 125-character width plain text
# with input/output paths hidden from the output message
artty pkg-defender.png -w 125 --no-color --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Plain TXT Output</th>
  </tr>
  <tr>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/pkg-defender.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/pkg-defender.png" alt="pkg-defender" width="100%"/></a></td>
    <td width="50%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/pkgd_plain_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/pkgd_plain_demo.png" alt="pkg-defender output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://github.com/divisionseven/pkg-defender" target="_blank">PKG-Defender GitHub</a> | "Supply-Chain Attack Defense CLI"</sub></p>

### Conversions With and Without Color Embedding

#### Arch Linux Logo

```bash
# Convert Arch Linux logo to color-embedded output (200-char width)
# with input/output paths hidden from the output message
artty arch.png -w 200 --hide-paths

# Convert Arch Linux logo to plain text output (200-char width)
# with input/output paths hidden from the output message
artty arch.png -w 200 --no-color --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Color-Embedded Output</th>
    <th align="center">arTTY Plain TXT Output</th>
  </tr>
  <tr>
    <td width="33%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/arch.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/arch.png" alt="arch" width="100%"/></a></td>
    <td width="33%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/arch_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/arch_color_demo.png" alt="arch color output" width="100%"/></a></td>
    <td width="33%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/arch_plain_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/arch_plain_demo.png" alt="arch plain output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://archlinux.org" target="_blank">Arch Linux</a> | Brand logos shown for demonstration purposes only. All trademarks are property of their respective owners.</sub></p>

#### Apple 1977-1998 Color Logo

```bash
# Convert Apple logo to color-embedded output (80-char width)
# with input/output paths hidden from the output message
artty apple.png -w 80 --hide-paths

# Convert Apple logo to plain text output (80-char width)
# with input/output paths hidden from the output message
artty apple.png -w 80 --no-color --hide-paths
```
<table width="100%">
  <tr>
    <th align="center">Input</th>
    <th align="center">arTTY Color-Embedded Output</th>
    <th align="center">arTTY Plain TXT Output</th>
  </tr>
  <tr>
    <td width="33%" align="center" valign="middle"><a href="docs/assets/demo_images/inputs/apple.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/inputs/apple.png" alt="apple" width="100%"/></a></td>
    <td width="33%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/apple_color_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/apple_color_demo.png" alt="apple color output" width="100%"/></a></td>
    <td width="33%" align="center" valign="middle"><a href="docs/assets/demo_images/outputs/screenshots/apple_plain_demo.png"><img src="https://github.com/divisionseven/artty/raw/main/docs/assets/demo_images/outputs/screenshots/apple_plain_demo.png" alt="apple plain output" width="100%"/></a></td>
  </tr>
</table>
<p align="center"><sub>Credit: <a href="https://www.apple.com" target="_blank">Apple</a> | Brand logos shown for demonstration purposes only. All trademarks are property of their respective owners.</sub></p>

---

## Technical Documentation

For detailed technical information, see the [Documentation Index][docs-index-link], which provides:

- [Algorithm][docs-algorithm-link] — How Unicode Braille rendering works
- [CLI & API Reference][docs-reference-link] — Complete command-line options and Python library examples
- [Examples][docs-examples-link] — Practical usage examples

---

## Configuration

| Category         | Option                       | Type    | Default                             | Description                                                                                                     |
|------------------|------------------------------|---------|-------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Input            | `input`                      | `path`  | (required)                          | Path to the input image file                                                                                    |
| Image Processing | `-w, --width`                | `int`   | `100`                               | Output width in braille characters (10-500)                                                                     |
| Image Processing | `-t, --threshold`            | `int`   | `50`                                | Luminance cutoff for braille dots (0-255)                                                                       |
| Image Processing | `--padding`                  | `int`   | `30`                                | Pixels of padding around auto-detected content                                                                  |
| Image Processing | `--contrast`                 | `float` | `1.0`                               | Contrast enhancement factor. 1.0 = unchanged                                                                    |
| Image Processing | `--sharpness`                | `float` | `1.0`                               | Sharpness enhancement factor. 1.0 = unchanged                                                                   |
| Image Processing | `--color` / `--no-color`     | `bool`  | `True`                              | Enable/disable ANSI color output                                                                                |
| Image Processing | `--boost`                    | `float` | `1.2`                               | Color brightness multiplier. Typical range: 1.0-1.4                                                             |
| Image Processing | `--bg`                       | `tuple` | `None`                              | Background color as three integers (R G B)                                                                      |
| Output/Terminal  | `-o, --output`               | `str`   | Input name w/ conversion attributes | Save output to file with custom name/path. Accepts full path or directory. Defaults to same directory as input. |
| Output/Terminal  | `--preview` / `--no-preview` | `bool`  | `True`                              | Show preview in terminal                                                                                        |
| Output/Terminal  | `--no-save`                  | `flag`  | `False`                             | Print to stdout only, don't save to file                                                                        |
| Output/Terminal  | `--hide-paths`               | `flag`  | `False`                             | Show only filenames in output (hide full paths)                                                                 |
| Output/Terminal  | `--version`                  | `flag`  | `False`                             | Show version number and exit                                                                                    |
| Output/Terminal  | `--help`                     | `flag`  | `False`                             | Show help message and exit                                                                                      |

---

## Python API

arTTY can be used directly as a Python library for more control over the conversion process. Import the `image_to_braille` function and pass various parameters to customize the output.

### Basic Usage

The simplest way to convert an image is to provide just the path. This uses all default settings (100-character width, color enabled, automatic background detection):

```python
from artty import image_to_braille

# Simple conversion with just the image path - uses all defaults
result = image_to_braille(path="logo.png")
print(result)
```

### Custom Dimensions

Control the output width to fit your needs. Smaller widths work better for narrow terminals, while larger widths capture more detail:

```python
from artty import image_to_braille

# Convert to narrower 60-character width (good for sidebars or compact displays)
result = image_to_braille(
    path="photo.jpg",
    width=60,  # Output width in braille characters (default is 100)
)
print(result)

# Or use a larger width for more detail (good for wide terminals)
result = image_to_braille(
    path="photo.jpg",
    width=150,  # Capture more image detail with wider output
)
print(result)
```

### Full Options Example

Here's a demonstration of every available parameter with explanations:

```python
from artty import image_to_braille

# Full example showing all parameters
result = image_to_braille(
    path="logo.png",        # Path to the input image file (supports PNG, JPEG, etc.)
    width=100,              # Output width in braille characters (10-500, default: 100)
    threshold=50,           # Brightness cutoff (0-255, default: 50) - lower = more dots
    contrast=1.0,           # Contrast multiplier (1.0 = unchanged, >1 = more contrast)
    sharpness=1.0,          # Sharpness multiplier (1.0 = unchanged, >1 = sharper edges)
    crop_padding=30,        # Padding pixels around image content before processing
    color=True,             # Enable 24-bit ANSI color output (True = color, False = plain text)
    bg_color=None,          # Background color as (R, G, B) tuple, or None for auto-detection
    color_boost=1.2,        # Color brightness multiplier (default: 1.2)
)
print(result)
```

### Plain Text Output

Disable color output when you need plain text for logging, saving to files, or terminals without color support:

```python
from artty import image_to_braille

# Convert to plain ASCII without ANSI color codes
result = image_to_braille(
    path="logo.png",
    color=False,  # Disable color - output will be plain text with braille characters only
)
print(result)

# Useful for saving to plain text files
with open("output.txt", "w") as f:
    f.write(result)
```

### With Background Color

Specify a background color when the image has transparency or you want to override the detected background:

```python
from artty import image_to_braille

# Use a black background (good for light images)
result = image_to_braille(
    path="logo.png",
    bg_color=(0, 0, 0),  # RGB tuple for black background
)
print(result)

# Use a white background (good for dark images)
result = image_to_braille(
    path="photo.jpg",
    bg_color=(255, 255, 255),  # RGB tuple for white background
)
print(result)

# Use a custom color (e.g., dark blue for a themed terminal)
result = image_to_braille(
    path="logo.png",
    bg_color=(10, 20, 40),  # RGB tuple for dark blue
)
print(result)
```

### From Bytes (File-like Objects)

Process images from memory without writing to disk - useful for web applications, APIs, or processing uploaded files:

```python
from artty import image_to_braille
from io import BytesIO

# Convert from bytes in memory
image_bytes = b"\x89PNG\r\n\x1a\n..."  # Your image bytes here
result = image_to_braille(path=image_bytes)
print(result)

# Or use BytesIO for more control
with open("photo.jpg", "rb") as f:
    image_data = f.read()

result = image_to_braille(path=image_data)
print(result)

# For web frameworks (FastAPI, Flask, etc.)
async def process_upload(upload):
    # upload.read() returns bytes
    result = image_to_braille(path=upload.read())
    return result
```
---

## Testing

```bash
# Using uv (recommended)
uv run pytest

# Or using pip
pytest tests/ -v
```
---

## Contributing

Contributions are welcome! Please review our [contributing guidelines][contributing-link] before getting started. If you'd like to contribute, please [open an issue][issues-link] to discuss your proposed changes or feel free to submit a pull request directly.

---

## Acknowledgements

- [Pillow][pillow-link] — Primary image processing library
- [click][click-link] — CLI framework

---

## License

Distributed under the MIT License. See [LICENSE][license-link] for more information.

---

**Last updated:** 2026-04-18

<!-- Badge Links -->
[pypi-badge-badge]: https://img.shields.io/pypi/v/artty?style=plastic&color=black&logo=pypi&logoColor=white
[pypi-badge-link]: https://pypi.org/project/artty/
[python-badge-badge]: https://img.shields.io/pypi/pyversions/artty?logo=python&style=plastic&color=black&logoColor=white
[python-badge-link]: https://www.python.org/
[license-badge-badge]: https://img.shields.io/badge/license-MIT-blue?style=plastic&logo=open-source-initiative&color=black&logoColor=white
[license-badge-link]: https://opensource.org/licenses/MIT
[codecov-badge-badge]: https://img.shields.io/codecov/c/github/divisionseven/artty?logo=codecov&style=plastic&color=black&logoColor=white
[codecov-badge-link]: https://app.codecov.io/gh/divisionseven/artty
[ci-badge-badge]: https://img.shields.io/github/actions/workflow/status/divisionseven/artty/ci.yml?branch=main&logo=github&style=plastic&color=black&logoColor=white
[ci-badge-link]: https://github.com/divisionseven/artty/actions/workflows/ci.yml

<!-- Logo Assets -->

<!-- Documentation Links -->
[docs-index-link]: docs/index.md
[docs-algorithm-link]: docs/algorithm.md
[docs-reference-link]: docs/reference.md
[docs-examples-link]: docs/examples.md
[contributing-link]: CONTRIBUTING.md
[license-link]: LICENSE

<!-- Repo Links -->
[issues-link]: https://github.com/divisionseven/artty/issues

<!-- Terminal Emulator Links -->
[ghostty-link]: https://ghostty.org
[iterm2-link]: https://iterm2.com
[kitty-link]: https://sw.kovidgoyal.net/kitty
[alacritty-link]: https://alacritty.org
[wezterm-link]: https://wezfurlong.org/wezterm
[vscode-link]: https://code.visualstudio.com

<!-- Acknowledgements -->
[pillow-link]: https://github.com/python-pillow/Pillow
[click-link]: https://github.com/pallets/click
