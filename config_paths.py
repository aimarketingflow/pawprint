#!/usr/bin/env python3
"""
Configuration paths for the Pawprinting PyQt6 Application

Centralizes path management for the application to ensure
consistent file access regardless of working directory.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys

# Base directory is the directory this script is in
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Resource paths
RESOURCE_DIR = os.path.join(BASE_DIR, 'resources')
IMAGES_DIR = os.path.join(RESOURCE_DIR, 'images')
LOGO_PATH = os.path.join(IMAGES_DIR, 'PawPrintLogo.jpg')
ICONS_DIR = os.path.join(RESOURCE_DIR, 'icons')
STYLES_DIR = os.path.join(RESOURCE_DIR, 'styles')

# Output paths
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
CHATLOGS_DIR = os.path.join(BASE_DIR, '_Chatlogs')

# Config paths
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
SETTINGS_PATH = os.path.join(CONFIG_DIR, 'settings.json')
FRACTAL_SETTINGS_PATH = os.path.join(CONFIG_DIR, 'fractal_settings.json')

# Test data
TEST_DATA_DIR = os.path.join(BASE_DIR, 'test_data')

# Create necessary directories if they don't exist
for directory in [RESOURCE_DIR, LOGS_DIR, RESULTS_DIR, CHATLOGS_DIR, 
                 CONFIG_DIR, ICONS_DIR, STYLES_DIR, TEST_DATA_DIR]:
    os.makedirs(directory, exist_ok=True)

# Ensure the application directory is in the system path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
