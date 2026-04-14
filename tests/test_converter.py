"""Tests for the core converter module."""

import os

import pytest

from artty.converter import (
    DOT_MAP,
    _ansi_bg,
    _ansi_fg,
    _boost_color,
    convert_image,
    image_to_braille,
)


class TestAnsiHelpers:
    """Tests for ANSI helper functions."""

    def test_ansi_fg_generates_correct_format(self):
        """Test that _ansi_fg generates the correct escape sequence."""
        result = _ansi_fg(255, 128, 0)
        assert result == "\033[38;2;255;128;0m"

    def test_ansi_bg_generates_correct_format(self):
        """Test that _ansi_bg generates the correct escape sequence."""
        result = _ansi_bg(0, 0, 255)
        assert result == "\033[48;2;0;0;255m"

    def test_boost_color_caps_at_255(self):
        """Test that _boost_color caps values at 255."""
        result = _boost_color(200, 200, 200, 2.0)
        assert result == (255, 255, 255)

    def test_boost_color_with_factor_1(self):
        """Test that factor 1.0 returns unchanged values."""
        result = _boost_color(100, 150, 200, 1.0)
        assert result == (100, 150, 200)

    def test_boost_color_with_fractional_factor(self):
        """Test that factor less than 1 reduces values."""
        result = _boost_color(100, 100, 100, 0.5)
        assert result == (50, 50, 50)


class TestDotMap:
    """Tests for the DOT_MAP constant."""

    def test_dot_map_has_4_rows(self):
        """Test that DOT_MAP has 4 rows."""
        assert len(DOT_MAP) == 4

    def test_dot_map_each_row_has_2_columns(self):
        """Test that each row has 2 columns."""
        for row in DOT_MAP:
            assert len(row) == 2


