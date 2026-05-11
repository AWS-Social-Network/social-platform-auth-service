# Auth Service

FastAPI service for registration, login, and JWT validation. Data lives in PostgreSQL under the `auth` schema (`auth.users`). The Ads service can read `auth.users` read-only.

## ALB path prefix

Expose this service behind an ALB rule with path prefix `/auth`. Routes are `/auth/register`, `/auth/login`, and `/auth/validate`. Health checks for Kubernetes target `/health` on the pod (no `/auth` prefix).

## Local run

```bash
cp .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```
