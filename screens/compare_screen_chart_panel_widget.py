#!/usr/bin/env python3
"""
Compare Screen - Chart Panel Widget

Creates a container widget for the chart panel.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)

def create_chart_panel_widget(self):
    """Create chart panel widget with all components
    
    Returns:
        QWidget: Panel containing chart display and controls
    """
    try:
        # Create container widget
        chart_panel = QWidget()
        
        # Create chart selector
        chart_selector = self.create_chart_selector()
        
        # Create chart display widget
        chart_widget = self.create_chart_display_widget()
        
        # Create action buttons
        report_button = self.create_report_button()
        export_button = self.create_export_data_button()
        
        # Connect buttons to handlers
        self.connect_report_button(report_button)
        self.connect_export_button(export_button)
        
        # Create button layout
        button_layout = self.create_action_buttons_layout(report_button, export_button)
