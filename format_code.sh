#!/bin/bash
set -e

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Run from the project root
cd "$SCRIPT_DIR"

TARGET="${1:-.}"

echo "Running Black on $TARGET..."
./myvenv/bin/black "$TARGET"

echo "Running Isort on $TARGET..."
./myvenv/bin/isort "$TARGET"

echo "Running Linter (Flake8) on $TARGET..."
./myvenv/bin/flake8 "$TARGET"

if [ "$TARGET" == "." ]; then
    echo "Running Tests..."
    ./myvenv/bin/pytest
else
    echo "Skipping tests for single file formatting."
fi

echo "All checks and formatting completed successfully!"
