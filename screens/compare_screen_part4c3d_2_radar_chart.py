#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-2: Radar Chart Processing

Implements the radar chart data processing methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for radar chart processing that would be included in the CompareScreen class

def format_radar_chart_data(self, base_data):
    """Format data for radar chart visualization
    
    Args:
        base_data: Base chart data dictionary
        
    Returns:
        dict: Radar chart data dictionary
    """
    # Radar charts work best with a limited number of categories
    # Group data by categories and take top N scores from each
    
    # Get all unique categories
    all_categories = list(set(base_data["categories"]))
    
    # Limit to top 8 categories max for radar chart readability
    if len(all_categories) > 8:
        # Sort categories by number of patterns
        category_counts = {cat: 0 for cat in all_categories}
        for cat in base_data["categories"]:
            category_counts[cat] = category_counts.get(cat, 0) + 1
            
        # Sort categories by count
        sorted_categories = sorted(
            category_counts.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Take top 8
        all_categories = [cat for cat, _ in sorted_categories[:8]]
    
    # Create data structure for radar chart
    radar_data = {
        "categories": all_categories,
        "before_values": [],
        "after_values": [],
        "avg_changes": []
    }
    
    # Calculate average scores per category
    for category in all_categories:
        # Get patterns in this category
        cat_patterns = [
            p for i, p in enumerate(base_data["patterns"])
            if base_data["categories"][i] == category
        ]
        
        # Calculate averages
        if cat_patterns:
            avg_before = sum(p.get("before_score", 0.0) for p in cat_patterns) / len(cat_patterns)
            avg_after = sum(p.get("after_score", 0.0) for p in cat_patterns) / len(cat_patterns)
            avg_change = sum(p.get("change", 0.0) for p in cat_patterns) / len(cat_patterns)
        else:
            avg_before = 0.0
            avg_after = 0.0
            avg_change = 0.0
        
        # Add to radar data
        radar_data["before_values"].append(avg_before)
        radar_data["after_values"].append(avg_after)
        radar_data["avg_changes"].append(avg_change)
    
    # Add metadata
    radar_data["title"] = "Pattern Score Comparison by Category"
    radar_data["subtitle"] = f"Comparing {len(base_data['patterns'])} patterns across {len(all_categories)} categories"
    
    return radar_data

def draw_radar_chart(self, chart_data):
    """Draw radar chart on the canvas
    
    Args:
        chart_data: Radar chart data dictionary
    """
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Clear previous figure
    self.chart_figure.clear()
    
    # Create polar projection for radar chart
    ax = self.chart_figure.add_subplot(111, polar=True)
    
    # Get data
    categories = chart_data["categories"]
    before_values = chart_data["before_values"]
    after_values = chart_data["after_values"]
    
    # Number of variables
    N = len(categories)
    
    # Handle empty data
    if N == 0:
        ax.text(0.5, 0.5, "No data available for radar chart", 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        self.chart_canvas.draw()
        return
    
    # What will be the angle of each axis in the plot
    # (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]  # Close the loop
    
    # Extend the values to close the loop
    before_values_plot = before_values + [before_values[0]]
    after_values_plot = after_values + [after_values[0]]
    
    # Draw both lines
    ax.plot(angles, before_values_plot, linewidth=1, linestyle='solid', 
            label='Before', color='#3388cc')
    ax.fill(angles, before_values_plot, alpha=0.1, color='#3388cc')
    
    ax.plot(angles, after_values_plot, linewidth=1, linestyle='solid', 
            label='After', color='#cc3388')
    ax.fill(angles, after_values_plot, alpha=0.1, color='#cc3388')
    
    # Fix axis to go in the right order and start at 12 o'clock
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Add title
    self.chart_figure.suptitle(chart_data["title"], fontsize=12)
    
    # Draw the updated chart
    self.chart_canvas.draw()

def get_radar_chart_description(self, chart_data):
    """Generate HTML description for radar chart
    
    Args:
        chart_data: Radar chart data dictionary
        
    Returns:
        str: HTML-formatted description
    """
    # Start with chart overview
    html = f"<h3>{chart_data['title']}</h3>"
    html += f"<p>{chart_data['subtitle']}</p>"
    
    # Calculate overall changes
    categories = chart_data["categories"]
    before_values = chart_data["before_values"]
    after_values = chart_data["after_values"]
    avg_changes = chart_data["avg_changes"]
    
    if not categories:
        return html + "<p>No data available for analysis.</p>"
    
    # Find biggest improvements and regressions
    improvements = []
    regressions = []
    
    for i, category in enumerate(categories):
        change = avg_changes[i]
        if change > 0:
            improvements.append((category, change))
        elif change < 0:
            regressions.append((category, change))
    
    # Sort by magnitude
    improvements.sort(key=lambda x: x[1], reverse=True)
    regressions.sort(key=lambda x: x[1])
    
    # Add insights
    html += "<h4>Key Insights:</h4><ul>"
    
    # Overall average change
    avg_overall_change = sum(avg_changes) / len(avg_changes) if avg_changes else 0
    if avg_overall_change > 0.01:
        html += f"<li>Overall <span style='color:green'>improvement</span> of {avg_overall_change:.2f} across all categories</li>"
    elif avg_overall_change < -0.01:
        html += f"<li>Overall <span style='color:red'>regression</span> of {abs(avg_overall_change):.2f} across all categories</li>"
    else:
        html += "<li>Overall minimal change across all categories</li>"
    
    # Top improvements
    if improvements:
        top_improvement = improvements[0]
        html += f"<li>Biggest <span style='color:green'>improvement</span> in <b>{top_improvement[0]}</b> category (+{top_improvement[1]:.2f})</li>"
        
        if len(improvements) > 1:
            html += "<li>Other improved categories: "
            other_impr = [f"{cat} (+{change:.2f})" for cat, change in improvements[1:3]]  # Show top 3 max
            html += ", ".join(other_impr)
            if len(improvements) > 3:
                html += f" and {len(improvements)-3} more"
            html += "</li>"
    
    # Top regressions
    if regressions:
        top_regression = regressions[0]
        html += f"<li>Biggest <span style='color:red'>regression</span> in <b>{top_regression[0]}</b> category ({top_regression[1]:.2f})</li>"
        
        if len(regressions) > 1:
            html += "<li>Other regressed categories: "
            other_regr = [f"{cat} ({change:.2f})" for cat, change in regressions[1:3]]  # Show top 3 max
            html += ", ".join(other_regr)
            if len(regressions) > 3:
                html += f" and {len(regressions)-3} more"
            html += "</li>"
    
    html += "</ul>"
    
    # Add recommendations section
    html += "<h4>Recommendations:</h4><ul>"
    
    if regressions:
        html += f"<li>Investigate causes for regression in the <b>{regressions[0][0]}</b> category</li>"
    
    if improvements and regressions:
        html += f"<li>Apply tactics from <b>{improvements[0][0]}</b> to improve other categories</li>"
    
    html += "<li>Use the detailed comparison view to examine specific pattern changes</li>"
    html += "</ul>"
    
    return html
