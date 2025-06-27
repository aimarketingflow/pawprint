#!/usr/bin/env python3
"""
Compare Screen - Connect Save Chart Button

Connects save chart button to its event handler.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_save_chart_button(self, save_button):
    """Connect save chart button to click event handler
    
    Args:
        save_button: Save chart image button
        
    Returns:
        None
    """
    try:
        # Connect to save chart image handler
        save_button.clicked.connect(self.save_chart_image)
        logger.debug("Save chart button connected to click event handler")
    except Exception as e:
        logger.error(f"Error connecting save chart button: {str(e)}")
