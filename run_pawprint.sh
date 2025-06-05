#!/bin/bash
# Pawprinting PyQt6 Launcher Script
# Launches the Pawprinting PyQt6 application with proper environment setup

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to script directory
cd "$SCRIPT_DIR" || { echo "Error: Could not change to script directory"; exit 1; }

# Activate virtual environment if it exists
VENV_DIR="$SCRIPT_DIR/venv_pawprinting_pyqt6"
if [ -d "$VENV_DIR" ]; then
  echo "Activating virtual environment..."
  source "$VENV_DIR/bin/activate" || { echo "Error: Could not activate virtual environment"; exit 1; }
else
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR" || { echo "Error: Could not create virtual environment"; exit 1; }
  source "$VENV_DIR/bin/activate" || { echo "Error: Could not activate virtual environment"; exit 1; }
  echo "Installing dependencies..."
  pip3 install -r requirements.txt || { echo "Error: Could not install dependencies"; exit 1; }
fi

# Run the application
echo "Starting Pawprinting PyQt6 application..."
python3 pawprint_pyqt6_main.py

# Deactivate virtual environment
deactivate

echo "Application closed"
