from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from database.models import SessionLocal, User
from utils.security import hash_password, verify_password


class AuthenticationService:
    """Handles authentication workflows and session metadata."""

    def login(self, username: str, password: str) -> Optional[User]:
        with SessionLocal() as db:
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.password_hash):
                user.last_login = datetime.utcnow()
                db.commit()
                return user
        return None

    def register(self, username: str, email: str, password: str, role: str = "hr") -> User:
        with SessionLocal() as db:
            if db.query(User).filter((User.username == username) | (User.email == email)).first():
                raise ValueError("User already exists")
            user = User(
                username=username,
                email=email,
                password_hash=hash_password(password),
                role=role,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        if not verify_password(old_password, user.password_hash):
            raise ValueError("Current password is incorrect")
        user.password_hash = hash_password(new_password)
        with SessionLocal() as db:
            db.merge(user)
            db.commit()

    def lock_account(self, user: User, locked_until: datetime) -> None:
        user.locked_until = locked_until
        with SessionLocal() as db:
            db.merge(user)
            db.commit()
