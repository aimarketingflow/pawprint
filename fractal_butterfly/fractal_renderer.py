#!/usr/bin/env python3
"""
Fractal Renderer Module

Renders fractal butterfly patterns using matplotlib.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from typing import Dict, Any, Tuple, List, Optional

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.renderer")

class FractalRenderer:
    """
    Renderer for fractal butterfly patterns
    """
    
    def __init__(self):
        """Initialize the fractal renderer"""
        # Default options
        self.options = {
            "dpi": 100,
            "cmap_name": "fractal_butterfly",
            "show_axes": True,
            "show_colorbar": True,
            "show_metrics": True,
            "title": "Fractal Butterfly Pattern",
            "overlay_grid": True,
            "show_base_pattern": False
        }
    
    def set_options(self, options: Dict[str, Any]) -> None:
        """
        Set rendering options
        
        Args:
            options: Dictionary of options
        """
        self.options.update(options)
        logger.debug(f"Renderer options updated: {options}")
    
    def render_fractal(self, 
                      fractal_data: np.ndarray, 
                      colors: List[Tuple[float, float, float]], 
                      figure: Optional[Figure] = None,
                      metrics: Optional[Dict[str, Any]] = None,
                      base_fractal: Optional[np.ndarray] = None) -> Figure:
        """
        Render fractal data to a figure
        
        Args:
            fractal_data: Numpy array containing fractal data
            colors: List of RGB color tuples for colormap
            figure: Optional figure to render to (creates new if None)
            metrics: Optional dictionary of metrics to display
            base_fractal: Optional base fractal data for comparison
            
        Returns:
            Matplotlib figure with rendered fractal
        """
        # Create figure if not provided
        if figure is None:
            figure = plt.figure(figsize=(8, 8), dpi=self.options["dpi"])
        
        # Clear figure
        figure.clear()
        
        # If showing base pattern comparison, create a subplot grid
        if self.options["show_base_pattern"] and base_fractal is not None:
            logger.info("Rendering fractal with base pattern comparison")
            
            # Create subplots
            ax1 = figure.add_subplot(121)  # Base pattern
            ax2 = figure.add_subplot(122)  # Butterfly pattern
            
            # Create colormap
            cmap = LinearSegmentedColormap.from_list(self.options["cmap_name"], colors, N=256)
            
            # Plot base fractal
            im1 = ax1.imshow(base_fractal, cmap=cmap, origin='lower', 
                           extent=[-2, 1, -1.5, 1.5])
            ax1.set_title("Base Fractal Pattern")
            
            # Plot butterfly fractal
            im2 = ax2.imshow(fractal_data, cmap=cmap, origin='lower', 
                           extent=[-2, 1, -1.5, 1.5])
            ax2.set_title("Fractal Butterfly Pattern")
            
            # Add labels
            if self.options["show_axes"]:
                ax1.set_xlabel("Real")
                ax1.set_ylabel("Imaginary")
                ax2.set_xlabel("Real")
                ax2.set_ylabel("Imaginary")
            else:
                ax1.axis('off')
                ax2.axis('off')
            
            # Add grid
            if self.options["overlay_grid"]:
                ax1.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
                ax2.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
            
            # Add colorbar
            if self.options["show_colorbar"]:
                cbar = figure.colorbar(im2, ax=[ax1, ax2], shrink=0.8)
                cbar.set_label("Iteration Depth")
            
            # Add metrics if provided
            if metrics and self.options["show_metrics"]:
                self._add_metrics_to_plot(ax2, metrics)
            
        else:
            # Single plot for fractal only
            logger.info(f"Rendering fractal with shape {fractal_data.shape}")
            
            # Create axis
            ax = figure.add_subplot(111)
            
            # Create colormap
            cmap = LinearSegmentedColormap.from_list(self.options["cmap_name"], colors, N=256)
            
            # Plot fractal
            im = ax.imshow(fractal_data, cmap=cmap, origin='lower', 
                          extent=[-2, 1, -1.5, 1.5])
            
            # Add title
            ax.set_title(self.options["title"])
            
            # Add labels
            if self.options["show_axes"]:
                ax.set_xlabel("Real")
                ax.set_ylabel("Imaginary")
            else:
                ax.axis('off')
            
            # Add colorbar
            if self.options["show_colorbar"]:
                cbar = figure.colorbar(im)
                cbar.set_label("Iteration Depth")
            
            # Add grid
            if self.options["overlay_grid"]:
                ax.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
            
            # Add metrics if provided
            if metrics and self.options["show_metrics"]:
                self._add_metrics_to_plot(ax, metrics)
        
        # Adjust layout
        figure.tight_layout()
        
        return figure
    
    def _add_metrics_to_plot(self, ax, metrics: Dict[str, Any]) -> None:
        """
        Add metrics text to plot
        
        Args:
            ax: Matplotlib axes object
            metrics: Dictionary of metrics
        """
        # Format metrics text
        metrics_text = "Fractal Metrics:\n"
        
        # Add key metrics with formatting
        if "fractal_dimension" in metrics:
            metrics_text += f"Dimension: {metrics['fractal_dimension']:.3f}\n"
        
        if "symmetry_score" in metrics:
            metrics_text += f"Symmetry: {metrics['symmetry_score']:.3f}\n"
        
        if "complexity" in metrics:
            metrics_text += f"Complexity: {metrics['complexity']:.3f}\n"
        
        if "entropy" in metrics:
            metrics_text += f"Entropy: {metrics['entropy']:.3f}\n"
        
        if "hurst_exponent" in metrics:
            metrics_text += f"Hurst Exponent: {metrics['hurst_exponent']:.3f}\n"
            
        if "lyapunov_exponent" in metrics:
            metrics_text += f"Lyapunov Exponent: {metrics['lyapunov_exponent']:.3f}"
        
        # Add base fractal info if present
        if "using_base_fractal" in metrics and metrics["using_base_fractal"]:
            metrics_text += f"\n\nBase Fractal: {metrics.get('base_pattern', 'Unknown')}"
            metrics_text += f"\nInfluence: {metrics.get('base_influence', 0):.2f}"
        
        # Add text box
        props = dict(boxstyle='round', facecolor='white', alpha=0.7)
        ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=props)
    
    def save_figure(self, figure: Figure, output_path: str, dpi: int = 300) -> bool:
        """
        Save figure to file
        
        Args:
            figure: Matplotlib figure to save
            output_path: Path to save the figure
            dpi: DPI for saving
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Save figure
            figure.savefig(output_path, dpi=dpi)
            logger.info(f"Saved fractal to {output_path} at {dpi} DPI")
            return True
            
        except Exception as e:
            logger.error(f"Error saving figure: {e}")
            return False
    
    def generate_comparison_figure(self, 
                                  original_fractal: np.ndarray,
                                  modified_fractal: np.ndarray,
                                  colors: List[Tuple[float, float, float]],
                                  diff_title: str = "Difference") -> Figure:
        """
        Generate a comparison figure showing original, modified, and difference
        
        Args:
            original_fractal: Original fractal data
            modified_fractal: Modified fractal data
            colors: List of RGB color tuples for colormap
            diff_title: Title for difference plot
            
        Returns:
            Matplotlib figure with comparison
        """
        # Create figure
        figure = plt.figure(figsize=(12, 4), dpi=self.options["dpi"])
        
        # Create colormap
        cmap = LinearSegmentedColormap.from_list(self.options["cmap_name"], colors, N=256)
        
        # Calculate difference
        diff = np.abs(modified_fractal - original_fractal)
        
        # Plot original fractal
        ax1 = figure.add_subplot(131)
        im1 = ax1.imshow(original_fractal, cmap=cmap, origin='lower',
                        extent=[-2, 1, -1.5, 1.5])
        ax1.set_title("Original Fractal")
        
        # Plot modified fractal
        ax2 = figure.add_subplot(132)
        im2 = ax2.imshow(modified_fractal, cmap=cmap, origin='lower',
                        extent=[-2, 1, -1.5, 1.5])
        ax2.set_title("Modified Fractal")
        
        # Plot difference
        ax3 = figure.add_subplot(133)
        im3 = ax3.imshow(diff, cmap='hot', origin='lower',
                        extent=[-2, 1, -1.5, 1.5])
        ax3.set_title(diff_title)
        
        # Add labels
        if self.options["show_axes"]:
            ax1.set_xlabel("Real")
            ax1.set_ylabel("Imaginary")
            ax2.set_xlabel("Real")
            ax3.set_xlabel("Real")
        else:
            ax1.axis('off')
            ax2.axis('off')
            ax3.axis('off')
        
        # Add colorbars
        if self.options["show_colorbar"]:
            cbar1 = figure.colorbar(im1, ax=ax1, shrink=0.8)
            cbar1.set_label("Iteration Depth")
            cbar2 = figure.colorbar(im2, ax=ax2, shrink=0.8)
            cbar2.set_label("Iteration Depth")
            cbar3 = figure.colorbar(im3, ax=ax3, shrink=0.8)
            cbar3.set_label("Difference")
        
        # Add grid
        if self.options["overlay_grid"]:
            ax1.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
            ax2.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
            ax3.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
        
        # Adjust layout
        figure.tight_layout()
        
        return figure
