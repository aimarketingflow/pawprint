#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-1: Chart Data Extraction

Implements the chart data extraction methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for chart data extraction that would be included in the CompareScreen class

def extract_chart_data(self, category=None, threshold=0.0):
    """Extract data for chart visualization from comparison files
    
    Args:
        category: Pattern category to filter by (None for all)
        threshold: Minimum absolute change threshold
        
    Returns:
        dict: Chart data dictionary
    """
    # Get pattern changes filtered by category and threshold
    patterns = self.get_pattern_changes_by_category(category, threshold)
    
    # Prepare data structure
    chart_data = {
        "patterns": patterns,
        "pattern_names": [p.get("name", "Unknown") for p in patterns],
        "before_scores": [p.get("before_score", 0.0) for p in patterns],
        "after_scores": [p.get("after_score", 0.0) for p in patterns],
        "changes": [p.get("change", 0.0) for p in patterns],
        "percent_changes": [p.get("percent_change", 0.0) for p in patterns],
        "categories": [p.get("category", "Unknown") for p in patterns],
        "category_counts": {},
        "positive_changes": [],
        "negative_changes": [],
        "neutral_changes": []
    }
    
    # Calculate category counts
    for pattern in patterns:
        category = pattern.get("category", "Unknown")
        if category not in chart_data["category_counts"]:
            chart_data["category_counts"][category] = 0
        chart_data["category_counts"][category] += 1
    
    # Separate positive and negative changes
    for pattern in patterns:
        change = pattern.get("change", 0.0)
        if change > threshold:
            chart_data["positive_changes"].append(pattern)
        elif change < -threshold:
            chart_data["negative_changes"].append(pattern)
        else:
            chart_data["neutral_changes"].append(pattern)
    
    return chart_data

def get_chart_data_by_type(self, chart_type, category=None, threshold=0.0):
    """Get chart data formatted for specific chart type
    
    Args:
        chart_type: Type of chart (radar, bar, pie, line, heatmap)
        category: Pattern category to filter by (None for all)
        threshold: Minimum absolute change threshold
        
    Returns:
        dict: Chart data dictionary specific to chart type
    """
    # Extract base chart data
    base_data = self.extract_chart_data(category, threshold)
    
    # Format data based on chart type
    if chart_type == "radar":
        return self.format_radar_chart_data(base_data)
    elif chart_type == "bar":
        return self.format_bar_chart_data(base_data)
    elif chart_type == "pie":
        return self.format_pie_chart_data(base_data)
    elif chart_type == "line":
        return self.format_line_chart_data(base_data)
    elif chart_type == "heatmap":
        return self.format_heatmap_chart_data(base_data)
    else:
        # Default to bar chart format
        return self.format_bar_chart_data(base_data)

def get_chart_description(self, chart_type, chart_data):
    """Generate text description for chart data
    
    Args:
        chart_type: Type of chart
        chart_data: Chart data dictionary
        
    Returns:
        str: HTML-formatted chart description
    """
    # Generate based on chart type
    if chart_type == "radar":
        return self.get_radar_chart_description(chart_data)
    elif chart_type == "bar":
        return self.get_bar_chart_description(chart_data)
    elif chart_type == "pie":
        return self.get_pie_chart_description(chart_data)
    elif chart_type == "line":
        return self.get_line_chart_description(chart_data)
    elif chart_type == "heatmap":
        return self.get_heatmap_chart_description(chart_data)
    else:
        return "<p>No description available for this chart type.</p>"

def get_available_categories(self):
    """Get list of available pattern categories
    
    Returns:
        list: List of category strings
    """
    # Get all unique categories
    categories = self.get_pattern_categories()
    
    # Add "All" option at the beginning
    return ["All"] + categories

def update_chart_display(self):
    """Update the chart display with current settings"""
    # Get current control values
    chart_type = self.chart_type_combo.currentText()
    category = self.pattern_category_combo.currentText()
    threshold = self.score_threshold_slider.value() / 100.0
    
    # If category is "All", set to None for filtering
    if category == "All":
        category = None
    
    # Get chart data
    chart_data = self.get_chart_data_by_type(chart_type, category, threshold)
    
    # Draw chart
    self.draw_chart(chart_type, chart_data)
    
    # Update description
    description = self.get_chart_description(chart_type, chart_data)
    self.chart_description_text.setHtml(description)
