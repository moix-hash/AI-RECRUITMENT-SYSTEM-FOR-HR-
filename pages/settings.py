from __future__ import annotations
import json
import streamlit as st
from app.auth import require_auth
from components.theme import apply_theme

def page() -> None:
    apply_theme(); require_auth()
    st.markdown("<div class='muted'>WORKSPACE / PREFERENCES</div>", unsafe_allow_html=True); st.title("Settings")
    tabs = st.tabs(["Profile","Appearance","Notifications","AI & integrations","Security","Data & billing"])
    with tabs[0]:
        with st.container(border=True):
            st.subheader("Profile"); name = st.text_input("Display name",value=st.session_state.get("user", {}).get("username", "Recruiter")); st.text_input("Work email",value="hr@example.com"); st.text_input("Role",value="HR / Recruiter",disabled=True)
            if st.button("Save profile",type="primary",icon=":material/save:"):
                st.session_state.user["username"] = name.strip() or "Recruiter"; st.toast("Profile saved.", icon=":material/check_circle:")
    with tabs[1]:
        with st.container(border=True):
            st.subheader("Appearance"); st.segmented_control("Theme",["System","Dark","Light"],default="Dark"); st.segmented_control("Accent",["Indigo","Teal","Rose"],default="Indigo"); st.toggle("Reduce motion"); st.toggle("High contrast")
    with tabs[2]:
        with st.container(border=True):
            st.subheader("Notifications"); st.toggle("Candidate activity",value=True); st.toggle("Interview reminders",value=True); st.toggle("Weekly hiring summary",value=True); st.toggle("Product updates")
    with tabs[3]:
        with st.container(border=True):
            st.subheader("AI & integrations"); st.write("Provider credentials stay protected in environment configuration."); st.badge("Gemini connected",icon=":material/check_circle:",color="green"); st.badge("Calendar ready",icon=":material/calendar_month:",color="blue")
            if st.button("Manage integrations",icon=":material/hub:"): st.info("Gemini and calendar status are managed securely through this workspace configuration.")
    with tabs[4]:
        with st.container(border=True):
            st.subheader("Security")
            if st.button("Manage sessions",icon=":material/devices:"): st.info("This browser is the active session. Use Sign out to end it safely.")
            if st.button("Review audit activity",icon=":material/history:"): st.session_state.current_page = "History"; st.rerun()
            if st.button("Change password",icon=":material/password:"): st.info("Password changes are managed by your workspace administrator in this local demo.")
    with tabs[5]:
        with st.container(border=True):
            st.subheader("Data & billing"); st.button("Export workspace data",icon=":material/download:"); st.button("Create backup",icon=":material/backup:"); st.write("**Professional plan** · Renewal on 01 Sep 2026")
