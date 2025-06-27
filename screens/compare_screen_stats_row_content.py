#!/usr/bin/env python3
"""
Compare Screen - Stats Row Content

Creates the actual HTML table rows for statistics with proper styling.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_stats_rows(self, pos_percent, neg_percent, neu_percent, positive_changes, negative_changes, neutral_changes, total_patterns):
    """Format HTML statistics table rows with proper styling
    
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
    # Create positive changes row with teal color
    html = f"""
                        <tr style="border-bottom: 1px solid #555555;">
                            <td style="padding: 8px; color: #03dac6;">Positive Changes</td>
                            <td style="padding: 8px; text-align: center; color: #03dac6;">{positive_changes}</td>
                            <td style="padding: 8px; text-align: center; color: #03dac6;">{pos_percent:.1f}%</td>
                        </tr>
    """
    return html
