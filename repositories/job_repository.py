from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from database.models import Job
from repositories.base_repository import BaseRepository


class JobRepository(BaseRepository[Job]):
    def __init__(self, session: Session) -> None:
        super().__init__(Job, session)

    def list_for_user(self, user_id: int, status: str | None = None, query: str = "") -> list[Job]:
        statement = self.session.query(Job).filter(Job.user_id == user_id)
        if status and status != "All":
            statement = statement.filter(Job.status == status)
        if query.strip():
            term = f"%{query.strip()}%"
            statement = statement.filter(or_(Job.title.ilike(term), Job.company.ilike(term), Job.location.ilike(term)))
        return statement.order_by(Job.updated_at.desc()).all()

    def list_open(self, query: str = "") -> list[Job]:
        statement = self.session.query(Job).filter(Job.status == "Open")
        if query.strip():
            term = f"%{query.strip()}%"
            statement = statement.filter(or_(Job.title.ilike(term), Job.company.ilike(term), Job.location.ilike(term)))
        return statement.order_by(Job.updated_at.desc()).all()

    def duplicate(self, job: Job) -> Job:
        copy = Job(
            user_id=job.user_id, title=f"{job.title} (Copy)", department=job.department, company=job.company,
            location=job.location, remote_status=job.remote_status, employment_type=job.employment_type,
            salary_range=job.salary_range, experience=job.experience, required_skills=job.required_skills,
            preferred_skills=job.preferred_skills, responsibilities=job.responsibilities, education=job.education,
            benefits=job.benefits, status="Draft", source="manual",
        )
        return self.create(copy)
