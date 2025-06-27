#!/usr/bin/env python3
"""
Compare Screen - Expanded Action Buttons

Creates an expanded horizontal layout for chart action buttons.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QHBoxLayout

logger = logging.getLogger(__name__)

def create_expanded_action_buttons_layout(self):
    """Create expanded horizontal layout for all chart action buttons
    
    Returns:
        QHBoxLayout: Horizontal layout with all action buttons
    """
    try:
        # Create all buttons
        report_button = self.create_report_button()
        export_button = self.create_export_data_button()
        save_button = self.create_save_chart_button()
        
        # Connect buttons to handlers
        self.connect_report_button(report_button)
        self.connect_export_button(export_button)
        self.connect_save_button(save_button)
        
        # Create horizontal layout for buttons with spacing
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch(1)
        button_layout.addWidget(save_button)
        button_layout.addWidget(export_button)
        button_layout.addWidget(report_button)
        
        logger.debug("Expanded chart action buttons layout created")
        return button_layout
    except Exception as e:
        logger.error(f"Error creating expanded action buttons layout: {str(e)}")
        return QHBoxLayout()
