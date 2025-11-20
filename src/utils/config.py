"""
Configuration management using Pydantic Settings
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(..., description="OpenAI API key")
    LLM_MODEL: str = Field(default="gpt-4", description="LLM model to use")
    LLM_TEMPERATURE: float = Field(default=0.7, description="LLM temperature")
    MAX_DESCRIPTION_LENGTH: int = Field(default=5000, description="Max description length")
    
    # YouTube Configuration
    YOUTUBE_CLIENT_ID: str = Field(..., description="YouTube API client ID")
    YOUTUBE_CLIENT_SECRET: str = Field(..., description="YouTube API client secret")
    
    # Video Configuration
    VIDEO_FOLDER_PATH: Path = Field(default=Path("./data/videos"), description="Path to video folder")
    UPLOAD_SCHEDULE_TIME: str = Field(default="09:00", description="Time to upload video daily (HH:MM)")
    
    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FILE: Path = Field(default=Path("./logs/app.log"), description="Log file path")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
