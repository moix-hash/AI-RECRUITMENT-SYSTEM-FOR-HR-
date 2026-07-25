from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Streamlit Community Cloud executes an entry point from its containing folder.
# Add the repository root so package imports work for both `app/main.py` Cloud
# deployments and local runs from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.auth import require_auth
from app.login import login_page
from components.sidebar import render_sidebar
from components.dashboard import render_dashboard
from components.theme import apply_theme
from database.models import init_db


init_db()


def main() -> None:
    apply_theme()
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        login_page()
        return

    require_auth()
    render_sidebar()
    selection = st.session_state.get("current_page", "Dashboard")
    routes = {
        "AI Assistant": "pages.ai_assistant",
        "Upload Resume": "pages.upload_resume",
        "Upload JD": "pages.upload_job_description",
        "Candidate Ranking": "pages.candidate_ranking",
        "Analytics": "pages.analytics",
        "History": "pages.candidate_history",
        "Settings": "pages.settings",
        "Profile": "pages.profile",
        "Help": "pages.help_center",
        "Jobs": "pages.job_portal",
        "Pipeline": "pages.pipeline",
    }
    if selection == "Dashboard":
        render_dashboard()
    elif selection == "Logout":
        st.session_state.pop("authenticated", None)
        st.session_state.pop("user", None)
        st.rerun()
    elif selection in routes:
        module = __import__(routes[selection], fromlist=["page"])
        module.page()
    else:
        st.info("This workspace area is being prepared. Choose Dashboard or Jobs to continue.")


if __name__ == "__main__":
    main()
