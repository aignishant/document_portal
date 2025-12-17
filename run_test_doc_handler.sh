#!/bin/bash

# Activate virtual environment
source myvenv/bin/activate

# Run the test
pytest tests/test_document_comparison_handler.py
