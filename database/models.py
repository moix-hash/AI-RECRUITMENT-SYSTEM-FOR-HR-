from __future__ import annotations

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
    inspect,
    text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config.settings import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default="hr")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    locked_until = Column(DateTime, nullable=True)

    resumes = relationship("Resume", back_populates="user")
    jobs = relationship("JobDescription", back_populates="user")
    analyses = relationship("AnalysisResult", back_populates="user")


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    website = Column(String(500), nullable=True)
    logo_url = Column(String(500), nullable=True)
    brand_color = Column(String(20), default="#6366f1", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class CompanyMembership(Base):
    __tablename__ = "company_memberships"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(50), default="recruiter", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    company = relationship("Company")
    user = relationship("User")


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    storage_path = Column(String(500), nullable=False)
    text_content = Column(Text, nullable=True)
    extracted_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="jobs")


class Job(Base):
    """A recruiter-managed vacancy. Provider fields keep external integrations decoupled."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    department = Column(String(120), nullable=True)
    company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    remote_status = Column(String(30), default="Hybrid", nullable=False)
    employment_type = Column(String(50), default="Full-time", nullable=False)
    salary_range = Column(String(120), nullable=True)
    experience = Column(String(120), nullable=True)
    required_skills = Column(Text, default="")
    preferred_skills = Column(Text, default="")
    responsibilities = Column(Text, default="")
    education = Column(String(255), nullable=True)
    benefits = Column(Text, default="")
    status = Column(String(30), default="Open", nullable=False, index=True)
    source = Column(String(80), default="manual", nullable=False)
    external_id = Column(String(255), nullable=True, index=True)
    expires_at = Column(DateTime, nullable=True)
    application_deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    candidate_name = Column(String(255), nullable=True)
    resume_filename = Column(String(255), nullable=True)
    job_title = Column(String(255), nullable=True)
    match_score = Column(Integer, default=0)
    recommendation = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    raw_result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="analyses")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    stage = Column(String(50), default="Applied", nullable=False, index=True)
    match_score = Column(Integer, default=0, nullable=False)
    recommendation = Column(String(80), nullable=True)
    notes = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    company = relationship("Company")
    job = relationship("Job")
    resume = relationship("Resume")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False)
    entity_id = Column(Integer, nullable=True)
    details = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


engine = create_engine(DATABASE_URL, future=True)
# Authentication and service methods return lightweight ORM records after the
# transaction scope closes; keep their already-loaded scalar values available.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    # `create_all` deliberately does not alter existing tables. Keep the small
    # SQLite deployment upgrade-safe until a dedicated migration runner is used.
    if engine.dialect.name == "sqlite":
        columns = {column["name"] for column in inspect(engine).get_columns("users")}
        if "locked_until" not in columns:
            with engine.begin() as connection:
                connection.execute(text("ALTER TABLE users ADD COLUMN locked_until DATETIME"))
