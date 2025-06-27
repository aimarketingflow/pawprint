#!/usr/bin/env python3
"""
Compare Screen - Report Button Connect

Connects report button click events to handlers.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_report_button(self, report_button):
    """Connect report button to event handler
    
    Args:
        report_button: Report button instance
        
    Returns:
        None
    """
    try:
        # Connect button click to report generation function
        report_button.clicked.connect(self.generate_report)
        logger.debug("Report button connected to event handler")
    except Exception as e:
        logger.error(f"Error connecting report button: {str(e)}")
