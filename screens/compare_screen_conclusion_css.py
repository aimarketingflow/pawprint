#!/usr/bin/env python3
"""
Compare Screen - Conclusion CSS

CSS styling for report conclusion section.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_conclusion_css():
    """Get CSS styling for report conclusion
    
    Returns:
        str: CSS styling for conclusion section
    """
    try:
        # CSS styling for conclusion section with dark theme
        conclusion_css = """
        .conclusion-section {
            margin: 30px 0 20px 0;
            padding: 15px;
            background-color: #1e1e1e;
            border-radius: 8px;
        }
        
        .conclusion-text {
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .report-timestamp {
            font-style: italic;
            color: #9e9e9e;
            margin-bottom: 10px;
        }
        
        .report-footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 15px;
            border-top: 1px solid #333333;
            color: #bb86fc;
            font-weight: bold;
        }
        """
        
        logger.debug("Conclusion CSS created")
        return conclusion_css
    except Exception as e:
        logger.error(f"Error creating conclusion CSS: {str(e)}")
        return ""
