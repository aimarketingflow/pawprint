#!/usr/bin/env python3
"""
Compare Screen - Report Handler

Event handler for report generation button clicks.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os

logger = logging.getLogger(__name__)

def generate_report(self):
    """Handle report button click event
    
    Extracts chart data and generates a complete HTML report
    
    Returns:
        None
    """
    try:
        logger.info("Report generation requested")
        
        # Check if we have valid chart data
        chart_data = self.extract_chart_data()
        if not chart_data:
            logger.warning("No chart data available for report")
            self.show_error_dialog("No Data Available", 
                                  "There is no comparison data available to generate a report.")
            return
            
        # Get export path
        export_path = self.get_export_path("reports")
        if not export_path:
            logger.warning("Failed to create export directory for report")
            self.show_error_dialog("Export Error", 
                                  "Failed to create export directory for report.")
            return
