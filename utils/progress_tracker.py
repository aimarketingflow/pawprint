#!/usr/bin/env python3
"""
Progress Tracker for Pawprinting PyQt6 Application

Provides robust progress tracking with proper signals for updating UI.
Includes calculation of estimated time remaining and other metrics.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple

from PyQt6.QtCore import QObject, pyqtSignal, QTimer

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.progress_tracker")


class ProgressTracker(QObject):
    """
    Progress tracking with proper signals for updating UI
    """
    # Signal emitted when progress is updated
    progress_updated = pyqtSignal(int, str)  # percentage, message
    
    # Signal emitted when operation is completed
    operation_completed = pyqtSignal(bool, str)  # success, message
    
    # Signal for more detailed progress information
    detailed_progress = pyqtSignal(dict)  # Dictionary with detailed progress info
    
    def __init__(self, parent=None):
        """Initialize progress tracker"""
        super().__init__(parent)
        self.start_time = None
        self.last_update_time = None
        self.total_items = 0
        self._completed_items = 0
        self._current_message = ""
        self._operation_name = ""
        self._is_running = False
        
        # For rate calculation
        self._progress_history = []  # List of (timestamp, completed_items)
        self._max_history_points = 10  # Number of history points to keep
    
    def start(self, total_items: int, operation_name: str = "Processing") -> None:
        """
        Start a new progress tracking operation
        
        Args:
            total_items: Total number of items to process
            operation_name: Name of the operation for display
        """
        self.start_time = datetime.now()
        self.last_update_time = self.start_time
        self.total_items = total_items
        self._completed_items = 0
        self._current_message = f"Starting {operation_name}..."
        self._operation_name = operation_name
        self._is_running = True
        self._progress_history = [(self.start_time, 0)]
        
        logger.info(f"Starting {operation_name} with {total_items} total items")
        
        # Emit initial progress
        self._emit_progress(0, f"Starting {operation_name}...")
    
    def update(self, completed_items: int, message: Optional[str] = None) -> None:
        """
        Update progress with completed items count and optional message
        
        Args:
            completed_items: Number of items completed
            message: Optional status message
        """
        if not self._is_running:
            logger.warning("Trying to update progress but no operation is running")
            return
        
        self._completed_items = completed_items
        now = datetime.now()
        self.last_update_time = now
        
        if message:
            self._current_message = message
        
        # Calculate percentage
        percentage = int((completed_items / self.total_items) * 100) if self.total_items else 0
        
        # Add to history for rate calculation
        self._progress_history.append((now, completed_items))
        
        # Keep history at manageable size
        if len(self._progress_history) > self._max_history_points:
            self._progress_history = self._progress_history[-self._max_history_points:]
        
        # Calculate ETA and rate
        eta_text, rate = self._calculate_metrics()
        
        # Create status message
        if message:
            status_message = f"{message} - {percentage}% ({completed_items}/{self.total_items}) - {eta_text}"
        else:
            status_message = f"{percentage}% ({completed_items}/{self.total_items}) - {eta_text}"
        
        # Log progress
        if percentage % 10 == 0 or completed_items == self.total_items:  # Log every 10% or at completion
            logger.info(f"Progress update: {status_message}")
        else:
            logger.debug(f"Progress update: {status_message}")
        
        # Emit progress update
        self._emit_progress(percentage, status_message)
    
    def complete(self, success: bool = True, message: Optional[str] = None) -> None:
        """
        Mark the operation as complete
        
        Args:
            success: Whether the operation completed successfully
            message: Optional completion message
        """
        if not self._is_running:
            logger.warning("Trying to complete progress but no operation is running")
            return
        
        self._is_running = False
        completion_time = datetime.now()
        
        if self.start_time:
            elapsed = (completion_time - self.start_time).total_seconds()
            completion_message = f"{message or 'Operation completed'} - Completed in {elapsed:.2f} seconds"
            
            if success:
                logger.info(f"Operation succeeded: {completion_message}")
            else:
                logger.error(f"Operation failed: {completion_message}")
            
            self.operation_completed.emit(success, completion_message)
        else:
            self.operation_completed.emit(success, message or "Operation completed")
    
    def is_running(self) -> bool:
        """Check if an operation is currently running"""
        return self._is_running
    
    def _calculate_metrics(self) -> Tuple[str, float]:
        """
        Calculate ETA and processing rate
        
        Returns:
            Tuple of (eta_text, items_per_second)
        """
        if len(self._progress_history) < 2:
            return "Calculating...", 0.0
        
        # Calculate items per second using recent history for stability
        oldest_time, oldest_count = self._progress_history[0]
        newest_time, newest_count = self._progress_history[-1]
        time_diff = (newest_time - oldest_time).total_seconds()
        count_diff = newest_count - oldest_count
        
        if time_diff > 0 and count_diff > 0:
            items_per_second = count_diff / time_diff
        else:
            # Fall back to overall rate if recent rate is zero
            elapsed = (self.last_update_time - self.start_time).total_seconds()
            items_per_second = self._completed_items / elapsed if elapsed > 0 else 0
        
        # Calculate ETA
        remaining_items = self.total_items - self._completed_items
        eta_seconds = remaining_items / items_per_second if items_per_second > 0 else 0
        
        # Format ETA text
        if eta_seconds < 1:
            eta_text = "Almost done"
        elif eta_seconds < 60:
            eta_text = f"ETA: {eta_seconds:.0f} seconds"
        elif eta_seconds < 3600:
            eta_minutes = eta_seconds / 60
            eta_text = f"ETA: {eta_minutes:.1f} minutes"
        else:
            eta_hours = eta_seconds / 3600
            eta_text = f"ETA: {eta_hours:.1f} hours"
        
        return eta_text, items_per_second
    
    def _emit_progress(self, percentage: int, message: str) -> None:
        """
        Emit progress signals with current status
        
        Args:
            percentage: Current percentage (0-100)
            message: Status message
        """
        # Emit basic progress signal
        self.progress_updated.emit(percentage, message)
        
        # Calculate detailed metrics for detailed progress signal
        elapsed = (self.last_update_time - self.start_time).total_seconds() if self.start_time else 0
        _, rate = self._calculate_metrics()
        
        # Create detailed progress info
        details = {
            "percentage": percentage,
            "message": message,
            "completed": self._completed_items,
            "total": self.total_items,
            "elapsed_seconds": elapsed,
            "items_per_second": rate,
            "operation_name": self._operation_name,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "is_running": self._is_running
        }
        
        # Emit detailed progress signal
        self.detailed_progress.emit(details)
