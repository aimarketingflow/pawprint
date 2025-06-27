#!/usr/bin/env python3
"""
Compare Screen - Report Button Handler

Handles report button click events.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def on_report_button_clicked(self):
    """Handle report button click event
    
    Extracts data, generates report, and handles completion
    
    Returns:
        None
    """
    try:
        logger.info("Report generation requested")
        
        # Check if we have valid comparison data
        chart_data = self.extract_chart_data()
        if not chart_data or not chart_data.get('patterns'):
            logger.warning("No comparison data available for report")
            self.show_error_dialog("No Data Available", 
                                  "There is no comparison data available to generate a report.")
            return
            
        # Get export path for report
        export_path = self.get_export_path("report")
        if not export_path:
            logger.warning("Failed to create export directory for report")
            self.show_error_dialog("Export Error", 
                                  "Failed to create export directory for report generation.")
            return
            
        # Get file names for report
        before_file = self.before_file if hasattr(self, 'before_file') else "Unknown"
        after_file = self.after_file if hasattr(self, 'after_file') else "Unknown"
        
        # Generate report
        success, file_path = self.generate_comparison_report(
            chart_data, before_file, after_file, export_path
        )
        
        # Handle report completion (notification and opening)
        self.handle_report_completion(success, file_path)
        
    except Exception as e:
        logger.error(f"Error handling report button click: {str(e)}")
        self.show_error_dialog("Report Error", 
                              f"An error occurred during report generation: {str(e)}")
