#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4b: Chart Generation

Implements the chart generation methods for the Charts Tab.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for chart generation that would be included in the CompareScreen class

def update_chart(self, chart_type, category="All Categories", threshold=0.0):
    """Update the current chart based on selected options
    
    Args:
        chart_type: Type of chart to display
        category: Pattern category to filter by
        threshold: Minimum score difference to display
    """
    if not MATPLOTLIB_AVAILABLE:
        logger.warning("Cannot update chart - matplotlib not available")
        return
    
    # Clear previous figure
    self.chart_figure.clear()
    
    # Get chart data filtered by category and threshold
    chart_data = self.get_chart_data(category, threshold)
    
    # Create the appropriate chart
    if chart_type == "Radar Chart":
        self.create_radar_chart(chart_data)
    elif chart_type == "Bar Chart":
        self.create_bar_chart(chart_data)
    elif chart_type == "Pie Chart":
        self.create_pie_chart(chart_data)
    elif chart_type == "Line Chart":
        self.create_line_chart(chart_data)
    elif chart_type == "Heatmap":
        self.create_heatmap_chart(chart_data)
    
    # Draw the updated chart
    self.chart_canvas.draw()
    
    # Update description
    self.update_chart_description(chart_type, chart_data)

def get_chart_data(self, category="All Categories", threshold=0.0):
    """Extract and filter chart data based on category and threshold
    
    Args:
        category: Pattern category to filter by
        threshold: Minimum score difference threshold
        
    Returns:
        Dictionary containing filtered chart data
    """
    # Start with empty chart data structure
    chart_data = {
        "patterns": [],
        "before_scores": [],
        "after_scores": [],
        "differences": [],
        "categories": []
    }
    
    # This would be populated with actual data from comparison_data
    # For now, we'll generate some example data
    example_patterns = [
        {"name": "Directory Structure", "category": "File System", "before": 0.75, "after": 0.82},
        {"name": "File Permissions", "category": "File System", "before": 0.93, "after": 0.87},
        {"name": "Registry Keys", "category": "Registry", "before": 0.68, "after": 0.79},
        {"name": "Network Ports", "category": "Network", "before": 0.81, "after": 0.81},
        {"name": "Process Tree", "category": "Processes", "before": 0.77, "after": 0.91},
        {"name": "User Accounts", "category": "Users & Groups", "before": 0.88, "after": 0.83},
        {"name": "Service Config", "category": "Services", "before": 0.73, "after": 0.75}
    ]
    
    # Filter by category and threshold
    for pattern in example_patterns:
        diff = abs(pattern["after"] - pattern["before"])
        
        # Apply filters
        if (category == "All Categories" or pattern["category"] == category) and diff >= threshold:
            chart_data["patterns"].append(pattern["name"])
            chart_data["before_scores"].append(pattern["before"])
            chart_data["after_scores"].append(pattern["after"])
            chart_data["differences"].append(pattern["after"] - pattern["before"])
            chart_data["categories"].append(pattern["category"])
    
    return chart_data

def create_radar_chart(self, chart_data):
    """Create a radar/spider chart to compare pattern scores
    
    Args:
        chart_data: Dictionary containing chart data
    """
    # Get axis
    ax = self.chart_figure.add_subplot(111, polar=True)
    
    # Get number of patterns (spokes)
    num_patterns = len(chart_data["patterns"])
    if num_patterns < 3:
        # Need at least 3 for a radar chart
        ax.text(0.5, 0.5, "Insufficient data for radar chart", 
                ha='center', va='center', transform=ax.transAxes)
        return
    
    # Set up angles for radar chart
    angles = np.linspace(0, 2*np.pi, num_patterns, endpoint=False).tolist()
    
    # Make the plot circular by repeating the first value
    values_before = chart_data["before_scores"] + [chart_data["before_scores"][0]]
    values_after = chart_data["after_scores"] + [chart_data["after_scores"][0]]
    angles = angles + [angles[0]]
    labels = chart_data["patterns"]
    
    # Plot before scores
    ax.plot(angles, values_before, 'b-', linewidth=1.5, label='Before')
    ax.fill(angles, values_before, 'b', alpha=0.1)
    
    # Plot after scores
    ax.plot(angles, values_after, 'r-', linewidth=1.5, label='After')
    ax.fill(angles, values_after, 'r', alpha=0.1)
    
    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    
    # Set y-axis limits
    ax.set_ylim(0, 1)
    
    # Add legend
    ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    # Set title
    self.chart_figure.suptitle("Pattern Score Comparison (Radar Chart)", fontsize=14)

