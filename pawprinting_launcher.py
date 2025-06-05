#!/usr/bin/env python3
"""
Pawprinting PyQt6 V2 Application Launcher
-----------------------------------------
This script launches the Pawprinting PyQt6 V2 application with proper
environment setup and error handling.

AIMF LLC Digital Forensics
"""

import os
import sys
import logging
import subprocess
import traceback
from datetime import datetime

# Configure logging
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"pawprinting_launcher_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("PawprintingLauncher")

def check_environment():
    """Check if the virtual environment exists and PyQt6 is installed"""
    try:
        # Check if we're in a virtual environment
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            logger.info("Running in virtual environment")
        else:
            logger.warning("Not running in a virtual environment. Will attempt to use system Python.")

        # Check required packages
        import importlib.util
        required_packages = ['PyQt6', 'matplotlib', 'numpy']
        missing_packages = []
        
        for package in required_packages:
            spec = importlib.util.find_spec(package)
            if spec is None:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing required packages: {', '.join(missing_packages)}")
            return False
            
        logger.info("Environment check passed")
        return True
    except Exception as e:
        logger.error(f"Error checking environment: {str(e)}")
        return False

def launch_application():
    """Launch the Pawprinting PyQt6 V2 application"""
    try:
        logger.info("Launching Pawprinting PyQt6 V2 application...")
        
        # Get the main application path
        app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pawprint_pyqt6_main.py")
        
        if not os.path.exists(app_path):
            logger.error(f"Application file not found: {app_path}")
            return False
        
        # Execute the application
        process = subprocess.Popen([sys.executable, app_path], 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
        
        logger.info(f"Application launched with PID: {process.pid}")
        
        # We don't wait for process completion as the app is a GUI
        return True
        
    except Exception as e:
        logger.error(f"Error launching application: {str(e)}")
        traceback.print_exc()
        return False

def main():
    """Main entry point for launcher"""
    logger.info("=" * 50)
    logger.info("Pawprinting PyQt6 V2 Launcher Started")
    logger.info("=" * 50)
    
    try:
        # Check environment
        if not check_environment():
            logger.error("Environment check failed. Application may not run correctly.")
            user_input = input("Environment check failed. Do you want to continue anyway? (y/n): ")
            if user_input.lower() != 'y':
                logger.info("Launch aborted by user")
                return
        
        # Launch application
        success = launch_application()
        
        if success:
            logger.info("Launcher completed successfully")
        else:
            logger.error("Launcher failed to start application")
            input("Press Enter to exit...")
    
    except Exception as e:
        logger.error(f"Unexpected error in launcher: {str(e)}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
