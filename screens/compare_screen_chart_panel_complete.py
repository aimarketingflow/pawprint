#!/usr/bin/env python3
"""
Compare Screen - Chart Panel Complete

Completes the chart panel widget creation with layout setup.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)

def complete_chart_panel_widget(self, chart_panel, chart_widget, chart_selector, button_layout):
    """Complete chart panel widget setup with layout
    
    Args:
        chart_panel: Chart panel widget
        chart_widget: Chart display widget
        chart_selector: Chart type selector combo box
        button_layout: Horizontal layout with action buttons
        
    Returns:
        QWidget: Fully configured chart panel widget
    """
    try:
        # Create chart panel layout
        chart_panel_layout = self.create_chart_panel_layout(
            chart_widget, chart_selector, button_layout
        )
        
        # Set layout on panel widget
        chart_panel.setLayout(chart_panel_layout)
        
        # Apply dark theme styling
        chart_panel.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 8px;
            }
        """)
        
        logger.debug("Chart panel widget completed")
        return chart_panel
    except Exception as e:
        logger.error(f"Error completing chart panel: {str(e)}")
        return chart_panel
