#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$SCRIPT_DIR"

TARGET="${1:-.}"

echo "Running Black on $TARGET..."
./myvenv/bin/black "$TARGET"

echo "Running Isort on $TARGET..."
./myvenv/bin/isort "$TARGET"

echo "Running Linter (Flake8) on $TARGET..."
echo "Pass 1: Critical errors"
./myvenv/bin/flake8 "$TARGET" --count --select=E9,F63,F7,F82 --show-source --statistics

echo "Pass 2: Style and complexity"
./myvenv/bin/flake8 "$TARGET" --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

if [ "$TARGET" == "." ]; then
    echo "Running Tests..."
    ./myvenv/bin/pytest
else
    echo "Skipping tests for single file formatting."
fi

echo "All checks and formatting completed successfully!"
