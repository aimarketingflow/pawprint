#!/usr/bin/env python3
"""
Compare Screen - Radar Chart Data

Processes data specifically for radar chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

def format_radar_chart_data(self, chart_data):
    """Format data for radar chart visualization
    
    Args:
        chart_data: General chart data dictionary
        
    Returns:
        dict: Radar-specific chart data
    """
    # Ensure we have data to work with
    if not chart_data or 'pattern_names' not in chart_data or len(chart_data['pattern_names']) == 0:
        return None
    
    # Create specific radar data format
    radar_data = {
        'labels': chart_data['pattern_names'],
        'before': chart_data['before_scores'],
        'after': chart_data['after_scores']
    }
    
    return radar_data
