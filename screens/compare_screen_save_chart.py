#!/usr/bin/env python3
"""
Compare Screen - Save Chart

Saves chart to file on disk.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

def save_chart_to_file(self, export_path, filename):
    """Save current chart figure to file
    
    Args:
        export_path: Path to save the file
        filename: Filename to use
        
    Returns:
        bool: Success status
    """
    try:
        # Build full file path
        file_path = os.path.join(export_path, filename)
        
        # Save figure
        self.chart_figure.savefig(
            file_path,
            dpi=150,
            bbox_inches='tight',
            facecolor=self.chart_figure.get_facecolor()
        )
        
        logger.info(f"Chart exported to: {file_path}")
        return True, file_path
