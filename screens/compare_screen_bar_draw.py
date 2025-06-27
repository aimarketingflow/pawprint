#!/usr/bin/env python3
"""
Compare Screen - Bar Chart Drawing

Draws bar chart visualization with matplotlib.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

def draw_bar_chart(self, bar_data):
    """Draw bar chart using matplotlib
    
    Args:
        bar_data: Bar-specific chart data
        
    Returns:
        bool: Success status
    """
    if not self.MATPLOTLIB_AVAILABLE:
        logger.error("Matplotlib not available for bar chart")
        return False
        
    try:
        # Clear the current figure
        self.chart_figure.clear()
        
        # Get axis
        ax = self.chart_figure.add_subplot(111)
        
        # Apply dark theme styling
        background_color = '#222222'
        text_color = '#dddddd'
        primary_color = '#bb86fc'  # Neon purple accent
        secondary_color = '#03dac6'  # Teal accent
