#!/bin/bash

echo "🎯 AI Agent YouTube - Quick Setup với Gemini"
echo "=============================================="
echo ""
echo "✅ Dependencies đã được cài đặt!"
echo "✅ File .env đã được tạo!"
echo ""
echo "📝 BƯỚC TIẾP THEO:"
echo ""
echo "1️⃣  LẤY GEMINI API KEY (MIỄN PHÍ)"
echo "   🔗 Truy cập: https://makersuite.google.com/app/apikey"
echo "   📋 Click 'Get API Key' hoặc 'Create API Key'"
echo "   📄 Copy API key"
echo ""
echo "2️⃣  THÊM API KEY VÀO FILE .ENV"
echo "   Chỉnh sửa file .env:"
read -p "   Bạn có muốn nhập API key ngay bây giờ? (y/n): " input

if [ "$input" = "y" ] || [ "$input" = "Y" ]; then
    echo ""
    read -p "   Nhập Google Gemini API key: " api_key
    
    if [ ! -z "$api_key" ]; then
        sed -i "s/GOOGLE_API_KEY=.*/GOOGLE_API_KEY=$api_key/" .env
        echo "   ✅ API key đã được lưu vào .env"
        echo ""
        echo "3️⃣  TEST THỬ NGAY"
        echo "   🧪 Chạy: python3 test_description.py"
        echo ""
        read -p "   Chạy test ngay? (y/n): " run_test
        
        if [ "$run_test" = "y" ] || [ "$run_test" = "Y" ]; then
            echo ""
            echo "🚀 Đang chạy test..."
            echo "===================="
            python3 test_description.py
        else
            echo ""
            echo "   Chạy test sau bằng: python3 test_description.py"
        fi
    else
        echo "   ⚠️  Không nhập API key. Hãy chỉnh sửa .env thủ công:"
        echo "   nano .env"
    fi
else
    echo ""
    echo "   Chỉnh sửa file .env:"
    echo "   $ nano .env"
    echo "   hoặc"
    echo "   $ code .env"
    echo ""
    echo "   Thay đổi dòng:"
    echo "   GOOGLE_API_KEY=your_google_api_key_here"
    echo "   thành:"
    echo "   GOOGLE_API_KEY=<your_actual_api_key>"
fi

echo ""
echo "4️⃣  (OPTIONAL) THÊM VIDEO VÀO FOLDER"
echo "   $ cp your_video.mp4 ./data/videos/"
echo ""
echo "5️⃣  TEST TẠO MÔ TẢ VIDEO"
echo "   $ python3 test_description.py"
echo ""
echo "6️⃣  KHI READY UPLOAD LÊN YOUTUBE"
echo "   - Setup YouTube API (xem SETUP_GUIDE.md)"
echo "   - Chạy: python3 main.py"
echo ""
echo "📚 Xem hướng dẫn chi tiết: SETUP_GUIDE.md"
echo ""
