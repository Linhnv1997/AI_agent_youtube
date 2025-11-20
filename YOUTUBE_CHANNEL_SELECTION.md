# 📺 Hướng dẫn Chọn Kênh YouTube

## 🎯 Tình huống

Bạn có **nhiều kênh YouTube** trên cùng một tài khoản Google và muốn chọn kênh cụ thể để upload video.

## 🔍 Cách 1: Tự động (Kênh mặc định)

**Mặc định:** Video sẽ upload lên **kênh chính** của tài khoản Google bạn đăng nhập.

Không cần config gì, để trống trong `config/settings.yaml`:

```yaml
youtube:
  channel_id: ""  # Để trống = kênh mặc định
```

## 🎛️ Cách 2: Chọn kênh cụ thể (Có nhiều kênh)

### Bước 1: Lấy danh sách kênh

Chạy script để xem tất cả kênh của bạn:

```bash
python3 list_youtube_channels.py
```

**Output mẫu:**
```
🔍 Đang tìm các kênh YouTube của bạn...
============================================================
✅ Tìm thấy 3 kênh:

📺 Kênh #1
   Tên: Kênh Chính Của Tôi
   Channel ID: UCxxxxxxxxxxxxxxxxxxx
   Subscribers: 1000
   Videos: 50
   URL: youtube.com/@channel-chinh

📺 Kênh #2
   Tên: Gaming Channel
   Channel ID: UCyyyyyyyyyyyyyyyyyy
   Subscribers: 500
   Videos: 20
   URL: youtube.com/@gaming-channel

📺 Kênh #3
   Tên: Tutorial Channel
   Channel ID: UCzzzzzzzzzzzzzzzzz
   Subscribers: 2000
   Videos: 100
   URL: youtube.com/@tutorial-channel
```

### Bước 2: Copy Channel ID

Chọn kênh bạn muốn upload và **copy Channel ID** (dòng `Channel ID: UCxxx...`)

### Bước 3: Cấu hình trong settings.yaml

Mở file `config/settings.yaml` và thêm Channel ID:

```yaml
youtube:
  channel_id: "UCzzzzzzzzzzzzzzzzz"  # Paste Channel ID của kênh bạn chọn
  default_category: "22"
  privacy_status: public
```

### Bước 4: Test

```bash
python3 test_description.py  # Test tạo mô tả
python3 main.py              # Upload thật
```

## 🔧 Cách 3: Lấy Channel ID thủ công

### Option A: Từ YouTube Studio

1. Truy cập: https://studio.youtube.com/
2. Click vào avatar → **Settings**
3. Tab **Channel** → **Advanced settings**
4. Copy **Channel ID**

### Option B: Từ URL kênh

1. Vào kênh YouTube của bạn
2. Xem URL, có 3 dạng:

**Dạng 1: Custom URL**
```
https://www.youtube.com/@your-channel-name
```
→ Cần chuyển sang Channel ID (dùng script hoặc YouTube Studio)

**Dạng 2: Channel ID trực tiếp**
```
https://www.youtube.com/channel/UCxxxxxxxxxxxxxxxxxxx
```
→ Copy phần `UCxxx...`

**Dạng 3: User ID (cũ)**
```
https://www.youtube.com/user/username
```
→ Cần chuyển sang Channel ID (dùng script)

### Option C: Dùng YouTube API Explorer

1. Truy cập: https://developers.google.com/youtube/v3/docs/channels/list
2. Trong "Try this API"
   - `part`: snippet
   - `mine`: true
3. Click **Execute**
4. Xem kết quả, tìm `"id": "UCxxx..."`

## 📝 Ví dụ cấu hình

### Ví dụ 1: Upload lên kênh Gaming

```yaml
youtube:
  channel_id: "UCgamingXXXXXXXXXXXXXXXX"
  default_category: "20"  # Gaming
  privacy_status: public
```

### Ví dụ 2: Upload lên kênh Tutorial (private)

```yaml
youtube:
  channel_id: "UCtutorialXXXXXXXXXXXXXX"
  default_category: "27"  # Education
  privacy_status: private  # Test trước khi public
```

### Ví dụ 3: Kênh mặc định

```yaml
youtube:
  channel_id: ""  # Để trống
  default_category: "22"
  privacy_status: public
```

