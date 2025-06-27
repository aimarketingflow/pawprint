#!/usr/bin/env python3
"""
Compare Screen - Load Chart Settings

Loads and applies user preferences for chart visualization.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
import json

logger = logging.getLogger(__name__)

def load_chart_settings(self):
    """Load chart settings from user preferences file
    
    Returns:
        dict: Chart settings or None if error
    """
    try:
        # Get path to settings file
        home_dir = os.path.expanduser("~")
        settings_dir = os.path.join(home_dir, "Documents", "Pawprinting_Settings")
        settings_file = os.path.join(settings_dir, "chart_preferences.json")
        
        # Check if settings file exists
        if not os.path.isfile(settings_file):
            logger.debug("No chart settings file found, using defaults")
            return {
                'chart_type': 'Bar Chart',
                'last_export_path': None
            }
        
        # Read settings from file
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            
        logger.debug(f"Chart settings loaded from {settings_file}")
        
        # Apply settings if chart selector exists
        if hasattr(self, 'chart_selector') and 'chart_type' in settings:
            idx = self.chart_selector.findText(settings['chart_type'])
            if idx >= 0:
                self.chart_selector.setCurrentIndex(idx)
                
        # Store last export path if available
        if 'last_export_path' in settings and settings['last_export_path']:
            self.last_export_path = settings['last_export_path']
            
        return settings
    except Exception as e:
        logger.error(f"Error loading chart settings: {str(e)}")
        return None
