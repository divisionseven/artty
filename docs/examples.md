# Usage Examples

Practical examples demonstrating common artty workflows.

---

## Basic Conversion

The simplest usage — convert an image with default settings:

```bash
artty photo.jpg
```

This produces:
- 100 Braille characters wide
- Color output enabled
- Default threshold (50), contrast (1.0), sharpness (1.0)
- Output file saved next to the input (e.g., `photo_ascii_color_w100.txt`)
- Preview displayed in terminal

---

## Color Output

Enable or disable color explicitly:

```bash
# Color output (default)
artty logo.png --color

# Plain text output (no ANSI codes)
artty logo.png --no-color
```

Use `--no-color` when:
- Printing to a printer
- Saving to a file that will be viewed in a plain text editor
- The terminal doesn't support ANSI colors

---

## Different Widths

Control the level of detail with `-w`:

```bash
# Compact output (50 chars wide)
artty image.png -w 50

# Default (100 chars wide)
artty image.png -w 100

# High detail (200 chars wide)
artty image.png -w 200
```

**Tip**: Higher widths produce more detail but require a wider terminal to view without wrapping.

---

## Threshold Tuning

The threshold controls which pixels become "lit" dots:

```bash
# Lower threshold = denser output (more dots)
artty image.png -t 20

# Default threshold
artty image.png -t 50

# Higher threshold = sparser output (fewer dots)
artty image.png -t 100
```

### When to Adjust

| Threshold | Best For |
|-----------|----------|
| 20–30 | Dark images, images with dark backgrounds |
| 50 | General purpose, default works for most images |
| 100+ | Very bright images, images with white backgrounds |

### Visual Comparison

For the same image with different thresholds:

```
Threshold 20:  ⣿⠿⠧⠟⠛⠻⠹⠷⠶⠦
Threshold 50:  ⠟⠛⠻⠹⠷⠶⠦⠄
Threshold 100: ⠛⠻⠹⠂
```

---

## Contrast and Sharpness Enhancement

Improve output quality for images with poor contrast or soft edges:

```bash
# Increase contrast only
artty photo.jpg --contrast 1.5

# Increase sharpness only
artty photo.jpg --sharpness 1.5

# Both enhancements
artty photo.jpg --contrast 1.3 --sharpness 1.2
```

### Recommended Values

| Scenario | Contrast | Sharpness |
|----------|----------|-----------|
| Low contrast photo | 1.3–1.5 | 1.0 |
| Blurry photo | 1.0 | 1.3–1.5 |
| Both | 1.3 | 1.3 |
| Screenshot with text | 1.2 | 1.4 |

---

## Solid Background Color

Add a solid background to the output:

```bash
# Black background
artty image.png --bg 0 0 0

# Dark blue background
artty image.png --bg 20 20 40

# White background
artty image.png --bg 255 255 255
```

The `--bg` option requires three integers (R G B), each from 0 to 255.

---

## Color Boost Adjustment

If colors appear too dark in the terminal, increase the boost:

```bash
# Slight brightness boost (default)
artty image.png --boost 1.2

# More brightness
artty image.png --boost 1.4

# No boost
artty image.png --boost 1.0
```

The boost compensates for the darkening effect that occurs when embedding colors in terminal backgrounds.

---

## Piping to File

Use `--no-save` and `--no-preview` to output raw text for piping:

```bash
# Save to a specific location
artty image.png --no-save --no-preview > output.txt

# Pipe to another command
artty image.png --no-save --no-preview | less

# Save plain text (no ANSI codes)
artty image.png --no-color --no-preview > output.txt
```

This is useful for:
- Scripted batch processing
- Integrating with other tools
- Saving plain text without ANSI codes

---

## Custom Output Path

Specify where to save the output:

```bash
# Save to specific file
artty photo.jpg -o ~/Desktop/ascii_art.txt

# Save to directory (auto-generates filename)
artty photo.jpg -o ~/ASCII_Output/

# Save with custom naming
artty photo.jpg -o /path/to/my_output.txt
```

The auto-generated filename follows this pattern:
```
{input_stem}_ascii_{mode}_w{width}.txt
```

Examples:
- `logo_ascii_color_w100.txt`
- `photo_ascii_plain_w80.txt`

---

## Padding Adjustment

If image content is being cropped too tightly, increase padding:

```bash
# Minimal padding (default 30)
artty image.png --padding 30

# More padding
artty image.png --padding 60

# No padding
artty image.png --padding 0
```

Use higher padding when:
- Parts of the image appear cut off
- The image has a narrow content region with important details near the edge

---

## Putting It All Together

Combining multiple options:

```bash
# High-quality color output with custom width
artty photo.jpg -w 150 -t 40 --contrast 1.2 --sharpness 1.1 --boost 1.3

# Compact plain text output
artty image.png -w 60 --no-color --contrast 1.3

# Dark background with bright colors
artty logo.png --bg 10 10 15 --boost 1.4

# Full options example
artty input.png \
  --width 120 \
  --threshold 45 \
  --padding 40 \
  --contrast 1.25 \
  --sharpness 1.15 \
  --boost 1.3 \
  --bg 0 0 0 \
  -o output.txt
```

---

## Batch Processing

While artty doesn't have built-in batch processing, you can use shell loops:

```bash
# Convert all JPG files in a directory
for img in *.jpg; do
    artty "$img" -w 100
done

# Convert with custom settings
for img in *.png; do
    artty "$img" -w 80 --no-color -o ./output/
done
```

Or use parallel processing for faster results:

```bash
# Parallel conversion (macOS)
ls *.jpg | xargs -P 4 -I {} artty {} -w 100

# Parallel conversion (Linux)
ls *.jpg | parallel -j 4 artty {} -w 100
```

---

## Troubleshooting

### Output appears garbled

- Your terminal may not support 24-bit color
- Try `--no-color` for plain text output

### Image too large error

- Resize the image first (max 8192×8192)
- Or use a lower output width

### Colors look wrong

- Increase `--boost` value (try 1.4)
- Check if terminal background is affecting perception
- Try `--no-color` to see the actual Braille pattern

### Parts of image are cropped

- Increase `--padding` value
- Check that the original image isn't already cropped tightly

### File is too large

- Maximum file size is 100MB
- Compress the image or use a smaller version