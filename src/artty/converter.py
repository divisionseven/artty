"""Core conversion logic for artty."""

import os

from artty.ansi import _supports_ansi
from typing import Optional

# Max dimensions to prevent memory exhaustion (8192x8192 = ~67M pixels)
MAX_WIDTH = 8192
MAX_HEIGHT = 8192

# Max file size: 100MB (104857600 bytes)
MAX_FILE_SIZE = 100 * 1024 * 1024

# Braille dot bit-positions for a 2-column × 4-row cell (Unicode U+2800 base)
DOT_MAP = [
    [0x01, 0x08],  # row 0: dot1 (left),  dot4 (right)
    [0x02, 0x10],  # row 1: dot2 (left),  dot5 (right)
    [0x04, 0x20],  # row 2: dot3 (left),  dot6 (right)
    [0x40, 0x80],  # row 3: dot7 (left),  dot8 (right)
]

# ANSI escape codes
ANSI_RESET = "\033[0m"


def _ansi_fg(r: int, g: int, b: int) -> str:
    """Generate ANSI 24-bit foreground color escape code."""
    return f"\033[38;2;{r};{g};{b}m"


def _ansi_bg(r: int, g: int, b: int) -> str:
    """Generate ANSI 24-bit background color escape code."""
    return f"\033[48;2;{r};{g};{b}m"


def _boost_color(r: int, g: int, b: int, factor: float) -> tuple[int, int, int]:
    """
    Apply a brightness multiplier to a color.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        factor: Multiplicative brightness factor

    Returns:
        Tuple of (r, g, b) with values capped at 255
    """
    return (
        min(255, int(r * factor)),
        min(255, int(g * factor)),
        min(255, int(b * factor)),
    )


