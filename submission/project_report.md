# Project Report

## Title
TalentOS — AI Recruitment Workspace

## Group Members
- Syed Moiz Shahab — Project developer / group member
- Registration number: **add your registration number before final submission**
- Project type: Individual project

## Introduction
TalentOS is an AI-assisted recruitment platform built using Python and Streamlit. The system aims to reduce manual effort in screening resumes by combining automated text extraction, job-description parsing, candidate scoring, and structured ranking into one workflow.

## Problem Statement
Recruiters often spend significant time reading and comparing CVs manually. This project addresses that challenge by creating a web-based system that helps HR teams quickly analyze resumes, identify the best-fit candidates, and manage applications through a hiring pipeline.

## Objectives
- automate resume and job-description processing,
- support AI-assisted candidate evaluation,
- rank candidates based on skill alignment,
- provide recruiters with a pipeline and interview workflow.

## Methodology
The application uses:
- Streamlit for the user interface,
- SQLAlchemy for database storage,
- PyMuPDF and pdfplumber for PDF text extraction,
- LangChain and Gemini for structured AI analysis when configured,
- a deterministic fallback for local scoring when AI services are unavailable.

The deterministic matching algorithm identifies recognised skills in the resume and job description, calculates skill overlap and gaps, and produces a bounded 0–100 readiness score with a recommendation. When a Gemini API key is available, LangChain requests a structured analysis; when it is unavailable or fails, the local fallback remains available. No model was trained or fine-tuned for this project.

## System Architecture
The project is divided into modules for authentication, UI pages, services, repositories, database models, and AI analysis. Resume data is processed through the service layer, stored in the database, and displayed through the Streamlit interface.

## Features Implemented
- resume upload and parsing,
- job-description upload and editing,
- AI-based candidate analysis,
- skill-level comparison and recommendation generation,
- candidate ranking and CSV export,
- hiring pipeline and interview workflow,
- demo data for testing and demonstration.

## Results and Discussion
The system successfully demonstrates how a recruitment workflow can be automated with a lightweight web application. The expected output is extracted CV text, candidate summary, matching and missing skills, a 0–100 fit score, recommendation, interview questions, ranked candidates, and pipeline activity. It provides recruiters with a faster way to review candidate suitability while preserving a clear audit trail of application activity.

## Conclusion
TalentOS provides a practical prototype for intelligent recruitment support. The project can be extended with stronger OCR, database deployment, email/calendar integrations, and improved authentication for real-world use.

## References
- Streamlit Documentation
- LangChain Documentation
- Google Gemini API Documentation
- Python and SQLAlchemy Documentation
- OpenAI Codex / ChatGPT documentation (development assistance disclosure)
