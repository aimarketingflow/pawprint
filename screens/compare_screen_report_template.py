#!/usr/bin/env python3
"""
Compare Screen - Report Template

HTML template for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_report_html_template(self):
    """Get HTML template for comparison report
    
    Returns:
        str: HTML template string
    """
    try:
        # Current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create HTML template with dark theme styling
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Pawprinting Comparison Report</title>
            <style>
                body {{ background-color: #222222; color: #dddddd; font-family: Arial, sans-serif; margin: 20px; }}
                h1, h2, h3 {{ color: #bb86fc; }} /* Neon purple accent */
                .container {{ max-width: 1200px; margin: 0 auto; }}
            </style>
        </head>
        """
        return html_template
