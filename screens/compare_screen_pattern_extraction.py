#!/usr/bin/env python3
"""
Compare Screen - Pattern Extraction

Continue the pattern changes extraction with category filtering.

Author: AIMF LLC
Date: June 6, 2025
"""

def extract_pattern_data(self, diff, category=None, threshold=0.0):
    """Extract pattern data from diff
    
    Args:
        diff: Diff data dictionary
        category: Pattern category to filter by
        threshold: Minimum change threshold
        
    Returns:
        list: Extracted pattern data
    """
    patterns = []
    
    # Process changed patterns
    if 'changed' in diff:
        for pattern_name, values in diff['changed'].items():
            if 'before' in values and 'after' in values:
                before = values['before']
                after = values['after']
