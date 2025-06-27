#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-7a: Base Chart Insights

Implements the base chart insights generation methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import json
import logging
from datetime import datetime

# This file contains methods for base chart insights generation that would be included in the CompareScreen class

def generate_basic_chart_insights(self, chart_data, chart_type):
    """Generate basic insights for any chart type
    
    Args:
        chart_data: Chart data dictionary
        chart_type: Type of chart (radar, bar, line, pie, heatmap)
        
    Returns:
        dict: Dictionary of basic insights
    """
    insights = {
        "chart_type": chart_type,
        "timestamp": datetime.now().isoformat(),
        "general": [],
        "improvements": [],
        "regressions": [],
        "recommendations": []
    }
    
    try:
        # Handle missing or invalid data
        if not chart_data:
            insights["general"].append("No chart data available for analysis.")
            return insights
            
        # Get core data elements
        patterns = chart_data.get("patterns", [])
        changes = chart_data.get("changes", [])
        categories = chart_data.get("categories", [])
        
        # Basic statistics across all patterns
        if patterns and changes:
            total_patterns = len(patterns)
            improved_count = sum(1 for c in changes if c > 0)
            regressed_count = sum(1 for c in changes if c < 0)
            unchanged_count = sum(1 for c in changes if c == 0)
            
            # Add general statistics
            insights["general"].append(f"Analyzed {total_patterns} pattern{'s' if total_patterns != 1 else ''}")
            
            if improved_count > 0:
                pct_improved = (improved_count / total_patterns) * 100
                insights["general"].append(f"{improved_count} patterns improved ({pct_improved:.1f}%)")
                
            if regressed_count > 0:
                pct_regressed = (regressed_count / total_patterns) * 100
                insights["general"].append(f"{regressed_count} patterns regressed ({pct_regressed:.1f}%)")
                
            if unchanged_count > 0:
                pct_unchanged = (unchanged_count / total_patterns) * 100
                insights["general"].append(f"{unchanged_count} patterns unchanged ({pct_unchanged:.1f}%)")
                
            # Overall trend assessment
            if improved_count > regressed_count * 2:
                insights["general"].append("Overall strong positive pattern change profile")
            elif improved_count > regressed_count:
                insights["general"].append("Overall moderately positive pattern change profile")
            elif regressed_count > improved_count * 2:
                insights["general"].append("Overall strong negative pattern change profile")
            elif regressed_count > improved_count:
                insights["general"].append("Overall moderately negative pattern change profile")
            else:
                insights["general"].append("Overall neutral pattern change profile")
                
        # Category analysis if available
        if categories:
            unique_categories = set(categories)
            insights["general"].append(f"Patterns span {len(unique_categories)} categories")
            
            # Check for category dominance
            category_counts = {}
            for cat in categories:
                category_counts[cat] = category_counts.get(cat, 0) + 1
                
            if category_counts:
                sorted_cats = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
                top_category, top_count = sorted_cats[0]
                
                if top_count > sum(count for cat, count in sorted_cats[1:]) / 2:
                    insights["general"].append(f"'{top_category}' is the dominant category")
                
        # Identify improvement patterns
        if patterns and changes and categories:
            # Zip together for easier analysis
            pattern_data = list(zip(patterns, changes, categories))
            
            # Find top improvements
            improvements = sorted(pattern_data, key=lambda x: x[1], reverse=True)
            
            for pattern, change, category in improvements[:3]:
                if change > 0:
                    insights["improvements"].append(f"{pattern} ({category}): +{change:.3f}")
                    
            # Find top regressions
            regressions = sorted(pattern_data, key=lambda x: x[1])
            
            for pattern, change, category in regressions[:3]:
                if change < 0:
                    insights["regressions"].append(f"{pattern} ({category}): {change:.3f}")
                    
        # Basic recommendations based on general trends
        if "general" in insights and insights["general"]:
            for statement in insights["general"]:
                if "negative pattern change" in statement:
                    insights["recommendations"].append("Review and address patterns showing regression")
                elif "positive pattern change" in statement:
                    insights["recommendations"].append("Document factors contributing to pattern improvements")
                    
        if "regressed_count" in locals() and regressed_count > 0:
            insights["recommendations"].append(f"Investigate the {regressed_count} regressed patterns")
            
        if "dominant category" in str(insights["general"]):
            insights["recommendations"].append(f"Focus analysis on the dominant '{top_category}' category")
            
    except Exception as e:
        logging.error(f"Error generating basic chart insights: {str(e)}")
        insights["general"].append(f"Error generating insights: {str(e)}")
        
    return insights

