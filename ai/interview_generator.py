from __future__ import annotations

from typing import List


def generate_interview_questions(skill_matches: list[str], recommendation: str) -> list[str]:
    questions: list[str] = []

    if skill_matches:
        questions.append(
            f"Describe your experience working with {', '.join(skill_matches[:3])} and the measurable impact you delivered."
        )
        questions.append("Walk me through a project where requirements changed mid-way and how you adapted the solution.")

    questions.extend(
        [
            "Tell me about a time you solved a complex technical or business problem under tight deadlines.",
            "How do you prioritize conflicting priorities when stakeholders disagree on urgency?",
            "Describe a situation where you improved team delivery quality through process or communication changes.",
            "What trade-offs did you make when balancing speed, reliability, and maintainability in a system design?",
        ]
    )

    if recommendation in {"Strong Hire", "Hire"}:
        questions.append("What leadership or mentorship responsibilities have you taken on within your team?")

    return questions
