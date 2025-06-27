#!/usr/bin/env python3
"""
Compare Screen - Get Pattern Changes

Helper function to get pattern changes for chart data extraction.

Author: AIMF LLC
Date: June 6, 2025
"""

def get_pattern_changes_by_category(self, category=None, threshold=0.0):
    """Extract pattern changes filtered by category
    
    Args:
        category: Pattern category to filter by (None for all)
        threshold: Minimum absolute change threshold
        
    Returns:
        list: Pattern changes
    """
    if not hasattr(self, 'diff_cache') or not self.diff_cache:
        return []
        
    patterns = []
    
    if 'current_diff' not in self.diff_cache:
        return []
        
    diff = self.diff_cache['current_diff']
