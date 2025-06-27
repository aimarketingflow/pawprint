#!/usr/bin/env python3
"""
Developer Settings Panel Component for Pawprinting PyQt6 V2

Manages developer-specific settings, including debug options,
test features, and developer tools integration.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
from typing import Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QCheckBox, QGroupBox, QPushButton,
    QLineEdit, QSpinBox, QComboBox
)

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.advanced.developer")

class DeveloperSettingsPanel(QWidget):
    """Settings panel for developer options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize developer settings panel"""
        super().__init__(parent)
        self.parent_widget = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("advanced", {}).get("developer", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Developer settings panel initialized")
    
    def setup_ui(self):
        """Set up the developer settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # Debug Options group
        self.debug_group = QGroupBox("Debug Options")
        debug_layout = QVBoxLayout(self.debug_group)
        debug_layout.setContentsMargins(15, 15, 15, 15)
        debug_layout.setSpacing(10)
        
        # Debug mode
        self.debug_mode = QCheckBox("Enable debug mode")
        self.debug_mode.stateChanged.connect(self.on_setting_changed)
        debug_layout.addWidget(self.debug_mode)
        
        # Show dev tools
        self.show_dev_tools = QCheckBox("Show developer tools")
        self.show_dev_tools.stateChanged.connect(self.on_setting_changed)
        debug_layout.addWidget(self.show_dev_tools)
        
        # Show performance metrics
        self.show_performance = QCheckBox("Show performance metrics")
        self.show_performance.stateChanged.connect(self.on_setting_changed)
        debug_layout.addWidget(self.show_performance)
        
        # Test Features group
        self.test_group = QGroupBox("Test Features")
        test_layout = QVBoxLayout(self.test_group)
        test_layout.setContentsMargins(15, 15, 15, 15)
        test_layout.setSpacing(10)
        
        # Enable experimental features
        self.experimental_features = QCheckBox("Enable experimental features")
        self.experimental_features.stateChanged.connect(self.on_setting_changed)
        test_layout.addWidget(self.experimental_features)
        
        # Test mode
        self.test_mode = QCheckBox("Test mode (use mock data)")
        self.test_mode.stateChanged.connect(self.on_setting_changed)
        test_layout.addWidget(self.test_mode)
        
        # API Integration group
        self.api_group = QGroupBox("API Integration")
        api_layout = QFormLayout(self.api_group)
        api_layout.setContentsMargins(15, 15, 15, 15)
        api_layout.setSpacing(10)
        
        # API endpoint
        self.api_endpoint = QLineEdit()
        self.api_endpoint.setPlaceholderText("https://api.example.com/v1")
        self.api_endpoint.textChanged.connect(self.on_setting_changed)
        api_layout.addRow("API endpoint:", self.api_endpoint)
        
        # API key
        key_layout = QHBoxLayout()
        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Enter API key")
        self.api_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key.textChanged.connect(self.on_setting_changed)
        
        self.show_key_btn = QPushButton("Show")
        self.show_key_btn.setFixedWidth(60)
        self.show_key_btn.setCheckable(True)
        self.show_key_btn.toggled.connect(self.toggle_key_visibility)
        
        key_layout.addWidget(self.api_key)
        key_layout.addWidget(self.show_key_btn)
        api_layout.addRow("API key:", key_layout)
        
        # Timeout
        self.api_timeout = QSpinBox()
        self.api_timeout.setRange(1, 120)
        self.api_timeout.setSuffix(" seconds")
        self.api_timeout.valueChanged.connect(self.on_setting_changed)
        api_layout.addRow("API timeout:", self.api_timeout)
        
        # Add all groups to main layout
        main_layout.addWidget(self.debug_group)
        main_layout.addWidget(self.test_group)
        main_layout.addWidget(self.api_group)
    
    def toggle_key_visibility(self, show):
        """Toggle API key visibility"""
        self.api_key.setEchoMode(
            QLineEdit.EchoMode.Normal if show else QLineEdit.EchoMode.Password
        )
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_widget:
            self.parent_widget.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Debug Options
        self.debug_mode.setChecked(self.current_settings.get("debug_mode", False))
        self.show_dev_tools.setChecked(self.current_settings.get("show_dev_tools", False))
        self.show_performance.setChecked(self.current_settings.get("show_performance", False))
        
        # Test Features
        self.experimental_features.setChecked(self.current_settings.get("experimental_features", False))
        self.test_mode.setChecked(self.current_settings.get("test_mode", False))
        
        # API Integration
        self.api_endpoint.setText(self.current_settings.get("api_endpoint", ""))
        self.api_key.setText(self.current_settings.get("api_key", ""))
        self.api_timeout.setValue(self.current_settings.get("api_timeout", 30))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default developer settings"""
        return {
            "debug_mode": False,
            "show_dev_tools": False,
            "show_performance": False,
            "experimental_features": False,
            "test_mode": False,
            "api_endpoint": "",
            "api_key": "",
            "api_timeout": 30
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        settings = {
            "debug_mode": self.debug_mode.isChecked(),
            "show_dev_tools": self.show_dev_tools.isChecked(),
            "show_performance": self.show_performance.isChecked(),
            "experimental_features": self.experimental_features.isChecked(),
            "test_mode": self.test_mode.isChecked(),
            "api_endpoint": self.api_endpoint.text(),
            "api_key": self.api_key.text(),
            "api_timeout": self.api_timeout.value()
        }
        
        # Save to state manager under advanced.developer
        advanced_settings = self.state_manager.get_settings().get("advanced", {})
        advanced_settings["developer"] = settings
        self.state_manager.update_settings("advanced", advanced_settings)
        
        logger.info("Developer settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
