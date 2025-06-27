#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab (Part 1)
Basic UI structure and folder selection functionality
"""

import os
import sys
import logging
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QGroupBox, QCheckBox,
    QRadioButton, QButtonGroup, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont

logger = logging.getLogger(__name__)

# Function to add to AutomationScreen class
def setup_batch_operations_tab(self):
    """Setup the Batch Operations tab UI components"""
    # Create layout for batch operations tab
    batch_layout = QVBoxLayout(self.batch_operations_tab)
    
    # Add description
    description = QLabel(
        "Perform batch pawprint operations on multiple folders at once. "
        "Select folders to process, configure options, and run the batch operation."
    )
    description.setWordWrap(True)
    description.setStyleSheet("color: #b0b0b0; font-style: italic; margin-bottom: 15px;")
    batch_layout.addWidget(description)
    
    # Create main content area with source selection and options
    content_layout = QHBoxLayout()
    
    # === Left side: Source selection ===
    sources_group = QGroupBox("Folder Sources")
    sources_layout = QVBoxLayout(sources_group)
    
    # Source type selection
    source_type_layout = QHBoxLayout()
    self.source_type_group = QButtonGroup(self)
    
    self.source_history_radio = QRadioButton("From History")
    self.source_history_radio.setChecked(True)
    self.source_history_radio.toggled.connect(self.update_batch_source)
    
    self.source_custom_radio = QRadioButton("Custom Selection")
    self.source_custom_radio.toggled.connect(self.update_batch_source)
    
    self.source_type_group.addButton(self.source_history_radio)
    self.source_type_group.addButton(self.source_custom_radio)
    
    source_type_layout.addWidget(self.source_history_radio)
    source_type_layout.addWidget(self.source_custom_radio)
    sources_layout.addLayout(source_type_layout)
    
    # Source options based on type
    self.history_options = QWidget()
    history_layout = QVBoxLayout(self.history_options)
    
    # Date range for history
    history_filter_layout = QHBoxLayout()
    history_filter_layout.addWidget(QLabel("Date Range:"))
    
    self.history_date_filter = QComboBox()
    self.history_date_filter.addItems(["All Time", "Last 7 Days", "Last 30 Days", "Custom..."])
    self.history_date_filter.currentIndexChanged.connect(self.update_history_folders)
    history_filter_layout.addWidget(self.history_date_filter)
    
    history_layout.addLayout(history_filter_layout)
    
    # Custom folder selection
    self.custom_options = QWidget()
    custom_layout = QVBoxLayout(self.custom_options)
    
    custom_buttons_layout = QHBoxLayout()
    self.add_folder_button = QPushButton("Add Folder")
    self.add_folder_button.clicked.connect(self.add_batch_folder)
    
    self.remove_folder_button = QPushButton("Remove Selected")
    self.remove_folder_button.clicked.connect(self.remove_batch_folder)
    
    self.clear_folders_button = QPushButton("Clear All")
    self.clear_folders_button.clicked.connect(self.clear_batch_folders)
    
    custom_buttons_layout.addWidget(self.add_folder_button)
    custom_buttons_layout.addWidget(self.remove_folder_button)
    custom_buttons_layout.addWidget(self.clear_folders_button)
    custom_layout.addLayout(custom_buttons_layout)
    
    # Folder list (shared between both source types)
    self.folder_list = QListWidget()
    self.folder_list.setAlternatingRowColors(True)
    self.folder_list.setStyleSheet(
        "alternate-background-color: #1a1a1a; background-color: #121212;"
    )
    
    # Add components to sources layout
    sources_layout.addWidget(self.history_options)
    sources_layout.addWidget(self.custom_options)
    sources_layout.addWidget(QLabel("Selected Folders:"))
    sources_layout.addWidget(self.folder_list)
    
    # Stats at bottom of source section
    stats_layout = QHBoxLayout()
    self.folder_count_label = QLabel("0 folders selected")
    stats_layout.addWidget(self.folder_count_label)
    
    sources_layout.addLayout(stats_layout)
    
    # Initial visibility
    self.history_options.setVisible(True)
    self.custom_options.setVisible(False)
    
    # Load initial folders from history
    self.update_history_folders()
    
    # Add sources group to content layout
    content_layout.addWidget(sources_group, 40)
    
    # Add content layout to main layout
    batch_layout.addLayout(content_layout)

# Event handlers and helper methods
def update_batch_source(self):
    """Update the batch source options based on radio button selection"""
    if self.source_history_radio.isChecked():
        self.history_options.setVisible(True)
        self.custom_options.setVisible(False)
        self.update_history_folders()
    else:
        self.history_options.setVisible(False)
        self.custom_options.setVisible(True)
    
    self.update_folder_count()

def update_history_folders(self):
    """Update the folder list from history based on selected filter"""
    try:
        # Clear existing items
        self.folder_list.clear()
        
        # Get history items
        history_items = self.history_manager.get_all_entries()
        
        # Apply date filter
        date_filter = self.history_date_filter.currentText()
        filtered_items = []
        
        # Filtering logic would go here, similar to the history tab
        # For this example, just use all items
        filtered_items = history_items
        
        # Add folder paths to list
        added_paths = set()  # To avoid duplicates
        for item in filtered_items:
            path = item.get('folder_path')
            if path and path not in added_paths and os.path.isdir(path):
                list_item = QListWidgetItem(path)
                list_item.setCheckState(Qt.CheckState.Checked)
                self.folder_list.addItem(list_item)
                added_paths.add(path)
        
        # Update count
        self.update_folder_count()
        
    except Exception as e:
        logger.error(f"Error updating history folders: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to load folders from history: {str(e)}")

def add_batch_folder(self):
    """Add a custom folder to the batch processing list"""
    try:
        # Open folder selection dialog
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder for Batch Processing"
        )
        
        if not folder_path:
            return  # User cancelled
            
        # Check if already in list
        for i in range(self.folder_list.count()):
            if self.folder_list.item(i).text() == folder_path:
                QMessageBox.information(self, "Already Added", 
                                       f"Folder {folder_path} is already in the list")
                return
        
        # Add to list
        item = QListWidgetItem(folder_path)
        item.setCheckState(Qt.CheckState.Checked)
        self.folder_list.addItem(item)
        
        # Update count
        self.update_folder_count()
        
    except Exception as e:
        logger.error(f"Error adding batch folder: {str(e)}")
        QMessageBox.critical(self, "Error", f"Failed to add folder: {str(e)}")

def remove_batch_folder(self):
    """Remove selected folder from the batch processing list"""
    selected_items = self.folder_list.selectedItems()
    
    if not selected_items:
        QMessageBox.information(self, "No Selection", 
                               "Please select a folder to remove")
        return
        
    # Remove all selected items
    for item in selected_items:
        row = self.folder_list.row(item)
        self.folder_list.takeItem(row)
    
    # Update count
    self.update_folder_count()

def clear_batch_folders(self):
    """Clear all folders from the batch processing list"""
    # Confirm with user
    if self.folder_list.count() > 0:
        reply = QMessageBox.question(self, "Confirm Clear", 
                                    "Are you sure you want to clear all folders?",
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.folder_list.clear()
            self.update_folder_count()

def update_folder_count(self):
    """Update the folder count label"""
    total_count = self.folder_list.count()
    checked_count = 0
    
    for i in range(total_count):
        if self.folder_list.item(i).checkState() == Qt.CheckState.Checked:
            checked_count += 1
    
    self.folder_count_label.setText(f"{checked_count} of {total_count} folders selected")

def get_selected_folders(self):
    """Get a list of selected (checked) folders"""
    selected = []
    
    for i in range(self.folder_list.count()):
        item = self.folder_list.item(i)
        if item.checkState() == Qt.CheckState.Checked:
            selected.append(item.text())
    
    return selected
