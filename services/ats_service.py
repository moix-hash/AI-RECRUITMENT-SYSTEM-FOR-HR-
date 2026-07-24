from __future__ import annotations

from sqlalchemy.orm import joinedload

from database.models import Application, AuditLog, Company, CompanyMembership, Job, Resume, SessionLocal
from utils.analysis_fallback import build_fallback_analysis

PIPELINE_STAGES = (
    "Applied", "AI Screening", "Recruiter Review", "Phone Screening", "Technical Interview",
    "HR Interview", "Manager Interview", "Assessment", "Reference Check", "Offer", "Hired", "Rejected", "Withdrawn",
)


class ATSService:
    def default_company_for(self, user_id: int) -> Company:
        with SessionLocal() as session:
            membership = session.query(CompanyMembership).filter_by(user_id=user_id).first()
            if membership:
                return membership.company
            company = Company(name=f"Workspace {user_id}")
            session.add(company)
            session.flush()
            session.add(CompanyMembership(company_id=company.id, user_id=user_id, role="admin"))
            session.commit()
            session.refresh(company)
            return company

    def list_applications(self, company_id: int) -> list[Application]:
        with SessionLocal() as session:
            return (
                session.query(Application)
                .options(joinedload(Application.resume), joinedload(Application.job))
                .filter_by(company_id=company_id)
                .order_by(Application.updated_at.desc())
                .all()
            )

    def move_application(self, user_id: int, application_id: int, stage: str) -> Application:
        if stage not in PIPELINE_STAGES:
            raise ValueError("Invalid pipeline stage.")
        with SessionLocal() as session:
            item = session.get(Application, application_id)
            if item is None:
                raise ValueError("Application not found.")
            membership = session.query(CompanyMembership).filter_by(company_id=item.company_id, user_id=user_id).first()
            if membership is None:
                raise PermissionError("You do not have access to this application.")
            item.stage = stage
            session.add(AuditLog(company_id=item.company_id, user_id=user_id, action="application.stage_changed", entity_type="application", entity_id=item.id, details=stage))
            session.commit()
            session.refresh(item)
            return item

    def schedule_interview(self, user_id: int, application_id: int, when: str, meeting_link: str = "") -> Application:
        """Store an interview plan and add an audit entry for the recruiter."""
        with SessionLocal() as session:
            item = session.get(Application, application_id)
            if item is None:
                raise ValueError("Application not found.")
            membership = session.query(CompanyMembership).filter_by(company_id=item.company_id, user_id=user_id).first()
            if membership is None:
                raise PermissionError("You do not have access to this application.")
            detail = f"Interview scheduled for {when}" + (f" | {meeting_link}" if meeting_link else "")
            item.notes = f"{item.notes}\n{detail}".strip()
            if item.stage in {"Applied", "AI Screening", "Recruiter Review"}:
                item.stage = "Phone Screening"
            session.add(AuditLog(company_id=item.company_id, user_id=user_id, action="application.interview_scheduled", entity_type="application", entity_id=item.id, details=detail))
            session.commit()
            session.refresh(item)
            return item

    def seed_demo_applications(self, user_id: int) -> int:
        """Create a small, clearly demo-only board once for a recruiter workspace."""
        from services.demo_candidates import seed_demo_candidates
        from services.job_catalog import populate_catalog

        populate_catalog(user_id)
        seed_demo_candidates(user_id)
        company = self.default_company_for(user_id)
        with SessionLocal() as session:
            if session.query(Application.id).filter_by(company_id=company.id).first():
                return 0
            resumes = session.query(Resume).filter_by(user_id=user_id).order_by(Resume.id).limit(6).all()
            jobs = session.query(Job).filter_by(user_id=user_id, status="Open").order_by(Job.id).limit(6).all()
            stages = ("Applied", "AI Screening", "Recruiter Review", "Phone Screening", "Technical Interview", "Offer")
            for index, (resume, job) in enumerate(zip(resumes, jobs)):
                session.add(Application(
                    company_id=company.id, job_id=job.id, resume_id=resume.id,
                    stage=stages[index], match_score=88 - index * 4,
                    recommendation="Interview" if index < 4 else "Review",
                    notes="[Demo data] Candidate added to the TalentOS sample pipeline.",
                ))
            session.commit()
            return min(len(resumes), len(jobs))

    def add_resume_to_pipeline(self, recruiter_user_id: int, resume_id: int) -> Application | None:
        """Place an uploaded recruiter CV into the newest open role for triage."""
        company = self.default_company_for(recruiter_user_id)
        with SessionLocal() as session:
            resume = session.get(Resume, resume_id)
            job = session.query(Job).filter_by(user_id=recruiter_user_id, status="Open").order_by(Job.updated_at.desc()).first()
            if not resume or resume.user_id != recruiter_user_id or not job:
                return None
            existing = session.query(Application).filter_by(company_id=company.id, job_id=job.id, resume_id=resume.id).first()
            if existing:
                return existing
            item = Application(company_id=company.id, job_id=job.id, resume_id=resume.id, stage="Applied", match_score=0, recommendation="New")
            session.add(item)
            session.add(AuditLog(company_id=company.id, user_id=recruiter_user_id, action="application.created", entity_type="application", details="Resume added to pipeline"))
            session.commit()
            session.refresh(item)
            return item

    def apply_to_job(self, candidate_user_id: int, job_id: int) -> Application:
        """Validate an open role and screen the candidate's newest CV before submission."""
        with SessionLocal() as session:
            job = session.get(Job, job_id)
            resume = session.query(Resume).filter_by(user_id=candidate_user_id).order_by(Resume.extracted_at.desc()).first()
            if not job or job.status != "Open":
                raise ValueError("This job is no longer accepting applications.")
            if not resume:
                raise ValueError("Upload your CV before applying.")
            analysis = build_fallback_analysis(
                resume.text_content or "",
                f"{job.required_skills or ''}\n{job.preferred_skills or ''}\n{job.responsibilities or ''}",
            )
        company = self.default_company_for(job.user_id)
        with SessionLocal() as session:
            existing = session.query(Application).filter_by(company_id=company.id, job_id=job_id, resume_id=resume.id).first()
            if existing:
                return existing
            accepted = int(analysis["final_score"]) >= 60
            decision = "Accepted for review" if accepted else "Rejected — insufficient job match"
            application = Application(
                company_id=company.id,
                job_id=job_id,
                resume_id=resume.id,
                stage="Applied" if accepted else "Rejected",
                match_score=int(analysis["final_score"]),
                recommendation=decision,
                notes=(
                    f"Automated CV screening: {decision}. "
                    f"Matching skills: {', '.join(analysis['matching_skills']) or 'none identified'}. "
                    f"Focus areas: {', '.join(analysis['missing_skills']) or 'none'}."
                ),
            )
            session.add(application)
            session.add(AuditLog(company_id=company.id, user_id=candidate_user_id, action="application.screened", entity_type="application", details=f"{job.title}: {decision} ({analysis['final_score']}%)"))
            session.commit()
            session.refresh(application)
            return application
