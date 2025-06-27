#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-9d: Chart Interaction

Handles user interaction with chart widgets.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

def setup_chart_interactions(self):
    """Set up chart interaction handlers"""
    try:
        # Connect chart type selection buttons
        self.radar_chart_btn.clicked.connect(lambda: self.display_chart("radar"))
        self.bar_chart_btn.clicked.connect(lambda: self.display_chart("bar"))
        self.line_chart_btn.clicked.connect(lambda: self.display_chart("line"))
        self.pie_chart_btn.clicked.connect(lambda: self.display_chart("pie"))
        self.heatmap_chart_btn.clicked.connect(lambda: self.display_chart("heatmap"))
        
        # Connect export buttons
        self.export_chart_image_btn.clicked.connect(self.show_export_image_dialog)
        self.export_chart_data_btn.clicked.connect(self.show_export_csv_dialog)
        
        # Set up view toggle buttons for chart types that support multiple views
        self.setup_view_toggle_buttons()
        
    except Exception as e:
        logging.error(f"Error setting up chart interactions: {str(e)}")

def setup_view_toggle_buttons(self):
    """Set up toggle buttons for charts with multiple views"""
    try:
        from PyQt6.QtWidgets import QPushButton
        
        # Create toggle button for pie chart
        self.toggle_pie_view_button = QPushButton("View by Category")
        self.toggle_pie_view_button.clicked.connect(self.toggle_pie_chart_view)
        self.chart_controls_layout.addWidget(self.toggle_pie_view_button)
        self.toggle_pie_view_button.hide()  # Initially hidden
        
        # Create toggle button for heatmap
        self.toggle_heatmap_view_button = QPushButton("View by Origin")
        self.toggle_heatmap_view_button.clicked.connect(self.toggle_heatmap_chart_view)
        self.chart_controls_layout.addWidget(self.toggle_heatmap_view_button)
        self.toggle_heatmap_view_button.hide()  # Initially hidden
        
    except Exception as e:
        logging.error(f"Error setting up view toggle buttons: {str(e)}")

def show_chart_view_options(self, chart_type):
    """Show or hide view toggle buttons based on chart type
    
    Args:
        chart_type: Type of chart currently displayed
    """
    # Hide all toggle buttons first
    if hasattr(self, 'toggle_pie_view_button'):
        self.toggle_pie_view_button.hide()
    if hasattr(self, 'toggle_heatmap_view_button'):
        self.toggle_heatmap_view_button.hide()
    
    # Show relevant toggle button
    if chart_type == "pie" and hasattr(self, 'toggle_pie_view_button'):
        self.toggle_pie_view_button.show()
    elif chart_type == "heatmap" and hasattr(self, 'toggle_heatmap_view_button'):
        self.toggle_heatmap_view_button.show()
