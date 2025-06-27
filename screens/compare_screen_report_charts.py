#!/usr/bin/env python3
"""
Compare Screen - Report Charts

Creates HTML charts section for reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def format_charts_section_html(self, chart_data):
    """Format HTML charts section for report
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        str: HTML charts section
    """
    # Create charts section with dark theme styling
    html = """
        <section class="charts">
            <h2>Charts & Visualizations</h2>
            <p>The following charts represent the pattern changes between the compared files.</p>
            <div class="chart-container" style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 20px;">
    """
    return html
