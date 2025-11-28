import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the Visual Verification Service"""
    
    # API Configuration
    SERP_API_KEY: Optional[str] = os.getenv("SERP_API_KEY")
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")
    GOOGLE_FACT_CHECK_CX: Optional[str] = os.getenv("GOOGLE_FACT_CHECK_CX")
    
    # Service Configuration
    SERVICE_HOST: str = os.getenv("SERVICE_HOST", "0.0.0.0")
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "7860"))
    
    # File Processing Configuration
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS: set = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    ALLOWED_VIDEO_EXTENSIONS: set = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv'}
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

config = Config()