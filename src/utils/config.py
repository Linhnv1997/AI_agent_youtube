"""
Configuration management using Pydantic Settings + YAML
"""
from pathlib import Path
from typing import Dict, List, Any
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
import yaml


class Settings(BaseSettings):
    """Application settings - Credentials from .env, Config from YAML"""
    
    # ============================================
    # CREDENTIALS (from .env)
    # ============================================
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    GOOGLE_API_KEY: str = Field(default="", description="Google Gemini API key")
    YOUTUBE_CLIENT_ID: str = Field(default="", description="YouTube API client ID")
    YOUTUBE_CLIENT_SECRET: str = Field(default="", description="YouTube API client secret")
    
    # ============================================
    # CONFIGURATION (from settings.yaml)
    # ============================================
    _config: Dict[str, Any] = {}
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_yaml_config()
    
    def _load_yaml_config(self):
        """Load configuration from YAML file"""
        config_file = Path(__file__).parent.parent.parent / "config" / "settings.yaml"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f) or {}
    
    # ============================================
    # LLM Configuration
    # ============================================
    @property
    def LLM_PROVIDER(self) -> str:
        return self._config.get('llm', {}).get('provider', 'gemini')
    
    @property
    def LLM_MODEL(self) -> str:
        return self._config.get('llm', {}).get('model', 'gemini-2.0-flash-exp')
    
    @property
    def LLM_TEMPERATURE(self) -> float:
        return self._config.get('llm', {}).get('temperature', 0.7)
    
    @property
    def MAX_DESCRIPTION_LENGTH(self) -> int:
        return self._config.get('llm', {}).get('max_description_length', 5000)
    
    # ============================================
    # Video Configuration
    # ============================================
    @property
    def VIDEO_FOLDER_PATH(self) -> Path:
        path = self._config.get('video', {}).get('folder_path', './data/videos')
        return Path(path)
    
    @property
    def SUPPORTED_VIDEO_FORMATS(self) -> List[str]:
        return self._config.get('video', {}).get('supported_formats', ['mp4', 'avi', 'mov', 'mkv'])
    
    # ============================================
    # Upload Schedule
    # ============================================
    @property
    def UPLOAD_SCHEDULE_TIME(self) -> str:
        return self._config.get('schedule', {}).get('upload_time', '09:00')
    
    @property
    def TIMEZONE(self) -> str:
        return self._config.get('schedule', {}).get('timezone', 'Asia/Ho_Chi_Minh')
    
    # ============================================
    # YouTube Settings
    # ============================================
    @property
    def YOUTUBE_CATEGORY(self) -> str:
        return self._config.get('youtube', {}).get('default_category', '22')
    
    @property
    def YOUTUBE_PRIVACY_STATUS(self) -> str:
        return self._config.get('youtube', {}).get('privacy_status', 'public')
    
    @property
    def YOUTUBE_CHANNEL_ID(self) -> str:
        return self._config.get('youtube', {}).get('channel_id', '')
    
    # ============================================
    # Logging Configuration
    # ============================================
    @property
    def LOG_LEVEL(self) -> str:
        return self._config.get('logging', {}).get('level', 'INFO')
    
    @property
    def LOG_FILE(self) -> Path:
        log_file = self._config.get('logging', {}).get('file', './logs/app.log')
        return Path(log_file)
    
    @property
    def LOG_ROTATION(self) -> str:
        return self._config.get('logging', {}).get('rotation', '1 day')
    
    @property
    def LOG_RETENTION(self) -> str:
        return self._config.get('logging', {}).get('retention', '7 days')
    
    # ============================================
    # Description Settings
    # ============================================
    @property
    def DESCRIPTION_MIN_LENGTH(self) -> int:
        return self._config.get('description', {}).get('min_length', 200)
    
    @property
    def DESCRIPTION_LANGUAGE(self) -> str:
        return self._config.get('description', {}).get('language', 'vi')
    
    # ============================================
    # Feature Flags
    # ============================================
    @property
    def AUTO_UPLOAD_ENABLED(self) -> bool:
        return self._config.get('features', {}).get('auto_upload', True)
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get any config value by key (supports nested keys like 'llm.model')"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
