#!/usr/bin/env python3
"""
Logging Settings Panel Component for Pawprinting PyQt6 V2

Manages application logging settings including log levels,
rotation policies, and output destinations.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
import os
from pathlib import Path
from typing import Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QComboBox, QGroupBox, QPushButton,
    QCheckBox, QSpinBox, QLineEdit, QFileDialog
)

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.advanced.logging")

class LoggingSettingsPanel(QWidget):
    """Settings panel for logging options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize logging settings panel"""
        super().__init__(parent)
        self.parent_widget = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("advanced", {}).get("logging", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Logging settings panel initialized")
    
    def setup_ui(self):
        """Set up the logging settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # Log Levels group
        self.levels_group = QGroupBox("Log Levels")
        levels_layout = QFormLayout(self.levels_group)
        levels_layout.setContentsMargins(15, 15, 15, 15)
        levels_layout.setSpacing(10)
        
        # Console log level
        self.console_level = QComboBox()
        self.console_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.console_level.currentIndexChanged.connect(self.on_setting_changed)
        levels_layout.addRow("Console log level:", self.console_level)
        
        # File log level
        self.file_level = QComboBox()
        self.file_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.file_level.currentIndexChanged.connect(self.on_setting_changed)
        levels_layout.addRow("File log level:", self.file_level)
        
        # Log Destinations group
        self.destinations_group = QGroupBox("Log Destinations")
        destinations_layout = QVBoxLayout(self.destinations_group)
        destinations_layout.setContentsMargins(15, 15, 15, 15)
        destinations_layout.setSpacing(10)
        
        # Log to console
        self.log_to_console = QCheckBox("Log to console")
        self.log_to_console.stateChanged.connect(self.on_setting_changed)
        destinations_layout.addWidget(self.log_to_console)
        
        # Log to file
        self.log_to_file = QCheckBox("Log to file")
        self.log_to_file.stateChanged.connect(self.on_log_file_toggled)
        destinations_layout.addWidget(self.log_to_file)
        
        # Log directory
        self.log_dir_container = QWidget()
        log_dir_layout = QHBoxLayout(self.log_dir_container)
        log_dir_layout.setContentsMargins(0, 5, 0, 5)
        log_dir_layout.setSpacing(10)
        
        log_dir_label = QLabel("Log directory:")
        self.log_dir = QLineEdit()
        self.log_dir.setReadOnly(True)
        self.log_dir.setPlaceholderText("Select log directory")
        
        self.browse_dir_btn = QPushButton("Browse...")
        self.browse_dir_btn.clicked.connect(self.browse_log_directory)
        
        log_dir_layout.addWidget(log_dir_label)
        log_dir_layout.addWidget(self.log_dir)
        log_dir_layout.addWidget(self.browse_dir_btn)
        destinations_layout.addWidget(self.log_dir_container)
        
        # Log Rotation group
        self.rotation_group = QGroupBox("Log Rotation")
        rotation_layout = QFormLayout(self.rotation_group)
        rotation_layout.setContentsMargins(15, 15, 15, 15)
        rotation_layout.setSpacing(10)
        
        # Enable log rotation
        self.enable_rotation = QCheckBox("Enable log rotation")
        self.enable_rotation.stateChanged.connect(self.on_rotation_toggled)
        rotation_layout.addRow("", self.enable_rotation)
        
        # Rotation settings container
        self.rotation_settings = QWidget()
        rotation_settings_layout = QFormLayout(self.rotation_settings)
        rotation_settings_layout.setContentsMargins(0, 0, 0, 0)
        rotation_settings_layout.setSpacing(10)
        
        # Max log size
        self.max_size = QSpinBox()
        self.max_size.setRange(1, 100)
        self.max_size.setSuffix(" MB")
        self.max_size.valueChanged.connect(self.on_setting_changed)
        rotation_settings_layout.addRow("Max log file size:", self.max_size)
        
        # Backup count
        self.backup_count = QSpinBox()
        self.backup_count.setRange(1, 20)
        self.backup_count.valueChanged.connect(self.on_setting_changed)
        rotation_settings_layout.addRow("Number of backups:", self.backup_count)
        
        rotation_layout.addRow("", self.rotation_settings)
        
        # Additional Options group
        self.options_group = QGroupBox("Additional Options")
        options_layout = QVBoxLayout(self.options_group)
        options_layout.setContentsMargins(15, 15, 15, 15)
        options_layout.setSpacing(10)
        
        # Include timestamps
        self.include_timestamps = QCheckBox("Include timestamps in logs")
        self.include_timestamps.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_timestamps)
        
        # Include thread info
        self.include_thread_info = QCheckBox("Include thread information")
        self.include_thread_info.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_thread_info)
        
        # Include source file info
        self.include_source_info = QCheckBox("Include source file information")
        self.include_source_info.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_source_info)
        
        # Add all groups to main layout
        main_layout.addWidget(self.levels_group)
        main_layout.addWidget(self.destinations_group)
        main_layout.addWidget(self.rotation_group)
        main_layout.addWidget(self.options_group)
    
    def browse_log_directory(self):
        """Open file dialog to select log directory"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Log Directory",
            self.log_dir.text() or str(Path.home()),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if directory:
            self.log_dir.setText(directory)
            self.on_setting_changed()
    
    def on_log_file_toggled(self, state):
        """Handle log to file checkbox toggle"""
        enabled = state == Qt.CheckState.Checked.value
        self.log_dir_container.setVisible(enabled)
        self.rotation_group.setEnabled(enabled)
        self.on_setting_changed()
    
    def on_rotation_toggled(self, state):
        """Handle rotation checkbox toggle"""
        enabled = state == Qt.CheckState.Checked.value
        self.rotation_settings.setVisible(enabled)
        self.on_setting_changed()
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_widget:
            self.parent_widget.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Log Levels
        console_level = self.current_settings.get("console_level", "INFO")
        self.console_level.setCurrentText(console_level)
        
        file_level = self.current_settings.get("file_level", "DEBUG")
        self.file_level.setCurrentText(file_level)
        
        # Log Destinations
        self.log_to_console.setChecked(self.current_settings.get("log_to_console", True))
        
        log_to_file = self.current_settings.get("log_to_file", True)
        self.log_to_file.setChecked(log_to_file)
        self.log_dir_container.setVisible(log_to_file)
        
        self.log_dir.setText(self.current_settings.get("log_directory", ""))
        
        # Log Rotation
        self.rotation_group.setEnabled(log_to_file)
        
        enable_rotation = self.current_settings.get("enable_rotation", True)
        self.enable_rotation.setChecked(enable_rotation)
        self.rotation_settings.setVisible(enable_rotation)
        
        self.max_size.setValue(self.current_settings.get("max_size", 10))
        self.backup_count.setValue(self.current_settings.get("backup_count", 5))
        
        # Additional Options
        self.include_timestamps.setChecked(self.current_settings.get("include_timestamps", True))
        self.include_thread_info.setChecked(self.current_settings.get("include_thread_info", True))
        self.include_source_info.setChecked(self.current_settings.get("include_source_info", True))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default logging settings"""
        return {
            "console_level": "INFO",
            "file_level": "DEBUG",
            "log_to_console": True,
            "log_to_file": True,
            "log_directory": os.path.join(os.path.expanduser("~"), "Documents", "Pawprinting_PyQt6_V2", "logs"),
            "enable_rotation": True,
            "max_size": 10,
            "backup_count": 5,
            "include_timestamps": True,
            "include_thread_info": True,
            "include_source_info": True
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        settings = {
            "console_level": self.console_level.currentText(),
            "file_level": self.file_level.currentText(),
            "log_to_console": self.log_to_console.isChecked(),
            "log_to_file": self.log_to_file.isChecked(),
            "log_directory": self.log_dir.text(),
            "enable_rotation": self.enable_rotation.isChecked(),
            "max_size": self.max_size.value(),
            "backup_count": self.backup_count.value(),
            "include_timestamps": self.include_timestamps.isChecked(),
            "include_thread_info": self.include_thread_info.isChecked(),
            "include_source_info": self.include_source_info.isChecked()
        }
        
        # Save to state manager under advanced.logging
        advanced_settings = self.state_manager.get_settings().get("advanced", {})
        advanced_settings["logging"] = settings
        self.state_manager.update_settings("advanced", advanced_settings)
        
        logger.info("Logging settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
