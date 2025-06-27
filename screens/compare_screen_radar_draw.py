#!/usr/bin/env python3
"""
Compare Screen - Radar Chart Drawing

Draws radar chart visualization with matplotlib.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import math
import numpy as np

logger = logging.getLogger(__name__)

def draw_radar_chart(self, radar_data):
    """Draw radar chart using matplotlib
    
    Args:
        radar_data: Radar-specific chart data
        
    Returns:
        bool: Success status
    """
    if not self.MATPLOTLIB_AVAILABLE:
        logger.error("Matplotlib not available for radar chart")
        return False
        
    try:
        # Clear the current figure
        self.chart_figure.clear()
        
        # Get axis
        ax = self.chart_figure.add_subplot(111, polar=True)
