import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "CareerPilot AI"
    API_V1_STR: str = "/api/v1"
    
    # Database config (defaults to SQLite if PostgreSQL is not provided, allowing zero-friction local run)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./careerpilot.db"
    )
    
    # LLM Provider Configuration (Gemini API)
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

