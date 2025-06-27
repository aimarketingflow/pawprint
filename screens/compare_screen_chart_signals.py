#!/usr/bin/env python3
"""
Compare Screen - Chart Signals

Handles signal connections for chart components.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def connect_chart_signals(self):
    """Connect signals for chart components
    
    Returns:
        bool: Success status
    """
    try:
        # Connect chart type selector
        if hasattr(self, 'chart_type_combo') and self.chart_type_combo:
            self.chart_type_combo.currentIndexChanged.connect(self.on_chart_type_changed)
            
        # Connect export button
        if hasattr(self, 'export_chart_button') and self.export_chart_button:
            self.export_chart_button.clicked.connect(self.on_export_chart_clicked)
            
        # Connect refresh button
        if hasattr(self, 'refresh_chart_button') and self.refresh_chart_button:
            self.refresh_chart_button.clicked.connect(self.on_refresh_chart_clicked)
