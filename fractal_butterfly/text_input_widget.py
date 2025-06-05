#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Text Input Widget for Fractal Butterfly Module

This widget allows users to enter text that will be converted to fractal parameters.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QTextCursor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QGroupBox, QFileDialog, QMessageBox, 
    QDialog, QListWidget, QListWidgetItem, 
    QDialogButtonBox, QLineEdit, QFormLayout, QSlider,
    QSpinBox, QFrame
)

# Import utilities to avoid local imports later
from utils.notification_manager import NotificationManager

# Configure logger
logger = logging.getLogger("pawprint_pyqt6.text_input")

from fractal_butterfly.text_to_fractal import TextToFractalConverter

class ConfigurationListDialog(QDialog):
    """Dialog for listing and selecting saved configurations"""
    
    def __init__(self, config_list: List[Dict[str, Any]], parent=None):
        """Initialize the dialog with list of configurations"""
        super().__init__(parent)
        
        self.selected_config = None
        self.config_list = config_list
        
        self.setWindowTitle("Saved Configurations")
        self.setMinimumSize(400, 300)
        
        # Setup UI
        layout = QVBoxLayout(self)
        
        # Instructions
        label = QLabel("Select a configuration to load:", self)
        layout.addWidget(label)
        
        # Configuration list
        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)
        
        # Add configurations to list
        for config in config_list:
            name = config.get("name", "Unnamed")
            created_at = config.get("created_at", "Unknown date")
            
            # Format date for display
            if "T" in created_at:
                date_part, time_part = created_at.split("T")
                time_part = time_part.split(".")[0]
                created_at = f"{date_part} {time_part}"
            
            item = QListWidgetItem(f"{name} (Created: {created_at})")
            item.setData(Qt.ItemDataRole.UserRole, config)
            self.list_widget.addItem(item)
        
        # Connect double-click
        self.list_widget.itemDoubleClicked.connect(self.accept)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Open | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def accept(self):
        """Accept the dialog and return selected configuration"""
        selected_items = self.list_widget.selectedItems()
        if selected_items:
            self.selected_config = selected_items[0].data(Qt.ItemDataRole.UserRole)
        super().accept()


class SaveConfigurationDialog(QDialog):
    """Dialog for saving a configuration with a custom name"""
    
    def __init__(self, parent=None):
        """Initialize the save dialog"""
        super().__init__(parent)
        
        self.config_name = ""
        
        self.setWindowTitle("Save Configuration")
        self.setMinimumWidth(300)
        
        # Setup UI
        layout = QVBoxLayout(self)
        
        # Name input
        form_layout = QFormLayout()
        self.name_input = QLineEdit(self)
        form_layout.addRow("Configuration Name:", self.name_input)
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def accept(self):
        """Accept the dialog and return the configuration name"""
        self.config_name = self.name_input.text().strip()
        if not self.config_name:
            QMessageBox.warning(
                self, 
                "Invalid Name", 
                "Please enter a valid configuration name."
            )
            return
        
        super().accept()


