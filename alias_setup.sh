#!/bin/bash
# Pawprinting PyQt6 Alias Setup
# Creates aliases for easy launching of the Pawprinting PyQt6 application

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define aliases
cat << EOF

# Add the following lines to your ~/.bashrc, ~/.zshrc, or ~/.bash_profile:

# Pawprinting PyQt6 aliases
alias pawprint='cd "$SCRIPT_DIR" && ./run_pawprint.sh'
alias pawprint_debug='cd "$SCRIPT_DIR" && python3 -m debugpy --wait-for-client --listen 5678 pawprint_pyqt6_main.py'

# For diagnostics and testing
alias pawprint_test='cd "$SCRIPT_DIR" && source venv_pawprinting_pyqt6/bin/activate && python3 -m pytest tests/'
alias pawprint_env='cd "$SCRIPT_DIR" && source venv_pawprinting_pyqt6/bin/activate'
alias pawprint_update='cd "$SCRIPT_DIR" && source venv_pawprinting_pyqt6/bin/activate && pip3 install -r requirements.txt'

EOF

# Create the actual alias file that can be sourced
cat > "$SCRIPT_DIR/pawprint_aliases.sh" << EOF
#!/bin/bash
# Pawprinting PyQt6 Aliases
# Source this file to add Pawprinting PyQt6 aliases to your shell

# Pawprinting PyQt6 aliases
alias pawprint='cd "$SCRIPT_DIR" && ./run_pawprint.sh'
alias pawprint_debug='cd "$SCRIPT_DIR" && python3 -m debugpy --wait-for-client --listen 5678 pawprint_pyqt6_main.py'

# For diagnostics and testing
alias pawprint_test='cd "$SCRIPT_DIR" && source venv_pawprinting_pyqt6/bin/activate && python3 -m pytest tests/'
alias pawprint_env='cd "$SCRIPT_DIR" && source venv_pawprinting_pyqt6/bin/activate'
alias pawprint_update='cd "$SCRIPT_DIR" && source venv_pawprinting_pyqt6/bin/activate && pip3 install -r requirements.txt'
EOF

chmod +x "$SCRIPT_DIR/pawprint_aliases.sh"

echo "Alias file created: $SCRIPT_DIR/pawprint_aliases.sh"
echo "Source this file to add Pawprinting PyQt6 aliases to your shell:"
echo "  source \"$SCRIPT_DIR/pawprint_aliases.sh\""
echo
echo "To add these aliases permanently, add the following line to your ~/.bashrc, ~/.zshrc, or ~/.bash_profile:"
echo "  source \"$SCRIPT_DIR/pawprint_aliases.sh\""
