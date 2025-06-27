#!/usr/bin/env python3
"""
Compare Screen - Create Chart Display

Creates chart display widget with dark theme styling.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)

def create_chart_display_widget(self):
    """Create chart display widget
    
    Returns:
        QWidget: Chart display widget
    """
    try:
        # Check matplotlib availability
        if not hasattr(self, 'MATPLOTLIB_AVAILABLE'):
            self.check_matplotlib_availability()
            
        # Create chart display widget
        chart_widget = QWidget()
        chart_layout = QVBoxLayout()
        chart_layout.setContentsMargins(10, 10, 10, 10)
        
        if not self.MATPLOTLIB_AVAILABLE:
            # Create placeholder if matplotlib not available
            placeholder = QLabel("Charts unavailable - matplotlib not installed")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            placeholder.setStyleSheet("""
                color: #bb86fc;
                font-size: 16px;
                padding: 20px;
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 8px;
            """)
            chart_layout.addWidget(placeholder)
        else:
            # Create matplotlib widget
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
            from matplotlib.figure import Figure
            import matplotlib.pyplot as plt
            
            # Set matplotlib dark style
            plt.style.use('dark_background')
            
            # Create figure with dark background
            self.chart_figure = Figure(figsize=(8, 6), facecolor='#1e1e1e')
            self.canvas = FigureCanvas(self.chart_figure)
            
            # Add to layout
            chart_layout.addWidget(self.canvas)
            
        # Set layout on widget
        chart_widget.setLayout(chart_layout)
        
        # Apply dark theme styling
        chart_widget.setStyleSheet("""
            QWidget {
                background-color: #121212;
                border: 1px solid #333333;
                border-radius: 8px;
            }
        """)
        
        # Set minimum size
        chart_widget.setMinimumSize(400, 300)
        
        logger.debug("Chart display widget created")
        return chart_widget
    except Exception as e:
        logger.error(f"Error creating chart display widget: {str(e)}")
        # Return a basic widget if there's an error
        widget = QWidget()
        widget.setMinimumSize(400, 300)
        return widget
