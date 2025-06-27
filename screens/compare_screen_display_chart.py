#!/usr/bin/env python3
"""
Compare Screen - Display Chart

Handles chart display logic based on selected chart type.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def display_chart(self, chart_type='Bar Chart', category=None, threshold=0.0):
    """Display chart based on type, category, and threshold
    
    Args:
        chart_type: Type of chart to display
        category: Pattern category to filter by
        threshold: Minimum change threshold
        
    Returns:
        bool: Success status
    """
    try:
        # Check if matplotlib is available
        if not self.MATPLOTLIB_AVAILABLE:
            logger.warning("Cannot display chart - matplotlib not available")
            return False
            
        # Extract chart data
        chart_data = self.extract_chart_data(category, threshold)
