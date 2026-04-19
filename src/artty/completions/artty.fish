# artty Fish Completion
# ==================
# Fish completion script for artty CLI.
#
# Install by copying to Fish completions directory:
#   cp artty.fish ~/.config/fish/completions/artty.fish
#
# Or link (for development):
#   ln -s (path/to/artty/completions/artty.fish) ~/.config/fish/completions/artty.fish

# Image file extensions
complete -c artty -f -a "png" -d "PNG image"
complete -c artty -f -a "jpg" -d "JPEG image"
complete -c artty -f -a "jpeg" -d "JPEG image"
complete -c artty -f -a "gif" -d "GIF image"
complete -c artty -f -a "bmp" -d "BMP image"
complete -c artty -f -a "tiff" -d "TIFF image"
complete -c artty -f -a "webp" -d "WebP image"

# Main command: artty (no subcommand completion since it's a single-command CLI)
# Just complete files for the main argument
complete -c artty -f -a "(__fish_complete_suffixes png jpg jpeg gif bmp tiff webp)" -d "Image file"

# Options with short and long forms
complete -c artty -n "__fish_use_minus" -s h -l help -d "Show this help message"
complete -c artty -n "__fish_use_minus" -s v -l version -d "Show version information"

# Output options
complete -c artty -n "__fish_use_minus" -s o -l output -d "Output file path or directory" -r
complete -c artty -n "__fish_use_minus" -s w -l width -d "Output width in characters (10-500)" -r

# Image processing options
complete -c artty -n "__fish_use_minus" -s t -l threshold -d "Luminance threshold 0-255" -r
complete -c artty -n "__fish_use_minus" -l padding -d "Pixels of padding around auto-detected content" -r
complete -c artty -n "__fish_use_minus" -l contrast -d "Contrast enhancement factor (default: 1.0)" -r
complete -c artty -n "__fish_use_minus" -l sharpness -d "Sharpness enhancement factor (default: 1.0)" -r

# Color options
complete -c artty -n "__fish_use_minus" -l color -d "Enable 24-bit ANSI color output"
complete -c artty -n "__fish_use_minus" -l no-color -d "Disable color output"
complete -c artty -n "__fish_use_minus" -l boost -d "Color brightness multiplier (1.0-1.4)" -r
complete -c artty -n "__fish_use_minus" -l bg -d "Background color as three integers (R G B)" -r

# Preview/save options
complete -c artty -n "__fish_use_minus" -l preview -d "Print result to terminal after saving"
complete -c artty -n "__fish_use_minus" -l no-preview -d "Only save to file, don't print"
complete -c artty -n "__fish_use_minus" -l no-save -d "Only print to stdout, don't save"
complete -c artty -n "__fish_use_minus" -l hide-paths -d "Show only filenames in output"

# Future subcommands (reserved for when/if they are added)
# complete -c artty -n "__fish_seen_subcommand_from convert" -a "convert" -d "Convert image to ASCII art"
# complete -c artty -n "__fish_seen_subcommand_from info" -a "info" -d "Show image information"
# complete -c artty -n "__fish_seen_subcommand_from demo" -a "demo" -d "Run demo"