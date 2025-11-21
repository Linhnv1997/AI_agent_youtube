# 📝 Hướng Dẫn Sử Dụng Custom Prompts

## 🎯 Tổng Quan

Dự án hỗ trợ **custom prompts** linh hoạt thông qua file `config/prompts.yaml`. Bạn có thể tùy chỉnh cách AI tạo mô tả video theo từng loại nội dung khác nhau.

## 📂 Cấu Trúc File prompts.yaml

```yaml
# Prompt mặc định cho mọi video
default_description_prompt: |
  Bạn là một chuyên gia viết mô tả video cho YouTube...

# Prompts tùy chỉnh theo loại nội dung
custom_prompts:
  tech_tutorial: |
    Tạo mô tả cho video hướng dẫn công nghệ...
    
  entertainment: |
    Tạo mô tả cho video giải trí...
    
  educational: |
    Tạo mô tả cho video giáo dục...

# Từ khóa SEO gợi ý
seo_keywords:
  - "học"
  - "hướng dẫn"
  - "tutorial"
```

## 🔧 Cách Sử Dụng

### 1️⃣ Chọn Prompt Type trong settings.yaml

Mở `config/settings.yaml` và tìm section `description`:

```yaml
description:
  min_length: 200
  max_length: 5000
  include_hashtags: true
  max_hashtags: 5
  include_call_to_action: true
  language: vi
  
  # Chọn loại prompt
  prompt_type: tech_tutorial  # Đổi thành: default, tech_tutorial, entertainment, educational
```

### 2️⃣ Các Prompt Type Có Sẵn

| Prompt Type | Mô Tả | Phù Hợp Với |
|------------|-------|-------------|
| `default` | Prompt chung cho mọi loại video | Video đa dạng chủ đề |
| `tech_tutorial` | Tối ưu cho video hướng dẫn công nghệ | Lập trình, DevOps, AI/ML |
| `entertainment` | Tập trung vào giải trí, hài hước | Vlog, Gaming, Comedy |
| `educational` | Nhấn mạnh giá trị giáo dục | Khóa học, Tutorial, Review |

### 3️⃣ Test Với Prompt Type Khác Nhau

```bash
# 1. Mở config/settings.yaml
# 2. Đổi prompt_type thành "tech_tutorial"
# 3. Chạy test

python3 test_description.py
```

## ✨ Tùy Chỉnh Prompt Riêng

### Bước 1: Thêm Custom Prompt

Mở `config/prompts.yaml` và thêm prompt mới:

```yaml
custom_prompts:
  # ... existing prompts ...
  
  product_review: |
    Tạo mô tả cho video review sản phẩm. Tập trung vào:
    - Đánh giá ưu/nhược điểm
    - So sánh với sản phẩm tương tự
    - Khuyến nghị cho người mua
    - Giá trị/chất lượng
```

### Bước 2: Sử Dụng Prompt Mới

Update `config/settings.yaml`:

```yaml
description:
  prompt_type: product_review  # Prompt mới của bạn
```

## 🎨 Ví Dụ Chi Tiết

### Tech Tutorial Prompt

**Khi nào dùng:** Video về Python, JavaScript, DevOps, AI...

**Output mẫu:**
```
📚 Hướng Dẫn Python Cho Người Mới Bắt Đầu

🎯 Trong video này bạn sẽ học:
✅ Cú pháp cơ bản Python
✅ Biến, vòng lặp, hàm
✅ Thực hành với 5 bài tập

⚙️ Yêu cầu tiên quyết:
- Không cần kinh nghiệm lập trình
- Đã cài Python 3.x

💡 Sau khóa học này, bạn có thể:
- Viết chương trình Python đơn giản
- Hiểu logic lập trình cơ bản
...
```

### Entertainment Prompt

**Khi nào dùng:** Vlog, gaming, challenge, comedy...

