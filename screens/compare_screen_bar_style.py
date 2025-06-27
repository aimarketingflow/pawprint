#!/usr/bin/env python3
"""
Compare Screen - Bar Chart Styling

Applies dark theme styling with neon purple accents to bar charts.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def apply_bar_style(self, ax, labels):
    """Apply dark theme styling to bar chart
    
    Args:
        ax: Matplotlib axis
        labels: Chart labels
        
    Returns:
        bool: Success status
    """
    try:
        # Dark theme colors
        background_color = '#222222'
        grid_color = '#444444'
        text_color = '#dddddd'
        
        # Set background color
        ax.set_facecolor(background_color)
        self.chart_figure.patch.set_facecolor(background_color)
        
        # Set grid style
        ax.grid(axis='y', color=grid_color, linestyle='--', alpha=0.5)
        
        return True
    except Exception as e:
        logger.error(f"Error applying bar style: {str(e)}")
        return False
