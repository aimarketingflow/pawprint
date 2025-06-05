# Pawprinting PyQt6 V2 - Diagrams

This directory contains diagram generators for the Pawprinting PyQt6 V2 application. These diagrams help visualize the data flow, architecture, and key processes within the application.

## Contents

- `pash_generation_diagram.py` - Generates a diagram showing the "Pash" (pawprint signature) generation flow

## Requirements

To run these diagram generators, you need:

1. Python 3.6+
2. The `diagrams` Python package (`pip3 install diagrams`)  
3. Graphviz (`brew install graphviz` on macOS)
4. Internet connectivity (first time only, for downloading component icons)

## Usage

### Generating the Pash Flow Diagram

```bash
cd /Users/flowgirl/Documents/FolderHackingAnalysis/Pawprinting_PyQt6_V2/diagrams
python3 ./pash_generation_diagram.py
```

This will create `pash_generation_flow.png` in the same directory.

## Troubleshooting

If you encounter errors about missing Graphviz:

```bash
brew install graphviz
```

If you see Python import errors:

```bash
pip3 install diagrams
```

## Output Examples

After running the diagram generators, you'll get image files such as:

- `pash_generation_flow.png` - Shows how text input is processed through the application to generate the "Pash" signature, which is then stored in configuration files and displayed in the UI.

The diagrams are rendered in the style similar to [diagrams.mingrammer.com](https://diagrams.mingrammer.com), with clean node organization and informative connection labels.
