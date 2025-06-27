#!/usr/bin/env python3
"""
Compare Screen - Create Export Directories

Creates export directories for charts and data if they don't exist.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def ensure_export_directories(self, export_paths):
    """Create export directories if they don't exist
    
    Args:
        export_paths: Dictionary of export paths
        
    Returns:
        bool: Success status
    """
    try:
        # Create each directory if it doesn't exist
        for path_name, path in export_paths.items():
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info(f"Created export directory: {path}")
                
        return True
    except Exception as e:
        logger.error(f"Error creating export directories: {str(e)}")
        return False
