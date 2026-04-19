# artty Bash Completion
# ====================
# Bash completion script for artty CLI.
#
# Install by sourcing this file in your .bashrc:
#   source /path/to/artty/completions/artty.bash
#
# Or copy to completions directory:
#   cp artty.bash /etc/bash_completion.d/  # system-wide
#   mkdir -p ~/.bash_completion.d && cp artty.bash ~/.bash_completion.d/  # user

_artty() {
    local cur prev words cword
    _init_completion || return

    # Main command options
    local opts=(
        "-h:--help:Show this help message"
        "-v:--version:Show version information"
        "-o:--output:Output file path or directory"
        "-w:--width:Output width in characters (10-500)"
        "-t:--threshold:Luminance threshold 0-255"
        "--padding:Pixels of padding around content"
        "--contrast:Contrast enhancement factor"
        "--sharpness:Sharpness enhancement factor"
        "--color:Enable 24-bit ANSI color output"
        "--no-color:Disable color output"
        "--boost:Color brightness multiplier (1.0-1.4)"
        "--bg:Background color as three integers (R G B)"
        "--preview:Print result to terminal after saving"
        "--no-preview:Only save to file, don't print"
        "--no-save:Only print to stdout, don't save"
        "--hide-paths:Show only filenames in output"
    )

    # Subcommands (for future use if added)
    local subcommands="convert info demo"

    # Handle the first argument (subcommand or file)
    if [[ $cword -eq 1 ]]; then
        # Complete subcommands or input files
        case "$cur" in
            -*)
                COMPREPLY=($(compgen -W "${opts[*]}" -- "$cur"))
                ;;
            *)
                # Check if there's a partial subcommand match
                local subcmds
                subcmds=$(compgen -W "$subcommands" -- "$cur")
                if [[ -n "$subcmds" ]]; then
                    COMPREPLY=($subcmds)
                fi
                # Also complete files
                _filedir "@(png|jpg|jpeg|gif|bmp|tiff|webp)"
                ;;
        esac
        return 0
    fi

    # Second argument and beyond - complete options
    prev="${words[cword - 1]}"
    cur="${words[cword]}"

    # Options requiring arguments
    case "$prev" in
        -o|--output|-w|--width|-t|--threshold|--padding|--contrast|--sharpness|--boost|--bg)
            return 0
            ;;
        -h|--help|-v|--version)
            return 0
            ;;
    esac

    # Complete options
    if [[ "$cur" == -* ]]; then
        COMPREPLY=($(compgen -W "${opts[*]}" -- "$cur"))
        return 0
    fi

    # Default: complete files for arguments that need paths
    _filedir "@(png|jpg|jpeg|gif|bmp|tiff|webp)"
}

# Register completion function
complete -F _artty artty