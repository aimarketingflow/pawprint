#!/usr/bin/env python3
"""
Compare Screen - Chart Switcher

Switches between different chart types based on selection.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def switch_chart_display(self, chart_type, chart_data):
    """Switch chart display based on selected type
    
    Args:
        chart_type: Type of chart to display
        chart_data: Chart data dictionary
        
    Returns:
        bool: Success status
    """
    try:
        # Check if we have data
        if not chart_data or 'patterns' not in chart_data or len(chart_data['patterns']) == 0:
            logger.warning("No chart data available for display")
            return False
            
        # Display based on chart type
        if chart_type == 'Bar Chart':
            bar_data = self.format_bar_chart_data(chart_data)
            return self.draw_bar_chart(bar_data)
