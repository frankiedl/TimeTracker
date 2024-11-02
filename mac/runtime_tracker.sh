#!/bin/bash
# Change to the directory where the script is located
cd "$(dirname "$0")"

# Check and install pandas and openpyxl if they are not present
if ! python3 -m pip show pandas > /dev/null 2>&1; then
    echo "Installing pandas..."
    python3 -m pip install pandas
fi

if ! python3 -m pip show openpyxl > /dev/null 2>&1; then
    echo "Installing openpyxl..."
    python3 -m pip install openpyxl
fi

# Run the Python script
python3 time_tracker.py
