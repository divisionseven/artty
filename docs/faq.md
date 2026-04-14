# Frequently Asked Questions

> **Last updated:** 2026-04-13

This page answers common questions about using artty. If you don't find what you're looking for, check the [GitHub Issues](https://github.com/divisionseven/artty/issues) or start a [Discussion](https://github.com/divisionseven/artty/discussions).

---

## Table of Contents

- [Terminal Compatibility](#terminal-compatibility)
- [Color and Display Issues](#color-and-display-issues)
- [File Size and Performance](#file-size-and-performance)
- [Multiple Image Conversion](#multiple-image-conversion)
- [Python Integration](#python-integration)
- [Unicode and Braille](#unicode-and-braille)
- [Troubleshooting](#troubleshooting)

---

## Terminal Compatibility

### What terminals support artty's color output?

Artty produces 24-bit ANSI color escape sequences, which require a terminal with TrueColor support. The following terminals are confirmed to work:

| Terminal | Platform | Support |
|----------|----------|---------|
| **Ghostty** | macOS, Linux | Full |
| **iTerm2** | macOS | Full |
| **Kitty** | macOS, Linux | Full |
| **WezTerm** | macOS, Linux, Windows | Full |
| **Alacritty** | macOS, Linux, Windows | Full |
| **Windows Terminal** | Windows | Full |
| **VS Code Integrated Terminal** | All | Full |

### Does artty work on Windows?

Yes. On Windows 10/11, use **Windows Terminal** (not the legacy Command Prompt) for color output. The old `cmd.exe` has limited color support.

```powershell
# Windows Terminal (recommended)
artty image.png

# PowerShell also works in Windows Terminal
artty image.png --no-color
```

### My terminal shows garbled characters instead of braille

This typically means your terminal doesn't support Unicode braille characters (U+2800–U+28FF). Check that:

1. Your terminal font includes the Braille Unicode block
2. Your locale is set to UTF-8: `export LC_ALL=en_US.UTF-8` (Linux/macOS)
3. The font you're using has braille glyphs (not all monospace fonts do)

If characters appear as boxes or question marks, try a different font like **JetBrains Mono**, **Fira Code**, or **Cascadia Code**.

### Can I use artty over SSH?

Yes, but ensure both the local and remote terminals support UTF-8 and TrueColor. The remote session needs:

```bash
# On the remote server
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
```

### Does artty work in tmux or screen?

Yes, but you may need to enable truecolor support explicitly:

```bash
# In .tmux.conf
set -g default-terminal "screen-256color"

# Or for truecolor (tmux 2.2+)
set -ga terminal-overrides ",xterm-256color:Tc"
```

---

## Color and Display Issues

### The output looks too dark / too light

Adjust the **threshold** and **contrast** options:

```bash
# Lower threshold = more dots (darker output)
artty image.png -t 30

# Higher threshold = fewer dots (lighter output)
artty image.png -t 80

# Adjust contrast
artty image.png --contrast 1.3
```

### Colors look washed out or too dark

Use the `--boost` option to adjust color brightness:

```bash
# Increase color brightness (default is 1.2)
artty image.png --boost 1.4

# Decrease for darker images
artty image.png --boost 1.0
```

### How do I set a background color?

Use the `--bg` option with RGB values:

```bash
# Black background
artty image.png --bg 0 0 0

# White background
artty image.png --bg 255 255 255

# Dark blue background
artty image.png --bg 10 20 40
```

The background is auto-detected from image corners by default. Use `--bg` to override.

### Why does my output have dark edges?

This happens when the background color isn't detected correctly. Try:

1. **Specify the background manually:**
   ```bash
   artty image.png --bg 255 255 255  # white background
   ```

2. **Increase padding:**
   ```bash
   artty image.png --padding 50
   ```

3. **Adjust contrast:**
   ```bash
   artty image.png --contrast 1.2
   ```

### Can I get plain text without ANSI colors?

Yes, use `--no-color`:

```bash
artty image.png --no-color
```

This outputs plain braille characters with no color codes, suitable for logging, saving to files, or terminals without color support.

---

## File Size and Performance

### What image formats are supported?

Artty supports any format Pillow can read:

- PNG, JPEG, GIF, BMP, WEBP, TIFF, and more

```bash
artty photo.jpg
artty image.png
artty picture.webp
```

### Is there a maximum image size?

There is no hard limit, but very large images (10MB+) may be slow. For best performance:

- Images under 5MB convert in 1-3 seconds
- Images 5-20MB may take 5-15 seconds
- Images over 20MB are not recommended

### Output file size?

A 100-character wide conversion produces a file of approximately 10-15KB. The file size scales linearly with width:

| Width | Approximate Size |
|-------|-----------------|
| 50 chars | 5-8 KB |
| 100 chars | 10-15 KB |
| 200 chars | 20-30 KB |
| 500 chars | 50-75 KB |

### Can I control output width?

Yes, use `-w` or `--width`:

```bash
# 80-character width
artty image.png -w 80

# 200-character width for more detail
artty image.png -w 200
```

Valid range: 10-500 characters.

---

## Multiple Image Conversion

### How do I convert multiple images?

Artty processes one image at a time. For batch conversion, use a shell loop:

```bash
# Convert all images in a directory
for img in *.png *.jpg; do
    artty "$img" -o "./output/${img%.png}.txt"
done

# Or with GNU parallel
ls *.png *.jpg | parallel -j 4 'artty {} -o {.}.txt'
```

### Can I use artty in a pipeline?

Yes! Use `--no-save` to output to stdout:

```bash
# Pipe to another program
artty image.png --no-save | grep "some-pattern"

# Save to file manually
artty image.png --no-save > output.txt
```

---

## Python Integration

### Can I use artty in my Python script?

Yes! Import the `image_to_braille` function:

```python
from artty import image_to_braille

# Simple conversion
result = image_to_braille(path="image.png")
print(result)

# With custom options
result = image_to_braille(
    path="image.png",
    width=80,
    threshold=60,
    color=True,
    contrast=1.2
)
print(result)
```

### Can I process images from memory?

Yes, pass bytes directly:

```python
from artty import image_to_braille

# From file
with open("image.png", "rb") as f:
    result = image_to_braille(path=f.read())

# From URL (using requests)
import requests
response = requests.get("https://example.com/image.png")
result = image_to_braille(path=response.content)
```

### Can I use artty in a web application?

Yes, here's an example with FastAPI:

```python
from fastapi import FastAPI, UploadFile
from artty import image_to_braille

app = FastAPI()

@app.post("/convert")
async def convert_image(file: UploadFile):
    image_data = await file.read()
    result = image_to_braille(path=image_data)
    return {"ascii_art": result}
```

### What does `image_to_braille` return?

It returns a string containing either:
- Plain braille characters (with `--no-color`)
- Braille characters with embedded ANSI color codes (default)

The string includes newline characters for proper terminal display.

---

## Unicode and Braille

### What is Unicode Braille?

Unicode braille patterns (U+2800–U+28FF) provide 256 possible dot combinations in a 2×4 cell:

```
⠁ ⠂ ⠃ ℀ ℁ ℂ ℃
⠇ ⠈ ⠉ ⠊ ⠋ ⠌ ⠍
```

Each braille character represents up to 8 pixels (2 columns × 4 rows), making braille ASCII art approximately 4× more detailed than traditional ASCII art.

### Why use braille instead of regular ASCII?

| Character Type | Pixels per Character | Detail Level |
|----------------|---------------------|--------------|
| Standard ASCII | 1 (.) | Low |
| Unicode Braille | 8 (2×4) | High |

Braille captures significantly more image detail while using fewer characters, making it ideal for terminal display.

### Are braille characters readable on all systems?

Most modern terminals and fonts support braille Unicode characters. If you see boxes or question marks, your terminal or font may not include the Braille Unicode block. Try a different terminal or font (see [Terminal Compatibility](#terminal-compatibility)).

---

## Troubleshooting

### "Could not open image: [Errno 2] No such file or directory"

The image file doesn't exist or the path is incorrect. Use an absolute path or check your current directory:

```bash
# Check current directory
pwd

# List files
ls -la

# Use absolute path
artty /full/path/to/image.png
```

### "ValueError: Output path must be in same directory as input"

For security, artty prevents writing output to directories outside the input file's directory. Move your output path or use a subdirectory:

```bash
# This will fail
artty image.png -o /tmp/output.txt

# This works (relative to input file's directory)
artty image.png -o ./output/
```

### Conversion is very slow

Large images take longer. Try:

1. **Resize the image first:**
   ```bash
   # Using ImageMagick
   convert large.jpg -resize 50% small.jpg
   artty small.jpg
   ```

2. **Use a smaller width:**
   ```bash
   artty image.png -w 50  # faster than -w 200
   ```

3. **Use --no-color** (slightly faster, no color processing)

### The output looks pixelated

Increase the width for more detail:

```bash
artty image.png -w 200  # More detail than default 100
```

You can also adjust sharpness:

```bash
artty image.png --sharpness 1.3
```

### Error: "ImportError: No module named 'Pillow'"

Install Pillow:

```bash
# Using uv (recommended)
uv pip install Pillow

# Or using pip
pip install Pillow
```

### Help still not working!

- Check the [GitHub Issues](https://github.com/divisionseven/artty/issues) for similar problems
- Start a [Discussion](https://github.com/divisionseven/artty/discussions) to ask questions
- Report a bug if you found an issue

---

## Quick Reference

| Task | Command |
|------|---------|
| Basic conversion | `artty image.png` |
| Custom width | `artty image.png -w 80` |
| Plain text | `artty image.png --no-color` |
| Black background | `artty image.png --bg 0 0 0` |
| Save to file | `artty image.png -o output.txt` |
| No preview | `artty image.png --no-preview` |

---

> See also: [Algorithm](algorithm.md) · [CLI & API Reference](reference.md) · [Examples](examples.md)