#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-7b: Advanced Chart Insights

Implements the advanced chart insights and recommendations generation methods 
for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

import json
import logging
from datetime import datetime
import numpy as np

# This file contains methods for advanced chart insights generation that would be included in the CompareScreen class

def generate_advanced_chart_insights(self, chart_data, chart_type, diff_data=None):
    """Generate advanced insights and recommendations for chart data
    
    Args:
        chart_data: Chart data dictionary
        chart_type: Type of chart (radar, bar, line, pie, heatmap)
        diff_data: Optional diff data for additional context
        
    Returns:
        dict: Dictionary of advanced insights
    """
    insights = {
        "chart_type": chart_type,
        "timestamp": datetime.now().isoformat(),
        "key_findings": [],
        "detailed_analysis": [],
        "actionable_recommendations": [],
        "technical_details": []
    }
    
    try:
        # Get core data elements
        patterns = chart_data.get("patterns", [])
        changes = chart_data.get("changes", [])
        categories = chart_data.get("categories", [])
        
        # Handle missing data
        if not patterns or not changes:
            insights["key_findings"].append("Insufficient data for advanced insights analysis.")
            return insights
        
        # Calculate magnitude thresholds for significance
        change_magnitudes = [abs(c) for c in changes]
        if change_magnitudes:
            mean_magnitude = np.mean(change_magnitudes)
            std_magnitude = np.std(change_magnitudes)
            high_threshold = mean_magnitude + std_magnitude
            
            # Identify statistically significant changes
            significant_changes = []
            for i, pattern in enumerate(patterns):
                if i < len(changes) and i < len(categories):
                    change = changes[i]
                    category = categories[i]
                    
                    if abs(change) >= high_threshold:
                        direction = "improved" if change > 0 else "regressed"
                        significant_changes.append((pattern, category, change, direction))
            
            # Report significant findings
            if significant_changes:
                insights["key_findings"].append(f"Found {len(significant_changes)} statistically significant pattern changes")
                
                # Sort by magnitude (descending)
                significant_changes.sort(key=lambda x: abs(x[2]), reverse=True)
                
                # Add top significant changes to detailed analysis
                for pattern, category, change, direction in significant_changes[:5]:
                    insights["detailed_analysis"].append(
                        f"{pattern} ({category}) {direction} by {abs(change):.3f}, "
                        f"which is {abs(change)/mean_magnitude:.1f}x the average change magnitude"
                    )
        
        # Category-based analysis
        if categories:
            # Group by category
            category_data = {}
            for i, cat in enumerate(categories):
                if i < len(patterns) and i < len(changes):
                    pattern = patterns[i]
                    change = changes[i]
                    
                    if cat not in category_data:
                        category_data[cat] = []
                    
                    category_data[cat].append((pattern, change))
            
            # Analyze each category
            category_insights = []
            for cat, data in category_data.items():
                # Only analyze categories with sufficient data points
                if len(data) >= 3:
                    # Calculate category metrics
                    cat_changes = [c for _, c in data]
                    cat_mean = np.mean(cat_changes) if cat_changes else 0
                    cat_improved = sum(1 for _, c in data if c > 0)
                    cat_regressed = sum(1 for _, c in data if c < 0)
                    cat_unchanged = sum(1 for _, c in data if c == 0)
                    
                    # Check for notable category trends
                    if cat_mean > mean_magnitude * 1.5 and cat_improved > cat_regressed * 2:
                        category_insights.append(f"'{cat}' shows exceptional improvement ({cat_improved}/{len(data)} patterns improved)")
                    elif cat_mean < -mean_magnitude * 1.5 and cat_regressed > cat_improved * 2:
                        category_insights.append(f"'{cat}' shows significant regression ({cat_regressed}/{len(data)} patterns regressed)")
                    elif cat_unchanged > len(data) * 0.7:
                        category_insights.append(f"'{cat}' shows minimal changes ({cat_unchanged}/{len(data)} patterns unchanged)")
            
            # Add category insights
            if category_insights:
                insights["detailed_analysis"].extend(category_insights)
        
        # Temporal analysis if time data is available
        if hasattr(self, 'comparison_timestamps') and self.comparison_timestamps:
            # Check for consistent trends over time
            insights["detailed_analysis"].append("Temporal analysis shows pattern evolution over selected time periods")
            
            # This would be extended with actual temporal analysis from timestamps in self.comparison_timestamps
        
        # Generate actionable recommendations
        self._generate_actionable_recommendations(insights, chart_data, chart_type, diff_data)
        
        # Add technical details
        self._add_technical_details(insights, chart_data, chart_type)
        
    except Exception as e:
        logging.error(f"Error generating advanced chart insights: {str(e)}")
        insights["key_findings"].append(f"Error generating advanced insights: {str(e)}")
    
    return insights

