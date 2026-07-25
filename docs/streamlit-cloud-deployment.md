# Streamlit Community Cloud deployment

TalentOS is ready to run from the GitHub repository with `app/main.py` as its entry point.
Community Cloud runs from the repository root and automatically finds `requirements.txt`.

## 1. Create a managed PostgreSQL database

Use a provider such as Supabase, Neon, Railway, or Render. Create a PostgreSQL database, then copy
its SSL connection string. Use the SQLAlchemy psycopg format below:

```toml
DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"
```

Do not use the local SQLite value (`sqlite:///recruitment_dashboard.db`) in Cloud. Streamlit
Community Cloud's local filesystem is not durable, while a managed PostgreSQL database persists
users, jobs, resumes' extracted text, rankings, applications, and audit data.

## 2. Deploy

1. Sign in at [share.streamlit.io](https://share.streamlit.io/) using the GitHub account that owns
   the repository.
2. Select **Create app** and then **Yup, I have an app**.
3. Select `moix-hash/AI-RECRUITMENT-SYSTEM-FOR-HR-`, branch `main`, and entry point `app/main.py`.
4. Open **Advanced settings**, select Python **3.12**, and paste the contents of
   `.streamlit/secrets.example.toml` after replacing all placeholder values.
5. Click **Deploy** and wait for dependencies to install.

## 3. Required Cloud secrets

Use the Secrets field in Streamlit Cloud, not GitHub or source code:

```toml
APP_ENV = "production"
DATABASE_URL = "postgresql+psycopg://USER:PASSWORD@HOST:5432/DATABASE?sslmode=require"
SECRET_KEY = "your-long-random-secret"
JWT_SECRET = "a-different-long-random-secret"
GEMINI_API_KEY = "your-rotated-gemini-key"
GEMINI_MODEL = "gemini-2.0-flash"
```

Root-level Streamlit secrets are also exposed as environment variables, so the existing settings
module securely reads them without committing a `.env` file.

## Important storage note

The PostgreSQL database makes application records durable. Uploaded PDF files are currently stored
on the app filesystem and are therefore temporary on Community Cloud. For production, set up an
object-storage provider (Supabase Storage, Amazon S3, or Cloudinary) before relying on long-term
PDF retention.
