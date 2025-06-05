#!/bin/bash
# Text to Fractal Demo Launcher
# Created: 2025-06-02

# Set up colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Record start time
START_TIME=$(date +%s)

echo -e "${BLUE}===================================================${NC}"
echo -e "${BLUE}       Text-to-Fractal Demonstration Tool${NC}"
echo -e "${BLUE}===================================================${NC}"
echo

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create timestamp for logs
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$SCRIPT_DIR/logs/launcher_$TIMESTAMP.log"

# Make sure log directory exists
mkdir -p "$SCRIPT_DIR/logs"
touch "$LOG_FILE"

# Function for logging
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "$LOG_FILE"
}

# Function to display progress
progress() {
    local current=$1
    local total=$2
    local percent=$((current * 100 / total))
    local completed=$((percent / 2))
    local remaining=$((50 - completed))
    
    printf "\r[${YELLOW}"
    printf "%0.s#" $(seq 1 $completed)
    printf "${NC}"
    printf "%0.s " $(seq 1 $remaining)
    printf "${NC}] ${YELLOW}%d%%${NC}" $percent
}

# Check for virtual environment
log "Checking for virtual environment..."
if [ ! -d "$PROJECT_DIR/fractal_butterfly_venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    log "Creating virtual environment..."
    cd "$PROJECT_DIR" && python3 -m venv fractal_butterfly_venv
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to create virtual environment. Exiting.${NC}"
        log "Failed to create virtual environment. Exiting."
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
log "Activating virtual environment..."
source "$PROJECT_DIR/fractal_butterfly_venv/bin/activate"

# Check if required packages are installed
log "Checking required packages..."
echo -e "${YELLOW}Checking required packages...${NC}"

# First, check if PyQt6 is installed
if ! python3 -c "import PyQt6" &> /dev/null; then
    echo -e "${YELLOW}Installing required packages...${NC}"
    log "Installing required packages..."
    pip3 install PyQt6 numpy matplotlib
    
    # Create requirements file if it doesn't exist
    if [ ! -f "$PROJECT_DIR/requirements_fractal_butterfly_venv.txt" ]; then
        echo -e "${YELLOW}Creating requirements file...${NC}"
        log "Creating requirements file..."
        pip3 freeze > "$PROJECT_DIR/requirements_fractal_butterfly_venv.txt"
    fi
fi

# Ensure configs directory exists
log "Ensuring configs directory exists..."
mkdir -p "$PROJECT_DIR/configs"

# Run the text to fractal CLI
echo -e "${GREEN}Starting Text-to-Fractal demonstration...${NC}"
log "Starting Text-to-Fractal demonstration..."

cd "$SCRIPT_DIR" && python3 text_to_fractal_cli.py "$@"

# Get result code
RESULT=$?

# Calculate execution time
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
FORMATTED_DURATION=$(printf '%02d:%02d:%02d' $((DURATION / 3600)) $((DURATION % 3600 / 60)) $((DURATION % 60)))

echo
if [ $RESULT -eq 0 ]; then
    echo -e "${GREEN}Demonstration completed successfully in ${FORMATTED_DURATION}${NC}"
    log "Demonstration completed successfully in ${FORMATTED_DURATION}"
else
    echo -e "${RED}Demonstration failed after ${FORMATTED_DURATION}${NC}"
    log "Demonstration failed after ${FORMATTED_DURATION}"
fi

echo -e "${BLUE}Log file saved to: ${LOG_FILE}${NC}"
echo -e "${BLUE}Output directory: ${SCRIPT_DIR}/output${NC}"

# Create an alias suggestion
echo
echo -e "${YELLOW}To add a convenient alias to your shell, add this line to your ~/.zshrc:${NC}"
echo -e "${BLUE}alias text2fractal='cd $SCRIPT_DIR && ./run_text_to_fractal_demo.sh'${NC}"

# Deactivate virtual environment
deactivate

exit $RESULT
