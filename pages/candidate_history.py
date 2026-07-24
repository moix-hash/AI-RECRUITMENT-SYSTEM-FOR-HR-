from __future__ import annotations

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from database.models import AuditLog, Resume, SessionLocal
from services.ats_service import ATSService
from services.demo_candidates import seed_demo_candidates


def _label(action: str) -> str:
    labels = {
        "application.created": "Candidate added to pipeline",
        "application.screened": "CV screening completed",
        "application.stage_changed": "Pipeline stage updated",
        "application.interview_scheduled": "Interview scheduled",
        "application.submitted": "Candidate submitted an application",
    }
    return labels.get(action, action.replace(".", " ").replace("_", " ").title())


def page() -> None:
    apply_theme()
    require_auth()
    user_id = int(st.session_state.get("user", {}).get("user_id", 1))
    demo_added = seed_demo_candidates(user_id)
    company = ATSService().default_company_for(user_id)
    applications = ATSService().list_applications(company.id)
    with SessionLocal() as session:
        audits = (
            session.query(AuditLog)
            .filter_by(company_id=company.id)
            .order_by(AuditLog.created_at.desc())
            .limit(20)
            .all()
        )
        resumes = session.query(Resume).filter_by(user_id=user_id).order_by(Resume.extracted_at.desc()).limit(8).all()

    st.markdown("<div class='muted'>WORKSPACE / ACTIVITY</div>", unsafe_allow_html=True)
    st.title("Candidate history")
    st.caption("A complete view of CV intake, screening decisions, pipeline movement, and interview activity.")
    if demo_added:
        st.toast(f"Loaded {demo_added} demo candidate records for this workspace.", icon=":material/groups:")
    uploaded, active, interviews = st.columns(3)
    with uploaded:
        st.metric("CVs received", len(resumes))
    with active:
        st.metric("Active candidates", sum(item.stage not in {"Rejected", "Withdrawn", "Hired"} for item in applications))
    with interviews:
        st.metric("Interviews planned", sum("Interview scheduled" in (item.notes or "") for item in applications))

    left, right = st.columns((3, 2), gap="large")
    with left:
        st.subheader("Recent activity")
        if audits:
            for event in audits:
                with st.container(border=True):
                    st.markdown(f"**{_label(event.action)}**")
                    st.caption(event.created_at.strftime("%d %b %Y, %H:%M") if event.created_at else "Recently")
                    st.write(event.details or "Activity recorded in this workspace.")
        else:
            st.info("No actions have been recorded yet. Upload a CV or move a candidate in the pipeline to start the activity feed.")
    with right:
        st.subheader("Recent candidate intake")
        for resume in resumes:
            with st.container(border=True):
                st.markdown(f"**{resume.filename}**")
                st.caption(f"Received {resume.extracted_at.strftime('%d %b %Y') if resume.extracted_at else 'recently'}")
                st.write("Text ready for matching" if (resume.text_content or "").strip() else "Awaiting readable CV text")
        with st.container(horizontal=True):
            st.button("Open pipeline", icon=":material/account_tree:", on_click=lambda: st.session_state.update(current_page="Pipeline"))
            st.button("View rankings", icon=":material/person_search:", on_click=lambda: st.session_state.update(current_page="Candidate Ranking"))


if __name__ == "__main__":
    page()
