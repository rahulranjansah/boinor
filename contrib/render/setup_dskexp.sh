#!/usr/bin/env bash
#
# setup_dskexp.sh
#
# Author: Rahul R. Sah
# Email: f1rahulranjan@gmail.com
#
# Description:
#   This script downloads and installs DSKEXP, a command-line utility from
#   NASA's SPICE Toolkit that exports data from DSK (Digital Shape Kernel)
#   files to various text formats. DSKEXP enables users to transform DSK files
#   into formats required by other applications and makes it easy to inspect
#   the data in a DSK file.
#
#   DSKEXP currently supports type 2 (plate model) DSK segments and can export
#   to multiple formats including:
#   - Plate-vertex table (MKDSK format code 1)
#   - Vertex-facet table / OBJ format (MKDSK format code 3)
#   - Rosetta/OSIRIS VER format (MKDSK format code 4)
#
# Reference:
#   DSKEXP User's Guide: https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/ug/dskexp.html


set -euo pipefail

# Supported platforms (all available from NAIF):
#   - Linux x86_64
#   - macOS x86_64 (Intel, works on Apple Silicon via Rosetta)
#   - Windows x86_64 (via Git Bash/MSYS2/WSL)

get_platform() {
    case "$(uname -s)" in
        Linux*)               echo "linux" ;;
        Darwin*)              echo "macos" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)                    echo "unknown" ;;
    esac
}

PLATFORM=$(get_platform)

case "$PLATFORM" in
    linux|macos)
        URL_BASE="https://naif.jpl.nasa.gov/pub/naif/utilities"
        if [[ "$PLATFORM" == "linux" ]]; then
            URL="$URL_BASE/PC_Linux_64bit/dskexp"
        else
            URL="$URL_BASE/MacIntel_OSX_64bit/dskexp"
        fi
        BIN="dskexp"
        INSTALL_DIR="$HOME/.local/bin"
        ;;
    windows)
        URL="https://naif.jpl.nasa.gov/pub/naif/utilities/PC_Windows_64bit/dskexp.exe"
        BIN="dskexp.exe"
        INSTALL_DIR="$LOCALAPPDATA/bin"
        ;;
    *)
        echo "Error: Unsupported platform '$(uname -s)'" >&2
        exit 1
        ;;
esac

INSTALL_PATH="$INSTALL_DIR/$BIN"

# Create install directory if needed
mkdir -p "$INSTALL_DIR"

if [[ -x "$INSTALL_PATH" ]]; then
    echo "dskexp already installed at $INSTALL_PATH"
    exit 0
fi

if ! command -v curl &>/dev/null; then
    echo "Error: curl is required" >&2
    exit 1
fi

echo "Downloading dskexp for $PLATFORM..."
curl -fSL "$URL" -o "$INSTALL_PATH"
chmod +x "$INSTALL_PATH"

echo "Installed to: $INSTALL_PATH"

# Check if install dir is in PATH
if ! echo "$PATH" | tr ':' '\n' | grep -qx "$INSTALL_DIR"; then
    echo ""
    echo "Warning: $INSTALL_DIR is not in your PATH"
    echo "Add this to your shell config:"
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
fi

echo "Done"