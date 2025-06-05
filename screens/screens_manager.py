#!/usr/bin/env python3
"""
Screen Manager for Pawprinting PyQt6 Application

Manages and integrates all screens in the application.
Handles navigation between screens and maintains state.

Author: AIMF LLC
Date: June 3, 2025
"""

import logging
import os
from typing import Dict, Optional, Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QStackedWidget, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QPushButton, QLabel, QFrame, QSplitter
)

# Import screens
from .history_screen import HistoryScreen
from utilities.notification import NotificationManager

# Set up logging
logger = logging.getLogger(__name__)

class ScreensManager(QMainWindow):
    """
    Main screen manager for the Pawprinting application.
    
    Handles navigation and integration between different screens.
    """
    
    # Define screen indices
    SCREEN_FRACTAL = 0
    SCREEN_HISTORY = 1
    
    # Signals
    loadPawprint = pyqtSignal(dict)
    
    def __init__(self, text_input_widget, fractal_display_widget, parent=None):
        super().__init__(parent)
        
        self.text_input_widget = text_input_widget
        self.fractal_display_widget = fractal_display_widget
        
        # Store the current screen
        self.current_screen = self.SCREEN_FRACTAL
        
        # Set up the UI
        self.setup_ui()
        
        # Set parent for notifications
        NotificationManager.set_parent(self)
    
    def setup_ui(self):
        """Set up the user interface components"""
        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Top navigation bar
        nav_bar = QFrame()
        nav_bar.setStyleSheet("background-color: #2C3E50;")
        nav_bar.setFixedHeight(50)
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(10, 0, 10, 0)
        
        # App title
        app_title = QLabel("Pawprinting PyQt6 V2")
        app_title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        nav_layout.addWidget(app_title)
        
        nav_layout.addStretch()
        
        # Navigation buttons
        self.fractal_btn = QPushButton("Fractal")
        self.fractal_btn.setStyleSheet(
            "QPushButton { background-color: #3498DB; color: white; padding: 5px 15px; border-radius: 5px; }"
            "QPushButton:hover { background-color: #2980B9; }"
            "QPushButton:checked { background-color: #1ABC9C; }"
        )
        self.fractal_btn.setCheckable(True)
        self.fractal_btn.setChecked(True)
        self.fractal_btn.clicked.connect(lambda: self.switch_screen(self.SCREEN_FRACTAL))
        
        self.history_btn = QPushButton("History")
        self.history_btn.setStyleSheet(
            "QPushButton { background-color: #3498DB; color: white; padding: 5px 15px; border-radius: 5px; }"
            "QPushButton:hover { background-color: #2980B9; }"
            "QPushButton:checked { background-color: #1ABC9C; }"
        )
        self.history_btn.setCheckable(True)
        self.history_btn.clicked.connect(lambda: self.switch_screen(self.SCREEN_HISTORY))
        
        nav_layout.addWidget(self.fractal_btn)
        nav_layout.addWidget(self.history_btn)
        
        main_layout.addWidget(nav_bar)
        
        # Create stacked widget for screens
        self.stacked_widget = QStackedWidget()
        
        # Create fractal screen (combining existing widgets)
        fractal_screen = QWidget()
        fractal_layout = QVBoxLayout(fractal_screen)
        fractal_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for text and fractal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.text_input_widget)
        splitter.addWidget(self.fractal_display_widget)
        splitter.setSizes([400, 600])  # Initial splitter sizes
        
        fractal_layout.addWidget(splitter)
        
        # Create history screen
        self.history_screen = HistoryScreen()
        
        # Connect history screen's loadPawprint signal to our handler
        self.history_screen.loadPawprint.connect(self.on_load_pawprint)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(fractal_screen)
        self.stacked_widget.addWidget(self.history_screen)
        
        main_layout.addWidget(self.stacked_widget)
        
        self.setCentralWidget(central_widget)
        
        # Set window properties
        self.setWindowTitle("Pawprinting PyQt6 V2")
        self.resize(1024, 768)
    
    def switch_screen(self, screen_index):
        """
        Switch to the specified screen.
        
        Args:
            screen_index: Index of the screen to switch to
        """
        self.current_screen = screen_index
        self.stacked_widget.setCurrentIndex(screen_index)
        
        # Update button states
        self.fractal_btn.setChecked(screen_index == self.SCREEN_FRACTAL)
        self.history_btn.setChecked(screen_index == self.SCREEN_HISTORY)
        
        logger.info(f"Switched to screen {screen_index}")
    
    def on_load_pawprint(self, params):
        """
        Handle loading a pawprint from history.
        
        Args:
            params: Parameter dictionary for the pawprint
        """
        logger.info("Loading pawprint from history")
        
        # Switch to fractal screen
        self.switch_screen(self.SCREEN_FRACTAL)
        
        # Set parameters in text input widget
        self.text_input_widget.set_parameters(params)
        
        # Forward signal for other components that might need it
        self.loadPawprint.emit(params)
