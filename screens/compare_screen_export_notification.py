#!/usr/bin/env python3
"""
Compare Screen - Export Notification

Handles notifications for successful chart exports.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

def show_export_notification(self, success, file_path=""):
    """Show notification for export result
    
    Args:
        success: Whether export was successful
        file_path: Path to exported file
        
    Returns:
        None
    """
    try:
        if success and file_path:
            msg = QMessageBox()
            msg.setWindowTitle("Export Successful")
            msg.setText(f"Chart exported successfully!")
            msg.setInformativeText(f"Saved to:\n{file_path}")
            msg.setIcon(QMessageBox.Icon.Information)
