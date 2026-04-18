#!/bin/zsh
# Extract changelog section for a specific version
# Usage: ./scripts/extract_changelog.sh VERSION
# Example: ./scripts/extract_changelog.sh 0.1.2

VERSION="${1:-}"
if [ -z "$VERSION" ]; then
    echo "Usage: $0 VERSION" >&2
    exit 1
fi

# Extract section from CHANGELOG.md matching "## [VERSION] - YYYY-MM-DD"
# up to the next "## [" section or end of file
# Using grep -A to get lines after match, and a second grep to stop at next section
awk -v version="$VERSION" '
    $0 ~ "## \\[" version "\\]" { found=1; next }
    found && $0 ~ "^## \\[" { found=0 }
    found { print }
' CHANGELOG.md