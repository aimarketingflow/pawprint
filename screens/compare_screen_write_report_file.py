#!/usr/bin/env python3
"""
Compare Screen - Write Report File

Handles writing HTML report content to file.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os

logger = logging.getLogger(__name__)

def write_report_file(self, file_path, html_content):
    """Write HTML report content to file
    
    Args:
        file_path: Path to save the report
        html_content: HTML report content
        
    Returns:
        bool: Success status
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write HTML content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        logger.info(f"Report saved successfully to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error saving report: {str(e)}")
        return False
