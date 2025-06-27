#!/usr/bin/env python3
"""
Compare Screen - Report Header

Creates HTML header section for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def create_report_header(self, title, timestamp):
    """Create HTML header for comparison report
    
    Args:
        title: Report title
        timestamp: Report generation timestamp
        
    Returns:
        str: HTML header content
    """
    try:
        # Format date for header
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get full CSS styling
        css = self.get_full_report_css()
        
        # Create header with dark theme styling and meta info
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {timestamp}</title>
    <style>
{css}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <div class="meta-info">
                <p>Generated: {current_date}</p>
                <p>Report ID: {timestamp}</p>
            </div>
        </header>
"""
        return html
    except Exception as e:
        logger.error(f"Error creating report header: {str(e)}")
        return "<!DOCTYPE html><html><head><title>Error</title></head><body>"
