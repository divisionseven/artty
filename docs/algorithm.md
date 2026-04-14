# How the Rendering Works

artty uses **Unicode Braille rendering** (2×4 pixel cells) to produce high-resolution ASCII art. This document provides a deep-dive technical explanation of each step in the conversion pipeline.

---

## Overview

The tool converts images into text representations using Unicode Braille characters (U+2800–U+28FF). Each Braille character encodes **8 dots** arranged in a 2×4 grid, representing 8 pixels of the original image. This provides **4× the detail** of traditional ASCII art, which typically only uses 2 dots per character.

| Metric | Traditional ASCII | artty Braille |
|--------|-------------------|---------------------|
| Dots per character | 2 | 8 |
| Pixel coverage | 1×2 | 2×4 |
| Detail multiplier | 1× | 4× |

---

## The Conversion Pipeline

### Step 1: Input Validation

Before any processing begins, the tool validates:

- **File existence**: Uses `os.path.isfile()` to confirm the image exists
- **File size limit**: Rejects files exceeding **100MB** (104,857,600 bytes)
- **Dimension limits**: Rejects images larger than **8192×8192 pixels**

```python
# From converter.py
MAX_WIDTH = 8192
MAX_HEIGHT = 8192
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

The dimension limits prevent memory exhaustion—a 8192×8192 image requires approximately 67 million pixels and significant processing overhead.

### Step 2: Image Loading & Pre-processing

The image is loaded using Pillow (PIL) and converted to grayscale for luminance analysis:

```python
img = Image.open(path)
img_gray = img.convert("L")
```

Then, optional enhancements are applied using PIL's `ImageEnhance`:

- **Contrast enhancement**: `ImageEnhance.Contrast(img_gray).enhance(contrast)` — default 1.0 (no change)
- **Sharpness enhancement**: `ImageEnhance.Sharpness(img_gray).enhance(sharpness)` — default 1.0 (no change)

These enhancements help bring out details in images with poor contrast or soft edges.

### Step 3: Content Detection & Cropping

The tool auto-detects the non-zero content region using PIL's `getbbox()` method:

```python
bbox = img_gray.getbbox()
if bbox:
    bbox = (
        max(0, bbox[0] - crop_padding),
        max(0, bbox[1] - crop_padding),
        min(img_gray.width, bbox[2] + crop_padding),
        min(img_gray.height, bbox[3] + crop_padding),
    )
    img_gray = img_gray.crop(bbox)
```

This removes empty borders while preserving a configurable **padding** (default: 30 pixels) around the content. The same crop is applied to the RGB image if color processing is enabled.

### Step 4: Resolution Calculation

The target Braille resolution is calculated based on the desired character width and the image's aspect ratio:

```python
aspect = img_gray.height / img_gray.width
char_height = int(width * aspect * 0.5)
px_width = width * 2       # 2 pixels per Braille char horizontally
px_height = char_height * 4  # 4 pixels per Braille char vertically
```

The **0.5 factor** compensates for the 2:1 aspect ratio of terminal characters (characters are approximately twice as tall as they are wide).

### Step 5: Braille Character Rendering (Core Algorithm)

This is where the magic happens. Each Braille cell represents a 2×4 pixel region:

```
Position:    Dot Index:    Bit Value:
┌───────────┐
│ •   •     │  ← row 0    →  0x01 (left), 0x08 (right)
│ •   •     │  ← row 1    →  0x02 (left), 0x10 (right)
│ •   •     │  ← row 2    →  0x04 (left), 0x20 (right)
│ •   •     │  ← row 3    →  0x40 (left), 0x80 (right)
└───────────┘
```

#### The DOT_MAP

```python
DOT_MAP = [
    [0x01, 0x08],  # row 0: dot1 (left),  dot4 (right)
    [0x02, 0x10],  # row 1: dot2 (left),  dot5 (right)
    [0x04, 0x20],  # row 2: dot3 (left),  dot6 (right)
    [0x40, 0x80],  # row 3: dot7 (left),  dot8 (right)
]
```

#### Threshold-Based Rendering

For each 2×4 pixel block:

1. **Luminance check**: Compare each pixel's grayscale value to the threshold (default: 50)
2. **Bit accumulation**: If `pixel_luminance > threshold`, set the corresponding bit in the pattern
3. **Unicode conversion**: Add the bit pattern to `0x2800` (Braille pattern base)

```python
bits = 0
for dy in range(4):
    for dx in range(2):
        lum = gray_px[px, py]
        if lum > threshold:
            bits |= DOT_MAP[dy][dx]

