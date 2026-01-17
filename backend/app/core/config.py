from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # API Settings
    PROJECT_NAME: str
    DEBUG: bool = True
    SECRET_KEY: str
    
    # AI API Keys (opsiyonel)
    ANTHROPIC_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ekstra alanları yok say

settings = Settings()

