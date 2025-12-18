#!/bin/bash

# Pipeline Log File
LOG_FILE="pipeline_log.txt"
echo "=== Pipeline Started at $(date) ===" > "$LOG_FILE"

log_and_exit() {
    echo "❌ ERROR: $1" | tee -a "$LOG_FILE"
    echo "Pipeline STOPPED due to failure." | tee -a "$LOG_FILE"
    exit 1
}

log_message() {
    echo "$1" | tee -a "$LOG_FILE"
}

# 1. Format Code (Includes Linting and Testing via format_code.sh which uses myvenv)
log_message "--- Step 1: Formatting and Testing ---"
if ./format_code.sh >> "$LOG_FILE" 2>&1; then
    log_message "✅ Formatting and Tests Passed"
else
    log_and_exit "Formatting/Testing Failed. See $LOG_FILE for details."
fi

# 2. Git Push
log_message "--- Step 2: Git Push ---"
git add . >> "$LOG_FILE" 2>&1
# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    log_message "ℹ️ No changes to commit."
else
    if git commit -m "chore: Automated pipeline commit" >> "$LOG_FILE" 2>&1; then
        log_message "✅ Changes Committed"
    else
         log_and_exit "Git Commit Failed."
    fi
fi

# Use GITHUB_TOKEN if available, otherwise fallback to standard push
if [ -n "$GITHUB_TOKEN" ]; then
    # Mask token in logs
    log_message "Using GITHUB_TOKEN for authentication."
    auth_url="https://${GITHUB_TOKEN}@github.com/aignishant/document_portal.git"
    if git push "$auth_url" main >> "$LOG_FILE" 2>&1; then
        log_message "✅ Changes Pushed to Remote"
    else
        log_and_exit "Git Push Failed."
    fi
else
    log_message "Using standard git push (credentials must be configured)."
    if git push origin main >> "$LOG_FILE" 2>&1; then
        log_message "✅ Changes Pushed to Remote"
    else
        log_and_exit "Git Push Failed."
    fi
fi

log_message "=== Pipeline Completed Successfully at $(date) ==="
log_message "All checks passed and changes pushed."
