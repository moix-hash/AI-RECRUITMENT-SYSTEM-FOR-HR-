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
