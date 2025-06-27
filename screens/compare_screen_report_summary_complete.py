#!/usr/bin/env python3
"""
Compare Screen - Report Summary Complete

Completes the summary section for comparison reports with HTML formatting.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os.path

logger = logging.getLogger(__name__)

def complete_report_summary(self, before_file, after_file, positive_changes, negative_changes, neutral_changes):
    """Complete HTML summary section with file details and statistics
    
    Args:
        before_file: Before comparison file
        after_file: After comparison file
        positive_changes: Count of positive changes
        negative_changes: Count of negative changes
        neutral_changes: Count of neutral changes
        
    Returns:
        str: HTML summary section
    """
    # Format file paths to show just filename when possible
    before_filename = os.path.basename(before_file) if before_file != "Unknown" else "Unknown"
    after_filename = os.path.basename(after_file) if after_file != "Unknown" else "Unknown"
