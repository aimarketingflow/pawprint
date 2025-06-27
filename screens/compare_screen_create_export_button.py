#!/usr/bin/env python3
"""
Compare Screen - Create Export Button

Creates and styles the export data button.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

logger = logging.getLogger(__name__)

def create_export_data_button(self):
    """Create and style the export data button
    
    Returns:
        QPushButton: Styled export button
    """
    try:
        # Create export button with dark theme styling
        export_button = QPushButton("Export Data")
        export_button.setMinimumSize(QSize(150, 40))
        export_button.setCursor(self.arrow_cursor)
        
        # Apply dark theme styling with teal accent
        export_button.setStyleSheet("""
            QPushButton {
                background-color: #03dac6;
                color: #000000;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #66fff8;
            }
            QPushButton:pressed {
                background-color: #018786;
            }
        """)
        
        logger.debug("Export data button created and styled")
        return export_button
    except Exception as e:
        logger.error(f"Error creating export button: {str(e)}")
        return QPushButton("Export Data")
