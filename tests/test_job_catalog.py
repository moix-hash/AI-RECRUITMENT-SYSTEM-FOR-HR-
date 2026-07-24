from __future__ import annotations

from database.models import Job, SessionLocal, init_db
from services.job_catalog import DEMO_JOBS, populate_catalog


def test_demo_catalog_is_seeded_once(monkeypatch) -> None:
    user_id = 987654
    monkeypatch.delenv("JOB_RSS_FEED_URL", raising=False)
    init_db()
    with SessionLocal() as session:
        session.query(Job).filter(Job.user_id == user_id).delete()
        session.commit()
    source, created = populate_catalog(user_id)
    assert source == "demo"
    assert created == len(DEMO_JOBS)
    assert populate_catalog(user_id) == ("demo", 0)
    with SessionLocal() as session:
        assert session.query(Job).filter(Job.user_id == user_id, Job.source == "demo").count() == len(DEMO_JOBS)
