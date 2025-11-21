# ⚡ Quick Start Guide

## 🎯 Mục Tiêu
Upload video lên YouTube tự động mỗi ngày với mô tả được tạo bởi AI (Gemini).

## ✅ Đã Có Sẵn
- ✅ Code hoàn chỉnh
- ✅ Gemini API key đã cấu hình
- ✅ 2 video test trong folder
- ✅ Prompt TOEIC đã tùy chỉnh

## 🚀 3 Bước Setup

### Bước 1: Tạo YouTube OAuth Credentials (10 phút)

```bash
# Xem hướng dẫn chi tiết
cat YOUTUBE_OAUTH_SETUP.md
```

**Tóm tắt:**
1. Vào [Google Cloud Console](https://console.cloud.google.com/)
2. Tạo project mới
3. Enable "YouTube Data API v3"
4. Tạo OAuth credentials (Desktop app)
5. Download file → đổi tên thành `credentials.json`
6. Copy vào folder project này

### Bước 2: Xác Thực YouTube (2 phút)

```bash
# Chạy script xác thực
python3 list_youtube_channels.py

# Script sẽ:
# 1. Mở browser
# 2. Yêu cầu đăng nhập Google
# 3. Xin permission upload video
# 4. Lưu token để dùng lâu dài
```

### Bước 3: Upload Video (Chọn 1 trong 3)

#### Option A: Upload Ngay 1 Video (Test)
```bash
python3 test_schedule.py
# Chọn option 1
```

#### Option B: Test Schedule (2 phút/video)
```bash
python3 test_schedule.py
# Chọn option 2
# Sẽ upload 3 videos với 2 phút mỗi video
```

#### Option C: Production (09:00 Mỗi Ngày)
```bash
python3 test_schedule.py
# Chọn option 3
# Chạy nền, upload 1 video lúc 09:00 mỗi ngày
```

## 📹 Thêm Video Mới

```bash
# Copy video vào folder
cp your_video.mp4 data/videos/

# Video sẽ được upload tự động theo schedule
```

## 🎨 Tùy Chỉnh Prompt

File: `config/prompts.yaml`

```yaml
custom_prompts:
  toeic_part_youtube: |
    # Chỉnh sửa prompt ở đây
    # Sẽ ảnh hưởng đến tất cả video tiếp theo
```

## ⚙️ Tùy Chỉnh Settings

File: `config/settings.yaml`

```yaml
description:
  prompt_type: toeic_part_youtube  # Đổi prompt type

schedule:
  upload_time: "09:00"  # Đổi giờ upload

youtube:
  channel_id: "UCxxx"  # Đổi kênh upload
  default_category: "22"  # 22=People&Blogs, 27=Education
  default_privacy_status: "public"  # public/private/unlisted
```

## 🧪 Test Scripts

```bash
# Test mô tả video (không upload)
python3 test_description.py

# Test workflow đầy đủ (dry run)
python3 test_workflow.py

# Test schedule với menu
python3 test_schedule.py

# Xem thông tin Gemini models
python3 check_gemini_models.py
```

## 📊 Kiểm Tra Status

```bash
# Option 1: Qua test script
python3 test_schedule.py
# Chọn option 4 (xem thông tin)

# Option 2: Xem log
tail -f logs/app.log

# Option 3: Check uploaded videos
cat data/.uploaded.json
```

## 🔄 Chạy Nền (Production)

### Dùng tmux (Khuyến nghị)
```bash
# Tạo session
tmux new -s youtube_upload

# Chạy scheduler
python3 test_schedule.py
# Chọn option 3

# Detach: Ctrl+B, sau đó nhấn D
# Reattach: tmux attach -t youtube_upload
```

### Dùng nohup
```bash
nohup python3 -c "
from test_schedule import ScheduleManager
m = ScheduleManager()
m.schedule_daily_upload()
m.run_schedule_loop()
" > logs/scheduler.log 2>&1 &

# Check process
ps aux | grep test_schedule

# Stop: kill <PID>
```

### Dùng systemd service
```bash
# Tạo service file
sudo nano /etc/systemd/system/youtube-upload.service

# Nội dung:
[Unit]
Description=YouTube Auto Upload Service
After=network.target

[Service]
Type=simple
User=linhnv1
WorkingDirectory=/home/linhnv1/project/AI_agent_youtube
ExecStart=/usr/bin/python3 -c "from test_schedule import ScheduleManager; m = ScheduleManager(); m.schedule_daily_upload(); m.run_schedule_loop()"
Restart=always

[Install]
WantedBy=multi-user.target

# Enable và start
sudo systemctl enable youtube-upload
sudo systemctl start youtube-upload
sudo systemctl status youtube-upload
```

## ⚠️ Lưu Ý Quan Trọng

### Quota Limits
- **Default**: 10,000 units/day
- **1 upload**: ~1,600 units
- **Max uploads**: ~6 videos/day

### Bảo Mật
⚠️ **KHÔNG** commit các file:
- `credentials.json` - OAuth credentials
- `token.pickle` - Access token
- `.env` - API keys

### Video Requirements
- **Max size**: 5GB
- **Formats**: mp4, avi, mov, mkv, flv, wmv
- **Title**: Max 100 characters
- **Description**: Max 5,000 characters

## 🐛 Troubleshooting

### Lỗi: "credentials.json not found"
```bash
# Làm theo YOUTUBE_OAUTH_SETUP.md
cat YOUTUBE_OAUTH_SETUP.md
```

### Lỗi: "insufficient authentication scopes"
```bash
# Xóa token cũ và xác thực lại
rm token.pickle
python3 list_youtube_channels.py
```

### Lỗi: "quota exceeded"
```bash
# Đợi đến 12:00 AM PST (quota reset)
# Hoặc request tăng quota tại Google Cloud Console
```

### Video không upload
```bash
# Check log
tail -n 50 logs/app.log

# Test workflow
python3 test_workflow.py

# Verify credentials
python3 list_youtube_channels.py
```

## 📚 Full Documentation

- `README.md` - Overview
- `SETUP_GUIDE.md` - Chi tiết setup
- `YOUTUBE_OAUTH_SETUP.md` - YouTube API setup
- `PROMPTS_GUIDE.md` - Custom prompts
- `PROJECT_SUMMARY.md` - Tổng hợp dự án

## 🎉 Done!

Sau khi hoàn thành 3 bước trên, hệ thống sẽ tự động:
1. ✅ Upload 1 video mỗi ngày lúc 09:00
2. ✅ Tạo mô tả bằng Gemini AI
3. ✅ Đăng lên YouTube kênh của bạn
4. ✅ Track video đã upload
5. ✅ Tiếp tục với video tiếp theo ngày hôm sau

---

**Happy uploading! 🚀**
