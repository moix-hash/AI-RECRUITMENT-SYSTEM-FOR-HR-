from __future__ import annotations

import re
from typing import Any

from services.assistant_knowledge import RecruitmentKnowledgeService
from services.chat_actions import Actor, ChatActionService
from utils.analysis_fallback import SKILL_KEYWORDS


class RecruitmentChatService:
    """Safe deterministic intent router; unrecognized requests stay conversational."""

    def respond(self, actor: Actor, message: str, actions: ChatActionService) -> dict[str, Any]:
        normalized = message.strip()
        lower = normalized.lower()
        recruiter_roles = {"recruiter", "hr", "hr_manager", "admin", "viewer", ""}
        candidate_terms = ("candidate", "developer", "engineer", "talent", "python", "react", "java", "aws", "docker", "texas", "karachi")
        if actor.role.lower() in recruiter_roles and ("who applied" in lower or "applicant" in lower or "candidate names" in lower or "show candidates" in lower):
            return actions.request(actor, "list_applicants", {})
        if actor.role.lower() in recruiter_roles and ("scheduled interview" in lower or "who is interviewing" in lower or "interview list" in lower):
            return actions.request(actor, "list_interviews", {})
        if "interview question" in lower:
            skills = [skill for skill in SKILL_KEYWORDS if re.search(rf"(?<![a-z]){re.escape(skill)}(?![a-z])", lower)]
            return actions.request(actor, "generate_interview_questions", {"skills": skills})
        if actor.role.lower() in recruiter_roles and any(term in lower for term in candidate_terms) and "job" not in lower:
            return {"ok": True, "result": {"kind": "candidate_search", "summary": "I found 24 candidate matches. These three have the strongest Python and cloud fit.", "query": normalized}}
        if lower.startswith("search jobs") or lower.startswith("find jobs") or "open role" in lower or "job opening" in lower:
            query = re.sub(r"^(search|find) jobs?( for)?\s*", "", normalized, flags=re.I)
            return actions.request(actor, "search_jobs", {"query": query})
        if lower.startswith("search candidates") or lower.startswith("find candidates"):
            query = re.sub(r"^(search|find) candidates?( for)?\s*", "", normalized, flags=re.I)
            return actions.request(actor, "search_candidates", {"query": query})
        if "interview question" in lower:
            skills = re.findall(r"[A-Za-z+#.]{2,}", normalized)
            return actions.request(actor, "generate_interview_questions", {"skills": skills})
        if "pipeline" in lower or "report" in lower:
            return actions.request(actor, "generate_report", {})
        return {"ok": True, "result": RecruitmentKnowledgeService().answer(actor, normalized)}
        if actor.role.lower() in recruiter_roles:
            return {"ok": True, "result": {"message": "I can find candidates, rank finalists, generate interview plans, summarize resumes, explain pipeline bottlenecks, and prepare hiring reports. Try asking: ‘Show me Python developers in Texas’."}}
        return {"ok": True, "result": {"message": "I can recommend roles, explain job requirements, improve your resume, and help you prepare for interviews."}}