**Output mẫu:**
```
🎮 THÁCH THỨC 24H SỐNG TRONG MINECRAFT! 🔥

Hôm nay mình sẽ thử thách bản thân sống sót 24 giờ trong thế giới Minecraft với điều kiện SIÊU KHÓ! 😱

🎯 Các nhiệm vụ:
⚡ Xây nhà trong 1 giờ
🗡️ Đánh bại Ender Dragon
💎 Thu thập 64 kim cương

Liệu mình có hoàn thành được? Hãy xem ngay! 👇
...
```

### Educational Prompt

**Khi nào dùng:** Khóa học, giảng dạy, kiến thức chuyên môn...

**Output mẫu:**
```
📖 Hiểu Rõ Về Trí Tuệ Nhân Tạo (AI)

🎓 Đối tượng mục tiêu:
- Sinh viên công nghệ thông tin
- Người muốn chuyển sang AI/ML
- Chuyên gia muốn nâng cao kiến thức

📚 Nội dung bài học:
✅ AI là gì? Lịch sử phát triển
✅ Machine Learning vs Deep Learning
✅ Ứng dụng thực tế của AI

🏆 Kết quả học tập:
Sau video này, bạn sẽ hiểu được...
```

## 🔍 Tips & Best Practices

### ✅ Nên Làm

- Sử dụng prompt phù hợp với nội dung video
- Thường xuyên test và cải thiện prompt
- Thêm từ khóa SEO vào `seo_keywords`
- Giữ prompt ngắn gọn, rõ ràng

### ❌ Không Nên

- Dùng prompt quá dài (> 500 từ)
- Copy nguyên prompt từ nguồn khác
- Quên test sau khi thay đổi prompt
- Dùng prompt không phù hợp với video

## 📊 So Sánh Kết Quả

| Prompt Type | Độ Dài | Emoji | Call-to-Action | SEO Score |
|-------------|--------|-------|----------------|-----------|
| default | 200-500 từ | Trung bình | Có | ⭐⭐⭐ |
| tech_tutorial | 300-600 từ | Ít | Có | ⭐⭐⭐⭐ |
| entertainment | 150-400 từ | Nhiều | Mạnh | ⭐⭐⭐ |
| educational | 400-800 từ | Vừa phải | Có | ⭐⭐⭐⭐⭐ |

## 🚀 Workflow Thực Tế

### Scenario 1: Upload 1 Video Về Python

```bash
# 1. Set prompt type
echo "prompt_type: tech_tutorial" >> config/settings.yaml

# 2. Test trước
python3 test_description.py

# 3. Upload thật
python3 main.py
```

### Scenario 2: Upload Mix Content

```yaml
# Option 1: Dùng default prompt cho linh hoạt
description:
  prompt_type: default

# Option 2: Thay đổi prompt_type trước mỗi lần upload
# - Tech video → tech_tutorial
# - Vlog → entertainment
# - Course → educational
```

## 🛠️ Troubleshooting

### Lỗi: "Prompts config not found"

**Nguyên nhân:** File `config/prompts.yaml` không tồn tại

**Giải pháp:**
```bash
# Kiểm tra file
ls -la config/prompts.yaml

# Nếu không có, tạo từ template
cp config/prompts.yaml.example config/prompts.yaml
```

### Prompt không được apply

**Nguyên nhân:** Chưa set `prompt_type` trong settings.yaml

**Giải pháp:**
```yaml
description:
  prompt_type: tech_tutorial  # Thêm dòng này
```

### Output không đúng mong đợi

**Nguyên nhân:** Prompt chưa tối ưu

**Giải pháp:**
1. Xem log để hiểu AI đang dùng prompt nào
2. Điều chỉnh prompt trong `prompts.yaml`
3. Test lại với `python3 test_description.py`

## 📚 Tài Nguyên

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [YouTube SEO Best Practices](https://www.youtube.com/creators)
- [OpenAI Prompt Examples](https://platform.openai.com/examples)

## 💡 Next Steps

1. ✅ Đã tích hợp prompts.yaml vào code
2. 🎯 Test với các prompt types khác nhau
3. 📝 Tùy chỉnh prompts theo nhu cầu
4. 🚀 Upload video với prompt tối ưu!

---

**Cần trợ giúp?** Mở issue trên GitHub hoặc xem log trong `logs/app.log`
