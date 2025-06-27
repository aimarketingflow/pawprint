#!/usr/bin/env python3
"""
Compare Screen - Export Report Data

Exports report data as JSON file.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def export_report_data_json(self, chart_data, before_file, after_file, export_path):
    """Export report data as JSON file
    
    Args:
        chart_data: Chart data dictionary
        before_file: Before comparison file
        after_file: After comparison file
        export_path: Path to save the JSON data
        
    Returns:
        tuple: (success, file_path)
    """
    try:
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pawprinting_report_data_{timestamp}.json"
        
        # Build full file path
        file_path = os.path.join(export_path, filename)
