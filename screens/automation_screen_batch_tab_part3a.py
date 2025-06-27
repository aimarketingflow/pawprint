#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab (Part 3a)
Execution controls and action buttons 
"""

import os
import sys
import logging
import datetime
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QGroupBox,
    QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

logger = logging.getLogger(__name__)

# This part extends the setup_batch_operations_tab function from parts 1 and 2

def setup_batch_operations_tab_part3a(self):
    """
    Setup the execution controls for the Batch Operations tab
    This continues the implementation from parts 1 and 2
    """
    # Get existing layout
    batch_layout = self.batch_operations_tab.layout()
    
    # Create execution controls group
    exec_group = QGroupBox("Execution Controls")
    exec_layout = QVBoxLayout(exec_group)
    
    # Add buttons layout
    buttons_layout = QHBoxLayout()
    
    # Validate button - checks configuration before execution
    self.validate_button = QPushButton("Validate")
    self.validate_button.setIcon(QIcon.fromTheme("dialog-question"))
    self.validate_button.setToolTip("Validate configuration before execution")
    self.validate_button.clicked.connect(self.validate_batch_config)
    self.validate_button.setMinimumHeight(40)
    
    # Execute button - starts the batch operation
    self.execute_button = QPushButton("Execute Batch Operation")
    self.execute_button.setIcon(QIcon.fromTheme("media-playback-start"))
    self.execute_button.setToolTip("Start the batch operation with current settings")
    self.execute_button.clicked.connect(self.execute_batch_operation)
    self.execute_button.setMinimumHeight(40)
    self.execute_button.setStyleSheet("""
        QPushButton {
            background-color: #37123C;
            border: 2px solid #9b30ff;
            border-radius: 4px;
            color: #e0e0e0;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #4A1E5B;
        }
        QPushButton:pressed {
            background-color: #9b30ff;
            color: white;
        }
    """)
    
    # Cancel button - stops the current operation
    self.cancel_button = QPushButton("Cancel")
    self.cancel_button.setIcon(QIcon.fromTheme("media-playback-stop"))
    self.cancel_button.setToolTip("Cancel the current batch operation")
    self.cancel_button.clicked.connect(self.cancel_batch_operation)
    self.cancel_button.setMinimumHeight(40)
    self.cancel_button.setEnabled(False)  # Disabled initially
    
    # Add buttons to layout
    buttons_layout.addWidget(self.validate_button)
    buttons_layout.addWidget(self.execute_button, 2)  # Higher stretch factor
    buttons_layout.addWidget(self.cancel_button)
    
    # Add to execution group
    exec_layout.addLayout(buttons_layout)
    
    # Add execution group to main layout
    batch_layout.addWidget(exec_group)
    
    # Create a placeholder for progress tracking (will be implemented in part 3b)
    self.progress_placeholder = QLabel("Progress tracking will be displayed here")
    self.progress_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.progress_placeholder.setStyleSheet("color: #777; font-style: italic;")
    self.progress_placeholder.setSizePolicy(
        QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
    )
    batch_layout.addWidget(self.progress_placeholder)

def validate_batch_config(self):
    """Validate the batch operation configuration before execution"""
    # Get selected folders
    folders = self.get_selected_folders()
    
    if not folders:
        QMessageBox.warning(self, "Validation Error", 
                           "No folders selected for batch processing")
        return False
    
    # Get operation type
    op_index = self.operation_type.currentIndex()
    op_types = ["generate", "refresh", "compare", "report"]
    op_type = op_types[op_index] if op_index < len(op_types) else "generate"
    
    # Validate based on operation type
    if op_type == "generate":
        # Check output directory if specified
        output_dir = self.output_dir.text()
        if output_dir and not os.path.isdir(output_dir):
            reply = QMessageBox.question(
                self, "Output Directory",
                f"Output directory '{output_dir}' does not exist. Create it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.makedirs(output_dir, exist_ok=True)
                except Exception as e:
                    QMessageBox.critical(self, "Error",
                                       f"Failed to create output directory: {str(e)}")
                    return False
            else:
                return False
                
    elif op_type == "refresh":
        # For refresh, ensure pawprints exist if auto-detect is off
        if not self.auto_detect.isChecked():
            # This would require an actual check for existing pawprints
            # For now, just inform user
            QMessageBox.information(
                self, "Validation Note",
                "Auto-detect is disabled. Ensure all folders have existing pawprints."
            )
            
    elif op_type == "compare":
        # For comparison, need at least one previous pawprint
        if self.compare_method.currentText() != "Custom Selection":
            # This would require checking history
            # For now, just inform user
            QMessageBox.information(
                self, "Validation Note",
                "Comparison requires existing pawprint history for selected folders."
            )
            
    elif op_type == "report":
        # Check report output directory
        report_dir = self.report_output_dir.text()
        if report_dir and not os.path.isdir(report_dir):
            reply = QMessageBox.question(
                self, "Report Directory",
                f"Report directory '{report_dir}' does not exist. Create it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    os.makedirs(report_dir, exist_ok=True)
                except Exception as e:
                    QMessageBox.critical(self, "Error",
                                       f"Failed to create report directory: {str(e)}")
                    return False
            else:
                return False
    
    # If we got here, validation passed
    QMessageBox.information(self, "Validation Successful", 
                          f"Configuration valid for {len(folders)} folders.")
    return True
