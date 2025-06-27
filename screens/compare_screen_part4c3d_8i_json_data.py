#!/usr/bin/env python3
"""
Compare Screen - Part 4c-3d-8i: JSON Data Preparation

Prepares comparison data for JSON export.

Author: AIMF LLC
Date: June 6, 2025
"""

from datetime import datetime

def _prepare_json_export_data(self):
    """Prepare comparison data for JSON export
    
    Returns:
        dict: JSON-serializable data structure
    """
    # Create base structure
    export_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "application": "Pawprinting PyQt6 V2",
            "version": "2.0.0"
        },
        "files": {},
        "diff": {},
        "analysis": {}
    }
    
    # Add file information
    if hasattr(self, 'file_groups') and self.file_groups:
        for origin, files in self.file_groups.items():
            export_data["files"][origin] = [
                {
                    "filename": f.get("filename", "Unknown"),
                    "path": f.get("path", "")
                } for f in files
            ]
    
    # Add diff information
    if hasattr(self, 'diff_cache') and self.diff_cache:
        export_data["diff"] = self.diff_cache.get('current_diff', {})
    
    # Add analysis information
    if hasattr(self, 'top_findings'):
        export_data["analysis"]["findings"] = self.top_findings
    
    return export_data
