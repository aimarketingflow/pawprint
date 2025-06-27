#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-3: Bar Chart Processing

Implements the bar chart data processing methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for bar chart processing that would be included in the CompareScreen class

def format_bar_chart_data(self, base_data):
    """Format data for bar chart visualization
    
    Args:
        base_data: Base chart data dictionary
        
    Returns:
        dict: Bar chart data dictionary
    """
    # Bar charts can handle more items than radar charts
    # but still need to limit for readability
    max_items = 15
    
    # Create data structure for bar chart
    bar_data = {
        "pattern_names": [],
        "before_values": [],
        "after_values": [],
        "changes": [],
        "categories": [],
        "colors": []
    }
    
    # Sort patterns by absolute change magnitude
    indices = list(range(len(base_data["patterns"])))
    indices.sort(key=lambda i: abs(base_data["changes"][i]), reverse=True)
    
    # Take top N patterns by change magnitude
    count = 0
    for i in indices:
        if count >= max_items:
            break
            
        # Add pattern data
        pattern_name = base_data["pattern_names"][i]
        before_score = base_data["before_scores"][i]
        after_score = base_data["after_scores"][i]
        change = base_data["changes"][i]
        category = base_data["categories"][i]
        
        # Add to bar data
        bar_data["pattern_names"].append(pattern_name)
        bar_data["before_values"].append(before_score)
        bar_data["after_values"].append(after_score)
        bar_data["changes"].append(change)
        bar_data["categories"].append(category)
        
        # Determine color based on change
        if change > 0:
            bar_data["colors"].append("#4CAF50")  # Green for improvement
        elif change < 0:
            bar_data["colors"].append("#F44336")  # Red for regression
        else:
            bar_data["colors"].append("#2196F3")  # Blue for unchanged
            
        count += 1
    
    # Add metadata
    bar_data["title"] = "Pattern Score Changes"
    bar_data["subtitle"] = f"Top {len(bar_data['pattern_names'])} patterns by change magnitude"
    
    return bar_data

