# Deployment guide

## Docker

1. Copy `.env.example` to `.env` and generate unique values for `SECRET_KEY` and `JWT_SECRET`.
2. Set the database and model-provider values. Never commit `.env`.
3. Run `docker compose --profile production up --build -d`.
4. Open `http://localhost:8501` and monitor `docker compose ps`.

The container runs as a non-root `app` user. Persistent application data and logs are stored in named volumes. For a reverse proxy deployment, terminate TLS at the proxy and restrict application access to private networks.

## Backups and recovery

For SQLite, stop writes and copy `recruitment_dashboard.db` plus the `data` volume. Test restores in a separate environment. Production installations should move to managed PostgreSQL and object storage, with encrypted automated backups and a documented recovery owner.

## Operations checklist

- Rotate application and provider keys regularly.
- Review authentication, AI, and security logs.
- Pin and scan container images before release.
- Apply HTTPS, firewall rules, and least-privilege database credentials.
