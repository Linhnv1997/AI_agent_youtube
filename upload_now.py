"""
Upload 1 video ngay lập tức - Simple script
"""
import asyncio
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.workflows.upload_workflow import YouTubeUploadWorkflow
from src.utils.config import Settings
from loguru import logger


async def upload_now():
    """Upload video ngay"""
    try:
        logger.info("🚀 Starting immediate upload...")
        
        settings = Settings()
        workflow = YouTubeUploadWorkflow(settings)
        
        # Run upload
        result = await workflow.upload_daily_video()
        
        if result:
            logger.success("✅ Upload thành công!")
            logger.info(f"Video ID: {result.get('video_id', 'N/A')}")
        else:
            logger.error("❌ Upload thất bại!")
            
    except Exception as e:
        logger.error(f"❌ Lỗi: {e}")
        import traceback
        logger.error(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(upload_now())
