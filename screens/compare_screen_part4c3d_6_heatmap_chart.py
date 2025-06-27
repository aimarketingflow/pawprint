#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3d-6: Heatmap Chart Processing

Implements the heatmap chart data processing methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for heatmap chart processing that would be included in the CompareScreen class

def format_heatmap_chart_data(self, base_data):
    """Format data for heatmap chart visualization
    
    Args:
        base_data: Base chart data dictionary
        
    Returns:
        dict: Heatmap chart data dictionary
    """
    # Heatmaps are best for showing relationships between two categorical dimensions
    # For pawprints, we can show:
    # 1. Categories vs change magnitude
    # 2. Origin vs pattern categories
    
    # Create data structure for heatmap chart
    heatmap_data = {
        "chart_mode": "category_changes",  # or "origin_categories"
        "x_labels": [],
        "y_labels": [],
        "z_values": [],
        "title": "Pattern Changes by Category"
    }
    
    # Get pattern changes
    patterns = base_data["patterns"]
    changes = base_data["changes"]
    categories = base_data["categories"]
    
    # Extract unique categories
    unique_categories = list(set(categories))
    
    # Define change buckets for x-axis
    change_buckets = [
        "Major Regression (<-0.1)",
        "Minor Regression (-0.1 to -0.01)",
        "Minimal Change (-0.01 to 0.01)",
        "Minor Improvement (0.01 to 0.1)",
        "Major Improvement (>0.1)"
    ]
    
    # Initialize empty matrix
    matrix = np.zeros((len(unique_categories), len(change_buckets)))
    
    # Populate matrix
    for i, pattern in enumerate(patterns):
        change = changes[i]
        category = categories[i]
        
        # Get category index
        cat_idx = unique_categories.index(category)
        
        # Determine change bucket
        if change < -0.1:
            bucket_idx = 0  # Major Regression
        elif change < -0.01:
            bucket_idx = 1  # Minor Regression
        elif change <= 0.01:
            bucket_idx = 2  # Minimal Change
        elif change <= 0.1:
            bucket_idx = 3  # Minor Improvement
        else:
            bucket_idx = 4  # Major Improvement
            
        # Increment count in matrix
        matrix[cat_idx, bucket_idx] += 1
    
    # Store matrix data
    heatmap_data["x_labels"] = change_buckets
    heatmap_data["y_labels"] = unique_categories
    heatmap_data["z_values"] = matrix
    
    # If we have file groups (multiple origins), prepare alternative view
    if hasattr(self, 'file_groups') and len(self.file_groups) > 1:
        # Initialize origin-category matrix
        origins = list(self.file_groups.keys())
        origin_cat_matrix = np.zeros((len(origins), len(unique_categories)))
        
        # Count patterns by origin and category
        for origin_idx, origin in enumerate(origins):
            # Get files for this origin
            files = self.file_groups.get(origin, [])
            
            for file_info in files:
                # Get patterns from file
                data = file_info.get("data", {})
                patterns_data = data.get("patterns", {})
                
                # Count patterns by category
                for pattern_key, pattern_data in patterns_data.items():
                    category = pattern_data.get("category", "Unknown")
                    if category in unique_categories:
                        cat_idx = unique_categories.index(category)
                        origin_cat_matrix[origin_idx, cat_idx] += 1
        
        # Store alternative matrix data
        heatmap_data["alt_x_labels"] = unique_categories
        heatmap_data["alt_y_labels"] = origins
        heatmap_data["alt_z_values"] = origin_cat_matrix
        heatmap_data["has_alt_view"] = True
    else:
        heatmap_data["has_alt_view"] = False
    
    # Add metadata
    heatmap_data["title"] = "Pattern Changes by Category"
    heatmap_data["subtitle"] = f"Analysis of {len(patterns)} patterns across {len(unique_categories)} categories"
    
    return heatmap_data

