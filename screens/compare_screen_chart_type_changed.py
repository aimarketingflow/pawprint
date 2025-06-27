#!/usr/bin/env python3
"""
Compare Screen - Chart Type Changed

Handles chart type selection changes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def on_chart_type_changed(self):
    """Handle chart type selection change event
    
    Updates chart visualization based on selected chart type
    
    Returns:
        None
    """
    try:
        if not hasattr(self, 'chart_selector'):
            logger.warning("Chart selector not initialized")
            return
            
        # Get selected chart type
        chart_type = self.chart_selector.currentText()
        logger.info(f"Chart type changed to: {chart_type}")
        
        # Update chart display with selected type
        self.update_chart_display()
    except Exception as e:
        logger.error(f"Error handling chart type change: {str(e)}")
