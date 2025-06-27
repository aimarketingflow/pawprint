#!/usr/bin/env python3
"""
Compare Screen - Open Report

Opens generated HTML report in default browser.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
import webbrowser
import platform

logger = logging.getLogger(__name__)

def open_report_in_browser(file_path):
    """Open generated HTML report in default browser
    
    Args:
        file_path: Path to HTML report file
        
    Returns:
        bool: Success status
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"Report file not found: {file_path}")
            return False
            
        # Convert to URL format for browser
        file_url = f"file://{os.path.abspath(file_path)}"
        
        # Special handling for macOS to use Safari
        if platform.system() == "Darwin":  # macOS
            webbrowser.get('safari').open(file_url)
        else:
            # Use default browser on other platforms
            webbrowser.open(file_url)
            
        logger.info(f"Opened report in browser: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error opening report in browser: {str(e)}")
        return False