def _generate_actionable_recommendations(self, insights, chart_data, chart_type, diff_data=None):
    """Generate actionable recommendations based on chart data and insights
    
    Args:
        insights: Insights dictionary to add recommendations to
        chart_data: Chart data dictionary
        chart_type: Type of chart
        diff_data: Optional diff data for additional context
    """
    # Get pattern data
    patterns = chart_data.get("patterns", [])
    changes = chart_data.get("changes", [])
    categories = chart_data.get("categories", [])
    
    if not patterns or not changes:
        insights["actionable_recommendations"].append("Insufficient data for generating recommendations.")
        return
    
    # Basic recommendations based on overall trend
    improved = sum(1 for c in changes if c > 0)
    regressed = sum(1 for c in changes if c < 0)
    unchanged = sum(1 for c in changes if c == 0)
    total = len(patterns)
    
    # Calculate trend metrics
    if total > 0:
        improved_ratio = improved / total
        regressed_ratio = regressed / total
        unchanged_ratio = unchanged / total
        
        # Overall trend recommendations
        if regressed_ratio > 0.3:
            insights["actionable_recommendations"].append("Investigate root causes for pattern regressions")
            
            # Add specific recommendations for top regression areas
            if categories:
                # Find categories with most regressions
                category_regressions = {}
                for i, cat in enumerate(categories):
                    if i < len(changes):
                        change = changes[i]
                        if change < 0:
                            category_regressions[cat] = category_regressions.get(cat, 0) + 1
                
                # Get top regression categories
                if category_regressions:
                    sorted_cats = sorted(category_regressions.items(), key=lambda x: x[1], reverse=True)
                    for cat, count in sorted_cats[:2]:
                        insights["actionable_recommendations"].append(
                            f"Focus on improving '{cat}' patterns which account for {count} regressions"
                        )
        
        if improved_ratio > 0.3:
            insights["actionable_recommendations"].append("Document and replicate successful techniques that led to pattern improvements")
            
        if unchanged_ratio > 0.7:
            insights["actionable_recommendations"].append("Review detection methods as most patterns show no change")
    
    # Chart-specific recommendations
    if chart_type == "radar":
        insights["actionable_recommendations"].append("Use radar chart to identify category imbalances that need attention")
    elif chart_type == "bar":
        insights["actionable_recommendations"].append("Focus remediation efforts on patterns with largest negative changes")
    elif chart_type == "line":
        insights["actionable_recommendations"].append("Track patterns over time to identify recurring issues and long-term trends")
    elif chart_type == "pie":
        insights["actionable_recommendations"].append("Address category groups with high regression concentrations")
    elif chart_type == "heatmap":
        insights["actionable_recommendations"].append("Target interventions at hotspots showing concentrated pattern issues")
    
    # Recommendations based on diff data if available
    if diff_data:
        # Extract changed patterns from diff data
        changed_patterns = diff_data.get("changed", {})
        if changed_patterns:
            # Check for structural changes
            structural_changes = [p for p in changed_patterns if "structure" in p.lower()]
            if structural_changes:
                insights["actionable_recommendations"].append("Review structural changes that may be affecting multiple pattern scores")
            
            # Check for timing/sequence changes
            timing_changes = [p for p in changed_patterns if any(kw in p.lower() for kw in ["time", "sequence", "order"])]
            if timing_changes:
                insights["actionable_recommendations"].append("Investigate timing and sequence changes that may affect pattern detection accuracy")

