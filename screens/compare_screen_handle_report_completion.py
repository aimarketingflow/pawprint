#!/usr/bin/env python3
"""
Compare Screen - Handle Report Completion

Handles actions after report generation is complete.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os

logger = logging.getLogger(__name__)

def handle_report_completion(self, success, file_path):
    """Handle actions after report generation completes
    
    Shows notification and optionally opens the report
    
    Args:
        success: Whether report generation was successful
        file_path: Path to the generated report file
        
    Returns:
        None
    """
    try:
        if not success:
            logger.warning("Report generation failed - showing error dialog")
            self.show_error_dialog("Report Generation Failed", 
                                  "Failed to generate the comparison report.")
            return
        
        # Import required functions
        from .compare_screen_report_success_notification import show_report_success_notification
        from .compare_screen_open_report import open_report_in_browser
        
        # Show success notification and get user's choice
        open_report = show_report_success_notification(self, file_path)
        
        # Open report in browser if user requested
        if open_report:
            logger.info("User requested to open report in browser")
            open_report_in_browser(file_path)
        
        # Log completion
        logger.info(f"Report generation completed successfully: {file_path}")
        
    except Exception as e:
        logger.error(f"Error handling report completion: {str(e)}")
        self.show_error_dialog("Error", 
                              f"An error occurred after report generation: {str(e)}")
