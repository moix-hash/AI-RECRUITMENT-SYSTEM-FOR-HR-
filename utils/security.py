from __future__ import annotations

import hashlib
import os
import re
import secrets
from datetime import datetime, timedelta
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    return generate_password_hash(password, method="pbkdf2:sha256")


def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)


def sanitize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def is_safe_filename(filename: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9._-]+$", filename))


def generate_session_token() -> str:
    return secrets.token_urlsafe(32)


def session_expired(last_activity: Optional[datetime], timeout_minutes: int) -> bool:
    if last_activity is None:
        return True
    return datetime.utcnow() - last_activity > timedelta(minutes=timeout_minutes)
