# TalentOS — AI Recruitment Workspace

## Project Title
TalentOS — AI Recruitment Workspace

## Objective
TalentOS is a Streamlit-based recruitment platform designed to help HR teams and candidates manage job applications efficiently. The system supports job-description upload, resume parsing, AI-assisted candidate analysis, candidate ranking, pipeline tracking, and interview scheduling in a single workflow.

## Installation Steps
1. Clone or download the project.
2. Open the project folder in a terminal.
3. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Copy the sample environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
6. Run the application:
   ```powershell
   python -m streamlit run app/main.py --server.port 8501
   ```

## Required Libraries
The project uses the following major libraries:
- streamlit
- pydantic
- sqlalchemy
- pandas
- plotly
- langchain
- langchain-google-genai
- pymupdf
- pdfplumber
- reportlab
- python-dotenv

A complete list is available in requirements.txt.

## How to Run the Project
1. Start the application with the command above.
2. Open the local URL displayed by Streamlit.
3. Sign in or use the available authentication flow.
4. Upload a job description and one or more resumes.
5. Review the AI-generated analysis and candidate ranking results.

## Expected Output
After running the app, the user should be able to:
- upload a job description,
- upload resumes,
- view extracted text and candidate summaries,
- compare candidates against a role,
- track applicants in the pipeline,
- and schedule interviews.

## Dataset Used
The project uses synthetic demo resumes and job descriptions. Source files are stored in `assets/samples/`; a structured, tabular submission dataset and data dictionary are stored in `dataset/`. No real candidate data is included.

## Model / Algorithm
No trained model file is applicable to this project. The system uses PDF text extraction, recognised-skill matching, deterministic scoring, and an optional Gemini + LangChain analysis path. See `trained_model_not_applicable.md`.
