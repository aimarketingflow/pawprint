#!/usr/bin/env python3
"""
Analysis Settings Panel Component for Pawprinting PyQt6 V2

Manages settings related to pawprint analysis, including algorithm options,
sensitivity settings, and pattern detection preferences.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from typing import Dict, Any, List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QComboBox, QSlider, QCheckBox, QGroupBox,
    QPushButton, QFrame, QSpacerItem, QSizePolicy,
    QSpinBox, QDoubleSpinBox, QListWidget, QListWidgetItem
)

from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.notification_manager import NotificationManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.analysis")

class AnalysisSettingsPanel(QWidget):
    """Analysis settings panel for configuring pawprint analysis options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize analysis settings panel"""
        super().__init__(parent)
        self.parent_screen = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("analysis", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Analysis settings panel initialized")
    
    def setup_ui(self):
        """Set up the analysis settings UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Algorithm Settings
        self.algorithm_group = QGroupBox("Algorithm Settings")
        algorithm_layout = QFormLayout(self.algorithm_group)
        algorithm_layout.setContentsMargins(15, 15, 15, 15)
        algorithm_layout.setSpacing(10)
        
        # Analysis algorithm
        self.analysis_algorithm = QComboBox()
        self.analysis_algorithm.addItem("Standard Analysis (Default)", "standard")
        self.analysis_algorithm.addItem("Deep Scan", "deep_scan")
        self.analysis_algorithm.addItem("Quick Scan", "quick_scan")
        self.analysis_algorithm.addItem("Forensic Mode", "forensic")
        self.analysis_algorithm.currentIndexChanged.connect(self.on_setting_changed)
        algorithm_layout.addRow("Analysis algorithm:", self.analysis_algorithm)
        
        # Thread count
        self.thread_count = QSpinBox()
        self.thread_count.setRange(1, 32)
        self.thread_count.valueChanged.connect(self.on_setting_changed)
        algorithm_layout.addRow("Thread count:", self.thread_count)
        
        # Sensitivity Settings
        self.sensitivity_group = QGroupBox("Sensitivity Settings")
        sensitivity_layout = QVBoxLayout(self.sensitivity_group)
        sensitivity_layout.setContentsMargins(15, 15, 15, 15)
        sensitivity_layout.setSpacing(15)
        
        # Pattern detection threshold
        threshold_layout = QVBoxLayout()
        threshold_label = QLabel("Pattern detection threshold:")
        self.pattern_threshold = QSlider(Qt.Orientation.Horizontal)
        self.pattern_threshold.setRange(10, 100)
        self.pattern_threshold.setSingleStep(5)
        self.pattern_threshold.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.pattern_threshold.setTickInterval(10)
        self.pattern_threshold.valueChanged.connect(self.on_threshold_changed)
        
        self.threshold_value_label = QLabel("50%")
        self.threshold_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.pattern_threshold)
        threshold_layout.addWidget(self.threshold_value_label)
        sensitivity_layout.addLayout(threshold_layout)
        
        # Noise filtering
        noise_layout = QVBoxLayout()
        noise_label = QLabel("Noise filtering level:")
        self.noise_filtering = QSlider(Qt.Orientation.Horizontal)
        self.noise_filtering.setRange(0, 100)
        self.noise_filtering.setSingleStep(5)
        self.noise_filtering.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.noise_filtering.setTickInterval(10)
        self.noise_filtering.valueChanged.connect(self.on_noise_changed)
        
        self.noise_value_label = QLabel("50%")
        self.noise_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        noise_layout.addWidget(noise_label)
        noise_layout.addWidget(self.noise_filtering)
        noise_layout.addWidget(self.noise_value_label)
        sensitivity_layout.addLayout(noise_layout)
        
        # Pattern Types
        self.pattern_types_group = QGroupBox("Pattern Types")
        pattern_types_layout = QVBoxLayout(self.pattern_types_group)
        pattern_types_layout.setContentsMargins(15, 15, 15, 15)
        pattern_types_layout.setSpacing(10)
        
        # Pattern types list with checkboxes
        pattern_types = [
            ("Structural patterns", "structural", True),
            ("Behavioral patterns", "behavioral", True),
            ("Temporal patterns", "temporal", True),
            ("Metadata patterns", "metadata", True),
            ("Cryptographic patterns", "crypto", True),
            ("Network patterns", "network", True),
            ("System-specific patterns", "system", False),
            ("Application-specific patterns", "application", False)
        ]
        
        self.pattern_checkboxes = {}
        for display_name, pattern_id, default_enabled in pattern_types:
            checkbox = QCheckBox(display_name)
            checkbox.setObjectName(f"pattern_{pattern_id}")
            checkbox.stateChanged.connect(self.on_setting_changed)
            pattern_types_layout.addWidget(checkbox)
            self.pattern_checkboxes[pattern_id] = checkbox
        
        # Select All / Deselect All
        select_buttons_layout = QHBoxLayout()
        
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_patterns)
        
        self.deselect_all_btn = QPushButton("Deselect All")
        self.deselect_all_btn.clicked.connect(self.deselect_all_patterns)
        
        select_buttons_layout.addWidget(self.select_all_btn)
        select_buttons_layout.addWidget(self.deselect_all_btn)
        pattern_types_layout.addLayout(select_buttons_layout)
        
        # Advanced Options
        self.advanced_group = QGroupBox("Advanced Options")
        advanced_layout = QFormLayout(self.advanced_group)
        advanced_layout.setContentsMargins(15, 15, 15, 15)
        advanced_layout.setSpacing(10)
        
        # Enable detailed logging
        self.detailed_logging = QCheckBox("Enable detailed analysis logging")
        self.detailed_logging.stateChanged.connect(self.on_setting_changed)
        advanced_layout.addRow("", self.detailed_logging)
        
        # Save intermediate results
        self.save_intermediate = QCheckBox("Save intermediate analysis results")
        self.save_intermediate.stateChanged.connect(self.on_setting_changed)
        advanced_layout.addRow("", self.save_intermediate)
        
        # Auto-recover from analysis failures
        self.auto_recover = QCheckBox("Auto-recover from analysis failures")
        self.auto_recover.stateChanged.connect(self.on_setting_changed)
        advanced_layout.addRow("", self.auto_recover)
        
        # Progress update interval
        self.progress_interval = QSpinBox()
        self.progress_interval.setRange(100, 5000)
        self.progress_interval.setSingleStep(100)
        self.progress_interval.setSuffix(" ms")
        self.progress_interval.valueChanged.connect(self.on_setting_changed)
        advanced_layout.addRow("Progress update interval:", self.progress_interval)
        
        # Add all groups to main layout
        main_layout.addWidget(self.algorithm_group)
        main_layout.addWidget(self.sensitivity_group)
        main_layout.addWidget(self.pattern_types_group)
        main_layout.addWidget(self.advanced_group)
        main_layout.addStretch(1)
    
    def on_threshold_changed(self, value):
        """Update threshold value label and notify about setting change"""
        self.threshold_value_label.setText(f"{value}%")
        self.on_setting_changed()
    
    def on_noise_changed(self, value):
        """Update noise value label and notify about setting change"""
        self.noise_value_label.setText(f"{value}%")
        self.on_setting_changed()
    
    def select_all_patterns(self):
        """Select all pattern types"""
        for checkbox in self.pattern_checkboxes.values():
            checkbox.setChecked(True)
    
    def deselect_all_patterns(self):
        """Deselect all pattern types"""
        for checkbox in self.pattern_checkboxes.values():
            checkbox.setChecked(False)
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_screen:
            self.parent_screen.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Algorithm Settings
        algorithm = self.current_settings.get("algorithm", "standard")
        index = self.analysis_algorithm.findData(algorithm)
        if index >= 0:
            self.analysis_algorithm.setCurrentIndex(index)
        
        self.thread_count.setValue(self.current_settings.get("thread_count", 4))
        
        # Sensitivity Settings
        self.pattern_threshold.setValue(self.current_settings.get("pattern_threshold", 50))
        self.threshold_value_label.setText(f"{self.pattern_threshold.value()}%")
        
        self.noise_filtering.setValue(self.current_settings.get("noise_filtering", 50))
        self.noise_value_label.setText(f"{self.noise_filtering.value()}%")
        
        # Pattern Types
        enabled_patterns = self.current_settings.get("enabled_patterns", {})
        for pattern_id, checkbox in self.pattern_checkboxes.items():
            # Default to True for core patterns if not specified
            default_enabled = pattern_id in ["structural", "behavioral", "temporal", "metadata", "crypto", "network"]
            checkbox.setChecked(enabled_patterns.get(pattern_id, default_enabled))
        
        # Advanced Options
        self.detailed_logging.setChecked(self.current_settings.get("detailed_logging", True))
        self.save_intermediate.setChecked(self.current_settings.get("save_intermediate", False))
        self.auto_recover.setChecked(self.current_settings.get("auto_recover", True))
        self.progress_interval.setValue(self.current_settings.get("progress_interval", 500))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default analysis settings"""
        return {
            "algorithm": "standard",
            "thread_count": 4,
            "pattern_threshold": 50,
            "noise_filtering": 50,
            "enabled_patterns": {
                "structural": True,
                "behavioral": True, 
                "temporal": True,
                "metadata": True,
                "crypto": True,
                "network": True,
                "system": False,
                "application": False
            },
            "detailed_logging": True,
            "save_intermediate": False,
            "auto_recover": True,
            "progress_interval": 500
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        # Collect enabled pattern types
        enabled_patterns = {}
        for pattern_id, checkbox in self.pattern_checkboxes.items():
            enabled_patterns[pattern_id] = checkbox.isChecked()
        
        settings = {
            "algorithm": self.analysis_algorithm.currentData(),
            "thread_count": self.thread_count.value(),
            "pattern_threshold": self.pattern_threshold.value(),
            "noise_filtering": self.noise_filtering.value(),
            "enabled_patterns": enabled_patterns,
            "detailed_logging": self.detailed_logging.isChecked(),
            "save_intermediate": self.save_intermediate.isChecked(),
            "auto_recover": self.auto_recover.isChecked(),
            "progress_interval": self.progress_interval.value()
        }
        
        # Save to state manager
        self.state_manager.update_settings("analysis", settings)
        logger.info("Analysis settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