class TextInputWidget(QWidget):
    """Widget for text input and configuration management"""
    
    # Signal emitted when parameters are generated from text
    parametersGenerated = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """Initialize the text input widget"""
        super().__init__(parent)
        
        # Setup converter
        self.converter = TextToFractalConverter()
        
        # Current parameters
        self.current_params = None
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Text input group
        text_group = QGroupBox("Text Input", self)
        text_layout = QVBoxLayout(text_group)
        text_layout.setContentsMargins(5, 5, 5, 5)
        text_layout.setSpacing(5)
        
        # Suggestion label - add recommendation for song lyrics
        suggestion_label = QLabel(
            "<i>Try entering a few verses of your favorite song lyrics for unique fractal patterns!</i>"
        )
        suggestion_label.setStyleSheet(
            "color: #3498db; background-color: #EFF8FF; padding: 8px; border-radius: 4px;"
        )
        suggestion_label.setWordWrap(True)
        text_layout.addWidget(suggestion_label)
        
        # Info label
        info_label = QLabel(
            "Enter text (0-2000 characters) to generate a unique fractal pattern:",
            self
        )
        info_label.setWordWrap(True)
        text_layout.addWidget(info_label)
        
        # Input area
        self.text_input = QTextEdit(self)
        self.text_input.setPlaceholderText("Enter text here to generate fractal parameters...")
        self.text_input.setMinimumHeight(80)
        self.text_input.setMaximumHeight(120)
        text_layout.addWidget(self.text_input)
        
        # Character counter
        self.char_count_label = QLabel("0 / 2000 characters (auto-truncated if over limit)")
        self.char_count_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        text_layout.addWidget(self.char_count_label)
        
        # Connect text changed signal
        self.text_input.textChanged.connect(self.update_char_count)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.generate_button = QPushButton("Generate Parameters", self)
        self.generate_button.clicked.connect(self.on_generate_clicked)
        button_layout.addWidget(self.generate_button)
        
        self.save_button = QPushButton("Save Configuration", self)
        self.save_button.clicked.connect(self.on_save_clicked)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)
        
        self.load_button = QPushButton("Load Configuration", self)
        self.load_button.clicked.connect(self.on_load_clicked)
        button_layout.addWidget(self.load_button)
        
        text_layout.addLayout(button_layout)
        
        # Pawprint Settings group
        pash_group = QGroupBox("Pawprint Signature (Pash) Settings", self)
        pash_layout = QVBoxLayout(pash_group)
        pash_layout.setContentsMargins(5, 5, 5, 5)
        pash_layout.setSpacing(5)
        
        # Info label
        pash_info_label = QLabel(
            "Customize how the pawprint signature (Pash) is generated from your text:",
            self
        )
        pash_info_label.setWordWrap(True)
        pash_layout.addWidget(pash_info_label)
        
        # Controls layout
        controls_layout = QFormLayout()
        
        # Sampling points control
        self.sampling_points_spinner = QSpinBox(self)
        self.sampling_points_spinner.setRange(1, 10)
        self.sampling_points_spinner.setValue(5)  # Default value
        self.sampling_points_spinner.setToolTip("Number of text segments to sample")
        controls_layout.addRow("Sampling Points:", self.sampling_points_spinner)
        
        # Sequence length control
        self.sequence_length_spinner = QSpinBox(self)
        self.sequence_length_spinner.setRange(1, 5)
        self.sequence_length_spinner.setValue(3)  # Default value
        self.sequence_length_spinner.setToolTip("Number of characters to extract at each sampling point")
        controls_layout.addRow("Chars per Sample:", self.sequence_length_spinner)
        
        pash_layout.addLayout(controls_layout)
        
        # Preview section
        preview_layout = QVBoxLayout()
        preview_label = QLabel("Pash Preview:", self)
        self.pash_preview = QLabel("(Generate parameters to see Pash preview)", self)
        self.pash_preview.setStyleSheet(
            "padding: 10px; background-color: #f0f0f0; border-radius: 4px; font-family: monospace;"
        )
        self.pash_preview.setWordWrap(True)
        
        preview_layout.addWidget(preview_label)
        preview_layout.addWidget(self.pash_preview)
        pash_layout.addLayout(preview_layout)
        
        # Add groups to main layout
        layout.addWidget(text_group)
        layout.addWidget(pash_group)
    
    def update_char_count(self):
        """Update character count label and truncate if over 2000 characters"""
        text = self.text_input.toPlainText()
        count = len(text)
        
        # Automatically truncate text if over 2000 characters
        if count > 2000:
            # Temporarily block signals to prevent recursion
            self.text_input.blockSignals(True)
            
            # Truncate the text to 2000 characters
            truncated_text = text[:2000]
            self.text_input.setPlainText(truncated_text)
            
            # Update count to reflect truncated text
            count = 2000
            
            # Re-enable signals
            self.text_input.blockSignals(False)
            
            # Show notification about truncation
            logger.warning("Text automatically truncated to 2000 characters")
            
            # Show status bar warning
            NotificationManager.show_warning("Your text has been automatically truncated to 2000 characters.")
            
            # Also show a message box for better visibility
            QMessageBox.information(
                self,
                "Text Truncated", 
                "Your text has been automatically truncated to 2000 characters."
            )
            
            # Ensure cursor is at the end of text
            cursor = self.text_input.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.text_input.setTextCursor(cursor)
        
        # Update character count label
        self.char_count_label.setText(f"{count} / 2000 characters (auto-truncated if over limit)")
        
        # Set text color based on count
        if count >= 1800:  # Warning when approaching limit
            self.char_count_label.setStyleSheet("color: orange;")
        else:
            self.char_count_label.setStyleSheet("")
    
    def on_generate_clicked(self):
        """Generate parameters from text input"""
        text = self.text_input.toPlainText()
        
        if not text:
            logger.info("Text input empty, using default AIMF LLC pawprinting text.")
            # Default text about digital pawprinting and fractal patterns
            default_text = """
            Digital Pawprinting: The Art and Science of Unique Digital Signatures
            
            Digital pawprinting represents a revolutionary approach to digital forensics and cryptography. 
            Unlike traditional fingerprinting methods that rely on physical characteristics, pawprinting 
            analyzes the unique behavioral patterns and operational signatures left behind by digital 
            interactions.
            
            At AIMF LLC, we've pioneered advanced fractal-based analysis techniques that transform these 
            digital traces into stunning visual representations. Each pawprint contains mathematically 
            unique properties that, when combined with fractal butterfly algorithms, create visually 
            distinct patterns that are both aesthetically beautiful and forensically valuable.
            
            The fractal dimension of these patterns reveals crucial information about data complexity 
            and entropy. Higher dimensions typically indicate more complex behavioral patterns, while 
            the symmetry and density reveal insights about operational consistency and focus.
            
            By combining text-based input with these pawprint signatures, we create a multi-layered 
            security mechanism that is extraordinarily difficult to replicate. Each generated fractal 
            becomes a unique visual key, representing the convergence of linguistic entropy and 
            behavioral digital patterns.
            
            The beauty of this system lies in its perfect balance between mathematical precision and 
            artistic expression - where science and art unite to create something truly remarkable.
            """
            
            # Set the default text in the input box
            self.text_input.setPlainText(default_text)
            text = default_text
            
            # Update character count
            self.update_char_count()
            
            # Inform user (non-blocking)
            NotificationManager.show_info(
                "Default AIMF LLC pawprinting text has been applied.", 
                duration=5000
            )
        
        try:
            # Get Pash settings from UI
            sampling_points = self.sampling_points_spinner.value()
            sequence_length = self.sequence_length_spinner.value()
            
            # Generate parameters with custom Pash settings
            params = self.converter.text_to_parameters(
                text, 
                num_sampling_points=sampling_points,
                sequence_length=sequence_length
            )
            
            # Store current parameters
            self.current_params = params
            
            # Update Pash preview
            self.update_pash_preview(params)
            
            # Enable save button
            self.save_button.setEnabled(True)
            
            # Emit signal with parameters
            self.parametersGenerated.emit(params)
            
            # Show success message
            QMessageBox.information(
                self,
                "Parameters Generated",
                "Fractal parameters have been generated successfully."
            )
            
        except Exception as e:
            logger.error(f"Error generating parameters: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error generating parameters: {e}"
            )
    
    def on_save_clicked(self):
        """Save current configuration"""
        if not self.current_params:
            QMessageBox.warning(
                self,
                "No Parameters",
                "No parameters to save. Generate parameters first."
            )
            return
        
        # Show save dialog
        save_dialog = SaveConfigurationDialog(self)
        if save_dialog.exec() != QDialog.DialogCode.Accepted:
            return
        
        config_name = save_dialog.config_name
        
        try:
            # Save configuration
            file_path = self.converter.save_configuration(self.current_params, config_name)
            
            QMessageBox.information(
                self,
                "Configuration Saved",
                f"Configuration saved as '{config_name}'."
            )
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error saving configuration: {e}"
            )
    
    def on_load_clicked(self):
        """Load a saved configuration"""
        try:
            # Get list of configurations
            configs = self.converter.list_configurations()
            
            if not configs:
                QMessageBox.information(
                    self,
                    "No Configurations",
                    "No saved configurations found."
                )
                return
            
            # Show configuration list dialog
            list_dialog = ConfigurationListDialog(configs, self)
            if list_dialog.exec() != QDialog.DialogCode.Accepted:
                return
            
            if not list_dialog.selected_config:
                return
            
            # Load selected configuration
            file_path = list_dialog.selected_config["file_path"]
            config = self.converter.load_configuration(file_path)
            
            # Update text input
            if "text_input" in config:
                self.text_input.setPlainText(config["text_input"])
            
            # Store current parameters
            self.current_params = config
            
            # Enable save button
            self.save_button.setEnabled(True)
            
            # Emit signal with parameters
            self.parametersGenerated.emit(config)
            
            # Show success message
            QMessageBox.information(
                self,
                "Configuration Loaded",
                f"Configuration '{config.get('name', 'Unknown')}' loaded successfully."
            )
            
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Error loading configuration: {e}"
            )
    
    def update_pash_preview(self, params: Dict[str, Any]):
        """Update the Pash preview with the generated pawprint signature"""
        if params and "pawprint_signature" in params:
            pash = params["pawprint_signature"]
            if pash:
                # Format the Pash with character position markers
                formatted_pash = ""
                for i, char in enumerate(pash):
                    formatted_pash += f"{char}"
                
                # Highlight the Pash signature
                self.pash_preview.setText(formatted_pash)
                self.pash_preview.setStyleSheet(
                    "padding: 10px; background-color: #e6f7ff; border-radius: 4px; "
                    "font-family: monospace; font-size: 16px; letter-spacing: 2px; "
                    "color: #0066cc; border: 1px solid #99ccff;"
                )
            else:
                self.pash_preview.setText("(No Pash generated - text may be too short)")
                self.pash_preview.setStyleSheet(
                    "padding: 10px; background-color: #f0f0f0; border-radius: 4px; font-family: monospace;"
                )
        else:
            self.pash_preview.setText("(Generate parameters to see Pash preview)")
            self.pash_preview.setStyleSheet(
                "padding: 10px; background-color: #f0f0f0; border-radius: 4px; font-family: monospace;"
            )
    
    def set_parameters(self, params: Dict[str, Any]):
        """Set the current parameters and update UI"""
        self.current_params = params
        
        if params and "text_input" in params:
            self.text_input.setPlainText(params["text_input"])
            self.update_pash_preview(params)
            self.save_button.setEnabled(True)
