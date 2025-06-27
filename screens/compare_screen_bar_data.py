#!/usr/bin/env python3
"""
Compare Screen - Bar Chart Data

Processes data specifically for bar chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

def format_bar_chart_data(self, chart_data):
    """Format data for bar chart visualization
    
    Args:
        chart_data: General chart data dictionary
        
    Returns:
        dict: Bar-specific chart data
    """
    # Ensure we have data to work with
    if not chart_data or 'pattern_names' not in chart_data or len(chart_data['pattern_names']) == 0:
        return None
    
    # Create specific bar data format
    bar_data = {
        'labels': chart_data['pattern_names'],
        'before': chart_data['before_scores'],
        'after': chart_data['after_scores'],
        'change': chart_data['changes']
    }
    
    return bar_data