row_chars.append(chr(0x2800 + bits))
```

The threshold defines the **luminance cutoff**:
- **Lower threshold (e.g., 20)**: More pixels are "lit," producing denser output
- **Higher threshold (e.g., 100)**: Only bright pixels are "lit," producing sparse output

### Step 6: Color Processing

When color is enabled, the tool samples colors from the image. The key insight is the **"lit pixels only"** approach:

```python
# Only sample from lit pixels — this prevents dark
# border pixels dragging edge colors toward black.
if lum > threshold:
    r, g, b = rgb_px[px, py]
    r_sum += r
    g_sum += g
    b_sum += b
    lit_count += 1
```

**Why this matters**: If you average all pixels in a Braille cell (including dark background pixels), the resulting color gets pulled toward black. By only averaging lit pixels, edge colors remain vibrant and accurate.

The averaged color is then optionally boosted:

```python
avg_r, avg_g, avg_b = (r_sum // lit_count, g_sum // lit_count, b_sum // lit_count)
row_colors.append(_boost_color(avg_r, avg_g, avg_b, color_boost))
```

The default **color boost of 1.2** compensates for the darkening effect that occurs when embedding colors in terminal backgrounds.

### Step 7: ANSI Escape Codes

Color is embedded using **24-bit ANSI escape codes**:

- **Foreground**: `\033[38;2;R;G;Bm`
- **Background**: `\033[48;2;R;G;Bm`

Example: Red foreground → `\033[38;2;255;0;0m`

The output accumulates colors efficiently by only emitting ANSI codes when the color changes:

```python
for ch, col in zip(row_chars, row_colors):
    if col != prev_color:
        parts.append(_ansi_fg(*col) if col else ANSI_RESET)
        prev_color = col
    parts.append(ch)
```

### Step 8: Post-processing

Two cleanup steps occur after rendering:

1. **Strip trailing blank cells**: Remove empty Braille characters (`\u2800`) from the end of each row
2. **Strip trailing blank rows**: Remove rows that contain only whitespace after removing ANSI codes

This ensures the output has no unnecessary empty space at the edges.

---

## Why Braille?

The math is straightforward:

| Character Type | Dots per Cell | Resolution Multiplier |
|---------------|---------------|----------------------|
| Standard ASCII | 2 | 1× |
| Braille | 8 | 4× |

Each Braille character covers **2 pixels wide × 4 pixels tall** = **8 total pixels**, versus the 2 pixels that a typical ASCII character represents.

This means for the same terminal width, Braille rendering provides **4× the visual detail**.

---

## Key Technical Decisions

### Why Threshold Over Dithering?

**Decision**: Use simple threshold-based rendering instead of dithering algorithms.

**Rationale**:
- **Simplicity**: Threshold is straightforward to implement and understand
- **Clean output**: High-resolution images (which Braille rendering targets) don't benefit from dithering—the pixel grid is already fine enough
- **Performance**: No need for error diffusion calculations
- **Color compatibility**: Dithering complicates color sampling; threshold works cleanly with the "lit pixels only" color approach

### Why "Lit Pixels Only" for Color?

**Decision**: Sample color exclusively from pixels above the luminance threshold.

**Rationale**:
- **Edge preservation**: Dark borders won't corrupt edge colors toward black
- **Visual accuracy**: The color you see in the Braille dot should match what the eye perceives as the "subject" color
- **Simplicity**: No need for complex weight calculations

### Why 8192×8192 Maximum?

**Decision**: Cap image dimensions at 8192×8192.

**Rationale**:
- **Memory safety**: 8192×8192 = ~67 million pixels × 3 bytes (RGB) = ~200MB in the worst case
- **Performance**: Very large images take significant time to process
- **Practicality**: Most images users want to convert are far smaller; this limit catches truly pathological cases

---

## Summary

artty's rendering pipeline is designed for **high-resolution, color-accurate ASCII art**:

1. **Validate** → Check file, size, and dimensions
2. **Enhance** → Apply contrast and sharpness
3. **Crop** → Auto-detect content region
4. **Calculate** → Compute target Braille resolution
5. **Render** → Threshold-based dot pattern generation
6. **Color** → Sample from lit pixels only
7. **Encode** → Emit ANSI 24-bit color codes
8. **Clean** → Strip trailing blanks

The result is a clean, detailed text representation that captures both the structure and color of the original image.