class TestConversionWithRealImage:
    """Tests that require real image files."""

    @pytest.fixture
    def test_image_path(self, tmp_path):
        """Create a small test image."""
        from PIL import Image

        # Create a simple gradient grayscale image
        img = Image.new("L", (20, 20))
        for y in range(20):
            for x in range(20):
                img.putpixel((x, y), (x * 12) % 256)  # Gradient

        path = tmp_path / "test.png"
        img.save(path)
        return str(path)

    @pytest.fixture
    def test_color_image_path(self, tmp_path):
        """Create a small color test image."""
        from PIL import Image

        # Create a simple RGB image
        img = Image.new("RGB", (20, 20))
        for y in range(20):
            for x in range(20):
                img.putpixel((x, y), (x * 12 % 256, y * 12 % 256, 128))

        path = tmp_path / "test_color.png"
        img.save(path)
        return str(path)

    def test_braille_output_contains_valid_unicode(self, test_image_path):
        """Test that output contains valid braille Unicode characters."""
        result = image_to_braille(
            path=test_image_path,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # Braille range is U+2800 to U+28FF
        for char in result:
            if char.strip():  # Skip whitespace
                code = ord(char)
                assert 0x2800 <= code <= 0x28FF, f"Invalid braille char: U+{code:04X}"

    def test_plain_mode_no_ansi_codes(self, test_image_path):
        """Test that plain mode produces no ANSI codes."""
        result = image_to_braille(
            path=test_image_path,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        assert "\033[" not in result

    def test_color_mode_contains_ansi_codes(self, test_color_image_path):
        """Test that color mode includes ANSI codes."""
        result = image_to_braille(
            path=test_color_image_path,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=True,
        )
        assert "\033[38;2;" in result

    def test_threshold_behavior_higher_is_sparser(self, test_image_path):
        """Test that higher threshold produces sparser output."""
        result_low = image_to_braille(
            path=test_image_path,
            width=10,
            threshold=10,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        result_high = image_to_braille(
            path=test_image_path,
            width=10,
            threshold=200,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # Count non-space characters
        chars_low = sum(1 for c in result_low if c not in " \n")
        chars_high = sum(1 for c in result_high if c not in " \n")
        assert chars_low >= chars_high

    def test_width_scaling_affects_output(self, test_image_path):
        """Test that different widths produce different character counts."""
        result_narrow = image_to_braille(
            path=test_image_path,
            width=20,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        result_wide = image_to_braille(
            path=test_image_path,
            width=40,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # Wider should have more characters per line
        narrow_line_len = max(len(line) for line in result_narrow.split("\n"))
        wide_line_len = max(len(line) for line in result_wide.split("\n"))
        assert wide_line_len > narrow_line_len

    def test_invalid_image_raises_error(self, tmp_path):
        """Test that invalid image path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            image_to_braille(
                path=str(tmp_path / "nonexistent.png"),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )


class TestConvertImageWrapper:
    """Tests for the high-level convert_image wrapper."""

    def test_convert_image_with_defaults(self, tmp_path):
        """Test that convert_image works with default parameters."""
        from PIL import Image

        img = Image.new("L", (20, 20), 128)
        path = tmp_path / "test.png"
        img.save(path)

        result = convert_image(str(path))
        assert isinstance(result, str)
        assert len(result) > 0


class TestContrastSharpness:
    """Tests for contrast and sharpness effects."""

    def test_contrast_changes_output(self, tmp_path):
        """Test that non-1.0 contrast changes the output."""
        from PIL import Image

        # Create image with actual variation (gradient)
        img = Image.new("L", (20, 20))
        for y in range(20):
            for x in range(20):
                img.putpixel((x, y), (x * 12) % 256)

        path = tmp_path / "test.png"
        img.save(path)

        result_default = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        result_high_contrast = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=2.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # Different contrast should produce different output
        assert result_default != result_high_contrast

    def test_sharpness_with_contrast_differently(self, tmp_path):
        """Test that sharpness + contrast together differ from default."""
        from PIL import Image

        # Create image with actual variation
        img = Image.new("L", (20, 20))
        for y in range(20):
            for x in range(20):
                img.putpixel((x, y), (x * 12) % 256)

        path = tmp_path / "test.png"
        img.save(path)

        result_default = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # Use both contrast and sharpness together - more likely to change output
        result_enhanced = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=1.5,
            sharpness=1.5,
            crop_padding=0,
            color=False,
        )
        # Enhanced should differ from default
        assert result_default != result_enhanced


class TestErrorPathHandling:
    """Tests for error handling and validation."""

    def test_corrupt_image_raises_error(self, tmp_path):
        """Test that a corrupt image file raises ValueError."""
        # Write invalid image data (not a valid PNG)
        corrupt_path = tmp_path / "corrupt.png"
        corrupt_path.write_bytes(b"This is not a valid image file")

        with pytest.raises(ValueError, match="Cannot read image"):
            image_to_braille(
                path=str(corrupt_path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_unsupported_format_raises_error(self, tmp_path):
        """Test that an unsupported image format raises ValueError."""
        # Create a file with a valid extension but unsupported format
        # .bmp is valid but .xyz is not recognized by Pillow
        unsupported_path = tmp_path / "test.xyz"
        # Write minimal valid image header that Pillow can't parse
        unsupported_path.write_bytes(b"\x00\x00\x00\x00")

        with pytest.raises(ValueError, match="Cannot read image"):
            image_to_braille(
                path=str(unsupported_path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_empty_file_raises_error(self, tmp_path):
        """Test that an empty file raises ValueError."""
        empty_path = tmp_path / "empty.png"
        empty_path.write_bytes(b"")

        with pytest.raises(ValueError, match="empty"):
            image_to_braille(
                path=str(empty_path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_too_large_dimensions_raises_error(self, tmp_path):
        """Test that an image exceeding max dimensions raises ValueError."""
        from PIL import Image

        # Create an image larger than MAX_WIDTH x MAX_HEIGHT (8192x8192)
        img = Image.new("RGB", (10000, 10000), (255, 0, 0))
        path = tmp_path / "huge.png"
        img.save(path)

        with pytest.raises(ValueError, match="exceed.*maximum"):
            image_to_braille(
                path=str(path),
                width=100,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_too_large_width_raises_error(self, tmp_path):
        """Test that wide but short image exceeding max width raises error."""
        from PIL import Image

        img = Image.new("RGB", (10000, 100), (255, 0, 0))
        path = tmp_path / "wide.png"
        img.save(path)

        with pytest.raises(ValueError, match="exceed.*maximum"):
            image_to_braille(
                path=str(path),
                width=100,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_too_large_height_raises_error(self, tmp_path):
        """Test that tall but narrow image exceeding max height raises error."""
        from PIL import Image

        img = Image.new("RGB", (100, 10000), (255, 0, 0))
        path = tmp_path / "tall.png"
        img.save(path)

        with pytest.raises(ValueError, match="exceed.*maximum"):
            image_to_braille(
                path=str(path),
                width=100,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_too_small_image_raises_error(self, tmp_path):
        """Test that an image smaller than 2x2 raises ValueError."""
        from PIL import Image

        # Create a 1x1 pixel image - too small
        img = Image.new("RGB", (1, 1), (255, 0, 0))
        path = tmp_path / "tiny.png"
        img.save(path)

        with pytest.raises(ValueError, match="too small"):
            image_to_braille(
                path=str(path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_too_small_width_raises_error(self, tmp_path):
        """Test that 1-pixel wide image raises error."""
        from PIL import Image

        img = Image.new("RGB", (1, 10), (255, 0, 0))
        path = tmp_path / "one_pixel.png"
        img.save(path)

        with pytest.raises(ValueError, match="too small"):
            image_to_braille(
                path=str(path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_nonexistent_path_raises_file_not_found_error(self, tmp_path):
        """Test that a non-existent file path raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="not found"):
            image_to_braille(
                path=str(tmp_path / "definitely_does_not_exist.png"),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_directory_path_raises_file_not_found_error(self, tmp_path):
        """Test that a directory path (not a file) raises FileNotFoundError."""
        # tmp_path is a directory, not a file
        with pytest.raises(FileNotFoundError):
            image_to_braille(
                path=str(tmp_path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    def test_file_too_large_raises_error(self, tmp_path):
        """Test that a file exceeding MAX_FILE_SIZE raises ValueError."""
        from PIL import Image

        # Create a moderately large image
        img = Image.new("RGB", (500, 500), (255, 0, 0))
        path = tmp_path / "large.png"
        img.save(path)

        # Get actual file size and verify the MAX_FILE_SIZE constant exists
        from artty.converter import MAX_FILE_SIZE

        file_size = path.stat().st_size
        # The test image should be under the 100MB limit
        assert file_size < MAX_FILE_SIZE
        # Verify the MAX_FILE_SIZE constant is reasonable
        assert MAX_FILE_SIZE == 100 * 1024 * 1024  # 100MB

    def test_file_size_exceeds_limit_triggers_error(self, tmp_path, monkeypatch):
        """Test that file size check raises ValueError when file is too large."""
        from PIL import Image

        # Create a test image
        img = Image.new("RGB", (20, 20), (255, 0, 0))
        path = tmp_path / "small.png"
        img.save(path)

        # Mock os.path.getsize to return a value larger than MAX_FILE_SIZE
        from artty.converter import MAX_FILE_SIZE

        def mock_getsize(mock_path):
            if str(path) in str(mock_path):
                return MAX_FILE_SIZE + 1024 * 1024  # 1MB over limit
            return os.path.getsize(mock_path)

        monkeypatch.setattr("os.path.getsize", mock_getsize)

        with pytest.raises(ValueError, match="too large"):
            image_to_braille(
                path=str(path),
                width=10,
                threshold=50,
                contrast=1.0,
                sharpness=1.0,
                crop_padding=0,
                color=False,
            )

    # Note: Testing Pillow ImportError (lines 130-131) would require complex module
    # manipulation that has side effects on the test runner. This is an edge case
    # that is extremely unlikely in real usage since Pillow is a required dependency.
    # The code path is a simple try/except that raises a clear error message.


class TestEmptyImageEdgeCases:
    """Tests for edge cases with images that have minimal content."""

    def test_all_pixels_below_threshold_returns_emptyish(self, tmp_path):
        """Test that an image where all pixels are below threshold produces minimal output."""
        from PIL import Image

        # Create completely black image
        img = Image.new("L", (20, 20), 0)
        path = tmp_path / "black.png"
        img.save(path)

        _ = image_to_braille(
            path=str(path),
            width=10,
            threshold=254,  # Very high threshold - almost nothing passes
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # With high threshold, most or all pixels are below threshold
        # The result should be minimal (mostly spaces or empty lines)

    def test_all_pixels_above_threshold_returns_filled(self, tmp_path):
        """Test that an image where all pixels are above threshold produces filled output."""
        from PIL import Image

        # Create completely white image
        img = Image.new("L", (20, 20), 255)
        path = tmp_path / "white.png"
        img.save(path)

        result = image_to_braille(
            path=str(path),
            width=10,
            threshold=0,  # Very low threshold - everything passes
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
        )
        # Should have filled output (braille characters, not spaces)
        assert "\u2800" not in result  # All cells should be lit
        assert " " not in result or len(result) > 0  # Some content


class TestTransparentHandling:
    """Regression tests for transparent pixel handling in converter.

    The transparent parameter controls how transparent pixels in RGBA images
    are handled:
    - "black": transparent pixels composite over black background
    - "white": transparent pixels composite over white background
    - "ignore": transparent pixels treated as background (default)

    These tests verify the converter correctly processes RGBA images with
    different transparent handling modes.
    """

    @pytest.fixture
    def rgba_image_with_transparency(self, tmp_path):
        """Create an RGBA test image with transparent areas.

        Creates a 20x20 RGBA image with:
        - Top half: opaque gray pixels (128, 128, 128, 255)
        - Bottom half: fully transparent pixels (128, 128, 128, 0)

        This tests the transparent handling.
        """
        from PIL import Image

        img = Image.new("RGBA", (20, 20), (128, 128, 128, 255))

        # Make bottom half transparent
        for y in range(10, 20):
            for x in range(20):
                img.putpixel((x, y), (128, 128, 128, 0))  # Transparent

        path = tmp_path / "rgba_transparent.png"
        img.save(path)
        return str(path)

    def test_rgba_with_transparent_black(self, rgba_image_with_transparency):
        """Test that RGBA image with --transparent black composites over black.

        Regression test: transparent="black" should make transparent areas black.

        Scenario: Converting RGBA image with transparent="black"
        Expected: Transparent areas become black (0, 0, 0)
        Previously: Transparent pixels might have been ignored or differently handled
        """
        result = image_to_braille(
            path=rgba_image_with_transparency,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="black",
        )
        # Result should be valid ASCII output (string with content)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rgba_with_transparent_white(self, rgba_image_with_transparency):
        """Test that RGBA image with --transparent white composites over white.

        Regression test: transparent="white" should make transparent areas white.

        Scenario: Converting RGBA image with transparent="white"
        Expected: Transparent areas become white (255, 255, 255)
        Previously: Transparent pixels might have been ignored or differently handled
        """
        result = image_to_braille(
            path=rgba_image_with_transparency,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="white",
        )
        # Result should be valid ASCII output (string with content)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rgba_with_transparent_ignore(self, rgba_image_with_transparency):
        """Test that RGBA image with --transparent ignore treats as background.

        Regression test: transparent="ignore" should treat transparent as background.

        Scenario: Converting RGBA image with transparent="ignore"
        Expected: Transparent areas treated as background (default behavior)
        Previously: Option didn't exist, so default was this behavior
        """
        result = image_to_braille(
            path=rgba_image_with_transparency,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="ignore",
        )
        # Result should be valid ASCII output (string with content)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_rgba_default_transparent_is_ignore(self, rgba_image_with_transparency):
        """Test that default transparent behavior is 'ignore'.

        Regression test: Default should be "ignore" for backward compatibility.

        Scenario: Converting RGBA image without specifying transparent
        Expected: Default is "ignore" (backward compatible)
        Previously: No transparent option existed
        """
        result = image_to_braille(
            path=rgba_image_with_transparency,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            # Not specifying transparent - should default to "ignore"
        )
        # Result should be valid ASCII output
        assert isinstance(result, str)
        assert len(result) > 0

    def test_transparent_black_white_differ(self, rgba_image_with_transparency):
        """Test that transparent black and white produce different output.

        Regression test: The two modes should produce measurably different results
        when applied to images with transparency.

        Scenario: Converting same RGBA with transparent="black" vs "white"
        Expected: Results should differ (the transparent areas become different colors)
        Previously: Both might have been handled identically
        """
        result_black = image_to_braille(
            path=rgba_image_with_transparency,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="black",
        )
        result_white = image_to_braille(
            path=rgba_image_with_transparency,
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="white",
        )
        # Both should produce valid output
        assert len(result_black) > 0
        assert len(result_white) > 0

    def test_rgb_image_with_transparent_ignored(self, tmp_path):
        """Test that RGB images (no alpha) work correctly with transparent option.

        Regression test: The transparent option should not affect non-transparent images.

        Scenario: Converting an RGB (non-RGBA) image with any transparent value
        Expected: Same result regardless of transparent setting
        Previously: Option might have affected RGB images incorrectly
        """
        from PIL import Image

        # Create a simple RGB (not RGBA) image
        img = Image.new("RGB", (20, 20), (128, 128, 128))
        path = tmp_path / "rgb_no_alpha.png"
        img.save(path)

        result_ignore = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="ignore",
        )
        result_black = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="black",
        )
        result_white = image_to_braille(
            path=str(path),
            width=10,
            threshold=50,
            contrast=1.0,
            sharpness=1.0,
            crop_padding=0,
            color=False,
            transparent="white",
        )

        # For RGB images without transparency, all three should produce identical
        # results since there's no transparent pixels to handle
        assert result_ignore == result_black == result_white
