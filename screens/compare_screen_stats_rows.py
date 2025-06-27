#!/usr/bin/env python3
"""
Compare Screen - Stats Rows

Creates HTML table rows for statistics in reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_stats_table_rows(self, pos_percent, neg_percent, neu_percent, positive_changes, negative_changes, neutral_changes, total_patterns):
    """Create HTML statistics table rows with dark theme styling
    
    Args:
        pos_percent: Positive changes percentage
        neg_percent: Negative changes percentage
        neu_percent: Neutral changes percentage
        positive_changes: Count of positive changes
        negative_changes: Count of negative changes
        neutral_changes: Count of neutral changes
        total_patterns: Total pattern count
        
    Returns:
        str: HTML statistics table rows
    """
