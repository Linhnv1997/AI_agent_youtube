# 📁 Cấu trúc Configuration

## 🎯 Triết lý

Dự án này tách biệt **credentials** (thông tin nhạy cảm) và **configuration** (cấu hình ứng dụng):

```
├── .env                    # ❗ Credentials (KHÔNG commit)
├── config/settings.yaml    # ⚙️  Configuration (commit được)
└── config/prompts.yaml     # 📝 Prompt templates
```

## 🔐 File `.env` - Chỉ chứa Credentials

**Mục đích:** Lưu trữ API keys và secrets

**Nội dung:**
```env
# API Keys
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...

# YouTube OAuth
YOUTUBE_CLIENT_ID=xxx.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=GOCSPX-...
```

**Đặc điểm:**
- ✅ Được liệt kê trong `.gitignore` (không push lên Git)
- ✅ Mỗi môi trường có file riêng (dev, staging, prod)
- ✅ Copy từ `.env.example` khi setup

## ⚙️ File `config/settings.yaml` - Application Configuration

**Mục đích:** Cấu hình ứng dụng, có thể commit lên Git

**Nội dung:**
```yaml
llm:
  provider: gemini
  model: gemini-2.0-flash-exp
  temperature: 0.7

video:
  folder_path: ./data/videos
  supported_formats: [mp4, avi, mov]

schedule:
  upload_time: "09:00"
  timezone: "Asia/Ho_Chi_Minh"

youtube:
  default_category: "22"
  privacy_status: public
```

**Đặc điểm:**
- ✅ Commit được lên Git
- ✅ Dễ đọc, dễ chỉnh sửa
- ✅ Có thể override bằng environment variables
- ✅ Hỗ trợ nhiều môi trường (dev, prod)

## 📝 File `config/prompts.yaml` - Prompt Templates

**Mục đích:** Quản lý các prompt template cho LLM

```yaml
default_description_prompt: |
  Bạn là chuyên gia viết mô tả YouTube...

custom_prompts:
  tech_tutorial: |
    Tạo mô tả cho video công nghệ...
```

## 🔄 Cách sử dụng trong Code

### 1. Load Settings

```python
from src.utils.config import Settings

settings = Settings()
```

### 2. Truy cập Credentials (.env)

```python
# API Keys
api_key = settings.GOOGLE_API_KEY
openai_key = settings.OPENAI_API_KEY

# YouTube OAuth
client_id = settings.YOUTUBE_CLIENT_ID
client_secret = settings.YOUTUBE_CLIENT_SECRET
```

### 3. Truy cập Configuration (settings.yaml)

```python
# LLM config
provider = settings.LLM_PROVIDER          # "gemini"
model = settings.LLM_MODEL                # "gemini-2.0-flash-exp"
temp = settings.LLM_TEMPERATURE           # 0.7

# Video config
video_folder = settings.VIDEO_FOLDER_PATH # Path("./data/videos")
formats = settings.SUPPORTED_VIDEO_FORMATS # ['mp4', 'avi', 'mov']

# Schedule
upload_time = settings.UPLOAD_SCHEDULE_TIME # "09:00"
timezone = settings.TIMEZONE              # "Asia/Ho_Chi_Minh"

# YouTube
category = settings.YOUTUBE_CATEGORY      # "22"
privacy = settings.YOUTUBE_PRIVACY_STATUS # "public"

# Logging
log_level = settings.LOG_LEVEL            # "INFO"
log_file = settings.LOG_FILE              # Path("./logs/app.log")
```

### 4. Truy cập Config bất kỳ

```python
# Nested keys
value = settings.get_config('llm.model')
value = settings.get_config('youtube.privacy_status', default='public')
```

## 📂 Cấu trúc thư mục

```
AI_agent_youtube/
├── .env                          # ❗ Credentials (git-ignored)
├── .env.example                  # Template cho .env
├── config/
│   ├── settings.yaml            # ⚙️  App configuration
│   └── prompts.yaml             # 📝 Prompt templates
└── src/
    └── utils/
        └── config.py            # Configuration loader
```

## 🔧 Customization

### Thay đổi LLM Model

**Option 1: Chỉnh `config/settings.yaml`** (khuyến nghị)
```yaml
llm:
  model: gemini-1.5-pro  # Đổi model
  temperature: 0.9       # Tăng sáng tạo
```

**Option 2: Override trong code**
```python
settings._config['llm']['model'] = 'gemini-1.5-pro'
```

### Thay đổi Upload Schedule

```yaml
schedule:
  upload_time: "18:00"  # Upload lúc 6 giờ chiều
  timezone: "Asia/Bangkok"
```

### Thay đổi Privacy Status

```yaml
youtube:
  privacy_status: private  # hoặc: public, unlisted
  default_category: "28"   # Science & Technology
```

## 🌍 Multiple Environments

### Development
```yaml
# config/settings.yaml
youtube:
  privacy_status: private  # Test với private

logging:
  level: DEBUG
```

### Production
```yaml
# config/settings.production.yaml
youtube:
  privacy_status: public

logging:
  level: INFO
```

Load theo environment:
```python
import os
env = os.getenv('APP_ENV', 'development')
config_file = f'config/settings.{env}.yaml'
```

## ✅ Best Practices

### 1. Credentials (.env)
- ❌ KHÔNG commit lên Git
- ✅ Dùng `.env.example` làm template
- ✅ Mỗi developer có file riêng
- ✅ Rotate keys định kỳ

### 2. Configuration (settings.yaml)
- ✅ Commit lên Git
- ✅ Document mỗi option
- ✅ Sử dụng defaults hợp lý
- ✅ Validate khi load

### 3. Separation of Concerns
```
.env              → Secrets (API keys, passwords)
settings.yaml     → Config (paths, options, flags)
prompts.yaml      → Templates (prompts, messages)
```

## 📚 Tài liệu liên quan

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Hướng dẫn setup
- [GEMINI_MODELS.md](GEMINI_MODELS.md) - Các model Gemini
- [GIT_SETUP.md](GIT_SETUP.md) - Setup Git repo

## 🔍 Troubleshooting

### Lỗi: "API key not configured"
```bash
# Kiểm tra .env
cat .env | grep GOOGLE_API_KEY

# Phải có giá trị
GOOGLE_API_KEY=AIza...
```

### Lỗi: "Config file not found"
```bash
# Kiểm tra settings.yaml tồn tại
ls config/settings.yaml

# Tạo nếu chưa có
cp config/settings.example.yaml config/settings.yaml
```

### Lỗi: "Invalid YAML syntax"
```bash
# Validate YAML
python3 -c "import yaml; yaml.safe_load(open('config/settings.yaml'))"
```

## 💡 Tips

1. **Dùng settings.yaml cho config thường xuyên thay đổi**
   - Model name, temperature
   - Upload time, timezone
   - Privacy status

2. **Dùng .env cho credentials**
   - API keys
   - OAuth secrets

3. **Version control settings.yaml**
   - Commit lên Git để team dùng chung
   - Document mỗi thay đổi

4. **Keep .env private**
   - Không share qua chat, email
   - Dùng secret management tools cho production
