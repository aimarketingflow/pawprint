#!/usr/bin/env python3
"""
Console Widget for Pawprinting PyQt6 Application

Rich text console widget with ANSI color support, timestamp formatting,
and automatic scrolling.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import re
import logging
from datetime import datetime
from typing import Optional, Dict, List, Tuple

from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QRegularExpression
from PyQt6.QtGui import QTextCursor, QColor, QTextCharFormat, QTextDocument, QFont, QTextOption
from PyQt6.QtWidgets import (
    QWidget, QTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, 
    QCheckBox, QLabel, QComboBox, QFileDialog, QApplication
)

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.console_widget")


class ConsoleWidget(QWidget):
    """
    Rich text console widget with ANSI color support
    """
    
    # Signal emitted when log message is added
    log_added = pyqtSignal(str, str)  # level, message
    
    def __init__(self, parent=None):
        """
        Initialize console widget
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        
        # Initialize state
        self.auto_scroll = True
        self.show_timestamps = True
        self.buffer_size = 10000  # Maximum number of lines to keep
        self.log_level = "INFO"
        self.ansi_color_map = self._create_ansi_color_map()
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Console text edit
        self.console = QTextEdit(self)
        self.console.setReadOnly(True)
        self.console.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.console.setWordWrapMode(QTextOption.WrapMode.WrapAtWordBoundaryOrAnywhere)
        
        # Set font (monospace)
        font = QFont("Menlo", 10)
        if not font.exactMatch():
            # Fallback fonts
            font = QFont("Courier New", 10)
            if not font.exactMatch():
                font = QFont("Monospace", 10)
        
        font.setFixedPitch(True)
        self.console.setFont(font)
        
        # Set colors
        self.console.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #F0F0F0;
                border: 1px solid #333333;
            }
        """)
        
        layout.addWidget(self.console)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(10)
        
        # Log level selector
        level_layout = QHBoxLayout()
        level_layout.setContentsMargins(0, 0, 0, 0)
        level_layout.setSpacing(5)
        
        level_label = QLabel("Level:", self)
        level_layout.addWidget(level_label)
        
        self.level_combo = QComboBox(self)
        self.level_combo.addItems(["DEBUG", "INFO", "WARNING", "ERROR"])
        self.level_combo.setCurrentText(self.log_level)
        self.level_combo.currentTextChanged.connect(self.set_log_level)
        level_layout.addWidget(self.level_combo)
        
        controls_layout.addLayout(level_layout)
        
        # Timestamp checkbox
        self.timestamp_check = QCheckBox("Show Timestamps", self)
        self.timestamp_check.setChecked(self.show_timestamps)
        self.timestamp_check.toggled.connect(self.toggle_timestamps)
        controls_layout.addWidget(self.timestamp_check)
        
        # Auto-scroll checkbox
        self.autoscroll_check = QCheckBox("Auto-scroll", self)
        self.autoscroll_check.setChecked(self.auto_scroll)
        self.autoscroll_check.toggled.connect(self.toggle_auto_scroll)
        controls_layout.addWidget(self.autoscroll_check)
        
        controls_layout.addStretch(1)
        
        # Clear button
        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear)
        controls_layout.addWidget(self.clear_button)
        
        # Save button
        self.save_button = QPushButton("Save Log", self)
        self.save_button.clicked.connect(self.save_log)
        controls_layout.addWidget(self.save_button)
        
        layout.addLayout(controls_layout)
    
    def _create_ansi_color_map(self) -> Dict[str, QColor]:
        """
        Create mapping of ANSI color codes to QColors
        
        Returns:
            Dictionary mapping ANSI codes to QColors
        """
        return {
            # Regular colors
            '30': QColor(0, 0, 0),       # Black
            '31': QColor(205, 49, 49),   # Red
            '32': QColor(13, 188, 121),  # Green
            '33': QColor(229, 229, 16),  # Yellow
            '34': QColor(36, 114, 200),  # Blue
            '35': QColor(188, 63, 188),  # Magenta
            '36': QColor(17, 168, 205),  # Cyan
            '37': QColor(229, 229, 229), # White
            
            # Bright colors
            '90': QColor(102, 102, 102), # Bright Black (Gray)
            '91': QColor(241, 76, 76),   # Bright Red
            '92': QColor(35, 209, 139),  # Bright Green
            '93': QColor(245, 245, 67),  # Bright Yellow
            '94': QColor(59, 142, 234),  # Bright Blue
            '95': QColor(214, 112, 214), # Bright Magenta
            '96': QColor(41, 184, 219),  # Bright Cyan
            '97': QColor(255, 255, 255), # Bright White
            
            # Default
            '0': QColor(229, 229, 229),  # Reset/Default (White)
        }
    
    def log(self, message: str, level: str = "INFO"):
        """
        Add a log message to the console
        
        Args:
            message: Log message
            level: Log level (DEBUG, INFO, WARNING, ERROR)
        """
        # Check log level
        if not self._should_log(level):
            return
        
        # Format message with timestamp if enabled
        if self.show_timestamps:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"[{timestamp}] [{level}] {message}"
        else:
            formatted_message = f"[{level}] {message}"
        
        # Process ANSI color codes
        self._append_text_with_ansi(formatted_message, level)
        
        # Emit signal
        self.log_added.emit(level, message)
        
        # Auto-scroll if enabled
        if self.auto_scroll:
            self._scroll_to_bottom()
        
        # Trim buffer if needed
        self._trim_buffer()
    
    def debug(self, message: str):
        """Log a debug message"""
        self.log(message, "DEBUG")
    
    def info(self, message: str):
        """Log an info message"""
        self.log(message, "INFO")
    
    def warning(self, message: str):
        """Log a warning message"""
        self.log(message, "WARNING")
    
    def error(self, message: str):
        """Log an error message"""
        self.log(message, "ERROR")
    
    def clear(self):
        """Clear the console"""
        self.console.clear()
    
    def toggle_auto_scroll(self, enabled: bool):
        """
        Toggle auto-scrolling
        
        Args:
            enabled: Whether auto-scrolling is enabled
        """
        self.auto_scroll = enabled
        if enabled:
            self._scroll_to_bottom()
    
    def toggle_timestamps(self, enabled: bool):
        """
        Toggle timestamp display
        
        Args:
            enabled: Whether timestamps are enabled
        """
        self.show_timestamps = enabled
    
    def set_log_level(self, level: str):
        """
        Set the log level
        
        Args:
            level: Log level (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_level = level
    
    def save_log(self):
        """Save console contents to file"""
        # Get save path
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log File",
            os.path.expanduser("~"),
            "Log Files (*.log);;Text Files (*.txt);;All Files (*)"
        )
        
        if not file_path:
            return
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save text
            with open(file_path, 'w') as f:
                f.write(self.console.toPlainText())
            
            # Log success
            self.info(f"Log saved to {file_path}")
            
        except Exception as e:
            self.error(f"Error saving log file: {e}")
    
    def _should_log(self, level: str) -> bool:
        """
        Check if a message should be logged based on log level
        
        Args:
            level: Log level to check
            
        Returns:
            True if message should be logged, False otherwise
        """
        levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        try:
            current_idx = levels.index(self.log_level)
            msg_idx = levels.index(level)
            return msg_idx >= current_idx
        except ValueError:
            return True
    
    def _scroll_to_bottom(self):
        """Scroll the console to the bottom"""
        cursor = self.console.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.console.setTextCursor(cursor)
    
    def _trim_buffer(self):
        """Trim the buffer to the maximum size"""
        document = self.console.document()
        line_count = document.blockCount()
        
        if line_count > self.buffer_size:
            # Calculate lines to remove
            lines_to_remove = line_count - self.buffer_size
            
            # Get cursor
            cursor = QTextCursor(document)
            cursor.movePosition(QTextCursor.MoveOperation.Start)
            
            # Select lines to remove
            for _ in range(lines_to_remove):
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock)
                cursor.movePosition(QTextCursor.MoveOperation.NextBlock)
            
            # Remove selected text
            cursor.removeSelectedText()
    
    def _append_text_with_ansi(self, text: str, level: str):
        """
        Append text with ANSI color code processing
        
        Args:
            text: Text to append
            level: Log level for default color
        """
        # Define default color for log level
        default_color = self._get_level_color(level)
        
        # ANSI escape code pattern
        ansi_pattern = QRegularExpression(r'\033\[([\d;]+)m')
        
        # Get current format
        cursor = self.console.textCursor()
        
        # Start with level-based format
        current_format = QTextCharFormat()
        current_format.setForeground(default_color)
        
        # Split text by ANSI codes
        remaining_text = text
        while remaining_text:
            # Find next ANSI code
            match = ansi_pattern.match(remaining_text)
            
            if not match.hasMatch():
                # No more ANSI codes, append remaining text with current format
                cursor.insertText(remaining_text, current_format)
                break
            
            # Append text before ANSI code
            prefix = remaining_text[:match.capturedStart()]
            if prefix:
                cursor.insertText(prefix, current_format)
            
            # Process ANSI code
            codes = match.captured(1).split(';')
            for code in codes:
                if code in self.ansi_color_map:
                    current_format.setForeground(self.ansi_color_map[code])
                elif code == '1':  # Bold
                    font = current_format.font()
                    font.setBold(True)
                    current_format.setFont(font)
                elif code == '0':  # Reset
                    current_format = QTextCharFormat()
                    current_format.setForeground(default_color)
            
            # Move to remaining text after ANSI code
            remaining_text = remaining_text[match.capturedEnd():]
        
        # Add newline
        cursor.insertText('\n')
        self.console.setTextCursor(cursor)
    
    def _get_level_color(self, level: str) -> QColor:
        """
        Get color for log level
        
        Args:
            level: Log level
            
        Returns:
            QColor for the log level
        """
        return {
            "DEBUG": QColor(150, 150, 150),   # Gray
            "INFO": QColor(220, 220, 220),    # Light Gray
            "WARNING": QColor(240, 180, 0),   # Orange
            "ERROR": QColor(240, 0, 0)        # Red
        }.get(level, QColor(220, 220, 220))
