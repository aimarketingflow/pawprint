#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-5: Pie Chart Processing

Implements the pie chart data processing methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for pie chart processing that would be included in the CompareScreen class

def format_pie_chart_data(self, base_data):
    """Format data for pie chart visualization
    
    Args:
        base_data: Base chart data dictionary
        
    Returns:
        dict: Pie chart data dictionary
    """
    # Pie charts are best for showing distribution across categories
    # We can use them to show:
    # 1. Distribution of improved/regressed/unchanged patterns
    # 2. Distribution by pattern category
    
    # Create data structure for pie chart
    pie_data = {
        "chart_mode": "change_distribution",  # or "category_distribution"
        "labels": [],
        "values": [],
        "colors": [],
        "explode": []
    }
    
    # Get pattern changes
    patterns = base_data["patterns"]
    changes = base_data["changes"]
    categories = base_data["categories"]
    
    # Process change distribution
    improved = [p for i, p in enumerate(patterns) if changes[i] > 0]
    regressed = [p for i, p in enumerate(patterns) if changes[i] < 0]
    unchanged = [p for i, p in enumerate(patterns) if changes[i] == 0]
    
    # Add change distribution data
    pie_data["labels"].append("Improved")
    pie_data["values"].append(len(improved))
    pie_data["colors"].append("#4CAF50")  # Green
    pie_data["explode"].append(0.1)
    
    pie_data["labels"].append("Regressed")
    pie_data["values"].append(len(regressed))
    pie_data["colors"].append("#F44336")  # Red
    pie_data["explode"].append(0.1)
    
    pie_data["labels"].append("Unchanged")
    pie_data["values"].append(len(unchanged))
    pie_data["colors"].append("#2196F3")  # Blue
    pie_data["explode"].append(0)
    
    # Count patterns by category
    category_counts = {}
    for cat in categories:
        if cat not in category_counts:
            category_counts[cat] = 0
        category_counts[cat] += 1
    
    # Store category distribution for alternate view
    pie_data["category_labels"] = list(category_counts.keys())
    pie_data["category_values"] = list(category_counts.values())
    
    # Generate category colors
    if len(category_counts) > 0:
        cmap = plt.cm.get_cmap('tab10', len(category_counts))
        pie_data["category_colors"] = [cmap(i) for i in range(len(category_counts))]
        pie_data["category_explode"] = [0.05] * len(category_counts)
    
    # Add metadata
    pie_data["title"] = "Pattern Change Distribution"
    pie_data["subtitle"] = f"Analysis of {len(patterns)} patterns"
    
    return pie_data

def draw_pie_chart(self, chart_data):
    """Draw pie chart on the canvas
    
    Args:
        chart_data: Pie chart data dictionary
    """
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Clear previous figure
    self.chart_figure.clear()
    
    # Create subplot
    ax = self.chart_figure.add_subplot(111)
    
    # Determine which data set to use
    if chart_data.get("chart_mode", "change_distribution") == "change_distribution":
        # Use change distribution data
        labels = chart_data.get("labels", [])
        values = chart_data.get("values", [])
        colors = chart_data.get("colors", [])
        explode = chart_data.get("explode", [])
        title = "Pattern Change Distribution"
    else:
        # Use category distribution data
        labels = chart_data.get("category_labels", [])
        values = chart_data.get("category_values", [])
        colors = chart_data.get("category_colors", [])
        explode = chart_data.get("category_explode", [])
        title = "Pattern Category Distribution"
    
    # Handle empty data
    if not labels or not values or sum(values) == 0:
        ax.text(0.5, 0.5, "No data available for pie chart", 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        self.chart_canvas.draw()
        return
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        values, 
        explode=explode, 
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        shadow=True, 
        startangle=90,
        textprops={'color': 'w'}
    )
    
    # Customize text properties
    for text in texts:
        text.set_color('#333333')
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    
    # Set title
    ax.set_title(title)
    
    # Add toggle button for switching between change and category distribution
    if hasattr(self, 'toggle_pie_view_button'):
        if chart_data.get("chart_mode", "change_distribution") == "change_distribution":
            self.toggle_pie_view_button.setText("View by Category")
        else:
            self.toggle_pie_view_button.setText("View by Change")
    
    # Draw the updated chart
    self.chart_canvas.draw()

