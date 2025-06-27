#!/usr/bin/env python3
"""
Compare Screen - Full HTML Report

Generates the complete HTML report structure.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def generate_full_html_report(before_file, after_file, summary_html, charts_html, pattern_details_html, conclusion_html):
    """Generate complete HTML report with all sections
    
    Args:
        before_file: Path to before comparison file
        after_file: Path to after comparison file
        summary_html: HTML content for summary section
        charts_html: HTML content for charts section
        pattern_details_html: HTML content for pattern details section
        conclusion_html: HTML content for conclusion section
        
    Returns:
        str: Complete HTML report
    """
    try:
        from .compare_screen_combined_report_css import get_combined_report_css
        
        # Get report CSS
        report_css = get_combined_report_css()
        
        # Create complete HTML document structure
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pawprinting Comparison Report</title>
    <style>
{report_css}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-header">
            <h1 class="report-title">Pawprinting Comparison Report</h1>
            <p class="report-subtitle">Detailed analysis of pattern changes</p>
        </div>
        
{summary_html}

{charts_html}

{pattern_details_html}

{conclusion_html}
    </div>
</body>
</html>
"""
        
        logger.info("Full HTML report generated")
        return full_html
    except Exception as e:
        logger.error(f"Error generating full HTML report: {str(e)}")
        return f"<html><body><h1>Pawprinting Comparison Report</h1><p>Error generating report: {str(e)}</p></body></html>"
