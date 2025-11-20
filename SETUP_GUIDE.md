# 🚀 Hướng dẫn Setup và Test với Gemini LLM

## Bước 1: Cài đặt Dependencies

```bash
cd /home/linhnv1/project/AI_agent_youtube

# Tạo virtual environment (khuyến nghị)
python3 -m venv venv
source venv/bin/activate

# Hoặc cài trực tiếp
pip3 install -r requirements.txt
```

## Bước 2: Lấy Google Gemini API Key

1. Truy cập: https://makersuite.google.com/app/apikey
2. Click **"Get API Key"** hoặc **"Create API Key"**
3. Chọn project hoặc tạo mới
4. Copy API key

**Lưu ý:** Gemini API **MIỄN PHÍ** với giới hạn:
- 60 requests/minute
- 1,500 requests/day
- Rất đủ cho dự án này!

## Bước 3: Tạo file .env

```bash
# Copy từ file example
cp .env.example .env

# Chỉnh sửa file .env
nano .env
# Hoặc: vi .env
# Hoặc: code .env
```

### Nội dung file .env tối thiểu:

```env
# LLM Provider
LLM_PROVIDER=gemini

# Google Gemini API Key
GOOGLE_API_KEY=your_actual_api_key_here

# Video Configuration
VIDEO_FOLDER_PATH=./data/videos
UPLOAD_SCHEDULE_TIME=09:00

# LLM Configuration
LLM_MODEL=gemini-pro
LLM_TEMPERATURE=0.7
MAX_DESCRIPTION_LENGTH=5000

# YouTube API (để trống nếu chưa có, test description không cần)
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
```

## Bước 4: Thêm Video vào Folder (Optional cho test)

```bash
# Tạo hoặc copy video vào folder
cp /path/to/your/video.mp4 ./data/videos/

# Hoặc tạo file test (không cần video thật)
touch ./data/videos/"Hướng_dẫn_Python_cơ_bản.mp4"
touch ./data/videos/"Review_sản_phẩm_công_nghệ.mp4"
```

**Lưu ý:** Script test có thể chạy mà không cần video thật!

## Bước 5: Test Tạo Mô Tả Video

```bash
# Test tạo description với Gemini (không cần YouTube API)
python3 test_description.py
```

Script này sẽ:
- ✅ Kiểm tra connection với Gemini
- ✅ Tìm video trong folder (hoặc dùng tên video mẫu)
- ✅ Tạo mô tả, title, tags tự động
- ✅ Hiển thị kết quả

## Bước 6: Setup YouTube API (Khi sẵn sàng upload thật)

### 6.1. Tạo Google Cloud Project

1. Truy cập: https://console.cloud.google.com/
2. Tạo project mới hoặc chọn project có sẵn
3. Enable **YouTube Data API v3**:
   - Menu → APIs & Services → Library
   - Tìm "YouTube Data API v3"
   - Click "Enable"

### 6.2. Tạo OAuth 2.0 Credentials

1. Menu → APIs & Services → Credentials
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Chọn **"Desktop app"**
4. Đặt tên: "YouTube Auto Upload"
5. Download credentials JSON

### 6.3. Cấu hình Credentials

**Option A: Từ JSON file**
```bash
# Download credentials JSON và đổi tên
mv ~/Downloads/client_secret_xxx.json ./credentials.json
```

**Option B: Từ Client ID và Secret**

Thêm vào file `.env`:
```env
YOUTUBE_CLIENT_ID=your_client_id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your_client_secret
```

## Bước 7: Test Upload Thật

```bash
# Chạy ứng dụng chính
python3 main.py
```

Lần đầu chạy sẽ:
1. Mở browser để xác thực
2. Cho phép app truy cập YouTube
3. Lưu token để lần sau không cần xác thực lại

## 📋 Checklist

- [ ] Cài đặt dependencies: `pip3 install -r requirements.txt`
- [ ] Lấy Gemini API key từ https://makersuite.google.com/app/apikey
- [ ] Tạo file `.env` và thêm `GOOGLE_API_KEY`
- [ ] Test description: `python3 test_description.py`
- [ ] (Optional) Thêm video vào `./data/videos/`
- [ ] (Khi cần upload) Setup YouTube API credentials
- [ ] (Khi cần upload) Chạy app: `python3 main.py`

## 🎯 Quick Start Commands

```bash
# 1. Cài đặt
cd /home/linhnv1/project/AI_agent_youtube
pip3 install -r requirements.txt

# 2. Setup
cp .env.example .env
nano .env  # Thêm GOOGLE_API_KEY

# 3. Test
python3 test_description.py

# 4. Thêm video (optional)
cp your_video.mp4 ./data/videos/

# 5. Upload thật (khi ready)
python3 main.py
```

## ⚡ Script tự động setup

Tạo file `quick_setup.sh`:

```bash
#!/bin/bash

echo "🚀 AI Agent YouTube - Quick Setup"
echo "=================================="
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Installation failed!"
    exit 1
fi

echo "✅ Dependencies installed!"
echo ""

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env created!"
    echo ""
    echo "⚠️  QUAN TRỌNG: Hãy chỉnh sửa file .env và thêm GOOGLE_API_KEY"
    echo ""
    read -p "Nhập Google API Key (hoặc Enter để bỏ qua): " api_key
    
    if [ ! -z "$api_key" ]; then
        sed -i "s/GOOGLE_API_KEY=.*/GOOGLE_API_KEY=$api_key/" .env
        echo "✅ API key đã được thêm vào .env"
    fi
else
    echo "✅ .env already exists"
fi

echo ""
echo "🎉 Setup hoàn thành!"
echo ""
echo "📝 Bước tiếp theo:"
echo "   1. Kiểm tra file .env có GOOGLE_API_KEY"
echo "   2. Test: python3 test_description.py"
echo "   3. Thêm video: cp your_video.mp4 ./data/videos/"
echo "   4. Run: python3 main.py"
echo ""
```

## 🐛 Troubleshooting

### Lỗi: "Import could not be resolved"
```bash
# Cài lại dependencies
pip3 install -r requirements.txt --upgrade
```

### Lỗi: "API key not configured"
```bash
# Kiểm tra .env
cat .env | grep GOOGLE_API_KEY

# Phải có: GOOGLE_API_KEY=AIza...
```

### Lỗi: "No module named 'langchain_google_genai'"
```bash
# Cài package cụ thể
pip3 install langchain-google-genai
```

### Lỗi YouTube API
```bash
# Xóa token cũ và xác thực lại
rm token.pickle
python3 main.py
```

## 📚 Tài liệu

- Gemini API: https://ai.google.dev/docs
- YouTube API: https://developers.google.com/youtube/v3
- LangChain: https://python.langchain.com/docs/get_started/introduction
- LangGraph: https://langchain-ai.github.io/langgraph/

## 💡 Tips

1. **Test description trước** bằng `test_description.py` để không tốn quota YouTube
2. **Gemini miễn phí** nên dùng thoải mái để test
3. **YouTube quota** có hạn (10,000 units/day), mỗi upload tốn ~1,600 units
4. Dùng **privacy_status="private"** khi test để không public video
5. Backup file `.uploaded.json` để track video đã upload

## 🎨 Tùy chỉnh Prompt

Chỉnh sửa prompt trong `src/agents/description_agent.py`:

```python
def _create_prompt_template(self):
    template = """Tùy chỉnh prompt của bạn ở đây...
    
    Tên video: {video_name}
    ...
    """
```

Hoặc sử dụng prompts từ file `config/prompts.yaml`
