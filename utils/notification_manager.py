#!/usr/bin/env python3
"""
Notification Manager for Pawprinting PyQt6 Application

Provides centralized notification system to display messages to the user
through status bar, dialogs, and optionally native macOS notifications.

Author: AIMF LLC
Date: June 2, 2025
"""

import os
import sys
import logging
from typing import Optional, Any

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

# Configure logging
logger = logging.getLogger("pawprint_pyqt6.notification_manager")


class NotificationManager:
    """
    Centralized notification system to display messages to the user
    """
    
    @staticmethod
    def show_info(message: str, duration: int = 3000) -> None:
        """
        Show information message in status bar
        
        Args:
            message: Information message to display
            duration: Display duration in milliseconds
        """
        logger.info(message)
        if QApplication.instance() and hasattr(QApplication.instance(), 'main_window'):
            main_window = QApplication.instance().main_window
            main_window.statusBar().showMessage(message, duration)
    
    @staticmethod
    def show_success(message: str, duration: int = 3000) -> None:
        """
        Show success message with green styling in status bar
        
        Args:
            message: Success message to display
            duration: Display duration in milliseconds
        """
        logger.info(f"SUCCESS: {message}")
        if QApplication.instance() and hasattr(QApplication.instance(), 'main_window'):
            main_window = QApplication.instance().main_window
            status_bar = main_window.statusBar()
            
            # Save original style
            original_style = status_bar.styleSheet()
            
            # Set green success style
            status_bar.setStyleSheet("QStatusBar { color: #4CAF50; font-weight: bold; }")
            status_bar.showMessage(message, duration)
            
            # Reset style after duration
            QTimer.singleShot(duration, lambda: status_bar.setStyleSheet(original_style))
    
    @staticmethod
    def show_error(message: str, duration: int = 5000) -> None:
        """
        Show error message with red styling in status bar
        
        Args:
            message: Error message to display
            duration: Display duration in milliseconds
        """
        logger.error(message)
        if QApplication.instance() and hasattr(QApplication.instance(), 'main_window'):
            main_window = QApplication.instance().main_window
            status_bar = main_window.statusBar()
            
            # Set red error style
            status_bar.setStyleSheet("QStatusBar { color: #F44336; font-weight: bold; }")
            status_bar.showMessage(message, duration)
            
            # Reset style after duration
            QTimer.singleShot(duration, lambda: status_bar.setStyleSheet(""))
    
    @staticmethod
    def show_warning(message: str, duration: int = 4000) -> None:
        """
        Show warning message with orange styling in status bar
        
        Args:
            message: Warning message to display
            duration: Display duration in milliseconds
        """
        logger.warning(message)
        if QApplication.instance() and hasattr(QApplication.instance(), 'main_window'):
            main_window = QApplication.instance().main_window
            status_bar = main_window.statusBar()
            
            # Set orange warning style
            status_bar.setStyleSheet("QStatusBar { color: #FF9800; font-weight: bold; }")
            status_bar.showMessage(message, duration)
            
            # Reset style after duration
            QTimer.singleShot(duration, lambda: status_bar.setStyleSheet(""))
    
    @staticmethod
    def show_dialog(title: str, message: str, dialog_type: str = "info") -> Any:
        """
        Show a native dialog box
        
        Args:
            title: Dialog title
            message: Dialog message
            dialog_type: Dialog type ("info", "warning", "error", "question")
        
        Returns:
            Boolean True if user clicked Yes for question dialogs, otherwise None
        """
        if QApplication.instance() and hasattr(QApplication.instance(), 'main_window'):
            main_window = QApplication.instance().main_window
            
            if dialog_type == "error":
                logger.error(f"ERROR DIALOG: {message}")
                QMessageBox.critical(main_window, title, message)
            elif dialog_type == "warning":
                logger.warning(f"WARNING DIALOG: {message}")
                QMessageBox.warning(main_window, title, message)
            elif dialog_type == "question":
                logger.info(f"QUESTION DIALOG: {message}")
                return QMessageBox.question(
                    main_window, title, message,
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.Yes
            else:  # info
                logger.info(f"INFO DIALOG: {message}")
                QMessageBox.information(main_window, title, message)
        else:
            # Fallback to console if no main window available
            print(f"{dialog_type.upper()}: {title} - {message}")
