#!/usr/bin/env python3
"""
Compare Screen - Bar Chart Description

Generates HTML description for bar chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_bar_html_description(self, bar_data):
    """Generate HTML description for bar chart
    
    Args:
        bar_data: Bar chart data
        
    Returns:
        str: HTML description
    """
    try:
        if not bar_data or 'labels' not in bar_data or len(bar_data['labels']) == 0:
            return "<p>No bar chart data available.</p>"
            
        # Generate description with dark theme styling
        html = "<h3 style='color:#bb86fc;'>Bar Chart: Before vs After Comparison</h3>"
        html += "<p style='color:#dddddd;'>This chart compares before and after scores for each pattern.</p>"
        html += "<p style='color:#dddddd;'>Purple bars represent original values, teal bars show modified values.</p>"
        
        return html
    except Exception as e:
        logger.error(f"Error generating bar description: {str(e)}")
        return "<p>Error generating chart description.</p>"
