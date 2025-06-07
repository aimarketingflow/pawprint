#!/usr/bin/env python3
"""
Scrollable Screen Utility

Provides functions to make screen widgets scrollable.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)

def make_scrollable(widget, layout=None, scroll_policy=None):
    """
    Convert a widget with its layout to be scrollable within a QScrollArea
    
    Args:
        widget: The widget to make scrollable
        layout: Optional layout to set on widget if it doesn't have one
        scroll_policy: Optional tuple of (horizontal policy, vertical policy)
    
    Returns:
        QScrollArea: Scrollable container containing the widget
    """
    # Create scroll area
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)  # This is important for proper resizing
    
    # Configure scroll area
    scroll_area.setFrameShape(Qt.FrameShape.NoFrame)  # Remove border
    
    # Set scroll policies
    if scroll_policy:
        horizontal, vertical = scroll_policy
        scroll_area.setHorizontalScrollBarPolicy(horizontal)
        scroll_area.setVerticalScrollBarPolicy(vertical)
    else:
        # Default: Only allow vertical scrolling
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    
    # If provided a layout, set it to the widget
    if layout and not widget.layout():
        widget.setLayout(layout)
    
    # Set the widget as the scroll area content
    scroll_area.setWidget(widget)
    
    logger.debug(f"Made {widget.__class__.__name__} scrollable")
    return scroll_area

def convert_widget_layout_to_scrollable(widget, parent_layout):
    """
    Convert an existing widget with layout to be scrollable by:
    1. Creating an internal content widget
    2. Moving the widget's layout to the content widget
    3. Creating a scroll area and setting the content widget as its content
    4. Setting a new layout on the widget with the scroll area
    
    Args:
        widget: Widget to convert
        parent_layout: The parent layout that will contain the scroll area
        
    Returns:
        The created scroll area
    """
    # Get the existing layout
    existing_layout = widget.layout()
    if not existing_layout:
        logger.warning(f"Widget {widget.__class__.__name__} has no layout to convert")
        return None
    
    # Create a new content widget
    content_widget = QWidget()
    
    # Take ownership of the existing layout
    existing_layout.setParent(None)
    
    # Set the existing layout on the content widget
    content_widget.setLayout(existing_layout)
    
    # Create a scroll area and set the content widget
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setFrameShape(Qt.FrameShape.NoFrame)  # No border
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setWidget(content_widget)
    
    # Replace the original layout with a new one containing the scroll area
    new_layout = QVBoxLayout()
    new_layout.setContentsMargins(0, 0, 0, 0)  # No margins
    new_layout.addWidget(scroll_area)
    widget.setLayout(new_layout)
    
    logger.debug(f"Converted {widget.__class__.__name__} layout to scrollable")
    return scroll_area
