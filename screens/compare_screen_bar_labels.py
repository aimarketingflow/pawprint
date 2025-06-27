#!/usr/bin/env python3
"""
Compare Screen - Bar Chart Labels

Handles label formatting and placement for bar charts.

Author: AIMF LLC
Date: June 6, 2025
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def format_bar_labels(self, ax, bar_data):
    """Format and position labels for bar chart
    
    Args:
        ax: Matplotlib axis
        bar_data: Bar chart data
        
    Returns:
        bool: Success status
    """
    try:
        # Get values
        labels = bar_data['labels']
        
        # Set dark theme colors
        text_color = '#dddddd'
        
        # Set x-axis labels with proper rotation
        x = np.arange(len(labels))
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, ha='right', color=text_color, fontsize=8)
        ax.tick_params(axis='y', colors=text_color)
        
        # Set labels
        ax.set_xlabel('Patterns', color=text_color)
        ax.set_ylabel('Score', color=text_color)
        
        return True
    except Exception as e:
        logger.error(f"Error formatting bar labels: {str(e)}")
        return False
