# Project Report

## Title
TalentOS - AI Recruitment Workspace

## Group Members
- Syed Moiz Shahab - Seat No: B23110006164 - Project developer / Group member
- Hamza Rizwan - Seat No: B2311006038 - Group member
- Project type: Team project

## Introduction
TalentOS is an AI-assisted recruitment platform built with Python and Streamlit. It reduces the manual effort of resume screening by combining PDF text extraction, job-description processing, candidate scoring, ranking, and applicant tracking in one workflow.

## Problem Statement
Recruiters often spend significant time reading and comparing CVs manually. This project addresses that problem with a web application that extracts resume content, compares it to job requirements, identifies suitable candidates, and supports the subsequent hiring workflow.

## Objectives
- Automate resume and job-description processing.
- Support AI-assisted candidate evaluation.
- Rank candidates based on skill alignment with an open role.
- Provide recruiters with a pipeline, history, and interview workflow.
- Keep a local fallback available when an external AI service is unavailable.

## Dataset
The project uses synthetic, non-identifying data for safe demonstration and testing. The dataset contains six demo CV summaries and two job descriptions in the `dataset/` folder. Original readable sample CVs and job descriptions are in `assets/samples/`. No real candidate data is included.

## Model and Algorithm
No custom trained or fine-tuned model is used. The application applies PDF text extraction with PyMuPDF and pdfplumber, recognised-skill matching, and deterministic scoring. The algorithm compares skills in a CV and a job description, identifies matching and missing skills, calculates a bounded 0-100 readiness score, and produces a recommendation. Gemini through LangChain is an optional external analysis path when a valid API key is configured. If it is unavailable, local scoring and workspace retrieval remain available.

## System Architecture
The system is organised into Streamlit pages, authentication modules, service classes, SQLAlchemy models, repositories, utility functions, AI modules, sample data, and automated tests. A resume moves through upload, PDF extraction, analysis, ranking, and the ATS pipeline. Sensitive workflow actions are permission checked and audited.

## Features Implemented
- User authentication and HR/candidate workflows.
- Resume PDF upload, extraction, cleaning, and email-based candidate de-duplication.
- Job-description entry and optional PDF extraction.
- Candidate summary, skill comparison, readiness score, recommendation, justification, and interview questions.
- Candidate ranking, comparison, and CSV export.
- Applicant pipeline, status tracking, interview scheduling, and candidate history.
- AI assistant with Gemini support when configured and a local retrieval fallback when it is not.
- Demo jobs, synthetic CVs, and automated tests.

## Results and Discussion
The application produces extracted CV text, candidate summaries, matching and missing skills, a 0-100 fit score, HR recommendation, interview questions, rankings, and pipeline activity. The system demonstrates a practical way to improve the speed and consistency of early-stage candidate review. Results are decision support only and should be reviewed by a qualified recruiter before a real hiring decision is made.

## Conclusion
TalentOS is a working prototype for intelligent recruitment support. It demonstrates end-to-end CV processing and candidate workflow management in a Streamlit application. Future improvements could include OCR for scanned files, persistent cloud object storage, calendar and email integration, and additional fairness and audit controls.

## AI Usage Disclosure
OpenAI Codex/ChatGPT was used as a development assistant for code review, debugging, documentation drafting, testing guidance, and UI/workflow improvement suggestions. Gemini is optionally integrated into the application through LangChain for runtime analysis. The accompanying AI usage declaration provides the complete disclosure.

## References
- Streamlit Documentation
- LangChain Documentation
- Google Gemini API Documentation
- Python, SQLAlchemy, PyMuPDF, and pdfplumber Documentation
