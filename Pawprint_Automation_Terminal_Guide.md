# Pawprinting Automation Terminal Guide

This guide provides instructions for using the Pawprinting automation features via the command line.

## Basic Commands

### List Pawprint History
View all previously analyzed folders in the pawprint history:

```bash
python3 utils/automation_pawprint_cli.py list
```

### Refresh All Pawprints
Re-analyze all folders in the pawprint history:

```bash
python3 utils/automation_pawprint_cli.py refresh --type all
```

### Refresh Recent Pawprints
Re-analyze only the most recent N folders (default is 5):

```bash
python3 utils/automation_pawprint_cli.py refresh --type recent --count 5
```

### Refresh Specific Folders
Re-analyze specific folders by providing their paths:

```bash
python3 utils/automation_pawprint_cli.py refresh --type specific --folders "/path/to/folder1" "/path/to/folder2"
```

### Specify Output Folder
Set a custom output folder for the refreshed pawprints:

```bash
python3 utils/automation_pawprint_cli.py refresh --type all --output-folder "/path/to/output"
```

### Control Overwrite Behavior
Choose whether to overwrite existing pawprint files:

```bash
python3 utils/automation_pawprint_cli.py refresh --type all --overwrite True
```

## Advanced Usage

### Combine Options
You can combine multiple options as needed:

```bash
python3 utils/automation_pawprint_cli.py refresh --type recent --count 3 --output-folder "/custom/output" --overwrite False
```

### Get Help
For a full list of options and commands:

```bash
python3 utils/automation_pawprint_cli.py --help
```

## Automation System

### Running the Automation System
Start the automation system with default settings:

```bash
python3 utils/automation_system.py
```

### Scheduling Tasks
Configure task schedules in the automation state JSON file and start the system:

```bash
python3 utils/automation_system.py --state-file /path/to/custom/state.json
```
