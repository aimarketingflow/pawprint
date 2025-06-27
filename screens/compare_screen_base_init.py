#!/usr/bin/env python3
"""
Compare Screen Base Initialization

Handles basic initialization for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

def init_compare_screen(self, parent=None):
    """Basic initialization for CompareScreen
    
    Args:
        self: CompareScreen instance
        parent: Parent widget
    """
    # Set up attributes
    self.file_groups = {}
    self.diff_cache = {}
    self.results_ready = False
    self.current_view = "side_by_side"
    self.current_chart_type = "radar"
    
    # Check matplotlib availability
    try:
        import matplotlib
        self.MATPLOTLIB_AVAILABLE = True
    except ImportError:
        self.MATPLOTLIB_AVAILABLE = False
