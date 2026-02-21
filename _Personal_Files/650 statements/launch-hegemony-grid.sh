#!/bin/bash
# v4 Psochic Hegemony Grid Launcher (Mac/Linux)
# Launches the standalone HTML file in your default browser

echo "========================================"
echo " v4 Psochic Hegemony Grid Launcher"
echo " 650 Political Spectrum Statements"
echo "========================================"
echo ""
echo "Opening grid in your default browser..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Detect OS and use appropriate command
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$SCRIPT_DIR/v4_Hegemony-Grid_650-Statements_COMPLETE.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$SCRIPT_DIR/v4_Hegemony-Grid_650-Statements_COMPLETE.html"
else
    echo "Unknown OS. Please open v4_Hegemony-Grid_650-Statements_COMPLETE.html manually."
    exit 1
fi

echo ""
echo "Grid launched successfully!"
echo "Close this terminal when done."
echo ""
