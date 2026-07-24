from __future__ import annotations

from urllib.parse import quote

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from database.models import Job, SessionLocal
from repositories.job_repository import JobRepository
from services.job_catalog import populate_catalog
from services.job_service import JobService
from services.ats_service import ATSService


def _user_id() -> int:
    return int(st.session_state.get("user", {}).get("user_id", 1))


def _is_hiring_user() -> bool:
    return str(st.session_state.get("user", {}).get("role", "")).lower() in {"recruiter", "hr", "hr_manager", "admin"}


def _render_job_editor(user_id: int) -> None:
    job_id = st.session_state.get("editing_job_id")
    if not job_id:
        return
    with SessionLocal() as session:
        job = session.get(Job, job_id)
        if not job or job.user_id != user_id:
            st.session_state.pop("editing_job_id", None)
            return
        values = {
            "title": job.title,
            "company": job.company or "",
            "location": job.location or "",
            "required_skills": job.required_skills or "",
            "responsibilities": job.responsibilities or "",
        }
    st.subheader(f"Edit {values['title']}")
    with st.form(f"edit-job-{job_id}", border=True):
        title = st.text_input("Job title", value=values["title"])
        company = st.text_input("Company", value=values["company"])
        location = st.text_input("Location", value=values["location"])
        skills = st.text_input("Required skills", value=values["required_skills"])
        description = st.text_area("Job description", value=values["responsibilities"], height=220)
        save, cancel = st.columns(2)
        with save:
            save_changes = st.form_submit_button("Save changes", type="primary", icon=":material/save:")
        with cancel:
            cancel_changes = st.form_submit_button("Cancel")
    if cancel_changes:
        st.session_state.pop("editing_job_id", None)
        st.rerun()
    if save_changes:
        if not title.strip() or not description.strip():
            st.error("A job title and description are required.")
            return
        try:
            JobService().update(user_id, job_id, {
                "title": title.strip(), "company": company.strip() or "Your company",
                "location": location.strip() or "Location flexible", "required_skills": skills.strip(),
                "responsibilities": description.strip(),
            })
        except ValueError as exc:
            st.error(str(exc))
            return
        st.session_state.pop("editing_job_id", None)
        st.toast("Job posting updated.", icon=":material/check_circle:")
        st.rerun()


def _share_job(job) -> None:
    """Render useful, user-facing sharing actions instead of a placeholder toast."""
    public_link = f"http://127.0.0.1:8501/?job_id={job.id}"
    summary = (
        f"{job.title} at {job.company or 'TalentOS partner'}\n"
        f"Location: {job.location or 'Location flexible'}\n\n"
        f"{(job.responsibilities or 'View this opportunity in TalentOS.').strip()[:500]}\n\n"
        f"Open the job: {public_link}"
    )
    mailto = f"mailto:?subject={quote('Job opportunity: ' + job.title)}&body={quote(summary)}"
    with st.popover("Share", icon=":material/share:"):
        st.caption("Share this job with a colleague or candidate.")
        st.text_input("Shareable job link", value=public_link, key=f"share-link-{job.id}")
        st.link_button("Email this job", mailto, icon=":material/mail:", width="stretch")


