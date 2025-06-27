#!/usr/bin/env python3
"""
Compare Screen - Export Data Complete

Completes the data export process and handles JSON file operations.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def complete_data_export(self, chart_data, export_path):
    """Complete data export with file operations
    
    Args:
        chart_data: Chart data dictionary
        export_path: Path to save the JSON data
        
    Returns:
        None
    """
    try:
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pawprinting_comparison_data_{timestamp}.json"
        
        # Build full file path
        file_path = os.path.join(export_path, filename)
        
        # Get file names for data
        before_file = self.before_file if hasattr(self, 'before_file') else "Unknown"
        after_file = self.after_file if hasattr(self, 'after_file') else "Unknown"
        
        # Write data to JSON file
        success = self.write_report_data_json(file_path, chart_data, before_file, after_file)
        
        # Show notification to user
        self.show_data_export_notification(success, file_path)
        
    except Exception as e:
        logger.error(f"Error completing data export: {str(e)}")
        self.show_error_dialog("Export Error", 
                             f"An error occurred during data export: {str(e)}")
