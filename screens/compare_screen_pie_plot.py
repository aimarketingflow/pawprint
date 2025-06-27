#!/usr/bin/env python3
"""
Compare Screen - Pie Chart Plotting

Plots pie chart data with proper styling and colors.

Author: AIMF LLC
Date: June 6, 2025
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def plot_pie_data(self, ax, pie_data):
    """Plot pie data on the given axis
    
    Args:
        ax: Matplotlib axis for plotting
        pie_data: Pie chart data
        
    Returns:
        bool: Success status
    """
    try:
        # Get categories and counts
        categories = pie_data['categories']
        counts = pie_data['counts']
        
        # Colors for dark theme - purple gradient
        colors = ['#bb86fc', '#985eff', '#7e3ff5', '#651fff', '#5034eb', '#3a29cc', '#2c1e99']
        
        # Extend colors if needed
        while len(colors) < len(categories):
            colors.extend(colors)
            
        # Plot pie chart
        wedges, texts = ax.pie(counts, colors=colors[:len(categories)], wedgeprops=dict(width=0.5))
        
        return True
    except Exception as e:
        logger.error(f"Error plotting pie data: {str(e)}")
        return False
