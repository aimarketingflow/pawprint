#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-9a: Chart Widget Setup

Basic chart widget initialization code.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

def setup_chart_widget(self):
    """Initialize the chart widget components
    
    Creates matplotlib figure and canvas for chart display
    """
    try:
        # Check if matplotlib is available
        global MATPLOTLIB_AVAILABLE
        try:
            import matplotlib
            matplotlib.use('Qt5Agg')
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            MATPLOTLIB_AVAILABLE = True
        except ImportError:
            logging.warning("Matplotlib not available, charts functionality will be limited")
            MATPLOTLIB_AVAILABLE = False
            return
            
        # Create figure with dark theme
        self.chart_figure = Figure(figsize=(10, 6), dpi=100)
        self.chart_figure.patch.set_facecolor('#333333')
        
        # Create canvas
        self.chart_canvas = FigureCanvas(self.chart_figure)
        
        # Add to chart container
        self.chart_container_layout.addWidget(self.chart_canvas)
        
    except Exception as e:
        logging.error(f"Error setting up chart widget: {str(e)}")
        MATPLOTLIB_AVAILABLE = False
