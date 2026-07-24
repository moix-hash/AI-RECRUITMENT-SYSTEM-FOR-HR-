from __future__ import annotations

import pandas as pd
import streamlit as st


def _go_to(page: str) -> None:
    st.session_state.current_page = page


def _candidate(name: str, role: str, score: int, years: str, skills: list[str]) -> None:
    with st.container(border=True):
        summary, actions = st.columns((4, 1), vertical_alignment="center")
        with summary:
            st.markdown(f"#### :material/account_circle: {name}")
            st.caption(f"{role} · {years} experience")
            st.pills("Skills", skills, selection_mode="multi", key=f"dashboard-skills-{name}")
        with actions:
            st.metric("Match", f"{score}%", "+4%")
            st.button("Review", key=f"review-{name}", icon=":material/arrow_forward:", on_click=_go_to, args=("Candidate Ranking",))


def render_dashboard() -> None:
    st.markdown("<div class='muted'>RECRUITING / TODAY</div>", unsafe_allow_html=True)
    st.title("Today’s hiring overview")
    st.caption("See what needs attention, move candidates forward, and keep your team aligned.")
    with st.container(horizontal=True):
        for label, value, delta, trend in (
            ("Applications", "45", "+12%", [28, 31, 33, 39, 45]),
            ("Interviews", "17", "+3", [9, 11, 12, 14, 17]),
            ("Offers", "8", "+2", [3, 4, 5, 6, 8]),
            ("Hired", "2", "This week", [0, 0, 1, 1, 2]),
        ):
            st.metric(label, value, delta, border=True, chart_data=trend)
    left, right = st.columns((1.5, 1), gap="large")
    with left:
        with st.container(border=True):
            st.subheader("Hiring funnel")
            st.caption("Candidates progressing through your active roles")
            funnel = pd.DataFrame({"Stage": ["Applications", "Screening", "Interview", "Offer", "Hired"], "Candidates": [45, 31, 17, 8, 2]})
            st.bar_chart(funnel, x="Stage", y="Candidates", color="#818CF8")
    with right:
        with st.container(border=True):
            st.subheader("AI priorities")
            st.write("**3 strong candidates** are ready for recruiter review.")
            st.write("**2 roles** have a skill gap in Kubernetes and cloud security.")
            st.write("**1 interview** needs feedback before the next stage.")
            st.button("Open AI assistant", width="stretch", type="primary", icon=":material/smart_toy:", on_click=_go_to, args=("AI Assistant",))
    st.subheader("Continue working")
    with st.container(horizontal=True):
        for label, caption, icon, target in (
            ("Upload a resume", "Add a candidate to your pipeline", "upload_file", "Upload Resume"),
            ("Analyze a candidate", "Get a clear match score", "auto_awesome", "Upload Resume"),
            ("Compare finalists", "Review top candidates side by side", "compare_arrows", "Candidate Ranking"),
            ("View the pipeline", "Move candidates to the next stage", "account_tree", "Pipeline"),
        ):
            with st.container(border=True):
                st.markdown(f"#### :material/{icon}: {label}")
                st.caption(caption)
                st.button("Open", key=f"quick-{target}-{label}", width="stretch", on_click=_go_to, args=(target,))
    left, right = st.columns((1.35, 1), gap="large")
    with left:
        st.subheader("Latest candidates")
        _candidate("Ahmed Khan", "Senior Python Engineer", 95, "8 years", ["Python", "AWS", "Docker"])
        _candidate("Sofia Martinez", "Machine Learning Engineer", 92, "6 years", ["PyTorch", "MLOps", "RAG"])
        _candidate("Daniel Brooks", "Backend Engineer", 89, "7 years", ["FastAPI", "PostgreSQL", "Redis"])
    with right:
        with st.container(border=True):
            st.subheader("Hiring trend")
            trend = pd.DataFrame({"Week": ["W1", "W2", "W3", "W4", "W5", "W6"], "Qualified candidates": [18, 23, 21, 28, 31, 37]})
            st.line_chart(trend, x="Week", y="Qualified candidates", color="#34D399")
        with st.container(border=True):
            st.subheader("Salary signal")
            st.write("Senior Python engineers in your target markets are trending around **$150k–$180k**.")
            st.button("Explore market insights", width="stretch", type="tertiary", on_click=_go_to, args=("Analytics",))
