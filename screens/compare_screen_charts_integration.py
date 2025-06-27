#!/usr/bin/env python3
"""
Compare Screen - Charts Integration

Main integration module for chart functionality in Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout

logger = logging.getLogger(__name__)

def setup_charts_functionality(self):
    """Set up all chart functionality in the Compare Screen
    
    Returns:
        QWidget: Chart panel widget
    """
    try:
        logger.info("Setting up chart functionality for Compare Screen")
        
        # Check matplotlib availability first
        self.check_matplotlib_availability()
        
        if not self.MATPLOTLIB_AVAILABLE:
            logger.warning("Charts disabled - matplotlib not available")
            # Create a placeholder widget with notification
            return self.create_charts_unavailable_widget()
            
        # Create chart panel for visualization
        chart_panel = self.create_chart_panel_widget()
        
        # Connect chart type selector
        self.connect_chart_selector(self.chart_selector)
        
        # Initialize with default chart
        self.update_chart_display()
        
        logger.info("Chart functionality setup complete")
        return chart_panel
    except Exception as e:
        logger.error(f"Error setting up charts functionality: {str(e)}")
        return QWidget()
