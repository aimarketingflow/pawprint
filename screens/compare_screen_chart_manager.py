#!/usr/bin/env python3
"""
Compare Screen - Chart Manager

Manages chart display and switching in the UI.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def initialize_chart_display(self):
    """Initialize chart display container and layout
    
    Returns:
        bool: Success status
    """
    try:
        # Check if matplotlib is available
        if not self.MATPLOTLIB_AVAILABLE:
            self.charts_container.setVisible(False)
            logger.warning("Charts disabled - matplotlib not available")
            return False
            
        # Create layout if needed
        if hasattr(self, 'charts_layout') and self.charts_layout:
            return True
            
        # Initialize container widget
        self.charts_container.setVisible(True)
        
        return True
    except Exception as e:
        logger.error(f"Error initializing chart display: {str(e)}")
        return False
