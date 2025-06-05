#!/usr/bin/env python3
"""
History Screen for Pawprinting PyQt6 Application

Provides interface to view, search, and manage previous pawprint generations.

Author: AIMF LLC
Date: June 3, 2025
"""

import logging
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from PyQt6.QtCore import Qt, pyqtSignal, QSortFilterProxyModel, QDate
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableView, QHeaderView, QComboBox, QLineEdit, QFormLayout,
    QGroupBox, QDateEdit, QMessageBox, QSplitter, QTabWidget
)

# Import database modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import (
    get_database, get_recent_pawprints, search_pawprints, get_pawprint_by_id,
    get_database_stats, get_run_history
)

from utilities.notification import NotificationManager

# Set up logging
logger = logging.getLogger(__name__)

class HistoryScreen(QWidget):
    """
    Screen for viewing and managing pawprint history.
    
    Allows searching, filtering, and loading of past pawprint generations.
    """
    
    # Signals
    loadPawprint = pyqtSignal(dict)  # Signal to load a pawprint into the fractal screen
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Load initial data
        self.refresh_data()
    
    def setup_ui(self):
        """Set up the UI components"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title
        title_label = QLabel("Pawprint History", self)
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        main_layout.addWidget(title_label)
        
        # Splitter for search/filters and results
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left side - Search and filters
        search_widget = QWidget()
        search_layout = QVBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 10, 0)
        
        # Search group
        search_group = QGroupBox("Search & Filters")
        search_content_layout = QVBoxLayout(search_group)
        
        # Text search
        text_search_layout = QHBoxLayout()
        text_search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, text, or signature...")
        self.search_input.textChanged.connect(self.apply_filters)
        text_search_layout.addWidget(text_search_label)
        text_search_layout.addWidget(self.search_input)
        search_content_layout.addLayout(text_search_layout)
        
        # Date filters
        date_layout = QFormLayout()
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.dateChanged.connect(self.apply_filters)
        
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        self.date_to.dateChanged.connect(self.apply_filters)
        
        date_layout.addRow("From:", self.date_from)
        date_layout.addRow("To:", self.date_to)
        search_content_layout.addLayout(date_layout)
        
        # Entropy range
        entropy_layout = QHBoxLayout()
        entropy_label = QLabel("Entropy Range:")
        self.entropy_combo = QComboBox()
        self.entropy_combo.addItem("All", None)
        self.entropy_combo.addItem("Low (< 0.3)", "low")
        self.entropy_combo.addItem("Medium (0.3 - 0.7)", "medium")
        self.entropy_combo.addItem("High (> 0.7)", "high")
        self.entropy_combo.currentIndexChanged.connect(self.apply_filters)
        entropy_layout.addWidget(entropy_label)
        entropy_layout.addWidget(self.entropy_combo)
        search_content_layout.addLayout(entropy_layout)
        
        # Filter buttons
        button_layout = QHBoxLayout()
        self.apply_filter_btn = QPushButton("Apply Filters")
        self.apply_filter_btn.clicked.connect(self.apply_filters)
        self.clear_filter_btn = QPushButton("Clear Filters")
        self.clear_filter_btn.clicked.connect(self.clear_filters)
        button_layout.addWidget(self.apply_filter_btn)
        button_layout.addWidget(self.clear_filter_btn)
        search_content_layout.addLayout(button_layout)
        
        # Stats group
        stats_group = QGroupBox("Database Statistics")
        stats_layout = QVBoxLayout(stats_group)
        self.stats_label = QLabel("Loading statistics...")
        stats_layout.addWidget(self.stats_label)
        
        search_layout.addWidget(search_group)
        search_layout.addWidget(stats_group)
        search_layout.addStretch()
        
        splitter.addWidget(search_widget)
        
        # Right side - Results and details tabs
        results_widget = QTabWidget()
        
        # Results table panel
        results_tab = QWidget()
        results_layout = QVBoxLayout(results_tab)
        
        # Table for displaying pawprints
        self.pawprints_table = QTableView()
        self.pawprints_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.pawprints_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.pawprints_table.doubleClicked.connect(self.on_pawprint_double_clicked)
        
        # Set up table model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["ID", "Name", "Date", "Signature", "Entropy", "Actions"])
        
        # Set up sorting proxy model
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.model)
        self.pawprints_table.setModel(self.proxy_model)
        
        # Configure table columns
        self.pawprints_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.pawprints_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.pawprints_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        
        results_layout.addWidget(self.pawprints_table)
        
        # Action buttons for the selected pawprint
        actions_layout = QHBoxLayout()
        self.load_btn = QPushButton("Load Selected")
        self.load_btn.clicked.connect(self.on_load_clicked)
        self.load_btn.setEnabled(False)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        self.delete_btn.setEnabled(False)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_data)
        
        actions_layout.addWidget(self.load_btn)
        actions_layout.addWidget(self.delete_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(self.refresh_btn)
        
        results_layout.addLayout(actions_layout)
        
        results_widget.addTab(results_tab, "Pawprint History")
        
        # Add another tab for detailed statistics
        stats_tab = QWidget()
        stats_tab_layout = QVBoxLayout(stats_tab)
        stats_tab_layout.addWidget(QLabel("Detailed statistics will be implemented in a future update."))
        
        results_widget.addTab(stats_tab, "Usage Analytics")
        
        splitter.addWidget(results_widget)
        
        # Set splitter sizes
        splitter.setSizes([300, 700])
        
        # Connect selection signals
        self.pawprints_table.selectionModel().selectionChanged.connect(self.on_selection_changed)
    
    def refresh_data(self):
        """Refresh the data in the table"""
        try:
            # Clear existing data
            self.model.removeRows(0, self.model.rowCount())
            
            # Get recent pawprints
            pawprints = get_recent_pawprints(limit=100)
            
            # Populate table
            for pawprint in pawprints:
                row = []
                
                # ID
                id_item = QStandardItem(str(pawprint['id']))
                row.append(id_item)
                
                # Name
                name_item = QStandardItem(pawprint['name'])
                row.append(name_item)
                
                # Date
                try:
                    date_str = datetime.fromisoformat(pawprint['created_at']).strftime('%Y-%m-%d %H:%M')
                except:
                    date_str = str(pawprint['created_at'])
                date_item = QStandardItem(date_str)
                row.append(date_item)
                
                # Signature
                signature_item = QStandardItem(pawprint['signature'])
                row.append(signature_item)
                
                # Entropy
                entropy_item = QStandardItem(str(round(pawprint['text_entropy'], 3)) if pawprint['text_entropy'] else "N/A")
                row.append(entropy_item)
                
                # Store the ID for action buttons
                for item in row:
                    item.setData(pawprint['id'], Qt.ItemDataRole.UserRole)
                
                self.model.appendRow(row)
            
            # Update database stats
            self.refresh_stats()
            
            logger.info(f"Loaded {len(pawprints)} pawprints from database")
            
        except Exception as e:
            logger.error(f"Error refreshing data: {e}")
            QMessageBox.critical(self, "Database Error", f"Error loading pawprints: {e}")
    
    def refresh_stats(self):
        """Update the statistics display"""
        try:
            stats = get_database_stats()
            
            stats_text = (
                f"Total Pawprints: {stats['total_pawprints']}\n"
                f"Total Runs: {stats['total_runs']}\n"
                f"Average Entropy: {stats['avg_entropy']:.3f}\n"
                f"\n"
                f"Low Entropy: {stats.get('low_entropy_count', 0)}\n"
                f"Medium Entropy: {stats.get('medium_entropy_count', 0)}\n"
                f"High Entropy: {stats.get('high_entropy_count', 0)}\n"
            )
            
            if stats['first_pawprint_date'] and stats['last_pawprint_date']:
                first_date = datetime.fromisoformat(stats['first_pawprint_date']).strftime('%Y-%m-%d')
                last_date = datetime.fromisoformat(stats['last_pawprint_date']).strftime('%Y-%m-%d')
                stats_text += f"\nFirst Pawprint: {first_date}\nLatest Pawprint: {last_date}"
            
            self.stats_label.setText(stats_text)
            
        except Exception as e:
            logger.error(f"Error refreshing stats: {e}")
            self.stats_label.setText("Error loading statistics")
    
    def on_selection_changed(self, selected, deselected):
        """Handle selection change in the table"""
        has_selection = len(self.pawprints_table.selectionModel().selectedRows()) > 0
        self.load_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
    
    def on_pawprint_double_clicked(self, index):
        """Handle double-click on a pawprint row"""
        # Get the ID from the selected row
        proxy_index = index
        source_index = self.proxy_model.mapToSource(proxy_index)
        row_index = source_index.row()
        id_item = self.model.item(row_index, 0)
        
        if id_item:
            pawprint_id = id_item.data(Qt.ItemDataRole.UserRole)
            self.load_pawprint_by_id(pawprint_id)
    
    def on_load_clicked(self):
        """Load the selected pawprint"""
        selected_indexes = self.pawprints_table.selectionModel().selectedRows()
        if not selected_indexes:
            return
        
        # Get the ID from the selected row
        proxy_index = selected_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        row_index = source_index.row()
        id_item = self.model.item(row_index, 0)
        
        if id_item:
            pawprint_id = id_item.data(Qt.ItemDataRole.UserRole)
            self.load_pawprint_by_id(pawprint_id)
    
    def on_delete_clicked(self):
        """Delete the selected pawprint"""
        selected_indexes = self.pawprints_table.selectionModel().selectedRows()
        if not selected_indexes:
            return
        
        # Get the ID from the selected row
        proxy_index = selected_indexes[0]
        source_index = self.proxy_model.mapToSource(proxy_index)
        row_index = source_index.row()
        id_item = self.model.item(row_index, 0)
        
        if not id_item:
            return
        
        pawprint_id = id_item.data(Qt.ItemDataRole.UserRole)
        name_item = self.model.item(row_index, 1)
        pawprint_name = name_item.text()
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete the pawprint '{pawprint_name}' (ID: {pawprint_id})?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from database import delete_pawprint
                success = delete_pawprint(pawprint_id)
                
                if success:
                    self.refresh_data()
                    NotificationManager.show_info(f"Deleted pawprint: {pawprint_name}")
                else:
                    QMessageBox.warning(self, "Deletion Failed", f"Could not delete pawprint {pawprint_id}")
            except Exception as e:
                logger.error(f"Error deleting pawprint: {e}")
                QMessageBox.critical(self, "Database Error", f"Error deleting pawprint: {e}")
    
    def apply_filters(self):
        """Apply search filters to the pawprints table"""
        try:
            # Get filter parameters
            query = self.search_input.text() if self.search_input.text() else None
            
            # Entropy filter
            entropy_filter = self.entropy_combo.currentData()
            min_entropy = None
            max_entropy = None
            
            if entropy_filter == "low":
                max_entropy = 0.3
            elif entropy_filter == "medium":
                min_entropy = 0.3
                max_entropy = 0.7
            elif entropy_filter == "high":
                min_entropy = 0.7
            
            # Date filters
            start_date = self.date_from.date().toString(Qt.DateFormat.ISODate) if self.date_from.date() else None
            end_date = self.date_to.date().toString(Qt.DateFormat.ISODate) if self.date_to.date() else None
            
            # Only search if we have actual filters
            if any([query, min_entropy is not None, max_entropy is not None, start_date, end_date]):
                results = search_pawprints(
                    query=query,
                    min_entropy=min_entropy,
                    max_entropy=max_entropy,
                    start_date=start_date,
                    end_date=end_date
                )
                
                # Clear and repopulate the table
                self.model.removeRows(0, self.model.rowCount())
                
                for pawprint in results:
                    row = []
                    
                    # ID
                    id_item = QStandardItem(str(pawprint['id']))
                    row.append(id_item)
                    
                    # Name
                    name_item = QStandardItem(pawprint['name'])
                    row.append(name_item)
                    
                    # Date
                    try:
                        date_str = datetime.fromisoformat(pawprint['created_at']).strftime('%Y-%m-%d %H:%M')
                    except:
                        date_str = str(pawprint['created_at'])
                    date_item = QStandardItem(date_str)
                    row.append(date_item)
                    
                    # Signature
                    signature_item = QStandardItem(pawprint['signature'])
                    row.append(signature_item)
                    
                    # Entropy
                    entropy_item = QStandardItem(str(round(pawprint['text_entropy'], 3)) if pawprint['text_entropy'] else "N/A")
                    row.append(entropy_item)
                    
                    # Store the ID for action buttons
                    for item in row:
                        item.setData(pawprint['id'], Qt.ItemDataRole.UserRole)
                    
                    self.model.appendRow(row)
                
                logger.info(f"Search filter applied, found {len(results)} results")
            else:
                # No filters, show all
                self.refresh_data()
            
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            QMessageBox.critical(self, "Search Error", f"Error searching pawprints: {e}")
    
    def clear_filters(self):
        """Clear all search filters"""
        self.search_input.clear()
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_to.setDate(QDate.currentDate())
        self.entropy_combo.setCurrentIndex(0)
        self.refresh_data()
    
    def load_pawprint_by_id(self, pawprint_id):
        """Load a pawprint by its ID"""
        try:
            pawprint_data = get_pawprint_by_id(pawprint_id)
            
            if not pawprint_data or not pawprint_data.get('params'):
                QMessageBox.warning(self, "Load Error", f"Could not load pawprint data for ID {pawprint_id}")
                return
            
            # Log the run
            try:
                from database import log_run
                log_run(pawprint_id, notes="Loaded from History screen")
            except Exception as e:
                logger.warning(f"Failed to log run: {e}")
            
            # Emit signal with parameters
            self.loadPawprint.emit(pawprint_data['params'])
            
            # Show success
            NotificationManager.show_info(f"Loaded pawprint: {pawprint_data['name']}")
            
        except Exception as e:
            logger.error(f"Error loading pawprint: {e}")
            QMessageBox.critical(self, "Database Error", f"Error loading pawprint: {e}")
