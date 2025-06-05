# Text to Fractal Feature - Pawprinting PyQt6

## Overview

The Text-to-Fractal feature enhances the Pawprinting fractal butterfly visualization system by allowing users to input text (0-2000 characters) which generates a unique base fractal pattern. This base fractal is then used as the foundation for fractal butterfly analysis, applying a "butterfly effect" transformation.

## Security Implications

- Text acts as a key, enabling two-factor visualization with pawprint data
- Creates unique fractal patterns based on text content and structure
- Adds an additional layer of entropy to the visualization process

## Features

- **Text Input**: Enter up to 2000 characters to generate fractal parameters
- **Parameter Generation**: Text is analyzed for entropy, character distribution, and structure to generate unique fractal parameters
- **Save/Load Configurations**: Save generated parameters for later use
- **Integration with Fractal Butterfly**: Seamlessly use text-generated parameters for visualization

## Implementation Details

### Components

1. **TextToFractalConverter** (`text_to_fractal.py`)
   - Handles text analysis and parameter generation
   - Manages configuration save/load functionality
   - Creates consistent, reproducible parameters from the same text

2. **TextInputWidget** (`text_input_widget.py`)
   - Provides UI for text input
   - Manages character count display and validation
   - Includes buttons for generating parameters, saving, and loading configurations

### Parameter Generation

Text analysis includes:
- Entropy calculation
- Character distribution analysis
- Word and line count
- Special character ratio
- Text length consideration

Generated parameters include:
- Fractal dimension
- Wing ratio
- Symmetry
- Density
- Iterations
- Resolution
- Color scheme
- Base fractal pattern
- Base fractal influence

## Usage

1. Enter text in the text input field (0-2000 characters)
2. Click "Generate Parameters" to create a unique fractal parameter set
3. Load a pawprint file using the file browser
4. Click "Generate Fractal Butterfly" to visualize
5. Save configurations for later use with the "Save Configuration" button
6. Load previous configurations with the "Load Configuration" button

## Configuration Files

Configurations are saved as JSON files in `~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/configs/`.

Each configuration contains:
- Original text input
- All generated parameters
- Metadata (creation date, name)

## Technical Notes

- Requires PyQt6, numpy, matplotlib
- Configurations are backward and forward compatible
- Parameters are deterministic - the same text will always generate the same parameters
