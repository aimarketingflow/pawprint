#!/usr/bin/env python3
"""
Compare Screen - Radar Chart Plotting

Continues radar chart plotting with styling and data plotting.

Author: AIMF LLC
Date: June 6, 2025
"""

import numpy as np
import logging

logger = logging.getLogger(__name__)

def plot_radar_data(self, ax, radar_data):
    """Plot radar data on the given axis
    
    Args:
        ax: Matplotlib axis for plotting
        radar_data: Radar chart data
        
    Returns:
        bool: Success status
    """
    try:
        # Get values
        labels = radar_data['labels']
        before = radar_data['before']
        after = radar_data['after']
        
        # Calculate angles for radar chart
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        
        # Close the loop
        before = np.concatenate((before, [before[0]]))
        after = np.concatenate((after, [after[0]]))
        angles = angles + [angles[0]]
