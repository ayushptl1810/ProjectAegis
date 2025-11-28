import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Basic configuration class"""
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "7860"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

config = Config()