# Pawprinting PyQt6 V2 Terminal Guide

## Running the Main Application

To run the main application with the full GUI:

```bash
cd /Users/flowgirl/Documents/FolderHackingAnalysis/Pawprinting_PyQt6_V2
python3 run_pawprint_pyqt6.py
```

### Opening Files Directly

To open a specific pawprint file directly when launching the app:

```bash
# Open a pawprint file in the analyze screen
python3 run_pawprint_pyqt6.py --file test_pawprint.json

# Open a fractal configuration file in the fractal butterfly screen 
python3 run_pawprint_pyqt6.py --fractal my_fractal_config.json
```

This will:
1. Set up a virtual environment if it doesn't exist
2. Install all necessary dependencies
3. Launch the Pawprinting PyQt6 V2 application

## Database CLI Commands

The database functionality can be accessed directly from the command line:

### List Recent Pawprints

```bash
cd /Users/flowgirl/Documents/FolderHackingAnalysis/Pawprinting_PyQt6_V2
python3 cli_database.py list --limit 10
```

### Search Pawprints

```bash
# Search by name
python3 cli_database.py search --name "test"

# Search by text content
python3 cli_database.py search --text "song"

# Search by date range
python3 cli_database.py search --from-date 2025-05-01 --to-date 2025-06-03

# Search by entropy range
python3 cli_database.py search --min-entropy 0.5 --max-entropy 0.9

# Search with multiple filters
python3 cli_database.py search --name "test" --min-entropy 0.7
```

### View Specific Pawprint Details

```bash
python3 cli_database.py view --id 1
```

### Delete Pawprints

```bash
# Delete a specific pawprint
python3 cli_database.py delete --id 1

# Delete with confirmation prompt
python3 cli_database.py delete --id 1 --confirm

# Force delete without confirmation
python3 cli_database.py delete --id 1 --force
```

### Export Pawprints

```bash
# Export all pawprints
python3 cli_database.py export --output-dir ./exports

# Export specific pawprints
python3 cli_database.py export --id 1 --output-dir ./exports
```

### Show Database Statistics

```bash
python3 cli_database.py stats
```

### Import Existing Configurations

```bash
python3 cli_database.py import --config-dir ./config
```

## Notes

- All pawprint data is stored locally in the SQLite database
- The database file is located at `./database/pawprints.db`
- The history screen can be accessed from the main application via File > History or by pressing Ctrl+H
