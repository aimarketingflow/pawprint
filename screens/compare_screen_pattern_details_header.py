#!/usr/bin/env python3
"""
Compare Screen - Pattern Details Header

Creates HTML header for pattern details section in report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_details_header():
    """Create HTML header for pattern details section
    
    Returns:
        str: HTML content for pattern details header
    """
    try:
        # Create HTML pattern details header with dark theme styling
        header_html = """
        <div class="section pattern-details-section">
            <h2 class="section-header">Pattern Details</h2>
            <p class="section-description">
                This section shows detailed changes in each pattern between the compared files.
                Patterns are sorted by change percentage from most positive to most negative.
            </p>
        </div>
        """
        
        logger.debug("Pattern details header HTML created")
        return header_html
    except Exception as e:
        logger.error(f"Error creating pattern details header: {str(e)}")
        return "<div class='section pattern-details-section'><h2>Pattern Details</h2></div>"