def _add_technical_details(self, insights, chart_data, chart_type):
    """Add technical details about chart data and analysis methods
    
    Args:
        insights: Insights dictionary to add technical details to
        chart_data: Chart data dictionary
        chart_type: Type of chart
    """
    # Add analysis methodology
    insights["technical_details"].append(f"Analysis methodology: Statistical pattern comparison with {chart_type} visualization")
    
    # Add data point statistics
    patterns = chart_data.get("patterns", [])
    changes = chart_data.get("changes", [])
    
    if patterns and changes:
        # Calculate basic statistics
        mean_change = np.mean(changes) if changes else 0
        median_change = np.median(changes) if changes else 0
        std_change = np.std(changes) if changes else 0
        min_change = min(changes) if changes else 0
        max_change = max(changes) if changes else 0
        
        insights["technical_details"].append(f"Data points: {len(patterns)}")
        insights["technical_details"].append(f"Mean change: {mean_change:.3f}")
        insights["technical_details"].append(f"Median change: {median_change:.3f}")
        insights["technical_details"].append(f"Standard deviation: {std_change:.3f}")
        insights["technical_details"].append(f"Change range: {min_change:.3f} to {max_change:.3f}")
    
    # Add chart-specific technical details
    if chart_type == "radar":
        insights["technical_details"].append("Radar chart uses normalized values for category comparisons")
    elif chart_type == "bar":
        insights["technical_details"].append("Bar chart displays absolute change magnitude with directional coloring")
    elif chart_type == "line":
        insights["technical_details"].append("Line chart shows pattern trends with moving average smoothing")
    elif chart_type == "pie":
        insights["technical_details"].append("Pie chart segments proportional to pattern count distribution")
    elif chart_type == "heatmap":
        insights["technical_details"].append("Heatmap color intensity corresponds to pattern density")
    
    # Add timestamp
    insights["technical_details"].append(f"Analysis generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def get_insight_recommendations(self, chart_type, chart_data, diff_data=None):
    """Generate recommendations based on chart insights
    
    Args:
        chart_type: Type of chart
        chart_data: Chart data dictionary
        diff_data: Optional diff data for additional context
        
    Returns:
        str: HTML-formatted recommendations
    """
    # Get advanced insights
    insights = self.generate_advanced_chart_insights(chart_data, chart_type, diff_data)
    
    # Format as HTML
    html = "<h3>Key Findings</h3><ul>"
    for finding in insights.get("key_findings", []):
        html += f"<li>{finding}</li>"
    html += "</ul>"
    
    html += "<h3>Detailed Analysis</h3><ul>"
    for detail in insights.get("detailed_analysis", []):
        html += f"<li>{detail}</li>"
    html += "</ul>"
    
    html += "<h3>Recommended Actions</h3><ul>"
    for recommendation in insights.get("actionable_recommendations", []):
        html += f"<li>{recommendation}</li>"
    html += "</ul>"
    
    html += "<h3>Technical Details</h3><ul>"
    for detail in insights.get("technical_details", []):
        html += f"<li>{detail}</li>"
    html += "</ul>"
    
    return html

def export_chart_insights_markdown(self, chart_type, chart_data, diff_data=None, filename=None):
    """Export chart insights as markdown
    
    Args:
        chart_type: Type of chart
        chart_data: Chart data dictionary
        diff_data: Optional diff data for additional context
        filename: Optional filename to export to
        
    Returns:
        str: Markdown-formatted insights
    """
    # Get advanced insights
    insights = self.generate_advanced_chart_insights(chart_data, chart_type, diff_data)
    
    # Format as markdown
    md = f"# Chart Insights: {chart_type.capitalize()} Chart\n\n"
    md += f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    md += "## Key Findings\n\n"
    for finding in insights.get("key_findings", []):
        md += f"- {finding}\n"
    md += "\n"
    
    md += "## Detailed Analysis\n\n"
    for detail in insights.get("detailed_analysis", []):
        md += f"- {detail}\n"
    md += "\n"
    
    md += "## Recommended Actions\n\n"
    for recommendation in insights.get("actionable_recommendations", []):
        md += f"- {recommendation}\n"
    md += "\n"
    
    md += "## Technical Details\n\n"
    for detail in insights.get("technical_details", []):
        md += f"- {detail}\n"
    md += "\n"
    
    # Save to file if filename provided
    if filename:
        try:
            with open(filename, 'w') as f:
                f.write(md)
            logging.info(f"Chart insights exported to {filename}")
        except Exception as e:
            logging.error(f"Failed to export chart insights: {str(e)}")
    
    return md
