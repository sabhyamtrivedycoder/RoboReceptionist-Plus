"""
core/config.py - Centralized Application Configuration & Runtime Settings
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class AppConfig(BaseSettings):
    APP_NAME: str = "Robo Receptionist +"
    APP_VERSION: str = "2.1.0"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 5000

    # Storage Paths
    DATABASE_PATH: Path = BASE_DIR / "receptionist.db"
    MODELS_DIR: Path = BASE_DIR / "models"
    STATIC_DIR: Path = BASE_DIR / "static"
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    WEIGHTS_FILE: Path = BASE_DIR / "models" / "emergency_vision_backbone_weights.pt"

    # Vision & Image Processing Constraints
    MAX_IMAGE_UPLOAD_BYTES: int = 15 * 1024 * 1024  # 15 MB
    DEFAULT_JPEG_QUALITY: int = 88
    MIN_CONTOUR_AREA_RATIO: float = 0.005
    REDNESS_HIGH_SEVERITY_THRESHOLD: float = 18.0

    # Cloud Vision Defaults
    GEMINI_API_TIMEOUT_SECONDS: float = 25.0
    OPENAI_API_TIMEOUT_SECONDS: float = 25.0
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = AppConfig()
