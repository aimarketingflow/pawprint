#!/usr/bin/env python3
"""
Compare Screen - Report Integration

Integrates report generation functionality with the main Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os

logger = logging.getLogger(__name__)

def integrate_report_functionality(self):
    """Integrate report generation functionality into Compare Screen
    
    Sets up report generation components, buttons, and handlers
    
    Returns:
        None
    """
    try:
        logger.info("Integrating report functionality into Compare Screen")
        
        # Add report button to UI
        report_button = self.create_report_button()
        self.connect_report_button(report_button)
        
        # Add export data button to UI
        export_button = self.create_export_data_button()
        self.connect_export_button(export_button)
        
        # Add save chart button to UI (if charts are available)
        if self.MATPLOTLIB_AVAILABLE:
            save_button = self.create_save_chart_button()
            self.connect_save_button(save_button)
            
        # Set up export directory for reports
        self.setup_export_directories()
        
        logger.debug("Report functionality integrated")
    except Exception as e:
        logger.error(f"Error integrating report functionality: {str(e)}")
        
def setup_export_directories(self):
    """Set up export directories for reports and data
    
    Returns:
        bool: Success status
    """
    try:
        # Set up base export directory in user's Documents
        home_dir = os.path.expanduser("~")
        export_base = os.path.join(home_dir, "Documents", "Pawprinting_Exports")
        
        # Create subdirectories for different export types
        report_dir = os.path.join(export_base, "reports")
        data_dir = os.path.join(export_base, "data")
        image_dir = os.path.join(export_base, "images")
        
        # Create directories if they don't exist
        os.makedirs(report_dir, exist_ok=True)
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(image_dir, exist_ok=True)
        
        # Store paths for later use
        self.export_base_dir = export_base
        self.report_export_dir = report_dir
        self.data_export_dir = data_dir
        self.image_export_dir = image_dir
        
        logger.debug(f"Export directories set up in {export_base}")
        return True
    except Exception as e:
        logger.error(f"Error setting up export directories: {str(e)}")
        return False
