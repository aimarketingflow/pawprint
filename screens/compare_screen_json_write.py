#!/usr/bin/env python3
"""
Compare Screen - JSON Write

Handles JSON file writing for chart data export.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import json
import logging

logger = logging.getLogger(__name__)

def write_json_file(self, data, file_path):
    """Write data to JSON file
    
    Args:
        data: Data to write
        file_path: Path to JSON file
        
    Returns:
        bool: Success status
    """
    try:
        # Format data for JSON serialization
        serializable_data = {}
        
        # Copy only serializable fields
        if 'patterns' in data:
            serializable_data['patterns'] = data['patterns']
        if 'pattern_names' in data:
            serializable_data['pattern_names'] = data['pattern_names']
