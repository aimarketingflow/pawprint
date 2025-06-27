#!/usr/bin/env python3
"""
Compare Screen - Stats Negative Row

Creates HTML table row for negative changes statistics.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_negative_stats_row(self, negative_changes, neg_percent):
    """Format HTML statistics table row for negative changes
    
    Args:
        negative_changes: Count of negative changes
        neg_percent: Negative changes percentage
        
    Returns:
        str: HTML statistics table row for negative changes
    """
    # Create negative changes row with red color
    html = f"""
                        <tr style="border-bottom: 1px solid #555555;">
                            <td style="padding: 8px; color: #cf6679;">Negative Changes</td>
                            <td style="padding: 8px; text-align: center; color: #cf6679;">{negative_changes}</td>
                            <td style="padding: 8px; text-align: center; color: #cf6679;">{neg_percent:.1f}%</td>
                        </tr>
    """
    return html
