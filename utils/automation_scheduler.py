#!/usr/bin/env python3
"""
Automation Scheduler for Pawprinting PyQt6 V2

Provides scheduling functionality for the Automation Manager, including one-time,
recurring, and conditional scheduling of tasks.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import time
import logging
import threading
import queue
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Tuple
from datetime import datetime, timedelta
import calendar
import heapq

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QDateTime

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.scheduler")

class ScheduleType(Enum):
    """Types of schedule for automation tasks"""
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    INTERVAL = "interval"
    CONDITIONAL = "conditional"

class Weekday(Enum):
    """Days of the week for scheduling"""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

class TaskScheduler(QObject):
    """
    Manages the scheduling of automation tasks
    """
    
    # Signals
    task_due = pyqtSignal(str)  # task_id
    schedule_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize task scheduler"""
        super().__init__(parent)
        
        # Scheduled tasks - {task_id: (next_run_time, schedule_info)}
        self.scheduled_tasks = {}
        
        # Priority queue of tasks ordered by next run time
        self.task_queue = []
        
        # Timer to check for due tasks
        self.check_timer = QTimer(self)
        self.check_timer.setInterval(30000)  # Check every 30 seconds
        self.check_timer.timeout.connect(self.check_due_tasks)
        
        # Thread-safe operation
        self.queue_lock = threading.RLock()
        
        logger.debug("Task Scheduler initialized")
    
    def start(self):
        """Start the scheduler"""
        self.check_timer.start()
        logger.info("Task scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.check_timer.stop()
        logger.info("Task scheduler stopped")
    
    def schedule_task(self, task_id: str, schedule_info: Dict[str, Any]) -> bool:
        """
        Schedule a task for execution
        
        Args:
            task_id: Unique ID of the task
            schedule_info: Dictionary containing schedule information
                Required keys:
                - type: ScheduleType - The type of schedule
                For ONE_TIME:
                - datetime: ISO format datetime string for execution
                For DAILY:
                - time: ISO format time string (HH:MM:SS)
                For WEEKLY:
                - time: ISO format time string (HH:MM:SS)
                - days: List of Weekday values
                For MONTHLY:
                - time: ISO format time string (HH:MM:SS)
                - day: Day of month (1-31) or "last"
                For INTERVAL:
                - interval: Seconds between executions
                - start_delay: Optional seconds to delay first execution
                For CONDITIONAL:
                - condition: Name of predefined condition
                - parameters: Dictionary of parameters for the condition
        
        Returns:
            success: True if task was scheduled successfully
        """
        try:
            # Validate schedule info
            if "type" not in schedule_info:
                raise ValueError("Schedule info missing required 'type' field")
            
            schedule_type = schedule_info["type"]
            
            # Calculate next execution time based on schedule type
            next_run = self._calculate_next_run(schedule_info)
            
            if next_run is None:
                logger.warning(f"Could not determine next run time for task {task_id}")
                return False
            
            # Add to scheduled tasks with lock for thread safety
            with self.queue_lock:
                self.scheduled_tasks[task_id] = (next_run, schedule_info)
                
                # Update priority queue
                heapq.heappush(self.task_queue, (next_run.timestamp(), task_id))
            
            # Signal that schedule was updated
            self.schedule_updated.emit()
            
            logger.info(f"Scheduled task {task_id} for next execution at {next_run.isoformat()}")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling task {task_id}: {str(e)}")
            return False
    
    def unschedule_task(self, task_id: str) -> bool:
        """
        Remove a task from the schedule
        
        Args:
            task_id: ID of the task to unschedule
        
        Returns:
            success: True if task was unscheduled
        """
        with self.queue_lock:
            if task_id in self.scheduled_tasks:
                # Remove from scheduled tasks
                del self.scheduled_tasks[task_id]
                
                # Rebuild priority queue to remove this task
                # This is inefficient but ensures consistency
                self.task_queue = [(timestamp, tid) for timestamp, tid in self.task_queue if tid != task_id]
                heapq.heapify(self.task_queue)
                
                # Signal that schedule was updated
                self.schedule_updated.emit()
                
                logger.info(f"Unscheduled task {task_id}")
                return True
            else:
                logger.warning(f"Attempted to unschedule non-existent task: {task_id}")
                return False
    
    def update_task_schedule(self, task_id: str, schedule_info: Dict[str, Any]) -> bool:
        """
        Update the schedule for an existing task
        
        Args:
            task_id: ID of the task to update
            schedule_info: New schedule information
        
        Returns:
            success: True if schedule was updated
        """
        # First unschedule the task if it exists
        if task_id in self.scheduled_tasks:
            self.unschedule_task(task_id)
        
        # Then schedule with new info
        return self.schedule_task(task_id, schedule_info)
    
    def check_due_tasks(self):
        """Check for tasks that are due to run"""
        now = datetime.now()
        due_tasks = []
        
        with self.queue_lock:
            # Check if any tasks are due
            while self.task_queue and self.task_queue[0][0] <= now.timestamp():
                # Get the earliest task
                _, task_id = heapq.heappop(self.task_queue)
                
                if task_id in self.scheduled_tasks:
                    # Add to due tasks list
                    due_tasks.append(task_id)
                    
                    # Get schedule info
                    next_run, schedule_info = self.scheduled_tasks[task_id]
                    
                    # Calculate next run time for recurring schedules
                    if schedule_info["type"] not in [ScheduleType.ONE_TIME.value, "one_time"]:
                        # Calculate next occurrence
                        next_run = self._calculate_next_run(schedule_info, reference_time=next_run)
                        
                        if next_run is not None:
                            # Update scheduled tasks and priority queue
                            self.scheduled_tasks[task_id] = (next_run, schedule_info)
                            heapq.heappush(self.task_queue, (next_run.timestamp(), task_id))
                    else:
                        # One-time task, remove from scheduled tasks
                        del self.scheduled_tasks[task_id]
        
        # Emit signals for due tasks
        for task_id in due_tasks:
            logger.debug(f"Task due for execution: {task_id}")
            self.task_due.emit(task_id)
        
        if due_tasks:
            # Signal that schedule was updated
            self.schedule_updated.emit()
    
    def get_upcoming_tasks(self, count: int = 10) -> List[Tuple[str, datetime]]:
        """
        Get a list of upcoming tasks sorted by execution time
        
        Args:
            count: Maximum number of tasks to return
        
        Returns:
            tasks: List of (task_id, execution_time) tuples
        """
        with self.queue_lock:
            # Sort tasks by timestamp
            upcoming = sorted(
                [(next_run, task_id) for task_id, (next_run, _) in self.scheduled_tasks.items()],
                key=lambda x: x[0]
            )
            
            # Return the requested number of tasks
            return [(task_id, exec_time) for exec_time, task_id in upcoming[:count]]
    
    def _calculate_next_run(self, schedule_info: Dict[str, Any], 
                           reference_time: Optional[datetime] = None) -> Optional[datetime]:
        """
        Calculate the next execution time based on schedule information
        
        Args:
            schedule_info: Schedule information dictionary
            reference_time: Reference time for calculation (default: now)
            
        Returns:
            next_run: Next execution time, or None if schedule is invalid
        """
        if reference_time is None:
            now = datetime.now()
        else:
            now = reference_time
            
        schedule_type = schedule_info["type"]
        
        try:
            if schedule_type in [ScheduleType.ONE_TIME.value, "one_time"]:
                # One-time schedule
                if "datetime" not in schedule_info:
                    return None
                
                run_time = datetime.fromisoformat(schedule_info["datetime"])
                
                # If the time is in the past and we're calculating from now, return None
                if reference_time is None and run_time < now:
                    return None
                
                return run_time
                
            elif schedule_type in [ScheduleType.DAILY.value, "daily"]:
                # Daily schedule
                if "time" not in schedule_info:
                    return None
                
                # Parse time (HH:MM:SS)
                time_parts = schedule_info["time"].split(":")
                hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2]) if len(time_parts) > 2 else 0
                
                # Create datetime for today with the specified time
                next_run = now.replace(hour=hour, minute=minute, second=second, microsecond=0)
                
                # If this time has already passed today, move to tomorrow
                if next_run <= now:
                    next_run += timedelta(days=1)
                
                return next_run
                
            elif schedule_type in [ScheduleType.WEEKLY.value, "weekly"]:
                # Weekly schedule
                if "time" not in schedule_info or "days" not in schedule_info:
                    return None
                
                # Parse time (HH:MM:SS)
                time_parts = schedule_info["time"].split(":")
                hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2]) if len(time_parts) > 2 else 0
                
                # Get days to run (0=Monday, 6=Sunday)
                days = schedule_info["days"]
                if not days:
                    return None
                
                # Convert to integers if they are enum strings
                days = [int(day) if isinstance(day, int) else Weekday[day].value for day in days]
                
                # Current weekday (0=Monday, 6=Sunday)
                current_weekday = now.weekday()
                
                # Find the next day to run
                days_ahead = None
                for day in sorted(days):
                    if day > current_weekday:
                        days_ahead = day - current_weekday
                        break
                
                # If no day is found, wrap around to the first day next week
                if days_ahead is None:
                    days_ahead = 7 + min(days) - current_weekday
                
                # Calculate next run date
                next_date = now.date() + timedelta(days=days_ahead)
                
                # Create datetime with the specified time
                next_run = datetime.combine(next_date, 
                                           datetime.min.time().replace(hour=hour, minute=minute, second=second))
                
                # If this time has already passed today and it's the same day, move to next week
                if days_ahead == 0 and next_run <= now:
                    next_run += timedelta(days=7)
                
                return next_run
                
            elif schedule_type in [ScheduleType.MONTHLY.value, "monthly"]:
                # Monthly schedule
                if "time" not in schedule_info or "day" not in schedule_info:
                    return None
                
                # Parse time (HH:MM:SS)
                time_parts = schedule_info["time"].split(":")
                hour, minute, second = int(time_parts[0]), int(time_parts[1]), int(time_parts[2]) if len(time_parts) > 2 else 0
                
                # Get the day of the month to run
                day = schedule_info["day"]
                
                # Calculate the next run date
                if day == "last":
                    # Last day of the month
                    if now.month == 12:
                        year, month = now.year + 1, 1
                    else:
                        year, month = now.year, now.month + 1
                    
                    # Get the last day of the current or next month
                    _, last_day = calendar.monthrange(year, month)
                    next_date = datetime(year, month, last_day)
                else:
                    day = int(day)
                    
                    # Get current year and month
                    year, month = now.year, now.month
                    
                    # Check if the day is valid for this month
                    _, last_day = calendar.monthrange(year, month)
                    if day > last_day:
                        day = last_day
                    
                    # Create date for this month
                    this_month = datetime(year, month, day)
                    
                    # If this date has already passed, move to next month
                    if this_month <= now:
                        # Move to next month
                        if month == 12:
                            year, month = year + 1, 1
                        else:
                            month += 1
                        
                        # Check if the day is valid for the next month
                        _, last_day = calendar.monthrange(year, month)
                        if day > last_day:
                            day = last_day
                    
                    next_date = datetime(year, month, day)
                
                # Create datetime with the specified time
                next_run = next_date.replace(hour=hour, minute=minute, second=second, microsecond=0)
                
                return next_run
                
            elif schedule_type in [ScheduleType.INTERVAL.value, "interval"]:
                # Interval schedule
                if "interval" not in schedule_info:
                    return None
                
                # Get interval in seconds
                interval = int(schedule_info["interval"])
                
                # Apply optional start delay for the first execution
                if reference_time is None and "start_delay" in schedule_info:
                    start_delay = int(schedule_info["start_delay"])
                    next_run = now + timedelta(seconds=start_delay)
                else:
                    # Calculate next interval from reference or now
                    next_run = now + timedelta(seconds=interval)
                
                return next_run
                
            elif schedule_type in [ScheduleType.CONDITIONAL.value, "conditional"]:
                # Conditional schedule
                # For conditional schedules, we don't calculate a next run time
                # These are triggered by external conditions
                return None
                
            else:
                logger.warning(f"Unknown schedule type: {schedule_type}")
                return None
                
        except Exception as e:
            logger.error(f"Error calculating next run time: {str(e)}")
            return None
