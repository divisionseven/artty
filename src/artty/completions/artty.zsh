# artty Zsh Completion
# ===================
# Zsh completion script for artty CLI.
#
# Install by adding to your .zshrc:
#   fpath=(~/path/to/artty/completions $fpath)
#   autoload -U compinit && compinit
#
# Or copy to your completion directory:
#   mkdir -p ~/.zsh/completions
#   cp artty.zsh ~/.zsh/completions/_artty
#   Then add to .zshrc:
#   fpath=(~/.zsh/completions $fpath)
#   autoload -U compinit && compinit

# Image file extensions
local -a image_extensions=(
    "png:PNG image"
    "jpg:JPEG image"
    "jpeg:JPEG image"
    "gif:GIF image"
    "bmp:BMP image"
    "tiff:TIFF image"
    "webp:WebP image"
)

# Main command options with descriptions
local -a artty_options=(
    "-h[Show this help message]"
    "--help[Show this help message]"
    "-v[Show version information]"
    "--version[Show version information]"
    "-o:[Output file path or directory]"
    "--output::[Output file path or directory]"
    "-w:[Output width in characters (10-500)]"
    "--width::[Output width in characters (10-500)]"
    "-t:[Luminance threshold 0-255]"
    "--threshold::[Luminance threshold 0-255]"
    "--padding::[Pixels of padding around content]"
    "--contrast::[Contrast enhancement factor]"
    "--sharpness::[Sharpness enhancement factor]"
    "--color[Enable 24-bit ANSI color output]"
    "--no-color[Disable color output]"
    "--boost::[Color brightness multiplier (1.0-1.4)]"
    "--bg::[Background color as three integers (R G B)]"
    "--preview[Print result to terminal after saving]"
    "--no-preview[Only save to file, don't print]"
    "--no-save[Only print to stdout, don't save]"
    "--hide-paths[Show only filenames in output]"
)

# Subcommands (for future use)
local -a artty_subcommands=(
    "convert:Convert image to ASCII art"
    "info:Show image information"
    "demo:Run demo"
)

_artty() {
    local -a commands opts

    # Set up completion options
    opts=($artty_options)

    # First argument - complete subcommands or files
    if ((CURRENT == 1)); then
        # Add subcommands
        commands=(${artty_subcommands[*]})
        _describe "command" commands && return

        # Also complete image files
        _describe "file" image_extensions
        return
    fi

    # Get the first word (command or file)
    local first="$words[1]"

    # Handle options
    if [[ "$first" == -* ]]; then
        # First arg is an option, complete files
        _describe "file" image_extensions
        return
    fi

    # Complete options after command/file
    _describe "option" opts
}

# Register completion function
_artty "$@"