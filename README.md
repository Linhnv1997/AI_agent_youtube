# AI Agent YouTube Auto Upload

Dự án AI Agent tự động đăng video lên YouTube mỗi ngày với mô tả được tạo bởi LLM.

## Tính năng

- 🤖 Sử dụng LangGraph để xây dựng workflow AI agent
- 📝 Tự động tạo mô tả video bằng LLM (hỗ trợ OpenAI + Google Gemini)
- 🎨 **Custom Prompts** - Tùy chỉnh prompts theo loại video (tech, entertainment, educational)
- 📅 Lên lịch đăng video hàng ngày
- 🎥 Quản lý hàng đợi video từ folder
- 📺 Chọn kênh YouTube cụ thể để upload
- 📊 Logging và tracking chi tiết

## Cấu trúc dự án

```
AI_agent_youtube/
├── src/
│   ├── agents/          # Các AI agents
│   ├── tools/           # Công cụ cho agents (YouTube API, file handling)
│   ├── utils/           # Các hàm tiện ích
│   └── workflows/       # LangGraph workflows
├── config/              # Configuration files
├── data/                # Dữ liệu và video folder
├── logs/                # Log files
├── tests/               # Unit tests
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── main.py              # Entry point
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Cấu hình

1. Tạo file `.env` và thêm các biến môi trường:
```
OPENAI_API_KEY=your_openai_key
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
VIDEO_FOLDER_PATH=path_to_your_videos
```

2. Cấu hình YouTube API credentials

## Sử dụng

### 🚀 Quick Start

```bash
# Test LLM description generation
python3 test_description.py

# Xác thực YouTube (chỉ lần đầu)
python3 list_youtube_channels.py

# Chạy upload workflow
python3 main.py
```

### 📝 Custom Prompts

Tùy chỉnh cách AI tạo mô tả video trong `config/settings.yaml`:

```yaml
description:
  prompt_type: tech_tutorial  # default, tech_tutorial, entertainment, educational
```

Xem chi tiết: [PROMPTS_GUIDE.md](./PROMPTS_GUIDE.md)

### 🎯 Chọn Kênh YouTube

Nếu bạn quản lý nhiều kênh YouTube:

```yaml
youtube:
  channel_id: "UCxxxxxxxxx"  # Để trống = kênh mặc định
```

Chi tiết: [YOUTUBE_CHANNEL_SELECTION.md](./YOUTUBE_CHANNEL_SELECTION.md)

## 📚 Documentation

- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Hướng dẫn cài đặt chi tiết
- [PROMPTS_GUIDE.md](./PROMPTS_GUIDE.md) - Hướng dẫn tùy chỉnh prompts
- [GEMINI_MODELS.md](./GEMINI_MODELS.md) - Danh sách Gemini models
- [CONFIG_STRUCTURE.md](./CONFIG_STRUCTURE.md) - Cấu trúc config files

## License

MIT
