# Pawprinting PyQt6 V2 - Fixed Size Window Implementation Guide

**AIMF LLC**  
**Date:** June 7, 2025  
**Version:** 1.0

## Overview

This guide documents the implementation of a fixed size window with internal scrolling for the Pawprinting PyQt6 V2 application. The fixed size window ensures that the application maintains consistent dimensions across different displays while allowing users to access all content through scrolling.

## Implementation Architecture

The fixed size window implementation follows a modular design that builds upon the existing scrollable screens feature, providing application-wide scrolling in both horizontal and vertical directions.

### Key Components

1. **Fixed Size Window Utility (`/utils/fixed_size_app_window.py`)**
   - Provides utility functions for setting fixed window dimensions
   - Implements application-wide scrolling for the main window
   - Automatically detects screen dimensions and applies appropriate scaling

2. **Main Application Integration (`pawprint_pyqt6_main.py`)**
   - Imports the fixed size window utility
   - Applies fixed size constraints after main window creation
   - Configures scrolling behavior for the entire application window

## Technical Implementation Details

### Window Size Calculation

The application window size is calculated based on the current screen size with a configurable margin:

```python
# Get screen dimensions
screen_width, screen_height = FixedSizeAppWindow.get_screen_dimensions()

# Apply margin percentage (e.g., 5%)
width = int(screen_width * (1 - margin_percent/100))
height = int(screen_height * (1 - margin_percent/100))
```

### Main Window Constraints

Fixed size constraints are applied to the main window to prevent resizing:

```python
# Set fixed size for the main window
main_window.setFixedSize(width, height)
main_window.setMinimumSize(width, height)
main_window.setMaximumSize(width, height)
```

### Scroll Area Implementation

The entire application UI is wrapped in a scroll area that provides both horizontal and vertical scrolling:

```python
# Create a scroll area wrapper
scroll_area = QScrollArea()
scroll_area.setWidgetResizable(True)
scroll_area.setFrameShape(QFrame.Shape.NoFrame)
scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
```

## Usage Characteristics

### Window Behavior

- The application window has a fixed size equal to the screen dimensions less a 5% margin
- The window cannot be resized by the user
- All content inside the window can be scrolled both horizontally and vertically

### Scrolling Behavior

- Horizontal scroll bars appear automatically when content exceeds the window width
- Vertical scroll bars appear automatically when content exceeds the window height
- Scroll bars are styled according to the application's dark theme

### Keyboard and Mouse Navigation

- Standard keyboard navigation (arrow keys, Page Up/Down, Home/End)
- Mouse wheel scrolling for vertical navigation
- Shift+Wheel or trackpad gestures for horizontal scrolling

## Integration with Individual Screens

The fixed size window implementation works in conjunction with the existing scrollable screens feature:

1. The main window provides application-wide scrolling for the entire UI
2. Individual screens have their own scrollable containers for screen-specific content
3. Both scrolling mechanisms operate independently, providing nested scrolling areas

## Example Dimensions

Based on common screen resolutions, the fixed window sizes (with 5% margin) would be:

| Screen Resolution | Window Size (5% margin) |
|-------------------|-------------------------|
| 1920 × 1080       | 1824 × 1026             |
| 1440 × 900        | 1368 × 855              |
| 1366 × 768        | 1297 × 729              |
| 2560 × 1440       | 2432 × 1368             |

## Error Handling

The implementation includes comprehensive error handling:

- Graceful fallback to standard window behavior if fixed size cannot be applied
- Detection of available screen dimensions with fallback to default values if needed
- Detailed logging of any issues encountered during the fixed size application

## Extending the Implementation

To modify the fixed size window behavior:

1. Adjust the margin percentage in `pawprint_pyqt6_main.py` (currently set to 5%)
2. Modify the scroll bar policies in `fixed_size_app_window.py` to change when scroll bars appear
3. Add custom styling for the scroll bars in the application's theme manager

## Troubleshooting

If issues occur with the fixed size window:

1. Check application logs for any errors related to the fixed size implementation
2. Verify that the screen dimensions are being correctly detected
3. Ensure that the main window's central widget is properly set up for scrolling

## Developer Notes

- The fixed window size is calculated once at application startup based on current screen dimensions
- Scroll bars only appear when content exceeds the visible area
- All UI components maintain their original functionality within the scrollable container

---

**© 2025 AIMF LLC - All Rights Reserved**
