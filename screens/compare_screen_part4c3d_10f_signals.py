#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10f: Charts Tab Signal Connections

Connects signals for chart tab UI components and handles user interactions.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

def connect_chart_signals(self):
    """Connect signals for chart tab UI components"""
    try:
        # Connect severity slider to value display and chart update
        self.chart_severity_slider.valueChanged.connect(self._handle_severity_change)
        
        # Connect category filter to chart update
        self.chart_category_combo.currentTextChanged.connect(self._handle_category_filter_change)
        
        # Connect normalize checkbox
        self.chart_normalize_check.stateChanged.connect(self._handle_normalize_toggle)
        
        # Connect export report button
        self.export_report_btn.clicked.connect(self._handle_report_export)
        
    except Exception as e:
        logging.error(f"Error connecting chart signals: {str(e)}")

def _handle_severity_change(self, value):
    """Handle changes to severity filter slider
    
    Args:
        value: New slider value
    """
    try:
        # Update label
        self.chart_severity_value.setText(str(value))
        
        # Update chart with new severity filter
        if hasattr(self, 'current_chart_type'):
            self.display_chart(self.current_chart_type)
    except Exception as e:
        logging.error(f"Error handling severity change: {str(e)}")

def _handle_category_filter_change(self, category):
    """Handle changes to category filter
    
    Args:
        category: Selected category text
    """
    try:
        # Update chart with new category filter
        if hasattr(self, 'current_chart_type'):
            self.display_chart(self.current_chart_type)
    except Exception as e:
        logging.error(f"Error handling category filter change: {str(e)}")

def _handle_normalize_toggle(self, state):
    """Handle toggling of normalize checkbox
    
    Args:
        state: Checkbox state
    """
    try:
        # Update chart with normalize setting
        if hasattr(self, 'current_chart_type'):
            self.display_chart(self.current_chart_type)
    except Exception as e:
        logging.error(f"Error handling normalize toggle: {str(e)}")
