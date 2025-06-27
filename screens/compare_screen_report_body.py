#!/usr/bin/env python3
"""
Compare Screen - Report Body

HTML body content for comparison reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def get_report_body(self, chart_data, timestamp):
    """Get HTML body content for comparison report
    
    Args:
        chart_data: Chart data dictionary
        timestamp: Report generation timestamp
        
    Returns:
        str: HTML body content
    """
    try:
        # Current date and time for report header
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get file info if available
        before_file = "Unknown"
        after_file = "Unknown"
        
        if hasattr(self, 'file_groups') and self.file_groups:
            if 'before' in self.file_groups and self.file_groups['before']:
                before_file = self.file_groups['before'][0] if self.file_groups['before'] else "Unknown"
            if 'after' in self.file_groups and self.file_groups['after']:
                after_file = self.file_groups['after'][0] if self.file_groups['after'] else "Unknown"
                
        # Create body content with report header
        body = f"""
        <body>
            <div class="container">
                <header>
                    <img src="data:image/png;base64,LOGO_BASE64_PLACEHOLDER" alt="AIMF LLC" style="height: 60px;">
                    <h1>Pawprinting Comparison Report</h1>
                    <p>Generated on: {current_datetime}</p>
                </header>
        """
        
        return body
    except Exception as e:
        logger.error(f"Error generating report body: {str(e)}")
        return "<body><p>Error generating report body.</p>"
