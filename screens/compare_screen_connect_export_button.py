#!/usr/bin/env python3
"""
Compare Screen - Connect Export Button

Connects export data button to its event handler.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_export_button(self, export_button):
    """Connect export button to click event handler
    
    Args:
        export_button: Export data button
        
    Returns:
        None
    """
    try:
        # Connect to export data handler
        export_button.clicked.connect(self.export_chart_data)
        logger.debug("Export button connected to click event handler")
    except Exception as e:
        logger.error(f"Error connecting export button: {str(e)}")
