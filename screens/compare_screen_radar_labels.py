#!/usr/bin/env python3
"""
Compare Screen - Radar Chart Labels

Handles label formatting and placement for radar charts.

Author: AIMF LLC
Date: June 6, 2025
"""

import numpy as np
import logging
import math

logger = logging.getLogger(__name__)

def format_radar_labels(self, ax, labels):
    """Format and position labels for radar chart
    
    Args:
        ax: Matplotlib axis
        labels: Chart labels
        
    Returns:
        bool: Success status
    """
    try:
        # Color settings for dark theme
        text_color = '#dddddd'
        
        # Calculate label positions
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        
        # Set the labels with proper rotation
        ax.set_xticks(angles)
        ax.set_xticklabels(labels, color=text_color, size=8)
