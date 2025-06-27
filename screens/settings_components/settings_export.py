#!/usr/bin/env python3
"""
Export Settings Panel Component for Pawprinting PyQt6 V2

Manages settings related to exporting pawprint analysis results,
including file formats, report customization, and branding options.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QComboBox, QCheckBox, QGroupBox,
    QPushButton, QFileDialog, QListWidget, QListWidgetItem,
    QFrame, QSpacerItem, QSizePolicy
)

from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager
from utils.notification_manager import NotificationManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.settings.export")

class ExportSettingsPanel(QWidget):
    """Export settings panel for configuring report and export options"""
    
    # Signal when settings are modified
    settings_modified = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize export settings panel"""
        super().__init__(parent)
        self.parent_screen = parent
        self.state_manager = StateManager.get_instance()
        
        # Load current settings
        self.current_settings = self.state_manager.get_settings().get("export", {})
        if not self.current_settings:
            self.current_settings = self.get_default_settings()
        
        # Setup UI
        self.setup_ui()
        
        # Load settings into UI
        self.load_settings()
        
        logger.debug("Export settings panel initialized")
    
    def setup_ui(self):
        """Set up the export settings UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Export Formats
        self.formats_group = QGroupBox("Export Formats")
        formats_layout = QVBoxLayout(self.formats_group)
        formats_layout.setContentsMargins(15, 15, 15, 15)
        formats_layout.setSpacing(10)
        
        # Default format
        format_selector_layout = QFormLayout()
        self.default_format = QComboBox()
        self.default_format.addItem("JSON (Default)", "json")
        self.default_format.addItem("XML", "xml")
        self.default_format.addItem("CSV", "csv")
        self.default_format.addItem("PDF", "pdf")
        self.default_format.addItem("HTML", "html")
        self.default_format.addItem("Markdown", "md")
        self.default_format.currentIndexChanged.connect(self.on_setting_changed)
        format_selector_layout.addRow("Default export format:", self.default_format)
        formats_layout.addLayout(format_selector_layout)
        
        # Available export formats checkboxes
        formats_layout.addWidget(QLabel("Available export formats:"))
        
        self.format_checkboxes = {}
        
        format_options = [
            ("JSON", "json"),
            ("XML", "xml"),
            ("CSV", "csv"),
            ("PDF", "pdf"),
            ("HTML", "html"),
            ("Markdown", "md"),
            ("Plain Text", "txt")
        ]
        
        for display_name, format_id in format_options:
            checkbox = QCheckBox(display_name)
            checkbox.setObjectName(f"format_{format_id}")
            checkbox.stateChanged.connect(self.on_setting_changed)
            formats_layout.addWidget(checkbox)
            self.format_checkboxes[format_id] = checkbox
        
        # Report Customization
        self.report_group = QGroupBox("Report Customization")
        report_layout = QFormLayout(self.report_group)
        report_layout.setContentsMargins(15, 15, 15, 15)
        report_layout.setSpacing(10)
        
        # Company Name
        self.company_name = QLineEdit()
        self.company_name.setPlaceholderText("Your company name")
        self.company_name.textChanged.connect(self.on_setting_changed)
        report_layout.addRow("Company name:", self.company_name)
        
        # Author Name
        self.author_name = QLineEdit()
        self.author_name.setPlaceholderText("Your name")
        self.author_name.textChanged.connect(self.on_setting_changed)
        report_layout.addRow("Author name:", self.author_name)
        
        # Logo selection
        logo_layout = QHBoxLayout()
        self.logo_path = QLineEdit()
        self.logo_path.setReadOnly(True)
        self.logo_path.setPlaceholderText("No logo selected")
        
        self.browse_logo_btn = QPushButton("Browse...")
        self.browse_logo_btn.clicked.connect(self.browse_logo)
        
        self.clear_logo_btn = QPushButton("Clear")
        self.clear_logo_btn.clicked.connect(self.clear_logo)
        
        logo_layout.addWidget(self.logo_path)
        logo_layout.addWidget(self.browse_logo_btn)
        logo_layout.addWidget(self.clear_logo_btn)
        report_layout.addRow("Company logo:", logo_layout)
        
        # Report Options
        self.options_group = QGroupBox("Report Options")
        options_layout = QVBoxLayout(self.options_group)
        options_layout.setContentsMargins(15, 15, 15, 15)
        options_layout.setSpacing(10)
        
        # Include options
        self.include_timestamp = QCheckBox("Include timestamp in reports")
        self.include_timestamp.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_timestamp)
        
        self.include_summary = QCheckBox("Include executive summary")
        self.include_summary.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_summary)
        
        self.include_charts = QCheckBox("Include charts and visualizations")
        self.include_charts.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_charts)
        
        self.include_raw_data = QCheckBox("Include raw data appendix")
        self.include_raw_data.stateChanged.connect(self.on_setting_changed)
        options_layout.addWidget(self.include_raw_data)
        
        # Auto-export options
        self.auto_export_group = QGroupBox("Auto-Export Options")
        auto_export_layout = QVBoxLayout(self.auto_export_group)
        auto_export_layout.setContentsMargins(15, 15, 15, 15)
        auto_export_layout.setSpacing(10)
        
        self.auto_export_results = QCheckBox("Automatically export results after analysis")
        self.auto_export_results.stateChanged.connect(self.on_setting_changed)
        auto_export_layout.addWidget(self.auto_export_results)
        
        self.auto_export_comparisons = QCheckBox("Automatically export comparison results")
        self.auto_export_comparisons.stateChanged.connect(self.on_setting_changed)
        auto_export_layout.addWidget(self.auto_export_comparisons)
        
        # Add all groups to main layout
        main_layout.addWidget(self.formats_group)
        main_layout.addWidget(self.report_group)
        main_layout.addWidget(self.options_group)
        main_layout.addWidget(self.auto_export_group)
        main_layout.addStretch(1)
    
    def browse_logo(self):
        """Open file dialog to select logo image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Logo Image",
            self.logo_path.text() or str(Path.home()),
            "Image Files (*.png *.jpg *.jpeg *.bmp *.svg);;All Files (*)"
        )
        
        if file_path:
            self.logo_path.setText(file_path)
            self.on_setting_changed()
    
    def clear_logo(self):
        """Clear selected logo"""
        self.logo_path.setText("")
        self.on_setting_changed()
    
    def on_setting_changed(self):
        """Handle when any setting is changed"""
        if self.parent_screen:
            self.parent_screen.mark_as_modified()
        self.settings_modified.emit()
    
    def load_settings(self):
        """Load current settings into UI components"""
        # Export Formats
        default_format = self.current_settings.get("default_format", "json")
        index = self.default_format.findData(default_format)
        if index >= 0:
            self.default_format.setCurrentIndex(index)
        
        available_formats = self.current_settings.get("available_formats", {})
        for format_id, checkbox in self.format_checkboxes.items():
            # Default to True for common formats if not specified
            default_enabled = format_id in ["json", "csv", "pdf", "html"]
            checkbox.setChecked(available_formats.get(format_id, default_enabled))
        
        # Report Customization
        self.company_name.setText(self.current_settings.get("company_name", "AIMF LLC"))
        self.author_name.setText(self.current_settings.get("author_name", ""))
        self.logo_path.setText(self.current_settings.get("logo_path", ""))
        
        # Report Options
        self.include_timestamp.setChecked(self.current_settings.get("include_timestamp", True))
        self.include_summary.setChecked(self.current_settings.get("include_summary", True))
        self.include_charts.setChecked(self.current_settings.get("include_charts", True))
        self.include_raw_data.setChecked(self.current_settings.get("include_raw_data", False))
        
        # Auto-export Options
        self.auto_export_results.setChecked(self.current_settings.get("auto_export_results", False))
        self.auto_export_comparisons.setChecked(self.current_settings.get("auto_export_comparisons", False))
    
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default export settings"""
        return {
            "default_format": "json",
            "available_formats": {
                "json": True,
                "xml": True,
                "csv": True,
                "pdf": True,
                "html": True,
                "md": True,
                "txt": False
            },
            "company_name": "AIMF LLC",
            "author_name": "",
            "logo_path": "",
            "include_timestamp": True,
            "include_summary": True,
            "include_charts": True,
            "include_raw_data": False,
            "auto_export_results": False,
            "auto_export_comparisons": False
        }
    
    def save_settings(self) -> Dict[str, Any]:
        """Save current settings to state manager"""
        # Collect available formats
        available_formats = {}
        for format_id, checkbox in self.format_checkboxes.items():
            available_formats[format_id] = checkbox.isChecked()
        
        settings = {
            "default_format": self.default_format.currentData(),
            "available_formats": available_formats,
            "company_name": self.company_name.text(),
            "author_name": self.author_name.text(),
            "logo_path": self.logo_path.text(),
            "include_timestamp": self.include_timestamp.isChecked(),
            "include_summary": self.include_summary.isChecked(),
            "include_charts": self.include_charts.isChecked(),
            "include_raw_data": self.include_raw_data.isChecked(),
            "auto_export_results": self.auto_export_results.isChecked(),
            "auto_export_comparisons": self.auto_export_comparisons.isChecked()
        }
        
        # Save to state manager
        self.state_manager.update_settings("export", settings)
        logger.info("Export settings saved")
        
        return settings
    
    def restore_defaults(self):
        """Restore default settings"""
        self.current_settings = self.get_default_settings()
        self.load_settings()
        self.on_setting_changed()
