#!/bin/bash
# Flutter Jobs Daily Daemon
# Runs continuously and executes daily search at 8:00 UTC (9AM Nigeria)

SCRIPT_DIR="/root/.openclaw/workspace/scripts"
LOG_DIR="/root/.openclaw/workspace/logs"
LAST_RUN_FILE="$LOG_DIR/.last-flutter-jobs"

mkdir -p "$LOG_DIR"

echo "Flutter Jobs Daemon started..."

while true; do
    CURRENT_HOUR=$(date -u +%H)
    TODAY=$(date +%Y-%m-%d)
    
    # Check if we should run (8:00 UTC = 9AM Nigeria)
    if [ "$CURRENT_HOUR" = "08" ]; then
        LAST_RUN=$(cat "$LAST_RUN_FILE" 2>/dev/null)
        
        if [ "$LAST_RUN" != "$TODAY" ]; then
            echo "Running daily Flutter jobs search..."
            python3 "$SCRIPT_DIR/flutter-jobs-scraper.py"
            echo "$TODAY" > "$LAST_RUN_FILE"
            echo "Search complete. Results saved."
        fi
    fi
    
    # Check every hour
    sleep 3600
done
