#!/usr/bin/env python3
"""
Advanced Settings Main Panel for Pawprinting PyQt6 V2

Main container for advanced settings that loads and organizes
subcomponents for developer, performance, and logging options.

Author: AIMF LLC
Date: June 20, 2025
"""

import logging
from typing import Dict, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel
)

from utils.state_manager import StateManager

# Import subcomponents
from screens.settings_components.settings_advanced_developer import DeveloperSettingsPanel
from screens.settings_components.settings_advanced_performance import PerformanceSettingsPanel
from screens.settings_components.settings_advanced_logging import LoggingSettingsPanel

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.advanced.main")

class AdvancedSettingsPanel(QWidget):
    """Main container for advanced settings that combines developer, performance, and logging settings"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize advanced settings panel with subcomponents"""
        super().__init__(parent)
        self.parent_screen = parent
        self.state_manager = StateManager.get_instance()
        
        # Setup UI
        self.setup_ui()
        
        logger.debug("Advanced settings main panel initialized")
    
    def setup_ui(self):
        """Set up the advanced settings UI with subcomponents"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Header
        header_label = QLabel("Advanced Settings")
        header_label.setStyleSheet("font-size: 14pt; font-weight: bold;")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Description
        description = QLabel(
            "These advanced settings should only be modified if you understand their impact. "
            "Improper configuration may affect application performance and stability."
        )
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 10pt;")
        main_layout.addWidget(description)
        
        # Add developer settings subcomponent
        self.dev_settings = DeveloperSettingsPanel(self)
        self.dev_settings.settings_modified.connect(self.on_subcomponent_modified)
        main_layout.addWidget(self.dev_settings)
        
        # Add performance settings subcomponent
        self.perf_settings = PerformanceSettingsPanel(self)
        self.perf_settings.settings_modified.connect(self.on_subcomponent_modified)
        main_layout.addWidget(self.perf_settings)
        
        # Add logging settings subcomponent
        self.log_settings = LoggingSettingsPanel(self)
        self.log_settings.settings_modified.connect(self.on_subcomponent_modified)
        main_layout.addWidget(self.log_settings)
        
        # Add a stretch at the end to push everything up
        main_layout.addStretch(1)
    
    def on_subcomponent_modified(self):
        """Forward modification signal from subcomponents"""
        self.mark_as_modified()
    
    def mark_as_modified(self):
        """Mark settings as modified"""
        if self.parent_screen:
            self.parent_screen.mark_as_modified()
        self.settings_modified.emit()
    
    def save_settings(self) -> Dict[str, Any]:
        """Save settings from all subcomponents"""
        # Collect settings from subcomponents
        dev_settings = self.dev_settings.save_settings()
        perf_settings = self.perf_settings.save_settings()
        log_settings = self.log_settings.save_settings()
        
        # Each subcomponent has already saved its settings to the state_manager
        logger.info("All advanced settings saved")
        return {
            "developer": dev_settings,
            "performance": perf_settings,
            "logging": log_settings
        }
    
    def restore_defaults(self):
        """Restore defaults in all subcomponents"""
        self.dev_settings.restore_defaults()
        self.perf_settings.restore_defaults()
        self.log_settings.restore_defaults()
        self.mark_as_modified()
        logger.info("All advanced settings restored to defaults")
