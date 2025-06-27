#!/usr/bin/env python3
"""
Compare Screen - Chart Panel Layout

Creates vertical layout combining chart and action buttons.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QVBoxLayout, QWidget

logger = logging.getLogger(__name__)

def create_chart_panel_layout(self, chart_widget, chart_selector, button_layout):
    """Create vertical layout combining chart display and actions
    
    Args:
        chart_widget: Chart display widget
        chart_selector: Chart type selector combo box
        button_layout: Horizontal layout with action buttons
        
    Returns:
        QVBoxLayout: Vertical layout with chart components
    """
    try:
        # Create vertical layout for chart panel
        chart_panel_layout = QVBoxLayout()
        chart_panel_layout.setContentsMargins(10, 10, 10, 10)
        chart_panel_layout.setSpacing(10)
        
        # Add chart type selector
        chart_panel_layout.addWidget(chart_selector)
        
        # Add chart display widget
        chart_panel_layout.addWidget(chart_widget)
        
        # Add action buttons layout
        chart_panel_layout.addLayout(button_layout)
        
        logger.debug("Chart panel layout created")
        return chart_panel_layout
    except Exception as e:
        logger.error(f"Error creating chart panel layout: {str(e)}")
        return QVBoxLayout()
