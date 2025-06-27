#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-9c: Chart Display

Handles displaying different chart types on canvas.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

def display_chart(self, chart_type, chart_data=None):
    """Display a chart of specified type
    
    Args:
        chart_type: Type of chart (radar, bar, line, pie, heatmap)
        chart_data: Optional chart data dictionary
    """
    try:
        # Store current chart type
        self.current_chart_type = chart_type
        
        # Check if matplotlib is available
        if not MATPLOTLIB_AVAILABLE:
            self.chart_description_browser.setHtml(
                "<h3>Charts Unavailable</h3>"
                "<p>Matplotlib is required for chart visualization.</p>"
            )
            return
            
        # Prepare data if not provided
        if chart_data is None:
            chart_data = self.prepare_chart_data(chart_type)
            
        # Store current chart data
        self.current_chart_data = chart_data
        
        # Draw chart based on type
        self.draw_chart(chart_type, chart_data)
        
    except Exception as e:
        logging.error(f"Error displaying chart: {str(e)}")
        self.chart_description_browser.setHtml(
            f"<h3>Error Displaying Chart</h3><p>{str(e)}</p>"
        )
