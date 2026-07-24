from __future__ import annotations

from pathlib import Path

from database.models import Resume, SessionLocal


DEMO_RESUME_FILES = (
    "demo_ahmed_khan_cv.txt", "demo_sofia_martinez_cv.txt", "demo_daniel_brooks_cv.txt",
    "demo_priya_nair_cv.txt", "demo_maya_chen_cv.txt", "demo_jordan_williams_cv.txt",
)


def seed_demo_candidates(user_id: int) -> int:
    """Add the bundled demo CVs once per recruiter workspace."""
    sample_dir = Path(__file__).resolve().parents[1] / "assets" / "samples"
    added = 0
    with SessionLocal() as session:
        existing = {name for (name,) in session.query(Resume.filename).filter(Resume.user_id == user_id).all()}
        for filename in DEMO_RESUME_FILES:
            if filename in existing:
                continue
            path = sample_dir / filename
            session.add(Resume(user_id=user_id, filename=filename, storage_path=str(path), text_content=path.read_text(encoding="utf-8"),))
            added += 1
        session.commit()
    return added
