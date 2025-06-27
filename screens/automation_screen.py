#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automation Screen for Pawprinting PyQt6 V2
Provides GUI integration with the CLI automation system
"""

import os
import sys
import logging
import datetime
from typing import List, Dict, Any, Optional, Tuple

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
    QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QProgressBar, QComboBox, QCheckBox, QSpinBox,
    QFileDialog, QMessageBox, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QDateTime, QTimer
from PyQt6.QtGui import QColor, QIcon, QFont

# Import the automation system
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from automation.task_manager import TaskManager
from automation.task_history import TaskHistoryManager
from automation.task_factory import TaskFactory

logger = logging.getLogger(__name__)

class AutomationScreen(QWidget):
    """
    Main automation screen that provides a GUI interface to the automation system.
    Allows users to view task history, schedule new tasks, and monitor running tasks.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.task_manager = TaskManager()
        self.history_manager = TaskHistoryManager()
        self.task_factory = TaskFactory()
        
        # Set dark mode stylesheet with neon purple accents
        self.setStyleSheet("""
            QWidget { 
                background-color: #121212; 
                color: #e0e0e0; 
            }
            QTableWidget { 
                gridline-color: #333333;
                border: 1px solid #333333;
            }
            QHeaderView::section { 
                background-color: #1e1e1e; 
                color: #9b30ff;
                border: 1px solid #333333;
            }
            QPushButton { 
                background-color: #2d2d2d; 
                color: #e0e0e0;
                border: 1px solid #9b30ff;
                border-radius: 4px;
                padding: 5px 10px;
            }
            QPushButton:hover { 
                background-color: #3d3d3d; 
                border: 1px solid #d186ff;
            }
            QPushButton:pressed { 
                background-color: #9b30ff; 
                color: white;
            }
            QProgressBar {
                border: 1px solid #333333;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #9b30ff;
                width: 1px;
            }
            QTabWidget::pane {
                border: 1px solid #333333;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                border-bottom: 2px solid #9b30ff;
                color: #9b30ff;
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the UI components for the automation screen"""
        # Main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        # Title and description
        self.title_label = QLabel("Automation Control Center")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #9b30ff;")
        self.description_label = QLabel(
            "Manage, monitor, and schedule automated pawprint operations."
        )
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("color: #b0b0b0; font-style: italic;")
        
        # Add to layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.description_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Create the tabs
        self.history_tab = QWidget()
        self.batch_operations_tab = QWidget()
        self.scheduler_tab = QWidget()
        self.monitor_tab = QWidget()
        
        # Add tabs to widget
        self.tab_widget.addTab(self.history_tab, "History")
        self.tab_widget.addTab(self.batch_operations_tab, "Batch Operations")
        self.tab_widget.addTab(self.scheduler_tab, "Scheduler")
        self.tab_widget.addTab(self.monitor_tab, "Monitor")
        
        # Setup individual tab contents
        self.setup_history_tab()
        self.setup_batch_operations_tab()
        self.setup_scheduler_tab()
        self.setup_monitor_tab()
        
        # Add tab widget to main layout
        self.main_layout.addWidget(self.tab_widget)
        
        # Create bottom action buttons
        self.action_buttons_layout = QHBoxLayout()
        
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_all_data)
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.show_settings)
        
        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)
        
        # Add buttons to action layout
        self.action_buttons_layout.addWidget(self.refresh_button)
        self.action_buttons_layout.addWidget(self.settings_button)
        self.action_buttons_layout.addWidget(self.help_button)
        
        # Add action layout to main layout
        self.main_layout.addLayout(self.action_buttons_layout)
