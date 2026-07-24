from __future__ import annotations

import os
import xml.etree.ElementTree as element_tree
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from urllib.request import Request, urlopen

from database.models import Job, SessionLocal


DEMO_JOBS = (
    ("Senior Software Engineer", "Northstar Systems", "Austin, TX", "$145k–$175k", "Python, FastAPI, PostgreSQL, AWS"),
    ("Machine Learning Engineer", "Vertex Grove", "San Francisco, CA", "$165k–$205k", "Python, PyTorch, MLOps, Docker"),
    ("Frontend Engineer", "Brightline Labs", "New York, NY", "$125k–$155k", "React, TypeScript, Next.js, CSS"),
    ("Backend Engineer", "Harbor Cloud", "Remote, US", "$130k–$165k", "Node.js, PostgreSQL, Redis, Kubernetes"),
    ("Cloud Engineer", "Summit Tech", "Denver, CO", "$135k–$170k", "AWS, Terraform, Linux, Python"),
    ("DevOps Engineer", "Cedarworks", "Seattle, WA", "$140k–$175k", "Kubernetes, CI/CD, Docker, AWS"),
    ("Cybersecurity Engineer", "Ironleaf Security", "Boston, MA", "$145k–$180k", "SIEM, Python, Cloud Security, IAM"),
    ("Data Analyst", "Atlas Insight", "Chicago, IL", "$85k–$110k", "SQL, Tableau, Python, Statistics"),
    ("Data Scientist", "Juniper Analytics", "Remote, US", "$125k–$160k", "Python, SQL, Machine Learning, Experimentation"),
    ("Business Analyst", "Pioneer Digital", "Atlanta, GA", "$85k–$115k", "SQL, Stakeholder Management, Analytics, Jira"),
    ("QA Automation Engineer", "Signal Foundry", "Raleigh, NC", "$105k–$135k", "Playwright, Python, CI/CD, API Testing"),
    ("Product Manager", "Orbit Products", "Los Angeles, CA", "$135k–$175k", "Product Strategy, Analytics, Agile, Research"),
    ("UI/UX Designer", "Willow Studio", "Portland, OR", "$105k–$140k", "Figma, Design Systems, Research, Prototyping"),
    ("React Developer", "Bayfront Software", "Miami, FL", "$110k–$145k", "React, TypeScript, Testing, GraphQL"),
    ("Node.js Developer", "Lighthouse Apps", "Remote, US", "$115k–$150k", "Node.js, TypeScript, MongoDB, APIs"),
    ("Java Engineer", "Granite Financial", "Charlotte, NC", "$120k–$155k", "Java, Spring Boot, SQL, Kafka"),
    ("Full Stack Engineer", "Mosaic HealthTech", "Minneapolis, MN", "$125k–$160k", "React, Python, PostgreSQL, AWS"),
    ("Mobile Engineer", "Kite Mobile", "San Diego, CA", "$120k–$155k", "Swift, Kotlin, REST APIs, Mobile CI"),
    ("Site Reliability Engineer", "Evergreen Platform", "Remote, US", "$145k–$180k", "SRE, Kubernetes, Terraform, Observability"),
    ("Platform Engineer", "Fathom Networks", "Dallas, TX", "$140k–$175k", "Kubernetes, Go, Terraform, AWS"),
    ("Prompt Engineer", "Lumen AI", "San Francisco, CA", "$150k–$190k", "LLMs, Prompt Design, Python, Evaluation"),
    ("LLM Engineer", "Aster AI", "New York, NY", "$165k–$210k", "Python, RAG, LangChain, Vector Databases"),
    ("AI Research Engineer", "Fieldstone Research", "Cambridge, MA", "$170k–$220k", "PyTorch, Deep Learning, Python, NLP"),
    ("Solutions Architect", "Oakbridge Cloud", "Remote, US", "$145k–$185k", "AWS, Architecture, APIs, Security"),
    ("Technical Program Manager", "Riverbend Technologies", "Washington, DC", "$130k–$165k", "Program Management, Agile, Analytics, Risk"),
)


def populate_catalog(user_id: int) -> tuple[str, int]:
    """Synchronize an opt-in RSS source or seed the complete demo catalog once."""
    feed_url = os.getenv("JOB_RSS_FEED_URL", "").strip()
    if feed_url:
        try:
            return "rss", _sync_rss(user_id, feed_url)
        except (OSError, element_tree.ParseError):
            # A configured but temporarily unavailable feed must not leave the jobs page empty.
            pass
    with SessionLocal() as session:
        exists = session.query(Job.id).filter(Job.user_id == user_id, Job.source == "demo").first()
        if exists:
            return "demo", 0
        now = datetime.utcnow()
        for index, (title, company, location, salary, skills) in enumerate(DEMO_JOBS):
            session.add(Job(
                user_id=user_id, title=title, company=company, location=location, salary_range=salary,
                remote_status="Remote" if location.startswith("Remote") else ("Hybrid" if index % 3 else "On-site"),
                employment_type="Full-time", experience=("5+ years" if index % 2 else "3+ years"),
                department="Engineering" if index not in {7, 9, 11, 12, 24} else "Product & Operations",
                required_skills=skills, preferred_skills="Communication, collaboration, ownership",
                responsibilities=f"[Demo data] Build reliable, customer-focused outcomes as a {title} on a cross-functional technology team.",
                benefits="Health coverage, flexible PTO, learning budget, and remote-work support.", status="Open", source="demo",
                external_id=f"demo-tech-{index + 1}", application_deadline=now + timedelta(days=21 + index),
            ))
        session.commit()
    return "demo", len(DEMO_JOBS)


def _sync_rss(user_id: int, feed_url: str) -> int:
    request = Request(feed_url, headers={"User-Agent": "AI-Recruitment-Assistant/1.0"})
    with urlopen(request, timeout=10) as response:  # nosec B310 - only explicit admin-configured feed URLs
        root = element_tree.fromstring(response.read())
    items = root.findall(".//item")
    created = 0
    with SessionLocal() as session:
        for item in items[:100]:
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("guid") or item.findtext("link") or "").strip()
            description = (item.findtext("description") or "").strip()
            if not title or not link or session.query(Job.id).filter(Job.user_id == user_id, Job.external_id == link).first():
                continue
            session.add(Job(user_id=user_id, title=title, responsibilities=description, status="Open", source="rss", external_id=link, remote_status="Not specified", employment_type="Not specified"))
            created += 1
        session.commit()
    return created
