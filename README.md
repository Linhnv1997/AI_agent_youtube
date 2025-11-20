# AI Agent YouTube Auto Upload

Dự án AI Agent tự động đăng video lên YouTube mỗi ngày với mô tả được tạo bởi LLM.

## Tính năng

- 🤖 Sử dụng LangGraph để xây dựng workflow AI agent
- 📝 Tự động tạo mô tả video bằng LLM dựa trên tên file
- 📅 Lên lịch đăng video hàng ngày
- 🎥 Quản lý hàng đợi video từ folder
- 📊 Logging và tracking

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

```bash
python main.py
```

## License

MIT
