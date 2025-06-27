#!/usr/bin/env python3
"""
Compare Screen - Report Data JSON

Formats and writes report data to JSON file.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import json
import os

logger = logging.getLogger(__name__)

def write_report_data_json(self, file_path, chart_data, before_file, after_file):
    """Write report data to JSON file
    
    Args:
        file_path: Path to save the JSON file
        chart_data: Chart data dictionary
        before_file: Before comparison file
        after_file: After comparison file
        
    Returns:
        bool: Success status
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Add file information to export data
        data = {
            "before_file": before_file,
            "after_file": after_file,
            "chart_data": chart_data
        }
        
        # Write JSON data to file with pretty formatting
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Report data JSON saved successfully to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving report data JSON: {str(e)}")
        return False
