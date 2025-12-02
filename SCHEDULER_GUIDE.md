# 🚀 Quick Guide - Chạy Schedule Hàng Ngày

## ✅ Đã Setup

- ⏰ **Upload time**: 17:10 (5:10 PM) mỗi ngày
- 🌍 **Timezone**: Asia/Ho_Chi_Minh
- 📹 **Auto thumbnail**: Enabled
- 📺 **Channel**: Song Ngữ Việt Anh

## 📋 Commands

### Start Scheduler
```bash
./start_scheduler.sh
```

### Xem Logs (Attach vào tmux)
```bash
tmux attach -t youtube_upload
```

**Detach (không stop):** Nhấn `Ctrl+B`, sau đó nhấn `D`

### Stop Scheduler
```bash
./stop_scheduler.sh
```

### Kiểm tra Status
```bash
tmux list-sessions
```

## 🎯 Workflow Tự Động

Mỗi ngày lúc **17:10**, hệ thống sẽ:

1. ✅ Chọn 1 video từ `data/videos/`
2. ✅ Tạo mô tả bằng Gemini AI (prompt TOEIC)
3. ✅ Tạo thumbnail tự động với title
4. ✅ Upload video lên YouTube
5. ✅ Upload thumbnail
6. ✅ Đánh dấu video đã upload
7. ⏰ Chờ đến 17:10 ngày hôm sau

## 📁 Thêm Video Mới

```bash
# Copy video vào folder
cp your_new_video.mp4 data/videos/

# Video sẽ được upload tự động ngày hôm sau lúc 17:10
```

## 🔧 Thay Đổi Settings

### Đổi giờ upload
Sửa file `config/settings.yaml`:
```yaml
schedule:
  upload_time: "17:10"  # HH:MM format (24-hour)
```

Sau đó restart scheduler:
```bash
./stop_scheduler.sh
./start_scheduler.sh
```

### Enable/Disable Thumbnail
```yaml
features:
  generate_thumbnail: true  # true/false
```

### Đổi prompt type
```yaml
description:
  prompt_type: toeic_part_youtube  # hoặc: default, tech_tutorial, entertainment
```

## 📊 Monitoring

### Xem log file
```bash
tail -f logs/app.log
```

### Check videos đã upload
```bash
cat data/videos/.uploaded.json
```

### Check pending videos
```bash
ls -la data/videos/*.mp4
```

## 🐛 Troubleshooting

### Scheduler không chạy?
```bash
# Check session
tmux list-sessions

# Nếu không có, start lại
./start_scheduler.sh
```

### Upload thất bại?
```bash
# Xem logs
tmux attach -t youtube_upload

# Hoặc
tail -50 logs/app.log
```

### Token expired?
```bash
# Xóa token và xác thực lại
rm token.pickle
python3 list_youtube_channels.py
```

## 🎊 Done!

Scheduler đang chạy trong background với tmux. 
Hệ thống sẽ tự động upload video mỗi ngày lúc 17:10!

---

**📺 Channels uploaded**: Song Ngữ Việt Anh
**🔗 Channel URL**: https://www.youtube.com/@song-ngu-viet-anh
