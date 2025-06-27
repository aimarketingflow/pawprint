#!/usr/bin/env python3
"""
Compare Screen - Chart Type Handler

Handles chart type change events.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def on_chart_type_changed(self, index):
    """Handle chart type change event
    
    Args:
        index: Selected index in the combo box
        
    Returns:
        bool: Success status
    """
    try:
        # Get selected chart type
        chart_types = ['Bar Chart', 'Pie Chart', 'Radar Chart']
        if index < 0 or index >= len(chart_types):
            logger.warning(f"Invalid chart type index: {index}")
            return False
            
        chart_type = chart_types[index]
        logger.debug(f"Chart type changed to: {chart_type}")
        
        # Update chart display
        return self.display_chart(chart_type=chart_type)
    except Exception as e:
        logger.error(f"Error handling chart type change: {str(e)}")
        return False
