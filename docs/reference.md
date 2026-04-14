# CLI and API Reference

Complete reference for artty's command-line interface and Python API.

---

## CLI Options

### Main Command

```bash
artty <input> [options]
```

### Option Reference

| Option | Flag(s) | Default | Range | Description |
|--------|---------|---------|-------|-------------|
| **Output width** | `-w`, `--width` | 100 | 10–500 | Output width in Braille characters. Height is auto-calculated based on image aspect ratio. |
| **Threshold** | `-t`, `--threshold` | 50 | 0–255 | Luminance cutoff. Pixels brighter than this become Braille dots. Lower = denser output, higher = sparser. |
| **Padding** | `--padding` | 30 | ≥0 | Pixels of padding around auto-detected content. Increase for images with tight cropping. |
| **Contrast** | `--contrast` | 1.0 | >0 | Contrast enhancement factor. 1.0 = unchanged. Values >1 increase contrast. |
| **Sharpness** | `--sharpness` | 1.0 | >0 | Sharpness enhancement factor. 1.0 = unchanged. Values >1 sharpen edges. |
| **Color boost** | `--boost` | 1.2 | >0 | Color brightness multiplier. Compensates for terminal background darkening. 1.0–1.4 typical. |
| **Background color** | `--bg R G B` | None | 0–255 each | Solid ANSI background color. Provide three integers (e.g., `--bg 0 0 0` for black). |
| **Color mode** | `--color` / `--no-color` | True | — | Enable or disable 24-bit ANSI color output. Default is enabled. |
| **Preview** | `--preview` / `--no-preview` | True | — | Print result to terminal after saving. Default is enabled. |
| **Save mode** | `--no-save` | False | — | Do not write a .txt file. Output to stdout only (useful for piping). |
| **Output path** | `-o`, `--output` | auto | — | Save location. Accepts a full file path or directory. Defaults to same directory as input. |

### Positional Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `input` | Yes | Path to the source image file. Must exist and be a valid image. |

### Detailed Option Descriptions

#### `-w, --width`

```
-w, --width INTEGER RANGE  Output width in braille characters. Height is auto-calculated.
                          (default: 100)
```

Controls the horizontal resolution of the output. Higher values produce more detail but take longer to render and may not fit on smaller terminals.

**Examples:**
- `-w 50` — Low resolution, compact output
- `-w 100` — Default, good balance
- `-w 200` — High detail, wide terminal required

#### `-t, --threshold`

```
-t, --threshold INTEGER RANGE  Luminance threshold (0-255). Pixels brighter than this become
                              braille dots. Lower = denser, higher = sparser. (default: 50)
```

Controls which pixels are considered "lit" in the Braille pattern.

- **0**: All pixels lit (solid block)
- **50**: Default, works well for most images
- **128**: Only bright pixels lit (very sparse)
- **255**: No pixels lit (empty output)

#### `--padding`

```
--padding INTEGER  Pixels of padding around auto-detected content. (default: 30)
```

Adds space around the detected content region before resizing. Increase this value if parts of your image are being cropped too tightly.

#### `--contrast`

```
--contrast FLOAT  Contrast enhancement factor. 1.0 = unchanged. (default: 1.0)
```

Enhances the difference between light and dark areas. Useful for images with low contrast.

- **0.5**: Reduced contrast
- **1.0**: Default (no change)
- **2.0**: Enhanced contrast

#### `--sharpness`

```
--sharpness FLOAT  Sharpness enhancement factor. 1.0 = unchanged. (default: 1.0)
```

Enhances edge definition. Useful for blurry images.

- **0.5**: Softer
- **1.0**: Default (no change)
- **2.0**: Sharper

#### `--color / --no-color`

```
--color / --no-color  Enable/disable 24-bit ANSI color output. (default: on)
```

When enabled, output includes ANSI escape codes for 24-bit true color. When disabled, outputs plain text (lighter pixels become Braille dots, darker become spaces).

#### `--boost`

```
--boost FLOAT  Color brightness multiplier. 1.0-1.4 typical. (default: 1.2)
```

Applies a brightness boost to sampled colors. The default (1.2) compensates for the darkening effect when colors are rendered on most terminal backgrounds.

#### `--bg`

```
--bg R G B  Solid ANSI background color as three integers (0-255).
```

Sets a solid background color for all Braille cells. Requires three integers for R, G, and B values.

**Example:** `--bg 20 20 30` sets a dark blue-gray background.

#### `--no-save`

```
--no-save  Do not write a .txt file — only print to stdout.
```

Disables file output. Use with `--no-preview` to pipe raw output to another command:

```bash
artty input.png --no-save --no-preview > output.txt
```

#### `-o, --output`

```
-o, --output TEXT  Where to save the .txt file. Accepts a full file path or a directory.
                   If a directory is given, the filename is derived from the input image name.
                   Defaults to the same directory as the input image.
```

Specifies where to save the output. If a directory is provided, the filename is auto-generated from the input name (e.g., `photo_ascii_color_w100.txt`).

#### `--preview / --no-preview`

```
--preview / --no-preview  Print the result to the terminal after saving (default: on)
```

Controls whether the result is displayed in the terminal. Use `--no-preview` when you don't want to see the output but still want to save the file.

---

## Python API

### Main Functions

#### `image_to_braille()`

