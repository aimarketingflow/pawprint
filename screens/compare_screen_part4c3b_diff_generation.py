#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3b: Diff Generation Methods

Implements the diff generation methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for generating diffs that would be included in the CompareScreen class

def generate_file_diffs(self):
    """Generate diffs for all file pairs in the comparison"""
    # Create progress tracker for diff generation
    self.progress_tracker.start_operation("Generating file differences...")
    
    # Keep track of total operations
    total_operations = len(self.comparison_files)
    completed = 0
    
    # Process all files
    for i, file_path in enumerate(self.comparison_files):
        # Skip first file if comparing with baseline
        if i == 0 and len(self.comparison_files) > 1:
            continue
            
        # Compare with baseline (first file)
        baseline_index = 0
        baseline_data = self.comparison_data[baseline_index]
        current_data = self.comparison_data[i]
        
        # Generate diff
        diff_key = f"{baseline_index}-{i}"
        self.diff_cache[diff_key] = self._compute_file_diff(baseline_data, current_data)
        
        # Update progress
        completed += 1
        progress = int((completed / total_operations) * 100)
        self.progress_tracker.update_progress(
            progress,
            f"Comparing {os.path.basename(file_path)}..."
        )
    
    # Complete operation
    self.progress_tracker.complete_operation(
        True, "File differences generated successfully"
    )

def _compute_file_diff(self, before_data, after_data):
    """Compute differences between two pawprint data dictionaries
    
    Args:
        before_data: First pawprint data dictionary
        after_data: Second pawprint data dictionary
        
    Returns:
        dict: Dictionary containing diff information
    """
    diff_result = {
        "added": {},
        "removed": {},
        "changed": {},
        "unchanged": {},
        "pattern_changes": []
    }
    
    # Flatten dictionaries for easier comparison
    flat_before = self._flatten_dict(before_data)
    flat_after = self._flatten_dict(after_data)
    
    # Find added, removed, and changed keys
    all_keys = set(flat_before.keys()) | set(flat_after.keys())
    
    for key in all_keys:
        if key.startswith("metadata."):
            # Skip metadata for diff calculation
            continue
            
        if key not in flat_before:
            # Key was added
            diff_result["added"][key] = flat_after[key]
        elif key not in flat_after:
            # Key was removed
            diff_result["removed"][key] = flat_before[key]
        elif flat_before[key] != flat_after[key]:
            # Value changed
            diff_result["changed"][key] = {
                "before": flat_before[key],
                "after": flat_after[key]
            }
        else:
            # Value unchanged
            diff_result["unchanged"][key] = flat_before[key]
    
    # Calculate pattern changes
    diff_result["pattern_changes"] = self._compute_pattern_changes(before_data, after_data)
    
    return diff_result

def _compute_pattern_changes(self, before_data, after_data):
    """Compute pattern score changes between two pawprint data dictionaries
    
    Args:
        before_data: First pawprint data dictionary
        after_data: Second pawprint data dictionary
        
    Returns:
        list: List of pattern change dictionaries
    """
    pattern_changes = []
    
    # Get patterns section from data (if available)
    before_patterns = before_data.get("patterns", {})
    after_patterns = after_data.get("patterns", {})
    
    # Combine all pattern keys
    all_pattern_keys = set(before_patterns.keys()) | set(after_patterns.keys())
    
    # Calculate changes for each pattern
    for pattern_key in all_pattern_keys:
        before_score = before_patterns.get(pattern_key, {}).get("score", 0.0)
        after_score = after_patterns.get(pattern_key, {}).get("score", 0.0)
        
        # Calculate change and percent change
        change = after_score - before_score
        percent_change = 0.0
        if before_score > 0:
            percent_change = (change / before_score) * 100
        
        # Get pattern metadata
        category = before_patterns.get(pattern_key, {}).get("category", 
                   after_patterns.get(pattern_key, {}).get("category", "Unknown"))
        
        description = before_patterns.get(pattern_key, {}).get("description", 
                     after_patterns.get(pattern_key, {}).get("description", ""))
        
        # Create pattern change record
        pattern_change = {
            "key": pattern_key,
            "name": pattern_key.split('.')[-1],  # Extract name from key
            "category": category,
            "description": description,
            "before_score": before_score,
            "after_score": after_score,
            "change": change,
            "percent_change": percent_change
        }
        
        pattern_changes.append(pattern_change)
    
    # Sort pattern changes by absolute change magnitude (largest first)
    pattern_changes.sort(key=lambda x: abs(x["change"]), reverse=True)
    
    return pattern_changes

