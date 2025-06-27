#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10i: Charts Tab Initialization

Main entry point for initializing the charts tab and integrating it into the main tab widget.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os

def initialize_charts_tab(self):
    """Initialize the charts tab and add it to the main tab widget
    
    This is the main entry point for charts tab setup from the CompareScreen class.
    """
    try:
        # Check matplotlib availability
        try:
            import matplotlib
            self.MATPLOTLIB_AVAILABLE = True
        except ImportError:
            self.MATPLOTLIB_AVAILABLE = False
            logging.warning("Matplotlib not available. Charts functionality will be limited.")
        
        # Set up default attributes
        self.current_chart_type = None
        self.current_chart_data = None
        self.diff_data_extracted = False
        self.chart_views = {}  # Store different views for chart types
        
        # Create directories for exports if they don't exist
        export_dirs = [
            os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports"),
            os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Images"),
            os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Data"),
            os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_Exports", "Reports"),
        ]
        for directory in export_dirs:
            os.makedirs(directory, exist_ok=True)
        
        # Assemble tab components and layout
        self.charts_tab = self.assemble_charts_tab_layout()
        
        # Connect signals
        self.connect_chart_signals()
        
        # Add to main tab widget if it exists
        if hasattr(self, 'tab_widget'):
            self.tab_widget.addTab(self.charts_tab, "Charts")
            
        # Set radar chart as default if matplotlib is available
        if self.MATPLOTLIB_AVAILABLE:
            self.display_chart("radar")
            
        return self.charts_tab
        
    except Exception as e:
        logging.error(f"Error initializing charts tab: {str(e)}")
        from PyQt6.QtWidgets import QLabel
        error_widget = QLabel(f"Error initializing charts tab: {str(e)}")
        error_widget.setStyleSheet("color: #F44336;")
        return error_widget
