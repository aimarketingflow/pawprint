#!/usr/bin/env python3
"""
Compare Screen - Export Button Connect

Connects export data button click events to handlers.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_export_button(self, export_button):
    """Connect export data button to event handler
    
    Args:
        export_button: Export data button instance
        
    Returns:
        None
    """
    try:
        # Connect button click to export data function
        export_button.clicked.connect(self.export_chart_data)
        logger.debug("Export data button connected to event handler")
    except Exception as e:
        logger.error(f"Error connecting export data button: {str(e)}")
