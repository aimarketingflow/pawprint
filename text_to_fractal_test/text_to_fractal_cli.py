#!/usr/bin/env python3
"""
Text-to-Fractal Quick Start CLI
Automates the process of generating and visualizing text-based fractals.
"""

import os
import sys
import time
import json
import logging
import argparse
from datetime import datetime
import shutil

# Add parent directory to path to import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'text_to_fractal_cli_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('text_to_fractal_cli')

# Constants
CONFIG_DIR = os.path.expanduser('~/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/configs')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

class TextToFractalCLI:
    """Command line interface for the Text-to-Fractal feature"""
    
    def __init__(self):
        self.progress = 0
        self.start_time = None
        self.sample_text = None
        self.pawprint_path = None
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
    def update_progress(self, increment, message):
        """Update progress with time estimate"""
        self.progress += increment
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        # Calculate estimated time remaining
        if self.progress > 0 and elapsed > 0:
            estimated_total = elapsed / (self.progress / 100)
            remaining = max(0, estimated_total - elapsed)
            remaining_str = time.strftime("%H:%M:%S", time.gmtime(remaining))
        else:
            remaining_str = "Unknown"
        
        logger.info(f"[{self.progress:.1f}%] {message} (ETA: {remaining_str})")
        print(f"\r[{'#' * int(self.progress/2)}{' ' * (50 - int(self.progress/2))}] {self.progress:.1f}% - {message} (ETA: {remaining_str})", end='')
        sys.stdout.flush()
    
    def load_sample_text(self, text_file=None):
        """Load sample text from file or use default"""
        self.update_progress(5, "Loading sample text...")
        
        if text_file and os.path.exists(text_file):
            try:
                with open(text_file, 'r') as f:
                    self.sample_text = f.read()
                    logger.info(f"Loaded sample text from {text_file}: {len(self.sample_text)} characters")
            except Exception as e:
                logger.error(f"Error loading text file: {e}")
                self.sample_text = None
        
        # Use default text if no file or loading failed
        if not self.sample_text:
            self.sample_text = """
            The butterfly effect is the concept that small changes can have large effects.
            Initially, it was used with weather prediction but later became a metaphor for 
            how small events can lead to significant changes in complex systems. The term comes
            from the suggestion that the flapping of a butterfly's wings in Brazil might 
            eventually cause a tornado in Texas.
            
            In chaos theory, this behavior is seen in systems where a small change in initial
            conditions can lead to vastly different outcomes, making prediction impossible
            beyond a certain time horizon. The butterfly effect is a poetic way to describe
            this mathematical concept - that in a complex and interconnected world, small actions
            can ripple outward to create massive transformations.
            """
            logger.info(f"Using default sample text: {len(self.sample_text)} characters")
        
        return self.sample_text
    
    def find_pawprint_file(self, file_path=None):
        """Find a pawprint file to use for visualization"""
        self.update_progress(10, "Finding pawprint file...")
        
        # Use provided file if it exists
        if file_path and os.path.exists(file_path):
            self.pawprint_path = file_path
            logger.info(f"Using provided pawprint file: {file_path}")
            return self.pawprint_path
        
        # Look for existing pawprint in common locations
        common_locations = [
            "/Users/flowgirl/Documents/CrashAnalyzer_pawprint.json",
            "/Users/flowgirl/Documents/FolderHackingAnalysis/Pawprinting_PyQt6/examples/sample_pawprint.json",
            "/Users/flowgirl/Documents"
        ]
        
        for location in common_locations:
            if os.path.isdir(location):
                # Search for .json files that might be pawprints
                for file in os.listdir(location):
                    if file.endswith('.json') and ('pawprint' in file.lower() or 'paw' in file.lower()):
                        self.pawprint_path = os.path.join(location, file)
                        logger.info(f"Found pawprint file: {self.pawprint_path}")
                        return self.pawprint_path
            elif os.path.isfile(location) and location.endswith('.json'):
                self.pawprint_path = location
                logger.info(f"Using pawprint file: {self.pawprint_path}")
                return self.pawprint_path
        
        logger.error("No pawprint file found. Visualization will not be possible.")
        return None
    
    def generate_fractal_parameters(self):
        """Generate fractal parameters from text"""
        self.update_progress(20, "Generating fractal parameters from text...")
        
        try:
            # Import converter module
            from fractal_butterfly.text_to_fractal import TextToFractalConverter
            
            # Create converter and generate parameters
            converter = TextToFractalConverter()
            params = converter.text_to_parameters(self.sample_text)
            
            # Save parameters to config file
            config_name = f"demo_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            config_path = converter.save_configuration(params, config_name)
            
            # Save parameters to output dir as well
            output_params_path = os.path.join(OUTPUT_DIR, f"{config_name}.json")
            with open(output_params_path, 'w') as f:
                json.dump(params, f, indent=2)
            
            self.update_progress(40, f"Parameters generated and saved to {output_params_path}")
            
            # Print key parameters
            logger.info(f"Generated parameters: Dimension={params['fractal_dimension']}, " 
                       f"Pattern={params['base_fractal_pattern']}, Symmetry={params['symmetry']}")
            
            return params, config_path
            
        except Exception as e:
            logger.error(f"Error generating fractal parameters: {e}")
            raise
    
    def generate_fractal_visualization(self, params):
        """Generate and save fractal visualization using the provided parameters"""
        self.update_progress(50, "Generating fractal visualization...")
        
        if not self.pawprint_path:
            logger.error("Cannot generate visualization without a pawprint file")
            return None
        
        try:
            # Import fractal generator
            from fractal_butterfly.fractal_generator import FractalGenerator
            from fractal_butterfly.fractal_renderer import FractalRenderer
            
            # Create generator and renderer
            generator = FractalGenerator()
            renderer = FractalRenderer()
            
            # Load pawprint data
            self.update_progress(60, "Loading pawprint data...")
            with open(self.pawprint_path, 'r') as f:
                pawprint_data = json.load(f)
            
            # Set parameters and generate fractal
            generator.set_parameters(params)
            
            # Generate base fractal if needed
            base_fractal = None
            if params.get("use_base_fractal", False):
                self.update_progress(70, f"Generating base fractal: {params['base_fractal_pattern']}...")
                base_pattern = params["base_fractal_pattern"]
                resolution = params["resolution"]
                base_fractal = generator._get_base_fractal(base_pattern, resolution)
            
            # Generate butterfly fractal
            self.update_progress(80, "Generating fractal butterfly...")
            fractal_data, colors = generator.generate_butterfly()
            
            # Render visualization
            self.update_progress(90, "Rendering visualization...")
            output_img_path = os.path.join(OUTPUT_DIR, f"fractal_butterfly_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            # Configure renderer options
            renderer_options = {
                "show_base_pattern": params.get("use_base_fractal", False) and base_fractal is not None,
                "title": f"Fractal Butterfly Pattern - Dimension {params['fractal_dimension']:.2f}"
            }
            renderer.set_options(renderer_options)
            
            # Render and save
            if base_fractal is not None and params.get("use_base_fractal", False):
                # Render with base fractal comparison
                fig = renderer.render_fractal(
                    fractal_data, colors, metrics=None, base_fractal=base_fractal
                )
            else:
                # Standard rendering
                fig = renderer.render_fractal(fractal_data, colors)
                
            # Save figure
            fig.savefig(output_img_path, dpi=300, bbox_inches='tight')
            logger.info(f"Saved fractal visualization to {output_img_path}")
            
            # Open image in default viewer
            self.update_progress(95, "Opening visualization...")
            self.open_file(output_img_path)
            
            return output_img_path
            
        except Exception as e:
            logger.error(f"Error generating fractal visualization: {e}")
            raise
    
    def open_file(self, file_path):
        """Open a file with the default application"""
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":  # macOS
                os.system(f"open {file_path}")
            else:  # linux
                os.system(f"xdg-open {file_path}")
            logger.info(f"Opened file: {file_path}")
        except Exception as e:
            logger.error(f"Error opening file: {e}")
    
    def copy_logs_to_output(self):
        """Copy log file to output directory for easy access"""
        try:
            log_output = os.path.join(OUTPUT_DIR, os.path.basename(log_file))
            shutil.copy2(log_file, log_output)
            logger.info(f"Copied log to output directory: {log_output}")
        except Exception as e:
            logger.error(f"Error copying log file: {e}")
    
    def run(self, text_file=None, pawprint_file=None, open_output=True):
        """Run the complete workflow"""
        self.start_time = time.time()
        self.progress = 0
        success = False
        
        try:
            logger.info(f"Started Text-to-Fractal demonstration at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Step 1: Load sample text
            self.load_sample_text(text_file)
            
            # Step 2: Find pawprint file
            self.find_pawprint_file(pawprint_file)
            
            # Step 3: Generate fractal parameters
            params, config_path = self.generate_fractal_parameters()
            
            # Step 4: Generate visualization
            if self.pawprint_path:
                output_img_path = self.generate_fractal_visualization(params)
                
                # Step 5: Open output directory
                if open_output and output_img_path:
                    self.open_file(OUTPUT_DIR)
            
            success = True
            total_time = time.time() - self.start_time
            self.update_progress(100, f"Completed successfully in {time.strftime('%H:%M:%S', time.gmtime(total_time))}")
            print()  # New line after progress bar
            
            # Copy log to output
            self.copy_logs_to_output()
            
            return success
            
        except Exception as e:
            total_time = time.time() - self.start_time
            logger.error(f"Failed after {time.strftime('%H:%M:%S', time.gmtime(total_time))}: {str(e)}")
            print(f"\nError: {str(e)}")
            
            # Copy log to output even on failure
            self.copy_logs_to_output()
            
            return False

def main():
    """Parse arguments and run the CLI"""
    parser = argparse.ArgumentParser(description='Text-to-Fractal Quick Start Tool')
    parser.add_argument('--text', type=str, help='Path to a text file to use for fractal generation')
    parser.add_argument('--pawprint', type=str, help='Path to a pawprint file for visualization')
    parser.add_argument('--no-open', action='store_true', help='Do not automatically open output files')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
    
    # Run the CLI
    cli = TextToFractalCLI()
    success = cli.run(
        text_file=args.text,
        pawprint_file=args.pawprint,
        open_output=not args.no_open
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
