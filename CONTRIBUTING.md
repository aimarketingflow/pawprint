# Contributing to Pawprinting PyQt6 V2

Thank you for considering contributing to the Pawprinting PyQt6 V2 project! This document provides guidelines and steps for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

If you find a bug, please create a detailed issue that includes:

1. A clear, descriptive title
2. Steps to reproduce the bug
3. Expected behavior
4. Actual behavior
5. Screenshots if applicable
6. Your environment details (OS, Python version, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:

1. A clear, descriptive title
2. Detailed description of the proposed feature
3. Any relevant mockups or examples
4. Explanation of why this feature would be beneficial

### Pull Requests

1. Fork the repository and create your branch from `main`
2. Install development dependencies:
   ```bash
   python3 -m venv venv_pawprinting_pyqt6_dev
   source venv_pawprinting_pyqt6_dev/bin/activate
   pip3 install -r requirements.txt
   ```
3. Make your changes, adhering to the existing code style
4. Add comprehensive tests for your changes when applicable
5. Ensure all tests pass
6. Update documentation as needed
7. Create a pull request with a descriptive title and detailed description

## Development Setup

### Environment Setup

```bash
# Clone the repo
git clone git@github.com:aimarketingflow/pawprint.git
cd pawprint

# Create a virtual environment
python3 -m venv venv_pawprinting_pyqt6
source venv_pawprinting_pyqt6/bin/activate

# Install dependencies
pip3 install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
python3 -m unittest discover

# Run specific test
python3 -m unittest tests/test_specific.py
```

### Development Best Practices

1. **Modular Design**: Keep functionality in modular components
2. **Dark Mode UI**: Maintain dark mode UI with neon purple accent styling
3. **Comprehensive Logging**: Include detailed logging for all actions with progress tracking
4. **Error Handling**: Add robust error handling and recovery mechanisms
5. **Documentation**: Update documentation for any new or changed functionality
6. **Testing**: Include appropriate tests for new functionality

### Folder Structure

Please maintain the following structure for new contributions:

```
pawprint/
├── screens/              # UI screens
├── utils/                # Utilities and backend logic
│   └── automation/       # Automation-related utilities
├── components/           # Reusable UI components
├── resources/            # Icons, assets, etc.
├── docs/                 # Documentation 
├── tests/                # Test files
├── config/               # Configuration files
└── logs/                 # Log output directory
```

## Pull Request Review Process

1. At least one project maintainer will review the pull request
2. Automated tests must pass
3. Code should follow project style and quality guidelines
4. Documentation must be updated as needed

## Style Guidelines

- Follow PEP 8 for Python code
- Use descriptive variable and function names
- Include docstrings for all functions, classes, and modules
- Comment complex sections of code
- Maintain consistent indentation (4 spaces for Python)

## License

By contributing, you agree that your contributions will be licensed under the project's [GNU GPL v3 License](LICENSE).
