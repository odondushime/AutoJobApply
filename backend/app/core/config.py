from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AutoJobApply"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    
    # Job board settings
    LINKEDIN_EMAIL: Optional[str] = None
    LINKEDIN_PASSWORD: Optional[str] = None
    
    # Document paths
    RESUME_PATH: Optional[Path] = None
    COVER_LETTER_PATH: Optional[Path] = None
    
    # Browser settings
    HEADLESS: bool = False
    USER_AGENT: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 