"""
Test upload workflow WITHOUT actually uploading to YouTube
Dùng để test logic workflow trước khi có OAuth credentials
"""
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.agents.description_agent import DescriptionAgent
from src.utils.config import Settings
from src.utils.file_manager import VideoFileManager
from loguru import logger


async def test_upload_workflow():
    """Test complete workflow (without YouTube upload)"""
    try:
        settings = Settings()
        
        logger.info("🤖 Testing Upload Workflow (Dry Run)")
        logger.info("=" * 60)
        
        # Step 1: Select video
        logger.info("\n📹 STEP 1: Selecting video...")
        file_manager = VideoFileManager(settings.VIDEO_FOLDER_PATH)
        video = file_manager.get_next_video()
        
        if not video:
            logger.warning("❌ Không tìm thấy video trong folder!")
            logger.info(f"Hãy thêm video vào: {settings.VIDEO_FOLDER_PATH}")
            return
        
        logger.success(f"✅ Selected: {video.name}")
        logger.info(f"   Path: {video}")
        logger.info(f"   Size: {video.stat().st_size / 1024 / 1024:.2f} MB")
        
        # Step 2: Generate description
        logger.info("\n✍️ STEP 2: Generating description...")
        
        agent = DescriptionAgent(
            provider=settings.LLM_PROVIDER,
            api_key=(settings.GOOGLE_API_KEY if settings.LLM_PROVIDER == "gemini" 
                    else settings.OPENAI_API_KEY),
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        
        prompt_type = settings.DESCRIPTION_PROMPT_TYPE
        logger.info(f"   Using prompt: {prompt_type}")
        
        result = await agent.generate_description(
            video_path=video,
            additional_context="",
            prompt_type=prompt_type
        )
        
        logger.success("✅ Description generated!")
        logger.info(f"\n📌 Title: {result['title']}")
        logger.info(f"\n📝 Description (first 500 chars):\n{result['description'][:500]}...")
        logger.info(f"\n🏷️  Tags: {', '.join(result['tags'][:5])}...")
        
        # Step 3: Simulate upload
        logger.info("\n📤 STEP 3: Uploading to YouTube...")
        logger.warning("⚠️  DRY RUN - Không upload thật (chưa có credentials.json)")
        
        upload_config = {
            "title": result['title'],
            "description": result['description'],
            "tags": result['tags'],
            "category_id": settings.YOUTUBE_CATEGORY,
            "privacy_status": settings.YOUTUBE_PRIVACY_STATUS,
            "channel_id": settings.YOUTUBE_CHANNEL_ID or "default"
        }
        
        logger.info("   Upload config:")
        logger.info(f"   - Category: {upload_config['category_id']}")
        logger.info(f"   - Privacy: {upload_config['privacy_status']}")
        logger.info(f"   - Channel: {upload_config['channel_id']}")
        
        # Step 4: Mark as uploaded (commented out for dry run)
        logger.info("\n✅ STEP 4: Marking as uploaded...")
        logger.warning("⚠️  DRY RUN - Không đánh dấu uploaded (test only)")
        # file_manager.mark_as_uploaded(video)
        
        # Summary
        logger.info("\n" + "=" * 60)
        logger.success("🎉 WORKFLOW TEST HOÀN THÀNH!")
        logger.info("=" * 60)
        
        logger.info("\n📊 Summary:")
        logger.info(f"   Video: {video.name}")
        logger.info(f"   Title length: {len(result['title'])} chars")
        logger.info(f"   Description length: {len(result['description'])} chars")
        logger.info(f"   Tags count: {len(result['tags'])}")
        logger.info(f"   Pending videos: {file_manager.get_pending_videos_count()}")
        
        logger.info("\n🚀 Next Steps:")
        logger.info("   1. Tạo credentials.json theo hướng dẫn trong YOUTUBE_OAUTH_SETUP.md")
        logger.info("   2. Chạy: python3 list_youtube_channels.py (để xác thực)")
        logger.info("   3. Chạy: python3 main.py (upload thật)")
        
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise


if __name__ == "__main__":
    asyncio.run(test_upload_workflow())
