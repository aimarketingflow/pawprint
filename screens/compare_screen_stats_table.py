#!/usr/bin/env python3
"""
Compare Screen - Stats Table

Creates styled HTML tables for statistics in reports.

Author: AIMF LLC
Date: June 6, 2025
"""

import logging

logger = logging.getLogger(__name__)

def create_stats_table(self, pos_percent, neg_percent, neu_percent, positive_changes, negative_changes, neutral_changes, total_patterns):
    """Create HTML statistics table with dark theme styling
    
    Args:
        pos_percent: Positive changes percentage
        neg_percent: Negative changes percentage
        neu_percent: Neutral changes percentage
        positive_changes: Count of positive changes
        negative_changes: Count of negative changes
        neutral_changes: Count of neutral changes
        total_patterns: Total pattern count
        
    Returns:
        str: HTML statistics table
    """
    # Create stats tables with dark theme and neon purple styling
    html = """
            <div class="stats" style="background-color: #333333; padding: 10px; border-radius: 5px;">
                <h3>Change Statistics</h3>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                    <thead>
                        <tr style="background-color: #444444;">
                            <th style="padding: 8px; text-align: left; color: #bb86fc;">Type</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">Count</th>
                            <th style="padding: 8px; text-align: center; color: #bb86fc;">Percentage</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    return html