def _job_card(job, hiring_user: bool) -> None:
    with st.container(border=True):
        identity, match = st.columns((5, 1), vertical_alignment="center")
        with identity:
            st.markdown(f"### :material/business: {job.title}")
            st.caption(f"{job.company or 'TalentOS partner'} · {job.location or 'Location flexible'} · {job.remote_status}")
        with match:
            st.metric("Match", "94%", "+3%")
        st.markdown(f"**{job.salary_range or 'Salary discussed during interview'}** · {job.employment_type} · {job.experience or 'Experience flexible'}")
        skills = [skill.strip() for skill in (job.required_skills or "Communication, collaboration").split(",")[:5]]
        st.pills("Role skills", skills, selection_mode="multi", key=f"job-skills-{job.id}")
        description = (job.responsibilities or "Build reliable products with a collaborative technology team.").replace("[Demo data]", "").strip()
        st.write(description[:220] + ("…" if len(description) > 220 else ""))
        with st.container(horizontal=True):
            if hiring_user:
                if st.button("View applicants", key=f"applicants-{job.id}", type="primary", icon=":material/group:"):
                    st.session_state["current_page"] = "Pipeline"
                    st.rerun()
                if st.button("Edit role", key=f"edit-{job.id}", icon=":material/edit:"):
                    # Set state in the same script run, then render the editor on
                    # a clean rerun. This is more reliable than a nested callback
                    # when cards are rendered dynamically.
                    st.session_state["editing_job_id"] = job.id
                    st.rerun()
                _share_job(job)
            else:
                st.button("Apply", key=f"apply-{job.id}", type="primary", icon=":material/send:", on_click=lambda: st.toast("Application started — add your resume to continue.", icon=":material/check_circle:"))
                if st.button("Check CV & apply", key=f"apply-cv-{job.id}", type="primary", icon=":material/fact_check:"):
                    try:
                        application = ATSService().apply_to_job(_user_id(), job.id)
                    except ValueError as exc:
                        st.warning(f"{exc} Use Upload Resume to add your CV.")
                    else:
                        if application.stage == "Rejected":
                            st.warning("Your CV does not currently meet this role's match threshold. The result was recorded as rejected.")
                        else:
                            st.toast("CV accepted for recruiter review. Your application is now in the pipeline.", icon=":material/check_circle:")
                st.button("Save", key=f"save-{job.id}", icon=":material/bookmark:", on_click=lambda: st.toast("Saved to your jobs.", icon=":material/bookmark_added:"))
                _share_job(job)


def page() -> None:
    apply_theme()
    require_auth()
    source, added = populate_catalog(_user_id())
    hiring_user = _is_hiring_user()
    st.markdown("<div class='muted'>CAREERS / DISCOVER</div>", unsafe_allow_html=True)
    st.title("Your active roles" if hiring_user else "Find your next great role")
    st.caption("Manage published openings and review applicants." if hiring_user else "Explore curated technology opportunities. Demo listings are clearly marked in the details.")
    if hiring_user:
        _render_job_editor(_user_id())
    query = st.text_input("Search jobs", placeholder="Job title, skill, company, or location", icon=":material/search:")
    filters = st.pills("Explore", ["Remote", "Engineering", "AI & ML", "Product", "Data", "Senior roles"], selection_mode="multi")
    with SessionLocal() as session:
        repository = JobRepository(session)
        jobs = repository.list_for_user(_user_id(), "Open", query) if hiring_user else repository.list_open(query)
    if filters:
        terms = {"Remote": "remote", "Engineering": "engineer", "AI & ML": "ai", "Product": "product", "Data": "data", "Senior roles": "senior"}
        jobs = [job for job in jobs if any(term in f"{job.title} {job.required_skills} {job.remote_status}".lower() for label, term in terms.items() if label in filters)]
    left, right = st.columns((3, 1), gap="large")
    with left:
        st.subheader(f"{len(jobs)} active roles" if hiring_user else f"{len(jobs)} opportunities for you")
        for job in jobs:
            _job_card(job, hiring_user)
    with right:
        with st.container(border=True):
            st.subheader("Hiring snapshot" if hiring_user else "Your job search")
            if hiring_user:
                st.metric("New applicants", "45", "+12 this week")
                st.metric("Interviews", "17", "+3")
                st.metric("Open roles", str(len(jobs)), "+2")
                if st.button("Open hiring pipeline", width="stretch", icon=":material/account_tree:"):
                    st.session_state["current_page"] = "Pipeline"
                    st.rerun()
            else:
                st.metric("Recommended roles", "25", "+7 this week")
                st.metric("Saved jobs", "8", "+2")
                st.metric("Applications", "14", "+3")
                if st.button("Improve your profile", width="stretch", icon=":material/auto_awesome:"):
                    st.session_state["current_page"] = "Profile"
                    st.rerun()
        with st.container(border=True):
            st.subheader("Recruiting insight" if hiring_user else "Career suggestion")
            st.write("Your cloud and platform roles have the strongest demand this week." if hiring_user else "Add **Kubernetes** to your profile to improve your match for platform and cloud roles.")
            if st.button("View market insight" if hiring_user else "View learning plan", width="stretch", type="tertiary", icon=":material/insights:"):
                st.session_state["current_page"] = "Analytics" if hiring_user else "Profile"
                st.rerun()
    if added:
        st.toast(f"Added {added} {'RSS' if source == 'rss' else 'demo'} opportunities.", icon=":material/check_circle:")


if __name__ == "__main__":
    page()
