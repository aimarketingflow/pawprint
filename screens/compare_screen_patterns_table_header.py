#!/usr/bin/env python3
"""
Compare Screen - Patterns Table Header

Creates HTML table header for patterns detail in reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_patterns_table_header(self):
    """Create HTML table header for patterns detail
    
    Returns:
        str: HTML patterns table header
    """
    # Create table header with dark theme and neon purple styling
    html = """
                            <th style="padding: 8px; text-align: left; color: #bb86fc;">Pattern Name</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">Category</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">Before</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">After</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">Change</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">Percent</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    return html
