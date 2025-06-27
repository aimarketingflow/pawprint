#!/usr/bin/env python3
"""
Compare Screen - Pattern Row Positive

Creates HTML table row for positive pattern changes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_row_positive(pattern_name, before_count, after_count, change, change_percent):
    """Create HTML table row for positive pattern changes
    
    Args:
        pattern_name: Name of pattern
        before_count: Count before comparison
        after_count: Count after comparison
        change: Absolute change
        change_percent: Percentage change
        
    Returns:
        str: HTML content for table row
    """
    try:
        # Create HTML row for positive pattern change with teal styling
        row_html = f"""
        <tr class="pattern-row positive">
            <td class="pattern-name">{pattern_name}</td>
            <td class="before-count">{before_count}</td>
            <td class="after-count">{after_count}</td>
            <td class="change positive">+{change}</td>
            <td class="change-percent positive">+{change_percent:.1f}%</td>
            <td class="impact positive">
                <span class="impact-indicator">POSITIVE</span>
            </td>
        </tr>
        """
        
        logger.debug(f"Positive pattern row HTML created for {pattern_name}")
        return row_html
    except Exception as e:
        logger.error(f"Error creating positive pattern row: {str(e)}")
        return f"<tr><td>{pattern_name}</td><td>{before_count}</td><td>{after_count}</td><td>+{change}</td><td>+{change_percent:.1f}%</td><td>POSITIVE</td></tr>"
