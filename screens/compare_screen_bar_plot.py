#!/usr/bin/env python3
"""
Compare Screen - Bar Chart Plotting

Plots bar chart data with proper styling and labels.

Author: AIMF LLC
Date: June 6, 2025
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def plot_bar_data(self, ax, bar_data):
    """Plot bar data on the given axis
    
    Args:
        ax: Matplotlib axis for plotting
        bar_data: Bar chart data
        
    Returns:
        bool: Success status
    """
    try:
        # Get values
        labels = bar_data['labels']
        before = bar_data['before']
        after = bar_data['after']
        
        # Set bar positions
        x = np.arange(len(labels))
        width = 0.35
        
        # Plot bars with dark theme colors
        before_bars = ax.bar(x - width/2, before, width, label='Before', color='#bb86fc', alpha=0.8)
        after_bars = ax.bar(x + width/2, after, width, label='After', color='#03dac6', alpha=0.8)
        
        return True
    except Exception as e:
        logger.error(f"Error plotting bar data: {str(e)}")
        return False
