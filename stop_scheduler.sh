#!/bin/bash
# Stop YouTube Upload Scheduler
# Usage: ./stop_scheduler.sh

SESSION_NAME="youtube_upload"

if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "⚠️  No scheduler session found"
    exit 1
fi

echo "🛑 Stopping YouTube Upload Scheduler..."
tmux kill-session -t $SESSION_NAME

echo "✅ Scheduler stopped"
