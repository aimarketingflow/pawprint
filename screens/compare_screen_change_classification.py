#!/usr/bin/env python3
"""
Compare Screen - Change Classification

Classifies pattern changes as positive, negative, or neutral.

Author: AIMF LLC
Date: June 6, 2025
"""

def classify_changes(self, patterns, threshold=0.05):
    """Classify patterns into positive, negative, or neutral changes
    
    Args:
        patterns: List of pattern dictionaries
        threshold: Small change threshold for neutral classification
        
    Returns:
        dict: Classification dictionary
    """
    classification = {
        "positive_changes": [],
        "negative_changes": [],
        "neutral_changes": []
    }
    
    for pattern in patterns:
        change = pattern.get("change", 0.0)
        
        if change > threshold:
            classification["positive_changes"].append(pattern)
        elif change < -threshold:
            classification["negative_changes"].append(pattern)
        else:
            classification["neutral_changes"].append(pattern)
