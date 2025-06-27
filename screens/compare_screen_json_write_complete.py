#!/usr/bin/env python3
"""
Compare Screen - JSON Write Complete

Completes JSON file writing process with error handling.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

def complete_json_write(self, serializable_data, file_path):
    """Complete JSON file writing with proper error handling
    
    Args:
        serializable_data: Data prepared for serialization
        file_path: Path to JSON file
        
    Returns:
        bool: Success status
    """
    try:
        # Write to file with pretty formatting
        with open(file_path, 'w') as f:
            json.dump(serializable_data, f, indent=4)
            
        logger.info(f"Chart data exported to: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error writing JSON file: {str(e)}")
        return False
