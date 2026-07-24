from __future__ import annotations

from database.models import Resume
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class ResumeRepository(BaseRepository[Resume]):
    """Repository for uploaded resumes."""

    def __init__(self, session: Session) -> None:
        super().__init__(Resume, session)

    def list_for_user(self, user_id: int):
        return self.session.query(Resume).filter(Resume.user_id == user_id).all()