def extract_chart_metadata(self, chart_data):
    """Extract metadata from chart_data for use in insights
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        dict: Metadata dictionary
    """
    metadata = {
        "title": chart_data.get("title", "Untitled Chart"),
        "subtitle": chart_data.get("subtitle", ""),
        "data_points": 0,
        "categories_count": 0,
        "date_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    
    # Extract data points count
    patterns = chart_data.get("patterns", [])
    metadata["data_points"] = len(patterns)
    
    # Extract categories count
    categories = chart_data.get("categories", [])
    if categories:
        metadata["categories_count"] = len(set(categories))
        
    # Extract min/max values when present
    changes = chart_data.get("changes", [])
    if changes:
        metadata["min_value"] = min(changes)
        metadata["max_value"] = max(changes)
        metadata["mean_value"] = sum(changes) / len(changes) if len(changes) > 0 else 0
        
    return metadata

def generate_trend_summary(self, chart_data):
    """Generate a natural language summary of the trend indicated by the chart data
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        str: Trend summary text
    """
    summary = []
    
    try:
        # Get chart data
        patterns = chart_data.get("patterns", [])
        changes = chart_data.get("changes", [])
        categories = chart_data.get("categories", [])
        
        if not patterns or not changes:
            return "No pattern data available for trend analysis."
        
        # Count improvements, regressions, and unchanged patterns
        improved = sum(1 for c in changes if c > 0)
        regressed = sum(1 for c in changes if c < 0)
        unchanged = sum(1 for c in changes if c == 0)
        total = len(patterns)
        
        if total == 0:
            return "No patterns found for analysis."
        
        # Generate trend summary based on the pattern changes
        if improved > regressed * 2:
            summary.append("The data shows a strong positive trend with significant improvements across most patterns.")
        elif improved > regressed:
            summary.append("The data shows a moderate positive trend with more improvements than regressions.")
        elif regressed > improved * 2:
            summary.append("The data shows a strong negative trend with significant regressions across most patterns.")
        elif regressed > improved:
            summary.append("The data shows a moderate negative trend with more regressions than improvements.")
        else:
            summary.append("The data shows a neutral trend with balanced improvements and regressions.")
            
        # Add specific counts
        summary.append(f"{improved} patterns improved, {regressed} patterns regressed, and {unchanged} patterns remained unchanged.")
        
        # Add category-specific insights if available
        if categories:
            # Create pattern-category-change mapping
            category_changes = {}
            for i, cat in enumerate(categories):
                if i < len(changes):
                    if cat not in category_changes:
                        category_changes[cat] = []
                    category_changes[cat].append(changes[i])
            
            # Calculate category trends
            category_trends = {}
            for cat, cat_changes in category_changes.items():
                improved = sum(1 for c in cat_changes if c > 0)
                regressed = sum(1 for c in cat_changes if c < 0)
                unchanged = sum(1 for c in cat_changes if c == 0)
                
                # Only report significant trends for categories with sufficient data points
                if len(cat_changes) >= 3:
                    if improved > regressed * 2:
                        category_trends[cat] = f"strong positive ({improved} improved, {regressed} regressed)"
                    elif regressed > improved * 2:
                        category_trends[cat] = f"strong negative ({improved} improved, {regressed} regressed)"
                        
            # Report top category trends (limit to 3)
            if category_trends:
                summary.append("Notable category trends:")
                for i, (cat, trend) in enumerate(list(category_trends.items())[:3]):
                    summary.append(f"- {cat}: {trend}")
    
    except Exception as e:
        logging.error(f"Error generating trend summary: {str(e)}")
        summary.append(f"Error generating trend summary: {str(e)}")
    
    return " ".join(summary)

def extract_pattern_correlations(self, chart_data):
    """Extract correlations between patterns from chart data
    
    Args:
        chart_data: Chart data dictionary
        
    Returns:
        list: List of correlation insights
    """
    correlations = []
    
    try:
        # Get pattern data
        patterns = chart_data.get("patterns", [])
        changes = chart_data.get("changes", [])
        categories = chart_data.get("categories", [])
        
        if len(patterns) < 2 or len(changes) < 2:
            return ["Not enough pattern data to analyze correlations."]
        
        # Group patterns by category and change direction
        category_groups = {}
        for i, cat in enumerate(categories):
            if i < len(changes) and i < len(patterns):
                if cat not in category_groups:
                    category_groups[cat] = {"improved": [], "regressed": [], "unchanged": []}
                
                change = changes[i]
                pattern = patterns[i]
                
                if change > 0:
                    category_groups[cat]["improved"].append(pattern)
                elif change < 0:
                    category_groups[cat]["regressed"].append(pattern)
                else:
                    category_groups[cat]["unchanged"].append(pattern)
        
        # Look for categories with clear correlation patterns
        for cat, data in category_groups.items():
            improved = len(data["improved"])
            regressed = len(data["regressed"])
            unchanged = len(data["unchanged"])
            total = improved + regressed + unchanged
            
            # Only consider categories with enough data points
            if total >= 3:
                # Strong improvement correlation
                if improved > total * 0.7:
                    correlations.append(f"Strong correlation of improvements in '{cat}' category ({improved}/{total}, {improved/total*100:.1f}%)")
                
                # Strong regression correlation
                if regressed > total * 0.7:
                    correlations.append(f"Strong correlation of regressions in '{cat}' category ({regressed}/{total}, {regressed/total*100:.1f}%)")
        
        # If we found correlations, add a final insights
        if correlations:
            correlations.append("These correlations suggest systemic factors affecting specific pattern categories.")
        else:
            correlations.append("No strong correlations detected between pattern changes and categories.")
    
    except Exception as e:
        logging.error(f"Error extracting pattern correlations: {str(e)}")
        correlations.append(f"Error analyzing correlations: {str(e)}")
    
    return correlations
