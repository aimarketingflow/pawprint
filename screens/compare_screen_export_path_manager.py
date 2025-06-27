#!/usr/bin/env python3
"""
Compare Screen - Export Path Manager

Manages export paths for different file types.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def get_export_path(self, export_type):
    """Get export path for specific file type
    
    Args:
        export_type: Type of export ('report', 'data', or 'image')
        
    Returns:
        str: Path to export directory or None if error
    """
    try:
        # Get base export path
        if not hasattr(self, 'export_base_dir'):
            self.setup_export_directories()
            
        # Get specific export directory based on type
        if export_type == 'report':
            export_dir = self.report_export_dir if hasattr(self, 'report_export_dir') else None
        elif export_type == 'data':
            export_dir = self.data_export_dir if hasattr(self, 'data_export_dir') else None
        elif export_type == 'image':
            export_dir = self.image_export_dir if hasattr(self, 'image_export_dir') else None
        else:
            # Default to base export directory
            export_dir = self.export_base_dir if hasattr(self, 'export_base_dir') else None
            
        # If no specific directory found, create a default one
        if not export_dir:
            home_dir = os.path.expanduser("~")
            export_dir = os.path.join(home_dir, "Documents", "Pawprinting_Exports", export_type)
            
        # Create directory if it doesn't exist
        os.makedirs(export_dir, exist_ok=True)
        
        # Store as last used export path
        self.last_export_path = export_dir
        
        logger.debug(f"Export path for {export_type}: {export_dir}")
        return export_dir
    except Exception as e:
        logger.error(f"Error getting export path: {str(e)}")
        return None