def draw_heatmap_chart(self, chart_data):
    """Draw heatmap chart on the canvas
    
    Args:
        chart_data: Heatmap chart data dictionary
    """
    if not MATPLOTLIB_AVAILABLE:
        return
    
    # Clear previous figure
    self.chart_figure.clear()
    
    # Determine which data set to use
    if chart_data.get("chart_mode", "category_changes") == "category_changes":
        # Use category-change distribution data
        x_labels = chart_data.get("x_labels", [])
        y_labels = chart_data.get("y_labels", [])
        z_values = chart_data.get("z_values", [])
        title = "Pattern Changes by Category"
    else:
        # Use origin-category distribution data
        x_labels = chart_data.get("alt_x_labels", [])
        y_labels = chart_data.get("alt_y_labels", [])
        z_values = chart_data.get("alt_z_values", [])
        title = "Patterns by Origin and Category"
    
    # Handle empty data
    if len(x_labels) == 0 or len(y_labels) == 0:
        ax = self.chart_figure.add_subplot(111)
        ax.text(0.5, 0.5, "No data available for heatmap chart", 
                horizontalalignment='center',
                verticalalignment='center',
                transform=ax.transAxes)
        self.chart_canvas.draw()
        return
        
    # Create subplot
    ax = self.chart_figure.add_subplot(111)
    
    # Create heatmap
    im = ax.imshow(z_values, cmap='plasma')
    
    # Set labels and ticks
    ax.set_xticks(np.arange(len(x_labels)))
    ax.set_yticks(np.arange(len(y_labels)))
    ax.set_xticklabels(x_labels)
    ax.set_yticklabels(y_labels)
    
    # Rotate x-tick labels for readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    
    # Add colorbar
    cbar = self.chart_figure.colorbar(im, ax=ax)
    cbar.set_label("Pattern Count")
    
    # Add values to cells
    for i in range(len(y_labels)):
        for j in range(len(x_labels)):
            # Only show text for cells with values
            if z_values[i, j] > 0:
                # Choose text color based on cell value
                text_color = 'white' if z_values[i, j] > np.max(z_values)/2 else 'black'
                ax.text(j, i, int(z_values[i, j]), 
                        ha="center", va="center", color=text_color)
    
    # Set title
    ax.set_title(title)
    
    # Add toggle button for switching between views if available
    if chart_data.get("has_alt_view", False) and hasattr(self, 'toggle_heatmap_view_button'):
        if chart_data.get("chart_mode", "category_changes") == "category_changes":
            self.toggle_heatmap_view_button.setText("View by Origin")
        else:
            self.toggle_heatmap_view_button.setText("View by Change")
    
    # Adjust layout for rotated labels
    self.chart_figure.tight_layout()
    
    # Draw the updated chart
    self.chart_canvas.draw()

def toggle_heatmap_chart_view(self):
    """Toggle between category-change and origin-category views"""
    # Get current chart data
    current_data = self.current_chart_data
    
    if not isinstance(current_data, dict):
        return
    
    # Toggle chart mode
    if current_data.get("chart_mode", "category_changes") == "category_changes":
        current_data["chart_mode"] = "origin_categories"
    else:
        current_data["chart_mode"] = "category_changes"
    
    # Redraw chart
    self.draw_chart("heatmap", current_data)

def get_heatmap_chart_description(self, chart_data):
    """Generate HTML description for heatmap chart
    
    Args:
        chart_data: Heatmap chart data dictionary
        
    Returns:
        str: HTML-formatted description
    """
    # Start with chart overview
    html = f"<h3>{chart_data.get('title', 'Pattern Distribution')}</h3>"
    html += f"<p>{chart_data.get('subtitle', 'Pattern distribution analysis')}</p>"
    
    # Determine which data set to use
    if chart_data.get("chart_mode", "category_changes") == "category_changes":
        # Category-change distribution insights
        html += self._get_category_change_heatmap_insights(chart_data)
    else:
        # Origin-category distribution insights
        html += self._get_origin_category_heatmap_insights(chart_data)
    
    return html

def _get_category_change_heatmap_insights(self, chart_data):
    """Generate insights for category-change heatmap
    
    Args:
        chart_data: Heatmap chart data dictionary
        
    Returns:
        str: HTML-formatted insights
    """
    html = "<h4>Key Insights:</h4><ul>"
    
    # Extract data
    x_labels = chart_data.get("x_labels", [])
    y_labels = chart_data.get("y_labels", [])
    z_values = chart_data.get("z_values", [])
    
    if len(y_labels) == 0 or len(x_labels) == 0:
        return html + "<li>No data available for analysis</li></ul>"
    
    # Calculate totals by category
    category_totals = np.sum(z_values, axis=1)
    
    # Calculate totals by change bucket
    change_totals = np.sum(z_values, axis=0)
    
    # Find category with most improvements
    improvement_cols = [3, 4]  # Minor and Major Improvement columns
    improvement_counts = np.sum(z_values[:, improvement_cols], axis=1)
    if len(improvement_counts) > 0 and np.max(improvement_counts) > 0:
        best_cat_idx = np.argmax(improvement_counts)
        best_cat = y_labels[best_cat_idx]
        html += f"<li>Category with most improvements: <b>{best_cat}</b> "
        html += f"with {int(improvement_counts[best_cat_idx])} improved patterns</li>"
    
    # Find category with most regressions
    regression_cols = [0, 1]  # Major and Minor Regression columns
    regression_counts = np.sum(z_values[:, regression_cols], axis=1)
    if len(regression_counts) > 0 and np.max(regression_counts) > 0:
        worst_cat_idx = np.argmax(regression_counts)
        worst_cat = y_labels[worst_cat_idx]
        html += f"<li>Category with most regressions: <b>{worst_cat}</b> "
        html += f"with {int(regression_counts[worst_cat_idx])} regressed patterns</li>"
    
    # Calculate overall distribution
    total_patterns = np.sum(z_values)
    if total_patterns > 0:
        major_improve_pct = (change_totals[4] / total_patterns) * 100
        minor_improve_pct = (change_totals[3] / total_patterns) * 100
        minimal_change_pct = (change_totals[2] / total_patterns) * 100
        minor_regress_pct = (change_totals[1] / total_patterns) * 100
        major_regress_pct = (change_totals[0] / total_patterns) * 100
        
        html += "<li>Overall distribution:</li>"
        html += "<ul>"
        html += f"<li><span style='color:#00cc00'>Major improvements:</span> {int(change_totals[4])} ({major_improve_pct:.1f}%)</li>"
        html += f"<li><span style='color:#88cc00'>Minor improvements:</span> {int(change_totals[3])} ({minor_improve_pct:.1f}%)</li>"
        html += f"<li><span style='color:#3388cc'>Minimal changes:</span> {int(change_totals[2])} ({minimal_change_pct:.1f}%)</li>"
        html += f"<li><span style='color:#cc8800'>Minor regressions:</span> {int(change_totals[1])} ({minor_regress_pct:.1f}%)</li>"
        html += f"<li><span style='color:#cc0000'>Major regressions:</span> {int(change_totals[0])} ({major_regress_pct:.1f}%)</li>"
        html += "</ul>"
    
    html += "</ul>"
    
    # Add recommendations
    html += "<h4>Recommendations:</h4><ul>"
    
    # Provide category-specific recommendations
    if len(regression_counts) > 0 and np.max(regression_counts) > 0:
        worst_cat = y_labels[np.argmax(regression_counts)]
        html += f"<li>Investigate causes for regressions in <b>{worst_cat}</b> category</li>"
    
    # Look for opportunities to apply learnings
    if len(improvement_counts) > 0 and np.max(improvement_counts) > 0 and len(regression_counts) > 0 and np.max(regression_counts) > 0:
        best_cat = y_labels[np.argmax(improvement_counts)]
        worst_cat = y_labels[np.argmax(regression_counts)]
        html += f"<li>Apply tactics from <b>{best_cat}</b> to improve patterns in <b>{worst_cat}</b></li>"
    
    html += "<li>Use the comparison tab to analyze specific pattern changes within categories</li>"
    html += "</ul>"
    
    return html