```python
from artty.converter import image_to_braille

def image_to_braille(
    path: str,
    width: int,
    threshold: int,
    contrast: float,
    sharpness: float,
    crop_padding: int,
    color: bool = True,
    bg_color: Optional[tuple[int, int, int]] = None,
    color_boost: float = 1.2,
) -> str:
    """Convert an image to a braille-character ASCII string."""
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | (required) | Path to the source image file. |
| `width` | `int` | (required) | Output width in Braille characters (height is auto-calculated). |
| `threshold` | `int` | (required) | Pixel luminance cutoff (0–255). Pixels above this are treated as foreground. |
| `contrast` | `float` | (required) | PIL contrast enhancement factor (1.0 = unchanged). |
| `sharpness` | `float` | (required) | PIL sharpness enhancement factor (1.0 = unchanged). |
| `crop_padding` | `int` | (required) | Extra pixels to keep around the auto-detected content bounding box. |
| `color` | `bool` | `True` | If True, embed 24-bit ANSI foreground color codes. |
| `bg_color` | `Optional[tuple[int, int, int]]` | `None` | Optional (R, G, B) tuple for solid ANSI background fill. |
| `color_boost` | `float` | `1.2` | Multiplicative factor for averaged lit-pixel colors. |

**Returns:**

- `str`: A multi-line string of Braille characters, with or without embedded ANSI codes.

**Raises:**

- `FileNotFoundError`: If the image file cannot be opened.
- `ValueError`: If image dimensions exceed 8192×8192 or file is too large.
- `ImportError`: If Pillow is not installed.

**Example:**

```python
result = image_to_braille(
    path="photo.jpg",
    width=100,
    threshold=50,
    contrast=1.2,
    sharpness=1.1,
    crop_padding=30,
    color=True,
    bg_color=None,
    color_boost=1.3,
)
print(result)
```

---

#### `convert_image()`

```python
from artty.converter import convert_image

def convert_image(
    path: str,
    width: int = 100,
    threshold: int = 50,
    contrast: float = 1.0,
    sharpness: float = 1.0,
    padding: int = 30,
    color: bool = True,
    bg_color: Optional[tuple[int, int, int]] = None,
    color_boost: float = 1.2,
) -> str:
    """High-level wrapper for image_to_braille with simplified parameter names."""
```

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `path` | `str` | (required) | Path to the source image. |
| `width` | `int` | 100 | Output width in Braille characters. |
| `threshold` | `int` | 50 | Pixel luminance cutoff (0-255). |
| `contrast` | `float` | 1.0 | PIL contrast enhancement factor. |
| `sharpness` | `float` | 1.0 | PIL sharpness enhancement factor. |
| `padding` | `int` | 30 | Pixels of padding around content. |
| `color` | `bool` | True | Whether to include color codes. |
| `bg_color` | `Optional[tuple[int, int, int]]` | None | Optional (R, G, B) for background color. |
| `color_boost` | `float` | 1.2 | Brightness multiplier for colors. |

**Returns:**

- `str`: Multi-line string of Braille characters.

**Example:**

```python
# Simple usage with defaults
ascii_art = convert_image("logo.png")

# Custom output
ascii_art = convert_image(
    path="photo.jpg",
    width=120,
    threshold=40,
    contrast=1.3,
    sharpness=1.5,
    padding=50,
    color=True,
    bg_color=(0, 0, 0),
    color_boost=1.3,
)
```

---

### Helper Functions

#### `_ansi_fg()`

```python
def _ansi_fg(r: int, g: int, b: int) -> str:
    """Generate ANSI 24-bit foreground color escape code."""
```

**Parameters:** RGB values (0–255 each)

**Returns:** ANSI escape string (e.g., `\033[38;2;255;0;0m`)

---

#### `_ansi_bg()`

```python
def _ansi_bg(r: int, g: int, b: int) -> str:
    """Generate ANSI 24-bit background color escape code."""
```

**Parameters:** RGB values (0–255 each)

**Returns:** ANSI escape string (e.g., `\033[48;2;0;0;0m`)

---

#### `_boost_color()`

```python
def _boost_color(r: int, g: int, b: int, factor: float) -> tuple[int, int, int]:
    """Apply a brightness multiplier to a color."""
```

**Parameters:**
- `r`, `g`, `b`: RGB components (0–255)
- `factor`: Multiplicative brightness factor

**Returns:** Tuple of (r, g, b) with values capped at 255

---

### Constants

| Constant | Value | Description |
|----------|-------|-------------|
| `MAX_WIDTH` | 8192 | Maximum image width in pixels |
| `MAX_HEIGHT` | 8192 | Maximum image height in pixels |
| `MAX_FILE_SIZE` | 104857600 | Maximum file size (100MB) |
| `DOT_MAP` | list | Braille dot bit-position mapping |

---

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid arguments or image processing error |

---

### Error Messages

Common CLI errors:

- `"Could not open image: Image file not found: <path>"` — Input file doesn't exist
- `"Image file too large (X MB). Maximum allowed: 100 MB"` — File exceeds size limit
- `"Image dimensions XxY exceed maximum allowed 8192x8192"` — Image too large
- `"--contrast must be a positive number."` — Invalid contrast value
- `"--sharpness must be a positive number."` — Invalid sharpness value
- `"--padding cannot be negative."` — Padding cannot be negative