#!/bin/bash

# upload_ai_common.sh

# Exit immediately if a command exits with a non-zero status
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PACKAGE_DIR="$SCRIPT_DIR/../ai-common"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
if ! command_exists python3; then
    echo "Error: python3 is not installed."
    exit 1
fi

if ! command_exists twine; then
    echo "Error: twine is not installed. Install it with: pip install twine"
    exit 1
fi

echo "Moving to package directory..."
if [ -d "$PACKAGE_DIR" ]; then
    cd "$PACKAGE_DIR"
elif [ -f "setup.py" ]; then
    # Already in the directory maybe?
    echo "Already in package directory or root... checking setup.py"
    if [ ! -f "setup.py" ]; then
        echo "Error: setup.py not found in current directory and could not find '$PACKAGE_DIR'"
        exit 1
    fi
else
    echo "Error: Directory '$PACKAGE_DIR' not found."
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

# Build the package
echo "Building package..."
python3 setup.py sdist bdist_wheel

# Check if dist directory exists
if [ ! -d "dist" ]; then
    echo "Error: Build failed, 'dist' directory not created."
    exit 1
fi

# Upload to PyPI
echo "Uploading to PyPI..."
# Note: You might need to configure .pypirc or provide credentials interactively
twine upload dist/*

echo "Successfully uploaded ai-common to PyPI!"
