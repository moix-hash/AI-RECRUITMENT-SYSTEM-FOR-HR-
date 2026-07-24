from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


@dataclass(frozen=True)
class AppConfig:
    app_name: str = os.getenv("APP_NAME", "AI Recruitment Assistant")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    environment: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///recruitment_dashboard.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-jwt-secret")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    session_timeout: int = int(os.getenv("SESSION_TIMEOUT", "1800"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    upload_directory: str = os.getenv("UPLOAD_DIRECTORY", str(Path(__file__).resolve().parents[1] / "data" / "uploads"))
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "20971520"))
    max_resume_count: int = int(os.getenv("MAX_RESUME_COUNT", "100"))
    enable_cache: bool = os.getenv("ENABLE_CACHE", "true").lower() == "true"
    allow_registration: bool = os.getenv("ALLOW_REGISTRATION", "true").lower() == "true"


CONFIG = AppConfig()
