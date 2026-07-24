# Ten-minute project demonstration script

Use this outline to record the required final-project walkthrough. Replace the repository
link and deployed app URL in the video description before publishing it on YouTube.

1. **Project introduction (0:00–0:45)** — Introduce TalentOS as an AI-assisted HR screening
   workspace built with Streamlit, Python, SQLite, Gemini/LangChain, and a local fallback.
2. **Folder structure (0:45–1:30)** — Show `pages/`, `services/`, `ai/`, `database/`,
   `assets/samples/`, `tests/`, and `docs/`. Explain that secrets are stored outside Git.
3. **Code overview (1:30–2:30)** — Show the resume service, PDF extraction/cleaning,
   email-based candidate de-duplication, and the analysis service.
4. **LangChain and Gemini (2:30–3:15)** — Show `ai/analysis.py`, the Pydantic schema, and
   the prompt. Explain that Gemini provides a structured response when configured and the
   app uses deterministic local scoring when it is unavailable.
5. **Upload a job description (3:15–4:00)** — Upload or paste a JD, review extracted text,
   add title/skills, and publish the opening.
6. **Upload resumes (4:00–5:45)** — Upload one or more selectable-text PDFs, review extracted
   text, select the best open role, and run the analysis. Point out the summary, matching,
   missing/extra skills, score, recommendation, justification, and interview questions.
7. **Ranking and comparison (5:45–7:00)** — Open Candidate ranking, show email de-duplication,
   CSV export, per-candidate best role, and compare two candidates side by side.
8. **HR workflow (7:00–8:15)** — Open Pipeline, show applicants, shortlist a candidate, move a
   candidate through stages, and schedule an interview.
9. **Feedback and history (8:15–9:00)** — Show the candidate history/audit information and how
   the recruiter can revisit results.
10. **Future improvements (9:00–10:00)** — Mention production RAG/semantic search, managed
    authentication, calendar/email integration, stronger OCR, a managed database, and bias
    monitoring. Finish with the GitHub repository and Streamlit deployment links.