def toggle_pie_chart_view(self):
    """Toggle between change distribution and category distribution views"""
    # Get current chart data
    current_data = self.current_chart_data
    
    if not isinstance(current_data, dict):
        return
    
    # Toggle chart mode
    if current_data.get("chart_mode", "change_distribution") == "change_distribution":
        current_data["chart_mode"] = "category_distribution"
    else:
        current_data["chart_mode"] = "change_distribution"
    
    # Redraw chart
    self.draw_chart("pie", current_data)

def get_pie_chart_description(self, chart_data):
    """Generate HTML description for pie chart
    
    Args:
        chart_data: Pie chart data dictionary
        
    Returns:
        str: HTML-formatted description
    """
    # Start with chart overview
    html = f"<h3>{chart_data.get('title', 'Pattern Change Distribution')}</h3>"
    html += f"<p>{chart_data.get('subtitle', 'Distribution analysis')}</p>"
    
    # Determine which data set to use
    if chart_data.get("chart_mode", "change_distribution") == "change_distribution":
        # Use change distribution data
        labels = chart_data.get("labels", [])
        values = chart_data.get("values", [])
    else:
        # Use category distribution data
        labels = chart_data.get("category_labels", [])
        values = chart_data.get("category_values", [])
    
    if not labels or not values or sum(values) == 0:
        return html + "<p>No data available for analysis.</p>"
    
    # Calculate total
    total = sum(values)
    
    # Add distribution summary
    html += "<h4>Distribution Summary:</h4>"
    html += "<ul>"
    
    for i, label in enumerate(labels):
        if i < len(values):
            value = values[i]
            percentage = (value / total) * 100
            
            # Color code based on label name
            color = "#333333"
            if label == "Improved":
                color = "#4CAF50"  # Green
            elif label == "Regressed":
                color = "#F44336"  # Red
            elif label == "Unchanged":
                color = "#2196F3"  # Blue
                
            html += f"<li><span style='color:{color}'><b>{label}:</b></span> {value} ({percentage:.1f}%)</li>"
    
    html += "</ul>"
    
    # Add insights based on chart mode
    if chart_data.get("chart_mode", "change_distribution") == "change_distribution":
        # Insights for change distribution
        html += self._get_change_distribution_insights(labels, values)
    else:
        # Insights for category distribution
        html += self._get_category_distribution_insights(labels, values)
    
    return html

