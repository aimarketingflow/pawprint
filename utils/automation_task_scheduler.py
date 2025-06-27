#!/usr/bin/env python3
"""
Task Scheduler for Pawprinting PyQt6 V2 Automation

Manages scheduling of tasks to run at specific times or on recurring intervals.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import logging
import threading
import time
import uuid
from enum import Enum
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple, Callable

from PyQt6.QtCore import QObject, pyqtSignal, QTimer, QDateTime, QTime

from utils.automation_action_base import Action
from utils.automation_task_result import TaskExecutionResult
from utils.automation_task_types import TaskExecutionStatus, TaskTriggerType
from utils.automation_task_manager import get_task_manager

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.automation.task_scheduler")

class ScheduleType(Enum):
    """Types of task schedules"""
    ONE_TIME = "one_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    INTERVAL = "interval"  # Every X minutes/hours

class TaskSchedule:
    """Represents a scheduled task"""
    
    def __init__(self, 
                 schedule_id: str,
                 task_id: str,
                 action: Action,
                 schedule_type: ScheduleType,
                 config: Dict[str, Any] = None):
        """Initialize task schedule"""
        self.schedule_id = schedule_id
        self.task_id = task_id
        self.action = action
        self.schedule_type = schedule_type
        self.config = config or {}
        self.enabled = True
        self.next_run_time = self._calculate_next_run()
        self.last_run_time = None
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "schedule_id": self.schedule_id,
            "task_id": self.task_id,
            "action_id": self.action.action_id,
            "action_config": self.action.config,
            "schedule_type": self.schedule_type.value,
            "config": self.config,
            "enabled": self.enabled,
            "next_run_time": self.next_run_time.isoformat() if self.next_run_time else None,
            "last_run_time": self.last_run_time.isoformat() if self.last_run_time else None
        }
        
    @staticmethod
    def from_dict(data: Dict[str, Any], action_factory: Callable[[str, Dict[str, Any]], Action]) -> 'TaskSchedule':
        """Create from dictionary"""
        action = action_factory(data["action_id"], data["action_config"])
        
        schedule = TaskSchedule(
            schedule_id=data["schedule_id"],
            task_id=data["task_id"],
            action=action,
            schedule_type=ScheduleType(data["schedule_type"]),
            config=data["config"]
        )
        
        schedule.enabled = data.get("enabled", True)
        
        if data.get("next_run_time"):
            schedule.next_run_time = datetime.fromisoformat(data["next_run_time"])
        
        if data.get("last_run_time"):
            schedule.last_run_time = datetime.fromisoformat(data["last_run_time"])
            
        return schedule
    
    def _calculate_next_run(self) -> Optional[datetime]:
        """Calculate the next run time based on schedule type"""
        now = datetime.now()
        
        if self.schedule_type == ScheduleType.ONE_TIME:
            # One time schedule
            if "run_time" in self.config:
                run_time = datetime.fromisoformat(self.config["run_time"])
                if run_time > now:
                    return run_time
            return None  # Past or invalid one-time schedule
            
        elif self.schedule_type == ScheduleType.INTERVAL:
            # Interval schedule (every X minutes/hours)
            interval_minutes = self.config.get("interval_minutes", 60)  # Default 1 hour
            
            # If we have a last run time, calculate from that
            if self.last_run_time:
                return self.last_run_time + timedelta(minutes=interval_minutes)
            else:
                # First run - start after delay or now
                delay_minutes = self.config.get("initial_delay_minutes", 0)
                return now + timedelta(minutes=delay_minutes)
                
        elif self.schedule_type == ScheduleType.DAILY:
            # Daily schedule at specific time
            hour = self.config.get("hour", 0)
            minute = self.config.get("minute", 0)
            
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If the time today is already past, move to tomorrow
            if next_run <= now:
                next_run = next_run + timedelta(days=1)
                
            return next_run
            
        elif self.schedule_type == ScheduleType.WEEKLY:
            # Weekly schedule on specific days at specific time
            days = self.config.get("days", [0])  # Default Monday (0=Monday in our config)
            hour = self.config.get("hour", 0)
            minute = self.config.get("minute", 0)
            
            # Convert to Python's day of week (0=Monday in our config, but weekday() gives 0=Monday)
            today_weekday = now.weekday()
            
            # Find the next day in our schedule
            days_until_next = None
            for day in sorted(days):
                if day > today_weekday:
                    days_until_next = day - today_weekday
                    break
            
            # If not found or we've passed all days this week, wrap to next week
            if days_until_next is None:
                days_until_next = 7 - today_weekday + min(days)
                
            next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            next_run = next_run + timedelta(days=days_until_next)
            
            # If today is the day but the time is past, go to next occurrence
            if days_until_next == 0 and next_run <= now:
                # Move to next week
                next_run = next_run + timedelta(days=7)
                
            return next_run
            
        elif self.schedule_type == ScheduleType.MONTHLY:
            # Monthly schedule on specific day of month
            day = self.config.get("day", 1)  # Default 1st of month
            hour = self.config.get("hour", 0)
            minute = self.config.get("minute", 0)
            
            # Start with this month
            next_run = now.replace(day=min(day, self._days_in_month(now)), 
                                  hour=hour, minute=minute, second=0, microsecond=0)
            
            # If already past this month's time, go to next month
            if next_run <= now:
                if now.month == 12:
                    next_month = now.replace(year=now.year + 1, month=1)
                else:
                    next_month = now.replace(month=now.month + 1)
                
                next_run = next_month.replace(
                    day=min(day, self._days_in_month(next_month)),
                    hour=hour, minute=minute, second=0, microsecond=0
                )
                
            return next_run
            
        # Default fallback
        return now + timedelta(days=1)
    
    def _days_in_month(self, date: datetime) -> int:
        """Get the number of days in the month"""
        if date.month == 12:
            next_month = date.replace(year=date.year + 1, month=1, day=1)
        else:
            next_month = date.replace(month=date.month + 1, day=1)
        
        return (next_month - timedelta(days=1)).day
    
    def update_next_run(self) -> Optional[datetime]:
        """Update the next run time after a run"""
        self.last_run_time = datetime.now()
        self.next_run_time = self._calculate_next_run()
        return self.next_run_time
    
    def is_due(self) -> bool:
        """Check if the schedule is due to run"""
        if not self.enabled:
            return False
        
        if self.next_run_time is None:
            return False
            
        return datetime.now() >= self.next_run_time

class TaskScheduler(QObject):
    """Manages scheduled tasks"""
    
    # Signals
    schedule_added = pyqtSignal(str)  # schedule_id
    schedule_updated = pyqtSignal(str)  # schedule_id
    schedule_removed = pyqtSignal(str)  # schedule_id
    schedule_triggered = pyqtSignal(str, str)  # schedule_id, task_id
    
    def __init__(self):
        """Initialize task scheduler"""
        super().__init__()
        self._schedules = {}  # schedule_id -> TaskSchedule
        self._timer = QTimer()
        self._timer.timeout.connect(self._check_schedules)
        self._timer.setInterval(60 * 1000)  # Check every minute
        self._running = False
        self._task_manager = get_task_manager()
    
    def start(self) -> bool:
        """Start the scheduler"""
        if self._running:
            return False
            
        self._timer.start()
        self._running = True
        logger.info("Task scheduler started")
        return True
    
    def stop(self) -> bool:
        """Stop the scheduler"""
        if not self._running:
            return False
            
        self._timer.stop()
        self._running = False
        logger.info("Task scheduler stopped")
        return True
    
    def is_running(self) -> bool:
        """Check if scheduler is running"""
        return self._running
    
    def add_schedule(self, schedule: TaskSchedule) -> bool:
        """Add a new schedule"""
        if schedule.schedule_id in self._schedules:
            logger.warning(f"Schedule with ID {schedule.schedule_id} already exists")
            return False
            
        self._schedules[schedule.schedule_id] = schedule
        self.schedule_added.emit(schedule.schedule_id)
        logger.info(f"Added schedule {schedule.schedule_id} for task {schedule.task_id}")
        return True
    
    def update_schedule(self, schedule_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing schedule"""
        if schedule_id not in self._schedules:
            logger.warning(f"Schedule with ID {schedule_id} does not exist")
            return False
            
        schedule = self._schedules[schedule_id]
        
        # Apply updates
        for key, value in updates.items():
            if key == "enabled":
                schedule.enabled = value
            elif key == "config":
                schedule.config = value
                # Recalculate next run time
                schedule.next_run_time = schedule._calculate_next_run()
            elif key == "schedule_type" and isinstance(value, str):
                schedule.schedule_type = ScheduleType(value)
                # Recalculate next run time
                schedule.next_run_time = schedule._calculate_next_run()
        
        self.schedule_updated.emit(schedule_id)
        logger.info(f"Updated schedule {schedule_id}")
        return True
    
    def remove_schedule(self, schedule_id: str) -> bool:
        """Remove a schedule"""
        if schedule_id not in self._schedules:
            logger.warning(f"Schedule with ID {schedule_id} does not exist")
            return False
            
        del self._schedules[schedule_id]
        self.schedule_removed.emit(schedule_id)
        logger.info(f"Removed schedule {schedule_id}")
        return True
    
    def get_schedule(self, schedule_id: str) -> Optional[TaskSchedule]:
        """Get a schedule by ID"""
        return self._schedules.get(schedule_id)
    
    def get_all_schedules(self) -> List[TaskSchedule]:
        """Get all schedules"""
        return list(self._schedules.values())
    
    def _check_schedules(self) -> None:
        """Check schedules for execution"""
        now = datetime.now()
        
        for schedule_id, schedule in list(self._schedules.items()):
            if schedule.is_due():
                logger.info(f"Schedule {schedule_id} is due, executing task {schedule.task_id}")
                
                # Execute the task
                task_id = f"{schedule.task_id}_scheduled_{uuid.uuid4().hex[:8]}"
                success = self._task_manager.execute_task(
                    task_id,
                    schedule.action,
                    {"variables": {"schedule_id": schedule_id}}
                )
                
                if success:
                    self.schedule_triggered.emit(schedule_id, task_id)
                    
                    # Update next run time
                    schedule.update_next_run()
                    
                    # For one-time schedules, remove after execution
                    if schedule.schedule_type == ScheduleType.ONE_TIME:
                        self.remove_schedule(schedule_id)
                else:
                    logger.error(f"Failed to execute task for schedule {schedule_id}")

# Singleton instance
_instance = None

def get_task_scheduler() -> TaskScheduler:
    """Get the singleton task scheduler instance"""
    global _instance
    if _instance is None:
        _instance = TaskScheduler()
    return _instance
