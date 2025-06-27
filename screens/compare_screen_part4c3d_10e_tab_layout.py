#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10e: Charts Tab Layout Assembly

Assembles all chart UI components into the final tab layout.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

def assemble_charts_tab_layout(self):
    """Assemble all chart components into the complete charts tab layout"""
    try:
        # Setup all required UI components if not already done
        if not hasattr(self, 'charts_tab'):
            self.setup_charts_tab_ui()
        if not hasattr(self, 'chart_buttons_container'):
            self.setup_chart_buttons()
        if not hasattr(self, 'export_buttons_container'):
            self.setup_export_buttons()
        if not hasattr(self, 'chart_controls_container'):
            self.setup_chart_controls()
            
        # Assemble the layout
        # 1. Add chart type selection buttons at top
        self.charts_tab_layout.addWidget(self.chart_buttons_container)
        
        # 2. Add chart controls below buttons
        self.charts_tab_layout.addWidget(self.chart_controls_container)
        
        # 3. Add chart/description splitter in the middle (taking most space)
        self.charts_tab_layout.addWidget(self.chart_splitter, 1)
        
        # 4. Add export buttons at bottom
        self.charts_tab_layout.addWidget(self.export_buttons_container)
        
        # Set initial chart if matplotlib is available
        if hasattr(self, 'MATPLOTLIB_AVAILABLE') and self.MATPLOTLIB_AVAILABLE:
            # Initialize matplotlib chart widget
            self.setup_chart_widget()
            self.configure_chart_theme()
        else:
            from PyQt6.QtWidgets import QLabel
            warning_label = QLabel("Matplotlib not available. Charts functionality limited.")
            warning_label.setStyleSheet("color: #F44336;")
            self.chart_container_layout.addWidget(warning_label)
            
        return self.charts_tab
        
    except Exception as e:
        logging.error(f"Error assembling charts tab layout: {str(e)}")
        from PyQt6.QtWidgets import QLabel
        error_widget = QLabel(f"Error setting up charts tab: {str(e)}")
        error_widget.setStyleSheet("color: #F44336;")
        return error_widget
