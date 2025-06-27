#!/usr/bin/env python3
"""
Compare Screen - Report Notification

Handles notifications for report generation success/failure.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QMessageBox

logger = logging.getLogger(__name__)

def show_report_notification(self, success, file_path):
    """Show notification for report generation result
    
    Args:
        success: Whether the report was saved successfully
        file_path: Path where the report was saved
        
    Returns:
        None
    """
    try:
        if success:
            # Success notification with dark theme styling
            msg = QMessageBox(self)
            msg.setWindowTitle("Report Generated")
            msg.setText("Comparison report generated successfully!")
            msg.setInformativeText(f"The report has been saved to:\n{file_path}")
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
            logger.info("Report success notification displayed")
        else:
            # Error notification
            msg = QMessageBox(self)
            msg.setWindowTitle("Report Generation Failed")
            msg.setText("Failed to generate comparison report.")
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
            logger.error("Report failure notification displayed")
    except Exception as e:
        logger.error(f"Error showing report notification: {str(e)}")
