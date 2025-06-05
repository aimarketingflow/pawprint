#!/usr/bin/env python3
"""
Metrics Widget Module

UI widget for displaying fractal metrics.

Author: AIMF LLC
Date: June 2, 2025
"""

import logging
from typing import Dict, Any, List

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QSizePolicy, QFrame, QScrollArea
)

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.fractal_butterfly.metrics_widget")

class MetricTile(QFrame):
    """
    Widget for displaying a single metric
    """
    
    def __init__(self, title: str, value: Any, parent=None):
        """
        Initialize the metric tile
        
        Args:
            title: Metric title
            value: Metric value
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Set frame style
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        
        # Set background color
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(240, 240, 240))
        self.setPalette(palette)
        
        # Set minimum size
        self.setMinimumSize(120, 80)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        
        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        # Add title label
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(9)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Add value label
        self.value_label = QLabel(self.format_value(value), self)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_font = QFont()
        value_font.setPointSize(12)
        self.value_label.setFont(value_font)
        layout.addWidget(self.value_label)
    
    def format_value(self, value: Any) -> str:
        """
        Format value for display
        
        Args:
            value: Value to format
            
        Returns:
            Formatted value string
        """
        if isinstance(value, float):
            return f"{value:.4f}"
        else:
            return str(value)
    
    def update_value(self, value: Any) -> None:
        """
        Update the displayed value
        
        Args:
            value: New value
        """
        self.value_label.setText(self.format_value(value))


class MetricsWidget(QWidget):
    """
    Widget for displaying fractal metrics
    """
    
    def __init__(self, parent=None):
        """Initialize the metrics widget"""
        super().__init__(parent)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        # Set up UI
        self.setup_ui()
        
        # Storage for tiles
        self.metric_tiles = {}
    
    def setup_ui(self):
        """Set up the UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title label
        title_label = QLabel("Fractal Metrics", self)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Create scroll area for metrics
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        main_layout.addWidget(scroll_area)
        
        # Container widget for scroll area
        scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(scroll_content)
        
        # Grid layout for metrics
        self.metrics_layout = QGridLayout(scroll_content)
        self.metrics_layout.setContentsMargins(3, 3, 3, 3)
        self.metrics_layout.setSpacing(5)
    
    def display_metrics(self, metrics: Dict[str, Any]) -> None:
        """
        Display metrics
        
        Args:
            metrics: Dictionary of metrics
        """
        logger.info("Displaying fractal metrics")
        
        # Clear existing tiles
        self.clear_metrics()
        
        # Add new tiles
        row, col = 0, 0
        cols_per_row = 2
        
        for title, value in metrics.items():
            # Format title
            formatted_title = title.replace('_', ' ').title()
            
            # Create tile
            tile = MetricTile(formatted_title, value, self)
            self.metrics_layout.addWidget(tile, row, col)
            
            # Store tile reference
            self.metric_tiles[title] = tile
            
            # Update position
            col += 1
            if col >= cols_per_row:
                col = 0
                row += 1
    
    def update_metric(self, name: str, value: Any) -> None:
        """
        Update a specific metric
        
        Args:
            name: Metric name
            value: New value
        """
        if name in self.metric_tiles:
            self.metric_tiles[name].update_value(value)
    
    def clear_metrics(self) -> None:
        """Clear all metrics"""
        # Remove all tiles
        for tile in self.metric_tiles.values():
            tile.deleteLater()
        
        # Clear dictionary
        self.metric_tiles = {}
        
        # Clear layout
        while self.metrics_layout.count():
            item = self.metrics_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def get_important_metrics(self, metrics: Dict[str, Any]) -> List[str]:
        """
        Get list of important metric names
        
        Args:
            metrics: Dictionary of metrics
            
        Returns:
            List of important metric names
        """
        important = [
            "fractal_dimension", "symmetry_score", "complexity", 
            "entropy", "hurst_exponent", "lyapunov_exponent"
        ]
        
        # Filter to metrics that exist
        return [m for m in important if m in metrics]
