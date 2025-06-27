#!/usr/bin/env python3
"""
Compare Screen - Export Paths

Manages export paths for chart images and data.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

def get_export_paths(self):
    """Get export paths for chart images and data
    
    Returns:
        dict: Dictionary of export paths
    """
    try:
        # Base export path in user Documents
        base_path = os.path.join(str(Path.home()), "Documents", "Pawprinting_Exports")
        
        # Create specific paths
        image_path = os.path.join(base_path, "images")
        data_path = os.path.join(base_path, "data")
        reports_path = os.path.join(base_path, "reports")
