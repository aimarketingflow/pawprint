#!/usr/bin/env python3
"""
Dashboard Screen for Pawprinting PyQt6 Application

Main dashboard screen with navigation options and recent activity display.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import json
import logging
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QTimer, QUrl
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QAction
from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, 
    QGridLayout, QScrollArea, QFrame, QListWidget, QListWidgetItem,
    QSizePolicy, QSpacerItem, QSplitter, QGroupBox, QCheckBox, QApplication,
    QAbstractItemView
)

# Import utility modules
from config_paths import LOGO_PATH
from utils.notification_manager import NotificationManager
from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.dashboard")


class ActivityItem(QFrame):
    """
    Widget representing a single activity item in the recent activity list
    """
    def __init__(self, title: str, timestamp: str, icon_type: str = "info", parent=None):
        """
        Initialize activity item widget
        
        Args:
            title: Activity title
            timestamp: Activity timestamp (string)
            icon_type: Icon type ("info", "success", "warning", "error")
            parent: Parent widget
        """
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setMinimumHeight(50)
        
        # Get theme manager
        self.theme_manager = ThemeManager.get_instance()
        
        # Create layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Get color from theme manager if available
        if self.theme_manager:
            icon_color = {
                "info": self.theme_manager.get_color_hex("info"),
                "success": self.theme_manager.get_color_hex("success"),
                "warning": self.theme_manager.get_color_hex("warning"),
                "error": self.theme_manager.get_color_hex("error")
            }.get(icon_type, self.theme_manager.get_color_hex("info"))
        else:
            # Fallback colors if theme manager not available
            icon_color = {
                "info": "#2196F3",      # Blue
                "success": "#4CAF50",   # Green
                "warning": "#FF9800",   # Orange
                "error": "#F44336"      # Red
            }.get(icon_type, "#2196F3")
        
        # Add icon indicator (just a colored square for now)
        icon = QFrame(self)
        icon.setFixedSize(16, 16)
        icon.setStyleSheet(f"background-color: {icon_color};")
        layout.addWidget(icon)
        
        # Add text content
        text_layout = QVBoxLayout()
        
        title_label = QLabel(title, self)
        title_label.setStyleSheet("font-weight: bold;")
        text_layout.addWidget(title_label)
        
        time_label = QLabel(timestamp, self)
        if self.theme_manager:
            text_color = self.theme_manager.get_color_hex("textSecondary")
            time_label.setStyleSheet(f"color: {text_color}; font-size: 10px;")
        else:
            time_label.setStyleSheet("color: #888888; font-size: 10px;")
        text_layout.addWidget(time_label)
        
        layout.addLayout(text_layout)
        layout.addStretch(1)


class DashboardScreen(QWidget):
    """
    Main dashboard screen for the Pawprinting PyQt6 application
    """
    def __init__(self, parent=None):
        """Initialize dashboard screen"""
        super().__init__(parent)
        self.main_window = parent
        self.state_manager = StateManager.get_instance()
        self.theme_manager = ThemeManager.get_instance()
        
        # Recent activities (to be loaded from state)
        self.recent_activities = []
        
        # Track pawprints generated in current session with timestamps
        self.current_session_pawprints = []  # List of (file_path, timestamp) tuples
        
        # Selected files for comparison
        self.selected_files_for_comparison = []
        
        # File metadata cache (path -> metadata dict)
        self.file_metadata_cache = {}
        
        # Set up UI
        self.setup_ui()
        
        # Load recent activities and files
        self.load_recent_activities()
        self.load_recent_files()
        self.update_current_session_list()
        self.update_comparison_section()
        
        # Connect theme manager signals
        if self.theme_manager:
            self.theme_manager.theme_changed.connect(self.on_theme_changed)
        
        logger.info("Dashboard screen initialized")
    
    def setup_ui(self):
        """Set up the dashboard UI components"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Add test files button (for development/testing only)
        test_files_btn = QPushButton("Load Test Files")
        test_files_btn.setToolTip("Load test pawprint files for demonstration")
        test_files_btn.clicked.connect(self.load_test_files)
        main_layout.addWidget(test_files_btn)
        
        # Application logo (use PawPrintLogo.jpg from resources)
        if os.path.exists(LOGO_PATH):
            logo_layout = QHBoxLayout()
            logo_label = QLabel(self)
            logo_pixmap = QPixmap(LOGO_PATH)
            # Scale the logo to a good size for the dashboard
            logo_label.setPixmap(logo_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            logo_layout.addWidget(logo_label)
            logo_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addLayout(logo_layout)
            
            # Add a subtitle with branding
            subtitle_label = QLabel("AIMF LLC Digital Forensics Tool", self)
            subtitle_label.setStyleSheet("font-size: 14px; font-style: italic; color: #666;")
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            main_layout.addWidget(subtitle_label)
        
        # Title
        title_label = QLabel("Pawprinting Dashboard", self)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Quick actions section
        actions_label = QLabel("Quick Actions", self)
        actions_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(actions_label)
        
        # Main actions grid
        actions_grid = QGridLayout()
        actions_grid.setSpacing(15)
        
        # Generate button
        self.generate_btn = self.create_action_button(
            "Generate Pawprint", 
            "Create a new pawprint from a folder",
            icon_name="generate"
        )
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        actions_grid.addWidget(self.generate_btn, 0, 0)
        
        # Analyze button
        self.analyze_btn = self.create_action_button(
            "Analyze Files", 
            "Analyze existing files or folders",
            icon_name="analyze"
        )
        self.analyze_btn.clicked.connect(self.on_analyze_clicked)
        actions_grid.addWidget(self.analyze_btn, 0, 1)
        
        # Settings button
        self.settings_btn = self.create_action_button(
            "Settings", 
            "Configure application settings",
            icon_name="settings"
        )
        self.settings_btn.clicked.connect(self.on_settings_clicked)
        actions_grid.addWidget(self.settings_btn, 1, 0)
        
        # Fractal button
        self.fractal_btn = self.create_action_button(
            "Fractal Butterfly", 
            "Advanced fractal pattern analysis",
            icon_name="fractal"
        )
        self.fractal_btn.clicked.connect(self.on_fractal_clicked)
        actions_grid.addWidget(self.fractal_btn, 1, 1)
        
        main_layout.addLayout(actions_grid)
        
        # Three-column section for current session, recent files, and activity
        columns_layout = QHBoxLayout()
        
        # Current Session section
        current_session_layout = QVBoxLayout()
        current_session_label = QLabel("Current Session", self)
        current_session_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")
        current_session_layout.addWidget(current_session_label)
        
        # Current session list with multi-selection
        self.current_session_list = QListWidget(self)
        self.current_session_list.setMinimumHeight(200)
        self.current_session_list.setMaximumWidth(220)
        self.current_session_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.current_session_list.itemClicked.connect(self.on_current_session_item_clicked)
        self.current_session_list.itemSelectionChanged.connect(self.on_selection_changed)
        current_session_layout.addWidget(self.current_session_list)
        
        columns_layout.addLayout(current_session_layout)
        
        # Recent files section
        recent_files_layout = QVBoxLayout()
        recent_files_label = QLabel("Recent Files", self)
        recent_files_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        recent_files_layout.addWidget(recent_files_label)
        
        # Recent files list with multi-selection
        self.recent_files_list = QListWidget(self)
        self.recent_files_list.setMinimumHeight(200)
        self.recent_files_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.recent_files_list.itemClicked.connect(self.on_recent_file_clicked)
        self.recent_files_list.itemSelectionChanged.connect(self.on_selection_changed)
        recent_files_layout.addWidget(self.recent_files_list)
        
        columns_layout.addLayout(recent_files_layout)
        
        # Recent activity section
        recent_activity_layout = QVBoxLayout()
        recent_activity_label = QLabel("Recent Activity", self)
        recent_activity_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        recent_activity_layout.addWidget(recent_activity_label)
        
        # Activity scroll area
        activity_scroll = QScrollArea(self)
        activity_scroll.setWidgetResizable(True)
        activity_scroll.setMinimumHeight(200)
        
        # Activity container
        self.activity_container = QWidget()
        self.activity_layout = QVBoxLayout(self.activity_container)
        self.activity_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.activity_layout.setSpacing(10)
        
        activity_scroll.setWidget(self.activity_container)
        recent_activity_layout.addWidget(activity_scroll)
        
        columns_layout.addLayout(recent_activity_layout)
        
        main_layout.addLayout(columns_layout)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setLineWidth(1)
        main_layout.addWidget(separator)
        
        # File comparison section
        comparison_group = QGroupBox("File Comparison")
        comparison_group.setStyleSheet("QGroupBox { font-weight: bold; padding-top: 15px; margin-top: 10px; }")
        comparison_layout = QVBoxLayout(comparison_group)
        
        # Instructions
        instructions = QLabel("Select files from lists above for comparison. Files with similar names will be automatically grouped.")
        comparison_layout.addWidget(instructions)
        
        # Files for comparison
        self.selected_files_label = QLabel("No files selected for comparison")
        self.selected_files_label.setStyleSheet("color: #FF9800; margin-top: 5px;")
        comparison_layout.addWidget(self.selected_files_label)
        
        # Similar files section
        similar_files_label = QLabel("Related Files:")
        similar_files_label.setStyleSheet("font-weight: bold; margin-top: 5px;")
        comparison_layout.addWidget(similar_files_label)
        
        self.similar_files_list = QListWidget()
        self.similar_files_list.setMaximumHeight(100)
        self.similar_files_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        comparison_layout.addWidget(self.similar_files_list)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.compare_btn = QPushButton("Compare Selected Files")
        self.compare_btn.setEnabled(False)
        self.compare_btn.clicked.connect(self.on_compare_clicked)
        button_layout.addWidget(self.compare_btn)
        
        self.clear_selection_btn = QPushButton("Clear Selection")
        self.clear_selection_btn.clicked.connect(self.clear_selection)
        button_layout.addWidget(self.clear_selection_btn)
        
        comparison_layout.addLayout(button_layout)
        
        main_layout.addWidget(comparison_group)
    
    def create_action_button(self, title: str, description: str, icon_name: str = None) -> QPushButton:
        """
        Create a styled action button
        
        Args:
            title: Button title
            description: Button description
            icon_name: Icon name (optional)
            
        Returns:
            Styled QPushButton
        """
        button = QPushButton(title, self)
        button.setMinimumHeight(80)
        button.setMinimumWidth(200)
        
        # Set icon if available
        if icon_name:
            # We would load an icon here if available
            pass
        
        # Set tooltip
        button.setToolTip(description)
        
        return button
    
    def load_recent_files(self):
        """Load recent files from state manager with timestamps"""
        self.recent_files_list.clear()
        
        # Get recent files from state
        recent_files = self.state_manager.get_value("recent_files", [])
        
        if recent_files:
            for file_path in recent_files:
                if os.path.exists(file_path):
                    # Get file modified time as timestamp
                    timestamp = datetime.fromtimestamp(os.path.getmtime(file_path))
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M")
                    
                    # Create list item with filename and timestamp
                    filename = os.path.basename(file_path)
                    display_text = f"{filename} [{time_str}]"
                    item = QListWidgetItem(display_text)
                    item.setToolTip(file_path)
                    item.setData(Qt.ItemDataRole.UserRole, file_path)
                    item.setData(Qt.ItemDataRole.UserRole + 1, timestamp)  # Store timestamp
                    
                    # Cache file metadata
                    self.file_metadata_cache[file_path] = {
                        'timestamp': timestamp,
                        'name': filename,
                        'path': file_path
                    }
                    
                    self.recent_files_list.addItem(item)
        else:
            # Add placeholder item
            item = QListWidgetItem("No recent files")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
            self.recent_files_list.addItem(item)
    
    def load_recent_activities(self):
        """Load recent activities"""
        # Clear existing activities
        for i in reversed(range(self.activity_layout.count())):
            widget = self.activity_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # For now, just add some sample activities
        # In a real app, these would come from the state manager
        sample_activities = [
            {"title": "Pawprint generated", "time": "Today, 2:30 PM", "type": "success"},
            {"title": "Fractal analysis completed", "time": "Yesterday, 11:45 AM", "type": "info"},
            {"title": "Settings updated", "time": "2 days ago", "type": "info"},
            {"title": "Failed to analyze corrupted file", "time": "3 days ago", "type": "error"}
        ]
        
        for activity in sample_activities:
            activity_item = ActivityItem(
                activity["title"],
                activity["time"],
                activity["type"]
            )
            self.activity_layout.addWidget(activity_item)
        
        # Add stretch to push items to the top
        self.activity_layout.addStretch(1)
    
    def on_recent_file_clicked(self, item):
        """Handle click on recent file item"""
        # Check if we're in selection mode (for comparison)
        if self.recent_files_list.selectionMode() == QAbstractItemView.SelectionMode.ExtendedSelection:
            # If shift/ctrl not held, this will still open the file when clicked
            modifiers = QApplication.keyboardModifiers()
            if not (modifiers & Qt.KeyboardModifier.ShiftModifier or 
                    modifiers & Qt.KeyboardModifier.ControlModifier):
                file_path = item.data(Qt.ItemDataRole.UserRole)
                if file_path and os.path.exists(file_path):
                    # Open the file (via main window)
                    logger.info(f"Opening recent file: {file_path}")
                    
                    # Use the on_open method from main window to handle the file
                    if hasattr(self.main_window, "on_open") and callable(self.main_window.on_open):
                        self.main_window.on_open(file_path)
                    else:
                        logger.error("Main window does not have on_open method")
                        NotificationManager.show_error("Cannot open file: Application error")
                        NotificationManager.show_dialog(
                            "Open File", 
                            f"Unable to open {os.path.basename(file_path)} due to application error.",
                            "error"
                        )
    
    def on_generate_clicked(self):
        """Handle click on generate button"""
        logger.info("Generate button clicked")
        if hasattr(self.main_window, "show_generate_screen") and callable(self.main_window.show_generate_screen):
            self.main_window.show_generate_screen()
    
    def on_analyze_clicked(self):
        """Handle click on analyze button"""
        logger.info("Analyze button clicked")
        if hasattr(self.main_window, "show_analyze_screen") and callable(self.main_window.show_analyze_screen):
            self.main_window.show_analyze_screen()
    
    def on_settings_clicked(self):
        """Handle click on settings button"""
        logger.info("Settings button clicked")
        if hasattr(self.main_window, "show_settings_screen") and callable(self.main_window.show_settings_screen):
            self.main_window.show_settings_screen()
    
    def on_fractal_clicked(self):
        """Handle click on fractal button"""
        logger.info("Fractal button clicked")
        if hasattr(self.main_window, "show_fractal_screen") and callable(self.main_window.show_fractal_screen):
            self.main_window.show_fractal_screen()
    
    def on_theme_changed(self, theme_name):
        """Handle theme change event"""
        logger.debug(f"Theme changed to {theme_name}, updating dashboard UI")
        # No specific updates needed yet, theme manager applies styles globally
    
    def update_current_session_list(self):
        """Update the current session pawprints list with timestamps"""
        self.current_session_list.clear()
        
        if self.current_session_pawprints:
            for file_path, timestamp in self.current_session_pawprints:
                if os.path.exists(file_path):
                    # Format timestamp for display
                    time_str = timestamp.strftime("%H:%M:%S")
                    
                    # Create list item with filename and timestamp
                    filename = os.path.basename(file_path)
                    display_text = f"{filename} [{time_str}]"
                    item = QListWidgetItem(display_text)
                    item.setToolTip(file_path)
                    item.setData(Qt.ItemDataRole.UserRole, file_path)
                    item.setData(Qt.ItemDataRole.UserRole + 1, timestamp)  # Store timestamp
                    
                    # Highlight current session items with a different style
                    item.setForeground(QColor("#2196F3"))  # Use primary blue color
                    self.current_session_list.addItem(item)
                    
                    # Cache file metadata
                    if file_path not in self.file_metadata_cache:
                        self.file_metadata_cache[file_path] = {
                            'timestamp': timestamp,
                            'name': filename,
                            'path': file_path
                        }
        else:
            # Add placeholder item
            item = QListWidgetItem("No files in session")
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEnabled)
            self.current_session_list.addItem(item)
    
    def add_to_current_session(self, file_path):
        """Add a file to the current session list with timestamp"""
        if file_path and os.path.exists(file_path):
            # Check if file is already in session
            for i, (existing_path, _) in enumerate(self.current_session_pawprints):
                if existing_path == file_path:
                    # Move it to the front (most recent)
                    item = self.current_session_pawprints.pop(i)
                    self.current_session_pawprints.insert(0, item)
                    self.update_current_session_list()
                    return True
            
            # Add to the beginning of the list with current timestamp
            timestamp = datetime.now()
            self.current_session_pawprints.insert(0, (file_path, timestamp))
            
            # Limit the list to 10 items
            if len(self.current_session_pawprints) > 10:
                self.current_session_pawprints.pop()
            
            # Update the UI
            self.update_current_session_list()
            self.find_related_files(file_path)  # Find similar files
            logger.info(f"Added to current session: {file_path}")
            return True
        return False
        
    def on_selection_changed(self):
        """Handle selection changes in either list"""
        # Clear existing selection
        self.selected_files_for_comparison = []
        
        # Get selected items from current session list
        for item in self.current_session_list.selectedItems():
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path and file_path not in self.selected_files_for_comparison:
                self.selected_files_for_comparison.append(file_path)
        
        # Get selected items from recent files list
        for item in self.recent_files_list.selectedItems():
            file_path = item.data(Qt.ItemDataRole.UserRole)
            if file_path and file_path not in self.selected_files_for_comparison:
                self.selected_files_for_comparison.append(file_path)
        
        # Update UI based on selection
        self.update_comparison_section()
        
    def clear_selection(self):
        """Clear all selections"""
        self.current_session_list.clearSelection()
        self.recent_files_list.clearSelection()
        self.selected_files_for_comparison = []
        self.similar_files_list.clear()
        self.update_comparison_section()
        
    def load_test_files(self):
        """Load test pawprint files for demonstration purposes"""
        test_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "test_files")
        
        if not os.path.exists(test_dir):
            NotificationManager.show_warning(f"Test directory not found: {test_dir}")
            return
            
        # Find all JSON files in the test directory
        test_files = []
        for file in os.listdir(test_dir):
            if file.endswith(".json"):
                test_files.append(os.path.join(test_dir, file))
                
        if not test_files:
            NotificationManager.show_warning("No test files found in the test directory")
            return
            
        # Add files to current session
        files_added = 0
        for file_path in test_files:
            if self.add_to_current_session(file_path):
                files_added += 1
                
        # Log and notify
        logger.info(f"Added {files_added} test files to current session from {test_dir}")
        NotificationManager.show_success(
            f"Added {files_added} test files to current session. \n" + 
            "You can now select them for comparison."
        )
    
    def update_comparison_section(self):
        """Update the comparison section based on selected files"""
        # Update selected files label
        num_selected = len(self.selected_files_for_comparison)
        if num_selected == 0:
            self.selected_files_label.setText("No files selected for comparison")
            self.compare_btn.setEnabled(False)
        else:
            file_names = [os.path.basename(path) for path in self.selected_files_for_comparison]
            self.selected_files_label.setText(f"Selected {num_selected} files for comparison: {', '.join(file_names[:3])}{'...' if num_selected > 3 else ''}")
            self.compare_btn.setEnabled(num_selected >= 2)
            
            # Find related files for the selected files
            self.find_related_files_for_selection()
    
    def find_related_files_for_selection(self):
        """Find files related to the current selection"""
        if not self.selected_files_for_comparison:
            self.similar_files_list.clear()
            return
        
        # Get the first selected file to find related files
        source_file = self.selected_files_for_comparison[0]
        self.find_related_files(source_file)
    
    def find_related_files(self, file_path):
        """Find files related to a given file path based on naming patterns"""
        if not file_path or not os.path.exists(file_path):
            return
            
        # Clear current list
        self.similar_files_list.clear()
        
        # Get base name for pattern matching
        filename = os.path.basename(file_path)
        name_parts = os.path.splitext(filename)[0]
        
        # Find common base name pattern (remove digits and special chars from end)
        base_pattern = re.sub(r'[_-]?\d+$', '', name_parts)  # Remove trailing numbers
        
        # If we have test_pawprint_1, we want to match test_pawprint_*
        related_paths = []
        
        # Search in current session files
        for session_path, _ in self.current_session_pawprints:
            if session_path != file_path and os.path.exists(session_path):
                session_filename = os.path.basename(session_path)
                if base_pattern and base_pattern in session_filename:
                    related_paths.append(session_path)
        
        # Search in recent files
        for i in range(self.recent_files_list.count()):
            item = self.recent_files_list.item(i)
            if item and not (item.flags() & ~Qt.ItemFlag.ItemIsEnabled):
                recent_path = item.data(Qt.ItemDataRole.UserRole)
                if recent_path and recent_path != file_path and os.path.exists(recent_path):
                    recent_filename = os.path.basename(recent_path)
                    if base_pattern and base_pattern in recent_filename:
                        if recent_path not in related_paths:
                            related_paths.append(recent_path)
        
        # Add found related files to the similar files list
        for related_path in related_paths:
            related_filename = os.path.basename(related_path)
            timestamp = None
            
            # Get timestamp from cache if available
            if related_path in self.file_metadata_cache:
                timestamp = self.file_metadata_cache[related_path]['timestamp']
            else:
                # Get from file system
                timestamp = datetime.fromtimestamp(os.path.getmtime(related_path))
            
            time_str = timestamp.strftime("%Y-%m-%d %H:%M") if timestamp else ""
            display_text = f"{related_filename} [{time_str}]"
            
            item = QListWidgetItem(display_text)
            item.setToolTip(related_path)
            item.setData(Qt.ItemDataRole.UserRole, related_path)
            self.similar_files_list.addItem(item)
    
    def on_compare_clicked(self):
        """Handle compare button click"""
        if len(self.selected_files_for_comparison) < 2:
            NotificationManager.show_warning("Please select at least two files to compare")
            return
            
        # For now, log the intent and show notification
        file_names = [os.path.basename(path) for path in self.selected_files_for_comparison]
        logger.info(f"Comparing files: {', '.join(file_names)}")
        
        # Check if files are from the same folder (auto-identify runs in same folder)
        folders = set([os.path.dirname(path) for path in self.selected_files_for_comparison])
        same_folder = len(folders) == 1
        
        # Launch comparison in analyze screen
        if hasattr(self.main_window, "show_analyze_screen") and callable(self.main_window.show_analyze_screen):
            self.main_window.show_analyze_screen()
            # If analyze screen has compare method, call it
            if hasattr(self.main_window.analyze_screen, "compare_files"):
                self.main_window.analyze_screen.compare_files(self.selected_files_for_comparison)
                NotificationManager.show_success(f"Comparing {len(self.selected_files_for_comparison)} files from {'same folder' if same_folder else 'different folders'}")
            else:
                NotificationManager.show_dialog(
                    "Not Implemented", 
                    f"File comparison feature is being developed. Selected {len(self.selected_files_for_comparison)} files.",
                    "info"
                )
        
    def on_current_session_item_clicked(self, item):
        """Handle click on current session item"""
        # Check if we're in selection mode (for comparison)
        if self.current_session_list.selectionMode() == QAbstractItemView.SelectionMode.ExtendedSelection:
            # If shift/ctrl not held, this will still open the file when clicked
            modifiers = QApplication.keyboardModifiers()
            if not (modifiers & Qt.KeyboardModifier.ShiftModifier or 
                    modifiers & Qt.KeyboardModifier.ControlModifier):
                file_path = item.data(Qt.ItemDataRole.UserRole)
                if file_path and os.path.exists(file_path):
                    # Open the file (via main window)
                    logger.info(f"Opening current session file: {file_path}")
                    
                    # Use the on_open method from main window to handle the file
                    if hasattr(self.main_window, "on_open") and callable(self.main_window.on_open):
                        self.main_window.on_open(file_path)
                    else:
                        logger.error("Main window does not have on_open method")
                        NotificationManager.show_error("Cannot open file: Application error")
