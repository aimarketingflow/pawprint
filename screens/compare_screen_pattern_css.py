#!/usr/bin/env python3
"""
Compare Screen - Pattern CSS

CSS styling for pattern details in report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_pattern_details_css():
    """Get CSS styling for pattern details in report
    
    Returns:
        str: CSS styling for pattern details
    """
    try:
        # CSS styling for pattern details section with dark theme
        pattern_css = """
        .pattern-details-section {
            margin: 20px 0;
            padding: 15px;
            background-color: #1e1e1e;
            border-radius: 8px;
        }
        
        .pattern-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            font-size: 14px;
        }
        
        .pattern-table th {
            background-color: #333333;
            color: #bb86fc;
            font-weight: bold;
            text-align: left;
            padding: 12px 10px;
            border-bottom: 2px solid #bb86fc;
        }
        
        .pattern-table td {
            padding: 8px 10px;
            border-bottom: 1px solid #333333;
        }
        
        .pattern-table tr:last-child td {
            border-bottom: none;
        }
        
        .pattern-table tr:nth-child(even) {
            background-color: #262626;
        }
        
        .pattern-table tr:hover {
            background-color: #2d2d2d;
        }
        """
        
        logger.debug("Pattern details CSS created")
        return pattern_css
    except Exception as e:
        logger.error(f"Error creating pattern details CSS: {str(e)}")
        return ""
