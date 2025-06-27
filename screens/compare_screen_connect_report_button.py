#!/usr/bin/env python3
"""
Compare Screen - Connect Report Button

Connects report button to its event handler.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_report_button(self, report_button):
    """Connect report button to click event handler
    
    Args:
        report_button: Report generation button
        
    Returns:
        None
    """
    try:
        # Connect to report generation handler
        report_button.clicked.connect(self.on_report_button_clicked)
        logger.debug("Report button connected to click event handler")
    except Exception as e:
        logger.error(f"Error connecting report button: {str(e)}")
