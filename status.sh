#!/bin/bash
# Check status of YouTube Upload Scheduler
# Usage: ./status.sh

SESSION_NAME="youtube_upload"

echo "📊 YouTube Upload Scheduler Status"
echo "=" | awk '{printf "%0.s=", $1}' | head -c 50; echo ""

# Check if tmux session exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "✅ Status: RUNNING"
    echo "📺 Session: $SESSION_NAME"
    echo ""
    
    # Get session info
    echo "Session info:"
    tmux list-sessions | grep $SESSION_NAME
    echo ""
    
    # Show recent logs
    echo "Recent activity (last 10 lines from logs/app.log):"
    echo "---"
    if [ -f logs/app.log ]; then
        tail -10 logs/app.log
    else
        echo "No logs found"
    fi
    echo ""
    
    # Show pending videos
    echo "📊 Videos status:"
    python3 -c "
from src.utils.file_manager import VideoFileManager
from src.utils.config import Settings

settings = Settings()
fm = VideoFileManager(settings.VIDEO_FOLDER_PATH)
pending = fm.get_pending_videos_count()
uploaded = len(fm.get_uploaded_videos())

print(f'  Pending: {pending}')
print(f'  Uploaded: {uploaded}')
"
    
else
    echo "❌ Status: STOPPED"
    echo ""
    echo "Start with: ./start_scheduler.sh"
fi

echo ""
echo "Commands:"
echo "  Start:  ./start_scheduler.sh"
echo "  Stop:   ./stop_scheduler.sh"
echo "  View:   ./view_logs.sh"
echo "  Status: ./status.sh"
