#!/bin/bash

# Pipeline Log File
LOG_FILE="pipeline_log.txt"
echo "=== Lenient Pipeline Started at $(date) ===" > "$LOG_FILE"

log_error() {
    echo "❌ ERROR: $1 (Continuing...)" | tee -a "$LOG_FILE"
}

log_message() {
    echo "$1" | tee -a "$LOG_FILE"
}

# 1. Format Code (Includes Linting and Testing via format_code.sh which uses myvenv)
log_message "--- Step 1: Formatting and Testing ---"
if ./format_code.sh >> "$LOG_FILE" 2>&1; then
    log_message "✅ Formatting and Tests Passed"
else
    log_error "Formatting Check Failed. See $LOG_FILE for details."
fi

# 2. Git Push
log_message "--- Step 2: Git Push ---"
git add . >> "$LOG_FILE" 2>&1

# Check if there are changes to commit
if ! git diff-index --quiet HEAD --; then
     if git commit -m "chore: Automated pipeline commit (Lenient)" >> "$LOG_FILE" 2>&1; then
        log_message "✅ Changes Committed"
     else
        log_error "Git Commit Failed."
     fi
else
    log_message "ℹ️ No changes to commit."
fi

# Use GITHUB_TOKEN if available, otherwise fallback to standard push
if [ -n "$GITHUB_TOKEN" ]; then
    log_message "Using GITHUB_TOKEN for authentication."
    auth_url="https://${GITHUB_TOKEN}@github.com/aignishant/document_portal.git"
    if git push "$auth_url" main >> "$LOG_FILE" 2>&1; then
        log_message "✅ Changes Pushed to Remote"
    else
        log_error "Git Push Failed."
    fi
else
    log_message "Using standard git push (credentials must be configured)."
    if git push origin main >> "$LOG_FILE" 2>&1; then
        log_message "✅ Changes Pushed to Remote"
    else
        log_error "Git Push Failed."
    fi
fi

log_message "=== Pipeline Finished at $(date) ==="
log_message "Check $LOG_FILE for any errors."
