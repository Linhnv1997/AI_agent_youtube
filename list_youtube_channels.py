"""
Script để list tất cả các kênh YouTube của bạn
Dùng để lấy Channel ID khi có nhiều kênh
"""
import pickle
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


def get_authenticated_service():
    """Xác thực với YouTube API"""
    credentials = None
    token_file = Path('token.pickle')
    
    # Load credentials
    if token_file.exists():
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)
    
    # Refresh hoặc tạo mới
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            if not Path('credentials.json').exists():
                print("❌ Không tìm thấy credentials.json")
                print("Hãy tạo OAuth credentials từ Google Cloud Console")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_file, 'wb') as token:
            pickle.dump(credentials, token)
    
    return build('youtube', 'v3', credentials=credentials)


def list_channels():
    """List tất cả kênh YouTube"""
    print("🔍 Đang tìm các kênh YouTube của bạn...")
    print("=" * 60)
    
    youtube = get_authenticated_service()
    if not youtube:
        return
    
    try:
        # Get channels
        request = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            mine=True
        )
        response = request.execute()
        
        channels = response.get('items', [])
        
        if not channels:
            print("⚠️  Không tìm thấy kênh YouTube nào!")
            print("Hãy đảm bảo tài khoản Google của bạn có kênh YouTube.")
            return
        
        print(f"✅ Tìm thấy {len(channels)} kênh:\n")
        
        for i, channel in enumerate(channels, 1):
            snippet = channel['snippet']
            stats = channel.get('statistics', {})
            
            print(f"📺 Kênh #{i}")
            print(f"   Tên: {snippet['title']}")
            print(f"   Channel ID: {channel['id']}")
            print(f"   Mô tả: {snippet.get('description', 'N/A')[:100]}...")
            print(f"   Subscribers: {stats.get('subscriberCount', 'N/A')}")
            print(f"   Videos: {stats.get('videoCount', 'N/A')}")
            print(f"   Views: {stats.get('viewCount', 'N/A')}")
            
            # Custom URL nếu có
            if 'customUrl' in snippet:
                print(f"   URL: youtube.com/{snippet['customUrl']}")
            
            print()
        
        print("=" * 60)
        print("\n💡 Cách sử dụng:")
        print("   1. Copy Channel ID của kênh bạn muốn upload")
        print("   2. Mở file config/settings.yaml")
        print("   3. Thêm vào phần youtube:")
        print("      youtube:")
        print("        channel_id: \"UCxxx...\"  # Paste Channel ID")
        print()
        print("   Nếu để trống, video sẽ upload lên kênh mặc định")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        print("\nĐảm bảo bạn đã:")
        print("   1. Enable YouTube Data API v3")
        print("   2. Tạo OAuth credentials")
        print("   3. Đặt file credentials.json trong thư mục dự án")


if __name__ == "__main__":
    list_channels()
