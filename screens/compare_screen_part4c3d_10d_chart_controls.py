#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10d: Chart Controls Layout

Sets up the chart control layout with additional controls for filtering and visualization options.

Author: AIMF LLC
Date: June 6, 2025
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                           QLabel, QCheckBox, QSlider, QPushButton)
from PyQt6.QtCore import Qt

def setup_chart_controls(self):
    """Create chart control panel with filtering and display options"""
    # Create control container
    self.chart_controls_container = QWidget()
    self.chart_controls_layout = QHBoxLayout(self.chart_controls_container)
    self.chart_controls_layout.setContentsMargins(0, 0, 0, 0)
    
    # Category filter
    self.chart_category_label = QLabel("Category Filter:")
    self.chart_category_combo = QComboBox()
    self.chart_category_combo.addItem("All Categories")
    self.chart_category_combo.setStyleSheet("background-color: #333; color: white; selection-background-color: #bb86fc;")
    
    # Severity filter
    self.chart_severity_label = QLabel("Min. Severity:")
    self.chart_severity_slider = QSlider(Qt.Orientation.Horizontal)
    self.chart_severity_slider.setMinimum(1)
    self.chart_severity_slider.setMaximum(10)
    self.chart_severity_slider.setValue(3)
    self.chart_severity_slider.setFixedWidth(100)
    self.chart_severity_value = QLabel("3")
    
    # Additional view options
    self.chart_normalize_check = QCheckBox("Normalize")
    self.chart_normalize_check.setStyleSheet("color: white;")
    
    # Add widgets to layout
    self.chart_controls_layout.addWidget(self.chart_category_label)
    self.chart_controls_layout.addWidget(self.chart_category_combo)
    self.chart_controls_layout.addWidget(self.chart_severity_label)
    self.chart_controls_layout.addWidget(self.chart_severity_slider)
    self.chart_controls_layout.addWidget(self.chart_severity_value)
    self.chart_controls_layout.addWidget(self.chart_normalize_check)
    self.chart_controls_layout.addStretch(1)
