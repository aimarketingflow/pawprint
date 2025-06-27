#!/usr/bin/env python3
"""
Compare Screen - Chart Image HTML

Creates HTML for embedded chart images in reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_chart_image_html(self, encoded_image, chart_type):
    """Create HTML for embedded chart image
    
    Args:
        encoded_image: Base64 encoded image data
        chart_type: Type of chart
        
    Returns:
        str: HTML with embedded chart image
    """
    try:
        # Format chart div with dark theme styling
        html = f"""
                <div class="chart" style="flex: 1; min-width: 300px; background-color: #333333; padding: 15px; border-radius: 5px;">
                    <h3 style="color: #bb86fc; margin-top: 0;">{chart_type}</h3>
                    <img src="data:image/png;base64,{encoded_image}" alt="{chart_type}" style="width: 100%; max-width: 500px;">
                </div>
        """
        return html
    except Exception as e:
        logger.error(f"Error creating chart HTML: {str(e)}")
        return ""
