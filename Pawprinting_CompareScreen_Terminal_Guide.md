# Pawprinting PyQt6 V2 - Compare Screen Terminal Guide

## Overview
This guide provides instructions for running and testing the Compare Screen component of the Pawprinting PyQt6 V2 application.

## Running the Example Application

To run the Compare Screen example application:

```bash
cd /Users/flowgirl/Documents/FolderHackingAnalysis/Pawprinting_PyQt6_V2
python3 examples/compare_screen_example.py
```

This will launch a demonstration window with:
- A "Load Sample Data" button to populate test data
- The complete Compare Screen with all tabs:
  - Summary tab
  - Charts tab with visualization options
  - Raw data tab
  - Comparison details tab

## Running Unit Tests

To verify the Compare Screen chart functionality:

```bash
cd /Users/flowgirl/Documents/FolderHackingAnalysis/Pawprinting_PyQt6_V2
python3 -m unittest tests/test_compare_screen_charts.py
```

## Directory Structure

The Compare Screen implementation consists of multiple modular components:

- **Base Structure**: `compare_screen_part1_structure.py`, `compare_screen_part2_ui_setup.py`
- **Tab Components**: `compare_screen_part3_comparison_tab.py`, `compare_screen_part4c1_raw_data_tab.py`, `compare_screen_part4c2_summary_tab.py`
- **Data Processing**: `compare_screen_part4c3a_data_loading.py`, `compare_screen_part4c3b_diff_generation.py`, `compare_screen_part4c3c_pattern_analysis.py`

### Chart Components:
- **Data Extraction**: `compare_screen_part4c3d_1_chart_data_extraction.py`
- **Chart Types**:
  - Radar: `compare_screen_part4c3d_2_radar_chart.py`
  - Bar: `compare_screen_part4c3d_3_bar_chart.py`
  - Line: `compare_screen_part4c3d_4_line_chart.py`
  - Pie: `compare_screen_part4c3d_5_pie_chart.py`
  - Heatmap: `compare_screen_part4c3d_6_heatmap_chart.py`
- **Insights**: `compare_screen_part4c3d_7a_base_insights.py`, `compare_screen_part4c3d_7b_advanced_insights.py`
- **Export Functions**: Files 8a through 8i
- **UI Components**: Files 9a through 10i
- **Integration**: `compare_screen_part4c3d_11_integration.py`

## Main Features

- **Interactive Charts**: Radar, bar, line, pie, and heatmap visualizations
- **Data Export**: Export as images, CSV, HTML reports, or text summaries
- **Filter Controls**: Filter by category and severity
- **Dark Theme UI**: Consistent styling with neon purple accents
- **Detailed Insights**: Pattern analysis with recommended actions

## Troubleshooting

If you encounter errors with matplotlib:
```bash
pip3 install matplotlib numpy
```

For PyQt6 issues:
```bash
pip3 install PyQt6
```
