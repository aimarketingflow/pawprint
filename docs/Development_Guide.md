# Pawprinting PyQt6 V2 Development Guide

This guide provides detailed information for developers working on the Pawprinting PyQt6 V2 project including diagnostic modes, testing procedures, and best practices.

## Diagnostic Mode

The application supports a diagnostic mode that can be activated to verify functionality, versions, and dependencies. This mode runs a smaller test dataset to quickly validate core features.

### Using Diagnostic Mode

```bash
# Run the application in diagnostic mode
python3 pawprint_pyqt6_main.py --diagnostic

# Run with verbose logging
python3 pawprint_pyqt6_main.py --diagnostic --verbose

# Run specific component tests
python3 pawprint_pyqt6_main.py --diagnostic --component=automation
```

### Available Diagnostic Flags

| Flag | Description |
|------|-------------|
| `--diagnostic` | Enables diagnostic mode |
| `--verbose` | Increases logging detail |
| `--component=X` | Tests a specific component (options: automation, pawprint, ui) |
| `--test-folder=PATH` | Specifies a test folder for pawprint generation |
| `--skip-ui` | Runs diagnostics without launching the UI |
| `--log-to-file` | Ensures all output is logged to a diagnostic file |

## Development Environment Setup

### Required Tools

- Python 3.9+
- Git
- Qt Designer (optional, for UI editing)
- pytest (for running tests)

### Setting Up Your Environment

1. Clone the repository:
   ```bash
   git clone git@github.com:aimarketingflow/pawprint.git
   cd pawprint
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv_pawprinting_pyqt6_dev
   source venv_pawprinting_pyqt6_dev/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip3 install -r requirements.txt
   pip3 freeze > requirements_pawprinting_pyqt6_dev.txt  # Snapshot dependencies
   ```

## Testing

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_automation_system.py

# Run with coverage report
python3 -m pytest --cov=. tests/
```

### Writing New Tests

1. Create test files in the `tests/` directory
2. Follow the naming convention `test_*.py`
3. Use the `unittest` framework
4. Include both unit tests and integration tests
5. Use the `TestAutomationAction` class as a template for testing actions

## Code Style Guidelines

- Follow PEP 8 for Python code
- Use 4 spaces for indentation (no tabs)
- Maximum line length of 100 characters
- Document all classes and functions with docstrings
- Use descriptive variable and function names
- Include type hints where appropriate

## Project Structure

```
pawprint/
├── screens/              # UI screens
├── utils/                # Utilities and backend logic
│   ├── automation_*.py   # Automation-related utilities
│   └── ...
├── components/           # Reusable UI components
├── resources/            # Icons, assets, etc.
├── docs/                 # Documentation 
├── tests/                # Test files
├── config/               # Configuration files
└── logs/                 # Log output directory
```

## UI Guidelines

- Maintain dark mode UI with neon purple accent colors
- All screens should be scrollable using the scrollable screen utility
- Use consistent spacing and margins (10px for content, 15px for sections)
- Group related controls together
- Provide clear, concise labels and tooltips

## Logging Standards

All code should include proper logging:

- Use the Python `logging` module
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Include contextual information in log messages
- Log the start and end of significant operations
- Add progress tracking for long-running operations

Example:

```python
import logging

logger = logging.getLogger(__name__)

def process_function():
    logger.info("Starting process")
    try:
        # Do work
        logger.info("Process completed successfully")
    except Exception as e:
        logger.error(f"Process failed: {str(e)}", exc_info=True)
        raise
```

## Error Handling

- Use try/except blocks to catch exceptions
- Log all exceptions with appropriate context
- Provide user-friendly error messages
- Implement recovery mechanisms where possible
- Always clean up resources in finally blocks

## Contributing Workflow

1. Create a new branch for your feature: `git checkout -b feature/your-feature-name`
2. Make your changes, following the code style guidelines
3. Write tests for your changes
4. Run all tests to ensure nothing was broken
5. Update documentation as needed
6. Commit your changes with clear commit messages
7. Push your branch and create a pull request
8. Respond to any feedback in the code review

## Release Process

1. Update version number in `VERSION` file
2. Update CHANGELOG.md with changes
3. Run all tests to ensure everything passes
4. Create a release tag: `git tag v1.x.x`
5. Push the tag: `git push origin v1.x.x`
6. Create a GitHub release with release notes

## Debugging Tips

- Use the `--diagnostic` flag to run in diagnostic mode
- Check the logs in the `logs/` directory
- Use the Python debugger (pdb) or an IDE debugger
- For UI issues, enable the debug console with `--debug-ui`
- For automation issues, run individual actions with `--debug-automation`

## Performance Considerations

- Profile code for performance bottlenecks
- Use caching for expensive operations
- Avoid unnecessary file I/O operations
- Run heavy processing in background threads
- Update UI asynchronously to avoid freezes
- Use progress reporting for long-running operations
