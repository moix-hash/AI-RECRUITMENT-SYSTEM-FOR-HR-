from __future__ import annotations

from typing import List, Tuple

SKILL_SYNONYMS = {
    "deep learning": ["tensorflow", "keras", "tf", "pytorch", "neural networks"],
    "frontend": ["react", "reactjs", "javascript", "html", "css", "angular", "vue"],
    "backend": ["node.js", "node", "nodejs", "express", "django", "flask", "java", "spring"],
    "devops": ["docker", "kubernetes", "container", "containers", "ci/cd", "terraform"],
    "cloud": ["aws", "azure", "gcp", "amazon web services", "cloud platforms"],
    "programming": ["python", "py", "scala", "go", "rust", "cpp", "c#"],
    "database": ["sql", "postgres", "mysql", "mongodb", "redis", "oracle"],
    "leadership": ["mentoring", "manager", "team lead", "technical lead"],
    "communication": ["stakeholder management", "presentation", "cross functional"],
}


def normalize_skill(skill: str) -> str:
    if not skill:
        return ""
    raw = skill.strip().lower().replace("-", " ")
    raw = " ".join(raw.split())
    for canonical, aliases in SKILL_SYNONYMS.items():
        if raw == canonical or raw in aliases:
            return canonical
    return raw


def match_skills(resume_skills: List[str], job_skills: List[str]) -> Tuple[List[str], List[str], List[str]]:
    normalized_resume = {normalize_skill(skill) for skill in resume_skills if skill}
    normalized_job = {normalize_skill(skill) for skill in job_skills if skill}

    matching = sorted(normalized_resume & normalized_job)
    missing = sorted(normalized_job - normalized_resume)
    extra = sorted(normalized_resume - normalized_job)
    return matching, missing, extra
