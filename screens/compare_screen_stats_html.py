#!/usr/bin/env python3
"""
Compare Screen - Stats HTML

Generates HTML statistics section for reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_stats_html(self, positive_changes, negative_changes, neutral_changes, total_patterns):
    """Format HTML statistics section
    
    Args:
        positive_changes: Count of positive changes
        negative_changes: Count of negative changes
        neutral_changes: Count of neutral changes
        total_patterns: Total pattern count
        
    Returns:
        str: HTML statistics content
    """
    # Calculate percentages
    pos_percent = (positive_changes / total_patterns * 100) if total_patterns > 0 else 0
    neg_percent = (negative_changes / total_patterns * 100) if total_patterns > 0 else 0
    neu_percent = (neutral_changes / total_patterns * 100) if total_patterns > 0 else 0
