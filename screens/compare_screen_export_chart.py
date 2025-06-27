#!/usr/bin/env python3
"""
Compare Screen - Export Chart

Handles chart image export functionality.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging

logger = logging.getLogger(__name__)

def export_current_chart(self):
    """Export current chart to image file
    
    Returns:
        bool: Success status
    """
    try:
        # Check if matplotlib is available
        if not self.MATPLOTLIB_AVAILABLE:
            logger.error("Cannot export chart - matplotlib not available")
            return False
            
        # Get export paths
        export_paths = self.get_export_paths()
        
        # Ensure directories exist
        if not self.ensure_export_directories(export_paths):
            logger.error("Failed to create export directories")
            return False
            
        # Get current chart type
        chart_type = "Bar Chart"  # Default
        if hasattr(self, 'chart_type_combo') and self.chart_type_combo:
            chart_type = self.chart_type_combo.currentText()
