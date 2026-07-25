from __future__ import annotations

import re
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI

from config.settings import GEMINI_API_KEY, GEMINI_MODEL, LLM_TEMPERATURE
from database.models import Application, Job, Resume, SessionLocal
from services.chat_actions import Actor


@dataclass(frozen=True)
class KnowledgeDocument:
    title: str
    text: str


class RecruitmentKnowledgeService:
    """Use Gemini when available, otherwise answer from retrieved workspace evidence."""

    def answer(self, actor: Actor, question: str) -> dict[str, object]:
        documents = self._retrieve(actor, question)
        if GEMINI_API_KEY:
            try:
                return {
                    "kind": "knowledge",
                    "message": self._gemini_answer(question, documents),
                    "source": "Gemini with workspace retrieval",
                    "sources": [document.title for document in documents],
                }
            except Exception:
                pass
        return {
            "kind": "knowledge",
            "message": self._local_answer(question, documents),
            "source": "Local workspace retrieval",
            "sources": [document.title for document in documents],
        }

    def _retrieve(self, actor: Actor, question: str) -> list[KnowledgeDocument]:
        recruiter_roles = {"recruiter", "hr", "hr_manager", "admin", "viewer", ""}
        documents: list[KnowledgeDocument] = []
        with SessionLocal() as session:
            for job in session.query(Job).filter(Job.status == "Open").all():
                documents.append(KnowledgeDocument(
                    f"Open role: {job.title}",
                    " ".join(part for part in (job.title, job.company, job.location, job.required_skills, job.preferred_skills, job.responsibilities) if part),
                ))
            if actor.role.lower() in recruiter_roles:
                for resume in session.query(Resume).filter(Resume.user_id == actor.user_id).all():
                    documents.append(KnowledgeDocument(f"Candidate CV: {resume.filename}", (resume.text_content or "")[:4000]))
                for application in session.query(Application).all():
                    documents.append(KnowledgeDocument(
                        f"Application {application.id}",
                        f"Stage: {application.stage}. Match score: {application.match_score}. Notes: {application.notes or ''}",
                    ))
        terms = self._terms(question)
        ranked = sorted(documents, key=lambda doc: len(terms & self._terms(doc.text)), reverse=True)
        return [document for document in ranked if terms & self._terms(document.text)][:4]

    @staticmethod
    def _terms(text: str) -> set[str]:
        return {
            token.lower() for token in re.findall(r"[A-Za-z0-9+#.]{2,}", text)
            if token.lower() not in {"the", "and", "for", "with", "that", "this", "about", "what", "are", "can", "you", "how"}
        }

    @staticmethod
    def _gemini_answer(question: str, documents: list[KnowledgeDocument]) -> str:
        context = "\n\n".join(f"{doc.title}:\n{doc.text[:1800]}" for doc in documents) or "No matching workspace records were found."
        prompt = (
            "You are TalentOS, a helpful recruitment assistant. Answer naturally and clearly. "
            "Use workspace context when relevant. Do not invent candidate facts or hiring decisions. "
            "If context is missing, say so and offer general recruiting guidance.\n\n"
            f"Workspace context:\n{context}\n\nUser question: {question}"
        )
        response = ChatGoogleGenerativeAI(
            model=GEMINI_MODEL,
            google_api_key=GEMINI_API_KEY,
            temperature=LLM_TEMPERATURE,
        ).invoke(prompt)
        return str(response.content).strip()

    @staticmethod
    def _local_answer(question: str, documents: list[KnowledgeDocument]) -> str:
        if documents:
            evidence = "\n".join(f"- **{doc.title}**: {doc.text[:300].strip()}" for doc in documents)
            return f"I searched your uploaded CVs, open roles, and hiring records. Here is the most relevant information:\n\n{evidence}"
        lower = question.lower()
        if "resume" in lower or "cv" in lower:
            return "For a stronger CV, lead with the target role, show measurable outcomes, and list skills named in the open job. Upload the CV and role description for a tailored report."
        if "job" in lower or "role" in lower:
            return "I could not find a matching open role. Create or upload a job description first, then I can match CVs to its required skills."
        return "I could not find matching evidence in this workspace. Add relevant resumes or job descriptions, or ask about candidates, interviews, pipeline status, or a specific role."
