from __future__ import annotations

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from services.job_service import JobService
from utils.file_utils import extract_text_from_pdf, save_upload, validate_file_size


def page() -> None:
    apply_theme()
    require_auth()
    st.markdown("<div class='muted'>HIRING / NEW ROLE</div>", unsafe_allow_html=True)
    st.title("Create a job posting")
    st.caption("Publish a role to your Jobs workspace, then use it to evaluate candidates.")

    st.session_state.setdefault("job-description-content", "")
    uploaded_description = st.file_uploader(
        "Upload a job description PDF",
        type=["pdf"],
        help="Optional. We extract the text so you can review and publish it as an open role.",
    )
    if uploaded_description is not None:
        upload_key = f"{uploaded_description.name}:{uploaded_description.size}"
        if st.session_state.get("job-description-upload-key") != upload_key:
            if not validate_file_size(uploaded_description):
                st.error("This job description exceeds the configured upload size limit.")
            else:
                storage_path, _ = save_upload(uploaded_description, uploaded_description.name)
                extracted = extract_text_from_pdf(storage_path)
                if extracted:
                    st.session_state["job-description-content"] = extracted
                    st.session_state["job-description-upload-key"] = upload_key
                    st.success("Job description text extracted. Review it below before publishing.")
                else:
                    st.warning("No selectable text was found in this PDF. Paste the job description below instead.")

    with st.form("create-job", border=True):
        title = st.text_input("Job title", placeholder="e.g. Senior Python Engineer")
        company = st.text_input("Company", placeholder="e.g. TalentOS")
        location = st.text_input("Location", placeholder="e.g. Remote or Karachi")
        required_skills = st.text_input("Required skills", placeholder="e.g. Python, FastAPI, AWS, Docker")
        content = st.text_area(
            "Job description",
            height=260,
            key="job-description-content",
            placeholder="Describe responsibilities, experience, outcomes, and the ideal candidate.",
        )
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
