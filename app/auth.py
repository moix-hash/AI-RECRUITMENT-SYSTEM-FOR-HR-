from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

# Streamlit runs files from ``app/`` directly, which can otherwise make this
# module shadow the root-level ``auth`` package.
PROJECT_ROOT = str(Path(__file__).resolve().parents[1])
if PROJECT_ROOT in sys.path:
    sys.path.remove(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from auth.services import AuthenticationService
from database.models import User
from validators.input_validators import ValidationError, validate_email, validate_password, validate_username

_auth_service = AuthenticationService()


def authenticate(username: str, password: str) -> Optional[User]:
    return _auth_service.login(username, password)


def register_user(username: str, email: str, password: str, role: str = "hr") -> User:
    validate_username(username)
    validate_email(email)
    validate_password(password)
    return _auth_service.register(username, email, password, role)


def require_auth() -> None:
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        st.switch_page("app/login.py")
