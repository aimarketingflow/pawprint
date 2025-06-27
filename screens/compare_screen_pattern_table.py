#!/usr/bin/env python3
"""
Compare Screen - Pattern Table

Creates HTML table structure for pattern details in report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_pattern_table_start():
    """Create HTML table structure for pattern details
    
    Returns:
        str: HTML content for pattern table structure
    """
    try:
        # Create HTML pattern table structure with dark theme styling
        table_html = """
        <table class="pattern-table">
            <thead>
                <tr>
                    <th>Pattern</th>
                    <th>Before Count</th>
                    <th>After Count</th>
                    <th>Change</th>
                    <th>Change %</th>
                    <th>Impact</th>
                </tr>
            </thead>
            <tbody>
        """
        
        logger.debug("Pattern table structure HTML created")
        return table_html
    except Exception as e:
        logger.error(f"Error creating pattern table structure: {str(e)}")
        return "<table class='pattern-table'><thead><tr><th>Pattern</th><th>Before</th><th>After</th><th>Change</th><th>%</th><th>Impact</th></tr></thead><tbody>"
