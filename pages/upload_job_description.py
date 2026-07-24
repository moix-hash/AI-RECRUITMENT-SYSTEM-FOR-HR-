from __future__ import annotations

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from services.job_service import JobService


def page() -> None:
    apply_theme()
    require_auth()
    st.markdown("<div class='muted'>HIRING / NEW ROLE</div>", unsafe_allow_html=True)
    st.title("Create a job posting")
    st.caption("Publish a role to your Jobs workspace, then use it to evaluate candidates.")

    with st.form("create-job", border=True):
        title = st.text_input("Job title", placeholder="e.g. Senior Python Engineer")
        company = st.text_input("Company", placeholder="e.g. TalentOS")
        location = st.text_input("Location", placeholder="e.g. Remote or Karachi")
        required_skills = st.text_input("Required skills", placeholder="e.g. Python, FastAPI, AWS, Docker")
        content = st.text_area("Job description", height=260, placeholder="Describe responsibilities, experience, outcomes, and the ideal candidate.")
        submitted = st.form_submit_button("Publish job", type="primary", icon=":material/publish:")

    if submitted:
        if not title.strip() or not content.strip():
            st.error("Add a job title and job description before publishing.")
            return
        try:
            user_id = int(st.session_state.get("user", {}).get("user_id", 1))
            job = JobService().create(
                user_id,
                {
                    "title": title,
                    "company": company or "Your company",
                    "location": location or "Location flexible",
                    "required_skills": required_skills,
                    "responsibilities": content,
                    "status": "Open",
                    "source": "manual",
                },
            )
        except Exception:
            st.error("We couldn't publish this job. Please try again.")
            return

        st.session_state.current_page = "Jobs"
        st.success(f"{job.title} is now published and visible in your Jobs workspace.")
        st.rerun()


if __name__ == "__main__":
    page()
