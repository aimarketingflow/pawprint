#!/usr/bin/env python3
"""
Pawprinting PyQt6 Main Application

Main entry point for the PyQt6-based Pawprinting Analysis tool.
This replaces the Kivy-based implementation with native macOS components.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import json
import logging
import traceback
from datetime import datetime
from pathlib import Path

# Import PyQt6 modules
from PyQt6.QtCore import Qt, QSize, pyqtSignal, pyqtSlot, QTimer, QUrl, QSettings, QEvent, QObject
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, 
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLineEdit, QTextEdit, QFileDialog, QDialog, QMessageBox,
    QTabWidget, QComboBox, QCheckBox, QRadioButton, QProgressBar,
    QScrollArea, QFrame, QSplitter, QMenuBar, QStatusBar, QToolBar,
    QStackedWidget
)

# Force use of the correct paths
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Import centralized configuration paths
from config_paths import *

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(os.path.join(
            LOGS_DIR, 
            f'pawprint_pyqt6_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        )),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("pawprint_pyqt6_main")

# Import screens and utils as they are created
# These will be uncommented as we implement each component
from screens.dashboard_screen import DashboardScreen
from screens.generate_screen import GenerateScreen
from screens.analyze_screen import AnalyzeScreen
# from screens.settings_screen import SettingsScreen
from screens.fractal_butterfly_screen import FractalButterflyScreen
from screens.history_screen import HistoryScreen
from screens.screens_manager import ScreensManager
# from screens.fractal_settings_screen import FractalSettingsScreen

# Import database module
from database import get_database, import_existing_configs

# Import utils
from utils.notification_manager import NotificationManager
from utils.progress_tracker import ProgressTracker
from utils.state_manager import StateManager
from utils.theme_manager import ThemeManager

# Import our custom notification manager
from utilities.notification import NotificationManager as NewNotificationManager

class PawprintMainWindow(QMainWindow):
    """
    Main application window for the Pawprinting PyQt6 application
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pawprinting Analysis Tool")
        self.resize(1200, 760)  # Reduced height by 40 pixels
        
        # Store reference for global access
        QApplication.instance().main_window = self
        
        # Set up status bar for notifications
        self.statusBar().showMessage("Ready")
        
        # Initialize theme manager before creating UI
        self.theme_manager = ThemeManager.get_instance()
        
        # Initialize state manager
        self.state_manager = StateManager.get_instance()
        
        # Set up central stacked widget for screen management
        self.central_widget = QStackedWidget(self)
        self.setCentralWidget(self.central_widget)
        
        # Apply initial theme
        self.apply_theme()
        
        # Set application icon
        self.set_app_icon()
        
        # Load screens
        self.load_screens()
        
        # Set up menu bar with native macOS integration
        self.setup_menu()
        
        # Show initial screen
        self.show_dashboard_screen()
        
        logger.info("Application initialized")
    
    def load_screens(self):
        """Load all application screens"""
        # Create dashboard screen
        self.dashboard_screen = DashboardScreen(self)
        self.central_widget.addWidget(self.dashboard_screen)
        
        # Add other screens as they are implemented
        self.generate_screen = GenerateScreen(self)
        self.central_widget.addWidget(self.generate_screen)
        
        self.analyze_screen = AnalyzeScreen(self)
        self.central_widget.addWidget(self.analyze_screen)
        
        # self.settings_screen = SettingsScreen(self)
        # self.central_widget.addWidget(self.settings_screen)
        
        # Initialize database
        try:
            self.db = get_database()
            logger.info("Database initialized successfully")
            
            # Import any existing configs into database
            total, imported = import_existing_configs()
            if imported > 0:
                logger.info(f"Imported {imported} configurations into database")
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
        
        self.fractal_butterfly_screen = FractalButterflyScreen(self)
        self.central_widget.addWidget(self.fractal_butterfly_screen)
        
        # Add history screen
        self.history_screen = HistoryScreen()
        self.central_widget.addWidget(self.history_screen)
        
        # Connect history screen signals
        self.history_screen.loadPawprint.connect(self.on_load_pawprint)
        
        # self.fractal_settings_screen = FractalSettingsScreen(self)
        # self.central_widget.addWidget(self.fractal_settings_screen)
        
        logger.info("Screens loaded")
    
    def apply_theme(self):
        """Apply current theme to the application"""
        if self.theme_manager:
            # Get theme stylesheet
            stylesheet = self.theme_manager.get_application_stylesheet()
            self.setStyleSheet(stylesheet)
            
            # Apply palette
            palette = self.theme_manager.get_palette()
            QApplication.instance().setPalette(palette)
            
            logger.info(f"Applied theme: {self.theme_manager.get_theme_preference()}")

    
    def set_app_icon(self):
        """Set the application icon from the logo file"""
        try:
            # Check if logo file exists
            if os.path.exists(LOGO_PATH):
                app_icon = QIcon(LOGO_PATH)
                self.setWindowIcon(app_icon)
                # Also set the application-wide icon
                QApplication.setWindowIcon(app_icon)
                logger.info(f"Set application icon from {LOGO_PATH}")
            else:
                logger.warning(f"Logo file not found at {LOGO_PATH}")
        except Exception as e:
            logger.error(f"Failed to set application icon: {e}")
    
    def setup_menu(self):
        """Set up native macOS menu bar"""
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        new_action = QAction("&New Pawprint", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.show_generate_screen)
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open)
        file_menu.addAction(open_action)
        
        # Add history menu item
        history_action = QAction("&History", self)
        history_action.setShortcut("Ctrl+H")
        history_action.triggered.connect(self.show_history_screen)
        file_menu.addAction(history_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = self.menuBar().addMenu("&Tools")
        
        analyze_action = QAction("&Analyze Files", self)
        analyze_action.triggered.connect(self.show_analyze_screen)
        tools_menu.addAction(analyze_action)
        
        fractal_action = QAction("&Fractal Butterfly", self)
        fractal_action.triggered.connect(self.show_fractal_screen)
        tools_menu.addAction(fractal_action)
        
        # View/Theme menu
        view_menu = self.menuBar().addMenu("&View")
        
        # Add theme selection submenu
        theme_menu = view_menu.addMenu("&Theme")
        
        # Theme actions
        light_theme_action = QAction("&Light", self)
        light_theme_action.setCheckable(True)
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        theme_menu.addAction(light_theme_action)
        
        dark_theme_action = QAction("&Dark", self)
        dark_theme_action.setCheckable(True)
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(dark_theme_action)
        
        auto_theme_action = QAction("&Auto (System)", self)
        auto_theme_action.setCheckable(True)
        auto_theme_action.triggered.connect(lambda: self.set_theme("auto"))
        theme_menu.addAction(auto_theme_action)
        
        # Update checkmarks based on current theme
        current_theme = "auto"
        if self.theme_manager:
            current_theme = self.theme_manager.get_theme_preference()
        
        light_theme_action.setChecked(current_theme == "light")
        dark_theme_action.setChecked(current_theme == "dark")
        auto_theme_action.setChecked(current_theme == "auto")
        
        # Settings menu option
        settings_action = QAction("&Settings", self)
        settings_action.triggered.connect(self.show_settings_screen)
        tools_menu.addAction(settings_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def show_dashboard_screen(self):
        """Switch to dashboard screen"""
        self.central_widget.setCurrentWidget(self.dashboard_screen)
        logger.info("Showing dashboard screen")
    
    def show_fractal_screen(self):
        """Switch to the fractal butterfly screen"""
        self.central_widget.setCurrentWidget(self.fractal_butterfly_screen)
        self.statusBar().showMessage("Fractal Butterfly Generator")
        logger.info("Switched to Fractal Butterfly screen")
        
    def show_history_screen(self):
        """Switch to the pawprint history screen"""
        self.central_widget.setCurrentWidget(self.history_screen)
        self.statusBar().showMessage("Pawprint History")
        logger.info("Switched to History screen")
    
    def show_generate_screen(self):
        """Switch to generate screen"""
        self.central_widget.setCurrentWidget(self.generate_screen)
        logger.info("Showing generate screen")
        
        # For now, show a message
        # NotificationManager.show_dialog(
        #     "Not Implemented", 
        #     "Generate screen is not yet implemented.",
        #     "info"
        # )
    
    def show_analyze_screen(self):
        """Switch to analyze screen"""
        self.central_widget.setCurrentWidget(self.analyze_screen)
        logger.info("Showing analyze screen")
        
        # For now, show a message
        # NotificationManager.show_dialog(
        #     "Not Implemented", 
        #     "Analyze screen is not yet implemented.",
        #     "info"
        # )
    
    def show_settings_screen(self):
        """Switch to settings screen"""
        # Ensure settings screen is created
        if not hasattr(self, "settings_screen") or self.settings_screen is None:
            from screens.settings_screen import SettingsScreen
            self.settings_screen = SettingsScreen(self)
            self.central_widget.addWidget(self.settings_screen)
        
        # Switch to settings screen
        self.central_widget.setCurrentWidget(self.settings_screen)
        logger.info("Showing settings screen")
        
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h2>Pawprinting Analysis Tool</h2>
        <p>Version 2.0.0</p>
        <p>A powerful digital pawprinting tool for security analysis.</p>
        <p>© 2025 AIMF LLC. All rights reserved.</p>
        """
        
        QMessageBox.about(self, "About Pawprinting Analysis Tool", about_text)
    def on_load_pawprint(self, params):
        """Handle loading a pawprint from history"""
        # Switch to the fractal butterfly screen
        self.show_fractal_screen()

        # Load the pawprint parameters
        try:
            self.fractal_butterfly_screen.load_parameters(params)
            NewNotificationManager.show_success(f"Loaded pawprint: {params.get('name', 'Unnamed')}")
            logger.info(f"Loaded pawprint from history: {params.get('name', 'Unnamed')}")
        except Exception as e:
            logger.error(f"Error loading pawprint: {e}")
            NewNotificationManager.show_error(f"Error loading pawprint: {str(e)}")
            
    def on_open(self, file_path=None):
        """Handle opening a file
        
        Args:
            file_path: Optional file path. If None, will open a file dialog.
        """
        # If no file path provided, use native file dialog
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Open Configuration",
                os.path.join(CONFIG_DIR),
                "Pawprint Configurations (*.json);;All Files (*.*)"
            )
        
        if not file_path or not os.path.exists(file_path):
            return False
        
        try:
            # Record this file in recent files
            self.state_manager.add_recent_file(file_path)
            
            # Handle the file based on its type
            if file_path.endswith('.json'):
                # Determine which screen should handle this file
                if self._is_fractal_config(file_path):
                    # Load into fractal butterfly screen
                    self.show_fractal_screen()
                    if hasattr(self.fractal_butterfly_screen, 'load_from_file'):
                        self.fractal_butterfly_screen.load_from_file(file_path)
                        logger.info(f"Opened fractal configuration: {file_path}")
                        NewNotificationManager.show_success(f"Opened {os.path.basename(file_path)} in Fractal screen")
                        # Add to current session list
                        self._add_to_current_session(file_path)
                        return True
                    else:
                        logger.warning("Fractal butterfly screen does not support loading from file")
                        NewNotificationManager.show_warning("Loading from file not supported yet")
                else:
                    # Load into analyze screen
                    self.show_analyze_screen()
                    if hasattr(self.analyze_screen, 'load_file'):
                        success = self.analyze_screen.load_file(file_path)
                        if success:
                            logger.info(f"Opened file in analyze screen: {file_path}")
                            NewNotificationManager.show_success(f"Opened {os.path.basename(file_path)} in Analyze screen")
                            # Add to current session list
                            self._add_to_current_session(file_path)
                            return True
                    else:
                        logger.warning("Analyze screen does not support loading files")
                        NewNotificationManager.show_warning("Analyze screen does not support loading files yet")
            else:
                # Unknown file type
                logger.warning(f"Unsupported file type: {file_path}")
                NewNotificationManager.show_warning(f"Unsupported file type: {os.path.basename(file_path)}")
        except Exception as e:
            logger.error(f"Error opening file {file_path}: {e}")
            NewNotificationManager.show_error(f"Error opening file: {str(e)}")
        
        return False
        
    def _add_to_current_session(self, file_path):
        """Add a file to the current session list in dashboard
        
        Args:
            file_path: Path to file to add
        """
        # Find dashboard and add to its current session
        if hasattr(self, 'dashboard_screen') and self.dashboard_screen is not None:
            self.dashboard_screen.add_to_current_session(file_path)
    
    def _is_fractal_config(self, file_path):
        """Check if the given JSON file is a fractal butterfly configuration
        
        Args:
            file_path: Path to JSON file to check
            
        Returns:
            bool: True if this is a fractal config, False otherwise
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Check for key fields that would indicate this is a fractal config
            if 'fractalType' in data or 'points' in data or 'viewportSettings' in data:
                return True
            
            # Otherwise, assume it's a regular pawprint
            return False
                
        except Exception as e:
            logger.error(f"Error checking file type: {e}")
            return False

# ... (rest of the code remains the same)

def exception_hook(exc_type, exc_value, exc_traceback):
    """Global exception handler to log unhandled exceptions"""
    # Log the exception
    logger.error("Unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback))
    
    # Also print to stderr for immediate visibility
    print("Unhandled exception:", file=sys.stderr)
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
    
    # Show an error dialog if the application is running
    if QApplication.instance():
        error_text = str(exc_value)
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Icon.Critical)
        dialog.setWindowTitle("Application Error")
        dialog.setText("An unhandled error has occurred")
        dialog.setInformativeText(error_text)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.exec()


def main():
    """
    Main application entry point
    """
    # Create QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Pawprinting Analysis Tool")
    
    # Import config paths again here for safety
    from config_paths import RESOURCE_DIR, LOGS_DIR, CONFIG_DIR, RESULTS_DIR
    
    # Import scrollable screens module to patch all screen classes
    try:
        from screens.apply_scrollable_screens import patch_all_screen_classes
        logger.info("Applied scrollable functionality to all screens")
    except Exception as e:
        logger.error(f"Failed to apply scrollable screens: {str(e)}")
        logger.debug(traceback.format_exc())
        
    # Import fixed size window utility
    try:
        from utils.fixed_size_app_window import FixedSizeAppWindow
        logger.info("Fixed size window utility imported")
    except Exception as e:
        logger.error(f"Failed to import fixed size window utility: {str(e)}")
        logger.debug(traceback.format_exc())
    
    # Set application icon (if available)
    icon_path = os.path.join(RESOURCE_DIR, "icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    # Set up global exception handler
    sys.excepthook = exception_hook

    # Initialize database before starting the UI
    try:
        from database import get_database
        db = get_database()
        logger.info("Database initialized successfully before UI load")
    except Exception as e:
        logger.warning(f"Initial database check error: {e}")

    # Show splash screen
    # splash = QSplashScreen(QPixmap(os.path.join(RESOURCES_DIR, "splash.png")))
    # splash.show()
    # app.processEvents()

    try:
        # Create the main window
        window = PawprintMainWindow()
        
        # Apply fixed size with internal scrolling
        try:
            # Get screen dimensions and apply fixed size with scrolling
            screen_width, screen_height = FixedSizeAppWindow.get_screen_dimensions()
            logger.info(f"Screen dimensions detected: {screen_width}x{screen_height}")
            
            # Apply a 5% margin as requested
            scroll_area = FixedSizeAppWindow.apply_fixed_size_with_scrolling(
                window, 
                screen_width, 
                screen_height, 
                margin_percent=5
            )
            
            logger.info("Applied fixed window size with internal scrolling")
        except Exception as e:
            logger.error(f"Failed to apply fixed window size: {str(e)}")
            logger.debug(traceback.format_exc())
        
        # Show the main window
        window.show()

        # Close splash if we added one
        # splash.finish(window)

        return app.exec()
    except Exception as e:
        logger.critical(f"Failed to start application: {e}")
        return 1

if __name__ == "__main__":
    main()
