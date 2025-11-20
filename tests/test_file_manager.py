"""
Tests for VideoFileManager
"""
import pytest
from pathlib import Path
from src.utils.file_manager import VideoFileManager


def test_file_manager_initialization(tmp_path):
    """Test khởi tạo VideoFileManager"""
    manager = VideoFileManager(tmp_path)
    assert manager.video_folder == tmp_path
    assert manager.video_folder.exists()


def test_get_all_videos(tmp_path):
    """Test lấy danh sách videos"""
    # Create test video files
    (tmp_path / "video1.mp4").touch()
    (tmp_path / "video2.avi").touch()
    (tmp_path / "not_video.txt").touch()
    
    manager = VideoFileManager(tmp_path)
    videos = manager.get_all_videos()
    
    assert len(videos) == 2
    assert all(v.suffix in ['.mp4', '.avi'] for v in videos)


def test_mark_and_get_uploaded(tmp_path):
    """Test đánh dấu và lấy danh sách đã upload"""
    video = tmp_path / "test.mp4"
    video.touch()
    
    manager = VideoFileManager(tmp_path)
    
    # Initially no uploaded videos
    assert len(manager.get_uploaded_videos()) == 0
    
    # Mark as uploaded
    manager.mark_as_uploaded(video)
    
    # Check if marked
    uploaded = manager.get_uploaded_videos()
    assert "test.mp4" in uploaded
