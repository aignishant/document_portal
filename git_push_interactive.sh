#!/usr/bin/env bash

# Log file for the interactive git push script
LOG_FILE="pipeline_log.txt"

echo "=== Interactive Git Push Started at $(date) ===" | tee -a "$LOG_FILE"

# Stage all changes
if git add . | tee -a "$LOG_FILE"; then
  echo "✅ Staged changes" | tee -a "$LOG_FILE"
else
  echo "❌ git add failed" | tee -a "$LOG_FILE"
  exit 1
fi

# Prompt user for a commit message
read -p "Enter commit message: " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
  echo "Commit message cannot be empty. Exiting." | tee -a "$LOG_FILE"
  exit 1
fi

# Commit the staged changes
if git commit -m "$COMMIT_MSG" | tee -a "$LOG_FILE"; then
  echo "✅ Changes committed" | tee -a "$LOG_FILE"
else
  echo "❌ Git commit failed" | tee -a "$LOG_FILE"
  exit 1
fi

# Push to remote, using GITHUB_TOKEN if set
if [ -n "$GITHUB_TOKEN" ]; then
  echo "Using GITHUB_TOKEN for authentication." | tee -a "$LOG_FILE"
  AUTH_URL="https://${GITHUB_TOKEN}@github.com/aignishant/document_portal.git"
  if git push "$AUTH_URL" main | tee -a "$LOG_FILE"; then
    echo "✅ Changes pushed to remote" | tee -a "$LOG_FILE"
  else
    echo "❌ Git push failed" | tee -a "$LOG_FILE"
    exit 1
  fi
else
  echo "Using standard git push (credentials must be configured)." | tee -a "$LOG_FILE"
  if git push origin main | tee -a "$LOG_FILE"; then
    echo "✅ Changes pushed to remote" | tee -a "$LOG_FILE"
  else
    echo "❌ Git push failed" | tee -a "$LOG_FILE"
    exit 1
  fi
fi

echo "=== Interactive Git Push Completed at $(date) ===" | tee -a "$LOG_FILE"
