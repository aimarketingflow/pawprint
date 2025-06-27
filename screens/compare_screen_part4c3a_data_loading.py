#!/usr/bin/env python3
"""
Compare Screen for Pawprinting PyQt6 Application - Part 4c-3a: Data Loading Methods

Implements the data loading methods for the Compare Screen.

Author: AIMF LLC
Date: June 6, 2025
"""

# This file contains methods for loading pawprint data that would be included in the CompareScreen class

def load_comparison_files(self, file_paths):
    """Load pawprint files for comparison
    
    Args:
        file_paths: List of paths to pawprint files to compare
        
    Returns:
        bool: True if loading was successful, False otherwise
    """
    # Reset current comparison data
    self.comparison_files = []
    self.comparison_data = []
    self.file_groups = {}
    self.diff_cache = {}
    
    # Check if we have enough files
    if len(file_paths) < 1:
        logger.error("At least one file is required for comparison")
        NotificationManager.show_error("At least one file is required for comparison")
        return False
    
    # Show progress dialog
    self.progress_tracker.start_operation("Loading pawprint files...")
    
    # Track loading success
    load_success = True
    
    # Load each file
    for i, file_path in enumerate(file_paths):
        progress = int((i / len(file_paths)) * 100)
        self.progress_tracker.update_progress(
            progress, f"Loading {os.path.basename(file_path)}..."
        )
        
        try:
            # Load pawprint file
            pawprint_data = self._load_pawprint_file(file_path)
            
            # Store file information
            self.comparison_files.append(file_path)
            self.comparison_data.append(pawprint_data)
            
        except Exception as e:
            logger.error(f"Error loading pawprint file {file_path}: {e}")
            NotificationManager.show_error(f"Error loading file: {os.path.basename(file_path)}")
            load_success = False
            break
    
    # If loading was successful, group files by origin
    if load_success:
        self._group_files_by_origin()
        
        # Complete operation
        self.progress_tracker.complete_operation(
            True, f"Successfully loaded {len(self.comparison_files)} pawprint files"
        )
    else:
        # Reset data
        self.comparison_files = []
        self.comparison_data = []
        self.file_groups = {}
        
        # Complete operation
        self.progress_tracker.complete_operation(
            False, "Failed to load pawprint files"
        )
    
    return load_success

def _load_pawprint_file(self, file_path):
    """Load a single pawprint file
    
    Args:
        file_path: Path to the pawprint file
        
    Returns:
        dict: Pawprint data dictionary
    
    Raises:
        Exception: If loading fails
    """
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        # Load JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Basic validation
        if not isinstance(data, dict):
            raise ValueError("Invalid pawprint format: root must be a dictionary")
        
        # Check for required sections
        if "metadata" not in data:
            logger.warning(f"Missing metadata section in {file_path}")
            data["metadata"] = {"origin": "unknown", "timestamp": "unknown"}
        
        # Add file path to metadata
        data["metadata"]["file_path"] = file_path
        
        return data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        raise Exception(f"Error loading file: {e}")

def _group_files_by_origin(self):
    """Group loaded files by their origin metadata"""
    # Reset file groups
    self.file_groups = {}
    
    # Group by origin
    for i, data in enumerate(self.comparison_data):
        # Get origin from metadata
        origin = data.get("metadata", {}).get("origin", "unknown")
        
        # Create group if it doesn't exist
        if origin not in self.file_groups:
            self.file_groups[origin] = []
        
        # Add file to group
        file_path = self.comparison_files[i]
        file_name = os.path.basename(file_path)
        
        self.file_groups[origin].append({
            "index": i,
            "name": file_name,
            "path": file_path,
            "data": data
        })
    
    # Sort files within each group by timestamp
    for origin in self.file_groups:
        self.file_groups[origin].sort(
            key=lambda x: x["data"].get("metadata", {}).get("timestamp", ""),
            reverse=False  # oldest to newest
        )

def on_file_selection_changed(self):
    """Handle file selection change in the sidebar file list"""
    # Get selected items
    selected_items = self.file_list.selectedItems()
    
    # Enable/disable remove button based on selection
    self.remove_file_button.setEnabled(len(selected_items) > 0)
    
    # Enable compare button if we have at least one file
    self.compare_button.setEnabled(len(self.file_list.findItems("*", Qt.MatchFlag.MatchWildcard)) > 0)

def on_add_file_clicked(self):
    """Handle add file button click"""
    # Open file dialog
    file_paths, _ = QFileDialog.getOpenFileNames(
        self,
        "Select Pawprint Files",
        "",
        "Pawprint Files (*.json);;All Files (*.*)"
    )
    
    # If files were selected, add them to the list
    if file_paths:
        for file_path in file_paths:
            # Check if file is already in the list
            file_name = os.path.basename(file_path)
            existing_items = self.file_list.findItems(file_name, Qt.MatchFlag.MatchExactly)
            
            if not existing_items:
                # Add to list
                item = QTreeWidgetItem([file_name])
                item.setData(0, Qt.ItemDataRole.UserRole, file_path)
                self.file_list.addTopLevelItem(item)
        
        # Enable compare button if we have files
        self.compare_button.setEnabled(True)

def on_remove_file_clicked(self):
    """Handle remove file button click"""
    # Get selected items
    selected_items = self.file_list.selectedItems()
    
    # Remove selected items
    for item in selected_items:
        index = self.file_list.indexOfTopLevelItem(item)
        self.file_list.takeTopLevelItem(index)
    
    # Enable/disable compare button based on remaining files
    self.compare_button.setEnabled(len(self.file_list.findItems("*", Qt.MatchFlag.MatchWildcard)) > 0)

def on_clear_files_clicked(self):
    """Handle clear all files button click"""
    # Clear file list
    self.file_list.clear()
    
    # Disable compare button
    self.compare_button.setEnabled(False)

def on_compare_clicked(self):
    """Handle compare button click"""
    # Collect file paths from list
    file_paths = []
    for i in range(self.file_list.topLevelItemCount()):
        item = self.file_list.topLevelItem(i)
        file_path = item.data(0, Qt.ItemDataRole.UserRole)
        file_paths.append(file_path)
    
    # Check if we have enough files
    if len(file_paths) < 1:
        NotificationManager.show_info("Add at least one file to compare")
        return
    
    # Load files
    if self.load_comparison_files(file_paths):
        # Update UI for comparison mode
        self.setup_comparison_ui()
        
        # Enable export button
        self.export_button.setEnabled(True)
        
        # Update all tabs
        self.update_comparison_tab()
        self.update_charts_tab()
        self.update_raw_data_tab()
        self.update_summary_tab()

def on_back_clicked(self):
    """Handle back button click"""
    # Emit back signal
    self.backClicked.emit()
