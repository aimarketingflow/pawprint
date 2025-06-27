#!/usr/bin/env python3
"""
Compare Screen - Process Chart Patterns

Processes patterns for chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def process_chart_patterns(self, diff_data, category=None, threshold=0.0):
    """Process patterns from diff data for charts
    
    Args:
        diff_data: Diff data from comparison
        category: Optional category filter
        threshold: Minimum change threshold
        
    Returns:
        list: Processed patterns
    """
    patterns = []
    
    # Process changed patterns
    if 'changed' not in diff_data:
        return patterns
        
    for pattern_name, values in diff_data['changed'].items():
        if 'before' not in values or 'after' not in values:
            continue