def _flatten_dict(self, d, parent_key='', sep='.'):
    """Flatten a nested dictionary
    
    Args:
        d: Dictionary to flatten
        parent_key: Parent key prefix
        sep: Separator between parent and child keys
        
    Returns:
        dict: Flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(self._flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Convert lists to string representations for comparison
            # This is simplified - a more robust implementation would handle list diffs better
            items.append((new_key, str(v)))
        else:
            items.append((new_key, v))
            
    return dict(items)

def generate_simple_diff_content(self, file_key, format_type="text"):
    """Generate simple line-by-line diff content for display
    
    Args:
        file_key: File identifier key
        format_type: Format type (text, json, etc.)
        
    Returns:
        str: Formatted diff content for display
    """
    # Get diff data
    before_data = self._get_before_data(file_key)
    after_data = self._get_after_data(file_key)
    
    # Format based on type
    before_formatted = self.format_data_for_diff(before_data, format_type)
    after_formatted = self.format_data_for_diff(after_data, format_type)
    
    # Generate line-by-line diff
    diff_lines = []
    
    # Split into lines
    before_lines = before_formatted.splitlines()
    after_lines = after_formatted.splitlines()
    
    # Use difflib to get differences
    import difflib
    diff = difflib.ndiff(before_lines, after_lines)
    
    # Process diff
    for line in diff:
        if line.startswith('+ '):
            # Line added
            diff_lines.append(f'<span style="color:#00cc00">{line}</span>')
        elif line.startswith('- '):
            # Line removed
            diff_lines.append(f'<span style="color:#cc0000">{line}</span>')
        elif line.startswith('? '):
            # Hint line, skip in output
            continue
        else:
            # Unchanged line
            diff_lines.append(line)
    
    return "<br>".join(diff_lines)

def generate_json_tree_diff(self, file_key):
    """Generate a JSON tree diff for display
    
    Args:
        file_key: File identifier key
        
    Returns:
        list: List of tree items for display
    """
    # Get diff data
    diff_data = self._get_diff_data(file_key)
    
    # Prepare tree items
    tree_items = []
    
    # Process added items
    for key, value in diff_data.get("added", {}).items():
        item = {
            "key": key,
            "value": str(value),
            "change_type": "added",
            "icon": "icons/added.png"
        }
        tree_items.append(item)
    
    # Process removed items
    for key, value in diff_data.get("removed", {}).items():
        item = {
            "key": key,
            "value": str(value),
            "change_type": "removed",
            "icon": "icons/removed.png"
        }
        tree_items.append(item)
    
    # Process changed items
    for key, value_dict in diff_data.get("changed", {}).items():
        item = {
            "key": key,
            "value": f"{value_dict.get('before', '')} → {value_dict.get('after', '')}",
            "change_type": "changed",
            "icon": "icons/changed.png"
        }
        tree_items.append(item)
    
    # Sort by key
    tree_items.sort(key=lambda x: x["key"])
    
    return tree_items

def generate_side_by_side_diff(self, file_key, format_type="json"):
    """Generate side-by-side diff content for display
    
    Args:
        file_key: File identifier key
        format_type: Format type (text, json, etc.)
        
    Returns:
        tuple: (before_content, after_content) for display
    """
    # Get diff data
    before_data = self._get_before_data(file_key)
    after_data = self._get_after_data(file_key)
    
    # Format based on type
    before_formatted = self.format_data_for_diff(before_data, format_type)
    after_formatted = self.format_data_for_diff(after_data, format_type)
    
    return (before_formatted, after_formatted)

def format_data_for_diff(self, data, format_type="json"):
    """Format data for diff display
    
    Args:
        data: Data to format
        format_type: Format type (json, text, etc.)
        
    Returns:
        str: Formatted data string
    """
    if format_type == "json":
        # Pretty-print JSON
        return json.dumps(data, indent=2, sort_keys=True)
    elif format_type == "text":
        # Basic text representation
        return str(data)
    else:
        # Default to JSON
        return json.dumps(data, indent=2, sort_keys=True)

def _get_diff_data(self, file_key):
    """Get diff data for a specific file
    
    Args:
        file_key: File identifier key
        
    Returns:
        dict: Diff data dictionary
    """
    # In a real implementation, this would look up the actual diff data
    # For now, return a simple example diff
    
    # Check if this key is in the diff cache
    if file_key in self.diff_cache:
        return self.diff_cache[file_key]
    
    # If not found, generate a new diff
    file_parts = file_key.split("-")
    if len(file_parts) == 2:
        try:
            before_index = int(file_parts[0])
            after_index = int(file_parts[1])
            
            if before_index < len(self.comparison_data) and after_index < len(self.comparison_data):
                before_data = self.comparison_data[before_index]
                after_data = self.comparison_data[after_index]
                
                # Compute and cache diff
                diff = self._compute_file_diff(before_data, after_data)
                self.diff_cache[file_key] = diff
                
                return diff
        except ValueError:
            pass
    
    # Default empty diff
    return {"added": {}, "removed": {}, "changed": {}, "unchanged": {}, "pattern_changes": []}

def _get_before_data(self, file_key):
    """Get 'before' data for a specific file
    
    Args:
        file_key: File identifier key
        
    Returns:
        dict: Before data dictionary
    """
    file_parts = file_key.split("-")
    if len(file_parts) == 2:
        try:
            before_index = int(file_parts[0])
            if before_index < len(self.comparison_data):
                return self.comparison_data[before_index]
        except ValueError:
            pass
    
    return {}

def _get_after_data(self, file_key):
    """Get 'after' data for a specific file
    
    Args:
        file_key: File identifier key
        
    Returns:
        dict: After data dictionary
    """
    file_parts = file_key.split("-")
    if len(file_parts) == 2:
        try:
            after_index = int(file_parts[1])
            if after_index < len(self.comparison_data):
                return self.comparison_data[after_index]
        except ValueError:
            pass
    
    return {}
