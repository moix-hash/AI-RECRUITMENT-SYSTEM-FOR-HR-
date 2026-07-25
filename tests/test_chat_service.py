from __future__ import annotations

from services.chat_actions import Actor, ChatActionService
from services.chat_service import RecruitmentChatService


def test_interview_questions_are_routed_before_candidate_search() -> None:
    response = RecruitmentChatService().respond(
        Actor(1, "recruiter"),
        "Generate interview questions for Python and AWS",
        ChatActionService(),
    )

    assert response["ok"] is True
    questions = response["result"]["questions"]
    assert questions
    assert "python" in questions[0].lower()
    assert "aws" in questions[0].lower()
