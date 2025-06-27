#!/usr/bin/env python3
"""
Compare Screen - Report Element CSS

Provides CSS styling for individual HTML report elements.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_element_css(self):
    """Get CSS styling for HTML report elements
    
    Returns:
        str: CSS styling for elements
    """
    # Element styling with dark theme
    css = """
        header {
            background-color: var(--surface-background);
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        h1 {
            color: var(--primary-color);
            margin: 0 0 10px 0;
            font-size: 28px;
        }
        
        h2 {
            color: var(--primary-color);
            margin: 30px 0 15px 0;
            font-size: 22px;
            border-bottom: 1px solid var(--primary-color);
            padding-bottom: 8px;
        }
        
        h3 {
            color: var(--secondary-color);
            margin: 20px 0 10px 0;
            font-size: 18px;
        }
        
        section {
            margin-bottom: 40px;
        }
        
        .meta-info {
            color: var(--text-secondary);
            font-size: 0.9em;
            margin-bottom: 10px;
        }
    """
    return css
