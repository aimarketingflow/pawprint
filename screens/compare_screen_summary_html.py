#!/usr/bin/env python3
"""
Compare Screen - Summary HTML

Generates HTML summary content with stats and styling.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_summary_html(self, before_filename, after_filename, positive_changes, negative_changes, neutral_changes, total_patterns):
    """Format HTML summary with statistics and file info
    
    Args:
        before_filename: Before comparison file name
        after_filename: After comparison file name
        positive_changes: Count of positive changes
        negative_changes: Count of negative changes
        neutral_changes: Count of neutral changes
        total_patterns: Total pattern count
        
    Returns:
        str: HTML summary content
    """
    # Create summary section with dark theme and neon purple accents
    html = """
        <section class="summary">
            <h2>Comparison Summary</h2>
            <div class="file-info" style="background-color: #333333; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
    """
