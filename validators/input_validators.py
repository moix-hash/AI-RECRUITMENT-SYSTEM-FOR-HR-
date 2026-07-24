from __future__ import annotations

import re
from typing import Optional


class ValidationError(ValueError):
    """Raised for invalid user input."""


def validate_email(email: str) -> str:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        raise ValidationError("Invalid email address")
    return email


def validate_username(username: str) -> str:
    if len(username) < 4:
        raise ValidationError("Username must be at least 4 characters")
    return username


def validate_password(password: str) -> str:
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must contain an uppercase character")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must contain a lowercase character")
    if not re.search(r"\d", password):
        raise ValidationError("Password must contain a number")
    if not re.search(r"[^A-Za-z0-9]", password):
        raise ValidationError("Password must contain a special character")
    return password


def sanitize_text(value: str) -> str:
    if value is None:
        return ""
    cleaned = value.replace("\x00", "")
    cleaned = re.sub(r"[\x00-\x1f\x7f]", "", cleaned)
    return cleaned.strip()
