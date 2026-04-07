#!/bin/bash
# Flutter Jobs Daily Scraper
# Runs daily at 9:00 AM Nigeria time
# Version: 1.0.0

SCRIPT_DIR="/root/.openclaw/workspace/scripts"
LOG_DIR="/root/.openclaw/workspace/logs"
PYTHON_SCRIPT="$SCRIPT_DIR/flutter-jobs-scraper.py"

TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/flutter-jobs-${TODAY}.md"

# Create log directory
mkdir -p "$LOG_DIR"

echo "Starting Flutter Jobs search for $TODAY..."

# Run the Python scraper
python3 "$PYTHON_SCRIPT"

echo "Search complete. Results saved to: $LOG_FILE"
