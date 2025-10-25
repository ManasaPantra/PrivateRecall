#!/bin/bash

# Navigate to the project root (if you're not already there)
cd "$(dirname "$0")"

# Ensure Python can import top-level packages (e.g., models/)
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run Streamlit app
streamlit run app/main.py
