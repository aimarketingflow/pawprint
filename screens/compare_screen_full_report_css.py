#!/usr/bin/env python3
"""
Compare Screen - Full Report CSS

Combines all CSS styling for HTML reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_full_report_css(self):
    """Get complete CSS styling for HTML reports
    
    Returns:
        str: Complete CSS styling
    """
    try:
        # Get base CSS
        base_css = self.get_report_css()
        
        # Get element CSS
        element_css = self.get_element_css()
        
        # Get table CSS
        table_css = self.get_table_css()
        
        # Additional component styles
        component_css = """
            /* Chart section styles */
            .chart-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .chart {
                flex: 1;
                min-width: 300px;
                background-color: var(--card-background);
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            
            .chart img {
                width: 100%;
                max-width: 500px;
                display: block;
                margin: 0 auto;
            }
            
            /* Cards and info boxes */
            .file-info, .stats {
                background-color: var(--card-background);
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            
            /* Responsive design */
            @media (max-width: 768px) {
                .chart {
                    min-width: 100%;
                }
            }
        """
        
        # Combine all CSS
        full_css = base_css + element_css + table_css + component_css
        
        return full_css
    except Exception as e:
        logger.error(f"Error creating full report CSS: {str(e)}")
        return ""
