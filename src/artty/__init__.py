"""ArTTY - Convert images to braille ASCII art."""

from importlib.metadata import version

__version__ = version("artty")
__author__ = "divisionseven"
__email__ = "dev@divisionseven.com"
__license__ = "MIT"

from artty.converter import image_to_braille

__all__ = [
    "__version__",
    "image_to_braille",
]
