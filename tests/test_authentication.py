from __future__ import annotations

import uuid

from app.auth import authenticate, register_user


def test_new_account_can_sign_in() -> None:
    suffix = uuid.uuid4().hex[:10]
    username = f"recruiter_{suffix}"
    password = "SecurePass1!"
    user = register_user(username, f"{username}@example.com", password, "recruiter")
    logged_in = authenticate(username, password)
    assert logged_in is not None
    assert logged_in.id == user.id
    assert logged_in.role == "recruiter"
