"""
Test script để thử nghiệm tạo mô tả video với Gemini
Không cần YouTube API
"""
import asyncio
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.description_agent import DescriptionAgent
from src.utils.config import Settings
from src.utils.file_manager import VideoFileManager
from loguru import logger

async def test_description_generation():
    """Test tạo mô tả video"""
    try:
        # Load settings
        settings = Settings()
        
        logger.info("🤖 Testing Video Description Generation")
        logger.info("=" * 60)
        logger.info(f"LLM Provider: {settings.LLM_PROVIDER}")
        logger.info(f"LLM Model: {settings.LLM_MODEL}")
        logger.info("=" * 60)
        
        # Check API key
        api_key = (settings.GOOGLE_API_KEY if settings.LLM_PROVIDER == "gemini" 
                   else settings.OPENAI_API_KEY)
        
        if not api_key:
            logger.error("❌ API key không được cấu hình!")
            logger.info("Hãy tạo file .env từ .env.example và thêm API key")
            return
        
        # Initialize agent
        agent = DescriptionAgent(
            provider=settings.LLM_PROVIDER,
            api_key=api_key,
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        
        # Check for videos
        file_manager = VideoFileManager(settings.VIDEO_FOLDER_PATH)
        video = file_manager.get_next_video()
        
        if not video:
            logger.warning("⚠️ Không tìm thấy video trong folder!")
            logger.info(f"Hãy thêm video vào: {settings.VIDEO_FOLDER_PATH}")
            
            # Test với video giả định
            logger.info(f"\n📝 Testing với tên video mẫu (prompt: {settings.DESCRIPTION_PROMPT_TYPE})...")
            test_video = Path("Shopping_Mall.mp4")  # TOEIC topic example
            
            result = await agent.generate_description(
                video_path=test_video,
                additional_context="",
                prompt_type=settings.DESCRIPTION_PROMPT_TYPE
            )
            
            logger.success("\n✅ Kết quả test:")
            logger.info(f"\n📌 Title: {result['title']}")
            logger.info(f"\n📝 Description:\n{result['description']}")
            logger.info(f"\n🏷️  Tags: {', '.join(result['tags'])}")
            
        else:
            logger.info(f"📹 Tìm thấy video: {video.name}")
            logger.info(f"� Prompt type: {settings.DESCRIPTION_PROMPT_TYPE}")
            logger.info("🔄 Đang tạo mô tả...")
            
            result = await agent.generate_description(
                video_path=video,
                additional_context="",
                prompt_type=settings.DESCRIPTION_PROMPT_TYPE
            )
            
            logger.success("\n✅ Tạo mô tả thành công!")
            logger.info(f"\n📌 Title: {result['title']}")
            logger.info(f"\n📝 Description:\n{result['description']}")
            logger.info(f"\n🏷️  Tags: {', '.join(result['tags'])}")
            
            # Show stats
            pending = file_manager.get_pending_videos_count()
            logger.info(f"\n📊 Số video còn lại: {pending}")
        
        logger.success("\n🎉 Test hoàn thành!")
        
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(test_description_generation())
