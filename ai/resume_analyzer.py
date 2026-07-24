from __future__ import annotations

from typing import Any, Dict

from ai.chains import AnalysisChain
from ai.interview_generator import generate_interview_questions
from ai.recommendation_engine import determine_recommendation, explain_recommendation
from ai.schemas import CandidateAnalysis
from ai.skill_matcher import match_skills


class ResumeAnalyzer:
    def __init__(self) -> None:
        self.chain = AnalysisChain()

    def analyze(self, resume_text: str, job_description: str) -> CandidateAnalysis:
        return self.chain.run_analysis(resume_text, job_description)

    def summarize(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        analysis = self.analyze(resume_text, job_description)
        matching, missing, extra = match_skills(
            analysis.technical_skills + analysis.frameworks + analysis.programming_languages,
            analysis.matching_skills,
        )
        recommendation = determine_recommendation({"final_score": analysis.final_score})
        explanation = explain_recommendation(
            {"final_score": analysis.final_score}, analysis.strengths, missing
        )
        questions = generate_interview_questions(matching, recommendation)
        return {
            "analysis": analysis,
            "recommendation": recommendation,
            "explanation": explanation,
            "questions": questions,
            "matching_skills": matching,
            "missing_skills": missing,
            "extra_skills": extra,
        }
