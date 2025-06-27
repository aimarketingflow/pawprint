#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen - Batch Operations Tab
Main module for the Batch Operations tab in AutomationScreen

This module integrates all components from the batch tab parts into 
a cohesive interface for batch pawprint operations.
"""

import os
import sys
import logging
import datetime
import json
import threading
from typing import List, Dict, Any, Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QFileDialog, QMessageBox, QGroupBox, QCheckBox,
    QRadioButton, QButtonGroup, QSpinBox, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QProgressBar, QSizePolicy, QFormLayout, QLineEdit,
    QApplication
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, pyqtSlot, QObject, QSize
from PyQt6.QtGui import QIcon, QFont, QColor

# Import parts
from screens.automation_screen_batch_tab_part1 import (
    setup_batch_operations_tab, 
    update_batch_source, 
    update_history_folders,
    add_batch_folder,
    remove_batch_folder,
    clear_batch_folders,
    update_folder_count,
    get_selected_folders
)

from screens.automation_screen_batch_tab_part2 import (
    setup_batch_operations_tab_part2,
    update_operation_options,
    browse_output_dir,
    browse_report_output_dir
)

from screens.automation_screen_batch_tab_part3a import (
    setup_batch_operations_tab_part3a,
    validate_batch_config
)

from screens.automation_screen_batch_tab_part3b import (
    setup_batch_operations_tab_part3b,
    reset_progress_ui,
    update_batch_time,
    update_progress,
    add_task_to_table,
    update_task_in_table
)

from screens.automation_screen_batch_tab_part3c import (
    BatchTaskWorker,
    execute_batch_operation,
    cancel_batch_operation,
    get_operation_settings,
    get_batch_settings
)

from screens.automation_screen_batch_tab_part3d import (
    on_task_started,
    on_task_progress,
    on_task_completed,
    on_task_error,
    on_batch_progress,
    on_batch_completed,
    prompt_export_results,
    export_results_json,
    export_results_csv,
    export_results_markdown
)

logger = logging.getLogger(__name__)

# Function to initiate the batch tab in AutomationScreen
def initialize_batch_operations_tab(self):
    """
    Initialize all components of the Batch Operations tab
    Should be called from the AutomationScreen __init__ method
    """
    logger.debug("Initializing batch operations tab...")
    
    # Create tab UI structure and folder selection
    setup_batch_operations_tab(self)
    
    # Set up operation settings section
    setup_batch_operations_tab_part2(self)
    
    # Set up execution controls
    setup_batch_operations_tab_part3a(self)
    
    # Set up progress tracking
    setup_batch_operations_tab_part3b(self)
    
    logger.debug("Batch operations tab initialization complete")

# Add all functions to AutomationScreen namespace 
def add_batch_tab_methods_to_class(cls):
    """Add all batch tab methods to the AutomationScreen class"""
    # Basic UI and folder selection methods
    cls.update_batch_source = update_batch_source
    cls.update_history_folders = update_history_folders
    cls.add_batch_folder = add_batch_folder
    cls.remove_batch_folder = remove_batch_folder
    cls.clear_batch_folders = clear_batch_folders
    cls.update_folder_count = update_folder_count
    cls.get_selected_folders = get_selected_folders
    
    # Operation settings methods
    cls.update_operation_options = update_operation_options
    cls.browse_output_dir = browse_output_dir
    cls.browse_report_output_dir = browse_report_output_dir
    
    # Execution control methods
    cls.validate_batch_config = validate_batch_config
    cls.execute_batch_operation = execute_batch_operation
    cls.cancel_batch_operation = cancel_batch_operation
    cls.get_operation_settings = get_operation_settings
    cls.get_batch_settings = get_batch_settings
    
    # Progress tracking methods
    cls.reset_progress_ui = reset_progress_ui
    cls.update_batch_time = update_batch_time
    cls.update_progress = update_progress
    cls.add_task_to_table = add_task_to_table
    cls.update_task_in_table = update_task_in_table
    
    # Event handler methods
    cls.on_task_started = on_task_started
    cls.on_task_progress = on_task_progress
    cls.on_task_completed = on_task_completed
    cls.on_task_error = on_task_error
    cls.on_batch_progress = on_batch_progress
    cls.on_batch_completed = on_batch_completed
    
    # Result export methods
    cls.prompt_export_results = prompt_export_results
    cls.export_results_json = export_results_json
    cls.export_results_csv = export_results_csv
    cls.export_results_markdown = export_results_markdown
