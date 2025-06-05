#!/usr/bin/env python3
"""
Export Manager Module

Handles exporting fractal butterfly patterns in various formats.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import json
import logging
import numpy as np
from typing import Dict, Any, Optional
from datetime import datetime
from matplotlib.figure import Figure

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.export")

class ExportManager:
    """
    Class for exporting fractal butterfly patterns and metrics
    """
    
    def __init__(self):
        """Initialize the export manager"""
        pass
    
    def export_image(self, fig: Figure, output_path: str, dpi: int = 300) -> bool:
        """
        Export fractal as image
        
        Args:
            fig: Matplotlib Figure object
            output_path: Path to save the image
            dpi: DPI for saving (dots per inch)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Save figure
            fig.savefig(output_path, dpi=dpi)
            logger.info(f"Exported fractal image to {output_path} at {dpi} DPI")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting fractal image: {e}")
            return False
    
    def export_data(self, fractal_data: np.ndarray, metrics: Dict[str, Any], 
                  params: Dict[str, Any], output_path: str) -> bool:
        """
        Export fractal data and metrics as JSON
        
        Args:
            fractal_data: Numpy array containing fractal data
            metrics: Dictionary of calculated metrics
            params: Dictionary of generation parameters
            output_path: Path to save the data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Prepare data
            # We can't directly serialize numpy arrays to JSON, so convert to list
            # For large arrays, we'll save a downsampled version
            h, w = fractal_data.shape
            downsample = max(1, min(h, w) // 200)  # Limit to ~200x200 for JSON
            
            data_export = {
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "original_dimensions": [h, w],
                    "downsampled": downsample > 1,
                    "downsampling_factor": downsample
                },
                "parameters": params,
                "metrics": metrics,
                "data_sample": fractal_data[::downsample, ::downsample].tolist()
            }
            
            # Save as JSON
            with open(output_path, 'w') as f:
                json.dump(data_export, f, indent=2)
                
            logger.info(f"Exported fractal data to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting fractal data: {e}")
            return False
    
    def export_report(self, fractal_data: np.ndarray, metrics: Dict[str, Any],
                     params: Dict[str, Any], image_path: str, output_path: str) -> bool:
        """
        Export a detailed HTML report
        
        Args:
            fractal_data: Numpy array containing fractal data
            metrics: Dictionary of calculated metrics
            params: Dictionary of generation parameters
            image_path: Path to the saved image file
            output_path: Path to save the HTML report
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Get image filename for embedding
            image_filename = os.path.basename(image_path)
            
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Fractal Butterfly Report</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    h1, h2 {{ color: #2c3e50; }}
                    .container {{ max-width: 1200px; margin: 0 auto; }}
                    .image-container {{ text-align: center; margin: 20px 0; }}
                    .image-container img {{ max-width: 100%; border: 1px solid #ddd; }}
                    .metrics-container {{ display: flex; flex-wrap: wrap; }}
                    .metric-box {{ 
                        border: 1px solid #ddd; border-radius: 4px; padding: 10px; 
                        margin: 10px; flex: 1; min-width: 200px; background-color: #f9f9f9; 
                    }}
                    .parameters {{ 
                        background-color: #eef7fa; padding: 15px;
                        border-radius: 4px; margin-top: 20px;
                    }}
                    table {{ width: 100%; border-collapse: collapse; }}
                    th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                    th {{ background-color: #f2f2f2; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Fractal Butterfly Analysis Report</h1>
                    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    
                    <div class="image-container">
                        <img src="{image_filename}" alt="Fractal Butterfly Pattern">
                    </div>
                    
                    <h2>Fractal Metrics</h2>
                    <div class="metrics-container">
            """
            
            # Add metrics
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)
                    html_content += f"""
                        <div class="metric-box">
                            <h3>{key.replace('_', ' ').title()}</h3>
                            <p>{formatted_value}</p>
                        </div>
                    """
            
            # Add parameters section
            html_content += """
                    </div>
                    
                    <h2>Generation Parameters</h2>
                    <div class="parameters">
                        <table>
                            <tr>
                                <th>Parameter</th>
                                <th>Value</th>
                            </tr>
            """
            
            # Add parameters
            for key, value in params.items():
                html_content += f"""
                            <tr>
                                <td>{key.replace('_', ' ').title()}</td>
                                <td>{value}</td>
                            </tr>
                """
            
            # Close HTML
            html_content += """
                        </table>
                    </div>
                    
                    <div class="footer" style="margin-top: 30px; text-align: center; color: #777;">
                        <p>Pawprinting Analysis Tool - Fractal Butterfly Module</p>
                        <p>© 2025 AIMF LLC. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Write HTML file
            with open(output_path, 'w') as f:
                f.write(html_content)
                
            logger.info(f"Exported HTML report to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting HTML report: {e}")
            return False
