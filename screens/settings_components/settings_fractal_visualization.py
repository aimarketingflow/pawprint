#!/usr/bin/env python3
"""
Fractal Visualization Settings Component for Pawprinting PyQt6 V2

Manages settings related to how fractal patterns are visualized,
including color schemes, rendering quality, and display options.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QSlider, QCheckBox, QGroupBox,
    QPushButton, QColorDialog, QSpinBox
)

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.fractal.visualization")

class ColorSchemeButton(QPushButton):
    """Custom button for color scheme selection"""
    
    color_changed = pyqtSignal(str, QColor)
    
    def __init__(self, color_name: str, color: QColor, parent=None):
        super().__init__(parent)
        self.color_name = color_name
        self.color = color
        self.setFixedSize(30, 30)
        self.update_color(color)
        self.clicked.connect(self.on_clicked)
    
    def update_color(self, color: QColor):
        """Update button color"""
        self.color = color
        self.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #888;")
    
    def on_clicked(self):
        """Open color dialog when clicked"""
        color = QColorDialog.getColor(self.color, self.parent(), f"Select {self.color_name} Color")
        if color.isValid():
            self.update_color(color)
            self.color_changed.emit(self.color_name, color)

class FractalVisualizationSettings(QWidget):
    """Settings panel for fractal visualization options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize fractal visualization settings panel"""
        super().__init__(parent)
        self.parent_widget = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("fractal", {}).get("visualization", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Color scheme buttons dictionary
        self.color_buttons = {}
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Fractal visualization settings panel initialized")
    
    def setup_ui(self):
        """Set up the fractal visualization settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # Visualization Options group
        self.viz_group = QGroupBox("Visualization Options")
        viz_layout = QFormLayout(self.viz_group)
        viz_layout.setContentsMargins(15, 15, 15, 15)
        viz_layout.setSpacing(10)
        
        # Visualization style
        self.viz_style = QComboBox()
        self.viz_style.addItem("Classic (Default)", "classic")
        self.viz_style.addItem("Modern", "modern")
        self.viz_style.addItem("Minimalist", "minimalist")
        self.viz_style.addItem("Detailed", "detailed")
        self.viz_style.currentIndexChanged.connect(self.on_setting_changed)
        viz_layout.addRow("Visualization style:", self.viz_style)
        
        # Rendering quality
        quality_layout = QVBoxLayout()
        quality_label = QLabel("Rendering quality:")
        self.render_quality = QSlider(Qt.Orientation.Horizontal)
        self.render_quality.setRange(1, 5)
        self.render_quality.setSingleStep(1)
        self.render_quality.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.render_quality.setTickInterval(1)
        self.render_quality.valueChanged.connect(self.on_quality_changed)
        
        self.quality_value_label = QLabel("3 (Medium)")
        self.quality_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.render_quality)
        quality_layout.addWidget(self.quality_value_label)
        viz_layout.addRow("", quality_layout)
        
        # Animation speed
        speed_layout = QVBoxLayout()
        speed_label = QLabel("Animation speed:")
        self.animation_speed = QSlider(Qt.Orientation.Horizontal)
        self.animation_speed.setRange(1, 10)
        self.animation_speed.setSingleStep(1)
        self.animation_speed.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.animation_speed.setTickInterval(1)
        self.animation_speed.valueChanged.connect(self.on_speed_changed)
        
        self.speed_value_label = QLabel("5 (Medium)")
        self.speed_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.animation_speed)
        speed_layout.addWidget(self.speed_value_label)
        viz_layout.addRow("", speed_layout)
        
        # Color Scheme group
        self.colors_group = QGroupBox("Color Scheme")
        colors_layout = QFormLayout(self.colors_group)
        colors_layout.setContentsMargins(15, 15, 15, 15)
        colors_layout.setSpacing(10)
        
        # Predefined color schemes
        self.color_scheme = QComboBox()
        self.color_scheme.addItem("Neon Purple (Default)", "neon_purple")
        self.color_scheme.addItem("Spectrum", "spectrum")
        self.color_scheme.addItem("Ocean", "ocean")
        self.color_scheme.addItem("Forest", "forest")
        self.color_scheme.addItem("Fire", "fire")
        self.color_scheme.addItem("Monochrome", "monochrome")
        self.color_scheme.addItem("Custom", "custom")
        self.color_scheme.currentIndexChanged.connect(self.on_scheme_changed)
        colors_layout.addRow("Color scheme:", self.color_scheme)
        
        # Custom colors section (initially hidden, shown when Custom scheme is selected)
        self.custom_colors_container = QWidget()
        self.custom_colors_container.setVisible(False)
        custom_colors_layout = QFormLayout(self.custom_colors_container)
        custom_colors_layout.setContentsMargins(0, 10, 0, 0)
        custom_colors_layout.setSpacing(10)
        
        # Custom color definitions
        color_definitions = [
            ("primary", "Primary", QColor("#9059FF")),
            ("secondary", "Secondary", QColor("#B28AFF")),
            ("background", "Background", QColor("#252526")),
            ("highlight", "Highlight", QColor("#00BFFF")),
            ("accent", "Accent", QColor("#FF4081"))
        ]
        
        for color_id, color_name, default_color in color_definitions:
            row_layout = QHBoxLayout()
            
            # Create color button
            saved_color = QColor(self.current_settings.get("custom_colors", {}).get(color_id, default_color.name()))
            color_btn = ColorSchemeButton(color_id, saved_color)
            color_btn.color_changed.connect(self.on_color_changed)
            
            # Store reference
            self.color_buttons[color_id] = color_btn
            
            row_layout.addWidget(color_btn)
            row_layout.addStretch(1)
            
            custom_colors_layout.addRow(f"{color_name}:", row_layout)
        
        colors_layout.addRow("", self.custom_colors_container)
        
        # Display Options group
        self.display_group = QGroupBox("Display Options")
        display_layout = QVBoxLayout(self.display_group)
        display_layout.setContentsMargins(15, 15, 15, 15)
        display_layout.setSpacing(10)
        
        # Show grid lines
        self.show_grid = QCheckBox("Show grid lines")
        self.show_grid.stateChanged.connect(self.on_setting_changed)
        display_layout.addWidget(self.show_grid)
        
        # Show labels
        self.show_labels = QCheckBox("Show pattern labels")
        self.show_labels.stateChanged.connect(self.on_setting_changed)
        display_layout.addWidget(self.show_labels)
        
        # Show tooltips
        self.show_tooltips = QCheckBox("Show interactive tooltips")
        self.show_tooltips.stateChanged.connect(self.on_setting_changed)
        display_layout.addWidget(self.show_tooltips)
        
        # Use hardware acceleration
        self.use_hardware_accel = QCheckBox("Use hardware acceleration when available")
        self.use_hardware_accel.stateChanged.connect(self.on_setting_changed)
        display_layout.addWidget(self.use_hardware_accel)
        
        # Add all groups to main layout
        main_layout.addWidget(self.viz_group)
        main_layout.addWidget(self.colors_group)
        main_layout.addWidget(self.display_group)
    
    def on_quality_changed(self, value):
        """Update quality value label and notify about setting change"""
        quality_labels = {
            1: "1 (Low)",
            2: "2 (Medium-Low)",
            3: "3 (Medium)",
            4: "4 (High)",
            5: "5 (Ultra)"
        }
        self.quality_value_label.setText(quality_labels.get(value, f"{value}"))
        self.on_setting_changed()
    
    def on_speed_changed(self, value):
        """Update speed value label and notify about setting change"""
        if value <= 3:
            label = f"{value} (Slow)"
        elif value <= 7:
            label = f"{value} (Medium)"
        else:
            label = f"{value} (Fast)"
        
        self.speed_value_label.setText(label)
        self.on_setting_changed()
    
    def on_scheme_changed(self, index):
        """Handle color scheme selection changed"""
        scheme_id = self.color_scheme.currentData()
        logger.debug(f"Color scheme changed to: {scheme_id}")
        
        # Show/hide custom colors section
        self.custom_colors_container.setVisible(scheme_id == "custom")
        
        # When switching to a predefined scheme, update color previews
        if scheme_id != "custom":
            # This could update a preview component if we had one
            pass
        
        self.on_setting_changed()
    
    def on_color_changed(self, color_name, color):
        """Handle color change in a color button"""
        logger.debug(f"Color {color_name} changed to {color.name()}")
        self.on_setting_changed()
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_widget:
            self.parent_widget.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Visualization style
        viz_style = self.current_settings.get("style", "classic")
        index = self.viz_style.findData(viz_style)
        if index >= 0:
            self.viz_style.setCurrentIndex(index)
        
        # Rendering quality
        self.render_quality.setValue(self.current_settings.get("quality", 3))
        self.on_quality_changed(self.render_quality.value())
        
        # Animation speed
        self.animation_speed.setValue(self.current_settings.get("animation_speed", 5))
        self.on_speed_changed(self.animation_speed.value())
        
        # Color scheme
        color_scheme = self.current_settings.get("color_scheme", "neon_purple")
        index = self.color_scheme.findData(color_scheme)
        if index >= 0:
            self.color_scheme.setCurrentIndex(index)
            self.custom_colors_container.setVisible(color_scheme == "custom")
        
        # Custom colors already loaded in setup_ui
        
        # Display Options
        self.show_grid.setChecked(self.current_settings.get("show_grid", True))
        self.show_labels.setChecked(self.current_settings.get("show_labels", True))
        self.show_tooltips.setChecked(self.current_settings.get("show_tooltips", True))
        self.use_hardware_accel.setChecked(self.current_settings.get("use_hardware_accel", True))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default fractal visualization settings"""
        return {
            "style": "classic",
            "quality": 3,
            "animation_speed": 5,
            "color_scheme": "neon_purple",
            "custom_colors": {
                "primary": "#9059FF",
                "secondary": "#B28AFF",
                "background": "#252526",
                "highlight": "#00BFFF",
                "accent": "#FF4081"
            },
            "show_grid": True,
            "show_labels": True,
            "show_tooltips": True,
            "use_hardware_accel": True
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        # Get current color scheme
        color_scheme = self.color_scheme.currentData()
        
        # Collect custom colors if using custom scheme
        custom_colors = {}
        if color_scheme == "custom":
            for color_id, button in self.color_buttons.items():
                custom_colors[color_id] = button.color.name()
        
        settings = {
            "style": self.viz_style.currentData(),
            "quality": self.render_quality.value(),
            "animation_speed": self.animation_speed.value(),
            "color_scheme": color_scheme,
            "custom_colors": custom_colors,
            "show_grid": self.show_grid.isChecked(),
            "show_labels": self.show_labels.isChecked(),
            "show_tooltips": self.show_tooltips.isChecked(),
            "use_hardware_accel": self.use_hardware_accel.isChecked()
        }
        
        # Save to state manager under fractal.visualization
        fractal_settings = self.state_manager.get_settings().get("fractal", {})
        fractal_settings["visualization"] = settings
        self.state_manager.update_settings("fractal", fractal_settings)
        
        logger.info("Fractal visualization settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        
        # Also update color buttons with default colors
        default_colors = self.current_settings.get("custom_colors", {})
        for color_id, color_value in default_colors.items():
            if color_id in self.color_buttons:
                self.color_buttons[color_id].update_color(QColor(color_value))
        
        self.on_setting_changed()
