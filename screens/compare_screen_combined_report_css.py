#!/usr/bin/env python3
"""
Compare Screen - Combined Report CSS

Combines all CSS styles for the comparison report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_combined_report_css():
    """Get combined CSS styling for the complete report
    
    Returns:
        str: Complete CSS styling for report
    """
    try:
        # Import all CSS components
        from .compare_screen_pattern_css import get_pattern_details_css
        from .compare_screen_pattern_impact_css import get_pattern_impact_css
        from .compare_screen_conclusion_css import get_conclusion_css
        
        # Base CSS for overall report styling with dark theme
        base_css = """
        body {
            font-family: Arial, sans-serif;
            background-color: #121212;
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }
        
        .report-container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #1a1a1a;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
        }
        
        .report-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .report-title {
            color: #bb86fc;
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .section {
            margin-bottom: 30px;
        }
        
        .section-header {
            color: #bb86fc;
            border-bottom: 2px solid #bb86fc;
            padding-bottom: 8px;
            margin-bottom: 15px;
        }
        
        .section-description {
            margin-bottom: 15px;
            line-height: 1.5;
        }
        
        .chart-container {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        
        .chart-image {
            max-width: 100%;
            height: auto;
            margin: 10px 0;
            border: 1px solid #333333;
        }
        
        .chart-caption {
            font-style: italic;
            color: #9e9e9e;
            margin-top: 10px;
            font-size: 14px;
        }
        """
        
        # Combine all CSS components
        all_css = base_css + get_pattern_details_css() + get_pattern_impact_css() + get_conclusion_css()
        
        logger.debug("Combined report CSS created")
        return all_css
    except Exception as e:
        logger.error(f"Error creating combined report CSS: {str(e)}")
        return ""
