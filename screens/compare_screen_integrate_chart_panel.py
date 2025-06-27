#!/usr/bin/env python3
"""
Compare Screen - Integrate Chart Panel

Integrates the chart panel into the main Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def integrate_chart_panel(self, main_layout):
    """Integrate chart panel into the main Compare Screen layout
    
    Args:
        main_layout: Main layout of the Compare Screen
        
    Returns:
        None
    """
    try:
        # Create chart panel widget
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
        
        # Complete chart panel setup
        chart_panel = self.complete_chart_panel_widget(
            chart_panel, chart_widget, chart_selector, button_layout
        )
        
        # Store references for later use
        self.chart_widget = chart_widget
        self.chart_selector = chart_selector
        
        # Add to main layout at the appropriate position
        # Assuming main layout is set up to accommodate the chart panel
        main_layout.addWidget(chart_panel)
        
        logger.debug("Chart panel integrated into Compare Screen")
    except Exception as e:
        logger.error(f"Error integrating chart panel: {str(e)}")
