#!/usr/bin/env python3
"""
Compare Screen - Export Data

Exports chart data to JSON format.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def export_chart_data(self, chart_data):
    """Export chart data to JSON file
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        bool: Success status, and file path if successful
    """
    try:
        # Get export paths
        export_paths = self.get_export_paths()
        
        # Ensure directories exist
        if not self.ensure_export_directories(export_paths):
            logger.error("Failed to create export directories")
            return False, ""
