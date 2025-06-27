#!/usr/bin/env python3
"""
Compare Screen - Report Header HTML

Generates HTML header and structure for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_report_header_html(self, before_file, after_file):
    """Generate HTML header and structure for comparison report
    
    Args:
        before_file: Path to before comparison file
        after_file: Path to after comparison file
        
    Returns:
        str: HTML header and structure
    """
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract just the filenames for display
        before_name = before_file.split('/')[-1] if before_file else "Unknown"
        after_name = after_file.split('/')[-1] if after_file else "Unknown"
        
        # Generate HTML header and document structure
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pawprinting Comparison Report</title>
    <style>
        /* CSS will be inserted here */
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <!-- Logo could be embedded here as base64 -->
            <h1>Pawprinting Comparison Report</h1>
        </div>
        
        <div class="file-info">
            <p><strong>Before File:</strong> {before_name}</p>
            <p><strong>After File:</strong> {after_name}</p>
            <p><strong>Generated:</strong> <span class="timestamp">{timestamp}</span></p>
        </div>
"""
        
        logger.debug("Report header HTML generated")
        return html
    except Exception as e:
        logger.error(f"Error generating report header HTML: {str(e)}")
        # Return minimal HTML in case of error
        return "<!DOCTYPE html><html><head><title>Comparison Report</title></head><body>"
