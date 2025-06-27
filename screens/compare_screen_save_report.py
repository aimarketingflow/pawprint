#!/usr/bin/env python3
"""
Compare Screen - Save Report

Handles saving HTML reports to file.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def save_report_to_file(self, html_content, export_path):
    """Save HTML report to file
    
    Args:
        html_content: HTML report content
        export_path: Path to save the report
        
    Returns:
        tuple: (success, file_path)
    """
    try:
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pawprinting_comparison_report_{timestamp}.html"
        
        # Build full file path
        file_path = os.path.join(export_path, filename)
