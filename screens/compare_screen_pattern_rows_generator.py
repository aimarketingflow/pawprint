#!/usr/bin/env python3
"""
Compare Screen - Pattern Rows Generator

Generates and sorts pattern rows for report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_pattern_rows(comparison_data):
    """Generate sorted HTML rows for all patterns
    
    Args:
        comparison_data: Dictionary of patterns with before/after counts
        
    Returns:
        str: HTML content for all pattern rows
    """
    try:
        from .compare_screen_pattern_row_positive import create_pattern_row_positive
        from .compare_screen_pattern_row_negative import create_pattern_row_negative
        from .compare_screen_pattern_row_neutral import create_pattern_row_neutral
        
        # Calculate changes and sort patterns
        patterns_with_changes = []
        for pattern_name, counts in comparison_data.items():
            before_count = counts.get('before', 0)
            after_count = counts.get('after', 0)
            
            change = after_count - before_count
            # Handle division by zero for percentage calculation
            if before_count == 0:
                if after_count == 0:
                    change_percent = 0.0
                else:
                    change_percent = 100.0
            else:
                change_percent = (change / before_count) * 100
                
            patterns_with_changes.append({
                'name': pattern_name,
                'before': before_count,
                'after': after_count,
                'change': change,
                'change_percent': change_percent
            })
        
        # Sort patterns by change percentage (descending)
        sorted_patterns = sorted(
            patterns_with_changes,
            key=lambda x: x['change_percent'],
            reverse=True
        )
        
        # Generate HTML for each pattern row
        rows_html = ""
        for pattern in sorted_patterns:
            if pattern['change'] > 0:
                rows_html += create_pattern_row_positive(
                    pattern['name'],
                    pattern['before'],
                    pattern['after'],
                    pattern['change'],
                    pattern['change_percent']
                )
            elif pattern['change'] < 0:
                rows_html += create_pattern_row_negative(
                    pattern['name'],
                    pattern['before'],
                    pattern['after'],
                    pattern['change'],
                    pattern['change_percent']
                )
            else:
                rows_html += create_pattern_row_neutral(
                    pattern['name'],
                    pattern['before'],
                    pattern['after']
                )
                
        logger.debug(f"Generated {len(sorted_patterns)} pattern rows")
        return rows_html
    except Exception as e:
        logger.error(f"Error generating pattern rows: {str(e)}")
        return "<tr><td colspan='6'>Error generating pattern details</td></tr>"
