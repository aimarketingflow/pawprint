#!/usr/bin/env python3
"""
Compare Screen - Create Chart Selector

Creates chart type selector dropdown with dark theme styling.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from PyQt6.QtWidgets import QComboBox

logger = logging.getLogger(__name__)

def create_chart_selector(self):
    """Create chart type selector dropdown
    
    Returns:
        QComboBox: Styled chart type selector
    """
    try:
        # Create chart type selector dropdown
        chart_selector = QComboBox()
        chart_selector.setMinimumHeight(30)
        
        # Add available chart types
        chart_types = ["Bar Chart", "Pie Chart", "Line Chart", "Radar Chart"]
        for chart_type in chart_types:
            chart_selector.addItem(chart_type)
            
        # Apply dark theme styling with neon purple accent
        chart_selector.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #bb86fc;
                border-radius: 4px;
                padding: 5px 10px;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 1px solid #d7b8fc;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(:/images/down_arrow.png);
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #bb86fc;
                selection-background-color: #bb86fc;
                selection-color: #000000;
            }
        """)
        
        logger.debug("Chart selector dropdown created")
        return chart_selector
    except Exception as e:
        logger.error(f"Error creating chart selector: {str(e)}")
        return QComboBox()
