#!/usr/bin/env python3
"""
Compare Screen - Save Chart Settings

Saves user preferences for chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
import json

logger = logging.getLogger(__name__)

def save_chart_settings(self):
    """Save chart settings to user preferences file
    
    Returns:
        bool: Success status
    """
    try:
        if not hasattr(self, 'chart_selector'):
            return False
            
        # Get current settings
        settings = {
            'chart_type': self.chart_selector.currentText(),
            'last_export_path': self.last_export_path if hasattr(self, 'last_export_path') else None
        }
        
        # Get path to settings file
        home_dir = os.path.expanduser("~")
        settings_dir = os.path.join(home_dir, "Documents", "Pawprinting_Settings")
        os.makedirs(settings_dir, exist_ok=True)
        
        settings_file = os.path.join(settings_dir, "chart_preferences.json")
        
        # Write settings to file
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
            
        logger.debug(f"Chart settings saved to {settings_file}")
        return True
    except Exception as e:
        logger.error(f"Error saving chart settings: {str(e)}")
        return False
