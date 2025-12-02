"""
Test cleaning instruction text from description
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.description_agent import DescriptionAgent

# Sample text with instruction
sample_text = """BƯỚC 1 - Tạo TIÊU ĐỀ (dòng đầu tiên):

BƯỚC 2 - Tạo MÔ TẢ CHI TIẾT theo template ví dụ về Banking:

Bạn đang ôn luyện TOEIC và muốn cải thiện khả năng nghe? Đây chính là video dành cho bạn!

📚 Nội dung video:

Bài nghe được thiết kế với phương pháp đặc biệt:
1️⃣ Lần đầu tiên: Nghe đoạn hội thoại không có phụ đề.
2️⃣ Lần thứ hai: Nghe lại với phụ đề tiếng Việt.
3️⃣ Lần cuối cùng: Nghe lại với phụ đề tiếng Anh.

#TOEIC #TiengAnh #LuyenNghe"""

# Create agent instance (just for the cleaning method)
agent = DescriptionAgent(
    provider="gemini",
    api_key="test",
    model="gemini-2.5-flash"
)

# Test cleaning
cleaned = agent._clean_instruction_text(sample_text)

print("=== BEFORE ===")
print(sample_text)
print("\n=== AFTER ===")
print(cleaned)
print("\n✅ Instructions removed!")
