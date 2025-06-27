#!/usr/bin/env python3
"""
Compare Screen - Write JSON Data

Writes comparison data to JSON file for export.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def write_report_data_json(self, file_path, chart_data, before_file, after_file):
    """Write comparison data to JSON file
    
    Args:
        file_path: Path to save JSON file
        chart_data: Chart data dictionary
        before_file: Path to before comparison file
        after_file: Path to after comparison file
        
    Returns:
        bool: Success status
    """
    try:
        # Create export data structure with metadata
        export_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "before_file": before_file,
                "after_file": after_file,
                "tool_version": "2.0.0"
            },
            "chart_data": chart_data,
            "summary": {
                "positive_changes": sum(1 for p in chart_data.get('patterns', {}).values() 
                                     if p.get('after', 0) > p.get('before', 0)),
                "negative_changes": sum(1 for p in chart_data.get('patterns', {}).values() 
                                     if p.get('after', 0) < p.get('before', 0)),
                "neutral_changes": sum(1 for p in chart_data.get('patterns', {}).values() 
                                    if p.get('after', 0) == p.get('before', 0))
            }
        }
        
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write data to JSON file with pretty formatting
        with open(file_path, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        logger.info(f"Chart data exported to JSON: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing JSON data: {str(e)}")
        return False
