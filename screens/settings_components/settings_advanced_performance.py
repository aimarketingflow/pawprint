#!/usr/bin/env python3
"""
Performance Settings Panel Component for Pawprinting PyQt6 V2

Manages performance-related settings including memory usage,
threading options, and resource allocation parameters.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
from typing import Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLabel, QSpinBox, QGroupBox, QSlider,
    QCheckBox, QComboBox
)

from utils.state_manager import StateManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.advanced.performance")

class PerformanceSettingsPanel(QWidget):
    """Settings panel for performance options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize performance settings panel"""
        super().__init__(parent)
        self.parent_widget = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("advanced", {}).get("performance", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Performance settings panel initialized")
    
    def setup_ui(self):
        """Set up the performance settings UI"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # Memory Usage group
        self.memory_group = QGroupBox("Memory Usage")
        memory_layout = QFormLayout(self.memory_group)
        memory_layout.setContentsMargins(15, 15, 15, 15)
        memory_layout.setSpacing(10)
        
        # Memory limit
        self.memory_limit = QSpinBox()
        self.memory_limit.setRange(256, 8192)
        self.memory_limit.setSingleStep(128)
        self.memory_limit.setSuffix(" MB")
        self.memory_limit.valueChanged.connect(self.on_setting_changed)
        memory_layout.addRow("Memory usage limit:", self.memory_limit)
        
        # Cache size
        self.cache_size = QSpinBox()
        self.cache_size.setRange(50, 2000)
        self.cache_size.setSingleStep(50)
        self.cache_size.setSuffix(" MB")
        self.cache_size.valueChanged.connect(self.on_setting_changed)
        memory_layout.addRow("Cache size:", self.cache_size)
        
        # Auto-clean cache
        self.auto_clean_cache = QCheckBox("Automatically clean cache when full")
        self.auto_clean_cache.stateChanged.connect(self.on_setting_changed)
        memory_layout.addRow("", self.auto_clean_cache)
        
        # Threading Options group
        self.threading_group = QGroupBox("Threading Options")
        threading_layout = QFormLayout(self.threading_group)
        threading_layout.setContentsMargins(15, 15, 15, 15)
        threading_layout.setSpacing(10)
        
        # Max threads
        self.max_threads = QSpinBox()
        self.max_threads.setRange(1, 32)
        self.max_threads.valueChanged.connect(self.on_setting_changed)
        threading_layout.addRow("Max threads:", self.max_threads)
        
        # Thread priority
        self.thread_priority = QComboBox()
        self.thread_priority.addItem("Low", "low")
        self.thread_priority.addItem("Normal", "normal")
        self.thread_priority.addItem("High", "high")
        self.thread_priority.currentIndexChanged.connect(self.on_setting_changed)
        threading_layout.addRow("Thread priority:", self.thread_priority)
        
        # Processing Options group
        self.processing_group = QGroupBox("Processing Options")
        processing_layout = QVBoxLayout(self.processing_group)
        processing_layout.setContentsMargins(15, 15, 15, 15)
        processing_layout.setSpacing(10)
        
        # CPU usage limit
        cpu_layout = QVBoxLayout()
        cpu_label = QLabel("CPU usage limit:")
        self.cpu_limit = QSlider(Qt.Orientation.Horizontal)
        self.cpu_limit.setRange(10, 100)
        self.cpu_limit.setSingleStep(5)
        self.cpu_limit.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.cpu_limit.setTickInterval(10)
        self.cpu_limit.valueChanged.connect(self.on_cpu_limit_changed)
        
        self.cpu_limit_value = QLabel("75%")
        self.cpu_limit_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        cpu_layout.addWidget(cpu_label)
        cpu_layout.addWidget(self.cpu_limit)
        cpu_layout.addWidget(self.cpu_limit_value)
        processing_layout.addLayout(cpu_layout)
        
        # Batch processing
        self.use_batch_processing = QCheckBox("Use batch processing for large datasets")
        self.use_batch_processing.stateChanged.connect(self.on_setting_changed)
        processing_layout.addWidget(self.use_batch_processing)
        
        # Batch size
        batch_layout = QHBoxLayout()
        batch_label = QLabel("Batch size:")
        self.batch_size = QSpinBox()
        self.batch_size.setRange(10, 10000)
        self.batch_size.setSingleStep(10)
        self.batch_size.setEnabled(False)  # Initially disabled
        self.batch_size.valueChanged.connect(self.on_setting_changed)
        
        batch_layout.addWidget(batch_label)
        batch_layout.addWidget(self.batch_size)
        batch_layout.addStretch(1)
        processing_layout.addLayout(batch_layout)
        
        # Connect batch processing checkbox to batch size enable/disable
        self.use_batch_processing.stateChanged.connect(
            lambda state: self.batch_size.setEnabled(state == Qt.CheckState.Checked.value)
        )
        
        # IO Settings group
        self.io_group = QGroupBox("I/O Settings")
        io_layout = QFormLayout(self.io_group)
        io_layout.setContentsMargins(15, 15, 15, 15)
        io_layout.setSpacing(10)
        
        # Buffer size
        self.buffer_size = QSpinBox()
        self.buffer_size.setRange(1, 128)
        self.buffer_size.setSuffix(" MB")
        self.buffer_size.valueChanged.connect(self.on_setting_changed)
        io_layout.addRow("File buffer size:", self.buffer_size)
        
        # Use async IO
        self.use_async_io = QCheckBox("Use asynchronous I/O")
        self.use_async_io.stateChanged.connect(self.on_setting_changed)
        io_layout.addRow("", self.use_async_io)
        
        # Add all groups to main layout
        main_layout.addWidget(self.memory_group)
        main_layout.addWidget(self.threading_group)
        main_layout.addWidget(self.processing_group)
        main_layout.addWidget(self.io_group)
    
    def on_cpu_limit_changed(self, value):
        """Update CPU limit value label and notify about setting change"""
        self.cpu_limit_value.setText(f"{value}%")
        self.on_setting_changed()
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_widget:
            self.parent_widget.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Memory Usage
        self.memory_limit.setValue(self.current_settings.get("memory_limit", 1024))
        self.cache_size.setValue(self.current_settings.get("cache_size", 200))
        self.auto_clean_cache.setChecked(self.current_settings.get("auto_clean_cache", True))
        
        # Threading Options
        self.max_threads.setValue(self.current_settings.get("max_threads", 4))
        
        thread_priority = self.current_settings.get("thread_priority", "normal")
        index = self.thread_priority.findData(thread_priority)
        if index >= 0:
            self.thread_priority.setCurrentIndex(index)
        
        # Processing Options
        self.cpu_limit.setValue(self.current_settings.get("cpu_limit", 75))
        self.on_cpu_limit_changed(self.cpu_limit.value())
        
        use_batch = self.current_settings.get("use_batch_processing", False)
        self.use_batch_processing.setChecked(use_batch)
        self.batch_size.setEnabled(use_batch)
        self.batch_size.setValue(self.current_settings.get("batch_size", 100))
        
        # IO Settings
        self.buffer_size.setValue(self.current_settings.get("buffer_size", 8))
        self.use_async_io.setChecked(self.current_settings.get("use_async_io", True))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default performance settings"""
        return {
            "memory_limit": 1024,
            "cache_size": 200,
            "auto_clean_cache": True,
            "max_threads": 4,
            "thread_priority": "normal",
            "cpu_limit": 75,
            "use_batch_processing": False,
            "batch_size": 100,
            "buffer_size": 8,
            "use_async_io": True
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        settings = {
            "memory_limit": self.memory_limit.value(),
            "cache_size": self.cache_size.value(),
            "auto_clean_cache": self.auto_clean_cache.isChecked(),
            "max_threads": self.max_threads.value(),
            "thread_priority": self.thread_priority.currentData(),
            "cpu_limit": self.cpu_limit.value(),
            "use_batch_processing": self.use_batch_processing.isChecked(),
            "batch_size": self.batch_size.value(),
            "buffer_size": self.buffer_size.value(),
            "use_async_io": self.use_async_io.isChecked()
        }
        
        # Save to state manager under advanced.performance
        advanced_settings = self.state_manager.get_settings().get("advanced", {})
        advanced_settings["performance"] = settings
        self.state_manager.update_settings("advanced", advanced_settings)
        
        logger.info("Performance settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
