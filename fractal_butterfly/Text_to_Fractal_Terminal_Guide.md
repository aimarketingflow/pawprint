# Text to Fractal Terminal Guide

## Setup and Environment Activation

```bash
# Navigate to the project directory
cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6

# Activate the virtual environment
source fractal_butterfly_venv/bin/activate

# Run the application
python3 pawprint_pyqt6_main.py
```

## Command Line Options

The application can be run with various command line options:

```bash
# Run with a specific pawprint file
python3 pawprint_pyqt6_main.py --file /path/to/pawprint.csv

# Run with debug logging
python3 pawprint_pyqt6_main.py --debug

# Open directly to the fractal butterfly screen
python3 pawprint_pyqt6_main.py --screen fractal_butterfly

# Load a saved text-fractal configuration
python3 pawprint_pyqt6_main.py --load-config "config_name"
```

## Useful Aliases

Add these aliases to your `.zshrc` or `.bash_profile` for quick access:

```bash
# Run the Pawprinting PyQt6 application
alias run_pawprint='cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6 && source fractal_butterfly_venv/bin/activate && python3 pawprint_pyqt6_main.py'

# Run with direct access to the fractal butterfly screen
alias run_fractals='cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6 && source fractal_butterfly_venv/bin/activate && python3 pawprint_pyqt6_main.py --screen fractal_butterfly'

# Run with a specific pawprint file
alias analyze_pawprint='cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6 && source fractal_butterfly_venv/bin/activate && python3 pawprint_pyqt6_main.py --file'
# Usage: analyze_pawprint /path/to/pawprint.csv
```

## Troubleshooting Commands

```bash
# Check PyQt6 installation
python3 -c "import PyQt6; print(PyQt6.__version__)"

# Update dependencies
pip3 install -r requirements_fractal_butterfly_venv.txt

# Repair virtual environment if needed
deactivate
rm -rf fractal_butterfly_venv
python3 -m venv fractal_butterfly_venv
source fractal_butterfly_venv/bin/activate
pip3 install -r requirements_fractal_butterfly_venv.txt
```

## Managing Configurations

```bash
# List all saved configurations
python3 -c "from fractal_butterfly.text_to_fractal import TextToFractalConverter; converter = TextToFractalConverter(); configs = converter.list_configurations(); [print(f\"{i+1}. {c['name']} - {c['created_at']}\") for i, c in enumerate(configs)]"

# Delete a configuration file
rm ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/configs/configuration_name.json
```

## Testing Text-to-Fractal Algorithm

```bash
# Test the text-to-fractal conversion with sample text
python3 -c "from fractal_butterfly.text_to_fractal import TextToFractalConverter; converter = TextToFractalConverter(); params = converter.text_to_parameters('Sample text for testing'); print(f'Fractal dimension: {params[\"fractal_dimension\"]}, Base pattern: {params[\"base_fractal_pattern\"]}')"
```

This terminal guide provides quick access to the most common commands needed for working with the Text-to-Fractal feature.
