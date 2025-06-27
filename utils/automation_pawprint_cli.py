#!/usr/bin/env python3
"""
Command Line Interface for Pawprint Automation Tasks

Provides a command line interface for executing pawprint automation tasks,
including batch refresh operations.

Author: AIMF LLC
Date: June 20, 2025
"""

import os
import sys
import argparse
import logging
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Ensure the parent directory is in the path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(
            os.path.expanduser("~"),
            "Pawprinting_PyQt6_V2",
            "logs",
            f"pawprint_cli_{datetime.now().strftime('%Y%m%d-%H%M%S')}.log"
        ))
    ]
)

logger = logging.getLogger("pawprint_cli")

# Import automation components
from utils.automation_system import get_automation_system
from utils.automation_task_manager import get_task_manager
from utils.automation_pawprint_refresh_action import (
    PawprintRefreshAction,
    PawprintBatchRefreshAction,
    get_pawprint_history_manager
)
from utils.automation_task_context import TaskContext
from utils.automation_logging import get_log_manager

class ProgressBar:
    """Simple console progress bar"""
    
    def __init__(self, total_width=50):
        self.total_width = total_width
        self.last_progress = 0
        self.start_time = None
        
    def update(self, progress, message=""):
        """Update progress bar"""
        if self.start_time is None:
            self.start_time = time.time()
            
        if progress == self.last_progress:
            return
            
        self.last_progress = progress
        
        # Calculate elapsed time and ETA
        elapsed = time.time() - self.start_time
        eta = None
        if progress > 0:
            eta = elapsed * (100 - progress) / progress
            
        # Build progress bar
        filled_width = int(self.total_width * progress / 100)
        bar = '█' * filled_width + '░' * (self.total_width - filled_width)
        
        # Format time strings
        elapsed_str = self._format_time(elapsed)
        eta_str = self._format_time(eta) if eta is not None else "--:--:--"
        
        # Print progress
        print(f"\r[{bar}] {progress:3d}% | Elapsed: {elapsed_str} | ETA: {eta_str} | {message}", end='')
        
        if progress == 100:
            print("")  # New line when complete
            
    def _format_time(self, seconds):
        """Format seconds as HH:MM:SS"""
        if seconds is None:
            return "--:--:--"
            
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def init_automation_system():
    """Initialize the automation system"""
    logger.info("Initializing automation system...")
    system = get_automation_system()
    
    if not system.is_initialized():
        if not system.initialize():
            logger.error("Failed to initialize automation system")
            return False
            
    logger.info("Automation system initialized")
    return True

def list_history():
    """List pawprint history entries"""
    history_manager = get_pawprint_history_manager()
    entries = history_manager.get_entries()
    
    if not entries:
        print("No pawprint history entries found.")
        return
        
    print(f"\n{'-'*80}")
    print(f"{'INDEX':^6} | {'FOLDER PATH':^40} | {'LAST ANALYZED':^20} | {'STATUS':^10}")
    print(f"{'-'*80}")
    
    for i, entry in enumerate(entries):
        folder_path = entry.folder_path
        if len(folder_path) > 38:
            folder_path = "..." + folder_path[-35:]
            
        last_analyzed = entry.last_analyzed.strftime("%Y-%m-%d %H:%M:%S") if entry.last_analyzed else "Never"
        status = entry.metadata.get("success", "N/A")
        status_str = "Success" if status is True else "Failed" if status is False else "N/A"
        
        print(f"{i:^6} | {folder_path:<40} | {last_analyzed:^20} | {status_str:^10}")
        
    print(f"{'-'*80}\n")

def refresh_pawprints(args):
    """Refresh pawprints based on command line arguments"""
    # Initialize system
    if not init_automation_system():
        return False
    
    # Create configuration based on arguments
    config = {
        "action_id": f"cli_refresh_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "overwrite": not args.no_overwrite
    }
    
    # Set refresh type and related config
    if args.all:
        config["refresh_type"] = "all"
    elif args.recent:
        config["refresh_type"] = "recent"
        config["count"] = args.count
    elif args.folders:
        config["refresh_type"] = "specific"
        config["folders"] = args.folders
    else:
        config["refresh_type"] = "recent"  # Default
        config["count"] = 5  # Default
    
    # Set output folder if specified
    if args.output:
        config["output_folder"] = args.output
    
    # Create progress callback
    progress_bar = ProgressBar()
    
    def progress_callback(progress):
        """Update progress bar"""
        progress_bar.update(progress, "Refreshing pawprints...")
    
    # Create action
    action = PawprintBatchRefreshAction(config["action_id"], config)
    
    # Connect progress signal
    action.progress_changed.connect(progress_callback)
    
    # Create task context
    context = TaskContext(config["action_id"], variables={})
    
    # Execute action
    logger.info(f"Starting pawprint refresh: {config}")
    print(f"Starting pawprint refresh operation...")
    
    start_time = time.time()
    success = action.execute(context)
    end_time = time.time()
    
    # Show result
    duration = end_time - start_time
    duration_str = progress_bar._format_time(duration)
    
    print(f"\nPawprint refresh {'completed successfully' if success else 'failed'}")
    print(f"Total execution time: {duration_str}")
    
    return success

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Pawprint Automation CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # History command
    history_parser = subparsers.add_parser('history', help='List pawprint history')
    
    # Refresh command
    refresh_parser = subparsers.add_parser('refresh', help='Refresh pawprints')
    refresh_group = refresh_parser.add_mutually_exclusive_group()
    refresh_group.add_argument('--all', action='store_true', help='Refresh all known folders')
    refresh_group.add_argument('--recent', action='store_true', help='Refresh most recent folders')
    refresh_group.add_argument('--folders', nargs='+', help='Refresh specific folders')
    
    refresh_parser.add_argument('--count', type=int, default=5, help='Number of recent folders to refresh (default: 5)')
    refresh_parser.add_argument('--output', type=str, help='Output folder for results')
    refresh_parser.add_argument('--no-overwrite', action='store_true', help='Do not overwrite existing pawprints')
    refresh_parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up debug logging if requested
    if hasattr(args, 'debug') and args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Execute command
    if args.command == 'history':
        list_history()
    elif args.command == 'refresh':
        refresh_pawprints(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
