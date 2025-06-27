#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab (Part 3b)
Progress tracking and real-time status updates
"""

import os
import sys
import logging
import datetime
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QProgressBar, QGroupBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont

logger = logging.getLogger(__name__)

# This part extends the setup_batch_operations_tab function

def setup_batch_operations_tab_part3b(self):
    """
    Setup the progress tracking components for the Batch Operations tab
    This continues the implementation from previous parts
    """
    # Get existing layout
    batch_layout = self.batch_operations_tab.layout()
    
    # Remove the placeholder (added in part 3a)
    placeholder_index = batch_layout.count() - 1
    if placeholder_index >= 0:
        placeholder = batch_layout.itemAt(placeholder_index).widget()
        if placeholder == self.progress_placeholder:
            placeholder.hide()
            batch_layout.removeWidget(placeholder)
    
    # Create progress group
    progress_group = QGroupBox("Operation Progress")
    progress_layout = QVBoxLayout(progress_group)
    
    # Overall progress section
    overall_layout = QHBoxLayout()
    
    # Status label
    self.batch_status_label = QLabel("Ready")
    self.batch_status_label.setStyleSheet("font-weight: bold; color: #9b30ff;")
    overall_layout.addWidget(self.batch_status_label)
    
    # Add spacer to push status to left and progress info to right
    overall_layout.addStretch()
    
    # Progress count
    self.progress_count_label = QLabel("0 / 0 completed")
    overall_layout.addWidget(self.progress_count_label)
    
    # Add overall layout to progress layout
    progress_layout.addLayout(overall_layout)
    
    # Overall progress bar
    self.overall_progress = QProgressBar()
    self.overall_progress.setRange(0, 100)
    self.overall_progress.setValue(0)
    self.overall_progress.setFormat("%p% Complete")
    self.overall_progress.setStyleSheet("""
        QProgressBar {
            border: 1px solid #333333;
            border-radius: 5px;
            text-align: center;
            height: 20px;
            background-color: #1e1e1e;
        }
        QProgressBar::chunk {
            background-color: #9b30ff;
            width: 1px;
        }
    """)
    progress_layout.addWidget(self.overall_progress)
    
    # ETA and timing info
    timing_layout = QHBoxLayout()
    
    self.elapsed_time_label = QLabel("Elapsed: 00:00:00")
    timing_layout.addWidget(self.elapsed_time_label)
    
    timing_layout.addStretch()
    
    self.eta_label = QLabel("ETA: --:--:--")
    timing_layout.addWidget(self.eta_label)
    
    # Add timing layout to progress layout
    progress_layout.addLayout(timing_layout)
    
    # Current task section
    current_task_layout = QHBoxLayout()
    
    current_task_layout.addWidget(QLabel("Current Task:"))
    
    self.current_task_label = QLabel("None")
    self.current_task_label.setStyleSheet("font-style: italic; color: #b0b0b0;")
    current_task_layout.addWidget(self.current_task_label, 1)  # Stretch factor for task name
    
    # Add current task layout to progress layout
    progress_layout.addLayout(current_task_layout)
    
    # Current file progress bar (for file operations)
    self.file_progress = QProgressBar()
    self.file_progress.setRange(0, 100)
    self.file_progress.setValue(0)
    self.file_progress.setFormat("File: %p%")
    self.file_progress.setStyleSheet("""
        QProgressBar {
            border: 1px solid #333333;
            border-radius: 5px;
            text-align: center;
            height: 15px;
            background-color: #1e1e1e;
        }
        QProgressBar::chunk {
            background-color: #7722bb;
            width: 1px;
        }
    """)
    progress_layout.addWidget(self.file_progress)
    
    # Tasks table showing status of each folder task
    self.tasks_table = QTableWidget()
    self.tasks_table.setColumnCount(5)
    self.tasks_table.setHorizontalHeaderLabels([
        "Folder", "Status", "Progress", "Time", "Result"
    ])
    
    # Set table properties
    self.tasks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    self.tasks_table.setAlternatingRowColors(True)
    self.tasks_table.setStyleSheet(
        "alternate-background-color: #1a1a1a; background-color: #121212;"
    )
    
    # Add table to progress layout
    progress_layout.addWidget(self.tasks_table)
    
    # Add progress group to main layout
    batch_layout.addWidget(progress_group)
    
    # Initialize progress tracking state
    self.is_batch_running = False
    self.batch_start_time = None
    self.batch_timer = QTimer(self)
    self.batch_timer.timeout.connect(self.update_batch_time)
    
    # Set initial state
    self.reset_progress_ui()

def reset_progress_ui(self):
    """Reset all progress UI elements to initial state"""
    # Reset status and labels
    self.batch_status_label.setText("Ready")
    self.progress_count_label.setText("0 / 0 completed")
    self.elapsed_time_label.setText("Elapsed: 00:00:00")
    self.eta_label.setText("ETA: --:--:--")
    self.current_task_label.setText("None")
    
    # Reset progress bars
    self.overall_progress.setValue(0)
    self.file_progress.setValue(0)
    
    # Clear tasks table
    self.tasks_table.setRowCount(0)
    
    # Reset state variables
    self.is_batch_running = False
    self.batch_start_time = None
    
    # Stop timer if running
    if self.batch_timer.isActive():
        self.batch_timer.stop()
    
    # Update button states
    self.execute_button.setEnabled(True)
    self.cancel_button.setEnabled(False)

def update_batch_time(self):
    """Update elapsed time and ETA during batch processing"""
    if not self.is_batch_running or not self.batch_start_time:
        return
    
    # Calculate elapsed time
    elapsed = datetime.datetime.now() - self.batch_start_time
    elapsed_str = str(datetime.timedelta(seconds=int(elapsed.total_seconds())))
    self.elapsed_time_label.setText(f"Elapsed: {elapsed_str}")
    
    # Calculate ETA based on progress
    progress = self.overall_progress.value()
    if progress > 0:
        total_seconds = elapsed.total_seconds()
        seconds_per_percent = total_seconds / progress
        remaining_seconds = seconds_per_percent * (100 - progress)
        
        eta = datetime.timedelta(seconds=int(remaining_seconds))
        self.eta_label.setText(f"ETA: {eta}")
    else:
        self.eta_label.setText("ETA: calculating...")

def update_progress(self, overall_percent, file_percent, status_text, current_task):
    """Update progress UI with current status"""
    if not self.is_batch_running:
        return
    
    # Update progress bars
    self.overall_progress.setValue(overall_percent)
    self.file_progress.setValue(file_percent)
    
    # Update status text
    self.batch_status_label.setText(status_text)
    self.current_task_label.setText(current_task)
    
    # Let the UI process events
    QApplication.processEvents()

def add_task_to_table(self, folder_path, status="Queued"):
    """Add a task row to the tasks table"""
    row = self.tasks_table.rowCount()
    self.tasks_table.insertRow(row)
    
    # Folder path
    folder_item = QTableWidgetItem(os.path.basename(folder_path))
    folder_item.setToolTip(folder_path)  # Full path on hover
    self.tasks_table.setItem(row, 0, folder_item)
    
    # Status
    status_item = QTableWidgetItem(status)
    if status == "Queued":
        status_item.setForeground(QColor("#b0b0b0"))  # Gray for queued
    self.tasks_table.setItem(row, 1, status_item)
    
    # Progress (empty initially)
    self.tasks_table.setItem(row, 2, QTableWidgetItem("0%"))
    
    # Time (empty initially)
    self.tasks_table.setItem(row, 3, QTableWidgetItem("--"))
    
    # Result (empty initially)
    self.tasks_table.setItem(row, 4, QTableWidgetItem("--"))
    
    # Return row index for later updates
    return row

def update_task_in_table(self, row, status=None, progress=None, time_str=None, result=None):
    """Update a task row in the tasks table"""
    if row < 0 or row >= self.tasks_table.rowCount():
        return
    
    if status:
        status_item = self.tasks_table.item(row, 1)
        status_item.setText(status)
        
        # Set color based on status
        if status == "Running":
            status_item.setForeground(QColor("#9b30ff"))  # Purple for running
        elif status == "Completed":
            status_item.setForeground(QColor("#00cc00"))  # Green for completed
        elif status == "Failed":
            status_item.setForeground(QColor("#ff5555"))  # Red for failed
    
    if progress is not None:
        progress_item = self.tasks_table.item(row, 2)
        progress_item.setText(f"{progress}%")
    
    if time_str:
        time_item = self.tasks_table.item(row, 3)
        time_item.setText(time_str)
    
    if result:
        result_item = self.tasks_table.item(row, 4)
        result_item.setText(result)
        
        # Set color based on result
        if "changed" in result.lower():
            result_item.setForeground(QColor("#ffaa00"))  # Orange for changes
        elif "unchanged" in result.lower():
            result_item.setForeground(QColor("#00cc00"))  # Green for unchanged
        elif "error" in result.lower():
            result_item.setForeground(QColor("#ff5555"))  # Red for errors
