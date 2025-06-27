#!/usr/bin/env python3
"""
Compare Screen - Pie Chart Drawing

Draws pie chart visualization with matplotlib.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import numpy as np

logger = logging.getLogger(__name__)

def draw_pie_chart(self, pie_data):
    """Draw pie chart using matplotlib
    
    Args:
        pie_data: Pie-specific chart data
        
    Returns:
        bool: Success status
    """
    if not self.MATPLOTLIB_AVAILABLE:
        logger.error("Matplotlib not available for pie chart")
        return False
        
    try:
        # Clear the current figure
        self.chart_figure.clear()
        
        # Get axis
        ax = self.chart_figure.add_subplot(111)
        
        # Get categories and counts
        categories = pie_data.get('categories', [])
        counts = pie_data.get('counts', [])
        
        if not categories or not counts or len(categories) == 0 or len(counts) == 0:
            logger.warning("No data for pie chart")
            return False
