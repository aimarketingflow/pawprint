#!/usr/bin/env python3
"""
Compare Screen - Update Chart

Updates chart display when data or selection changes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def update_chart_display(self):
    """Update chart display based on current data and selection
    
    Returns:
        bool: Success status
    """
    try:
        # Get chart data
        chart_data = self.extract_chart_data()
        if not chart_data:
            logger.warning("No chart data available to display")
            return False
        
        # Get selected chart type
        chart_type = self.chart_selector.currentText() if hasattr(self, 'chart_selector') else "Bar Chart"
        
        # Draw the selected chart
        success = self.draw_chart(chart_data, chart_type)
        if not success:
            logger.warning(f"Failed to draw {chart_type}")
            return False
            
        logger.debug(f"Chart display updated with {chart_type}")
        return True
    except Exception as e:
        logger.error(f"Error updating chart display: {str(e)}")
        return False
