#!/usr/bin/env python3
"""
Compare Screen - Pattern Rows

Creates HTML table rows for individual patterns in reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_rows(self, patterns):
    """Create HTML table rows for individual patterns
    
    Args:
        patterns: List of pattern dictionaries
        
    Returns:
        str: HTML pattern table rows
    """
    html = ""
    
    try:
        for pattern in patterns:
            name = pattern.get('name', 'Unknown')
            category = pattern.get('category', 'Unknown')
            before = pattern.get('before_score', 0.0)
            after = pattern.get('after_score', 0.0)
            change = pattern.get('change', 0.0)
            percent = pattern.get('percent_change', 0.0)
            
            # Determine row color based on change
            if change > 0.05:
                change_color = "#03dac6"  # Teal for positive
            elif change < -0.05:
                change_color = "#cf6679"  # Red for negative
            else:
                change_color = "#bbbbbb"  # Gray for neutral