def _get_origin_category_heatmap_insights(self, chart_data):
    """Generate insights for origin-category heatmap
    
    Args:
        chart_data: Heatmap chart data dictionary
        
    Returns:
        str: HTML-formatted insights
    """
    html = "<h4>Key Insights:</h4><ul>"
    
    # Extract data
    x_labels = chart_data.get("alt_x_labels", [])
    y_labels = chart_data.get("alt_y_labels", [])
    z_values = chart_data.get("alt_z_values", [])
    
    if len(y_labels) == 0 or len(x_labels) == 0:
        return html + "<li>No data available for analysis</li></ul>"
    
    # Calculate totals by origin
    origin_totals = np.sum(z_values, axis=1)
    
    # Calculate totals by category
    category_totals = np.sum(z_values, axis=0)
    
    # Find origin with most patterns
    if len(origin_totals) > 0:
        largest_origin_idx = np.argmax(origin_totals)
        largest_origin = y_labels[largest_origin_idx]
        html += f"<li>Origin with most patterns: <b>{largest_origin}</b> "
        html += f"with {int(origin_totals[largest_origin_idx])} total patterns</li>"
    
    # Find most common category across all origins
    if len(category_totals) > 0:
        largest_cat_idx = np.argmax(category_totals)
        largest_cat = x_labels[largest_cat_idx]
        html += f"<li>Most common category: <b>{largest_cat}</b> "
        html += f"with {int(category_totals[largest_cat_idx])} total patterns</li>"
    
    # Look for origin-specific category concentrations
    for i, origin in enumerate(y_labels):
        if i < len(z_values):
            # Find dominant category for this origin
            if len(z_values[i]) > 0 and np.max(z_values[i]) > 0:
                dom_cat_idx = np.argmax(z_values[i])
                dom_cat = x_labels[dom_cat_idx]
                
                # Only report if it's a significant concentration
                total = np.sum(z_values[i])
                if total > 0:
                    concentration = (z_values[i][dom_cat_idx] / total) * 100
                    if concentration > 50:
                        html += f"<li><b>{origin}</b> has {concentration:.1f}% of its patterns "
                        html += f"in the <b>{dom_cat}</b> category</li>"
    
    html += "</ul>"
    
    # Add recommendations
    html += "<h4>Recommendations:</h4><ul>"
    
    # Look for missing categories in origins
    for i, origin in enumerate(y_labels):
        if i < len(z_values):
            # Find categories with zero patterns
            missing_cats = []
            for j, cat in enumerate(x_labels):
                if j < len(z_values[i]) and z_values[i][j] == 0:
                    missing_cats.append(cat)
            
            # Only report if there are a few missing categories
            if 0 < len(missing_cats) <= 3:
                html += f"<li>Investigate missing {', '.join(missing_cats)} patterns for <b>{origin}</b></li>"
    
    # General recommendations
    html += "<li>Use the comparison tab to analyze patterns by origin</li>"
    html += "<li>Check the Raw Data tab to examine specific differences in patterns between origins</li>"
    html += "</ul>"
    
    return html
