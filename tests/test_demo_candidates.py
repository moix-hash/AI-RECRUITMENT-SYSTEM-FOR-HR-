from __future__ import annotations

from database.models import Resume, SessionLocal, init_db
from services.demo_candidates import DEMO_RESUME_FILES, seed_demo_candidates


def test_demo_cvs_are_seeded_once() -> None:
    user_id = 876543
    init_db()
    with SessionLocal() as session:
        session.query(Resume).filter(Resume.user_id == user_id).delete()
        session.commit()
    assert seed_demo_candidates(user_id) == len(DEMO_RESUME_FILES)
    assert seed_demo_candidates(user_id) == 0
    with SessionLocal() as session:
        assert session.query(Resume).filter(Resume.user_id == user_id).count() == len(DEMO_RESUME_FILES)
