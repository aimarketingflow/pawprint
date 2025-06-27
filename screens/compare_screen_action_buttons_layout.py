#!/usr/bin/env python3
"""
Compare Screen - Action Buttons Layout

Creates a horizontal layout for chart action buttons.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QHBoxLayout

logger = logging.getLogger(__name__)

def create_action_buttons_layout(self, report_button, export_button):
    """Create horizontal layout for chart action buttons
    
    Args:
        report_button: Report generation button
        export_button: Data export button
        
    Returns:
        QHBoxLayout: Horizontal layout with buttons
    """
    try:
        # Create horizontal layout for buttons with spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch(1)
        button_layout.addWidget(export_button)
        button_layout.addWidget(report_button)
        
        logger.debug("Chart action buttons layout created")
        return button_layout
    except Exception as e:
        logger.error(f"Error creating action buttons layout: {str(e)}")
        return QHBoxLayout()
