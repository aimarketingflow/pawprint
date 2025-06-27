#!/usr/bin/env python3
"""
Compare Screen - Data Export Notification

Provides notifications for data export operations.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

def show_data_export_notification(self, success, file_path):
    """Show notification for data export result
    
    Args:
        success: Whether the data was exported successfully
        file_path: Path where the data was saved
        
    Returns:
        None
    """
    try:
        if success:
            # Success notification with dark theme styling
            msg = QMessageBox(self)
            msg.setWindowTitle("Data Exported")
            msg.setText("Chart data exported successfully!")
            msg.setInformativeText(f"The data has been saved to:\n{file_path}")
            msg.setIcon(QMessageBox.Icon.Information)
            
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
            logger.info("Data export success notification displayed")
        else:
            # Error notification
            self.show_error_dialog("Data Export Failed", "Failed to export chart data.")
    except Exception as e:
        logger.error(f"Error showing data export notification: {str(e)}")
