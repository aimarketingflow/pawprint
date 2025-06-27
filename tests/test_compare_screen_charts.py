#!/usr/bin/env python3
"""
Test Compare Screen Charts Components

Test script to verify the chart components in the Compare Screen are working properly.

Author: AIMF LLC
Date: June 6, 2025
"""

import sys
import os
import logging
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path to allow importing modules
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PyQt6.QtWidgets import QApplication
from screens.compare_screen import CompareScreen

class TestCompareScreenCharts(unittest.TestCase):
    """Test case for Compare Screen chart components"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        # Create application instance
        cls.app = QApplication([])
        
        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        
    def setUp(self):
        """Set up test case"""
        self.compare_screen = CompareScreen()
        
    def tearDown(self):
        """Clean up after test"""
        self.compare_screen.deleteLater()
        
    def test_initialization(self):
        """Test that charts tab is initialized properly"""
        # Check that charts tab exists
        self.assertTrue(hasattr(self.compare_screen, 'charts_tab'))
        
        # Check that matplotlib is checked
        self.assertTrue(hasattr(self.compare_screen, 'MATPLOTLIB_AVAILABLE'))
        
    @patch('matplotlib.pyplot')
    def test_chart_methods(self, mock_plt):
        """Test chart methods with mocked matplotlib"""
        # Mock chart data
        self.compare_screen.diff_cache = {
            'current_diff': {
                'added': ['pattern1', 'pattern2'],
                'removed': ['pattern3'],
                'changed': {
                    'pattern4': {'before': 0.5, 'after': 0.8},
                    'pattern5': {'before': 0.7, 'after': 0.3}
                }
            }
        }
        
        # Set mock file groups
        self.compare_screen.file_groups = {
            'Original': [{'filename': 'test1.json', 'path': '/path/to/test1.json'}],
            'Modified': [{'filename': 'test2.json', 'path': '/path/to/test2.json'}]
        }
        
        # Test extract chart data
        self.compare_screen.extract_chart_data()
        self.assertTrue(hasattr(self.compare_screen, 'chart_data'))
        
        # Test radar chart
        self.compare_screen.display_chart("radar")
        
        # Test bar chart
        self.compare_screen.display_chart("bar")
        
        # Test line chart
        self.compare_screen.display_chart("line")
        
        # Test pie chart
        self.compare_screen.display_chart("pie")
        
        # Test heatmap chart
        self.compare_screen.display_chart("heatmap")
    
    def test_export_paths(self):
        """Test export path generation"""
        # Test summary export path
        with patch('builtins.open'), patch('os.makedirs'):
            path = self.compare_screen.export_comparison_summary()
            self.assertIsNotNone(path)
            self.assertTrue('Pawprinting_Exports' in path)
            self.assertTrue('Reports' in path)

if __name__ == '__main__':
    unittest.main()
