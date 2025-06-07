#!/usr/bin/env python3
"""
Screen Wrapper Module

Provides a wrapper to make screens scrollable.
Used to modify all main screens in the application.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)

def make_screen_scrollable(screen_class):
    """
    Decorator to make a screen class scrollable.
    This wraps the screen's setup_ui method to make it scrollable.
    
    Args:
        screen_class: The screen class to make scrollable
        
    Returns:
        The modified screen class
    """
    original_setup_ui = screen_class.setup_ui
    
    def wrapped_setup_ui(self, *args, **kwargs):
        # Create a content widget that will be scrollable
        self.content_widget = QWidget()
        
        # Create the original UI in the content widget
        # Store original layout reference
        self._original_layout = self.layout() if self.layout() else QVBoxLayout()
        
        # Clear any existing layout from the screen
        if self.layout():
            # Temporarily store widgets from main layout
            temp_items = []
            layout = self.layout()
            while layout and layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    temp_items.append(item.widget())
                elif item.layout():
                    temp_items.append(item.layout())
                    
            # Clear old layout
            while self.layout():
                QWidget().setLayout(self.layout())
        
        # Call the original setup_ui on self (not content_widget)
        original_setup_ui(self, *args, **kwargs)
        
        # After the original setup_ui, the screen has its layouts and widgets
        # We need to move all of these to the content widget
        if self.layout():
            # Take ownership of the layout
            layout = self.layout()
            layout.setParent(None)
            
            # Set layout on content widget
            self.content_widget.setLayout(layout)
            
            # Create scroll area
            self.scroll_area = QScrollArea()
            self.scroll_area.setWidgetResizable(True)
            self.scroll_area.setFrameShape(Qt.FrameShape.NoFrame)  # No border
            self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.scroll_area.setWidget(self.content_widget)
            
            # Set new layout on screen with scroll area
            scroll_layout = QVBoxLayout()
            scroll_layout.setContentsMargins(0, 0, 0, 0)
            scroll_layout.addWidget(self.scroll_area)
            self.setLayout(scroll_layout)
            
            logger.debug(f"Made {self.__class__.__name__} scrollable")
        else:
            logger.warning(f"Could not make {self.__class__.__name__} scrollable - no layout found")
            
    # Replace the setup_ui method
    screen_class.setup_ui = wrapped_setup_ui
    return screen_class
