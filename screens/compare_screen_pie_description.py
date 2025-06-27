#!/usr/bin/env python3
"""
Compare Screen - Pie Chart Description

Generates HTML description for pie chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_pie_html_description(self, pie_data):
    """Generate HTML description for pie chart
    
    Args:
        pie_data: Pie chart data
        
    Returns:
        str: HTML description
    """
    try:
        if not pie_data or 'categories' not in pie_data or len(pie_data['categories']) == 0:
            return "<p>No pie chart data available.</p>"
            
        # Generate description with dark theme styling
        html = "<h3 style='color:#bb86fc;'>Pie Chart: Category Distribution</h3>"
        html += "<p style='color:#dddddd;'>This chart shows the distribution of patterns by category.</p>"
        html += "<ul style='color:#dddddd;'>"
        
        # Add category counts
        for i, (category, count) in enumerate(zip(pie_data['categories'], pie_data['counts'])):
            html += f"<li><b>{category}</b>: {count} patterns</li>"
            
        html += "</ul>"
        
        return html
    except Exception as e:
        logger.error(f"Error generating pie description: {str(e)}")
        return "<p>Error generating chart description.</p>"
