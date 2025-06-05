#!/usr/bin/env python3
"""
Pawprinting PyQt6 Launcher

Launcher script for the Pawprinting PyQt6 application with proper environment setup.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("pawprint_launcher")


def setup_environment():
    """Set up the virtual environment and ensure dependencies are installed"""
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check if virtual environment exists
    venv_dir = os.path.join(script_dir, "venv_pawprinting_pyqt6")
    if not os.path.exists(venv_dir):
        logger.info("Creating virtual environment...")
        try:
            subprocess.run(
                [sys.executable, "-m", "venv", venv_dir],
                check=True
            )
            logger.info("Virtual environment created")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating virtual environment: {e}")
            return False
    
    # Determine activation script
    if sys.platform == "win32":
        activate_script = os.path.join(venv_dir, "Scripts", "activate")
    else:
        activate_script = os.path.join(venv_dir, "bin", "activate")
    
    # Check if requirements file exists
    req_file = os.path.join(script_dir, "requirements.txt")
    if not os.path.exists(req_file):
        logger.error(f"Requirements file not found: {req_file}")
        return False
    
    # Install dependencies if needed
    try:
        # Use pip from the virtual environment
        if sys.platform == "win32":
            pip_path = os.path.join(venv_dir, "Scripts", "pip3")
        else:
            pip_path = os.path.join(venv_dir, "bin", "pip3")
        
        # Check if pip exists
        if not os.path.exists(pip_path):
            logger.error(f"Pip not found in virtual environment: {pip_path}")
            return False
        
        logger.info("Installing dependencies...")
        subprocess.run(
            [pip_path, "install", "-r", req_file],
            check=True
        )
        logger.info("Dependencies installed")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing dependencies: {e}")
        return False
    
    return True


def run_application():
    """Run the Pawprinting PyQt6 application"""
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Main application file
    main_file = os.path.join(script_dir, "pawprint_pyqt6_main.py")
    if not os.path.exists(main_file):
        logger.error(f"Main application file not found: {main_file}")
        return False
    
    # Determine Python interpreter in virtual environment
    if sys.platform == "win32":
        python_path = os.path.join(script_dir, "venv_pawprinting_pyqt6", "Scripts", "python.exe")
    else:
        python_path = os.path.join(script_dir, "venv_pawprinting_pyqt6", "bin", "python3")
    
    # Check if Python interpreter exists
    if not os.path.exists(python_path):
        logger.error(f"Python interpreter not found in virtual environment: {python_path}")
        return False
    
    # Run application
    try:
        logger.info("Starting Pawprinting PyQt6 application...")
        subprocess.run(
            [python_path, main_file],
            check=True
        )
        logger.info("Application closed")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running application: {e}")
        return False


def main():
    """Main entry point"""
    print("=" * 80)
    print(f"Pawprinting PyQt6 Launcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Set up environment
    if not setup_environment():
        print("Failed to set up environment. Please check the logs.")
        sys.exit(1)
    
    # Run application
    if not run_application():
        print("Failed to run application. Please check the logs.")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
