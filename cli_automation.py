#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cli_automation.py - Command Line Interface for Pawprinting PyQt6 V2 Automation

This module provides a comprehensive CLI for the automation system, allowing
users to manage pawprint history, trigger batch refreshes, and monitor
automation tasks from the terminal.

Usage:
    python3 cli_automation.py --list-history
    python3 cli_automation.py --refresh-all
    python3 cli_automation.py --refresh-recent [--days 7]
    python3 cli_automation.py --refresh-folder /path/to/folder
    python3 cli_automation.py --diagnostic

AIMF LLC - 2025
"""

import os
import sys
import time
import logging
import argparse
import datetime
from pathlib import Path

# Add project root to path if needed
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import automation components
from utils.automation_system import AutomationSystem
from utils.automation_pawprint_refresh_action import PawprintBatchRefreshAction
from utils.automation_task_manager import TaskContext
from utils.automation_pawprint_cli import (
    PawprintHistoryCommand,
    PawprintRefreshCommand,
    setup_pawprint_logging
)


def setup_logging(log_dir=None, verbose=False):
    """Configure logging for the CLI application"""
    if log_dir is None:
        log_dir = os.path.join(PROJECT_ROOT, 'logs')
    
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Create timestamp for log filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f'cli_automation_{timestamp}.log')
    
    # Configure logging
    log_level = logging.DEBUG if verbose else logging.INFO
    
    # Setup file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logging.info(f"Logging initialized. Log file: {log_file}")
    return log_file


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Pawprinting PyQt6 V2 Automation CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # Main action groups
    action_group = parser.add_argument_group('Actions')
    action_group.add_argument('--list-history', action='store_true', 
                             help='List pawprint history')
    action_group.add_argument('--refresh-all', action='store_true',
                             help='Refresh all pawprints in history')
    action_group.add_argument('--refresh-recent', action='store_true',
                             help='Refresh recently accessed pawprints')
    action_group.add_argument('--refresh-folder', type=str, metavar='PATH',
                             help='Refresh pawprint for a specific folder')
    
    # Options
    options_group = parser.add_argument_group('Options')
    options_group.add_argument('--days', type=int, default=7, metavar='N',
                              help='Number of days to consider as recent (default: 7)')
    options_group.add_argument('--verbose', '-v', action='store_true',
                              help='Enable verbose output')
    options_group.add_argument('--log-dir', type=str, metavar='DIR',
                              help='Custom log directory')
    options_group.add_argument('--data-dir', type=str, metavar='DIR',
                              help='Custom data directory')
    
    # Diagnostic mode
    diagnostic_group = parser.add_argument_group('Diagnostic Options')
    diagnostic_group.add_argument('--diagnostic', action='store_true',
                                 help='Run in diagnostic mode with test data')
    diagnostic_group.add_argument('--test-folder', type=str, metavar='PATH',
                                 help='Test folder for diagnostic mode')
    
    return parser.parse_args()


def run_diagnostic(args, automation_system):
    """Run system diagnostics"""
    logging.info("Starting diagnostic mode...")
    
    # Check system components
    components = {
        "Task Manager": automation_system.task_manager,
        "History Manager": automation_system.history_manager,
        "Scheduler": automation_system.scheduler,
        "Trigger Manager": automation_system.trigger_manager,
        "Factory": automation_system.factory
    }
    
    all_ok = True
    for name, component in components.items():
        if component is not None:
            logging.info(f"✅ {name}: OK")
        else:
            logging.error(f"❌ {name}: Missing or failed to initialize")
            all_ok = False
    
    # Check data and log directories
    data_dir = automation_system.data_dir
    log_dir = automation_system.log_dir
    
    if os.path.exists(data_dir) and os.access(data_dir, os.W_OK):
        logging.info(f"✅ Data directory: OK ({data_dir})")
    else:
        logging.error(f"❌ Data directory: Issue ({data_dir})")
        all_ok = False
    
    if os.path.exists(log_dir) and os.access(log_dir, os.W_OK):
        logging.info(f"✅ Log directory: OK ({log_dir})")
    else:
        logging.error(f"❌ Log directory: Issue ({log_dir})")
        all_ok = False
    
    # Test creating and executing a simple task
    try:
        logging.info("Testing task execution...")
        context = TaskContext()
        action_config = {
            "name": "Test action",
            "description": "Diagnostic test action"
        }
        context.config = action_config
        
        # Use the batch refresh action for testing
        action = PawprintBatchRefreshAction(context)
        
        # If a test folder was provided, use it
        if args.test_folder:
            test_path = os.path.abspath(args.test_folder)
            if os.path.exists(test_path) and os.path.isdir(test_path):
                action.folders = [test_path]
                logging.info(f"Using test folder: {test_path}")
            else:
                logging.warning(f"Test folder not found or not a directory: {test_path}")
        
        # For diagnostic, just run validation
        if action.validate():
            logging.info("✅ Task validation: OK")
        else:
            logging.error("❌ Task validation: Failed")
            all_ok = False
        
        logging.info("Diagnostic test completed.")
        
    except Exception as e:
        logging.error(f"❌ Task execution test failed: {str(e)}", exc_info=True)
        all_ok = False
    
    if all_ok:
        logging.info("🎉 All diagnostic tests passed!")
    else:
        logging.error("⚠️ Some diagnostic tests failed. Check the log for details.")
    
    return all_ok


def generate_summary(log_file):
    """Generate a summary markdown file of the CLI run"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = os.path.join(os.path.dirname(log_file), f'cli_summary_{timestamp}.md')
    
    with open(summary_file, 'w') as f:
        f.write(f"# Pawprinting PyQt6 V2 CLI Automation Summary\n\n")
        f.write(f"**Run Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Log File:** `{os.path.basename(log_file)}`\n\n")
        
        f.write("## Actions Executed\n\n")
        # Read the log file to extract key information
        try:
            with open(log_file, 'r') as log:
                lines = log.readlines()
                
                # Extract completed actions
                actions = []
                errors = []
                for line in lines:
                    if "completed successfully" in line.lower():
                        actions.append(line.strip())
                    elif "error" in line.lower():
                        errors.append(line.strip())
                
                if actions:
                    f.write("### Completed Actions\n\n")
                    for action in actions:
                        f.write(f"- {action}\n")
                    f.write("\n")
                
                if errors:
                    f.write("### Errors\n\n")
                    for error in errors:
                        f.write(f"- {error}\n")
                    f.write("\n")
        except Exception as e:
            f.write(f"Error generating summary details: {str(e)}\n\n")
        
        f.write("## Next Steps\n\n")
        f.write("- Review the complete log file for detailed information\n")
        f.write("- Check the results of any refresh operations\n")
        f.write("- Run `python3 cli_automation.py --list-history` to see updated pawprint history\n")
    
    logging.info(f"Summary generated: {summary_file}")
    return summary_file


