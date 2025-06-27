#!/usr/bin/env python3
"""
Compare Screen - Chart Switcher Completion

Continues chart switching functionality with radar and pie chart options.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def switch_chart_display_completion(self, chart_type, chart_data):
    """Complete chart display switching logic
    
    Args:
        chart_type: Type of chart to display
        chart_data: Chart data dictionary
        
    Returns:
        bool: Success status
    """
    try:
        # Handle pie chart
        if chart_type == 'Pie Chart':
            pie_data = self.format_pie_chart_data(chart_data)
            return self.draw_pie_chart(pie_data)
            
        # Handle radar chart
        elif chart_type == 'Radar Chart':
            radar_data = self.format_radar_chart_data(chart_data)
            return self.draw_radar_chart(radar_data)
            
        return False
    except Exception as e:
        logger.error(f"Error switching chart display: {str(e)}")
        return False