USE_ANSI = _supports_ansi()


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
    transparent: str = "ignore",
) -> str:
    """
    Convert an image to a braille-character ASCII string.

    Parameters
    ----------
    path : str
        Path to the source image.
    width : int
        Output width in braille characters (height is auto-calculated).
    threshold : int
        Pixel luminance cutoff (0–255). Pixels above this are treated
        as foreground; pixels at or below are treated as background.
    contrast : float
        PIL contrast enhancement factor (1.0 = unchanged).
    sharpness : float
        PIL sharpness enhancement factor (1.0 = unchanged).
    crop_padding : int
        Extra pixels to keep around the auto-detected content bounding
        box before resizing.
    color : bool
        If True, embed 24-bit ANSI foreground color codes (sampled only
        from lit pixels, so dark borders never corrupt edge colors).
    bg_color : Optional[tuple[int, int, int]]
        Optional (R, G, B) tuple for a solid ANSI background fill.
        Ignored when color=False.
    color_boost : float
        Multiplicative factor applied to averaged lit-pixel colors.
        Values 1.0–1.4 work well for most source images.
    transparent : str
        How to handle transparent pixels: "black" composites over black,
        "white" composites over white, "ignore" treats as background
        (default: "ignore").

    Returns
    -------
    str
        A multi-line string of braille characters, with or without embedded ANSI codes.

    Raises
    ------
    FileNotFoundError
        If the image file cannot be opened.
    ValueError
        If image dimensions exceed MAX_WIDTH x MAX_HEIGHT or file is too large.
    ImportError
        If Pillow is not installed.
    """
    # ── Validate inputs ─────────────────────────────────────────────────────────────
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Image file not found: {path}")

    file_size = os.path.getsize(path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"Image file too large ({file_size // (1024 * 1024)}MB). "
            f"Maximum allowed: {MAX_FILE_SIZE // (1024 * 1024)}MB"
        )

    if file_size == 0:
        raise ValueError("Image file is empty (0 bytes)")

    try:
        from PIL import Image, ImageEnhance
    except ImportError:
        raise ImportError("Pillow is required. Install it with: pip install Pillow")

    # ── Load image and validate dimensions ─────────────────────────────────────────
    try:
        img: "Image.Image" = Image.open(path)
        width_px, height_px = img.size
    except Exception as e:
        raise ValueError(f"Cannot read image: {e}")

    # ── Handle transparency based on mode ────────────────────────────────────────
    # Check if image has transparency (either RGBA or indexed with palette)
    has_transparency = img.mode in ("RGBA", "PA") or (
        img.mode == "P" and "transparency" in img.info
    )

    # Handle transparency: composite all transparent pixels to background color.
    # This ensures consistent behavior regardless of the original transparent color.
    # We use (1,1,1) for black mode instead of (0,0,0) because pure black gets
    # cropped out by PIL's getbbox(), which would lose the transparent area.
    if has_transparency:
        if transparent == "black":
            bg_color_composite = (1, 1, 1)  # Nearly black, won't be bbox-cropped
        elif transparent == "white":
            bg_color_composite = (255, 255, 255)
        else:  # "ignore"
            # Composite to dark gray (1,1,1) so transparent pixels have low luminance
            # and won't be rendered (achieving true "ignore")
            bg_color_composite = (1, 1, 1)

        composite_img = Image.new("RGBA", img.size, bg_color_composite)
        if img.mode == "P":
            img = img.convert("RGBA")
        composite_img.paste(img, (0, 0), img)
        img = composite_img

    if width_px > MAX_WIDTH or height_px > MAX_HEIGHT:
        raise ValueError(
            f"Image dimensions {width_px}x{height_px} exceed maximum allowed "
            f"{MAX_WIDTH}x{MAX_HEIGHT}. Resize the image first or use a lower "
            f"resolution."
        )

    if width_px < 2 or height_px < 2:
        raise ValueError(
            f"Image too small ({width_px}x{height_px}px). Minimum size is 2x2 pixels."
        )

    # ── Load & enhance ────────────────────────────────────────────────────────────
    # Note: img already loaded at line 140; do NOT re-open here as that would
    # discard the transparency composite created at lines 151-161.
    img_gray = img.convert("L")
    img_gray = ImageEnhance.Contrast(img_gray).enhance(contrast)
    img_gray = ImageEnhance.Sharpness(img_gray).enhance(sharpness)

    if color:
        img_rgb = img.convert("RGB")
        img_rgb = ImageEnhance.Contrast(img_rgb).enhance(contrast)
        img_rgb = ImageEnhance.Sharpness(img_rgb).enhance(sharpness)
    else:
        img_rgb = None  # not needed in plain mode

    # ── Crop to content bounding box ──────────────────────────────────────────────
    bbox = img_gray.getbbox()
    if bbox:
        bbox = (
            max(0, bbox[0] - crop_padding),
            max(0, bbox[1] - crop_padding),
            min(img_gray.width, bbox[2] + crop_padding),
            min(img_gray.height, bbox[3] + crop_padding),
        )
        img_gray = img_gray.crop(bbox)
        if img_rgb:
            img_rgb = img_rgb.crop(bbox)

    # ── Resize to target braille resolution ────────────────────────────────────────
    aspect = img_gray.height / img_gray.width
    char_height = int(width * aspect * 0.5)
    px_width = width * 2
    px_height = char_height * 4

    img_gray = img_gray.resize((px_width, px_height), Image.Resampling.LANCZOS)
    if img_rgb:
        img_rgb = img_rgb.resize((px_width, px_height), Image.Resampling.LANCZOS)

    gray_px = img_gray.load()
    rgb_px = img_rgb.load() if img_rgb else None

    # ── Render braille rows ───────────────────────────────────────────────────────
    bg_prefix = _ansi_bg(*bg_color) if (color and bg_color) else ""

    # For black mode: we need to detect black pixels specially
    # since black has luminance=0 which would be below threshold
    # The key is: if transparent="black", black pixels should render
    render_black = transparent == "black"

    lines = []
    for cy in range(char_height):
        row_chars = []
        row_colors: list[Optional[tuple[int, int, int]]] = []

        for cx in range(width):
            bits = 0
            r_sum = g_sum = b_sum = 0
            lit_count = 0
            has_black_pixels = False  # Track black pixels for black mode

            for dy in range(4):
                for dx in range(2):
                    px = cx * 2 + dx
                    py = cy * 4 + dy
                    if px < px_width and py < px_height:
                        lum: int = gray_px[px, py]  # type: ignore[assignment,index]
                        is_black = False

                        # In black mode: treat nearly-black (luminance<=1) as lit
                        # since transparent pixels were composited to nearly-black (1,1,1)
                        # to avoid getbbox() cropping them out
                        if render_black and lum <= 1 and rgb_px:
                            r, g, b = rgb_px[px, py]  # type: ignore[misc]
                            if r <= 1 and g <= 1 and b <= 1:
                                is_black = True

                        if lum > threshold or is_black:
                            bits |= DOT_MAP[dy][dx]
                            if is_black:
                                # Black pixel - count it but don't add to color sum
                                has_black_pixels = True
                            elif color and rgb_px:
                                # Only sample from lit pixels — this prevents dark
                                # border pixels dragging edge colors toward black.
                                r, g, b = rgb_px[px, py]  # type: ignore[misc]
                                r_sum += r
                                g_sum += g
                                b_sum += b
                                lit_count += 1

            row_chars.append(chr(0x2800 + bits))

            if color:
                if has_black_pixels and not lit_count:
                    # All pixels in this cell are black (transparent areas)
                    row_colors.append((0, 0, 0))
                elif lit_count:
                    avg_r, avg_g, avg_b = (
                        r_sum // lit_count,
                        g_sum // lit_count,
                        b_sum // lit_count,
                    )
                    row_colors.append(_boost_color(avg_r, avg_g, avg_b, color_boost))
                else:
                    row_colors.append(None)
            else:
                row_colors.append(None)

        # Strip trailing blank braille cells
        while row_chars and row_chars[-1] == "\u2800":
            row_chars.pop()
            row_colors.pop()

        if color:
            parts = [bg_prefix] if bg_color else []
            prev_color = None
            for ch, col in zip(row_chars, row_colors):
                if ch == "\u2800":
                    ch = " "
                if col != prev_color:
                    parts.append(_ansi_fg(*col) if col else ANSI_RESET)
                    prev_color = col
                parts.append(ch)
            parts.append(ANSI_RESET)
            lines.append("".join(parts))
        else:
            lines.append("".join(row_chars).replace("\u2800", " "))

    # Strip trailing blank rows
    while lines and not lines[-1].strip(ANSI_RESET).strip():
        lines.pop()

    return "\n".join(lines)


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
    transparent: str = "ignore",
) -> str:
    """
    High-level wrapper for image_to_braille with simplified parameter names.

    Args:
        path: Path to the source image.
        width: Output width in braille characters.
        threshold: Pixel luminance cutoff (0-255).
        contrast: PIL contrast enhancement factor.
        sharpness: PIL sharpness enhancement factor.
        padding: Pixels of padding around content.
        color: Whether to include color codes.
        bg_color: Optional (R, G, B) for background color.
        color_boost: Brightness multiplier for colors.

    Returns:
        Multi-line string of braille characters.
    """
    return image_to_braille(
        path=path,
        width=width,
        threshold=threshold,
        contrast=contrast,
        sharpness=sharpness,
        crop_padding=padding,
        color=color,
        bg_color=bg_color,
        color_boost=color_boost,
        transparent=transparent,
    )
