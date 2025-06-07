#!/usr/bin/env python3
"""
Fixed Size Application Window Utility

Provides functionality to set the main application window to a fixed size
with internal scrolling in both directions.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QApplication, QScrollArea, QMainWindow, QWidget, QFrame
from PyQt6.QtCore import Qt, QSize

logger = logging.getLogger(__name__)

class FixedSizeAppWindow:
    """Utility class to make the entire application window fixed size with scrolling"""
    
    @staticmethod
    def apply_fixed_size_with_scrolling(main_window, width, height, margin_percent=5):
        """
        Apply fixed size constraints to the main window and make its content scrollable
        
        Args:
            main_window: The main QMainWindow instance
            width: Target width for the window
            height: Target height for the window
            margin_percent: Percentage margin to reduce from dimensions (default 5%)
            
        Returns:
            QScrollArea: The scroll area added to make content scrollable
        """
        # Apply margin if specified
        if margin_percent > 0:
            width = int(width * (1 - margin_percent/100))
            height = int(height * (1 - margin_percent/100))
            
        # Set fixed size for the main window
        main_window.setFixedSize(width, height)
        main_window.setMinimumSize(width, height)
        main_window.setMaximumSize(width, height)
        
        # Get the central widget
        central_widget = main_window.centralWidget()
        if not central_widget:
            logger.error("No central widget found in main window")
            return None
            
        # Create a scroll area wrapper
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)  # No visible border
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Take ownership of the central widget
        central_widget.setParent(None)
        
        # Set the central widget in the scroll area
        scroll_area.setWidget(central_widget)
        
        # Set the scroll area as the new central widget
        main_window.setCentralWidget(scroll_area)
        
        logger.info(f"Applied fixed size {width}x{height} with internal scrolling to application window")
        return scroll_area
    
    @staticmethod
    def get_screen_dimensions():
        """
        Get the current screen dimensions for the primary display
        
        Returns:
            tuple: (width, height) of the primary screen
        """
        app = QApplication.instance()
        if not app:
            logger.error("No QApplication instance found")
            return (1024, 768)  # Default fallback
            
        screen = app.primaryScreen()
        if not screen:
            logger.error("No primary screen found")
            return (1024, 768)  # Default fallback
            
        geometry = screen.availableGeometry()
        return (geometry.width(), geometry.height())