def create_bar_chart(self, chart_data):
    """Create a bar chart comparing before/after pattern scores
    
    Args:
        chart_data: Dictionary containing chart data
    """
    # Get axis
    ax = self.chart_figure.add_subplot(111)
    
    # Set up positions
    patterns = chart_data["patterns"]
    num_patterns = len(patterns)
    bar_width = 0.35
    x = np.arange(num_patterns)
    
    # Create bars
    before_bars = ax.bar(x - bar_width/2, chart_data["before_scores"], bar_width, 
                         label='Before', color='#3366cc', alpha=0.8)
    after_bars = ax.bar(x + bar_width/2, chart_data["after_scores"], bar_width, 
                        label='After', color='#cc3366', alpha=0.8)
    
    # Add labels and title
    ax.set_xlabel('Patterns')
    ax.set_ylabel('Score (0-1)')
    ax.set_title('Pattern Score Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(patterns, rotation=45, ha='right')
    
    # Add legend
    ax.legend()
    
    # Adjust layout to ensure labels fit
    self.chart_figure.tight_layout()
    
    # Optional: add value labels on top of bars
    for i, (before, after) in enumerate(zip(chart_data["before_scores"], chart_data["after_scores"])):
        diff = after - before
        color = 'green' if diff > 0 else 'red' if diff < 0 else 'gray'
        
        # Only show change indicator if there's a meaningful difference
        if abs(diff) >= 0.01:
            indicator = "↑" if diff > 0 else "↓"
            ax.text(i, max(before, after) + 0.02, f"{indicator} {abs(diff):.2f}", 
                    ha='center', va='bottom', color=color, fontweight='bold')

def create_pie_chart(self, chart_data):
    """Create pie charts showing distribution of pattern scores
    
    Args:
        chart_data: Dictionary containing chart data
    """
    # Create two subplots for before and after
    ax1 = self.chart_figure.add_subplot(121)
    ax2 = self.chart_figure.add_subplot(122)
    
    # Group data by categories for pie chart
    categories = set(chart_data["categories"])
    before_by_category = {cat: 0 for cat in categories}
    after_by_category = {cat: 0 for cat in categories}
    
    # Sum scores by category
    for i, cat in enumerate(chart_data["categories"]):
        before_by_category[cat] += chart_data["before_scores"][i]
        after_by_category[cat] += chart_data["after_scores"][i]
    
    # Sort for consistent wedge order
    cat_labels = sorted(categories)
    before_values = [before_by_category[cat] for cat in cat_labels]
    after_values = [after_by_category[cat] for cat in cat_labels]
    
    # Create pie charts
    ax1.pie(before_values, labels=cat_labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.set_title('Before')
    
    ax2.pie(after_values, labels=cat_labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.set_title('After')
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    ax2.axis('equal')
    
    # Add overall title
    self.chart_figure.suptitle('Pattern Score Distribution by Category', fontsize=14)
    
    # Adjust layout
    self.chart_figure.tight_layout()

def create_line_chart(self, chart_data):
    """Create a line chart showing pattern score trends
    
    Args:
        chart_data: Dictionary containing chart data
    """
    # Get axis
    ax = self.chart_figure.add_subplot(111)
    
    # Set up x-axis with pattern names
    x = np.arange(len(chart_data["patterns"]))
    
    # Plot lines
    ax.plot(x, chart_data["before_scores"], 'b-o', label='Before')
    ax.plot(x, chart_data["after_scores"], 'r-o', label='After')
    
    # Highlight differences with connecting lines
    for i in range(len(x)):
        before = chart_data["before_scores"][i]
        after = chart_data["after_scores"][i]
        diff = after - before
        color = 'green' if diff > 0 else 'red' if diff < 0 else 'gray'
        
        if abs(diff) >= 0.01:  # Only show significant changes
            ax.plot([x[i], x[i]], [before, after], color=color, linestyle='-', 
                    linewidth=1.5, alpha=0.7)
    
    # Set axis labels and title
    ax.set_xlabel('Patterns')
    ax.set_ylabel('Score (0-1)')
    ax.set_title('Pattern Score Trends')
    ax.set_xticks(x)
    ax.set_xticklabels(chart_data["patterns"], rotation=45, ha='right')
    
    # Add grid lines for better readability
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add legend
    ax.legend()
    
    # Set y-axis limits with a bit of padding
    ax.set_ylim(min(0, min(chart_data["before_scores"] + chart_data["after_scores"]) - 0.1),
                max(1, max(chart_data["before_scores"] + chart_data["after_scores"]) + 0.1))
    
    # Adjust layout to ensure labels fit
    self.chart_figure.tight_layout()

def create_heatmap_chart(self, chart_data):
    """Create a heatmap showing pattern score changes
    
    Args:
        chart_data: Dictionary containing chart data
    """
    # Get axis
    ax = self.chart_figure.add_subplot(111)
    
    # Prepare data for heatmap - we'll use differences
    data = np.array(chart_data["differences"]).reshape(-1, 1)
    
    # If we have no data, show a message
    if len(data) == 0:
        ax.text(0.5, 0.5, "No data available for heatmap", 
                ha='center', va='center', transform=ax.transAxes)
        return
    
    # Create heatmap
    im = ax.imshow(data.T, cmap='RdYlGn', aspect='auto')
    
    # Set y-tick (just one labeled "Change")
    ax.set_yticks([0])
    ax.set_yticklabels(["Change"])
    
    # Set x-ticks for pattern names
    ax.set_xticks(np.arange(len(chart_data["patterns"])))
    ax.set_xticklabels(chart_data["patterns"], rotation=45, ha='right')
    
    # Add colorbar
    cbar = self.chart_figure.colorbar(im)
    cbar.set_label('Score Change')
    
    # Add title
    ax.set_title("Pattern Score Changes Heatmap")
    
    # Add text annotations with the actual difference values
    for i, diff in enumerate(chart_data["differences"]):
        text_color = 'black' if abs(diff) < 0.2 else 'white'
        ax.text(i, 0, f"{diff:.2f}", ha="center", va="center", color=text_color)
    
    # Adjust layout
    self.chart_figure.tight_layout()

def update_chart_description(self, chart_type, chart_data):
    """Update the chart description with insights about the data
    
    Args:
        chart_type: Type of chart being displayed
        chart_data: Dictionary containing chart data
    """
    # Generate description and insights
    description = f"<h3>{chart_type} Analysis</h3>"
    
    # Add overview statistics
    if len(chart_data["differences"]) > 0:
        avg_change = sum(chart_data["differences"]) / len(chart_data["differences"])
        max_improvement = max(chart_data["differences"])
        max_decline = min(chart_data["differences"])
        
        description += f"<p><b>Average change:</b> {avg_change:.4f}</p>"
        
        # Find patterns with biggest improvement and decline
        if max_improvement > 0:
            max_idx = chart_data["differences"].index(max_improvement)
            description += (f"<p><b>Biggest improvement:</b> {chart_data['patterns'][max_idx]} "
                           f"(+{max_improvement:.4f})</p>")
        
        if max_decline < 0:
            min_idx = chart_data["differences"].index(max_decline)
            description += (f"<p><b>Largest decline:</b> {chart_data['patterns'][min_idx]} "
                           f"({max_decline:.4f})</p>")
    
    # Add specific analysis based on chart type
    if chart_type == "Radar Chart":
        description += "<p>The radar chart shows the before and after scores for each pattern. "
        description += "Larger area indicates higher overall scores.</p>"
        
    elif chart_type == "Bar Chart":
        description += "<p>The bar chart compares before and after scores side-by-side. "
        description += "Arrows indicate the magnitude and direction of changes.</p>"
        
    elif chart_type == "Pie Chart":
        description += "<p>The pie charts show the distribution of scores across different pattern categories. "
        description += "This helps identify which categories account for the largest portions of the overall score.</p>"
        
    elif chart_type == "Line Chart":
        description += "<p>The line chart shows score trends across patterns. "
        description += "Vertical connecting lines highlight the direction and magnitude of changes.</p>"
        
    elif chart_type == "Heatmap":
        description += "<p>The heatmap visualizes score changes with colors: "
        description += "green for improvements, red for declines, and yellow for minimal changes.</p>"
    
    # Add general insights if we have enough data
    if len(chart_data["differences"]) >= 3:
        improved = sum(1 for d in chart_data["differences"] if d > 0)
        declined = sum(1 for d in chart_data["differences"] if d < 0)
        unchanged = sum(1 for d in chart_data["differences"] if d == 0)
        
        description += f"<p>Out of {len(chart_data['differences'])} patterns analyzed:"
        description += f"<br>• {improved} patterns showed improvement"
        description += f"<br>• {declined} patterns showed decline"
        description += f"<br>• {unchanged} patterns remained unchanged</p>"
        
        # Add interpretation
        if improved > declined:
            description += "<p><b>Insight:</b> Overall positive trend observed across patterns.</p>"
        elif declined > improved:
            description += "<p><b>Insight:</b> Overall negative trend observed across patterns.</p>"
        else:
            description += "<p><b>Insight:</b> Mixed results with balanced improvements and declines.</p>"
    
    # Set the description text
    self.chart_description.setHtml(description)

def filter_chart_by_category(self, category):
    """Filter chart data by selected category
    
    Args:
        category: Pattern category to filter by
    """
    # Get current chart type and threshold
    chart_type = self.chart_type_combo.currentText()
    threshold_text = self.threshold_combo.currentText()
    
    # Parse threshold value
    if threshold_text == "Any Change":
        threshold = 0.0
    else:
        # Extract number from text like "> 0.05"
        threshold = float(threshold_text.split(" ")[1])
    
    # Update chart with new category filter
    self.update_chart(chart_type, category, threshold)

def filter_chart_by_threshold(self, threshold):
    """Filter chart data by selected threshold
    
    Args:
        threshold: Minimum score difference threshold
    """
    # Get current chart type and category
    chart_type = self.chart_type_combo.currentText()
    category = self.category_combo.currentText()
    
    # Update chart with new threshold filter
    self.update_chart(chart_type, category, threshold)
