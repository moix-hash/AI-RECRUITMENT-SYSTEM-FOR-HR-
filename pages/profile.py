from __future__ import annotations

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from database.models import Job, SessionLocal
from services.ats_service import ATSService


def _open_ai(prompt: str) -> None:
    st.session_state["assistant_prompt"] = prompt
    st.session_state["current_page"] = "AI Assistant"


def _open_pipeline(application_id: int | None = None) -> None:
    if application_id is not None:
        st.session_state["schedule_application_id"] = application_id
    st.session_state["current_page"] = "Pipeline"


def _recruiter_profile(user_id: int, username: str) -> None:
    company = ATSService().default_company_for(user_id)
    applications = ATSService().list_applications(company.id)
    with SessionLocal() as session:
        roles = session.query(Job).filter_by(user_id=user_id, status="Open").order_by(Job.updated_at.desc()).all()
    interviews = [item for item in applications if "Interview scheduled" in (item.notes or "")]
    offers = [item for item in applications if item.stage == "Offer"]
    st.markdown("<div class='muted'>HR WORKSPACE / PROFILE</div>", unsafe_allow_html=True)
    st.title(f"Hello, {username}")
    st.caption("Your hiring workspace at a glance — roles, candidates, interviews, and decisions.")
    with st.container(horizontal=True):
        st.metric("Open roles", len(roles), border=True)
        st.metric("Candidates in pipeline", len(applications), border=True)
        st.metric("Interviews planned", len(interviews), border=True)
        st.metric("Offers in progress", len(offers), border=True)
    left, right = st.columns((3, 1), gap="large")
    with left:
        st.subheader("Your active hiring")
        if not roles:
            st.info("No open roles yet. Create a job posting to begin recruiting.")
            st.button("Create a job", type="primary", icon=":material/add_business:", on_click=lambda: st.session_state.update(current_page="Upload JD"))
        for role in roles[:5]:
            role_candidates = [item for item in applications if item.job_id == role.id]
            with st.container(border=True):
                st.markdown(f"#### {role.title}")
                st.caption(f"{role.company or 'Your company'} · {role.location or 'Location flexible'}")
                st.write(f"{len(role_candidates)} candidates in pipeline · {role.required_skills or 'Skills to be defined'}")
                if role_candidates:
                    st.caption("Candidates: " + ", ".join(item.resume.filename.rsplit(".", 1)[0].replace("demo_", "").replace("_cv", "").replace("_", " ").title() for item in role_candidates[:3]))
                if st.button("Review candidates", key=f"review-role-{role.id}", icon=":material/groups:"):
                    _open_pipeline()
                    st.rerun()
                for item in role_candidates[:2]:
                    candidate_name = item.resume.filename.rsplit(".", 1)[0].replace("demo_", "").replace("_cv", "").replace("_", " ").title()
                    if st.button(f"Schedule {candidate_name}", key=f"profile-schedule-{item.id}", icon=":material/event:"):
                        _open_pipeline(item.id)
                        st.rerun()
    with right:
        with st.container(border=True):
            st.subheader("Hiring priorities")
            st.write("Review new applications, schedule shortlisted candidates, and keep your open roles current.")
            if st.button("Open pipeline", width="stretch", type="primary", icon=":material/account_tree:"):
                _open_pipeline()
                st.rerun()
        with st.container(border=True):
            st.subheader("AI recommendations")
            for recommendation, prompt in (
                ("Review highest-match candidates", "Who applied to my jobs?"),
                ("Identify skill gaps", "Show candidate skill gaps"),
                ("Prepare interview questions", "Generate interview questions for the active roles"),
            ):
                st.button(recommendation, key=f"hr-{recommendation}", width="stretch", type="tertiary", icon=":material/auto_awesome:", on_click=_open_ai, args=(prompt,))


def page() -> None:
    apply_theme(); require_auth()
    user = st.session_state.get("user", {})
    if str(user.get("role", "")).lower() in {"recruiter", "hr", "hr_manager", "admin"}:
        _recruiter_profile(int(user.get("user_id", 1)), str(user.get("username") or "Recruiter"))
        return
    st.markdown("<div class='muted'>CANDIDATE / HOME</div>", unsafe_allow_html=True)
    st.title("Hello Moiz 👋"); st.caption("Keep your profile current to unlock better recommendations.")
    with st.container(horizontal=True):
        for label, value, delta, trend in (("Profile strength", "92%", "+6%", [66,72,81,87,92]), ("Resume ATS score", "89%", "+4%", [72,75,80,85,89]), ("Recommended jobs", "25", "+7", [12,15,17,22,25]), ("Applications", "14", "+3", [6,8,9,11,14])):
            st.metric(label, value, delta, border=True, chart_data=trend)
    a,b,c = st.columns(3)
    for col, label, value in ((a,"Interviews","3"),(b,"Offers","1"),(c,"Rejected","2")):
        with col: st.metric(label, value, border=True)
    left,right = st.columns((3,1), gap="large")
    with left:
        st.subheader("Recommended for you")
        for company, role, salary, skills in (("Google","Senior Python Engineer","$150k–$190k",["Python","GCP","Kubernetes"]),("Microsoft","Cloud Platform Engineer","$145k–$180k",["Azure","Terraform","Docker"]),("OpenAI","Applied AI Engineer","$170k–$220k",["LLMs","Python","RAG"]),("Netflix","Backend Engineer","$140k–$185k",["Java","AWS","Distributed systems"])):
            with st.container(border=True):
                st.markdown(f"#### :material/business: {company} · {role}"); st.caption(f"Remote · {salary}")
                st.pills("Skills", skills, selection_mode="multi", key=f"candidate-{company}")
                st.button("View role", key=f"view-{company}", icon=":material/arrow_forward:")
    with right:
        with st.container(border=True):
            st.subheader("AI suggestions")
            for suggestion in ("Improve Docker experience","Add Kubernetes project","Strengthen resume summary","Complete an AWS certificate"):
                st.button(suggestion, key=suggestion, width="stretch", type="tertiary", icon=":material/auto_awesome:")
        with st.container(border=True):
            st.subheader("Next interview"); st.write("**Cloud platform engineer**"); st.caption("Tomorrow · 10:30 AM · Video call")
            st.button("Prepare with AI", width="stretch", type="primary", icon=":material/rocket_launch:")
