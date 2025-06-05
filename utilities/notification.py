#!/usr/bin/env python3
"""
Notification Manager for Pawprinting PyQt6 Application

Provides toast-style notification functionality throughout the application.

Author: AIMF LLC
Date: June 3, 2025
"""

import logging
from enum import Enum
from typing import Optional, List, Callable

from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPen, QBrush
from PyQt6.QtWidgets import (
    QWidget, QLabel, QHBoxLayout, QApplication, 
    QGraphicsDropShadowEffect, QVBoxLayout
)

# Set up logging
logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Types of notifications with associated colors"""
    INFO = QColor(53, 153, 219)      # Blue
    SUCCESS = QColor(46, 204, 113)    # Green
    WARNING = QColor(241, 196, 15)    # Yellow
    ERROR = QColor(231, 76, 60)       # Red


class NotificationWidget(QWidget):
    """A floating toast-style notification widget"""
    
    DEFAULT_TIMEOUT = 3000  # 3 seconds
    
    def __init__(
            self, 
            message: str, 
            notification_type: NotificationType = NotificationType.INFO,
            parent: Optional[QWidget] = None,
            timeout: int = DEFAULT_TIMEOUT
        ):
        super().__init__(parent)
        
        # Set background to transparent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        
        # Store properties
        self._opacity = 1.0
        self._message = message
        self._type = notification_type
        self._timeout = timeout
        
        self._setup_ui()
        
        # Auto-close timer
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.start_fade_out)
        
        # Animation for fading out
        self._animation = QPropertyAnimation(self, b"opacity")
        self._animation.setDuration(500)  # 500ms fade
        self._animation.setStartValue(1.0)
        self._animation.setEndValue(0.0)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.finished.connect(self.close)
        
        # Start the timer
        self._timer.start(self._timeout)
    
    def _setup_ui(self):
        """Set up the UI components"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create message label
        self._label = QLabel(self._message)
        self._label.setStyleSheet(
            f"""
            color: white;
            font-weight: bold;
            padding: 8px;
            """
        )
        layout.addWidget(self._label)
        
        # Set fixed size based on content
        self.setFixedSize(self.sizeHint())
        
        # Add drop shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
    
    def paintEvent(self, event):
        """Custom paint event for rounded rectangle with color"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity)
        
        # Set up the rounded rectangle
        rect = self.rect()
        color = self._type.value
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(color))
        
        # Draw rounded rectangle
        painter.drawRoundedRect(rect, 10, 10)
        
        super().paintEvent(event)
    
    def position_at_bottom_right(self, parent: QWidget):
        """Position the notification at the bottom right of the parent"""
        parent_rect = parent.rect()
        parent_bottom_right = parent.mapToGlobal(
            QPoint(parent_rect.right() - self.width() - 20, 
                  parent_rect.bottom() - self.height() - 20)
        )
        self.move(parent_bottom_right)
    
    @pyqtProperty(float)
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, value):
        self._opacity = value
        self.update()
    
    def start_fade_out(self):
        """Start the fade out animation"""
        self._animation.start()


class NotificationManager:
    """
    Manages creating and displaying notifications across the application.
    
    This is a static utility class.
    """
    
    _active_notifications: List[NotificationWidget] = []
    _parent: Optional[QWidget] = None
    
    @classmethod
    def set_parent(cls, parent: QWidget):
        """Set the parent widget for notifications"""
        cls._parent = parent
    
    @classmethod
    def _get_parent(cls) -> QWidget:
        """Get the parent widget, or try to find the main window"""
        if cls._parent:
            return cls._parent
            
        # Try to get the active window
        parent = QApplication.activeWindow()
        if parent:
            return parent
            
        # Last resort: create a dummy widget
        logger.warning("No parent widget set for notifications")
        return QWidget()
    
    @classmethod
    def show_notification(cls, message: str, notification_type: NotificationType, timeout: int = NotificationWidget.DEFAULT_TIMEOUT):
        """Show a notification with the specified type"""
        parent = cls._get_parent()
        
        # Create notification
        notification = NotificationWidget(
            message,
            notification_type,
            parent,
            timeout
        )
        
        # Position at bottom right
        notification.position_at_bottom_right(parent)
        
        # Add to active notifications
        cls._active_notifications.append(notification)
        
        # Remove from active when closed
        notification.destroyed.connect(lambda: cls._on_notification_closed(notification))
        
        # Show the notification
        notification.show()
        
        return notification
    
    @classmethod
    def _on_notification_closed(cls, notification: NotificationWidget):
        """Remove notification from active list when closed"""
        if notification in cls._active_notifications:
            cls._active_notifications.remove(notification)
    
    @classmethod
    def close_all(cls):
        """Close all active notifications"""
        for notification in cls._active_notifications.copy():
            notification.close()
        cls._active_notifications.clear()
    
    @classmethod
    def show_info(cls, message: str, timeout: int = NotificationWidget.DEFAULT_TIMEOUT):
        """Show an info notification"""
        return cls.show_notification(message, NotificationType.INFO, timeout)
    
    @classmethod
    def show_success(cls, message: str, timeout: int = NotificationWidget.DEFAULT_TIMEOUT):
        """Show a success notification"""
        return cls.show_notification(message, NotificationType.SUCCESS, timeout)
    
    @classmethod
    def show_warning(cls, message: str, timeout: int = NotificationWidget.DEFAULT_TIMEOUT):
        """Show a warning notification"""
        return cls.show_notification(message, NotificationType.WARNING, timeout)
    
    @classmethod
    def show_error(cls, message: str, timeout: int = NotificationWidget.DEFAULT_TIMEOUT):
        """Show an error notification"""
        return cls.show_notification(message, NotificationType.ERROR, timeout)
