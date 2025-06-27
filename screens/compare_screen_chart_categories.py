#!/usr/bin/env python3
"""
Compare Screen - Chart Categories

Handles chart category counts and organization.

Author: AIMF LLC
Date: June 6, 2025
"""

def calculate_category_counts(self, patterns):
    """Calculate counts per category from patterns
    
    Args:
        patterns: List of pattern dictionaries
        
    Returns:
        dict: Category count dictionary
    """
    category_counts = {}
    
    for pattern in patterns:
        category = pattern.get("category", "Unknown")
        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1
            
    return category_counts
