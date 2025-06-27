#!/usr/bin/env python3
"""
Compare Screen - Patterns Section

Creates HTML patterns detail section for reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_patterns_section_html(self, chart_data):
    """Create HTML patterns detail section for report
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        str: HTML patterns section
    """
    # Create patterns section with dark theme styling
    html = """
        <section class="patterns">
            <h2>Pattern Details</h2>
            <p>Detailed information about individual pattern changes.</p>
            <div class="pattern-table-container" style="overflow-x: auto;">
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <thead>
                        <tr style="background-color: #444444;">
    """
    return html
