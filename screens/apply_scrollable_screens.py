#!/usr/bin/env python3
"""
Apply Scrollable Screens Module

Automatically makes all main screen classes scrollable.
This module is imported by pawprint_pyqt6_main.py and patches all screen classes.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import inspect
import sys
import importlib
import os
from pathlib import Path
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QApplication
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)

# Screen class names to modify
MAIN_SCREEN_CLASSES = [
    "DashboardScreen",
    "AnalyzeScreen",
    "CompareScreen",
    "HistoryScreen",
    "GenerateScreen",
    "FractalButterflyScreen"
]

class ScrollableScreenPatcher:
    """Class to patch screen widgets with scrollable functionality"""
    
    @staticmethod
    def make_scrollable(screen):
        """
        Convert a screen's content to be scrollable.
        
        Args:
            screen: The screen instance to make scrollable
        """
        # Skip if already made scrollable
        if hasattr(screen, 'is_scrollable_patched') and screen.is_scrollable_patched:
            return
            
        # Store original layout
        original_layout = screen.layout()
        if not original_layout:
            logger.warning(f"Cannot make {screen.__class__.__name__} scrollable: no layout")
            return
            
        # Create content widget to hold the existing layout
        content_widget = QWidget()
        
        # Take all widgets from original layout and add to content widget
        new_layout = QVBoxLayout()
        while original_layout.count():
            item = original_layout.takeAt(0)
            if item.widget():
                new_layout.addWidget(item.widget())
            elif item.layout():
                new_layout.addLayout(item.layout())
                
        # Set layout to content widget
        content_widget.setLayout(new_layout)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(Qt.FrameShape.NoFrame)  # No border
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(content_widget)
        
        # Set new layout with scroll area to screen
        scroll_layout = QVBoxLayout()
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.addWidget(scroll_area)
        screen.setLayout(scroll_layout)
        
        # Mark as patched
        screen.is_scrollable_patched = True
        
        logger.debug(f"Made {screen.__class__.__name__} scrollable")
        
    @classmethod
    def patch_screen_class(cls, screen_class):
        """
        Patch a screen class to make instances scrollable after initialization.
        
        Args:
            screen_class: The screen class to patch
        """
        # Store original __init__ method
        original_init = screen_class.__init__
        
        # Define new __init__ method
        def new_init(self, *args, **kwargs):
            # Call original __init__
            original_init(self, *args, **kwargs)
            
            # Make scrollable after initialization is complete
            cls.make_scrollable(self)
            
        # Replace __init__ method
        screen_class.__init__ = new_init
        logger.info(f"Patched {screen_class.__name__} to be scrollable")
        
def patch_all_screen_classes():
    """Find and patch all main screen classes to be scrollable"""
    # Import screens package to ensure all screen modules are loaded
    from screens import (
        dashboard_screen, analyze_screen, compare_screen, 
        history_screen, generate_screen, fractal_butterfly_screen
    )
    
    # Import each screen module
    modules = {
        'dashboard_screen': dashboard_screen,
        'analyze_screen': analyze_screen,
        'compare_screen': compare_screen,
        'history_screen': history_screen,
        'generate_screen': generate_screen,
        'fractal_butterfly_screen': fractal_butterfly_screen
    }
    
    # Patch each main screen class
    for module_name, module in modules.items():
        for class_name in MAIN_SCREEN_CLASSES:
            if hasattr(module, class_name):
                screen_class = getattr(module, class_name)
                ScrollableScreenPatcher.patch_screen_class(screen_class)
                logger.info(f"Patched {class_name} in {module_name}")

# Apply patches when module is imported
patch_all_screen_classes()
