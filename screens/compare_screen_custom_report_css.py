#!/usr/bin/env python3
"""
Compare Screen - Custom Report CSS

Provides custom CSS styling for the HTML report.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_custom_report_css():
    """Get custom CSS styling for the HTML report
    
    Returns:
        str: CSS styling code
    """
    try:
        # Define dark theme custom CSS
        css = """
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background-color: #121212;
                color: #ffffff;
                margin: 0;
                padding: 20px;
                line-height: 1.6;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #1e1e1e;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
            }
            
            h1, h2, h3, h4 {
                color: #bb86fc;
                margin-top: 24px;
                margin-bottom: 16px;
            }
            
            h1 {
                font-size: 28px;
                text-align: center;
                padding-bottom: 16px;
                border-bottom: 1px solid #333333;
            }
            
            h2 {
                font-size: 24px;
                padding-bottom: 8px;
                border-bottom: 1px solid #333333;
            }
            
            h3 {
                font-size: 20px;
                color: #03dac6;
            }
            
            p {
                margin-bottom: 16px;
            }
            
            .summary-section {
                background-color: #2d2d2d;
                padding: 16px;
                border-radius: 6px;
                margin-bottom: 24px;
            }
            
            .chart-section {
                text-align: center;
                margin-bottom: 32px;
            }
            
            .chart-image {
                max-width: 100%;
                height: auto;
                border-radius: 6px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
                margin-top: 16px;
            }
            
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background-color: #1e1e1e;
            }
            
            th {
                background-color: #2d2d2d;
                color: #bb86fc;
                font-weight: bold;
                text-align: left;
                padding: 12px;
                border-bottom: 2px solid #333333;
            }
            
            td {
                padding: 10px 12px;
                border-bottom: 1px solid #333333;
            }
            
            tr:nth-child(even) {
                background-color: #252525;
            }
            
            tr:hover {
                background-color: #303030;
            }
            
            .positive {
                color: #03dac6;
            }
            
            .negative {
                color: #cf6679;
            }
            
            .neutral {
                color: #a0a0a0;
            }
            
            .percentage {
                font-weight: bold;
            }
            
            .pattern-name {
                font-weight: bold;
            }
            
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #333333;
                font-size: 14px;
                color: #808080;
                text-align: center;
            }
            
            .file-info {
                font-style: italic;
                margin-bottom: 8px;
            }
            
            .timestamp {
                font-weight: 600;
            }
            
            .logo {
                text-align: center;
                margin-bottom: 20px;
            }
            
            .logo img {
                max-width: 200px;
                height: auto;
            }
        """
        
        logger.debug("Custom report CSS generated")
        return css
    except Exception as e:
        logger.error(f"Error generating custom report CSS: {str(e)}")
        # Return minimal CSS in case of error
        return "body { font-family: Arial, sans-serif; }"
