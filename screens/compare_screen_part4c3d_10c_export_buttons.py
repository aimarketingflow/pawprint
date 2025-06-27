#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10c: Export Button Controls

Creates the export button controls with consistent styling.

Author: AIMF LLC
Date: June 6, 2025
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

def setup_export_buttons(self):
    """Create export buttons for chart data"""
    # Create export button container
    self.export_buttons_container = QWidget()
    self.export_buttons_layout = QHBoxLayout(self.export_buttons_container)
    self.export_buttons_layout.setContentsMargins(0, 0, 0, 0)
    
    # Create export buttons
    self.export_chart_image_btn = QPushButton("Export Image")
    self.export_chart_data_btn = QPushButton("Export Data")
    self.export_report_btn = QPushButton("Export Report")
    
    # Add buttons to layout
    self.export_buttons_layout.addWidget(QLabel("Export:"))
    self.export_buttons_layout.addWidget(self.export_chart_image_btn)
    self.export_buttons_layout.addWidget(self.export_chart_data_btn)
    self.export_buttons_layout.addWidget(self.export_report_btn)
    self.export_buttons_layout.addStretch(1)
    
    # Apply dark theme styling
    for button in [self.export_chart_image_btn, self.export_chart_data_btn, self.export_report_btn]:
        button.setStyleSheet("""
            QPushButton { 
                background-color: #333; 
                color: #bb86fc; 
                border: 1px solid #bb86fc; 
                padding: 5px 10px; 
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #444; }
            QPushButton:pressed { background-color: #555; }
        """)
