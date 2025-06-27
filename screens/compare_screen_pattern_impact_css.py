#!/usr/bin/env python3
"""
Compare Screen - Pattern Impact CSS

CSS styling for pattern impact indicators in report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_pattern_impact_css():
    """Get CSS styling for pattern impact indicators
    
    Returns:
        str: CSS styling for pattern impact indicators
    """
    try:
        # CSS styling for pattern impact indicators with color coding
        impact_css = """
        /* Positive Impact Styling */
        .pattern-row.positive .change,
        .pattern-row.positive .change-percent {
            color: #03dac6;
            font-weight: bold;
        }
        
        .impact.positive .impact-indicator {
            background-color: #03dac6;
            color: #000000;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
        }
        
        /* Negative Impact Styling */
        .pattern-row.negative .change,
        .pattern-row.negative .change-percent {
            color: #cf6679;
            font-weight: bold;
        }
        
        .impact.negative .impact-indicator {
            background-color: #cf6679;
            color: #000000;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
        }
        
        /* Neutral Impact Styling */
        .pattern-row.neutral .change,
        .pattern-row.neutral .change-percent {
            color: #9e9e9e;
        }
        
        .impact.neutral .impact-indicator {
            background-color: #9e9e9e;
            color: #000000;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
        }
        
        .table-notes {
            font-size: 12px;
            color: #9e9e9e;
            margin-top: 10px;
            font-style: italic;
        }
        """
        
        logger.debug("Pattern impact CSS created")
        return impact_css
    except Exception as e:
        logger.error(f"Error creating pattern impact CSS: {str(e)}")
        return ""
