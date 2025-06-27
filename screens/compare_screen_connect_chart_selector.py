#!/usr/bin/env python3
"""
Compare Screen - Connect Chart Selector

Connects chart selector to its change event handler.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_chart_selector(self, chart_selector):
    """Connect chart selector to change event handler
    
    Args:
        chart_selector: Chart type selector combo box
        
    Returns:
        None
    """
    try:
        # Connect chart selector to change event handler
        chart_selector.currentTextChanged.connect(self.on_chart_type_changed)
        logger.debug("Chart selector connected to change event handler")
    except Exception as e:
        logger.error(f"Error connecting chart selector: {str(e)}")
