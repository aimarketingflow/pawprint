#!/usr/bin/env python3
"""
Compare Screen - Charts Unavailable

Creates placeholder widget when matplotlib is unavailable.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)

def create_charts_unavailable_widget(self):
    """Create placeholder widget when charts are unavailable
    
    Returns:
        QWidget: Placeholder widget with notification
    """
    try:
        # Create placeholder widget
        placeholder = QWidget()
        layout = QVBoxLayout()
        
        # Create notification label
        message = QLabel("Charts functionality is unavailable.\nPlease install matplotlib to enable charts.")
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setStyleSheet("""
            QLabel {
                color: #bb86fc;
                font-size: 16px;
                padding: 20px;
                background-color: #1e1e1e;
                border: 1px solid #333333;
                border-radius: 8px;
            }
        """)
        
        layout.addWidget(message)
        placeholder.setLayout(layout)
        
        # Apply dark theme styling
        placeholder.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
            }
        """)
        
        logger.warning("Charts unavailable widget created - matplotlib not found")
        return placeholder
    except Exception as e:
        logger.error(f"Error creating charts unavailable widget: {str(e)}")
        return QWidget()
