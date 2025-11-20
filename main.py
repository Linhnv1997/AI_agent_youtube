"""
Main entry point for YouTube Auto Upload AI Agent
"""
import asyncio
from pathlib import Path
from loguru import logger

from src.utils.config import Settings
from src.workflows.upload_workflow import YouTubeUploadWorkflow


def setup_logging(settings: Settings):
    """Cấu hình logging"""
    logger.add(
        settings.LOG_FILE,
        rotation="1 day",
        retention="7 days",
        level=settings.LOG_LEVEL,
    )


async def main():
    """Main function"""
    # Load settings
    settings = Settings()
    setup_logging(settings)
    
    logger.info("🚀 Starting YouTube Auto Upload AI Agent")
    
    # Initialize workflow
    workflow = YouTubeUploadWorkflow(settings)
    
    # Run the workflow
    try:
        await workflow.run()
    except KeyboardInterrupt:
        logger.info("⚠️ Application stopped by user")
    except Exception as e:
        logger.error(f"❌ Error occurred: {e}")
        raise
    finally:
        logger.info("👋 Application shutdown")


if __name__ == "__main__":
    asyncio.run(main())
