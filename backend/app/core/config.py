"""
Configuration settings for ContextLink
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://contextlink_user:password@localhost:5432/contextlink"
    
    # LLM API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # Application
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Vector Database
    PINECONE_API_KEY: str = ""
    PINECONE_ENVIRONMENT: str = ""
    
    # Carbon Tracking
    CARBON_INTERFACE_API_KEY: str = ""
    
    # Model Settings
    DEFAULT_MODEL: str = "gpt-4"
    MAX_CONTEXT_LENGTH: int = 8000
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
