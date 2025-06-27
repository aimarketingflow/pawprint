#!/usr/bin/env python3
"""
Compare Screen - Report Summary

Generates summary section for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def get_report_summary_section(self, chart_data, before_file, after_file):
    """Get HTML summary section for comparison report
    
    Args:
        chart_data: Chart data dictionary
        before_file: Before comparison file
        after_file: After comparison file
        
    Returns:
        str: HTML summary section
    """
    try:
        # Count patterns by change direction
        positive_changes = 0
        negative_changes = 0
        neutral_changes = 0
        
        for pattern in chart_data.get('patterns', []):
            change = pattern.get('change', 0)
            if change > 0.05:
                positive_changes += 1
            elif change < -0.05:
                negative_changes += 1
            else:
                neutral_changes += 1