def draw_bar_chart(self, chart_data):
    """Draw bar chart on the canvas
    
    Args:
        chart_data: Bar chart data dictionary
    """
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Clear previous figure
    self.chart_figure.clear()
    
    # Create subplot
    ax = self.chart_figure.add_subplot(111)
    
    # Get data
    pattern_names = chart_data.get("pattern_names", [])
    before_values = chart_data.get("before_values", [])
    after_values = chart_data.get("after_values", [])
    changes = chart_data.get("changes", [])
    colors = chart_data.get("colors", [])
    
    # Handle empty data
    if not pattern_names:
        ax.text(0.5, 0.5, "No data available for bar chart", 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        self.chart_canvas.draw()
        return
    
    # Create positions for bars
    positions = np.arange(len(pattern_names))
    width = 0.35
    
    # Create bars for before and after scores
    ax.bar(positions - width/2, before_values, width, label='Before', color='#3388cc', alpha=0.7)
    ax.bar(positions + width/2, after_values, width, label='After', color='#cc3388', alpha=0.7)
    
    # Add change indicators
    for i, change in enumerate(changes):
        if change > 0:
            ax.annotate(f"+{change:.2f}", 
                     xy=(positions[i], max(before_values[i], after_values[i]) + 0.02),
                     ha='center', va='bottom', color='green')
        elif change < 0:
            ax.annotate(f"{change:.2f}", 
                     xy=(positions[i], max(before_values[i], after_values[i]) + 0.02),
                     ha='center', va='bottom', color='red')
    
    # Set labels and title
    ax.set_title(chart_data["title"])
    ax.set_xlabel('Patterns')
    ax.set_ylabel('Score')
    
    # Set y-axis range to start from 0
    ax.set_ylim(0, max(max(before_values, default=0), max(after_values, default=0)) * 1.2)
    
    # Set x-tick labels
    ax.set_xticks(positions)
    
    # If we have many patterns, rotate labels for readability
    if len(pattern_names) > 5:
        shortened_names = [name[:15] + '...' if len(name) > 15 else name for name in pattern_names]
        ax.set_xticklabels(shortened_names, rotation=45, ha='right')
    else:
        ax.set_xticklabels(pattern_names)
    
    # Add legend
    ax.legend()
    
    # Adjust layout for rotated labels
    self.chart_figure.tight_layout()
    
    # Draw the updated chart
    self.chart_canvas.draw()

def get_bar_chart_description(self, chart_data):
    """Generate HTML description for bar chart
    
    Args:
        chart_data: Bar chart data dictionary
        
    Returns:
        str: HTML-formatted description
    """
    # Start with chart overview
    html = f"<h3>{chart_data.get('title', 'Pattern Score Changes')}</h3>"
    html += f"<p>{chart_data.get('subtitle', 'Changes in pattern scores')}</p>"
    
    # Extract data
    pattern_names = chart_data.get("pattern_names", [])
    before_values = chart_data.get("before_values", [])
    after_values = chart_data.get("after_values", [])
    changes = chart_data.get("changes", [])
    
    if not pattern_names:
        return html + "<p>No data available for analysis.</p>"
    
    # Calculate statistics
    improved_count = sum(1 for change in changes if change > 0)
    regressed_count = sum(1 for change in changes if change < 0)
    unchanged_count = sum(1 for change in changes if change == 0)
    
    avg_change = sum(changes) / len(changes) if changes else 0
    
    # Find largest improvement and regression
    largest_improvement = max(changes) if changes else 0
    largest_improvement_idx = changes.index(largest_improvement) if largest_improvement > 0 else -1
    
    largest_regression = min(changes) if changes else 0
    largest_regression_idx = changes.index(largest_regression) if largest_regression < 0 else -1
    
    # Add summary stats
    html += "<h4>Summary Statistics:</h4>"
    html += f"<p>Showing {len(pattern_names)} patterns:</p>"
    html += "<ul>"
    html += f"<li><span style='color:green'>Improved:</span> {improved_count} patterns</li>"
    html += f"<li><span style='color:red'>Regressed:</span> {regressed_count} patterns</li>"
    html += f"<li><span style='color:blue'>Unchanged:</span> {unchanged_count} patterns</li>"
    html += f"<li>Average change: <span style='color:{'green' if avg_change > 0 else 'red' if avg_change < 0 else 'blue'}'>{avg_change:.2f}</span></li>"
    html += "</ul>"
    
    # Add insights
    html += "<h4>Key Insights:</h4><ul>"
    
    # Largest improvement
    if largest_improvement > 0:
        pattern_name = pattern_names[largest_improvement_idx]
        before_score = before_values[largest_improvement_idx]
        after_score = after_values[largest_improvement_idx]
        
        html += f"<li>Largest <span style='color:green'>improvement</span>: <b>{pattern_name}</b> "
        html += f"increased from {before_score:.2f} to {after_score:.2f} (+{largest_improvement:.2f})</li>"
    
    # Largest regression
    if largest_regression < 0:
        pattern_name = pattern_names[largest_regression_idx]
        before_score = before_values[largest_regression_idx]
        after_score = after_values[largest_regression_idx]
        
        html += f"<li>Largest <span style='color:red'>regression</span>: <b>{pattern_name}</b> "
        html += f"decreased from {before_score:.2f} to {after_score:.2f} ({largest_regression:.2f})</li>"
    
    # Overall trend
    if improved_count > regressed_count:
        html += f"<li>Overall <span style='color:green'>positive trend</span> with {improved_count} improvements vs. {regressed_count} regressions</li>"
    elif regressed_count > improved_count:
        html += f"<li>Overall <span style='color:red'>negative trend</span> with {regressed_count} regressions vs. {improved_count} improvements</li>"
    else:
        html += f"<li>Balanced changes with {improved_count} improvements and {regressed_count} regressions</li>"
    
    html += "</ul>"
    
    # Add recommendations
    html += "<h4>Recommendations:</h4><ul>"
    if regressed_count > 0:
        html += "<li>Investigate patterns showing significant regressions</li>"
    if improved_count > 0:
        html += "<li>Identify factors behind the biggest improvements</li>"
    html += "<li>Use the pattern detail view for deeper analysis of individual changes</li>"
    html += "</ul>"
    
    return html
