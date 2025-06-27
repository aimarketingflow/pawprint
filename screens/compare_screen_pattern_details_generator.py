#!/usr/bin/env python3
"""
Compare Screen - Pattern Details Generator

Generates complete pattern details section for report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_pattern_details_section(comparison_data):
    """Generate complete pattern details section for report
    
    Args:
        comparison_data: Dictionary of patterns with before/after counts
        
    Returns:
        str: Complete HTML for pattern details section
    """
    try:
        from .compare_screen_pattern_details_header import create_pattern_details_header
        from .compare_screen_pattern_table import create_pattern_table_start
        from .compare_screen_pattern_row_positive import create_pattern_row_positive
        from .compare_screen_pattern_row_negative import create_pattern_row_negative
        from .compare_screen_pattern_row_neutral import create_pattern_row_neutral
        from .compare_screen_pattern_table_footer import create_pattern_table_footer
        
        # Create section header
        pattern_details_html = create_pattern_details_header()
        
        # Create table structure
        pattern_details_html += create_pattern_table_start()
        
        # Add pattern rows
        pattern_details_html += generate_pattern_rows(comparison_data)
        
        # Add table footer
        pattern_details_html += create_pattern_table_footer()
        
        logger.debug("Pattern details section generated")
        return pattern_details_html
    except Exception as e:
        logger.error(f"Error generating pattern details section: {str(e)}")
        return "<div class='section pattern-details-section'><h2>Pattern Details</h2><p>Error generating pattern details</p></div>"