## ⚠️ Lưu ý quan trọng

### 1. Quyền truy cập

Khi chạy lần đầu, YouTube sẽ hỏi quyền:
```
✓ View your YouTube account
✓ Manage your YouTube videos
✓ Upload videos
```

Phải accept tất cả để upload được.

### 2. Nhiều tài khoản Google

Nếu bạn có nhiều tài khoản Google:
- Mỗi tài khoản cần file `token.pickle` riêng
- Xóa `token.pickle` cũ để login tài khoản khác
- Hoặc dùng profile/environment khác nhau

### 3. Kênh Brand Account

Nếu kênh là **Brand Account** (managed channel):
- Script `list_youtube_channels.py` sẽ hiển thị tất cả
- Chọn Channel ID của Brand Account
- Đảm bảo tài khoản Google có quyền quản lý kênh đó

### 4. Channel ID vs User ID

- **Channel ID**: Bắt đầu bằng `UC`, dài 24 ký tự
  ```
  UCxxxxxxxxxxxxxxxxxxx (✅ Đúng)
  ```
- **User ID**: Là username cũ
  ```
  @channelname (❌ Không dùng được)
  ```

## 🐛 Troubleshooting

### Lỗi: "Channel not found"

**Nguyên nhân:** Channel ID sai

**Giải pháp:**
```bash
# List lại các kênh
python3 list_youtube_channels.py

# Kiểm tra Channel ID format
# Phải bắt đầu bằng UC và dài 24 ký tự
```

### Lỗi: "Insufficient permissions"

**Nguyên nhân:** Token không có quyền

**Giải pháp:**
```bash
# Xóa token cũ và login lại
rm token.pickle
python3 list_youtube_channels.py
# Cho phép tất cả quyền khi login
```

### Lỗi: "The user is not a channel owner"

**Nguyên nhân:** Tài khoản không phải owner của kênh

**Giải pháp:**
- Đảm bảo đăng nhập đúng tài khoản Google
- Kiểm tra quyền trong YouTube Studio
- Với Brand Account, cần là Manager hoặc Owner

### Video upload lên kênh sai

**Nguyên nhân:** 
- Channel ID không được set
- Hoặc token của tài khoản khác

**Giải pháp:**
```yaml
# Kiểm tra config/settings.yaml
youtube:
  channel_id: "UCxxx..."  # Phải có giá trị

# Xóa token và login lại
rm token.pickle
python3 main.py
```

## 💡 Tips

### 1. Test với kênh nhỏ trước

Nếu mới setup, test với:
- Kênh có ít subscribers
- Privacy = private
- Xóa video test sau khi thành công

### 2. Backup Channel ID

Lưu Channel ID vào note để không phải tra lại:
```
Gaming Channel: UCgamingXXXXXXXXXXXXXXXX
Tutorial Channel: UCtutorialXXXXXXXXXXXXXX
```

### 3. Multiple configs

Tạo nhiều file config cho mỗi kênh:
```bash
config/settings.gaming.yaml   # Cho kênh gaming
config/settings.tutorial.yaml # Cho kênh tutorial
```

Load theo environment:
```bash
export CHANNEL=gaming
python3 main.py
```

### 4. Scheduling theo kênh

Upload video khác nhau lên kênh khác nhau:
```yaml
# Gaming channel: Upload lúc 18:00
schedule:
  upload_time: "18:00"

# Tutorial channel: Upload lúc 09:00  
schedule:
  upload_time: "09:00"
```

## 📚 Tài liệu liên quan

- [YouTube Channel API](https://developers.google.com/youtube/v3/docs/channels)
- [Brand Accounts](https://support.google.com/youtube/answer/9367690)
- [YouTube Studio](https://studio.youtube.com/)

## 🎬 Quick Start

```bash
# 1. Xem các kênh của bạn
python3 list_youtube_channels.py

# 2. Chọn và copy Channel ID
# Channel ID: UCxxxxxxxxxxxxxxxxxxx

# 3. Thêm vào config
nano config/settings.yaml
# youtube:
#   channel_id: "UCxxxxxxxxxxxxxxxxxxx"

# 4. Test upload
python3 main.py
```

**Done! Video sẽ upload lên kênh bạn chọn! 🎉**
