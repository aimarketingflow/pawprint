#!/usr/bin/env python3
"""
Compare Screen - Report Success Notification

Shows notification for successful report generation.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)

def show_report_success_notification(self, file_path):
    """Show notification for successful report generation
    
    Args:
        file_path: Path to the generated report file
        
    Returns:
        bool: User's choice to open report (True) or not (False)
    """
    try:
        filename = os.path.basename(file_path)
        
        # Create styled message box
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Report Generated")
        msg_box.setText("Comparison report generated successfully!")
        msg_box.setInformativeText(f"Report saved as:\n{filename}\n\nWould you like to open it now?")
        msg_box.setIcon(QMessageBox.Icon.Information)
        
        # Configure buttons
        open_button = msg_box.addButton("Open Report", QMessageBox.ButtonRole.AcceptRole)
        close_button = msg_box.addButton("Close", QMessageBox.ButtonRole.RejectRole)
        
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
                background-color: #bb86fc;
                color: #000000;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d7b8fc;
            }
        """)
        
        # Show dialog and process result
        msg_box.exec()
        
        # Return true if user clicked Open Report
        result = (msg_box.clickedButton() == open_button)
        
        logger.debug(f"Report success notification shown, open report: {result}")
        return result
    except Exception as e:
        logger.error(f"Error showing report success notification: {str(e)}")
        return False
