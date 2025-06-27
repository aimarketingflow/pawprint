#!/usr/bin/env python3
"""
Compare Screen - Pattern Row HTML

Creates the actual HTML for individual pattern rows.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_row_html(self, name, category, before, after, change, percent, change_color):
    """Create HTML for pattern table row
    
    Args:
        name: Pattern name
        category: Pattern category
        before: Before score
        after: After score
        change: Score change
        percent: Percentage change
        change_color: Color based on change direction
        
    Returns:
        str: HTML pattern row
    """
    # Format row with styling based on change direction
    html = f"""
                        <tr style="border-bottom: 1px solid #555555;">
                            <td style="padding: 8px; color: #dddddd;">{name}</td>
                            <td style="padding: 8px; text-align: center; color: #dddddd;">{category}</td>
                            <td style="padding: 8px; text-align: center; color: #dddddd;">{before:.2f}</td>
                            <td style="padding: 8px; text-align: center; color: #dddddd;">{after:.2f}</td>
                            <td style="padding: 8px; text-align: center; color: {change_color};">{change:.2f}</td>
                            <td style="padding: 8px; text-align: center; color: {change_color};">{percent:.1f}%</td>
                        </tr>
    """
    return html
