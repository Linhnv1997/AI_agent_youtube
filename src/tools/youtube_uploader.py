"""
YouTube API integration for uploading videos
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from loguru import logger
import pickle


class YouTubeUploader:
    """Xử lý upload video lên YouTube"""
    
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.credentials = None
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Xác thực với YouTube API"""
        token_file = Path('token.pickle')
        
        # Load credentials từ file nếu có
        if token_file.exists():
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)
        
        # Nếu không có credentials hoặc đã hết hạn
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                # Tạo credentials.json tạm thời
                self._create_credentials_file()
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            
            # Lưu credentials
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)
        
        # Build YouTube service
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
        logger.info("✅ YouTube API authenticated successfully")
    
    def _create_credentials_file(self):
        """Tạo file credentials.json từ env variables"""
        credentials_content = {
            "installed": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uris": ["http://localhost"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        
        import json
        with open('credentials.json', 'w') as f:
            json.dump(credentials_content, f)
    
    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: list[str],
        category_id: str = "22",
        privacy_status: str = "public"
    ) -> Optional[Dict[str, Any]]:
        """
        Upload video lên YouTube
        
        Args:
            video_path: Đường dẫn video
            title: Tiêu đề video
            description: Mô tả video
            tags: Danh sách tags
            category_id: ID category YouTube
            privacy_status: public/private/unlisted
        
        Returns:
            Dict chứa thông tin video đã upload
        """
        try:
            logger.info(f"📤 Uploading video: {video_path.name}")
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': privacy_status
                }
            }
            
            # Upload video
            media = MediaFileUpload(
                str(video_path),
                chunksize=-1,
                resumable=True
            )
            
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.success(f"✅ Video uploaded successfully: {video_url}")
            
            return {
                'video_id': video_id,
                'video_url': video_url,
                'title': title,
                'status': 'success'
            }
            
        except Exception as e:
            logger.error(f"❌ Error uploading video: {e}")
            return None
