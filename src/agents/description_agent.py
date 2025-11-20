"""
AI Agent for generating video descriptions using LLM
"""
from pathlib import Path
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from loguru import logger


class DescriptionAgent:
    """Agent tạo mô tả video bằng LLM"""
    
    def __init__(
        self, 
        provider: str = "gemini",
        api_key: str = "",
        model: str = "gemini-pro", 
        temperature: float = 0.7
    ):
        """
        Initialize Description Agent
        
        Args:
            provider: "openai" hoặc "gemini"
            api_key: API key tương ứng
            model: Model name
            temperature: Temperature cho LLM
        """
        self.provider = provider.lower()
        
        # Initialize LLM based on provider
        if self.provider == "openai":
            self.llm = ChatOpenAI(
                api_key=api_key,
                model=model,
                temperature=temperature
            )
            logger.info(f"✅ Initialized OpenAI LLM: {model}")
        elif self.provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model=model,
                temperature=temperature
            )
            logger.info(f"✅ Initialized Gemini LLM: {model}")
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")
        
        self.prompt_template = self._create_prompt_template()
        self.chain = self.prompt_template | self.llm | StrOutputParser()
    
    def _create_prompt_template(self) -> ChatPromptTemplate:
        """Tạo prompt template cho LLM"""
        template = """Bạn là một chuyên gia viết mô tả video cho YouTube. 
Nhiệm vụ của bạn là tạo một mô tả hấp dẫn, SEO-friendly cho video dựa trên tên file.

Tên video: {video_name}

Yêu cầu:
1. Mô tả phải hấp dẫn và thu hút người xem
2. Tối ưu cho SEO với từ khóa liên quan
3. Độ dài khoảng 200-500 từ
4. Bao gồm:
   - Giới thiệu ngắn gọn về video
   - Nội dung chính
   - Lợi ích người xem nhận được
   - Call-to-action (like, share, subscribe)
5. Sử dụng emoji phù hợp để tăng tính thu hút

{additional_context}

Hãy tạo mô tả video:"""
        
        return ChatPromptTemplate.from_template(template)
    
    async def generate_description(
        self, 
        video_path: Path, 
        additional_context: str = ""
    ) -> Dict[str, Any]:
        """
        Tạo mô tả cho video
        
        Args:
            video_path: Đường dẫn đến video file
            additional_context: Thông tin bổ sung về video
        
        Returns:
            Dict chứa description và metadata
        """
        try:
            video_name = video_path.stem  # Lấy tên file không có extension
            
            logger.info(f"Generating description for: {video_name}")
            
            # Generate description using LLM
            description = await self.chain.ainvoke({
                "video_name": video_name,
                "additional_context": additional_context or "Không có thông tin bổ sung."
            })
            
            # Extract potential title and tags from video name
            title = self._generate_title(video_name)
            tags = self._extract_tags(video_name)
            
            result = {
                "title": title,
                "description": description.strip(),
                "tags": tags,
                "video_path": str(video_path)
            }
            
            logger.success(f"✅ Generated description for {video_name}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Error generating description: {e}")
            raise
    
    def _generate_title(self, video_name: str) -> str:
        """Tạo title từ tên video"""
        # Làm sạch và format tên video thành title
        title = video_name.replace('_', ' ').replace('-', ' ')
        title = ' '.join(word.capitalize() for word in title.split())
        return title[:100]  # YouTube title limit
    
    def _extract_tags(self, video_name: str) -> list[str]:
        """Trích xuất tags từ tên video"""
        # Tách tên thành các từ khóa
        words = video_name.replace('_', ' ').replace('-', ' ').split()
        tags = [word.lower() for word in words if len(word) > 2]
        return tags[:10]  # Giới hạn 10 tags
