# TalentOS — AI Recruitment Workspace

TalentOS is a Streamlit recruitment workspace for HR teams and candidates. It combines job posting, CV intake, candidate matching, ATS pipeline management, interview scheduling, and a role-aware AI assistant in one application.

## Project objective

TalentOS reduces manual CV screening by extracting resume text, comparing it with a job description, producing a transparent candidate-fit score, and supporting recruiters through ranking, pipeline, and interview workflows. Gemini through LangChain is used when configured; a local skill-based and retrieval fallback keeps core functionality available without an API key.


## What it does

### HR and recruiter workflows

- Create, edit, share, and manage open job postings
- Upload CVs and automatically add them to the hiring pipeline
- Upload a job-description PDF or write a role manually; extracted text remains editable before publishing
- Review candidate names, stages, match scores, and job alignment
- Move candidates through Applied, AI Screening, Recruiter Review, Phone Screening, Interview, Offer, and other stages
- Schedule interviews with date, time, meeting link, and an audit record
- Rank unique candidates by CV email address—re-uploading the same email updates the existing candidate instead of creating duplicate ranking cards
- View candidate activity history, recent CV intake, screening activity, and interview events

### Candidate workflows

- Create a candidate account using **Find a job** during sign-up
- Upload a CV and browse open jobs
- Use **Check CV & apply** to verify the role is open and screen the CV against that job
- Applications meeting the threshold enter recruiter review; lower-match applications are recorded as rejected with an explanation

### AI assistant

The assistant works with a deterministic local fallback, so common recruiting answers remain available without an AI API key. HR users can ask questions such as:

- `Who applied to my jobs?`
- `Show candidate names`
- `Show scheduled interviews`
- `Who is interviewing?`
- `Generate interview questions for Python and AWS`
- `Show the hiring pipeline`

Results show live workspace candidate names, roles, stages, and scores. Recruiters can open the selected candidate's scheduling workflow from the result card.

## Matching and uniqueness

- CV text is extracted from text-based PDFs using PyMuPDF and pdfplumber.
- Scanned/image-only PDFs require pasted text unless OCR is added to the environment.
- CV matching uses recognised role skills, rather than common words, to avoid misleading scores.
- Each candidate is uniquely grouped by the email extracted from their CV. If no email is available, the CV is treated as an unverified record.
- Candidate Ranking compares every CV against its best-fitting open job, so different candidates can be matched to different vacancies.
- The ranking screen supports a focused side-by-side comparison and a CSV export for recruiter review.

## Demo content

Without a configured RSS feed, TalentOS seeds approximately 25 realistic technology jobs marked as demo data. It also provides bundled demo CVs and pipeline applications for a populated first-run experience.

Sample job descriptions are available in `assets/samples/`, including `sample_data_engineer_job_description.txt`. The course recording outline and submission checklist are in `docs/`.

Set `JOB_RSS_FEED_URL` to an explicitly approved public RSS feed to synchronize jobs instead of relying only on demo data.

## Dataset and model

- **Dataset:** Synthetic, clearly labelled demo CVs and job descriptions are in `assets/samples/`. A tabular submission dataset and data dictionary are in `dataset/`.
- **Model / algorithm:** No trained model artifact is used. The application combines PDF text extraction, recognised-skill matching, deterministic scoring, and optional Gemini + LangChain structured analysis. See `submission/trained_model_not_applicable.md`.

## Run locally

Requirements: Python 3.10+ and PowerShell on Windows.

```powershell
cd "C:\Users\FBC\AI RECURUITM ENT FOR HR"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python -m streamlit run app/main.py --server.port 8501
```

Open `http://127.0.0.1:8501`.

## Required libraries

The complete dependency list is in `requirements.txt`. The primary libraries are Streamlit, SQLAlchemy, Pydantic, Pandas, PyMuPDF, pdfplumber, LangChain, langchain-google-genai, FAISS, ReportLab, and python-dotenv.

## Expected output

After launching the app, users can create or upload a job description, upload one or more resumes, review extracted text, receive a candidate-fit report with a score and skill gaps, compare/rank candidates, export CSV results, move applications through the hiring pipeline, and schedule interviews.

## Configuration

Copy `.env.example` to `.env`. `.env` is ignored by Git.

```dotenv
APP_ENV=development
DATABASE_URL=sqlite:///recruitment_dashboard.db
MODEL_PROVIDER=gemini
GEMINI_MODEL=gemini-2.0-flash
GEMINI_API_KEY=
JOB_RSS_FEED_URL=
```

Never commit API keys, candidate CVs, uploaded files, database files, or logs. If an API key was ever pasted into chat, source code, or a commit, rotate it before deployment.

## Deploy to Streamlit Community Cloud

1. Create a dedicated GitHub repository containing only this project.
2. Do **not** commit `.env`, `data/`, SQLite databases, uploaded CVs, or `.streamlit/secrets.toml`.
3. In Streamlit Community Cloud, choose **Create app**, select the repository and branch, and set the entry point to `app/main.py`.
4. Create a managed PostgreSQL database (Supabase, Neon, Railway, or Render) and add production
   settings through the Community Cloud **Secrets** panel, for example:

```toml
MODEL_PROVIDER = "gemini"
GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_API_KEY = "replace-with-your-rotated-key"
DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"
```

5. Click **Deploy**.

The current default SQLite database is appropriate for local development only. A managed PostgreSQL
database is required for durable Cloud records. See [Streamlit Cloud deployment](docs/streamlit-cloud-deployment.md)
for the exact app settings and secrets template.

## Project layout

```text
app/           Application entry point and authentication
pages/         Dashboard, jobs, pipeline, AI assistant, help, profile, settings
services/      ATS, CV, job, analysis, chat, and demo-data workflows
database/      SQLAlchemy models and database initialization
repositories/  Query and persistence helpers
components/    Shared sidebar, dashboard, and theme components
utils/         PDF extraction and deterministic matching fallback
assets/samples Bundled demo CVs
docs/          Course demo script and submission checklist
tests/         Automated tests
```

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Submission package

The ready-to-submit files are in `submission/`:

- `project_report.pdf` — project report with group-member details.
- `ai_usage_declaration.md` — transparent AI usage declaration.
- `submission_manifest.txt` — delivery checklist.
- `video_recording_checklist.md` — 5–10 minute recording outline.

Before submitting, record the requested demonstration and include its file or accessible link according to your instructor's submission method.

## Security notes

- Authentication and role checks are enforced in application workflows.
- Sensitive AI actions use permission checks and confirmation handling.
- ATS stage changes and interview scheduling are recorded in the audit log.
- Read-only roles must not be given workflow-changing permissions.

## License

MIT. See [LICENSE](LICENSE).
