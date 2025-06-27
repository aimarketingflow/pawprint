#!/usr/bin/env python3
"""
Compare Screen - Export Filenames

Generates filenames for chart exports with timestamps.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_export_filename(self, chart_type, file_extension=".png"):
    """Generate export filename with timestamp
    
    Args:
        chart_type: Type of chart being exported
        file_extension: File extension for the export
        
    Returns:
        str: Generated filename
    """
    try:
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Format chart type for filename (remove spaces)
        chart_type_clean = chart_type.lower().replace(" ", "_")
        
        # Build filename
        filename = f"pawprinting_chart_{chart_type_clean}_{timestamp}{file_extension}"
        
        return filename
    except Exception as e:
        logger.error(f"Error generating export filename: {str(e)}")
        return f"pawprinting_chart_export{file_extension}"
