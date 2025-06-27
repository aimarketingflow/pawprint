#!/usr/bin/env python3
"""
Compare Screen - Report Button

Creates and styles the report generation button.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

logger = logging.getLogger(__name__)

def create_report_button(self):
    """Create and style the report generation button
    
    Returns:
        QPushButton: Styled report button
    """
    try:
        # Create report button with dark theme and neon purple styling
        report_button = QPushButton("Generate Report")
        report_button.setMinimumSize(QSize(150, 40))
        report_button.setCursor(self.arrow_cursor)
        
        # Apply dark theme styling with neon purple accent
        report_button.setStyleSheet("""
            QPushButton {
                background-color: #bb86fc;
                color: #000000;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #a375df;
            }
            QPushButton:pressed {
                background-color: #8c5fc7;
            }
        """)
        
        logger.debug("Report button created and styled")
        return report_button
    except Exception as e:
        logger.error(f"Error creating report button: {str(e)}")
        return QPushButton("Generate Report")
