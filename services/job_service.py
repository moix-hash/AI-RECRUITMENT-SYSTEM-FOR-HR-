from __future__ import annotations

from datetime import datetime
from typing import Any

from database.models import Job, SessionLocal
from repositories.job_repository import JobRepository


class JobService:
    """Transactional job workflow service and extension point for provider adapters."""

    def create(self, user_id: int, payload: dict[str, Any]) -> Job:
        title = str(payload.get("title", "")).strip()
        if not title:
            raise ValueError("A job title is required.")
        allowed = {column.name for column in Job.__table__.columns} - {"id", "created_at", "updated_at", "user_id"}
        values = {key: value for key, value in payload.items() if key in allowed}
        with SessionLocal() as session:
            return JobRepository(session).create(Job(user_id=user_id, **values))

    def transition(self, user_id: int, job_id: int, status: str) -> Job:
        if status not in {"Draft", "Open", "Scheduled", "Archived", "Closed"}:
            raise ValueError("Invalid job status.")
        with SessionLocal() as session:
            job = session.get(Job, job_id)
            if not job or job.user_id != user_id:
                raise ValueError("Job not found.")
            job.status = status
            session.commit()
            session.refresh(job)
            return job

    def update(self, user_id: int, job_id: int, payload: dict[str, Any]) -> Job:
        """Update a recruiter's own job without allowing cross-user edits."""
        with SessionLocal() as session:
            job = session.get(Job, job_id)
            if not job or job.user_id != user_id:
                raise ValueError("Job not found.")
            allowed = {column.name for column in Job.__table__.columns} - {
                "id", "created_at", "updated_at", "user_id", "source", "external_id"
            }
            values = {key: value for key, value in payload.items() if key in allowed}
            if "title" in values and not str(values["title"]).strip():
                raise ValueError("A job title is required.")
            for key, value in values.items():
                setattr(job, key, value)
            session.commit()
            session.refresh(job)
            return job

    def duplicate(self, user_id: int, job_id: int) -> Job:
        with SessionLocal() as session:
            job = session.get(Job, job_id)
            if not job or job.user_id != user_id:
                raise ValueError("Job not found.")
            return JobRepository(session).duplicate(job)
