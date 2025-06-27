#!/usr/bin/env python3
"""
Compare Screen - Chart Data Preparation

Prepares final chart data structure from filtered patterns.

Author: AIMF LLC
Date: June 6, 2025
"""

def prepare_chart_data(self, patterns):
    """Prepare chart data structure from patterns
    
    Args:
        patterns: List of pattern dictionaries
        
    Returns:
        dict: Prepared chart data
    """
    # Create basic chart data structure
    chart_data = {
        "patterns": patterns,
        "pattern_names": [p.get("name", "Unknown") for p in patterns],
        "before_scores": [p.get("before_score", 0.0) for p in patterns],
        "after_scores": [p.get("after_score", 0.0) for p in patterns],
        "changes": [p.get("change", 0.0) for p in patterns],
        "percent_changes": [p.get("percent_change", 0.0) for p in patterns],
        "categories": [p.get("category", "Unknown") for p in patterns]
    }
