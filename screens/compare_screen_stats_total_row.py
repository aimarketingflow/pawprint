#!/usr/bin/env python3
"""
Compare Screen - Stats Total Row

Creates HTML table row for total changes statistics.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_total_stats_row(self, total_patterns):
    """Format HTML statistics table row for total changes
    
    Args:
        total_patterns: Total pattern count
        
    Returns:
        str: HTML statistics table row for total changes
    """
    # Create total row with neon purple accent
    html = f"""
                        <tr>
                            <td style="padding: 8px; color: #bb86fc; font-weight: bold;">Total Patterns</td>
                            <td style="padding: 8px; text-align: center; color: #bb86fc; font-weight: bold;">{total_patterns}</td>
                            <td style="padding: 8px; text-align: center; color: #bb86fc; font-weight: bold;">100%</td>
                        </tr>
    """
    return html
