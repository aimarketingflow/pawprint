# Pawprinting PyQt6 V2 - Command Line Interface Guide

This comprehensive guide covers all command line functionality available in the Pawprinting PyQt6 V2 project. Use these commands to automate pawprinting tasks, manage pawprint history, and perform batch operations without the GUI.

## Table of Contents

- [Installation and Setup](#installation-and-setup)
- [Basic Usage](#basic-usage)
- [Automation Commands](#automation-commands)
- [Diagnostic Commands](#diagnostic-commands)
- [Configuration Options](#configuration-options)
- [Recommended Aliases](#recommended-aliases)
- [Logging and Output](#logging-and-output)
- [Troubleshooting](#troubleshooting)

## Installation and Setup

### Prerequisites

- Python 3.9+
- All dependencies installed (`pip3 install -r requirements.txt`)
- Virtual environment activated (`source venv_pawprinting_pyqt6/bin/activate`)

### Setting Up Your Environment

```bash
# Clone the repository
git clone git@github.com:aimarketingflow/pawprint.git
cd Pawprinting_PyQt6_V2

# Create and activate virtual environment
python3 -m venv venv_pawprinting_pyqt6
source venv_pawprinting_pyqt6/bin/activate

# Install dependencies
pip3 install -r requirements.txt
```

## Basic Usage

### Starting the GUI Application

```bash
# From the project root with virtual environment activated
python3 pawprint_pyqt6_main.py
```

### Running Pawprint Generation from CLI

```bash
# Generate a pawprint for a folder
python3 pawprint_pyqt6_main.py --cli --generate --folder "/path/to/folder" --output "/path/to/output.pawprint"

# Generate a pawprint with options
python3 pawprint_pyqt6_main.py --cli --generate --folder "/path/to/folder" --depth 5 --include-hidden
```

## Automation Commands

The `cli_automation.py` script provides comprehensive automation capabilities:

### Pawprint History Management

```bash
# List all pawprints in history
./cli_automation.py --list-history

# View details for a specific pawprint entry
./cli_automation.py --list-history --detail --id "PAWPRINT_ID"
```

### Batch Refresh Operations

```bash
# Refresh all pawprints in history
./cli_automation.py --refresh-all

# Refresh only pawprints from the last 7 days
./cli_automation.py --refresh-recent

# Refresh pawprints from the last 30 days
./cli_automation.py --refresh-recent --days 30

# Refresh a specific folder
./cli_automation.py --refresh-folder "/path/to/folder"
```

### Progress and Monitoring

All commands show real-time progress with:
- Current operation status
- Percent complete indicator
- ETA for completion
- Log file path for detailed monitoring

## Diagnostic Commands

```bash
# Run system diagnostics
./cli_automation.py --diagnostic

# Test with a specific folder
./cli_automation.py --diagnostic --test-folder "/path/to/test/folder"

# Verbose diagnostics for detailed output
./cli_automation.py --diagnostic --verbose
```

## Configuration Options

The CLI supports various configuration options:

```bash
# Specify custom data directory
./cli_automation.py --data-dir "/path/to/data" --list-history

# Specify custom log directory
./cli_automation.py --log-dir "/path/to/logs" --refresh-all

# Enable verbose logging
./cli_automation.py --verbose --refresh-recent
```

## Recommended Aliases

Add these to your `.zshrc` or `.bash_profile` for convenience:

```bash
# General usage
alias pawprint='cd /path/to/Pawprinting_PyQt6_V2 && source venv_pawprinting_pyqt6/bin/activate && python3 pawprint_pyqt6_main.py'

# CLI automation
alias pawprint-cli='cd /path/to/Pawprinting_PyQt6_V2 && source venv_pawprinting_pyqt6/bin/activate && ./cli_automation.py'

# Common operations
alias pawprint-history='pawprint-cli --list-history'
alias pawprint-refresh-all='pawprint-cli --refresh-all'
alias pawprint-refresh-recent='pawprint-cli --refresh-recent'
```

## Logging and Output

All CLI commands generate:

1. **Terminal output** - Real-time progress and status
2. **Log files** - Detailed logs stored in `/logs` directory
3. **Summary files** - Markdown summaries of operations in `/logs` directory

### Log File Structure

```
logs/
├── cli_automation_20250627_122536.log   # Detailed timestamped log
├── cli_summary_20250627_122536.md       # Operation summary in markdown
└── ...
```

## Troubleshooting

### Common Issues

#### Command Not Found
```
-bash: ./cli_automation.py: Permission denied
```
**Solution**: Ensure the file has execution permissions:
```bash
chmod +x ./cli_automation.py
```

#### Import Errors
```
ImportError: No module named 'PyQt6'
```
**Solution**: Activate the virtual environment:
```bash
source venv_pawprinting_pyqt6/bin/activate
```

#### Data Access Errors
```
Error: Cannot access data directory
```
**Solution**: Check permissions or specify an accessible directory:
```bash
./cli_automation.py --data-dir "/Users/username/Documents/pawprint_data" --refresh-all
```

### Getting Help

For detailed help on all available commands and options:

```bash
./cli_automation.py --help
```

For diagnostic information:

```bash
./cli_automation.py --diagnostic --verbose
```

## Examples

### Complete Refresh Workflow

```bash
# List current history
./cli_automation.py --list-history

# Refresh all pawprints
./cli_automation.py --refresh-all --verbose

# Verify results
./cli_automation.py --list-history
```

### Targeted Refresh Example

```bash
# Refresh only recently modified folders (last 14 days)
./cli_automation.py --refresh-recent --days 14 --verbose
```

### Diagnostic Check

```bash
# Run full diagnostics with a test folder
./cli_automation.py --diagnostic --test-folder "/Users/username/Documents/test_data"
```
