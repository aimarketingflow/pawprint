#!/usr/bin/env python3
"""
Compare Screen - Error Dialog

Shows styled error dialog messages.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

def show_error_dialog(self, title, message):
    """Show error dialog with dark theme styling
    
    Args:
        title: Dialog title
        message: Error message
        
    Returns:
        None
    """
    try:
        # Create styled error message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Icon.Critical)
        
        # Apply dark theme styling
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #121212;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #cf6679;
                color: #000000;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff94a1;
            }
        """)
        
        msg_box.exec()
        logger.debug(f"Error dialog shown: {title} - {message}")
    except Exception as e:
        # Fallback if custom dialog fails
        logger.error(f"Failed to show error dialog: {str(e)}")
        QMessageBox.critical(self, title, message)
