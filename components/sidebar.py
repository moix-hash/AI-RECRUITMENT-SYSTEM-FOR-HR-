from __future__ import annotations

import streamlit as st


NAVIGATION = (
    ("Dashboard", "dashboard"), ("AI Assistant", "smart_toy"), ("Jobs", "work"),
    ("Pipeline", "account_tree"), ("Candidate Ranking", "person_search"), ("Analytics", "analytics"),
    ("Upload Resume", "upload_file"), ("Upload JD", "description"),
)
WORKSPACE = (("History", "history"), ("Profile", "account_circle"), ("Settings", "settings"), ("Help", "help"))


def render_sidebar() -> None:
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"
    with st.sidebar:
        st.markdown("## TalentOS")
        st.caption("AI recruiting workspace")
        st.button("Ask TalentOS AI", key="ai-launcher", width="stretch", type="primary", icon=":material/smart_toy:", on_click=lambda: st.session_state.update(current_page="AI Assistant"))
        st.caption("WORKSPACE")
        for label, icon in NAVIGATION:
            kind = "secondary" if st.session_state.current_page == label else "tertiary"
            st.button(label, key=f"nav-{label}", width="stretch", type=kind, icon=f":material/{icon}:", on_click=lambda page=label: st.session_state.update(current_page=page))
        st.caption("ACCOUNT")
        for label, icon in WORKSPACE:
            kind = "secondary" if st.session_state.current_page == label else "tertiary"
            st.button(label, key=f"nav-{label}", width="stretch", type=kind, icon=f":material/{icon}:", on_click=lambda page=label: st.session_state.update(current_page=page))
        st.space("small")
        st.button("Sign out", width="stretch", type="tertiary", icon=":material/logout:", on_click=lambda: [st.session_state.pop("authenticated", None), st.session_state.pop("user", None)])
