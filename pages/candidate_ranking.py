from __future__ import annotations

from pathlib import Path
import re

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from database.models import Job, Resume, SessionLocal
from services.demo_candidates import seed_demo_candidates
from services.job_catalog import populate_catalog
from utils.analysis_fallback import build_fallback_analysis


def _candidate_name(filename: str) -> str:
    return Path(filename).stem.replace("demo_", "").replace("_cv", "").replace("_", " ").title()


def _status(score: int) -> str:
    if score >= 80:
        return "Strong match"
    if score >= 60:
        return "Interview"
    return "Needs review"


def _candidate_email(resume: Resume) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume.text_content or "")
    return match.group(0).lower() if match else f"resume-{resume.id}@unknown"


def page() -> None:
    apply_theme()
    require_auth()
    user_id = int(st.session_state.get("user", {}).get("user_id", 1))
    populate_catalog(user_id)
    added = seed_demo_candidates(user_id)
    with SessionLocal() as session:
        roles = session.query(Job).filter_by(user_id=user_id, status="Open").order_by(Job.updated_at.desc()).all()
        resumes = session.query(Resume).filter_by(user_id=user_id).order_by(Resume.extracted_at.desc()).all()
    st.markdown("<div class='muted'>CANDIDATES / MATCHING</div>", unsafe_allow_html=True)
    st.title("Candidate ranking")
    if not roles:
        st.info("Create an open job first, then TalentOS can rank candidate CVs against it.")
        return
    st.caption("Each candidate is matched against the open role that best fits their individual CV.")
    unique_resumes: dict[str, Resume] = {}
    for resume in resumes:
        unique_resumes.setdefault(_candidate_email(resume), resume)

    ranked = []
    for resume in unique_resumes.values():
        if not (resume.text_content or "").strip():
            continue
        best_role, analysis = max(
            (
                (role, build_fallback_analysis(
                    resume.text_content,
                    f"{role.required_skills or ''}\n{role.preferred_skills or ''}\n{role.responsibilities or ''}",
                ))
                for role in roles
            ),
            key=lambda item: int(item[1]["final_score"]),
        )
        ranked.append((int(analysis["final_score"]), resume, best_role, analysis))
    ranked.sort(key=lambda item: item[0], reverse=True)
    if added:
        st.toast(f"Added {added} demo CVs to your workspace.", icon=":material/groups:")
    if not ranked:
        st.info("Upload text-based CVs to generate candidate match scores.")
        return
    st.caption(f"{len(ranked)} candidates ranked — scores are based on skills and job requirements, never placeholder zeroes.")
    for position, (score, resume, role, analysis) in enumerate(ranked, start=1):
        with st.container(border=True):
            heading, score_column = st.columns((4, 1), vertical_alignment="center")
            with heading:
                st.subheader(f"#{position} {_candidate_name(resume.filename)}")
                st.caption(f"{_status(score)} · {_candidate_email(resume)} · Best role: {role.title}")
            with score_column:
                st.metric("Match score", f"{score}%")
            st.write(analysis["candidate_summary"])
            st.caption("Matching skills: " + (", ".join(analysis["matching_skills"]) or "No direct skills identified"))
            with st.container(horizontal=True):
                st.button("Shortlist", key=f"shortlist-{resume.id}", icon=":material/bookmark_add:", on_click=lambda: st.toast("Candidate added to your shortlist.", icon=":material/bookmark_added:"))
                st.button("Schedule", key=f"rank-schedule-{resume.id}", icon=":material/event:", on_click=lambda: st.session_state.update(current_page="Pipeline"))


if __name__ == "__main__":
    page()
