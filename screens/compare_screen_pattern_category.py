#!/usr/bin/env python3
"""
Compare Screen - Pattern Category Extraction

Handles pattern category determination and filtering.

Author: AIMF LLC
Date: June 6, 2025
"""

def get_pattern_category(self, pattern_name, values):
    """Determine pattern category from pattern data
    
    Args:
        pattern_name: Name of the pattern
        values: Pattern value dictionary
        
    Returns:
        str: Category name
    """
    # If category is directly provided
    if 'category' in values:
        return values['category']
        
    # Try to extract from pattern name
    if '_network_' in pattern_name.lower():
        return 'Network'
    elif '_file_' in pattern_name.lower():
        return 'File System'
    elif '_memory_' in pattern_name.lower():
        return 'Memory'
    elif '_process_' in pattern_name.lower():
        return 'Process'
