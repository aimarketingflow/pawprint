#!/usr/bin/env python3
"""
General Settings Panel Component for Pawprinting PyQt6 V2

Handles general application settings including file paths, startup behavior, 
and session management.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox,
    QFileDialog, QGroupBox, QSpinBox, QFrame, QSizePolicy,
    QSpacerItem
)

from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.notification_manager import NotificationManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.general")

class GeneralSettingsPanel(QWidget):
    """General application settings panel"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize general settings panel"""
        super().__init__(parent)
        self.parent_screen = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("general", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("General settings panel initialized")
    
    def setup_ui(self):
        """Set up the general settings UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Default paths section
        self.paths_group = QGroupBox("Default Paths")
        paths_layout = QFormLayout(self.paths_group)
        paths_layout.setContentsMargins(15, 15, 15, 15)
        paths_layout.setSpacing(10)
        
        # Default save location
        save_path_layout = QHBoxLayout()
        self.default_save_path = QLineEdit()
        self.default_save_path.setReadOnly(True)
        self.default_save_path.setPlaceholderText("Default save location")
        
        self.browse_save_btn = QPushButton("Browse...")
        self.browse_save_btn.clicked.connect(self.browse_save_path)
        
        save_path_layout.addWidget(self.default_save_path)
        save_path_layout.addWidget(self.browse_save_btn)
        
        paths_layout.addRow("Default save location:", save_path_layout)
        
        # Default import location
        import_path_layout = QHBoxLayout()
        self.default_import_path = QLineEdit()
        self.default_import_path.setReadOnly(True)
        self.default_import_path.setPlaceholderText("Default import location")
        
        self.browse_import_btn = QPushButton("Browse...")
        self.browse_import_btn.clicked.connect(self.browse_import_path)
        
        import_path_layout.addWidget(self.default_import_path)
        import_path_layout.addWidget(self.browse_import_btn)
        
        paths_layout.addRow("Default import location:", import_path_layout)
        
        # Session Management
        self.session_group = QGroupBox("Session Management")
        session_layout = QFormLayout(self.session_group)
        session_layout.setContentsMargins(15, 15, 15, 15)
        session_layout.setSpacing(10)
        
        # Auto-save session interval
        self.autosave_interval = QSpinBox()
        self.autosave_interval.setRange(0, 60)
        self.autosave_interval.setSuffix(" minutes")
        self.autosave_interval.setSpecialValueText("Disabled")
        self.autosave_interval.valueChanged.connect(self.on_setting_changed)
        session_layout.addRow("Auto-save interval:", self.autosave_interval)
        
        # Keep history for
        self.history_retention = QSpinBox()
        self.history_retention.setRange(1, 365)
        self.history_retention.setSuffix(" days")
        self.history_retention.valueChanged.connect(self.on_setting_changed)
        session_layout.addRow("Keep history for:", self.history_retention)
        
        # Startup behavior
        self.startup_group = QGroupBox("Startup Behavior")
        startup_layout = QFormLayout(self.startup_group)
        startup_layout.setContentsMargins(15, 15, 15, 15)
        startup_layout.setSpacing(10)
        
        # Load last session
        self.load_last_session = QCheckBox("Load last session on startup")
        self.load_last_session.stateChanged.connect(self.on_setting_changed)
        startup_layout.addRow("", self.load_last_session)
        
        # Show startup tips
        self.show_startup_tips = QCheckBox("Show tips on startup")
        self.show_startup_tips.stateChanged.connect(self.on_setting_changed)
        startup_layout.addRow("", self.show_startup_tips)
        
        # Check for updates
        self.check_updates = QCheckBox("Check for updates on startup")
        self.check_updates.stateChanged.connect(self.on_setting_changed)
        startup_layout.addRow("", self.check_updates)
        
        # Add all groups to main layout
        main_layout.addWidget(self.paths_group)
        main_layout.addWidget(self.session_group)
        main_layout.addWidget(self.startup_group)
        main_layout.addStretch(1)
    
    def browse_save_path(self):
        """Open file dialog to select default save path"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Default Save Location",
            self.default_save_path.text() or str(Path.home())
        )
        
        if directory:
            self.default_save_path.setText(directory)
            self.on_setting_changed()
    
    def browse_import_path(self):
        """Open file dialog to select default import path"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Default Import Location",
            self.default_import_path.text() or str(Path.home())
        )
        
        if directory:
            self.default_import_path.setText(directory)
            self.on_setting_changed()
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_screen:
            self.parent_screen.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Default paths
        self.default_save_path.setText(self.current_settings.get("default_save_path", ""))
        self.default_import_path.setText(self.current_settings.get("default_import_path", ""))
        
        # Session management
        self.autosave_interval.setValue(self.current_settings.get("autosave_interval", 5))
        self.history_retention.setValue(self.current_settings.get("history_retention", 30))
        
        # Startup behavior
        self.load_last_session.setChecked(self.current_settings.get("load_last_session", True))
        self.show_startup_tips.setChecked(self.current_settings.get("show_startup_tips", True))
        self.check_updates.setChecked(self.current_settings.get("check_updates", True))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default general settings"""
        return {
            "default_save_path": str(Path.home() / "Documents" / "Pawprinting_Results"),
            "default_import_path": str(Path.home() / "Documents"),
            "autosave_interval": 5,
            "history_retention": 30,
            "load_last_session": True,
            "show_startup_tips": True,
            "check_updates": True
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        settings = {
            "default_save_path": self.default_save_path.text(),
            "default_import_path": self.default_import_path.text(),
            "autosave_interval": self.autosave_interval.value(),
            "history_retention": self.history_retention.value(),
            "load_last_session": self.load_last_session.isChecked(),
            "show_startup_tips": self.show_startup_tips.isChecked(),
            "check_updates": self.check_updates.isChecked()
        }
        
        # Ensure paths exist
        for path_key in ["default_save_path", "default_import_path"]:
            if settings[path_key] and not os.path.exists(settings[path_key]):
                try:
                    os.makedirs(settings[path_key], exist_ok=True)
                except Exception as e:
                    logger.error(f"Could not create directory {settings[path_key]}: {str(e)}")
                    NotificationManager.show_message(f"Could not create directory: {settings[path_key]}")
        
        # Save to state manager
        self.state_manager.update_settings("general", settings)
        logger.info("General settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
