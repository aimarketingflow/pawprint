#!/usr/bin/env python3
"""
Compare Screen - Generate Report Filename

Generates timestamped filenames for reports and exports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging
import os
from datetime import datetime
import re

logger = logging.getLogger(__name__)

def generate_report_filename(self, before_file=None, after_file=None, extension=".html"):
    """Generate a timestamped filename for reports
    
    Args:
        before_file: Path to before comparison file (optional)
        after_file: Path to after comparison file (optional)
        extension: File extension for the report (default: .html)
        
    Returns:
        str: Generated filename
    """
    try:
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Extract base filenames if provided
        before_name = "unknown"
        after_name = "unknown"
        
        if before_file:
            before_name = os.path.basename(before_file)
            before_name = os.path.splitext(before_name)[0]
            # Remove non-alphanumeric characters for filename safety
            before_name = re.sub(r'[^\w]', '_', before_name)
            
        if after_file:
            after_name = os.path.basename(after_file)
            after_name = os.path.splitext(after_name)[0]
            # Remove non-alphanumeric characters for filename safety
            after_name = re.sub(r'[^\w]', '_', after_name)
            
        # Generate filename: compare_before_after_timestamp.ext
        filename = f"compare_{before_name}_{after_name}_{timestamp}{extension}"
        
        logger.debug(f"Generated report filename: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error generating report filename: {str(e)}")
        return f"comparison_report_{timestamp}{extension}"
