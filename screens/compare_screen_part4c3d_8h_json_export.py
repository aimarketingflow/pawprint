#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8h: JSON Export

Exports comparison data in JSON format.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import json
import logging
from datetime import datetime

def export_json_data(self, file_path=None):
    """Export comparison data as JSON
    
    Args:
        file_path: Optional file path
        
    Returns:
        str: Path to created file or None
    """
    try:
        # Generate default path if needed
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            export_dir = os.path.join(os.path.expanduser("~"), 
                         "Documents", "Pawprinting_Exports", "Data")
            os.makedirs(export_dir, exist_ok=True)
            file_path = os.path.join(export_dir, f"comparison_data_{timestamp}.json")
        
        # Prepare exportable data
        export_data = self._prepare_json_export_data()
        
        # Write to file with pretty formatting
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        return file_path
        
    except Exception as e:
        logging.error(f"Export JSON error: {e}")
        return None
