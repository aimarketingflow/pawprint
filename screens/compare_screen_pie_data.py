#!/usr/bin/env python3
"""
Compare Screen - Pie Chart Data

Processes data specifically for pie chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_pie_chart_data(self, chart_data):
    """Format data for pie chart visualization by category
    
    Args:
        chart_data: General chart data dictionary
        
    Returns:
        dict: Pie-specific chart data
    """
    # Ensure we have data to work with
    if not chart_data or 'patterns' not in chart_data or len(chart_data['patterns']) == 0:
        return None
    
    # Count patterns by category
    category_counts = {}
    for pattern in chart_data['patterns']:
        category = pattern.get('category', 'Unknown')
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1
    
    return {
        'categories': list(category_counts.keys()),
        'counts': list(category_counts.values())
    }
