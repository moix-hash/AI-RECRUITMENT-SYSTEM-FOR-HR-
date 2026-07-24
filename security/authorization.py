from __future__ import annotations

from dataclasses import dataclass


ROLE_PERMISSIONS = {
    "candidate": {"jobs.read", "career.read", "interview.generate"},
    "viewer": {"jobs.read", "candidates.read", "analytics.read", "interview.generate"},
    "recruiter": {"jobs.read", "jobs.write", "candidates.read", "applications.write", "notes.write", "interview.generate", "reports.read"},
    "hr_manager": {"jobs.read", "jobs.write", "candidates.read", "applications.write", "notes.write", "interview.generate", "reports.read", "emails.send"},
    "admin": {"*"},
    "hr": {"jobs.read", "jobs.write", "candidates.read", "applications.write", "notes.write", "interview.generate", "reports.read"},
}


def has_permission(role: str, permission: str) -> bool:
    grants = ROLE_PERMISSIONS.get((role or "viewer").lower(), set())
    return "*" in grants or permission in grants
