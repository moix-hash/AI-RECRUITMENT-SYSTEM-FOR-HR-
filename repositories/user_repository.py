from __future__ import annotations

from typing import Optional

from database.models import User
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class UserRepository(BaseRepository[User]):
    """Repository for user records."""

    def __init__(self, session: Session) -> None:
        super().__init__(User, session)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
