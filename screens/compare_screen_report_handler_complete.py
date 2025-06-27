#!/usr/bin/env python3
"""
Compare Screen - Report Handler Complete

Completes the report generation process and handles file operations.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def complete_report_generation(self, chart_data, export_path):
    """Complete report generation with file operations
    
    Args:
        chart_data: Chart data dictionary
        export_path: Path to save the report
        
    Returns:
        None
    """
    try:
        # Get file names for report
        before_file = self.before_file if hasattr(self, 'before_file') else "Unknown"
        after_file = self.after_file if hasattr(self, 'after_file') else "Unknown"
        
        # Generate the report
        success, file_path = self.generate_comparison_report(
            chart_data, before_file, after_file, export_path
        )
        
        # Show notification to user
        self.show_report_notification(success, file_path)
        
    except Exception as e:
        logger.error(f"Error completing report generation: {str(e)}")
        self.show_error_dialog("Report Error", 
                             f"An error occurred during report generation: {str(e)}")
