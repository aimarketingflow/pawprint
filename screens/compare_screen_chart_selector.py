#!/usr/bin/env python3
"""
Compare Screen - Chart Selector

Handles chart type selection and UI updates.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QComboBox

logger = logging.getLogger(__name__)

def initialize_chart_selector(self):
    """Initialize chart type selector combo box
    
    Returns:
        bool: Success status
    """
    try:
        # Create chart selector if needed
        if not hasattr(self, 'chart_type_combo') or not self.chart_type_combo:
            self.chart_type_combo = QComboBox()
            
        # Configure chart types
        self.chart_type_combo.clear()
        self.chart_type_combo.addItems(['Bar Chart', 'Pie Chart', 'Radar Chart'])
        
        # Style the combo box for dark theme
        self.chart_type_combo.setStyleSheet("""
            QComboBox {
                background-color: #333333;
                color: #dddddd;
                border: 1px solid #555555;
                padding: 5px;
            }
        """)
