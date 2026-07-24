from __future__ import annotations

from datetime import date, time
from pathlib import Path

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from services.ats_service import ATSService, PIPELINE_STAGES


BOARD_STAGES = ("Applied", "AI Screening", "Recruiter Review", "Phone Screening")


def _candidate_name(filename: str) -> str:
    return Path(filename).stem.replace("demo_", "").replace("_cv", "").replace("_", " ").title()


def _schedule_panel(service: ATSService, user_id: int, applications) -> None:
    application_id = st.session_state.get("schedule_application_id")
    item = next((candidate for candidate in applications if candidate.id == application_id), None)
    if not item:
        return
    st.subheader(f"Schedule interview — {_candidate_name(item.resume.filename)}")
    with st.form(f"schedule-{item.id}", border=True):
        interview_date = st.date_input("Interview date", value=date.today())
        interview_time = st.time_input("Interview time", value=time(10, 0))
        meeting_link = st.text_input("Meeting link (optional)", placeholder="Zoom, Google Meet, or Teams link")
        confirm = st.form_submit_button("Schedule interview", type="primary", icon=":material/event_available:")
        cancel = st.form_submit_button("Cancel")
    if cancel:
        st.session_state.pop("schedule_application_id", None)
        st.rerun()
    if confirm:
        service.schedule_interview(user_id, item.id, f"{interview_date.isoformat()} at {interview_time.strftime('%H:%M')}", meeting_link.strip())
        st.session_state.pop("schedule_application_id", None)
        st.toast("Interview scheduled and recorded.", icon=":material/event_available:")
        st.rerun()


def _candidate_card(service: ATSService, user_id: int, item) -> None:
    with st.container(border=True):
        st.markdown(f"**{_candidate_name(item.resume.filename)}**")
        st.caption(f"{item.job.title} · {item.recommendation or 'Review'}")
        st.metric("Match", f"{item.match_score}%")
        with st.container(horizontal=True):
            index = PIPELINE_STAGES.index(item.stage)
            if index < len(PIPELINE_STAGES) - 1 and st.button("Advance", key=f"advance-{item.id}", icon=":material/arrow_forward:"):
                service.move_application(user_id, item.id, PIPELINE_STAGES[index + 1])
                st.rerun()
            if st.button("Schedule", key=f"schedule-{item.id}", icon=":material/event:"):
                st.session_state["schedule_application_id"] = item.id
                st.rerun()


def page() -> None:
    apply_theme()
    require_auth()
    user_id = int(st.session_state.get("user", {}).get("user_id", 1))
    service = ATSService()
    seeded = service.seed_demo_applications(user_id)
    company = service.default_company_for(user_id)
    applications = service.list_applications(company.id)
    st.markdown("<div class='muted'>ATS / PIPELINE</div>", unsafe_allow_html=True)
    st.title("Candidate pipeline")
    st.caption("Review candidates, move them through each stage, and schedule interviews from one workspace.")
    with st.container(horizontal=True):
        st.button("Add candidate CV", icon=":material/upload_file:", type="primary", on_click=lambda: st.session_state.update(current_page="Upload Resume"))
        st.button("View candidate ranking", icon=":material/person_search:", on_click=lambda: st.session_state.update(current_page="Candidate Ranking"))
    _schedule_panel(service, user_id, applications)
    grouped = {stage: [item for item in applications if item.stage == stage] for stage in BOARD_STAGES}
    for column, stage in zip(st.columns(4), BOARD_STAGES):
        with column:
            st.subheader(stage)
            st.caption(f"{len(grouped[stage])} candidates")
            for item in grouped[stage]:
                _candidate_card(service, user_id, item)
            if not grouped[stage]:
                st.caption("No candidates in this stage yet.")
    later = [item for item in applications if item.stage not in BOARD_STAGES]
    if later:
        with st.expander(f"Later stages ({len(later)})"):
            for item in later:
                st.write(f"{_candidate_name(item.resume.filename)} — {item.stage} — {item.job.title}")
    if seeded:
        st.toast(f"Added {seeded} demo candidates to your pipeline.", icon=":material/group_add:")


if __name__ == "__main__":
    page()
