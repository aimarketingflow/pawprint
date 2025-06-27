#!/usr/bin/env python3
"""
Compare Screen - Pattern Row Negative

Creates HTML table row for negative pattern changes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_row_negative(pattern_name, before_count, after_count, change, change_percent):
    """Create HTML table row for negative pattern changes
    
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
        # Create HTML row for negative pattern change with red styling
        row_html = f"""
        <tr class="pattern-row negative">
            <td class="pattern-name">{pattern_name}</td>
            <td class="before-count">{before_count}</td>
            <td class="after-count">{after_count}</td>
            <td class="change negative">{change}</td>
            <td class="change-percent negative">{change_percent:.1f}%</td>
            <td class="impact negative">
                <span class="impact-indicator">NEGATIVE</span>
            </td>
        </tr>
        """
        
        logger.debug(f"Negative pattern row HTML created for {pattern_name}")
        return row_html
    except Exception as e:
        logger.error(f"Error creating negative pattern row: {str(e)}")
        return f"<tr><td>{pattern_name}</td><td>{before_count}</td><td>{after_count}</td><td>{change}</td><td>{change_percent:.1f}%</td><td>NEGATIVE</td></tr>"
