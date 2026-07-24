from __future__ import annotations

import streamlit as st

from app.auth import authenticate, register_user
from app_logging.app_logger import AppLogger
from components.theme import apply_theme
from database.models import init_db

init_db()
logger = AppLogger("auth").get_logger()


def login_page() -> None:
    apply_theme()
    hero, access = st.columns((1.15, 1), gap="large")
    with hero:
        st.markdown("<div class='muted'>TALENTOS / AI RECRUITING</div>", unsafe_allow_html=True)
        st.title("Hire with clarity, not guesswork.")
        st.write("A focused workspace for finding exceptional candidates, creating confident shortlists, and moving every hiring decision forward.")
        with st.container(border=True):
            st.metric("Candidate decisions made faster", "42%", "+12% this quarter", chart_data=[21, 26, 31, 36, 42])
            st.caption("Trusted by recruiting teams building thoughtful, high-performing organizations.")
        st.markdown(":green-badge[AI-powered matching] :blue-badge[Secure workspace] :violet-badge[Human-first hiring]")
    with access:
        with st.container(border=True):
            st.subheader("Welcome back")
            st.caption("Sign in to continue to your hiring workspace.")
            login, signup = st.tabs(["Sign in", "Create account"])
            with login:
                with st.form("login_form"):
                    username = st.text_input("Username", placeholder="Enter your username", icon=":material/person:")
                    password = st.text_input("Password", type="password", placeholder="Enter your password", icon=":material/lock:")
                    remember = st.checkbox("Keep me signed in")
                    submitted = st.form_submit_button("Sign in", width="stretch", type="primary", icon=":material/login:")
                if submitted:
                    try:
                        user = authenticate(username, password)
                        if user:
                            logger.info("Successful login for %s", username)
                            st.session_state.authenticated = True
                            st.session_state.user = {"user_id": user.id, "username": user.username, "role": user.role}
                            if remember: st.session_state.remember_me = True
                            st.rerun()
                        else:
                            st.error("Check your username and password, then try again.")
                    except Exception as exc:
                        logger.exception("Login error: %s", exc); st.error("We couldn’t sign you in. Please try again.")
            with signup:
                with st.form("signup_form"):
                    username = st.text_input("Your name", key="signup_username", icon=":material/person:")
                    email = st.text_input("Work email", key="signup_email", icon=":material/mail:")
                    password = st.text_input("Create password", type="password", key="signup_password", icon=":material/lock:")
                    account_type = st.segmented_control("I want to", ["Hire candidates", "Find a job"], default="Hire candidates")
                    st.caption("Use 8+ characters with uppercase, lowercase, a number, and a special character. Your workspace role can be adjusted by an administrator after signup.")
                    created = st.form_submit_button("Create workspace account", width="stretch", type="primary", icon=":material/arrow_forward:")
                if created:
                    try:
                        user = register_user(username, email, password, "candidate" if account_type == "Find a job" else "recruiter")
                        logger.info("New workspace account created for %s", username)
                        st.session_state.authenticated = True
                        st.session_state.user = {"user_id": user.id, "username": user.username, "role": user.role}
                        st.toast("Your account is ready. Welcome to TalentOS!", icon=":material/check_circle:")
                        st.rerun()
                    except ValueError as exc: st.error(str(exc))
                    except Exception as exc:
                        logger.exception("Signup error: %s", exc); st.error("We couldn’t create your account. Please try again.")
