#!/usr/bin/env python3
"""
Compare Screen - Pattern Data Assembly

Finalizes pattern data for visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

def assemble_pattern_data(self, pattern_name, before, after, change, percent_change, category="Unknown"):
    """Assemble final pattern data dictionary
    
    Args:
        pattern_name: Name of the pattern
        before: Before score value
        after: After score value
        change: Absolute change value
        percent_change: Percentage change
        category: Pattern category
        
    Returns:
        dict: Complete pattern data
    """
    return {
        "name": pattern_name,
        "before_score": before,
        "after_score": after,
        "change": change,
        "percent_change": percent_change,
        "category": category
    }
