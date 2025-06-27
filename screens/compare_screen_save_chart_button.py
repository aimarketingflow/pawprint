#!/usr/bin/env python3
"""
Compare Screen - Save Chart Button

Creates and styles the save chart button.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize

logger = logging.getLogger(__name__)

def create_save_chart_button(self):
    """Create and style the save chart button
    
    Returns:
        QPushButton: Styled save chart button
    """
    try:
        # Create save chart button with dark theme styling
        save_button = QPushButton("Save Image")
        save_button.setMinimumSize(QSize(150, 40))
        save_button.setCursor(self.arrow_cursor)
        
        # Apply dark theme styling with blue accent
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #3700b3;
                color: #ffffff;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #6200ee;
            }
            QPushButton:pressed {
                background-color: #2a0086;
            }
        """)
        
        logger.debug("Save chart button created and styled")
        return save_button
    except Exception as e:
        logger.error(f"Error creating save chart button: {str(e)}")
        return QPushButton("Save Image")
