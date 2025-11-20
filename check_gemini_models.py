"""
Script để kiểm tra Gemini API và list các models có sẵn
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ GOOGLE_API_KEY không được cấu hình trong file .env")
    exit(1)

print(f"🔑 API Key: {api_key[:20]}...")
print()

try:
    # Configure API
    genai.configure(api_key=api_key)
    
    print("✅ Gemini API connected successfully!")
    print()
    print("📋 Danh sách models có sẵn:")
    print("=" * 60)
    
    # List models
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"\n✓ {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description[:100]}...")
            print(f"  Input token limit: {model.input_token_limit}")
            print(f"  Output token limit: {model.output_token_limit}")
    
    print()
    print("=" * 60)
    print("\n💡 Sử dụng model name trong config:")
    print("   Ví dụ: models/gemini-pro → dùng 'gemini-pro'")
    print("   Ví dụ: models/gemini-1.5-pro-latest → dùng 'gemini-1.5-pro-latest'")
    
except Exception as e:
    print(f"❌ Lỗi kết nối Gemini API: {e}")
    print()
    print("🔍 Kiểm tra:")
    print("   1. API key có đúng không?")
    print("   2. API key đã được enable Gemini API?")
    print("   3. Truy cập: https://makersuite.google.com/app/apikey")
