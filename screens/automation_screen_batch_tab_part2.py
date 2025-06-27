#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab (Part 2)
Operation settings and options UI components
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QGroupBox, QCheckBox,
    QSpinBox, QComboBox, QLineEdit, QFormLayout,
    QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

logger = logging.getLogger(__name__)

# This part extends the setup_batch_operations_tab function from part 1

def setup_batch_operations_tab_part2(self):
    """
    Setup the right side of the Batch Operations tab with operation settings
    This continues the implementation from part 1
    """
    # Get existing layout
    batch_layout = self.batch_operations_tab.layout()
    
    # Get the content_layout that was created in part 1
    content_layout = batch_layout.itemAt(1).layout()
    
    # === Right side: Operation settings ===
    settings_group = QGroupBox("Operation Settings")
    settings_layout = QVBoxLayout(settings_group)
    
    # Operation type selection
    operation_type_layout = QVBoxLayout()
    operation_type_layout.addWidget(QLabel("Operation Type:"))
    
    self.operation_type = QComboBox()
    self.operation_type.addItems([
        "Generate New Pawprints", 
        "Refresh Existing Pawprints",
        "Compare with Previous",
        "Generate & Export Report"
    ])
    self.operation_type.currentIndexChanged.connect(self.update_operation_options)
    operation_type_layout.addWidget(self.operation_type)
    settings_layout.addLayout(operation_type_layout)
    
    # Options section - will change based on operation type
    self.option_widgets = {}  # Store widgets for different operation types
    
    # Create a container for each operation type's options
    for op_type in ["generate", "refresh", "compare", "report"]:
        container = QWidget()
        container.setVisible(False)  # Hidden initially
        self.option_widgets[op_type] = container
        
        if op_type == "generate":
            # Options for generating new pawprints
            layout = QFormLayout(container)
            
            # Recursion depth option
            self.depth_spinner = QSpinBox()
            self.depth_spinner.setRange(1, 100)
            self.depth_spinner.setValue(5)  # Default value
            self.depth_spinner.setToolTip("Maximum directory recursion depth")
            layout.addRow("Recursion Depth:", self.depth_spinner)
            
            # Include hidden files
            self.include_hidden = QCheckBox("Include hidden files and directories")
            self.include_hidden.setChecked(False)
            layout.addRow("", self.include_hidden)
            
            # Output directory option
            output_layout = QHBoxLayout()
            self.output_dir = QLineEdit()
            self.output_dir.setPlaceholderText("Default output directory")
            self.output_dir.setToolTip("Leave empty to use source folder locations")
            
            self.browse_output = QPushButton("Browse...")
            self.browse_output.clicked.connect(self.browse_output_dir)
            
            output_layout.addWidget(self.output_dir)
            output_layout.addWidget(self.browse_output)
            layout.addRow("Output Directory:", output_layout)
            
        elif op_type == "refresh":
            # Options for refreshing existing pawprints
            layout = QFormLayout(container)
            
            # Auto-detect existing pawprints
            self.auto_detect = QCheckBox("Auto-detect existing pawprints")
            self.auto_detect.setChecked(True)
            layout.addRow("", self.auto_detect)
            
            # Update timestamp
            self.update_timestamp = QCheckBox("Update timestamp on unchanged files")
            self.update_timestamp.setChecked(False)
            layout.addRow("", self.update_timestamp)
            
            # Force refresh
            self.force_refresh = QCheckBox("Force refresh (ignore modification dates)")
            self.force_refresh.setChecked(False)
            layout.addRow("", self.force_refresh)
            
        elif op_type == "compare":
            # Options for comparison operations
            layout = QFormLayout(container)
            
            # Comparison method
            self.compare_method = QComboBox()
            self.compare_method.addItems([
                "Latest with Previous", 
                "Latest with Baseline",
                "Custom Selection"
            ])
            layout.addRow("Compare Method:", self.compare_method)
            
            # Detail level
            self.compare_detail = QComboBox()
            self.compare_detail.addItems([
                "Summary Only", 
                "Changed Files Only",
                "Full Comparison"
            ])
            layout.addRow("Detail Level:", self.compare_detail)
            
            # Visualization options
            self.visualization = QComboBox()
            self.visualization.addItems([
                "Simple", 
                "Side by Side",
                "JSON Tree", 
                "Charts"
            ])
            layout.addRow("Visualization:", self.visualization)
            
        elif op_type == "report":
            # Options for report generation
            layout = QFormLayout(container)
            
            # Report format
            self.report_format = QComboBox()
            self.report_format.addItems([
                "Markdown", 
                "HTML",
                "PDF", 
                "CSV"
            ])
            layout.addRow("Report Format:", self.report_format)
            
            # Report content options
            self.include_summary = QCheckBox("Include summary statistics")
            self.include_summary.setChecked(True)
            layout.addRow("", self.include_summary)
            
            self.include_changes = QCheckBox("Include detailed changes")
            self.include_changes.setChecked(True)
            layout.addRow("", self.include_changes)
            
            self.include_charts = QCheckBox("Include visual charts")
            self.include_charts.setChecked(True)
            layout.addRow("", self.include_charts)
            
            # Output directory for reports
            report_output_layout = QHBoxLayout()
            self.report_output_dir = QLineEdit()
            self.report_output_dir.setPlaceholderText("Default reports directory")
            
            self.browse_report_output = QPushButton("Browse...")
            self.browse_report_output.clicked.connect(self.browse_report_output_dir)
            
            report_output_layout.addWidget(self.report_output_dir)
            report_output_layout.addWidget(self.browse_report_output)
            layout.addRow("Output Directory:", report_output_layout)
        
        # Add the container to settings layout
        settings_layout.addWidget(container)
    
    # Show default operation type options
    self.update_operation_options()
    
    # Processing options (common to all operations)
    process_group = QGroupBox("Processing Options")
    process_layout = QFormLayout(process_group)
    
    # Parallel processing
    self.parallel_processing = QCheckBox("Enable parallel processing")
    self.parallel_processing.setChecked(True)
    process_layout.addRow("", self.parallel_processing)
    
    # Thread count
    self.thread_count = QSpinBox()
    self.thread_count.setRange(1, 16)
    self.thread_count.setValue(4)  # Default value
    process_layout.addRow("Max Threads:", self.thread_count)
    
    # Priority
    self.process_priority = QComboBox()
    self.process_priority.addItems(["Low", "Normal", "High"])
    self.process_priority.setCurrentIndex(1)  # Normal by default
    process_layout.addRow("Process Priority:", self.process_priority)
    
    # Add process group to settings layout
    settings_layout.addWidget(process_group)
    
    # Add settings group to content layout
    content_layout.addWidget(settings_group, 60)

def update_operation_options(self):
    """Update visible options based on selected operation type"""
    op_index = self.operation_type.currentIndex()
    
    # Map index to operation type
    op_types = ["generate", "refresh", "compare", "report"]
    selected_type = op_types[op_index] if op_index < len(op_types) else "generate"
    
    # Update visibility
    for op_type, widget in self.option_widgets.items():
        widget.setVisible(op_type == selected_type)

def browse_output_dir(self):
    """Open file dialog to select output directory for pawprints"""
    dir_path = QFileDialog.getExistingDirectory(
        self, "Select Output Directory for Pawprints"
    )
    
    if dir_path:
        self.output_dir.setText(dir_path)

def browse_report_output_dir(self):
    """Open file dialog to select output directory for reports"""
    dir_path = QFileDialog.getExistingDirectory(
        self, "Select Output Directory for Reports"
    )
    
    if dir_path:
        self.report_output_dir.setText(dir_path)
