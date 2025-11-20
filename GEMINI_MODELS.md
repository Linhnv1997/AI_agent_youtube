# 🚀 Gemini Models - So sánh và Hướng dẫn

## 📊 Bảng so sánh các model Gemini miễn phí

| Model | Tốc độ | Chất lượng | Free Tier Limits | Khuyến nghị |
|-------|--------|------------|------------------|-------------|
| **gemini-2.0-flash-exp** | ⚡⚡⚡ Rất nhanh | ⭐⭐⭐⭐ Rất tốt | 10 RPM, 4M TPM | ✅ **Tốt nhất cho dự án** |
| gemini-1.5-flash | ⚡⚡⚡ Nhanh | ⭐⭐⭐ Tốt | 15 RPM, 1M TPM | ✅ Backup option |
| gemini-1.5-pro | ⚡⚡ Vừa | ⭐⭐⭐⭐⭐ Xuất sắc | 2 RPM, 32K TPM | 💡 Khi cần chất lượng cao |
| gemini-1.0-pro | ⚡ Chậm | ⭐⭐ Cũ | 60 RPM, 32K TPM | ⚠️ Deprecated |

**Chú thích:**
- **RPM**: Requests Per Minute (Số request mỗi phút)
- **TPM**: Tokens Per Minute (Số tokens mỗi phút)
- **4M TPM** = 4 triệu tokens/phút (rất nhiều!)

## ✅ Khuyến nghị cho dự án YouTube Auto Upload

### 🥇 Lựa chọn tốt nhất: `gemini-2.0-flash-exp`

**Tại sao?**
- ⚡ **Cực nhanh**: Tạo mô tả trong < 2 giây
- 🎯 **Chất lượng cao**: Output tốt, sáng tạo
- 💰 **Free tier hào phóng**: 4M tokens/phút (đủ cho hàng nghìn video)
- 🆕 **Công nghệ mới nhất**: Model thế hệ mới của Google

**Phù hợp với:**
- Upload video hàng ngày (1 video/ngày)
- Tạo mô tả dài 200-500 từ
- Không lo về quota

### 🥈 Lựa chọn dự phòng: `gemini-1.5-flash`

Nếu `2.0-flash-exp` có vấn đề (do experimental), dùng model này.

### 🥉 Khi nào dùng: `gemini-1.5-pro`

- Khi cần mô tả **CỰC KỲ** chất lượng cao
- Video quan trọng, ra mắt sản phẩm
- Không vội (2 requests/phút)

## 🔧 Cách đổi model

### Option 1: Chỉnh sửa file .env

```bash
nano .env
```

Đổi dòng:
```env
LLM_MODEL=gemini-2.0-flash-exp
```

### Option 2: Test nhanh trong code

Trong `test_description.py` hoặc `main.py`, bạn có thể override:

```python
agent = DescriptionAgent(
    provider="gemini",
    api_key=api_key,
    model="gemini-1.5-flash",  # Thử model khác
    temperature=0.7
)
```

## 📈 Chi phí và Giới hạn

### Free Tier (Không tốn tiền)

**gemini-2.0-flash-exp:**
- ✅ 10 requests/minute
- ✅ 4,000,000 tokens/minute
- ✅ 1,500 requests/day

**Với dự án của bạn:**
- Upload 1 video/ngày
- Mỗi mô tả ~500-1000 tokens
- **→ Hoàn toàn FREE mãi mãi! 🎉**

### Khi nào bị giới hạn?

Chỉ khi bạn:
- Upload > 10 video/phút (không khả thi)
- Hoặc > 1,500 video/ngày (không thực tế)

→ **Yên tâm sử dụng!**

## 🧪 Test các model

```bash
# Test với Gemini 2.0 Flash (mặc định)
python3 test_description.py

# Test với model khác (tạm thời)
# Chỉnh sửa .env hoặc code
```

## 🎨 Tùy chỉnh Temperature

Temperature ảnh hưởng đến độ sáng tạo:

```env
# Conservative (ít sáng tạo, chính xác)
LLM_TEMPERATURE=0.3

# Balanced (khuyến nghị)
LLM_TEMPERATURE=0.7

# Creative (sáng tạo, đa dạng)
LLM_TEMPERATURE=0.9
```

**Cho video YouTube:**
- `0.7` là tốt nhất (cân bằng)
- `0.9` nếu muốn mô tả độc đáo hơn

## 🔍 So sánh Output

### Ví dụ: Tên video "Hướng dẫn Python cho người mới"

**gemini-2.0-flash-exp:**
```
✅ Nhanh (1.5s)
✅ Mô tả chi tiết, có cấu trúc
✅ Emoji phù hợp
✅ SEO-friendly
```

**gemini-1.5-pro:**
```
✅ Chậm hơn (3-4s)
✅ Mô tả rất chi tiết, chuyên sâu
✅ Ngôn từ chuyên nghiệp hơn
⚠️  Có thể dài dòng
```

## 💡 Tips

1. **Bắt đầu với `gemini-2.0-flash-exp`** - Nhanh và tốt
2. **Monitor output** - Nếu không hài lòng, thử `1.5-pro`
3. **Không cần lo quota** - Free tier rất hào phóng
4. **Temperature 0.7** - Tối ưu cho mô tả video

## 📚 Tài liệu tham khảo

- [Gemini Models Overview](https://ai.google.dev/models/gemini)
- [Gemini API Pricing](https://ai.google.dev/pricing)
- [Rate Limits](https://ai.google.dev/docs/rate_limits)

## ✨ Kết luận

Cho dự án **AI Agent YouTube Auto Upload**:

```env
# RECOMMENDED SETUP
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.0-flash-exp
LLM_TEMPERATURE=0.7
GOOGLE_API_KEY=your_key_here
```

**= Tốc độ nhanh + Chất lượng cao + Hoàn toàn miễn phí! 🚀**
