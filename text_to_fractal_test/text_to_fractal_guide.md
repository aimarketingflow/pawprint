# Text-to-Fractal Feature Guide
**AIMF LLC - Pawprinting PyQt6 Application**  
*Last Updated: June 2, 2025*

## Overview

The Text-to-Fractal feature allows you to generate unique fractal patterns based on text input. This guide will help you understand how to use this powerful feature in the Pawprinting PyQt6 application.

## Quick Start Guide

1. **Launch the application**
   ```bash
   cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6
   python3 main.py
   ```

2. **Navigate to the Fractal Butterfly screen**
   Click on "Fractal Butterfly" in the navigation menu.

3. **Select a pawprint file**
   - Click "Browse" and choose either:
     - "Browse for File" to select your own pawprint file
     - "Use Default Pawprint" to use the built-in demo pawprint

4. **Enter text for parameter generation**
   - Type your text in the Text Input box (up to 2000 characters)
   - If you leave it empty, you'll be offered the default AIMF LLC pawprinting text

5. **Generate parameters**
   - Click "Generate Parameters" to create unique fractal settings based on your text
   - The generated parameters will automatically update in the Parameter Widget

6. **Generate the fractal visualization**
   - Click the highlighted "Generate Fractal Butterfly" button
   - Watch as your text-influenced fractal visualization appears!

7. **Export your visualization**
   - Click "Export Image" to save your unique text-based fractal

## Understanding Text Influence

The text you enter influences the fractal in the following ways:

- **Fractal Dimension:** Determined by text complexity and length
- **Wing Ratio:** Influenced by word frequency patterns
- **Symmetry:** Affected by text structure and balance
- **Density:** Based on punctuation and whitespace distribution
- **Base Fractal Pattern:** Selected based on text entropy analysis
- **Color Scheme:** Derived from emotional content analysis

## Tips for Unique Results

- **Use varied text:** Mix short and long sentences
- **Include technical terms:** Specialized vocabulary creates distinctive patterns
- **Try different languages:** Each language produces different entropy profiles
- **Use emotional content:** Text with strong emotional content affects color schemes
- **Try poetry vs. prose:** Different text structures yield different symmetry patterns

## Command-Line Demonstration

For quick demonstrations without using the GUI:

```bash
cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/text_to_fractal_test
./run_text_to_fractal_demo.sh
```

Add the following to your `~/.zshrc` for easy access:

```bash
alias text2fractal='cd ~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/text_to_fractal_test && ./run_text_to_fractal_demo.sh'
```

## Troubleshooting

- **No visuals appear:** Ensure both text parameters AND pawprint data are loaded
- **Generate button disabled:** You need both text parameters and a pawprint file
- **Error during generation:** Use the "Retry Generation" button that appears
- **Parameters not updating:** Click "Generate Parameters" again after changing text

## Additional Information

The text-to-fractal feature creates a deterministic mapping between text content and fractal parameters, ensuring that the same text will always generate the same fractal pattern when combined with the same pawprint data.

For advanced usage, explore the parameter widget to manually fine-tune any parameters after text generation.
