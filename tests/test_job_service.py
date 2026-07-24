from __future__ import annotations

import pytest

from database.models import Job
from services.job_service import JobService


def test_job_model_has_portal_defaults() -> None:
    job = Job(user_id=1, title="Data Engineer")
    assert job.title == "Data Engineer"
    assert job.status in (None, "Open")


def test_job_service_rejects_blank_title() -> None:
    with pytest.raises(ValueError, match="title"):
        JobService().create(1, {"title": "   "})


def test_job_service_rejects_invalid_state() -> None:
    with pytest.raises(ValueError, match="Invalid"):
        JobService().transition(1, 1, "Deleted")
