from __future__ import annotations

import hashlib

import streamlit as st

from app.auth import require_auth
from app_logging.app_logger import AppLogger
from components.theme import apply_theme
from database.models import Job, SessionLocal
from services.analysis_service import AnalysisService
from services.ats_service import ATSService
from services.resume_service import ResumeService
from utils.analysis_fallback import build_fallback_analysis

logger = AppLogger("upload").get_logger()
DEFAULT_JOB_DESCRIPTION = """Software engineer

Build reliable web and data products with Python and SQL. Work with cloud services,
APIs, version control, Docker, and collaborative product teams. The ideal candidate
communicates clearly, solves problems independently, and can describe measurable
project outcomes."""


def _file_key(uploaded_file) -> str:
    content = uploaded_file.getvalue()
    return f"{uploaded_file.name}:{hashlib.sha256(content).hexdigest()}"


def _job_text(job: Job) -> str:
    return "\n".join(part for part in (job.title, job.required_skills, job.preferred_skills, job.responsibilities) if part)


def _best_role_for(resume_text: str, jobs: list[Job]) -> tuple[str, str]:
    """Select the best open vacancy for this CV rather than using one global template."""
    if not jobs:
        return "General technology role", DEFAULT_JOB_DESCRIPTION
    selected = max(jobs, key=lambda job: int(build_fallback_analysis(resume_text, _job_text(job))["final_score"]))
    return f"{selected.title} — {selected.company or 'Your company'}", _job_text(selected)


def _show_analysis(analysis: dict) -> None:
    st.subheader("Resume readiness report")
    score, recommendation = st.columns(2)
    with score:
        st.metric("Readiness score", f"{analysis['final_score']}/100", border=True)
    with recommendation:
        st.metric("Recommendation", analysis["recommendation"], border=True)
    st.write(analysis["candidate_summary"])
    matching, missing = st.columns(2)
    with matching:
        st.markdown("**Strengths found**")
        st.write(", ".join(analysis["matching_skills"]) or "General professional experience and transferable skills")
    with missing:
        st.markdown("**Focus areas**")
        st.write(", ".join(analysis["missing_skills"]) or "Add role-specific achievements and measurable outcomes")
    st.markdown("**Suggested interview questions**")
    for question in analysis["interview_questions"]:
        st.write(f"• {question}")


def page() -> None:
    apply_theme()
    require_auth()
    st.markdown("<div class='muted'>CANDIDATES / RESUME INTAKE</div>", unsafe_allow_html=True)
    st.title("Upload and review resumes")
    st.caption("Upload a PDF to extract candidate information and receive an immediate AI-assisted readiness report.")
    if "processed_uploads" not in st.session_state:
        st.session_state.processed_uploads = {}
    user_id = int(st.session_state.get("user", {}).get("user_id", 1))
    with SessionLocal() as session:
        open_jobs = session.query(Job).filter_by(user_id=user_id, status="Open").order_by(Job.updated_at.desc()).all()
    uploaded_files = st.file_uploader("Choose resume PDFs", type=["pdf"], accept_multiple_files=True, help="PDF files up to the configured size limit.")
    for uploaded_file in uploaded_files or []:
        key = _file_key(uploaded_file)
        if key not in st.session_state.processed_uploads:
            try:
                st.session_state.processed_uploads[key] = ResumeService().upload_resume(uploaded_file, user_id)
                ATSService().add_resume_to_pipeline(user_id, st.session_state.processed_uploads[key]["id"])
                st.toast(f"{uploaded_file.name} added to the candidate workspace.", icon=":material/check_circle:")
            except Exception as exc:
                logger.exception("Upload failed: %s", exc)
                st.error("We couldn’t process this PDF. Confirm it is a valid, unlocked PDF and try again.")
                continue
        result = st.session_state.processed_uploads[key]
        with st.container(border=True):
            st.subheader(result["filename"])
            extracted_text = result["text_preview"].strip()
            if extracted_text:
                st.success("Text extracted successfully. Review it, then run the analysis.", icon=":material/check_circle:")
                resume_text = st.text_area("Extracted resume text", value=extracted_text, height=180, key=f"resume-text-{key}")
            else:
                st.warning("This PDF appears to contain no selectable text. It may be scanned or design-only. Paste the resume text below to continue with analysis.", icon=":material/document_scanner:")
                resume_text = st.text_area("Paste resume text", height=180, key=f"resume-text-{key}", placeholder="Paste the candidate’s experience, skills, education, and projects here…")
            st.markdown("**Role match**")
            role_name, suggested_description = _best_role_for(resume_text, open_jobs)
            st.caption(f"Best available role for this CV: **{role_name}**. You can replace the description to compare another vacancy.")
            job_description = st.text_area(
                "Job description used for this review",
                value=suggested_description,
                height=160,
                key=f"job-description-{key}",
                help="This role is selected from your current open vacancies using the candidate's extracted CV text.",
            )
            if st.button("Analyze resume", key=f"analyze-{key}", type="primary", icon=":material/auto_awesome:"):
                if not resume_text.strip():
                    st.error("Add readable resume text before analysis. For scanned PDFs, paste the text from the CV.")
                else:
                    with st.status("Reviewing the resume…", expanded=False) as status:
                        analysis = AnalysisService().analyze(resume_text, job_description or DEFAULT_JOB_DESCRIPTION)
                        status.update(label="Resume analysis complete", state="complete")
                    _show_analysis(analysis)


if __name__ == "__main__":
    page()
