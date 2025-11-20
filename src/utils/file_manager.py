"""
File management utilities for handling video files
"""
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import json
from loguru import logger


class VideoFileManager:
    """Quản lý video files trong folder"""
    
    def __init__(self, video_folder: Path):
        self.video_folder = Path(video_folder)
        self.uploaded_log_file = self.video_folder / ".uploaded.json"
        self._ensure_folder_exists()
    
    def _ensure_folder_exists(self):
        """Đảm bảo folder tồn tại"""
        self.video_folder.mkdir(parents=True, exist_ok=True)
    
    def get_all_videos(self) -> List[Path]:
        """Lấy tất cả video files"""
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
        videos = []
        
        for ext in video_extensions:
            videos.extend(self.video_folder.glob(f'*{ext}'))
        
        return sorted(videos)
    
    def get_uploaded_videos(self) -> set:
        """Lấy danh sách video đã upload"""
        if not self.uploaded_log_file.exists():
            return set()
        
        try:
            with open(self.uploaded_log_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data.get('uploaded', []))
        except Exception as e:
            logger.error(f"Error reading uploaded log: {e}")
            return set()
    
    def mark_as_uploaded(self, video_path: Path):
        """Đánh dấu video đã được upload"""
        uploaded = self.get_uploaded_videos()
        uploaded.add(str(video_path.name))
        
        data = {
            'uploaded': list(uploaded),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            with open(self.uploaded_log_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Marked {video_path.name} as uploaded")
        except Exception as e:
            logger.error(f"Error marking video as uploaded: {e}")
    
    def get_next_video(self) -> Optional[Path]:
        """Lấy video tiếp theo cần upload"""
        all_videos = self.get_all_videos()
        uploaded = self.get_uploaded_videos()
        
        for video in all_videos:
            if video.name not in uploaded:
                return video
        
        return None
    
    def get_pending_videos_count(self) -> int:
        """Đếm số video còn chờ upload"""
        all_videos = self.get_all_videos()
        uploaded = self.get_uploaded_videos()
        return len([v for v in all_videos if v.name not in uploaded])
