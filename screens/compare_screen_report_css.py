#!/usr/bin/env python3
"""
Compare Screen - Report CSS

Provides CSS styling for HTML reports with dark theme.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_report_css(self):
    """Get CSS styling for HTML reports
    
    Returns:
        str: CSS styling
    """
    # Dark theme with neon purple accent styling
    css = """
        :root {
            --dark-background: #121212;
            --surface-background: #1e1e1e;
            --card-background: #333333;
            --primary-color: #bb86fc;
            --secondary-color: #03dac6;
            --error-color: #cf6679;
            --text-primary: #ffffff;
            --text-secondary: #bbbbbb;
        }
        
        body {
            background-color: var(--dark-background);
            color: var(--text-primary);
            font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
    """
    return css
