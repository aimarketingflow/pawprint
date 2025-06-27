#!/usr/bin/env python3
"""
Compare Screen - JSON Export

Handles JSON export functionality for chart data.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def export_to_json(self, data, export_path):
    """Export data to JSON file
    
    Args:
        data: Data to export
        export_path: Directory to save the file
        
    Returns:
        tuple: (success, file_path)
    """
    try:
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"pawprinting_chart_data_{timestamp}.json"
        
        # Build full file path
        file_path = os.path.join(export_path, filename)
