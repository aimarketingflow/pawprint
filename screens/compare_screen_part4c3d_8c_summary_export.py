#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8c: Summary Export

Creates simple summary export for comparison results.

Author: AIMF LLC
Date: June 6, 2025
"""

import os
import logging
from datetime import datetime

def export_comparison_summary(self, file_path=None):
    """Export basic comparison summary to text file
    
    Args:
        file_path: Optional file path
        
    Returns:
        str: Path to created file or None
    """
    try:
        # Generate default path if needed
        if file_path is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            export_dir = os.path.join(os.path.expanduser("~"), 
                         "Documents", "Pawprinting_Exports", "Reports")
            os.makedirs(export_dir, exist_ok=True)
            file_path = os.path.join(export_dir, f"comparison_summary_{timestamp}.txt")
        
        # Get summary data
        summary = self._generate_text_summary()
        
        # Write to file
        with open(file_path, 'w') as f:
            f.write(summary)
            
        return file_path
        
    except Exception as e:
        logging.error(f"Export summary error: {e}")
        return None
