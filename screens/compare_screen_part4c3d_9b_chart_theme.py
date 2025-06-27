#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-9b: Chart Theme Configuration

Sets up dark theme and styling for matplotlib charts.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

def configure_chart_theme(self):
    """Configure dark theme styling for matplotlib charts
    """
    try:
        # Check if matplotlib is available
        if not MATPLOTLIB_AVAILABLE:
            return
            
        import matplotlib.pyplot as plt
        
        # Set dark theme colors
        plt.style.use('dark_background')
        
        # Custom colors for the Pawprinting theme
        self.chart_colors = {
            'background': '#333333',
            'text': '#ffffff',
            'accent': '#bb86fc',  # Neon purple
            'grid': '#444444',
            'improved': '#4CAF50',  # Green
            'regressed': '#F44336',  # Red
            'unchanged': '#2196F3'   # Blue
        }
        
        # Update rcParams for consistent styling
        plt.rcParams['axes.facecolor'] = self.chart_colors['background']
        plt.rcParams['figure.facecolor'] = self.chart_colors['background']
        plt.rcParams['text.color'] = self.chart_colors['text']
        plt.rcParams['axes.labelcolor'] = self.chart_colors['text']
        plt.rcParams['xtick.color'] = self.chart_colors['text']
        plt.rcParams['ytick.color'] = self.chart_colors['text']
        plt.rcParams['grid.color'] = self.chart_colors['grid']
        
    except Exception as e:
        logging.error(f"Error configuring chart theme: {str(e)}")
