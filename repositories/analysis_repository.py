from __future__ import annotations

from database.models import AnalysisResult
from repositories.base_repository import BaseRepository
from sqlalchemy.orm import Session


class AnalysisRepository(BaseRepository[AnalysisResult]):
    """Repository for analysis results."""

    def __init__(self, session: Session) -> None:
        super().__init__(AnalysisResult, session)

    def list_for_user(self, user_id: int):
        return self.session.query(AnalysisResult).filter(AnalysisResult.user_id == user_id).all()
