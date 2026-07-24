from __future__ import annotations

import re
from typing import List

from database.models import SessionLocal, Resume
from repositories.resume_repository import ResumeRepository
from utils.file_utils import extract_text_from_pdf, save_upload, validate_file_size


class ResumeService:
    """Service layer for resume validation, storage, and extraction."""

    def upload_resume(self, uploaded_file, user_id: int) -> dict:
        if not validate_file_size(uploaded_file):
            raise ValueError("File exceeds maximum allowed size")

        storage_path, safe_name = save_upload(uploaded_file, uploaded_file.name)
        text = extract_text_from_pdf(storage_path)
        email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
        candidate_email = email_match.group(0).lower() if email_match else ""

        with SessionLocal() as db:
            repository = ResumeRepository(db)
            if candidate_email:
                existing = db.query(Resume).filter(
                    Resume.user_id == user_id,
                    Resume.text_content.ilike(f"%{candidate_email}%"),
                ).first()
                if existing:
                    existing.filename = safe_name
                    existing.storage_path = storage_path
                    existing.text_content = text[:4000]
                    db.commit()
                    db.refresh(existing)
                    return {"id": existing.id, "filename": safe_name, "storage_path": storage_path, "text_preview": text[:4000], "deduplicated": True}
            record = Resume(
                user_id=user_id,
                filename=safe_name,
                storage_path=storage_path,
                text_content=text[:4000],
            )
            repository.create(record)
            return {"id": record.id, "filename": safe_name, "storage_path": storage_path, "text_preview": text[:4000], "deduplicated": False}

    def list_for_user(self, user_id: int) -> List[Resume]:
        with SessionLocal() as db:
            return ResumeRepository(db).list_for_user(user_id)
