#!/usr/bin/env python3
"""
Compare Screen - Export Data Handler

Event handler for data export button clicks.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def export_chart_data(self):
    """Handle export data button click event
    
    Extracts chart data and exports it as JSON
    
    Returns:
        None
    """
    try:
        logger.info("Chart data export requested")
        
        # Check if we have valid chart data
        chart_data = self.extract_chart_data()
        if not chart_data:
            logger.warning("No chart data available for export")
            self.show_error_dialog("No Data Available", 
                                  "There is no comparison data available to export.")
            return
            
        # Get export path for data
        export_path = self.get_export_path("data")
        if not export_path:
            logger.warning("Failed to create export directory for data")
            self.show_error_dialog("Export Error", 
                                  "Failed to create export directory for data export.")
            return
