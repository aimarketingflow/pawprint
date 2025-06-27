#!/usr/bin/env python3
"""
Compare Screen - Chart Data Extraction

Extracts data for chart visualization from comparison files.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def extract_chart_data(self, category=None, threshold=0.0):
    """Extract data for chart visualization from comparison files
    
    Args:
        category: Pattern category to filter by (None for all)
        threshold: Minimum absolute change threshold
        
    Returns:
        dict: Chart data dictionary
    """
    try:
        # Get pattern changes by first calling the helper function
        patterns = []
        
        # If file_groups aren't set, return empty data
        if not hasattr(self, 'file_groups') or not self.file_groups:
            logger.warning("No file groups available for chart data extraction")
            return {"patterns": [], "pattern_names": []}
            
        # If diff_cache isn't set, return empty data
        if not hasattr(self, 'diff_cache') or not self.diff_cache or 'current_diff' not in self.diff_cache:
            logger.warning("No diff data available for chart data extraction")
            return {"patterns": [], "pattern_names": []}
