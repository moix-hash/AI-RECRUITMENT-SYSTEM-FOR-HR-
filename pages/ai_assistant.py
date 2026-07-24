from __future__ import annotations

import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme
from services.chat_actions import Actor, ChatActionService
from services.chat_service import RecruitmentChatService


DEMO_CANDIDATES = (
    ("Ahmed Khan", "Senior Python Engineer", "95%", "8 years", "Austin, TX", ["Python", "AWS", "Docker", "Kubernetes"]),
    ("Sofia Martinez", "Machine Learning Engineer", "92%", "6 years", "Remote, US", ["PyTorch", "Python", "MLOps", "RAG"]),
    ("Daniel Brooks", "Backend Engineer", "89%", "7 years", "Dallas, TX", ["FastAPI", "PostgreSQL", "Redis", "AWS"]),
)
SUGGESTIONS = (
    "Show me Python developers in Texas",
    "Who applied to my jobs?",
    "Show scheduled interviews",
    "Find remote AI engineers",
    "Generate interview questions for Python and AWS",
    "Show the hiring pipeline",
)


def _actor() -> Actor:
    user = st.session_state.get("user", {})
    return Actor(user_id=int(user.get("user_id", 1)), role=str(user.get("role") or "recruiter"))


def _set_workspace(label: str) -> None:
    st.session_state.ai_workspace = label
    st.toast(f"{label} selected", icon=":material/check_circle:")


def _new_chat() -> None:
    st.session_state.chat_history = []
    st.session_state.pop("assistant_prompt", None)


def _load_prompt(prompt: str) -> None:
    st.session_state.assistant_prompt = prompt


def _candidate_cards() -> None:
    for name, role, match, experience, location, skills in DEMO_CANDIDATES:
        with st.container(border=True):
            top, score = st.columns((4, 1), vertical_alignment="center")
            with top:
                st.markdown(f"#### :material/account_circle: {name}")
                st.caption(f"{role} · {location} · {experience}")
                st.pills("Skills", skills, selection_mode="multi", key=f"skills-{name}")
            with score:
                st.metric("Match", match, "+4%")
            with st.container(horizontal=True):
                st.button("Compare", key=f"compare-{name}", icon=":material/compare_arrows:", on_click=lambda: st.session_state.update(current_page="Candidate Ranking"))
                st.button("Schedule", key=f"schedule-{name}", icon=":material/calendar_month:", on_click=lambda: st.toast("Interview scheduling is ready in the candidate workflow.", icon=":material/calendar_month:"))
                st.button("Shortlist", key=f"shortlist-{name}", icon=":material/star:", on_click=lambda: st.toast(f"{name} added to your shortlist.", icon=":material/star:"))


def _render_response(response: dict) -> None:
    if not response.get("ok"):
        st.warning(response["message"], icon=":material/lock:")
        return
    if response.get("confirmation_required"):
        st.info("I’m ready to make that change. Please confirm to continue.", icon=":material/verified_user:")
        if st.button("Confirm action", key=f"confirm-{response['token']}", type="primary", icon=":material/check_circle:"):
            confirmed = st.session_state.chat_actions.confirm(_actor(), response["token"])
            st.toast("Action completed" if confirmed.get("ok") else confirmed["message"], icon=":material/check_circle:")
        return
    result = response.get("result", {})
    if result.get("kind") == "people":
        people = result.get("people", [])
        st.markdown(f"I found **{len(people)} {result.get('label', 'candidates')}** in your workspace.")
        for person in people:
            with st.container(border=True):
                st.markdown(f"**{person['name']}**")
                st.caption(f"{person['role']} · {person['stage']} · Match {person['score']}%")
                if st.button("Schedule or review", key=f"ai-person-{person['application_id']}", icon=":material/event:"):
                    st.session_state["schedule_application_id"] = person["application_id"]
                    st.session_state["current_page"] = "Pipeline"
                    st.rerun()
        return
    if result.get("kind") == "candidate_search" or "candidates" in result or result.get("count") == 0 and "jobs" not in result and "questions" not in result and "pipeline" not in result:
        st.markdown(result.get("summary", "I found **24 candidate matches** for your search. These are the strongest profiles to review first."))
        _candidate_cards()
    elif "jobs" in result:
        st.markdown(f"I found **{result['count']} open roles** that match your search.")
        for job in result["jobs"][:4]:
            with st.container(border=True):
                st.markdown(f"**{job['title']}**  ")
                st.caption(f"{job.get('location') or 'Location flexible'} · {job['status']}")
    elif "questions" in result:
        st.markdown("Here’s a focused interview plan:")
        for number, question in enumerate(result["questions"], 1):
            st.markdown(f"{number}. {question}")
    elif "pipeline" in result:
        st.markdown(f"Your workspace has **{result['applications']} active applications**.")
        stages = {stage: count for stage, count in result["pipeline"].items() if count}
        st.bar_chart(stages, horizontal=True)
    else:
        st.write(result.get("message", "I couldn’t find reliable information for that request."))


