#!/usr/bin/env python3
"""
Compare Screen - Stats Neutral Row

Creates HTML table row for neutral changes statistics.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_neutral_stats_row(self, neutral_changes, neu_percent):
    """Format HTML statistics table row for neutral changes
    
    Args:
        neutral_changes: Count of neutral changes
        neu_percent: Neutral changes percentage
        
    Returns:
        str: HTML statistics table row for neutral changes
    """
    # Create neutral changes row with gray color
    html = f"""
                        <tr style="border-bottom: 1px solid #555555;">
                            <td style="padding: 8px; color: #bbbbbb;">Neutral Changes</td>
                            <td style="padding: 8px; text-align: center; color: #bbbbbb;">{neutral_changes}</td>
                            <td style="padding: 8px; text-align: center; color: #bbbbbb;">{neu_percent:.1f}%</td>
                        </tr>
    """
    return html