def main():
    """Main entry point for the CLI application"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    log_file = setup_logging(args.log_dir, args.verbose)
    
    try:
        logging.info("Initializing automation system...")
        
        # Initialize the automation system
        automation_system = AutomationSystem(
            data_dir=args.data_dir,
            log_dir=args.log_dir
        )
        
        logging.info("Automation system initialized")
        
        # Run diagnostic mode if requested
        if args.diagnostic:
            success = run_diagnostic(args, automation_system)
            generate_summary(log_file)
            return 0 if success else 1
        
        # Initialize CLI commands
        history_command = PawprintHistoryCommand(automation_system.history_manager)
        refresh_command = PawprintRefreshCommand(automation_system)
        
        # Execute requested command
        if args.list_history:
            history_command.list_history()
        
        elif args.refresh_all:
            refresh_command.refresh_all()
        
        elif args.refresh_recent:
            refresh_command.refresh_recent(days=args.days)
        
        elif args.refresh_folder:
            folder_path = os.path.abspath(args.refresh_folder)
            refresh_command.refresh_folder(folder_path)
        
        else:
            logging.error("No action specified. Use --help for available commands.")
            return 1
        
        # Generate summary
        generate_summary(log_file)
        logging.info("CLI execution completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logging.info("Operation cancelled by user")
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)
        return 1
    finally:
        # Ensure the automation system is properly shut down
        if 'automation_system' in locals():
            automation_system.shutdown()


if __name__ == "__main__":
    sys.exit(main())
