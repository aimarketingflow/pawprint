#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-4: Line Chart Processing

Implements the line chart data processing methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for line chart processing that would be included in the CompareScreen class

def format_line_chart_data(self, base_data):
    """Format data for line chart visualization
    
    Args:
        base_data: Base chart data dictionary
        
    Returns:
        dict: Line chart data dictionary
    """
    # Line charts are used to show trends over time or sequence
    # In pawprint comparison, we can use line charts to show:
    # 1. Score progression across multiple pawprint files
    # 2. Sorted pattern scores to see distribution
    
    # Create data structure for line chart
    line_data = {
        "pattern_names": [],
        "value_series": [],
        "categories": [],
        "timestamps": []
    }
    
    # For line charts, we need time series data
    # If we have multiple files from the same origin, use those
    # Otherwise, just use the before/after values
    
    # Check if we have grouping by origin
    has_time_series = False
    
    for origin, files in self.file_groups.items():
        if len(files) >= 2:
            has_time_series = True
            break
    
    if has_time_series:
        # Get all unique pattern keys from all files
        all_pattern_keys = set()
        for diff_key, diff_data in self.diff_cache.items():
            pattern_changes = diff_data.get("pattern_changes", [])
            for pattern in pattern_changes:
                all_pattern_keys.add(pattern.get("key", ""))
        
        # For each unique pattern, collect scores across all files
        for pattern_key in all_pattern_keys:
            # Get pattern name and category
            pattern_name = pattern_key.split(".")[-1]
            pattern_category = "Unknown"
            
            # Series data for this pattern
            series_data = []
            timestamps = []
            
            # Check each file for this pattern
            for origin, files in self.file_groups.items():
                for file_info in files:
                    # Extract pattern data if available
                    data = file_info.get("data", {})
                    pattern_data = data.get("patterns", {}).get(pattern_key, {})
                    
                    if pattern_data:
                        # Get score and timestamp
                        score = pattern_data.get("score", 0.0)
                        timestamp = data.get("metadata", {}).get("timestamp", "")
                        
                        # Update category if available
                        if "category" in pattern_data:
                            pattern_category = pattern_data["category"]
                        
                        # Add to series
                        series_data.append(score)
                        timestamps.append(timestamp)
            
            # Only add patterns that have multiple data points
            if len(series_data) >= 2:
                line_data["pattern_names"].append(pattern_name)
                line_data["value_series"].append(series_data)
                line_data["categories"].append(pattern_category)
                if not line_data["timestamps"]:
                    line_data["timestamps"] = timestamps
    else:
        # Just use before/after data for each pattern
        for i, pattern_name in enumerate(base_data["pattern_names"]):
            # Only include patterns with significant change
            if abs(base_data["changes"][i]) > 0.01:
                line_data["pattern_names"].append(pattern_name)
                line_data["value_series"].append([
                    base_data["before_scores"][i],
                    base_data["after_scores"][i]
                ])
                line_data["categories"].append(base_data["categories"][i])
        
        # Set timestamps to "Before" and "After"
        line_data["timestamps"] = ["Before", "After"]
    
    # Sort patterns by category
    if line_data["pattern_names"]:
        # Create indices and sort by category
        indices = list(range(len(line_data["pattern_names"])))
        indices.sort(key=lambda i: line_data["categories"][i])
        
        # Apply sorting
        line_data["pattern_names"] = [line_data["pattern_names"][i] for i in indices]
        line_data["value_series"] = [line_data["value_series"][i] for i in indices]
        line_data["categories"] = [line_data["categories"][i] for i in indices]
    
    # Add metadata
    line_data["title"] = "Pattern Score Progression"
    line_data["subtitle"] = f"Showing {len(line_data['pattern_names'])} patterns over time"
    line_data["has_time_series"] = has_time_series
    
    return line_data

