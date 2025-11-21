"""
AI Agent for generating video descriptions using LLM
"""
from pathlib import Path
from typing import Dict, Any, Optional
import yaml
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
        temperature: float = 0.7,
        prompts_config_path: Optional[Path] = None
    ):
        """
        Initialize Description Agent
        
        Args:
            provider: "openai" hoặc "gemini"
            api_key: API key tương ứng
            model: Model name
            temperature: Temperature cho LLM
            prompts_config_path: Đường dẫn đến file prompts.yaml (optional)
        """
        self.provider = provider.lower()
        self.prompts_config = self._load_prompts_config(prompts_config_path)
        
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
    
    def _load_prompts_config(self, config_path: Optional[Path] = None) -> Dict[str, Any]:
        """Load prompts từ file YAML"""
        if config_path is None:
            # Default path
            config_path = Path(__file__).parent.parent.parent / "config" / "prompts.yaml"
        
        if not config_path.exists():
            logger.warning(f"⚠️ Prompts config not found at {config_path}, using default prompts")
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ Loaded prompts config from {config_path}")
            return config or {}
        except Exception as e:
            logger.error(f"❌ Error loading prompts config: {e}")
            return {}
    
    def _create_prompt_template(self, prompt_type: str = "default") -> ChatPromptTemplate:
        """
        Tạo prompt template cho LLM
        
        Args:
            prompt_type: Loại prompt (default, tech_tutorial, entertainment, educational, toeic_part_youtube)
        """
        # Load prompt từ config nếu có
        custom_prompt_types = {"tech_tutorial", "entertainment", "educational", "toeic_part_youtube"}
        
        if self.prompts_config and prompt_type in custom_prompt_types:
            custom_prompts = self.prompts_config.get("custom_prompts", {})
            if prompt_type in custom_prompts:
                base_prompt = custom_prompts[prompt_type]
            else:
                base_prompt = self.prompts_config.get("default_description_prompt", "")
        else:
            # Default prompt nếu không có config
            base_prompt = self.prompts_config.get("default_description_prompt", "") if self.prompts_config else ""
        
        # Fallback to hardcoded prompt if no config
        if not base_prompt:
            base_prompt = """Bạn là một chuyên gia viết mô tả video cho YouTube. 
Nhiệm vụ của bạn là tạo một mô tả hấp dẫn, SEO-friendly cho video dựa trên tên file."""
        
        # Special handling for toeic_part_youtube - prompt đã có format đầy đủ
        if prompt_type == "toeic_part_youtube":
            template = base_prompt  # Sử dụng trực tiếp prompt từ config
        else:
            # Build full template for other types
            template = f"""{base_prompt}

Tên video: {{video_name}}

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

{{additional_context}}

Hãy tạo mô tả video:"""
        
        return ChatPromptTemplate.from_template(template)
    
    async def generate_description(
        self, 
        video_path: Path, 
        additional_context: str = "",
        prompt_type: str = "default"
    ) -> Dict[str, Any]:
        """
        Tạo mô tả cho video
        
        Args:
            video_path: Đường dẫn đến video file
            additional_context: Thông tin bổ sung về video
            prompt_type: Loại prompt (default, tech_tutorial, entertainment, educational)
        
        Returns:
            Dict chứa description và metadata
        """
        try:
            video_name = video_path.stem  # Lấy tên file không có extension
            
            logger.info(f"Generating description for: {video_name} (prompt: {prompt_type})")
            
            # Recreate chain with specified prompt type
            if prompt_type != "default":
                self.prompt_template = self._create_prompt_template(prompt_type)
                self.chain = self.prompt_template | self.llm | StrOutputParser()
            
            # Generate description using LLM
            description = await self.chain.ainvoke({
                "video_name": video_name,
                "additional_context": additional_context or ""
            })
            
            # Parse title and description for TOEIC prompts
            if prompt_type == "toeic_part_youtube":
                title, description = self._parse_toeic_output(description.strip(), video_name)
            else:
                # Extract potential title and tags from video name for other types
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
    
    def _parse_toeic_output(self, llm_output: str, video_name: str) -> tuple[str, str]:
        """
        Parse output từ LLM cho prompt TOEIC để extract title
        LLM có thể generate title trong output, ta cần tách nó ra
        
        Args:
            llm_output: Full output từ LLM
            video_name: Tên video gốc (fallback)
            
        Returns:
            Tuple of (title, description)
        """
        import re
        
        # Try to find title pattern: 🔥 [TOEIC PART 3] ...
        title_pattern = r'(?:^|\n)([🔥✨]\s*\[TOEIC[^\]]*\][^\n]+)'
        match = re.search(title_pattern, llm_output, re.IGNORECASE)
        
        if match:
            title = match.group(1).strip()
            # Remove title from description
            description = llm_output.replace(match.group(0), '').strip()
            logger.info(f"📌 Extracted title: {title[:50]}...")
        else:
            # Fallback: Generate title from video_name
            title = self._generate_toeic_title(video_name)
            description = llm_output
            logger.warning(f"⚠️ Could not extract title from LLM output, using generated: {title[:50]}...")
        
        return title[:100], description  # YouTube title limit
    
    def _generate_toeic_title(self, video_name: str) -> str:
        """Generate TOEIC style title from video name"""
        # Extract topic from filename (e.g., "Banking", "Shopping", "Office")
        topic = video_name.replace('_', ' ').replace('-', ' ').title()
        return f"🔥 [TOEIC PART 3] Luyện Nghe Tiếng Anh Song Ngữ - {topic} 🔥"
    
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
