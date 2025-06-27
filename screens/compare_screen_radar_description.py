#!/usr/bin/env python3
"""
Compare Screen - Radar Chart Description

Generates HTML description for radar chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_radar_html_description(self, radar_data):
    """Generate HTML description for radar chart
    
    Args:
        radar_data: Radar chart data
        
    Returns:
        str: HTML description
    """
    try:
        if not radar_data or 'labels' not in radar_data or len(radar_data['labels']) == 0:
            return "<p>No radar chart data available.</p>"
            
        # Generate description with dark theme styling
        html = "<h3 style='color:#bb86fc;'>Radar Chart: Pattern Distribution</h3>"
        html += "<p style='color:#dddddd;'>This chart shows how pattern scores are distributed before and after comparison.</p>"
        html += "<p style='color:#dddddd;'>The purple line represents the original values, while the teal line shows the modified values.</p>"
        
        return html
    except Exception as e:
        logger.error(f"Error generating radar description: {str(e)}")
        return "<p>Error generating chart description.</p>"
