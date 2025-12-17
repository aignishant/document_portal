#!/bin/bash

# Check if gnome-screenshot is installed
if ! command -v gnome-screenshot &> /dev/null
then
    echo "Error: gnome-screenshot is not installed."
    echo "Please install it using: sudo apt-get install gnome-screenshot"
    exit 1
fi

echo "gnome-screenshot is installed."

# Install python-docx
echo "Installing python-docx..."
pip install python-docx

echo "-----------------------------------"
echo "Setup complete. You can now run the screenshot tool:"
echo "python3 screenshot_to_doc.py"
