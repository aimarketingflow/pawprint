#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10b: Charts Tab Button Layout

Creates the chart type selection and export buttons with dark theme styling.

Author: AIMF LLC
Date: June 6, 2025
"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

def setup_chart_buttons(self):
    """Create chart type selection buttons with consistent dark theme styling"""
    # Create button container
    self.chart_buttons_container = QWidget()
    self.chart_buttons_layout = QHBoxLayout(self.chart_buttons_container)
    self.chart_buttons_layout.setContentsMargins(0, 0, 0, 0)
    
    # Create chart type buttons with neon purple styling
    self.radar_chart_btn = QPushButton("Radar")
    self.bar_chart_btn = QPushButton("Bar")
    self.line_chart_btn = QPushButton("Line")
    self.pie_chart_btn = QPushButton("Pie")
    self.heatmap_chart_btn = QPushButton("Heatmap")
    
    # Add buttons to layout
    self.chart_buttons_layout.addWidget(QLabel("Chart Type:"))
    self.chart_buttons_layout.addWidget(self.radar_chart_btn)
    self.chart_buttons_layout.addWidget(self.bar_chart_btn)
    self.chart_buttons_layout.addWidget(self.line_chart_btn)
    self.chart_buttons_layout.addWidget(self.pie_chart_btn)
    self.chart_buttons_layout.addWidget(self.heatmap_chart_btn)
    self.chart_buttons_layout.addStretch(1)
    
    # Apply dark theme styling
    for button in [self.radar_chart_btn, self.bar_chart_btn, self.line_chart_btn, 
                  self.pie_chart_btn, self.heatmap_chart_btn]:
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
