# 🔐 Hướng Dẫn Setup YouTube OAuth

## 📋 Yêu Cầu

Để upload video lên YouTube, bạn cần:
1. Tài khoản Google/YouTube
2. Google Cloud Project với YouTube Data API v3 enabled
3. OAuth 2.0 credentials (file `credentials.json`)

## 🚀 Các Bước Setup

### Bước 1: Tạo Google Cloud Project

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"New Project"** hoặc chọn project hiện có
3. Đặt tên project (ví dụ: "AI YouTube Auto Upload")
4. Click **"Create"**

### Bước 2: Enable YouTube Data API v3

1. Trong project vừa tạo, vào **"APIs & Services"** > **"Library"**
2. Tìm kiếm **"YouTube Data API v3"**
3. Click vào API đó và nhấn **"Enable"**

### Bước 3: Cấu Hình OAuth Consent Screen (QUAN TRỌNG!)

1. Vào **"APIs & Services"** > **"OAuth consent screen"** (menu bên trái)
2. Chọn **"External"** (hoặc Internal nếu có Google Workspace)
3. Click **"Create"**

#### 3.1. OAuth consent screen - Page 1 (App information)
- **App name**: `AI YouTube Auto Upload`
- **User support email**: Chọn email của bạn
- **App logo**: (Optional - có thể bỏ qua)
- **Application home page**: (Optional - có thể bỏ qua)
- **Authorized domains**: (Optional - có thể bỏ qua)
- **Developer contact information**: Email của bạn
- Click **"Save and Continue"**

#### 3.2. OAuth consent screen - Page 2 (Scopes) ⚠️ QUAN TRỌNG
- Click **"ADD OR REMOVE SCOPES"** (button lớn màu xanh)
- Trong popup, tìm kiếm **"youtube"**
- Chọn 2 scopes sau:
  - ✅ `https://www.googleapis.com/auth/youtube` - Manage your YouTube account
  - ✅ `https://www.googleapis.com/auth/youtube.upload` - Upload YouTube videos
- Click **"UPDATE"** ở dưới popup
- Click **"Save and Continue"**

#### 3.3. OAuth consent screen - Page 3 (Test users) ⚠️ QUAN TRỌNG
- Click **"ADD USERS"**
- Nhập email YouTube của bạn (email sẽ upload video)
- Click **"Add"**
- Click **"Save and Continue"**

#### 3.4. OAuth consent screen - Page 4 (Summary)
- Review lại thông tin
- Click **"Back to Dashboard"**

### Bước 4: Tạo OAuth 2.0 Credentials

1. Vào **"APIs & Services"** > **"Credentials"** (menu bên trái)
2. Click **"+ Create Credentials"** (ở trên)
3. Chọn **"OAuth client ID"**
4. **Application type**: Chọn **"Desktop app"**
5. **Name**: `YouTube Uploader Desktop`
6. Click **"Create"**

### Bước 5: Download credentials.json

1. Sau khi tạo xong, click biểu tượng **Download** (⬇️) 
2. Lưu file với tên `credentials.json`
3. Copy file vào thư mục root của project:
   ```bash
   cp ~/Downloads/client_secret_*.json /home/linhnv1/project/AI_agent_youtube/credentials.json
   ```

### Bước 6: Xác thực lần đầu

```bash
cd /home/linhnv1/project/AI_agent_youtube
python3 list_youtube_channels.py
```

Script sẽ:
1. Mở browser để bạn đăng nhập Google
2. Yêu cầu cấp quyền upload video
3. Lưu token vào `token.pickle` (dùng cho lần sau)
4. Hiển thị danh sách kênh YouTube của bạn

## ⚠️ Lưu Ý Quan Trọng

### Quota Limits

YouTube API có giới hạn quota:
- **Default quota**: 10,000 units/day
- **Upload 1 video**: ~1,600 units
- **Có thể upload**: ~6 videos/day

Nếu cần tăng quota, request tại [Google Cloud Console](https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas)

### Bảo mật

⚠️ **KHÔNG COMMIT** các file sau vào Git:
- `credentials.json` - OAuth credentials
- `token.pickle` - Access token
- `.env` - API keys

Đã thêm vào `.gitignore`:
```
credentials.json
token.pickle
.env
```

## 🧪 Kiểm tra Setup

### Test 1: List channels
```bash
python3 list_youtube_channels.py
```

Kết quả mong đợi:
```
📺 Danh sách kênh YouTube:
============================================================
1. [Tên Kênh]
   Channel ID: UCxxxxxxxxxx
   Subscribers: xxx
   Videos: xxx
```

### Test 2: Upload video thử
```bash
# Thêm video test vào folder
cp test_video.mp4 data/videos/

# Chạy upload
python3 main.py
```

## 🔧 Troubleshooting

### Lỗi: "insufficient authentication scopes"

**Nguyên nhân**: Token thiếu quyền upload

**Giải pháp**:
```bash
# Xóa token cũ
rm token.pickle

# Xác thực lại với đủ scopes
python3 list_youtube_channels.py
```

### Lỗi: "The request cannot be completed because you have exceeded your quota"

**Nguyên nhân**: Đã dùng hết 10,000 units/day

**Giải pháp**:
1. Đợi đến 12:00 AM PST (reset quota)
2. Hoặc request tăng quota tại Google Cloud Console

### Lỗi: "invalid_client"

**Nguyên nhân**: File `credentials.json` không đúng

**Giải pháp**:
1. Download lại credentials.json từ Google Cloud Console
2. Đảm bảo file đúng tên và đúng vị trí

### Lỗi: "redirect_uri_mismatch"

**Nguyên nhân**: OAuth redirect URI không khớp

**Giải pháp**:
1. Vào Google Cloud Console > Credentials
2. Edit OAuth client
3. Thêm `http://localhost:8080/` vào Authorized redirect URIs

## 📚 Resources

- [YouTube Data API Docs](https://developers.google.com/youtube/v3)
- [OAuth 2.0 Guide](https://developers.google.com/identity/protocols/oauth2)
- [Python Quickstart](https://developers.google.com/youtube/v3/quickstart/python)

## ✅ Checklist

- [ ] Tạo Google Cloud Project
- [ ] Enable YouTube Data API v3
- [ ] Tạo OAuth consent screen
- [ ] Thêm scopes cần thiết
- [ ] Thêm test users
- [ ] Tạo OAuth credentials
- [ ] Download credentials.json
- [ ] Copy vào project folder
- [ ] Chạy xác thực lần đầu
- [ ] Test upload video

---

**Sau khi hoàn thành setup, quay lại chạy:**
```bash
python3 list_youtube_channels.py
python3 main.py
```
