from __future__ import annotations

from utils.analysis_fallback import build_fallback_analysis


def test_build_fallback_analysis_produces_reasonable_scores() -> None:
    result = build_fallback_analysis(
        resume_text="Python, SQL, LangChain, AWS, leadership",
        job_description="Python, SQL, LangChain, cloud, mentoring",
    )

    assert result["final_score"] >= 0
    assert result["final_score"] <= 100
    assert result["recommendation"] in {"Strong Hire", "Hire", "Interview", "Hold", "Reject"}
    assert len(result["matching_skills"]) >= 1
    assert result["analysis_mode"] == "Local skill-based fallback"
    assert result["experience_summary"]
    assert result["education_summary"]
    assert result["project_summary"]
    assert result["justification"]


def test_fallback_analysis_returns_role_specific_skill_differences() -> None:
    result = build_fallback_analysis(
        resume_text="8 years Python SQL AWS Docker. Built data pipelines for analytics.",
        job_description="Senior data engineer needs Python SQL Airflow dbt and BigQuery.",
    )

    assert "python" in result["matching_skills"]
    assert "airflow" not in result["matching_skills"]
    assert result["missing_skills"]
