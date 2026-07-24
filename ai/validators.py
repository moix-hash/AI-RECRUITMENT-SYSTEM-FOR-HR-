from __future__ import annotations

import re
from typing import List

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_REGEX = re.compile(r"^(\+?[0-9\- ]{7,20})$")
USERNAME_REGEX = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
PASSWORD_RULES = {
    "min_length": 12,
    "uppercase": True,
    "lowercase": True,
    "digit": True,
    "special": True,
}


def validate_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_phone(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone.strip()))


def validate_username(username: str) -> bool:
    return bool(USERNAME_REGEX.match(username.strip()))


def validate_password(password: str) -> List[str]:
    errors: List[str] = []
    if len(password) < PASSWORD_RULES["min_length"]:
        errors.append(f"Password must be at least {PASSWORD_RULES['min_length']} characters")
    if PASSWORD_RULES["uppercase"] and not re.search(r"[A-Z]", password):
        errors.append("Password must include at least one uppercase letter")
    if PASSWORD_RULES["lowercase"] and not re.search(r"[a-z]", password):
        errors.append("Password must include at least one lowercase letter")
    if PASSWORD_RULES["digit"] and not re.search(r"\d", password):
        errors.append("Password must include at least one digit")
    if PASSWORD_RULES["special"] and not re.search(r"[!@#$%^&*()_+\-=[\]{};':\",.<>/?\\|`~]", password):
        errors.append("Password must include at least one special character")
    return errors


def sanitize_resume_text(text: str) -> str:
    if not text or not isinstance(text, str):
        return ""
    cleaned = re.sub(r"[\x00-\x1f\x7f]+", " ", text)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return strip_junk_prompts(cleaned).strip()


def strip_junk_prompts(text: str) -> str:
    patterns = [
        r"(?i)(system|user|assistant)\s*:\s*.*",
        r"(?i)ignore the above.*",
        r"(?i)do not follow.*",
        r"(?i)you are now.*",
        r"(?i)override.*",
    ]
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned)
    return cleaned.strip()


def normalize_not_found(value: str | None) -> str:
    if value is None:
        return "Not Found"
    stripped = value.strip()
    return stripped if stripped else "Not Found"