def _get_change_distribution_insights(self, labels, values):
    """Generate insights for change distribution pie chart
    
    Args:
        labels: Chart labels
        values: Chart values
        
    Returns:
        str: HTML-formatted insights
    """
    html = "<h4>Key Insights:</h4><ul>"
    
    # Extract values for improved, regressed, unchanged
    improved_idx = labels.index("Improved") if "Improved" in labels else -1
    regressed_idx = labels.index("Regressed") if "Regressed" in labels else -1
    unchanged_idx = labels.index("Unchanged") if "Unchanged" in labels else -1
    
    improved_count = values[improved_idx] if improved_idx >= 0 else 0
    regressed_count = values[regressed_idx] if regressed_idx >= 0 else 0
    unchanged_count = values[unchanged_idx] if unchanged_idx >= 0 else 0
    
    # Calculate total
    total = sum(values)
    
    # Generate insights
    if total == 0:
        return html + "<li>No pattern data available for analysis</li></ul>"
    
    # Compare improved vs regressed
    if improved_count > regressed_count:
        ratio = improved_count / max(regressed_count, 1)
        html += f"<li><span style='color:green'>Positive trend</span> with {improved_count} improvements "
        html += f"vs {regressed_count} regressions ({ratio:.1f}:1 ratio)</li>"
    elif regressed_count > improved_count:
        ratio = regressed_count / max(improved_count, 1)
        html += f"<li><span style='color:red'>Negative trend</span> with {regressed_count} regressions "
        html += f"vs {improved_count} improvements ({ratio:.1f}:1 ratio)</li>"
    else:
        html += f"<li><span style='color:blue'>Balanced changes</span> with equal improvements and regressions</li>"
    
    # Comment on unchanged patterns
    if unchanged_count > (total * 0.5):
        html += f"<li>Majority of patterns ({unchanged_count}/{total}, {unchanged_count/total*100:.1f}%) showed no change</li>"
    
    # Overall assessment
    if improved_count > regressed_count * 2:
        html += "<li>Overall <span style='color:green'>strong positive</span> pattern change profile</li>"
    elif improved_count > regressed_count:
        html += "<li>Overall <span style='color:green'>moderately positive</span> pattern change profile</li>"
    elif regressed_count > improved_count * 2:
        html += "<li>Overall <span style='color:red'>strong negative</span> pattern change profile</li>"
    elif regressed_count > improved_count:
        html += "<li>Overall <span style='color:red'>moderately negative</span> pattern change profile</li>"
    else:
        html += "<li>Overall <span style='color:blue'>neutral</span> pattern change profile</li>"
    
    html += "</ul>"
    
    # Add recommendations
    html += "<h4>Recommendations:</h4><ul>"
    if regressed_count > 0:
        html += "<li>Investigate patterns showing regressions</li>"
    if improved_count > regressed_count:
        html += "<li>Document factors contributing to pattern improvements</li>"
    if unchanged_count > (total * 0.7):
        html += "<li>Review detection methods as most patterns show no change</li>"
    html += "</ul>"
    
    return html

def _get_category_distribution_insights(self, labels, values):
    """Generate insights for category distribution pie chart
    
    Args:
        labels: Chart labels
        values: Chart values
        
    Returns:
        str: HTML-formatted insights
    """
    html = "<h4>Key Insights:</h4><ul>"
    
    # Calculate total
    total = sum(values)
    
    if total == 0:
        return html + "<li>No category data available for analysis</li></ul>"
    
    # Sort categories by count
    categories = list(zip(labels, values))
    categories.sort(key=lambda x: x[1], reverse=True)
    
    # Top categories
    if categories:
        top_category, top_count = categories[0]
        html += f"<li>Dominant category: <b>{top_category}</b> with {top_count} patterns "
        html += f"({top_count/total*100:.1f}% of total)</li>"
    
    # Check for category imbalance
    if len(categories) >= 2:
        top_category, top_count = categories[0]
        second_category, second_count = categories[1]
        
        if top_count > second_count * 3:
            html += f"<li>Significant imbalance with <b>{top_category}</b> having {top_count/second_count:.1f}x "
            html += f"more patterns than next category (<b>{second_category}</b>)</li>"
    
    # Comment on diversity
    if len(categories) >= 3:
        html += f"<li>Pattern diversity across {len(categories)} different categories</li>"
        
        # Calculate concentration in top 3 categories
        top3_count = sum(count for _, count in categories[:3])
        top3_percent = (top3_count / total) * 100
        
        if top3_percent > 80:
            html += f"<li>High concentration with {top3_percent:.1f}% of patterns in top 3 categories</li>"
        elif top3_percent < 50:
            html += f"<li>Wide distribution with only {top3_percent:.1f}% of patterns in top 3 categories</li>"
    
    html += "</ul>"
    
    # Add recommendations
    html += "<h4>Recommendations:</h4><ul>"
    
    if categories and len(categories) >= 2:
        top_category, _ = categories[0]
        bottom_categories = categories[-2:]
        
        html += f"<li>Focus analysis on dominant <b>{top_category}</b> category</li>"
        
        html += "<li>Consider expanding detection for underrepresented categories: "
        html += ", ".join(f"<b>{cat}</b>" for cat, _ in bottom_categories)
        html += "</li>"
    
    html += "<li>Use the comparison tab to analyze patterns by category</li>"
    html += "</ul>"
    
    return html
