from __future__ import annotations

from services.chat_actions import Actor, ChatActionService


def test_read_only_role_cannot_prepare_mutation() -> None:
    result = ChatActionService().request(Actor(1, "viewer"), "create_job", {"title": "Engineer"})
    assert result["ok"] is False
    assert "permission" in result["message"]


def test_recruiter_mutation_requires_confirmation() -> None:
    result = ChatActionService().request(Actor(1, "recruiter"), "create_job", {"title": "Engineer"})
    assert result["ok"] is True
    assert result["confirmation_required"] is True


def test_confirmation_cannot_be_used_by_another_actor() -> None:
    actions = ChatActionService()
    requested = actions.request(Actor(1, "recruiter"), "create_job", {"title": "Engineer"})
    result = actions.confirm(Actor(2, "recruiter"), requested["token"])
    assert result["ok"] is False
