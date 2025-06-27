#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8f: HTML Report Template

Provides HTML template for styled comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

from datetime import datetime

def _generate_html_report(self):
    """Generate HTML report with styling
    
    Returns:
        str: Complete HTML document
    """
    # Start with HTML template
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Pawprinting Comparison Report</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #222; color: #eee; margin: 20px; }
        h1, h2, h3 { color: #bb86fc; }
        .container { max-width: 1000px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 30px; }
        .section { margin-bottom: 25px; padding: 15px; background-color: #333; border-radius: 5px; }
        .improved { color: #4CAF50; }
        .regressed { color: #F44336; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Pawprinting Comparison Report</h1>
            <p>Generated: {date}</p>
        </div>
"""
    
    # Insert comparison data
    html = html.format(date=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    # Add file information
    html += self._get_html_files_section()
    
    # Add summary section
    html += self._get_html_summary_section()
    
    # Close HTML document
    html += """
    </div>
</body>
</html>"""

    return html
