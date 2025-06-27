#!/usr/bin/env python3
"""
Compare Screen - Comprehensive Chart Panel

Creates a comprehensive chart panel with all components integrated.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout

logger = logging.getLogger(__name__)

def create_comprehensive_chart_panel(self):
    """Create comprehensive chart panel with all components integrated
    
    Returns:
        QWidget: Chart panel with all components
    """
    try:
        logger.info("Creating comprehensive chart panel")
        
        # Check matplotlib availability first
        self.check_matplotlib_availability()
        
        if not self.MATPLOTLIB_AVAILABLE:
            logger.warning("Charts disabled - matplotlib not available")
            return self.create_charts_unavailable_widget()
            
        # Create container widget
        chart_panel = QWidget()
        
        # Create chart selector
        chart_selector = self.create_chart_selector()
        self.connect_chart_selector(chart_selector)
        self.chart_selector = chart_selector
        
        # Create chart display widget
        chart_widget = self.create_chart_display_widget()
        self.chart_widget = chart_widget
        
        # Create expanded button layout with all action buttons
        button_layout = self.create_expanded_action_buttons_layout()
        
        # Create panel layout
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Add components to layout
        layout.addWidget(chart_selector)
        layout.addWidget(chart_widget)
        layout.addLayout(button_layout)
        
        # Set layout on panel
        chart_panel.setLayout(layout)
        
        # Apply dark theme styling
        chart_panel.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: #ffffff;
                border: 1px solid #333333;
                border-radius: 8px;
            }
        """)
        
        # Load user preferences
        self.load_chart_settings()
        
        # Initial chart update
        self.update_chart_display()
        
        logger.info("Comprehensive chart panel created")
        return chart_panel
    except Exception as e:
        logger.error(f"Error creating comprehensive chart panel: {str(e)}")
        return QWidget()
