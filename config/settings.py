from __future__ import annotations

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///recruitment_dashboard.db")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt-secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "gemini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))
APP_ENV = os.getenv("APP_ENV", "development")
MAX_UPLOAD_SIZE_MB = int(os.getenv("MAX_UPLOAD_SIZE_MB", "20"))
SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "60"))
UPLOAD_DIRECTORY = os.getenv("UPLOAD_DIRECTORY", str(BASE_DIR / "data" / "uploads"))
MAX_RESUME_COUNT = int(os.getenv("MAX_RESUME_COUNT", "100"))
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
ALLOW_REGISTRATION = os.getenv("ALLOW_REGISTRATION", "true").lower() == "true"
APP_NAME = os.getenv("APP_NAME", "AI Recruitment Assistant")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

DEFAULT_THEME = "dark"
