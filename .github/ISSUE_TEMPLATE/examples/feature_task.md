---
name: "[Help Wanted] Implement Dark/Light Theme Toggle"
about: Add a quick toggle button for switching between dark and light themes
title: "[Feature] Implement Dark/Light Theme Toggle Button"
labels: enhancement, help wanted, ui
assignees: ''
---

## Overview

While the application currently supports system theme detection, users may want to quickly switch between dark and light themes without changing their system settings. This task involves implementing a toggle button in the application's header to switch themes on demand.

## Required Changes

- Add a theme toggle button in the application header/toolbar
- Implement theme switching logic that overrides the system theme detection
- Save the user preference in the application settings
- Ensure all UI components update correctly when themes change dynamically

## Technical Details

- Theme management is handled in `/utils/theme_manager.py`
- Settings management is in `/utils/state_manager.py`
- The main application window is in `pawprint_pyqt6_main.py`

## Skills Needed

- Python with PyQt6 experience
- Understanding of CSS-like styling in Qt
- Working knowledge of state management

## Difficulty

Medium - Requires understanding the existing theme system but doesn't require extensive changes.

## Resources

- [PyQt6 Style Sheets Documentation](https://doc.qt.io/qt-6/stylesheet.html)
- Review our [contribution guidelines](../../CONTRIBUTING.md) before submitting your PR
