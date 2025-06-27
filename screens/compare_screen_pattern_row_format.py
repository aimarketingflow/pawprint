#!/usr/bin/env python3
"""
Compare Screen - Pattern Row Format

Formats HTML table rows for individual patterns with styling.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_pattern_row(self, name, category, before, after, change, percent, change_color):
    """Format HTML table row for an individual pattern
    
    Args:
        name: Pattern name
        category: Pattern category
        before: Before score
        after: After score
        change: Score change
        percent: Percentage change
        change_color: Color based on change direction
        
    Returns:
        str: HTML pattern table row
    """
