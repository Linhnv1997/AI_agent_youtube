"""
Test scheduling system - Upload videos theo lịch
"""
import asyncio
import schedule
import time
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from src.workflows.upload_workflow import YouTubeUploadWorkflow
from src.utils.config import Settings
from src.utils.file_manager import VideoFileManager
from loguru import logger


class ScheduleManager:
    """Quản lý lịch trình upload video"""
    
    def __init__(self):
        self.settings = Settings()
        self.file_manager = VideoFileManager(self.settings.VIDEO_FOLDER_PATH)
        
    async def run_upload_job(self):
        """Job upload 1 video"""
        try:
            logger.info("🚀 Starting scheduled upload job...")
            logger.info(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check for pending videos
            pending_count = self.file_manager.get_pending_videos_count()
            logger.info(f"📊 Pending videos: {pending_count}")
            
            if pending_count == 0:
                logger.warning("⚠️ Không còn video để upload!")
                logger.info("💡 Hãy thêm video mới vào folder: data/videos/")
                return
            
            # Initialize workflow
            workflow = YouTubeUploadWorkflow(self.settings)
            
            # Run workflow
            result = await workflow.run()
            
            if result.get("status") == "uploaded":
                logger.success("✅ Upload thành công!")
                logger.info(f"📹 Video: {result.get('video_path')}")
                logger.info(f"📌 Title: {result.get('title')}")
                logger.info(f"🔗 Video ID: {result.get('video_id', 'N/A')}")
                logger.info(f"📊 Videos còn lại: {pending_count - 1}")
            else:
                logger.error(f"❌ Upload thất bại: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"❌ Lỗi khi chạy upload job: {e}")
            import traceback
            logger.error(traceback.format_exc())
    
    def schedule_daily_upload(self):
        """Setup lịch upload hàng ngày"""
        upload_time = self.settings.UPLOAD_SCHEDULE_TIME
        
        logger.info("📅 Setting up daily upload schedule...")
        logger.info(f"⏰ Upload time: {upload_time} ({self.settings.TIMEZONE})")
        logger.info("=" * 60)
        
        # Schedule job
        schedule.every().day.at(upload_time).do(
            lambda: asyncio.run(self.run_upload_job())
        )
        
        logger.success(f"✅ Scheduled daily upload at {upload_time}")
        
        # Show next run time
        next_run = schedule.next_run()
        if next_run:
            logger.info(f"🕐 Next upload: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return schedule
    
    def run_schedule_loop(self):
        """Chạy schedule loop (blocking)"""
        logger.info("\n🔄 Starting schedule loop...")
        logger.info("Press Ctrl+C to stop")
        logger.info("=" * 60)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logger.warning("\n⚠️ Schedule stopped by user")
            logger.info("Goodbye! 👋")


async def test_immediate_upload():
    """Test upload ngay lập tức (không đợi schedule)"""
    logger.info("🧪 Testing immediate upload...")
    logger.info("=" * 60)
    
    manager = ScheduleManager()
    await manager.run_upload_job()


async def test_schedule_simulation():
    """Test schedule với thời gian ngắn (mỗi 2 phút)"""
    logger.info("🧪 Testing schedule simulation...")
    logger.info("⏰ Will upload every 2 minutes (for testing)")
    logger.info("=" * 60)
    
    manager = ScheduleManager()
    
    # Override schedule for testing (every 2 minutes)
    schedule.every(2).minutes.do(
        lambda: asyncio.run(manager.run_upload_job())
    )
    
    logger.success("✅ Scheduled uploads every 2 minutes")
    logger.info("\n🔄 Starting test loop...")
    logger.info("Will run 3 uploads then stop")
    logger.info("Press Ctrl+C to stop early")
    logger.info("=" * 60)
    
    try:
        upload_count = 0
        max_uploads = 3
        
        while upload_count < max_uploads:
            schedule.run_pending()
            
            # Check if we just ran a job
            if schedule.jobs and schedule.jobs[0].last_run:
                pending = manager.file_manager.get_pending_videos_count()
                if pending == 0:
                    logger.warning("⚠️ Hết video để upload!")
                    break
            
            time.sleep(10)  # Check every 10 seconds
            
        logger.success(f"\n🎉 Test hoàn thành! Đã chạy {upload_count} lần")
        
    except KeyboardInterrupt:
        logger.warning("\n⚠️ Test stopped by user")


def show_menu():
    """Hiển thị menu lựa chọn"""
    print("\n" + "=" * 60)
    print("📅 YouTube Upload Scheduler - Test Menu")
    print("=" * 60)
    print("\n1. Test upload ngay lập tức (1 video)")
    print("2. Test schedule với 2 phút/video (3 videos)")
    print("3. Chạy schedule thật (theo config - hàng ngày)")
    print("4. Xem thông tin schedule hiện tại")
    print("5. Exit")
    print("\n" + "=" * 60)
    
    choice = input("\nChọn option (1-5): ").strip()
    return choice


async def show_schedule_info():
    """Hiển thị thông tin schedule"""
    settings = Settings()
    file_manager = VideoFileManager(settings.VIDEO_FOLDER_PATH)
    
    print("\n" + "=" * 60)
    print("📊 Schedule Information")
    print("=" * 60)
    
    print(f"\n⏰ Upload Time: {settings.UPLOAD_SCHEDULE_TIME}")
    print(f"🌍 Timezone: {settings.TIMEZONE}")
    print(f"📹 Video Folder: {settings.VIDEO_FOLDER_PATH}")
    print(f"📊 Pending Videos: {file_manager.get_pending_videos_count()}")
    print(f"✅ Uploaded Videos: {len(file_manager.get_uploaded_videos())}")
    
    print(f"\n📝 Upload Config:")
    print(f"   - LLM: {settings.LLM_PROVIDER} ({settings.LLM_MODEL})")
    print(f"   - Prompt: {settings.DESCRIPTION_PROMPT_TYPE}")
    print(f"   - Category: {settings.YOUTUBE_CATEGORY}")
    print(f"   - Privacy: {settings.YOUTUBE_PRIVACY_STATUS}")
    print(f"   - Channel: {settings.YOUTUBE_CHANNEL_ID or 'default'}")
    
    print("\n" + "=" * 60)


async def main():
    """Main function với menu"""
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            await test_immediate_upload()
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            await test_schedule_simulation()
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            manager = ScheduleManager()
            manager.schedule_daily_upload()
            manager.run_schedule_loop()
            break
            
        elif choice == "4":
            await show_schedule_info()
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice! Please select 1-5")


if __name__ == "__main__":
    asyncio.run(main())
