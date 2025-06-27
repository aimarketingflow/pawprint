#!/usr/bin/env python3
"""
Compare Screen - Report Error Handling

Handles errors during report generation process.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

def show_error_dialog(self, title, message):
    """Show error dialog with dark theme styling
    
    Args:
        title: Error dialog title
        message: Error message
        
    Returns:
        None
    """
    try:
        # Create error dialog with dark theme styling
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
        
        # Apply dark theme styling
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
                color: #ffffff;
            }
            QPushButton {
                background-color: #bb86fc;
                color: #000000;
                padding: 5px 15px;
                border-radius: 4px;
            }
        """)
        
        msg.exec()
        logger.warning(f"Error dialog displayed: {title} - {message}")
    except Exception as e:
        logger.error(f"Error showing error dialog: {str(e)}")
