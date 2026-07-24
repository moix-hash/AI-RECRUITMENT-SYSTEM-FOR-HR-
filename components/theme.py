from __future__ import annotations

import html
from pathlib import Path
from typing import Optional

import streamlit as st


def apply_theme() -> None:
    if not st.session_state.get("_talentos_page_configured"):
        st.set_page_config(page_title="TalentOS | AI Recruitment", page_icon="✨", layout="wide", initial_sidebar_state="expanded")
        st.session_state["_talentos_page_configured"] = True
    css_path = Path(__file__).resolve().parents[1] / "styles" / "theme.css"
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def render_metric_card(title: str, value: str, delta: str = "", icon: str = "✦", trend: Optional[str] = None) -> None:
    title, value, delta = map(html.escape, (title, value, delta))
    st.markdown(f"""<div class="card"><div class="kpi-icon">{icon}</div><div class="muted" style="margin-top:.65rem">{title}</div><div class="kpi-value">{value}</div><div class="positive">↗ {delta} <span class="muted">{html.escape(trend or 'vs last month')}</span></div></div>""", unsafe_allow_html=True)