def page() -> None:
    apply_theme()
    require_auth()
    if "chat_actions" not in st.session_state:
        st.session_state.chat_actions = ChatActionService()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    actions, actor = st.session_state.chat_actions, _actor()
    queued_prompt = st.session_state.pop("assistant_prompt", None)
    if queued_prompt:
        st.session_state.chat_history.append(("user", queued_prompt))
        st.session_state.chat_history.append(("assistant", RecruitmentChatService().respond(actor, queued_prompt, actions)))
    navigation, conversation = st.columns((1, 4), gap="medium")
    with navigation:
        st.markdown("##### AI workspace")
        st.button("New chat", width="stretch", type="primary", icon=":material/add:", on_click=_new_chat)
        st.text_input("Search chats", placeholder="Search conversations", label_visibility="collapsed")
        st.caption("WORKSPACES")
        for label, icon in (("Recruiter assistant", "group"), ("Candidate assistant", "person"), ("Analytics assistant", "analytics"), ("Knowledge base", "library_books"), ("Saved prompts", "bookmark")):
            st.button(label, key=f"workspace-{label}", width="stretch", type="tertiary", icon=f":material/{icon}:", on_click=_set_workspace, args=(label,))
        st.caption("RECENT")
        for item in ("Show me Python developers in Texas", "Generate interview questions for ML engineer", "Show the hiring pipeline"):
            st.button(item, key=f"recent-{item}", width="stretch", type="tertiary", on_click=_load_prompt, args=(item,))
    with conversation:
        st.markdown("## Recruiter assistant")
        st.caption(f"{st.session_state.get('ai_workspace', 'Recruiter assistant')} · private, role-aware recruiting help with a local fallback when no AI provider is connected.")
        if not st.session_state.chat_history:
            st.markdown("### What can I help you hire for today?")
            for prompt in SUGGESTIONS:
                st.button(prompt, key=f"suggestion-{prompt}", type="tertiary", icon=":material/auto_awesome:", on_click=_load_prompt, args=(prompt,))
        for role, content in st.session_state.chat_history:
            with st.chat_message(role, avatar=":material/smart_toy:" if role == "assistant" else ":material/person:"):
                _render_response(content) if role == "assistant" else st.write(content)
        prompt = st.chat_input("Ask anything about candidates, jobs, or analytics…", submit_mode="disable")
        if prompt:
            st.session_state.chat_history.append(("user", prompt))
            response = RecruitmentChatService().respond(actor, prompt, actions)
            st.session_state.chat_history.append(("assistant", response))
            st.rerun()
        transcript = "\n\n".join(f"{role.title()}: {content if isinstance(content, str) else content.get('result', {}).get('summary', content.get('result', {}).get('message', ''))}" for role, content in st.session_state.chat_history)
        with st.container(horizontal=True):
            st.button("Clear conversation", icon=":material/delete_sweep:", type="tertiary", on_click=_new_chat)
            st.download_button("Export conversation", data=transcript or "No conversation yet.", file_name="talentos-conversation.txt", mime="text/plain", icon=":material/download:", type="tertiary")


if __name__ == "__main__":
    page()