def draw_line_chart(self, chart_data):
    """Draw line chart on the canvas
    
    Args:
        chart_data: Line chart data dictionary
    """
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Clear previous figure
    self.chart_figure.clear()
    
    # Create subplot
    ax = self.chart_figure.add_subplot(111)
    
    # Get data
    pattern_names = chart_data.get("pattern_names", [])
    value_series = chart_data.get("value_series", [])
    categories = chart_data.get("categories", [])
    timestamps = chart_data.get("timestamps", [])
    
    # Handle empty data
    if not pattern_names or not value_series:
        ax.text(0.5, 0.5, "No data available for line chart", 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        self.chart_canvas.draw()
        return
    
    # Get unique categories for coloring
    unique_categories = list(set(categories))
    
    # Create color map for categories
    cmap = plt.cm.get_cmap('tab10', len(unique_categories))
    category_colors = {cat: cmap(i) for i, cat in enumerate(unique_categories)}
    
    # Determine x-axis values
    x_values = list(range(len(timestamps)))
    
    # Plot lines for each pattern
    for i, pattern_name in enumerate(pattern_names):
        # Get series data
        series = value_series[i]
        category = categories[i]
        color = category_colors[category]
        
        # Skip if not enough data points
        if len(series) < 2:
            continue
        
        # Plot line
        ax.plot(x_values[:len(series)], series, marker='o', 
                label=f"{pattern_name} ({category})", alpha=0.7, color=color)
    
    # Set labels and title
    ax.set_title(chart_data["title"])
    ax.set_xlabel('Time')
    ax.set_ylabel('Pattern Score')
    
    # Set x-tick labels
    ax.set_xticks(x_values)
    
    # Format timestamps if they look like ISO dates
    formatted_timestamps = []
    for ts in timestamps:
        try:
            # Try to parse as ISO date
            dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            formatted_timestamps.append(dt.strftime('%Y-%m-%d'))
        except (ValueError, TypeError):
            # If not a valid date, use as is
            formatted_timestamps.append(ts)
    
    ax.set_xticklabels(formatted_timestamps, rotation=45, ha='right')
    
    # Add legend (only show if reasonable number of patterns)
    if len(pattern_names) <= 10:
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    else:
        # Group legend by category
        legend_entries = []
        for cat in unique_categories:
            legend_entries.append(mpatches.Patch(color=category_colors[cat], label=cat))
        ax.legend(handles=legend_entries, loc='upper right', bbox_to_anchor=(1.15, 1))
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # Adjust layout for rotated labels and legend
    self.chart_figure.tight_layout()
    
    # Draw the updated chart
    self.chart_canvas.draw()

def get_line_chart_description(self, chart_data):
    """Generate HTML description for line chart
    
    Args:
        chart_data: Line chart data dictionary
        
    Returns:
        str: HTML-formatted description
    """
    # Start with chart overview
    html = f"<h3>{chart_data.get('title', 'Pattern Score Progression')}</h3>"
    html += f"<p>{chart_data.get('subtitle', 'Pattern scores over time')}</p>"
    
    # Extract data
    pattern_names = chart_data.get("pattern_names", [])
    value_series = chart_data.get("value_series", [])
    categories = chart_data.get("categories", [])
    timestamps = chart_data.get("timestamps", [])
    has_time_series = chart_data.get("has_time_series", False)
    
    if not pattern_names or not value_series:
        return html + "<p>No data available for analysis.</p>"
    
    # Calculate trend information
    trends = []
    for i, pattern_name in enumerate(pattern_names):
        series = value_series[i]
        category = categories[i]
        
        # Skip if not enough data points
        if len(series) < 2:
            continue
            
        # Calculate trend
        first_val = series[0]
        last_val = series[-1]
        overall_change = last_val - first_val
        
        trends.append({
            "pattern": pattern_name,
            "category": category,
            "first": first_val,
            "last": last_val,
            "change": overall_change,
            "percent_change": (overall_change / first_val * 100) if first_val > 0 else 0.0
        })
    
    # Sort trends by absolute change
    trends.sort(key=lambda x: abs(x["change"]), reverse=True)
    
    # Add summary section
    html += "<h4>Trend Summary:</h4>"
    
    # Timestamp range
    if has_time_series:
        html += f"<p>Time range: {timestamps[0]} to {timestamps[-1]}</p>"
    else:
        html += "<p>Comparing before and after states</p>"
    
    # Count improvements and regressions
    improved = [t for t in trends if t["change"] > 0]
    regressed = [t for t in trends if t["change"] < 0]
    unchanged = [t for t in trends if t["change"] == 0]
    
    html += f"<p>Out of {len(trends)} patterns with trend data:</p>"
    html += "<ul>"
    html += f"<li><span style='color:green'>Improved:</span> {len(improved)} patterns</li>"
    html += f"<li><span style='color:red'>Regressed:</span> {len(regressed)} patterns</li>"
    html += f"<li><span style='color:blue'>Unchanged:</span> {len(unchanged)} patterns</li>"
    html += "</ul>"
    
    # Add insights
    html += "<h4>Key Insights:</h4><ul>"
    
    # Patterns with consistent improvement
    consistent_improvement = []
    for i, pattern_name in enumerate(pattern_names):
        series = value_series[i]
        
        # Skip if not enough data points
        if len(series) < 3:
            continue
            
        # Check if consistently increasing
        consistent = True
        for j in range(1, len(series)):
            if series[j] < series[j-1]:
                consistent = False
                break
                
        if consistent and (series[-1] - series[0]) > 0.05:
            consistent_improvement.append((pattern_name, series[-1] - series[0]))
    
    if consistent_improvement:
        # Sort by improvement amount
        consistent_improvement.sort(key=lambda x: x[1], reverse=True)
        
        html += "<li><span style='color:green'>Consistently improving</span> patterns:"
        html += "<ul>"
        for name, change in consistent_improvement[:3]:  # Show top 3
            html += f"<li>{name} (+{change:.2f})</li>"
        html += "</ul></li>"
    
    # Patterns with consistent regression
    consistent_regression = []
    for i, pattern_name in enumerate(pattern_names):
        series = value_series[i]
        
        # Skip if not enough data points
        if len(series) < 3:
            continue
            
        # Check if consistently decreasing
        consistent = True
        for j in range(1, len(series)):
            if series[j] > series[j-1]:
                consistent = False
                break
                
        if consistent and (series[0] - series[-1]) > 0.05:
            consistent_regression.append((pattern_name, series[0] - series[-1]))
    
    if consistent_regression:
        # Sort by regression amount
        consistent_regression.sort(key=lambda x: x[1], reverse=True)
        
        html += "<li><span style='color:red'>Consistently declining</span> patterns:"
        html += "<ul>"
        for name, change in consistent_regression[:3]:  # Show top 3
            html += f"<li>{name} (-{change:.2f})</li>"
        html += "</ul></li>"
    
    # Category trends
    category_trends = {}
    for trend in trends:
        cat = trend["category"]
        if cat not in category_trends:
            category_trends[cat] = []
        category_trends[cat].append(trend["change"])
    
    # Calculate average change by category
    cat_avg_changes = {}
    for cat, changes in category_trends.items():
        cat_avg_changes[cat] = sum(changes) / len(changes)
    
    # Sort categories by average change
    sorted_cats = sorted(cat_avg_changes.items(), key=lambda x: x[1], reverse=True)
    
    # Show top improved and regressed categories
    if sorted_cats:
        best_cat, best_avg = sorted_cats[0]
        if best_avg > 0:
            html += f"<li>Best performing category: <b>{best_cat}</b> (avg. +{best_avg:.2f})</li>"
        
        worst_cat, worst_avg = sorted_cats[-1]
        if worst_avg < 0:
            html += f"<li>Worst performing category: <b>{worst_cat}</b> (avg. {worst_avg:.2f})</li>"
    
    html += "</ul>"
    
    # Add recommendations
    html += "<h4>Recommendations:</h4><ul>"
    if regressed:
        html += "<li>Investigate patterns showing negative trends</li>"
    if consistent_regression:
        html += f"<li>Prioritize addressing the {consistent_regression[0][0]} pattern showing consistent decline</li>"
    if consistent_improvement:
        html += f"<li>Analyze factors contributing to consistent improvement in {consistent_improvement[0][0]}</li>"
    html += "</ul>"
    
    return html
