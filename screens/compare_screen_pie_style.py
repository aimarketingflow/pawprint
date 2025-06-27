#!/usr/bin/env python3
"""
Compare Screen - Pie Chart Styling

Applies dark theme styling with neon purple accents to pie charts.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def apply_pie_style(self, ax, pie_data):
    """Apply dark theme styling to pie chart
    
    Args:
        ax: Matplotlib axis
        pie_data: Pie chart data
        
    Returns:
        bool: Success status
    """
    try:
        # Dark theme colors
        background_color = '#222222'
        text_color = '#dddddd'
        
        # Set background color
        ax.set_facecolor(background_color)
        self.chart_figure.patch.set_facecolor(background_color)
        
        # Get categories
        categories = pie_data['categories']
        
        # Add legend with dark theme styling
        ax.legend(
            categories,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=8,
            frameon=False,
            labelcolor=text_color
        )
        
        return True
    except Exception as e:
        logger.error(f"Error applying pie style: {str(e)}")
        return False
