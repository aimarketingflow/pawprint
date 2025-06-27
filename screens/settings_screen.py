#!/usr/bin/env python3
"""
Settings Screen for Pawprinting PyQt6 V2 Application

Main settings screen with various configuration options organized by categories.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from typing import Optional, Dict, Any

from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QLabel, QPushButton, QFrame, QSpacerItem,
    QSizePolicy, QScrollArea, QGroupBox
)

# Import settings components
from screens.settings_components.settings_general import GeneralSettingsPanel
from screens.settings_components.settings_appearance import AppearanceSettingsPanel
from screens.settings_components.settings_analysis import AnalysisSettingsPanel
from screens.settings_components.settings_export import ExportSettingsPanel
from screens.settings_components.settings_fractal_main import FractalSettingsPanel
from screens.settings_components.settings_advanced_main import AdvancedSettingsPanel

# Import utility modules
from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.notification_manager import NotificationManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings")

class SettingsScreen(QWidget):
    """Main settings screen for the Pawprinting PyQt6 V2 application"""
    
    # Signal emitted when settings are saved
    settings_saved = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize settings screen"""
        super().__init__(parent)
        self.main_window = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        
        # Track whether settings have been modified
        self.settings_modified = False
        
        # Set up UI
        self.setup_ui()
        
        # Connect theme manager signals
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        logger.info("Settings screen initialized")
    
    def setup_ui(self):
        """Set up the settings UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header_frame = QFrame()
        header_frame.setObjectName("settingsHeader")
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("Settings")
        title_label.setObjectName("settingsTitle")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Tabs container - will be inside a scroll area
        self.tabs_widget = QTabWidget()
        self.tabs_widget.setObjectName("settingsTabs")
        
        # Create tab panels
        self.general_panel = GeneralSettingsPanel(self)
        self.appearance_panel = AppearanceSettingsPanel(self)
        self.analysis_panel = AnalysisSettingsPanel(self)
        self.export_panel = ExportSettingsPanel(self)
        self.fractal_panel = FractalSettingsPanel(self)
        self.advanced_panel = AdvancedSettingsPanel(self)
        
        # Add tabs
        self.tabs_widget.addTab(self.general_panel, "General")
        self.tabs_widget.addTab(self.appearance_panel, "Appearance")
        self.tabs_widget.addTab(self.analysis_panel, "Analysis")
        self.tabs_widget.addTab(self.export_panel, "Export")
        self.tabs_widget.addTab(self.fractal_panel, "Fractal")
        self.tabs_widget.addTab(self.advanced_panel, "Advanced")
        
        # Create scroll area for tabs
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.tabs_widget)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Button bar at bottom
        button_frame = QFrame()
        button_frame.setObjectName("settingsButtonBar")
        button_layout = QHBoxLayout(button_frame)
        
        self.restore_defaults_btn = QPushButton("Restore Defaults")
        self.restore_defaults_btn.setObjectName("secondaryButton")
        self.restore_defaults_btn.clicked.connect(self.on_restore_defaults)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("secondaryButton")
        self.cancel_btn.clicked.connect(self.on_cancel)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.clicked.connect(self.on_save)
        
        button_layout.addWidget(self.restore_defaults_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        # Add all components to main layout
        main_layout.addWidget(header_frame)
        main_layout.addWidget(scroll_area, 1)  # 1 = stretch factor
        main_layout.addWidget(button_frame)
        
        # Apply theme
        self.on_theme_changed(self.theme_manager.current_theme if self.theme_manager else "dark")
    
    def on_theme_changed(self, theme_name):
        """Handle theme change event"""
        logger.debug(f"Applying theme {theme_name} to settings screen")
        
        # Theme handled by theme manager, but we can add specific styling here
        pass
    
    def on_restore_defaults(self):
        """Handle restore defaults button click"""
        logger.info("Restore defaults requested")
        
        # Confirm with user
        confirmed = NotificationManager.show_confirmation(
            "Restore Defaults?",
            "This will reset all settings to their default values. This action cannot be undone.",
            "warning"
        )
        
        if confirmed:
            # Delegate to each panel
            self.general_panel.restore_defaults()
            self.appearance_panel.restore_defaults()
            self.analysis_panel.restore_defaults()
            self.export_panel.restore_defaults()
            self.fractal_panel.restore_defaults()
            self.advanced_panel.restore_defaults()
            
            self.settings_modified = True
            NotificationManager.show_message("Settings restored to defaults")
    
    def on_cancel(self):
        """Handle cancel button click"""
        logger.info("Settings changes canceled")
        
        if self.settings_modified:
            confirmed = NotificationManager.show_confirmation(
                "Discard Changes?",
                "You have unsaved changes that will be lost. Are you sure?",
                "warning"
            )
            
            if not confirmed:
                return
        
        # Return to previous screen
        self.main_window.show_dashboard_screen()
    
    def on_save(self):
        """Handle save button click"""
        logger.info("Saving settings")
        
        # Collect settings from each panel and save them
        try:
            # Delegate saving to each panel
            self.general_panel.save_settings()
            self.appearance_panel.save_settings()
            self.analysis_panel.save_settings()
            self.export_panel.save_settings()
            self.fractal_panel.save_settings()
            self.advanced_panel.save_settings()
            
            # Save to state manager
            self.state_manager.save_state()
            
            # Notify about successful save
            NotificationManager.show_message("Settings saved successfully")
            
            # Emit signal that settings were saved
            self.settings_saved.emit()
            
            # Reset modified flag
            self.settings_modified = False
            
            # Return to previous screen
            self.main_window.show_dashboard_screen()
            
        except Exception as e:
            logger.error(f"Error saving settings: {str(e)}")
            NotificationManager.show_dialog(
                "Save Error",
                f"Could not save settings: {str(e)}",
                "error"
            )
    
    def mark_as_modified(self):
        """Mark settings as modified"""
        self.settings_modified = True
