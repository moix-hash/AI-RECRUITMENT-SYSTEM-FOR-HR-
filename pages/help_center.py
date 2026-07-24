from __future__ import annotations
import streamlit as st
from app.auth import require_auth
from components.theme import apply_theme


TOPICS = {
    "Getting started": "Create an open role in Upload JD, upload candidate CVs, then review applicants in Pipeline.",
    "Candidate intelligence": "Candidate Ranking compares each CV with the best fitting open role and displays recognised job skills.",
    "Jobs & pipeline": "Create and edit roles in Jobs. Use Pipeline to move candidates and schedule interviews.",
    "AI assistant": "Ask ‘Who applied to my jobs?’ or ‘Show scheduled interviews’ to see real workspace candidates.",
    "Security & privacy": "Recruiting actions require the appropriate role permissions and are recorded in activity history.",
    "Developer resources": "Integration settings are managed from the protected Settings workspace.",
}

def page() -> None:
    apply_theme(); require_auth()
    st.markdown("<div class='muted'>SUPPORT / HELP CENTER</div>", unsafe_allow_html=True); st.title("How can we help?")
    selected = st.session_state.get("help_topic")
    if selected:
        with st.container(border=True):
            st.subheader(selected)
            st.write(TOPICS[selected])
            if selected == "Jobs & pipeline" and st.button("Open pipeline", type="primary", icon=":material/account_tree:"):
                st.session_state.current_page = "Pipeline"; st.rerun()
            if selected == "AI assistant" and st.button("Ask TalentOS AI", type="primary", icon=":material/smart_toy:"):
                st.session_state.assistant_prompt = "Who applied to my jobs?"; st.session_state.current_page = "AI Assistant"; st.rerun()
            if st.button("Back to help topics", icon=":material/arrow_back:"):
                st.session_state.pop("help_topic", None); st.rerun()
        return
    st.text_input("Search help", placeholder="Search guides, FAQs, and release notes", icon=":material/search:")
    topics = (("Getting started","Set up your workspace and invite your team","rocket_launch"),("Candidate intelligence","Understand match scores and recommendations","person_search"),("Jobs & pipeline","Publish roles and manage applicants","account_tree"),("AI assistant","Use natural-language recruiting workflows","smart_toy"),("Security & privacy","Sessions, permissions, and data controls","shield"),("Developer resources","API guidance and integration status","code"))
    for col, group in zip(st.columns(3), (topics[:2],topics[2:4],topics[4:])):
        with col:
            for title, description, icon in group:
                with st.container(border=True):
                    st.markdown(f"#### :material/{icon}: {title}"); st.caption(description)
                    if st.button("Explore",key=f"help-{title}",type="tertiary"):
                        st.session_state.help_topic = title; st.rerun()
    st.subheader("Popular answers")
    for question in ("How do match scores work?","How do I prepare an interview?","How do I export a hiring report?","How do I manage team access?"):
        with st.expander(question): st.write("Our guided workflows keep the next action close to the relevant candidate, role, or report. Ask the AI assistant for step-by-step help.")
    with st.container(horizontal=True):
        if st.button("Ask AI support", type="primary", icon=":material/support_agent:"):
            st.session_state.assistant_prompt = "Help me use the recruiting workspace"; st.session_state.current_page = "AI Assistant"; st.rerun()
        if st.button("Raise a ticket", icon=":material/add_comment:"):
            st.session_state.help_topic = "Getting started"; st.rerun()
        if st.button("System status", type="tertiary", icon=":material/monitoring:"):
            st.info("TalentOS local services are available. Refresh with Ctrl + F5 if a page appears stale.")
