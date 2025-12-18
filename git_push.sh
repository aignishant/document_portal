#!/bin/bash

# Log file


log_message() {
    echo "$1"
}

log_error() {
    echo "❌ ERROR: $1" | tee -a "pipeline_log.txt"
}

log_message "--- Git Push Step Started ---"

# Check if there are changes to commit
if git diff-index --quiet HEAD --; then
    log_message "ℹ️ No changes to commit."
else
    git add . 2>>pipeline_log.txt
    if git commit -m "chore: Automated commit" 2>>pipeline_log.txt; then
        log_message "✅ Changes Committed"
    else
        log_error "Git Commit Failed."
        exit 1
    fi
fi

# Push Logic
REMOTE_URL="https://github.com/aignishant/document_portal.git"
log_message "Pushing to $REMOTE_URL..."

if [ -n "$GITHUB_TOKEN" ]; then
    log_message "Using GITHUB_TOKEN for authentication."
    auth_url="https://${GITHUB_TOKEN}@github.com/aignishant/document_portal.git"
    if git push "$auth_url" main 2>>pipeline_log.txt; then
        log_message "✅ Changes Pushed to Remote"
    else
        log_error "Git Push Failed."
        exit 1
    fi
else
    log_message "Using standard git push (credentials must be configured)."
    if git push origin main 2>>pipeline_log.txt; then
        log_message "✅ Changes Pushed to Remote"
    else
        log_error "Git Push Failed."
        exit 1
    fi
fi
