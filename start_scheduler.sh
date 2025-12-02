#!/bin/bash
# Start YouTube Upload Scheduler in tmux
# Usage: ./start_scheduler.sh

SESSION_NAME="youtube_upload"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo "❌ tmux is not installed!"
    echo "Install with: sudo apt-get install tmux"
    exit 1
fi

# Check if session already exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "⚠️  Session '$SESSION_NAME' already exists!"
    echo ""
    echo "Options:"
    echo "  1. Attach to existing session: tmux attach -t $SESSION_NAME"
    echo "  2. Kill existing session: tmux kill-session -t $SESSION_NAME"
    echo "  3. Run this script again after killing"
    exit 1
fi

# Create new tmux session
echo "🚀 Starting YouTube Upload Scheduler..."
echo "📅 Schedule: Daily at 17:30 (Asia/Ho_Chi_Minh)"
echo ""

cd "$SCRIPT_DIR"

# Start tmux session in detached mode
tmux new-session -d -s $SESSION_NAME -n "scheduler" \
    "python3 main.py"

echo "✅ Scheduler started in tmux session: $SESSION_NAME"
echo ""
echo "Commands:"
echo "  📺 View logs:    tmux attach -t $SESSION_NAME"
echo "  🔌 Detach:       Press Ctrl+B, then D"
echo "  🛑 Stop:         tmux kill-session -t $SESSION_NAME"
echo "  📋 List:         tmux list-sessions"
echo ""
echo "The scheduler will upload 1 video daily at 09:00"
