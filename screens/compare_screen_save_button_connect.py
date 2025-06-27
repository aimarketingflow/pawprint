#!/usr/bin/env python3
"""
Compare Screen - Save Button Connect

Connects save chart button to its event handler.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_save_button(self, save_button):
    """Connect save chart button to event handler
    
    Args:
        save_button: Save chart button instance
        
    Returns:
        None
    """
    try:
        # Connect button click to save chart image function
        save_button.clicked.connect(self.save_chart_image)
        logger.debug("Save chart button connected to event handler")
    except Exception as e:
        logger.error(f"Error connecting save button: {str(e)}")
