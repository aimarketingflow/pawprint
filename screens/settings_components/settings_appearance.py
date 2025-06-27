#!/usr/bin/env python3
"""
Appearance Settings Panel Component for Pawprinting PyQt6 V2

Manages application appearance settings including themes, colors,
font sizes, and UI display options.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPalette, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QSlider, QCheckBox, QGroupBox,
    QPushButton, QColorDialog, QFrame, QSpacerItem,
    QSizePolicy, QSpinBox
)

from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.notification_manager import NotificationManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.appearance")

class ColorButton(QPushButton):
    """Custom button for color selection"""
    
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

class AppearanceSettingsPanel(QWidget):
    """Appearance settings panel"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize appearance settings panel"""
        super().__init__(parent)
        self.parent_screen = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("appearance", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Available themes and their display names
        self.available_themes = {
            "dark": "Dark Mode (Default)",
            "light": "Light Mode",
            "high_contrast": "High Contrast",
            "custom": "Custom"
        }
        
        # Color buttons dictionary to store references
        self.color_buttons = {}
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Appearance settings panel initialized")
    
    def setup_ui(self):
        """Set up the appearance settings UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Theme section
        self.theme_group = QGroupBox("Theme")
        theme_layout = QFormLayout(self.theme_group)
        theme_layout.setContentsMargins(15, 15, 15, 15)
        theme_layout.setSpacing(10)
        
        # Theme selector
        self.theme_selector = QComboBox()
        for theme_id, theme_name in self.available_themes.items():
            self.theme_selector.addItem(theme_name, theme_id)
        
        self.theme_selector.currentIndexChanged.connect(self.on_theme_changed)
        theme_layout.addRow("Select theme:", self.theme_selector)
        
        # Custom Colors section (initially hidden, shown when Custom theme is selected)
        self.colors_group = QGroupBox("Custom Colors")
        self.colors_group.setVisible(False)
        colors_layout = QFormLayout(self.colors_group)
        colors_layout.setContentsMargins(15, 15, 15, 15)
        colors_layout.setSpacing(10)
        
        # Color customization
        color_definitions = [
            ("background", "Background", QColor("#2D2D30")),
            ("foreground", "Text", QColor("#FFFFFF")),
            ("accent", "Accent", QColor("#9059FF")),
            ("accent_light", "Accent (Light)", QColor("#B28AFF")),
            ("secondary_background", "Secondary Background", QColor("#252526")),
            ("success", "Success", QColor("#47D764")),
            ("warning", "Warning", QColor("#FFC107")),
            ("error", "Error", QColor("#F44336"))
        ]
        
        for color_id, color_name, default_color in color_definitions:
            row_layout = QHBoxLayout()
            
            # Create color button
            saved_color = QColor(self.current_settings.get("colors", {}).get(color_id, default_color.name()))
            color_btn = ColorButton(color_id, saved_color)
            color_btn.color_changed.connect(self.on_color_changed)
            
            # Store reference
            self.color_buttons[color_id] = color_btn
            
            row_layout.addWidget(color_btn)
            row_layout.addStretch(1)
            
            # Reset button
            reset_btn = QPushButton("Reset")
            reset_btn.setObjectName("smallButton")
            reset_btn.clicked.connect(lambda checked, cid=color_id, dc=default_color: self.reset_color(cid, dc))
            row_layout.addWidget(reset_btn)
            
            colors_layout.addRow(f"{color_name}:", row_layout)
        
        # UI Display Options
        self.display_group = QGroupBox("UI Display Options")
        display_layout = QFormLayout(self.display_group)
        display_layout.setContentsMargins(15, 15, 15, 15)
        display_layout.setSpacing(10)
        
        # Font size
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 18)
        self.font_size.setSuffix(" pt")
        self.font_size.valueChanged.connect(self.on_setting_changed)
        display_layout.addRow("UI font size:", self.font_size)
        
        # UI density
        self.ui_density = QComboBox()
        self.ui_density.addItem("Comfortable", "comfortable")
        self.ui_density.addItem("Compact", "compact")
        self.ui_density.currentIndexChanged.connect(self.on_setting_changed)
        display_layout.addRow("UI density:", self.ui_density)
        
        # Show tooltips
        self.show_tooltips = QCheckBox("Show tooltips")
        self.show_tooltips.stateChanged.connect(self.on_setting_changed)
        display_layout.addRow("", self.show_tooltips)
        
        # Animate transitions
        self.animate_transitions = QCheckBox("Animate transitions")
        self.animate_transitions.stateChanged.connect(self.on_setting_changed)
        display_layout.addRow("", self.animate_transitions)
        
        # Add all groups to main layout
        main_layout.addWidget(self.theme_group)
        main_layout.addWidget(self.colors_group)
        main_layout.addWidget(self.display_group)
        main_layout.addStretch(1)
    
    def on_theme_changed(self, index):
        """Handle theme selection changed"""
        theme_id = self.theme_selector.currentData()
        logger.debug(f"Theme changed to: {theme_id}")
        
        # Show/hide custom colors section
        self.colors_group.setVisible(theme_id == "custom")
        
        # Apply theme preview
        if theme_id != "custom" and self.theme_manager:
            self.theme_manager.set_theme(theme_id)
        
        self.on_setting_changed()
    
    def on_color_changed(self, color_name, color):
        """Handle color change in a color button"""
        logger.debug(f"Color {color_name} changed to {color.name()}")
        
        # Apply custom theme with updated colors
        if self.theme_manager and self.theme_selector.currentData() == "custom":
            colors = {}
            for color_id, button in self.color_buttons.items():
                colors[color_id] = button.color.name()
            
            self.theme_manager.set_custom_theme(colors)
        
        self.on_setting_changed()
    
    def reset_color(self, color_id, default_color):
        """Reset a color to its default value"""
        if color_id in self.color_buttons:
            self.color_buttons[color_id].update_color(default_color)
            self.on_color_changed(color_id, default_color)
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_screen:
            self.parent_screen.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Theme
        theme = self.current_settings.get("theme", "dark")
        index = self.theme_selector.findData(theme)
        if index >= 0:
            self.theme_selector.setCurrentIndex(index)
            
            # Show colors group if custom theme
            self.colors_group.setVisible(theme == "custom")
        
        # Colors - already loaded in setup_ui
        
        # UI Display Options
        self.font_size.setValue(self.current_settings.get("font_size", 11))
        
        density = self.current_settings.get("ui_density", "comfortable")
        index = self.ui_density.findData(density)
        if index >= 0:
            self.ui_density.setCurrentIndex(index)
        
        self.show_tooltips.setChecked(self.current_settings.get("show_tooltips", True))
        self.animate_transitions.setChecked(self.current_settings.get("animate_transitions", True))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default appearance settings"""
        return {
            "theme": "dark",
            "colors": {
                "background": "#2D2D30",
                "foreground": "#FFFFFF",
                "accent": "#9059FF",
                "accent_light": "#B28AFF",
                "secondary_background": "#252526",
                "success": "#47D764",
                "warning": "#FFC107",
                "error": "#F44336"
            },
            "font_size": 11,
            "ui_density": "comfortable",
            "show_tooltips": True,
            "animate_transitions": True
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        theme = self.theme_selector.currentData()
        
        # Collect colors if using custom theme
        colors = {}
        if theme == "custom":
            for color_id, button in self.color_buttons.items():
                colors[color_id] = button.color.name()
        else:
            # Use default colors for the selected theme
            colors = self.theme_manager.get_theme_colors(theme)
        
        settings = {
            "theme": theme,
            "colors": colors,
            "font_size": self.font_size.value(),
            "ui_density": self.ui_density.currentData(),
            "show_tooltips": self.show_tooltips.isChecked(),
            "animate_transitions": self.animate_transitions.isChecked()
        }
        
        # Save to state manager
        self.state_manager.update_settings("appearance", settings)
        
        # Apply theme right away
        if self.theme_manager:
            if theme == "custom":
                self.theme_manager.set_custom_theme(colors)
            else:
                self.theme_manager.set_theme(theme)
        
        logger.info("Appearance settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        
        # Also restore default colors in color buttons
        default_colors = self.current_settings.get("colors", {})
        for color_id, color_value in default_colors.items():
            if color_id in self.color_buttons:
                self.color_buttons[color_id].update_color(QColor(color_value))
        
        # Apply the default theme
        if self.theme_manager:
            self.theme_manager.set_theme(self.current_settings.get("theme", "dark"))
        
        self.on_setting_changed()
