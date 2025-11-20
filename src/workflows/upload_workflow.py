"""
LangGraph workflow for YouTube video upload automation
"""
import asyncio
from typing import Dict, Any, TypedDict
from datetime import datetime, time as dt_time
from pathlib import Path
from loguru import logger
import schedule

from langgraph.graph import StateGraph, END
from src.agents.description_agent import DescriptionAgent
from src.tools.youtube_uploader import YouTubeUploader
from src.utils.file_manager import VideoFileManager
from src.utils.config import Settings


class WorkflowState(TypedDict):
    """State cho workflow"""
    video_path: str
    title: str
    description: str
    tags: list[str]
    upload_result: Dict[str, Any]
    error: str
    status: str


class YouTubeUploadWorkflow:
    """Workflow tự động upload video lên YouTube"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.description_agent = DescriptionAgent(
            api_key=settings.OPENAI_API_KEY,
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE
        )
        self.youtube_uploader = YouTubeUploader(
            client_id=settings.YOUTUBE_CLIENT_ID,
            client_secret=settings.YOUTUBE_CLIENT_SECRET
        )
        self.file_manager = VideoFileManager(settings.VIDEO_FOLDER_PATH)
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Xây dựng LangGraph workflow"""
        
        # Define nodes
        async def select_video_node(state: WorkflowState) -> WorkflowState:
            """Node: Chọn video tiếp theo"""
            logger.info("📹 Selecting next video to upload...")
            
            video_path = self.file_manager.get_next_video()
            if not video_path:
                logger.warning("⚠️ No more videos to upload")
                state["status"] = "no_videos"
                state["error"] = "No pending videos found"
                return state
            
            state["video_path"] = str(video_path)
            state["status"] = "video_selected"
            logger.info(f"Selected video: {video_path.name}")
            return state
        
        async def generate_description_node(state: WorkflowState) -> WorkflowState:
            """Node: Tạo mô tả video"""
            logger.info("✍️ Generating video description...")
            
            try:
                video_path = Path(state["video_path"])
                result = await self.description_agent.generate_description(
                    video_path=video_path,
                    additional_context=""
                )
                
                state["title"] = result["title"]
                state["description"] = result["description"]
                state["tags"] = result["tags"]
                state["status"] = "description_generated"
                
            except Exception as e:
                logger.error(f"Error generating description: {e}")
                state["error"] = str(e)
                state["status"] = "error"
            
            return state
        
        async def upload_video_node(state: WorkflowState) -> WorkflowState:
            """Node: Upload video lên YouTube"""
            logger.info("🚀 Uploading video to YouTube...")
            
            try:
                video_path = Path(state["video_path"])
                result = self.youtube_uploader.upload_video(
                    video_path=video_path,
                    title=state["title"],
                    description=state["description"],
                    tags=state["tags"]
                )
                
                if result:
                    state["upload_result"] = result
                    state["status"] = "uploaded"
                    
                    # Mark video as uploaded
                    self.file_manager.mark_as_uploaded(video_path)
                else:
                    state["error"] = "Upload failed"
                    state["status"] = "error"
                    
            except Exception as e:
                logger.error(f"Error uploading video: {e}")
                state["error"] = str(e)
                state["status"] = "error"
            
            return state
        
        def should_continue(state: WorkflowState) -> str:
            """Điều kiện để tiếp tục workflow"""
            status = state.get("status", "")
            
            if status == "no_videos":
                return "end"
            elif status == "error":
                return "end"
            elif status == "video_selected":
                return "generate_description"
            elif status == "description_generated":
                return "upload_video"
            elif status == "uploaded":
                return "end"
            else:
                return "end"
        
        # Build graph
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("select_video", select_video_node)
        workflow.add_node("generate_description", generate_description_node)
        workflow.add_node("upload_video", upload_video_node)
        
        # Add edges
        workflow.set_entry_point("select_video")
        workflow.add_conditional_edges(
            "select_video",
            should_continue,
            {
                "generate_description": "generate_description",
                "end": END
            }
        )
        workflow.add_conditional_edges(
            "generate_description",
            should_continue,
            {
                "upload_video": "upload_video",
                "end": END
            }
        )
        workflow.add_conditional_edges(
            "upload_video",
            should_continue,
            {
                "end": END
            }
        )
        
        return workflow.compile()
    
    async def upload_daily_video(self):
        """Upload một video (gọi hàng ngày)"""
        logger.info("=" * 60)
        logger.info(f"🎬 Starting daily video upload at {datetime.now()}")
        logger.info("=" * 60)
        
        # Check pending videos
        pending_count = self.file_manager.get_pending_videos_count()
        logger.info(f"📊 Pending videos: {pending_count}")
        
        if pending_count == 0:
            logger.warning("⚠️ No videos left to upload!")
            return
        
        # Run workflow
        initial_state = WorkflowState(
            video_path="",
            title="",
            description="",
            tags=[],
            upload_result={},
            error="",
            status="start"
        )
        
        result = await self.workflow.ainvoke(initial_state)
        
        # Log result
        if result["status"] == "uploaded":
            logger.success("✅ Video uploaded successfully!")
            logger.info(f"Video URL: {result['upload_result'].get('video_url')}")
        else:
            logger.error(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
    
    async def run(self):
        """Chạy workflow với schedule"""
        logger.info("🤖 YouTube Auto Upload Bot started")
        logger.info(f"📅 Upload schedule: {self.settings.UPLOAD_SCHEDULE_TIME} daily")
        
        # Parse schedule time
        hour, minute = map(int, self.settings.UPLOAD_SCHEDULE_TIME.split(':'))
        
        # Schedule daily upload
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
            lambda: asyncio.create_task(self.upload_daily_video())
        )
        
        # Upload immediately on first run (for testing)
        logger.info("🚀 Running first upload immediately...")
        await self.upload_daily_video()
        
        # Keep running
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # Check every minute
