#!/bin/bash
# View YouTube Upload Scheduler logs
# Usage: ./view_logs.sh

SESSION_NAME="youtube_upload"

if ! tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "⚠️  No scheduler session found"
    echo "Start with: ./start_scheduler.sh"
    exit 1
fi

echo "📺 Attaching to scheduler..."
echo "   Press Ctrl+B, then D to detach"
echo ""
sleep 1

tmux attach -t $SESSION_NAME
