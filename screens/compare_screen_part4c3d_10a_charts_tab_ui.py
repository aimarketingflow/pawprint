#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-10a: Charts Tab UI Components

Creates the UI components for the Charts tab.

Author: AIMF LLC
Date: June 6, 2025
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                           QLabel, QSplitter, QGroupBox, QTextBrowser)
from PyQt6.QtCore import Qt

def setup_charts_tab_ui(self):
    """Create UI components for Charts tab"""
    # Create main container for charts tab
    self.charts_tab = QWidget()
    self.charts_tab_layout = QVBoxLayout(self.charts_tab)
    
    # Create splitter for chart and description
    self.chart_splitter = QSplitter(Qt.Orientation.Vertical)
    
    # Create chart area container
    self.chart_container = QWidget()
    self.chart_container_layout = QVBoxLayout(self.chart_container)
    
    # Create description area
    self.chart_description_container = QWidget()
    self.chart_description_layout = QVBoxLayout(self.chart_description_container)
    self.chart_description_label = QLabel("Chart Description")
    self.chart_description_browser = QTextBrowser()
    self.chart_description_browser.setOpenExternalLinks(True)
    self.chart_description_layout.addWidget(self.chart_description_label)
    self.chart_description_layout.addWidget(self.chart_description_browser)
    
    # Add containers to splitter
    self.chart_splitter.addWidget(self.chart_container)
    self.chart_splitter.addWidget(self.chart_description_container)
    self.chart_splitter.setStretchFactor(0, 2)  # Chart gets more space
    self.chart_splitter.setStretchFactor(1, 1)  # Description gets less space
