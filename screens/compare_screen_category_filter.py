#!/usr/bin/env python3
"""
Compare Screen - Category Filter

Handles filtering patterns by category.

Author: AIMF LLC
Date: June 6, 2025
"""

def filter_by_category(self, patterns, category=None, threshold=0.0):
    """Filter patterns by category and threshold
    
    Args:
        patterns: List of pattern dictionaries
        category: Category to filter by (None for all)
        threshold: Minimum absolute change threshold
        
    Returns:
        list: Filtered patterns
    """
    if not category:
        # Just filter by threshold
        return [p for p in patterns if abs(p.get('change', 0)) >= threshold]
    
    # Filter by both category and threshold
    return [p for p in patterns 
            if p.get('category', 'Unknown') == category 
            and abs(p.get('change', 0)) >= threshold]
