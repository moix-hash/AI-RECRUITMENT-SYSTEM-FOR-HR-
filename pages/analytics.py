from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from app.auth import require_auth
from components.theme import apply_theme, render_metric_card


def _style(fig):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=25, b=10), font=dict(color="#cbd5e1"))
    return fig


def page() -> None:
    apply_theme()
    require_auth()
    st.markdown("<div class='muted'>WORKSPACE / INSIGHTS</div><h1 style='margin:.2rem 0'>Hiring analytics</h1><div class='muted'>Decision-ready insights across your recruitment pipeline.</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, metric in zip((c1,c2,c3,c4), [("Average score", "84%", "+7.2%", "◎"), ("Strong hire rate", "27%", "+4.1%", "✦"), ("Interview rate", "41%", "+5.6%", "↗"), ("Time to screen", "2.4d", "-18%", "◷")]):
        with col: render_metric_card(*metric)
    st.write("")
    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("<div class='section-title'>Hiring funnel</div><div class='muted'>Conversion through the selection journey</div>", unsafe_allow_html=True)
        funnel = pd.DataFrame({"Stage":["Uploaded","Screened","Interview","Offer","Hired"], "Candidates":[128,87,53,21,14]})
        st.plotly_chart(_style(px.funnel(funnel, x="Candidates", y="Stage", color="Stage", color_discrete_sequence=["#818cf8", "#22d3ee", "#38bdf8", "#fbbf24", "#34d399"])), use_container_width=True, config={"displayModeBar":False})
    with right:
        st.markdown("<div class='section-title'>Experience distribution</div><div class='muted'>Years of relevant experience</div>", unsafe_allow_html=True)
        exp = pd.DataFrame({"Band":["0–2 years","3–5 years","6–8 years","9+ years"], "Candidates":[22,49,34,23]})
        st.plotly_chart(_style(px.bar(exp, x="Band", y="Candidates", color="Band", color_discrete_sequence=["#818cf8", "#6366f1", "#38bdf8", "#22d3ee"])), use_container_width=True, config={"displayModeBar":False})
    left, right = st.columns((1.2, 1), gap="large")
    with left:
        st.markdown("<div class='section-title'>Top skills</div><div class='muted'>Most frequent capabilities in the talent pool</div>", unsafe_allow_html=True)
        skills = pd.DataFrame({"Skill":["Python","SQL","AWS","React","Docker","Figma"],"Candidates":[78,65,54,43,37,31]})
        st.plotly_chart(_style(px.bar(skills, x="Candidates", y="Skill", orientation="h", color_discrete_sequence=["#818cf8"])), use_container_width=True, config={"displayModeBar":False})
    with right:
        st.markdown("<div class='section-title'>Score quality</div><div class='muted'>Recommendation mix</div>", unsafe_allow_html=True)
        recommendation = pd.DataFrame({"Recommendation":["Strong hire","Interview","Review","Reject"],"Value":[27,41,20,12]})
        st.plotly_chart(_style(px.pie(recommendation, names="Recommendation", values="Value", hole=.65, color="Recommendation", color_discrete_sequence=["#34d399", "#22d3ee", "#fbbf24", "#fb7185"])), use_container_width=True, config={"displayModeBar":False})


if __name__ == "__main__":
    page()
