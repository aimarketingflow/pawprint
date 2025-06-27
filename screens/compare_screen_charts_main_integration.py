#!/usr/bin/env python3
"""
Compare Screen - Charts Main Integration

Main module for integrating all chart functionality within CompareScreen.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)

class ChartIntegration:
    """
    Chart functionality integration for CompareScreen.
    Provides methods to add all chart functionality to the main compare screen.
    """
    
    @staticmethod
    def add_chart_components(compare_screen, main_layout):
        """Add all chart components to the Compare Screen
        
        Args:
            compare_screen: The main CompareScreen instance
            main_layout: The main layout for the Compare Screen
            
        Returns:
            None
        """
        try:
            logger.info("Integrating chart components into Compare Screen")
            
            # Create comprehensive chart panel
            chart_panel = compare_screen.create_comprehensive_chart_panel()
            
            # Add to main layout
            if main_layout is not None:
                main_layout.addWidget(chart_panel)
                
            logger.info("Chart components integrated successfully")
            
        except Exception as e:
            logger.error(f"Error integrating chart components: {str(e)}")
