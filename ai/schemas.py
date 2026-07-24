from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class CandidateAnalysis(BaseModel):
    candidate_name: str = Field(default="Not Found")
    email: str = Field(default="Not Found")
    phone: str = Field(default="Not Found")
    linkedin: str = Field(default="Not Found")
    github: str = Field(default="Not Found")
    portfolio: str = Field(default="Not Found")
    professional_summary: str = Field(default="Not Found")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    matching_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    extra_skills: List[str] = Field(default_factory=list)
    experience_analysis: str = Field(default="Not Found")
    education_analysis: str = Field(default="Not Found")
    project_analysis: str = Field(default="Not Found")
    certification_analysis: str = Field(default="Not Found")
    leadership_assessment: str = Field(default="Not Found")
    communication_assessment: str = Field(default="Not Found")
    learning_ability: str = Field(default="Not Found")
    risk_assessment: str = Field(default="Not Found")
    overall_candidate_evaluation: str = Field(default="Not Found")
    confidence_score: str = Field(default="Medium", description="Low, Medium, or High")
    confidence_explanation: str = Field(default="Not Found")
    technical_skills: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    programming_languages: List[str] = Field(default_factory=list)
    cloud_platforms: List[str] = Field(default_factory=list)
    databases: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)
    skill_match: int = Field(default=0, ge=0, le=100)
    experience_match: int = Field(default=0, ge=0, le=100)
    education_match: int = Field(default=0, ge=0, le=100)
    project_match: int = Field(default=0, ge=0, le=100)
    certification_match: int = Field(default=0, ge=0, le=100)
    soft_skill_match: int = Field(default=0, ge=0, le=100)
    overall_match: int = Field(default=0, ge=0, le=100)
    final_score: int = Field(default=0, ge=0, le=100)
    recommendation: str = Field(
        default="Interview",
        description="Strong Hire, Hire, Interview, Hold, or Reject",
    )
    recommendation_justification: str = Field(default="Not Found")
    interview_focus: str = Field(default="Not Found")
    interview_questions: List[str] = Field(default_factory=list)


class ParsedResume(BaseModel):
    candidate_name: str = Field(default="Not Found")
    email: str = Field(default="Not Found")
    phone: str = Field(default="Not Found")
    linkedin: str = Field(default="Not Found")
    github: str = Field(default="Not Found")
    portfolio: str = Field(default="Not Found")
    education: str = Field(default="Not Found")
    university: str = Field(default="Not Found")
    degree: str = Field(default="Not Found")
    graduation_year: str = Field(default="Not Found")
    experience_summary: str = Field(default="Not Found")
    companies: str = Field(default="Not Found")
    roles: str = Field(default="Not Found")
    duration: str = Field(default="Not Found")
    projects: str = Field(default="Not Found")
    technical_skills: str = Field(default="Not Found")
    soft_skills: str = Field(default="Not Found")
    frameworks: str = Field(default="Not Found")
    programming_languages: str = Field(default="Not Found")
    cloud_platforms: str = Field(default="Not Found")
    databases: str = Field(default="Not Found")
    certifications: str = Field(default="Not Found")
    achievements: str = Field(default="Not Found")
    languages: str = Field(default="Not Found")
    publications: str = Field(default="Not Found")
    volunteer_work: str = Field(default="Not Found")


class ParsedJobDescription(BaseModel):
    job_title: str = Field(default="Not Found")
    department: str = Field(default="Not Found")
    experience_required: str = Field(default="Not Found")
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    education: str = Field(default="Not Found")
    responsibilities: str = Field(default="Not Found")
    tools: List[str] = Field(default_factory=list)
    frameworks: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)


class CandidateComparison(BaseModel):
    overall_best_candidate: str = Field(default="Not Found")
    comparison_summary: str = Field(default="Not Found")
    advantages: List[str] = Field(default_factory=list)
    disadvantages: List[str] = Field(default_factory=list)
    skill_differences: List[str] = Field(default_factory=list)
    experience_differences: List[str] = Field(default_factory=list)
    education_differences: List[str] = Field(default_factory=list)
    project_differences: List[str] = Field(default_factory=list)
    recommendation: str = Field(default="Interview")


class CandidateRankingResult(BaseModel):
    ranked_candidates: List[dict] = Field(default_factory=list)
    ranking_summary: str = Field(default="Not Found")
