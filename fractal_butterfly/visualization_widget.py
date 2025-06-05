#!/usr/bin/env python3
"""
Visualization Widget Module

UI widget for displaying fractal butterfly visualizations.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import logging
import numpy as np
from typing import Dict, Any, Tuple, List, Optional
import copy
import matplotlib.pyplot as plt

from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QSizePolicy, QScrollArea, QFrame
)

try:
    from matplotlib.figure import Figure
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.viz_widget")

class VisualizationWidget(QWidget):
    """
    Widget for displaying fractal butterfly visualizations
    """
    
    def __init__(self, parent=None):
        """Initialize the visualization widget"""
        super().__init__(parent)
        
        # Default properties
        self.figure_size = (6, 6)  # inches
        self.dpi = 100
        self.title = "Fractal Butterfly Pattern"
        self.extent = [-2, 1, -1.5, 1.5]  # Default coordinate extent
        
        # Storage for current data
        self.fractal_data = None
        self.colormap = None
        self.metrics = None
        
        # Set up UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        if not MATPLOTLIB_AVAILABLE:
            # Fallback if matplotlib not available
            layout = QVBoxLayout(self)
            error_label = QLabel(
                "Matplotlib is required for visualization. Please install matplotlib.",
                self
            )
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            error_label.setStyleSheet("color: red; font-weight: bold;")
            layout.addWidget(error_label)
            return
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Create matplotlib figure and canvas
        self.fig = Figure(figsize=self.figure_size, dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMinimumSize(350, 350)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        # Create navigation toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setIconSize(QSize(16, 16))
        
        # Add to layout
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        # Add status label
        self.status_label = QLabel("Ready", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMaximumHeight(16)
        layout.addWidget(self.status_label)
    
    def clear_plot(self) -> None:
        """Clear the current plot"""
        if not MATPLOTLIB_AVAILABLE:
            return
            
        self.fig.clear()
        self.canvas.draw()
        
        # Clear stored data
        self.fractal_data = None
        self.colormap = None
        self.metrics = None
        
        # Update status
        self.status_label.setText("Plot cleared")
    
    def render_fractal(self, fractal_data: np.ndarray, 
                      colors: List[Tuple[float, float, float]], 
                      metrics: Optional[Dict[str, Any]] = None) -> None:
        """
        Render fractal data to the plot
        
        Args:
            fractal_data: Numpy array containing fractal data
            colors: List of RGB color tuples for colormap
            metrics: Optional dictionary of metrics to display
        """
        if not MATPLOTLIB_AVAILABLE:
            return
            
        logger.info(f"Rendering fractal with dimensions {fractal_data.shape}")
        
        # Store data
        self.fractal_data = fractal_data
        self.colormap = colors
        self.metrics = metrics
        
        # Clear figure
        self.fig.clear()
        ax = self.fig.add_subplot(111)
        
        # Create colormap
        cmap_name = 'fractal_butterfly'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=256)
        
        # Render fractal
        im = ax.imshow(fractal_data, cmap=cmap, origin='lower', extent=self.extent)
        
        # Add labels
        ax.set_title(self.title)
        ax.set_xlabel("Real")
        ax.set_ylabel("Imaginary")
        
        # Add colorbar
        cbar = self.fig.colorbar(im)
        cbar.set_label("Iteration Depth")
        
        # Add grid for reference
        ax.grid(color='white', linestyle='--', linewidth=0.5, alpha=0.3)
        
        # Add metrics if provided
        if metrics:
            self.add_metrics_to_plot(ax, metrics)
        
        # Tight layout and draw
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Update status
        self.status_label.setText(f"Rendered fractal: {fractal_data.shape[0]}x{fractal_data.shape[1]}")
    
    def render_from_figure(self, figure: Figure) -> None:
        """
        Render from an existing matplotlib figure
        
        Args:
            figure: Matplotlib figure to render
        """
        if not MATPLOTLIB_AVAILABLE:
            return
            
        logger.info("Rendering from external figure")
        
        # Clear existing figure
        self.fig.clear()
        
        # Copy the figure contents to our canvas
        for ax in figure.axes:
            # Create a new axes with the same dimensions
            new_ax = self.fig.add_axes(ax.get_position())
            
            # Copy all artists from the original axes
            for artist in ax.get_children():
                # Skip text objects as they might have references to the original axes
                if not isinstance(artist, plt.Text):
                    artist_copy = copy.copy(artist)
                    new_ax.add_artist(artist_copy)
            
            # Copy axes properties
            new_ax.set_title(ax.get_title())
            new_ax.set_xlabel(ax.get_xlabel())
            new_ax.set_ylabel(ax.get_ylabel())
            new_ax.set_xlim(ax.get_xlim())
            new_ax.set_ylim(ax.get_ylim())
            
            # Copy grid
            new_ax.grid(ax.get_grid())
        
        # Redraw the canvas
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Update status
        self.status_label.setText("Rendered from external figure")
    
    def add_metrics_to_plot(self, ax, metrics: Dict[str, Any]) -> None:
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
            metrics_text += f"Hurst Exponent: {metrics['hurst_exponent']:.3f}"
        
        # Add text box
        props = dict(boxstyle='round', facecolor='white', alpha=0.7)
        ax.text(0.02, 0.98, metrics_text, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=props)
    
    def set_title(self, title: str) -> None:
        """
        Set plot title
        
        Args:
            title: Plot title
        """
        self.title = title
        
        # Update plot if exists
        if MATPLOTLIB_AVAILABLE and hasattr(self, 'fig') and self.fractal_data is not None:
            if len(self.fig.axes) > 0:
                self.fig.axes[0].set_title(title)
                self.canvas.draw()
    
    def save_figure(self, output_path: str, dpi: int = 300) -> bool:
        """
        Save figure to file
        
        Args:
            output_path: Path to save the figure
            dpi: DPI for saving (dots per inch)
            
        Returns:
            True if successful, False otherwise
        """
        if not MATPLOTLIB_AVAILABLE or self.fractal_data is None:
            logger.error("Cannot save figure: No data or matplotlib not available")
            return False
            
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            
            # Save figure
            self.fig.savefig(output_path, dpi=dpi)
            logger.info(f"Saved fractal to {output_path} at {dpi} DPI")
            
            # Update status
            self.status_label.setText(f"Saved to {os.path.basename(output_path)}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving figure: {e}")
            self.status_label.setText(f"Error saving: {str(e)}")
            return False
    
    def resizeEvent(self, event: QResizeEvent) -> None:
        """
        Handle resize events
        
        Args:
            event: Resize event
        """
        super().resizeEvent(event)
        
        # Redraw canvas on resize if data exists
        if MATPLOTLIB_AVAILABLE and self.fractal_data is not None:
            self.canvas.draw()
