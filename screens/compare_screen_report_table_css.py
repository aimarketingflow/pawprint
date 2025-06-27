#!/usr/bin/env python3
"""
Compare Screen - Report Table CSS

Provides CSS styling for HTML report tables.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_table_css(self):
    """Get CSS styling for HTML report tables
    
    Returns:
        str: CSS styling for tables
    """
    # Table styling with dark theme
    css = """
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
            background-color: var(--card-background);
            border-radius: 8px;
            overflow: hidden;
        }
        
        thead tr {
            background-color: var(--surface-background);
        }
        
        th {
            text-align: left;
            padding: 12px;
            color: var(--primary-color);
            font-weight: 600;
        }
        
        td {
            padding: 10px 12px;
            border-bottom: 1px solid var(--surface-background);
        }
        
        tbody tr:last-child td {
            border-bottom: none;
        }
    """
    return css
