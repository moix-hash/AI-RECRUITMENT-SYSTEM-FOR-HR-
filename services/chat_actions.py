from __future__ import annotations

import secrets
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable

from ai.interview_generator import generate_interview_questions
from database.models import Application, AuditLog, Job, Resume, SessionLocal
from security.authorization import has_permission
from services.ats_service import ATSService, PIPELINE_STAGES
from services.job_service import JobService


@dataclass(frozen=True)
class Actor:
    user_id: int
    role: str


@dataclass(frozen=True)
class ActionSpec:
    name: str
    permission: str
    sensitive: bool
    handler: Callable[[Actor, dict[str, Any]], dict[str, Any]]


class ChatActionService:
    """Tenant-scoped action gateway. AI output never invokes handlers directly."""

    def __init__(self) -> None:
        self._pending: dict[str, tuple[Actor, str, dict[str, Any], datetime]] = {}
        self._actions = {
            "search_jobs": ActionSpec("search_jobs", "jobs.read", False, self._search_jobs),
            "search_candidates": ActionSpec("search_candidates", "candidates.read", False, self._search_candidates),
            "list_applicants": ActionSpec("list_applicants", "candidates.read", False, self._list_applicants),
            "list_interviews": ActionSpec("list_interviews", "candidates.read", False, self._list_interviews),
            "generate_interview_questions": ActionSpec("generate_interview_questions", "interview.generate", False, self._interview_questions),
            "create_job": ActionSpec("create_job", "jobs.write", True, self._create_job),
            "update_application_status": ActionSpec("update_application_status", "applications.write", True, self._update_status),
            "save_recruiter_note": ActionSpec("save_recruiter_note", "notes.write", True, self._save_note),
            "generate_report": ActionSpec("generate_report", "reports.read", False, self._report),
        }

    def available_actions(self, actor: Actor) -> list[str]:
        return [name for name, spec in self._actions.items() if has_permission(actor.role, spec.permission)]

    def request(self, actor: Actor, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        spec = self._actions.get(name)
        if spec is None:
            return {"ok": False, "message": "That action is not available."}
        if not has_permission(actor.role, spec.permission):
            return {"ok": False, "message": "You do not have permission to perform that action."}
        if not spec.sensitive:
            return {"ok": True, "result": spec.handler(actor, payload)}
        token = secrets.token_urlsafe(24)
        self._pending[token] = (actor, name, dict(payload), datetime.utcnow() + timedelta(minutes=5))
        return {"ok": True, "confirmation_required": True, "token": token, "message": f"Confirm {name.replace('_', ' ')}. This request expires in 5 minutes."}

    def confirm(self, actor: Actor, token: str) -> dict[str, Any]:
        pending = self._pending.pop(token, None)
        if not pending:
            return {"ok": False, "message": "Confirmation expired or was already used."}
        original_actor, name, payload, expires = pending
        if original_actor != actor or datetime.utcnow() > expires:
            return {"ok": False, "message": "Confirmation is invalid or expired."}
        spec = self._actions[name]
        if not has_permission(actor.role, spec.permission):
            return {"ok": False, "message": "Your current role cannot perform this action."}
        result = spec.handler(actor, payload)
        self._audit(actor, name, payload)
        return {"ok": True, "result": result}

    @staticmethod
    def _audit(actor: Actor, action: str, payload: dict[str, Any]) -> None:
        company = ATSService().default_company_for(actor.user_id)
        with SessionLocal() as session:
            session.add(AuditLog(company_id=company.id, user_id=actor.user_id, action=f"chat.{action}", entity_type="chat_action", details="Confirmed tool action"))
            session.commit()

    @staticmethod
    def _search_jobs(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        query = str(payload.get("query", "")).strip().lower()
        with SessionLocal() as session:
            jobs = session.query(Job).filter(Job.status == "Open").all()
            matches = [job for job in jobs if not query or query in f"{job.title} {job.location or ''} {job.required_skills or ''}".lower()]
            return {"count": len(matches), "jobs": [{"id": job.id, "title": job.title, "location": job.location, "status": job.status} for job in matches[:20]]}

    @staticmethod
    def _search_candidates(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        query = str(payload.get("query", "")).strip().lower()
        with SessionLocal() as session:
            resumes = session.query(Resume).filter(Resume.user_id == actor.user_id).all()
            matches = [resume for resume in resumes if not query or query in (resume.text_content or "").lower()]
            return {"count": len(matches), "candidates": [{"id": item.id, "filename": item.filename} for item in matches[:20]]}

    @staticmethod
    def _workspace_people(actor: Actor, interviews_only: bool) -> dict[str, Any]:
        company = ATSService().default_company_for(actor.user_id)
        applications = ATSService().list_applications(company.id)
        if interviews_only:
            applications = [item for item in applications if "Interview scheduled" in (item.notes or "") or "Interview" in item.stage]
        people = []
        for item in applications:
            name = Path(item.resume.filename).stem.replace("demo_", "").replace("_cv", "").replace("_", " ").title()
            people.append({"name": name, "role": item.job.title, "stage": item.stage, "score": item.match_score, "application_id": item.id})
        return {"kind": "people", "label": "scheduled interviews" if interviews_only else "applicants", "people": people}

    @staticmethod
    def _list_applicants(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        return ChatActionService._workspace_people(actor, interviews_only=False)

    @staticmethod
    def _list_interviews(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        return ChatActionService._workspace_people(actor, interviews_only=True)

    @staticmethod
    def _interview_questions(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        skills = [str(skill) for skill in payload.get("skills", [])][:12]
        return {"questions": generate_interview_questions(skills, str(payload.get("recommendation", "Interview")))}

    @staticmethod
    def _create_job(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        job = JobService().create(actor.user_id, payload)
        return {"id": job.id, "title": job.title, "status": job.status}

    @staticmethod
    def _update_status(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        application_id = int(payload["application_id"])
        stage = str(payload["stage"])
        application = ATSService().move_application(actor.user_id, application_id, stage)
        return {"id": application.id, "stage": application.stage}

    @staticmethod
    def _save_note(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        application_id = int(payload["application_id"])
        note = str(payload.get("note", "")).strip()
        if not note:
            raise ValueError("A note is required.")
        with SessionLocal() as session:
            item = session.get(Application, application_id)
            if item is None:
                raise ValueError("Application not found.")
            company = ATSService().default_company_for(actor.user_id)
            if company.id != item.company_id:
                raise PermissionError("You do not have access to this application.")
            item.notes = f"{item.notes}\n{note}".strip()
            session.add(AuditLog(company_id=company.id, user_id=actor.user_id, action="application.note_added", entity_type="application", entity_id=item.id, details="Recruiter note added"))
            session.commit()
            return {"id": item.id, "message": "Note saved."}

    @staticmethod
    def _report(actor: Actor, payload: dict[str, Any]) -> dict[str, Any]:
        company = ATSService().default_company_for(actor.user_id)
        with SessionLocal() as session:
            applications = session.query(Application).filter_by(company_id=company.id).all()
            counts = {stage: sum(item.stage == stage for item in applications) for stage in PIPELINE_STAGES}
            return {"applications": len(applications), "pipeline": counts}
