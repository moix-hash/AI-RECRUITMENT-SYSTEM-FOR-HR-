from __future__ import annotations

from typing import Callable

import streamlit as st


def require_role(required_role: str) -> Callable:
    def decorator(function: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            user = st.session_state.get("user", {})
            if user.get("role") != required_role and user.get("role") != "admin":
                st.warning("You do not have access to this feature")
                return None
            return function(*args, **kwargs)

        return wrapper

    return decorator
