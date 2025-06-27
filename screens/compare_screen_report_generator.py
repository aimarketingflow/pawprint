#!/usr/bin/env python3
"""
Compare Screen - Report Generator

Generates HTML reports for pattern comparisons.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_comparison_report(self, chart_data):
    """Generate HTML report for comparison data
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        tuple: (success, report_html, file_path)
    """
    try:
        # Get export paths
        export_paths = self.get_export_paths()
        reports_path = export_paths.get('reports', '')
        
        # Ensure report directory exists
        if not os.path.exists(reports_path):
            os.makedirs(reports_path)
            
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
