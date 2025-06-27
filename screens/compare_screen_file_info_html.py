#!/usr/bin/env python3
"""
Compare Screen - File Info HTML

Generates HTML file information section for reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_file_info_html(self, before_filename, after_filename):
    """Format HTML file information section
    
    Args:
        before_filename: Before comparison file name
        after_filename: After comparison file name
        
    Returns:
        str: HTML file info content
    """
    # Create file info section with dark theme styling
    html = f"""
                <h3>Files Compared</h3>
                <p><strong>Before:</strong> {before_filename}</p>
                <p><strong>After:</strong> {after_filename}</p>
            </div>
    """
    return html
