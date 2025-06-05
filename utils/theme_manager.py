#!/usr/bin/env python3
"""
Theme Manager for Pawprinting PyQt6 Application

Manages application theming including dark mode support and theme switching.
Integrates with macOS native theme preferences and provides consistent styling.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import logging
import json
from typing import Dict, Any, Optional, Tuple

from PyQt6.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QSettings, QTimer, QEvent
from PyQt6.QtGui import QColor, QPalette, QIcon, QPixmap, QFont
from PyQt6.QtWidgets import QApplication, QStyleFactory

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.theme_manager")


class ThemeManager(QObject):
    """
    Manages application theming including dark mode support
    """
    # Signal emitted when theme changes
    theme_changed = pyqtSignal(str)  # Theme name
    
    # Signal emitted when colors change
    colors_changed = pyqtSignal(dict)  # Dictionary of colors
    
    # Singleton instance
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'ThemeManager':
        """Get or create the singleton instance"""
        if cls._instance is None:
            cls._instance = ThemeManager()
        return cls._instance
    
    def __init__(self):
        """Initialize theme manager"""
        super().__init__()
        
        if ThemeManager._instance is not None:
            raise RuntimeError("ThemeManager is a singleton. Use get_instance() instead")
        
        # Initialize settings
        self._settings = QSettings("AIMF LLC", "Pawprinting PyQt6")
        
        # Current theme name
        self._theme_name = self._settings.value("theme", "auto")  # "auto", "light", "dark"
        
        # Colors for light and dark themes
        self._colors = {
            "light": {
                "primary": "#2196F3",        # Blue
                "secondary": "#03A9F4",      # Light Blue
                "accent": "#FF5722",         # Deep Orange
                "success": "#4CAF50",        # Green
                "warning": "#FF9800",        # Orange
                "error": "#F44336",          # Red
                "info": "#2196F3",           # Blue
                "background": "#FFFFFF",     # White
                "card": "#FAFAFA",           # Very Light Grey
                "text": "#212121",           # Very Dark Grey
                "textSecondary": "#757575",  # Grey
                "border": "#EEEEEE",         # Light Grey
                "disabled": "#BDBDBD"        # Medium Grey
            },
            "dark": {
                "primary": "#2196F3",        # Blue
                "secondary": "#0288D1",      # Darker Blue
                "accent": "#FF5722",         # Deep Orange
                "success": "#4CAF50",        # Green
                "warning": "#FF9800",        # Orange
                "error": "#F44336",          # Red
                "info": "#2196F3",           # Blue
                "background": "#121212",     # Very Dark Grey
                "card": "#1E1E1E",           # Dark Grey
                "text": "#FFFFFF",           # White
                "textSecondary": "#B0B0B0",  # Light Grey
                "border": "#333333",         # Dark Grey
                "disabled": "#757575"        # Medium Grey
            }
        }
        
        # Current active colors (will be set based on theme)
        self._active_colors = {}
        
        # CSS templates for different components
        self._css_templates = {
            "app": """
                QWidget {
                    background-color: {{background}};
                    color: {{text}};
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
                }
                
                QPushButton {
                    background-color: {{primary}};
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                
                QPushButton:hover {
                    background-color: {{secondary}};
                }
                
                QPushButton:pressed {
                    background-color: {{primary}};
                }
                
                QPushButton:disabled {
                    background-color: {{disabled}};
                    color: {{textSecondary}};
                }
                
                QLineEdit, QTextEdit, QComboBox {
                    background-color: {{card}};
                    color: {{text}};
                    border: 1px solid {{border}};
                    border-radius: 4px;
                    padding: 4px 8px;
                }
                
                QLabel {
                    color: {{text}};
                }
                
                QCheckBox, QRadioButton {
                    color: {{text}};
                }
                
                QProgressBar {
                    background-color: {{card}};
                    color: {{text}};
                    border: 1px solid {{border}};
                    border-radius: 4px;
                    text-align: center;
                }
                
                QProgressBar::chunk {
                    background-color: {{primary}};
                    border-radius: 3px;
                }
                
                QGroupBox {
                    border: 1px solid {{border}};
                    border-radius: 4px;
                    margin-top: 8px;
                    padding-top: 16px;
                }
                
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    left: 8px;
                    padding: 0 5px;
                    color: {{text}};
                }
                
                QTabWidget::pane {
                    border: 1px solid {{border}};
                    border-radius: 4px;
                    top: -1px;
                }
                
                QTabBar::tab {
                    background-color: {{card}};
                    color: {{text}};
                    border: 1px solid {{border}};
                    border-bottom-color: {{border}};
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                    min-width: 8ex;
                    padding: 4px 8px;
                }
                
                QTabBar::tab:selected {
                    background-color: {{background}};
                    border-bottom-color: {{background}};
                }
                
                QTabBar::tab:!selected {
                    margin-top: 2px;
                }
                
                QListWidget, QTreeWidget, QTableWidget {
                    background-color: {{card}};
                    color: {{text}};
                    border: 1px solid {{border}};
                    border-radius: 4px;
                }
                
                QListWidget::item:selected, QTreeWidget::item:selected, QTableWidget::item:selected {
                    background-color: {{primary}};
                    color: white;
                }
                
                QScrollBar:vertical {
                    border: none;
                    background-color: {{card}};
                    width: 10px;
                    margin: 0px;
                }
                
                QScrollBar::handle:vertical {
                    background-color: {{border}};
                    min-height: 20px;
                    border-radius: 5px;
                }
                
                QScrollBar::handle:vertical:hover {
                    background-color: {{primary}};
                }
                
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                
                QScrollBar:horizontal {
                    border: none;
                    background-color: {{card}};
                    height: 10px;
                    margin: 0px;
                }
                
                QScrollBar::handle:horizontal {
                    background-color: {{border}};
                    min-width: 20px;
                    border-radius: 5px;
                }
                
                QScrollBar::handle:horizontal:hover {
                    background-color: {{primary}};
                }
                
                QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                    width: 0px;
                }
                
                QStatusBar {
                    background-color: {{card}};
                    color: {{text}};
                    border-top: 1px solid {{border}};
                }
                
                QMenuBar {
                    background-color: {{card}};
                    color: {{text}};
                }
                
                QMenuBar::item {
                    background-color: transparent;
                    padding: 4px 8px;
                }
                
                QMenuBar::item:selected {
                    background-color: {{primary}};
                    color: white;
                    border-radius: 4px;
                }
                
                QMenu {
                    background-color: {{card}};
                    color: {{text}};
                    border: 1px solid {{border}};
                    border-radius: 4px;
                    padding: 4px;
                }
                
                QMenu::item {
                    padding: 4px 20px 4px 20px;
                    border-radius: 4px;
                }
                
                QMenu::item:selected {
                    background-color: {{primary}};
                    color: white;
                }
                
                QMenu::separator {
                    height: 1px;
                    background-color: {{border}};
                    margin: 4px 0px;
                }
            """
        }
        
        # Check if we're on macOS
        self._is_macos = sys.platform == "darwin"
        
        # Apply initial theme
        self.update_active_theme()
        
        # Set up timer to check for system theme changes
        if self._theme_name == "auto" and self._is_macos:
            self._theme_check_timer = QTimer(self)
            self._theme_check_timer.timeout.connect(self._check_system_theme)
            self._theme_check_timer.start(5000)  # Check every 5 seconds
        
        logger.info(f"Theme manager initialized with theme: {self._theme_name}")
    
    def get_theme(self) -> str:
        """Get current theme name"""
        return self._theme_name
    
    def get_theme_preference(self) -> str:
        """Get user preference for theme (auto, light, dark)"""
        return self._theme_name
    
    def set_theme(self, theme_name: str) -> None:
        """Set theme by name"""
        if theme_name not in ["auto", "light", "dark"]:
            logger.warning(f"Invalid theme name: {theme_name}")
            return
        
        # Update theme name
        self._theme_name = theme_name
        
        # Save to settings
        self._settings.setValue("theme", theme_name)
        
        # Update active theme
        self.update_active_theme()
        
        # Start or stop system theme check timer
        if theme_name == "auto" and self._is_macos:
            if not hasattr(self, "_theme_check_timer") or not self._theme_check_timer.isActive():
                self._theme_check_timer = QTimer(self)
                self._theme_check_timer.timeout.connect(self._check_system_theme)
                self._theme_check_timer.start(5000)  # Check every 5 seconds
        else:
            if hasattr(self, "_theme_check_timer") and self._theme_check_timer.isActive():
                self._theme_check_timer.stop()
        
        logger.info(f"Theme set to: {theme_name}")
    
    def toggle_theme(self) -> None:
        """Toggle between light and dark theme"""
        if self._get_current_theme_name() == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")
    
    def update_active_theme(self) -> None:
        """Update active theme based on current theme name"""
        theme_name = self._get_current_theme_name()
        
        # Set active colors
        self._active_colors = self._colors[theme_name].copy()
        
        # Emit signals
        self.theme_changed.emit(theme_name)
        self.colors_changed.emit(self._active_colors)
        
        logger.info(f"Active theme updated to: {theme_name}")
    
    def _get_current_theme_name(self) -> str:
        """Get the actual theme name based on auto setting"""
        if self._theme_name == "auto":
            return self._get_system_theme()
        return self._theme_name
    
    def _get_system_theme(self) -> str:
        """Get system theme (light or dark)"""
        if not self._is_macos:
            return "light"  # Default to light on non-macOS
        
        # On macOS, check for dark mode
        if self._check_macos_dark_mode():
            return "dark"
        return "light"
    
    def _check_macos_dark_mode(self) -> bool:
        """Check if macOS is in dark mode"""
        try:
            import subprocess
            result = subprocess.run(
                ["defaults", "read", "-g", "AppleInterfaceStyle"],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == "Dark"
        except Exception as e:
            logger.error(f"Error checking macOS dark mode: {e}")
            return False
    
    def _check_system_theme(self) -> None:
        """Check for system theme changes"""
        if self._theme_name != "auto":
            return
        
        # Get current system theme
        current_system_theme = self._get_system_theme()
        
        # Check if theme has changed
        previous_theme = self._get_current_theme_name()
        if current_system_theme != previous_theme:
            logger.info(f"System theme changed from {previous_theme} to {current_system_theme}")
            self.update_active_theme()
    
    def get_color(self, name: str) -> QColor:
        """Get color by name"""
        if name in self._active_colors:
            return QColor(self._active_colors[name])
        return QColor("#000000")
    
    def get_color_hex(self, name: str) -> str:
        """Get color hex value by name"""
        if name in self._active_colors:
            return self._active_colors[name]
        return "#000000"
    
    def get_palette(self) -> QPalette:
        """Get QPalette for current theme"""
        palette = QPalette()
        
        # Get colors
        bg_color = QColor(self._active_colors["background"])
        text_color = QColor(self._active_colors["text"])
        highlight_color = QColor(self._active_colors["primary"])
        highlight_text_color = QColor("#FFFFFF")
        button_color = QColor(self._active_colors["card"])
        button_text_color = QColor(self._active_colors["text"])
        link_color = QColor(self._active_colors["primary"])
        
        # Set palette colors
        palette.setColor(QPalette.ColorRole.Window, bg_color)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, QColor(self._active_colors["card"]))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(self._active_colors["border"]))
        palette.setColor(QPalette.ColorRole.Text, text_color)
        palette.setColor(QPalette.ColorRole.Button, button_color)
        palette.setColor(QPalette.ColorRole.ButtonText, button_text_color)
        palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.white)
        palette.setColor(QPalette.ColorRole.Highlight, highlight_color)
        palette.setColor(QPalette.ColorRole.HighlightedText, highlight_text_color)
        palette.setColor(QPalette.ColorRole.Link, link_color)
        palette.setColor(QPalette.ColorRole.LinkVisited, link_color.darker(120))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(self._active_colors["card"]))
        palette.setColor(QPalette.ColorRole.ToolTipText, text_color)
        
        # Set disabled colors
        disabled_color = QColor(self._active_colors["disabled"])
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, disabled_color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, disabled_color)
        palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, disabled_color)
        
        return palette
    
    def get_application_stylesheet(self) -> str:
        """Get stylesheet for the application"""
        # Get template
        template = self._css_templates["app"]
        
        # Replace placeholders with actual colors
        for color_name, color_value in self._active_colors.items():
            template = template.replace("{{" + color_name + "}}", color_value)
        
        return template
