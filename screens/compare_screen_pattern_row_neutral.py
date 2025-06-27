#!/usr/bin/env python3
"""
Compare Screen - Pattern Row Neutral

Creates HTML table row for neutral pattern changes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_row_neutral(pattern_name, before_count, after_count):
    """Create HTML table row for neutral pattern changes
    
    Args:
        pattern_name: Name of pattern
        before_count: Count before comparison
        after_count: Count after comparison
        
    Returns:
        str: HTML content for table row
    """
    try:
        # Create HTML row for neutral pattern change with gray styling
        row_html = f"""
        <tr class="pattern-row neutral">
            <td class="pattern-name">{pattern_name}</td>
            <td class="before-count">{before_count}</td>
            <td class="after-count">{after_count}</td>
            <td class="change neutral">0</td>
            <td class="change-percent neutral">0.0%</td>
            <td class="impact neutral">
                <span class="impact-indicator">NEUTRAL</span>
            </td>
        </tr>
        """
        
        logger.debug(f"Neutral pattern row HTML created for {pattern_name}")
        return row_html
    except Exception as e:
        logger.error(f"Error creating neutral pattern row: {str(e)}")
        return f"<tr><td>{pattern_name}</td><td>{before_count}</td><td>{after_count}</td><td>0</td><td>0.0%</td><td>NEUTRAL</td></tr>"
