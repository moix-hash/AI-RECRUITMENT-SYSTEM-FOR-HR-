from ai.chains import build_analysis_chain
from ai.skill_matcher import match_skills
from ai.recommendation_engine import determine_recommendation


def test_analysis_chain_builder_is_callable() -> None:
    chain = build_analysis_chain()
    assert hasattr(chain, "invoke")


def test_skill_matching_handles_synonyms_and_taxonomy() -> None:
    matching, missing, extra = match_skills(
        ["TensorFlow", "React", "AWS"],
        ["Deep Learning", "Frontend", "Cloud"],
    )
    assert "deep learning" in matching
    assert "frontend" in matching
    assert "cloud" in matching
    assert missing == []
    assert extra == []


def test_recommendation_thresholds_are_deterministic() -> None:
    assert determine_recommendation({"final_score": 90}) == "Strong Hire"
    assert determine_recommendation({"final_score": 70}) == "Hire"
    assert determine_recommendation({"final_score": 55}) == "Interview"
