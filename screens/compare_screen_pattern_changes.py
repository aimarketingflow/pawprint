#!/usr/bin/env python3
"""
Compare Screen - Pattern Changes

Continue pattern data calculation with change calculation.

Author: AIMF LLC
Date: June 6, 2025
"""

def calculate_pattern_changes(self, pattern_name, before, after, category="Unknown"):
    """Calculate pattern change metrics
    
    Args:
        pattern_name: Name of the pattern
        before: Before score value
        after: After score value
        category: Pattern category
        
    Returns:
        dict: Pattern change data
    """
    change = after - before
    abs_change = abs(change)
    
    # Calculate percent change safely
    if before > 0:
        percent_change = (change / before) * 100
    else:
        percent_change = 0 if change == 0 else 100
