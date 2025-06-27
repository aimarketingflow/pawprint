#!/usr/bin/env python3
"""
Compare Screen - Radar Chart Styling

Applies dark theme styling with neon purple accents to radar charts.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def apply_radar_style(self, ax, labels):
    """Apply dark theme styling to radar chart
    
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
        primary_color = '#bb86fc'  # Neon purple accent
        secondary_color = '#03dac6'  # Teal accent
        
        # Set background color
        ax.set_facecolor(background_color)
        
        # Set grid color
        ax.grid(color=grid_color, linestyle='--', alpha=0.7)
