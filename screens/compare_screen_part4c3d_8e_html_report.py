#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8e: HTML Report Generator

Creates HTML reports with styling for comparison results.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

def export_html_report(self, file_path=None):
    """Export comparison report as styled HTML
    
    Args:
        file_path: Optional file path
        
    Returns:
        str: Path to created file or None
    """
    try:
        # Generate default path if needed
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            export_dir = os.path.join(os.path.expanduser("~"), 
                         "Documents", "Pawprinting_Exports", "Reports")
            os.makedirs(export_dir, exist_ok=True)
            file_path = os.path.join(export_dir, f"comparison_report_{timestamp}.html")
        
        # Generate HTML content
        html_content = self._generate_html_report()
        
        # Write to file
        with open(file_path, 'w') as f:
            f.write(html_content)
            
        return file_path
        
    except Exception as e:
        logging.error(f"Export HTML report error: {e}")
        return None
