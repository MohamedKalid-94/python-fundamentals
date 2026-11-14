# Lesson 12: Deployment notes

## 1. Ways to run the server

| Command | Use |
|---|---|
| `fastapi dev app_12_deployment.py` | Development: auto-reload, listens on 127.0.0.1 |
| `fastapi run app_12_deployment.py` | Production style: no reload |
| `uvicorn app_12_deployment:app --host 0.0.0.0 --port 8000` | The same with Uvicorn directly |
| `uvicorn app_12_deployment:app --workers 4` | Several processes on one machine (cannot be combined with `--reload`) |

Rules of thumb:
- One Uvicorn process uses one CPU core for Python code. More cores means more worker processes.
- In containers, the usual pattern is ONE process per container, and the platform (Kubernetes, ECS, Cloud Run) starts more containers.
- Put a reverse proxy (nginx, Caddy, a cloud load balancer) in front. It terminates HTTPS, adds buffering and limits.
  Behind a proxy start Uvicorn with `--proxy-headers` so the real client address and scheme are known.
- Log to standard output; the platform collects the logs.

## 2. Dockerfile (saved as `Dockerfile` in this folder)

```dockerfile
FROM python:3.12-slim

WORKDIR /code

# Install the dependencies first: Docker caches this layer until requirements.txt changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app_12_deployment.py .

# Do not run as root
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')" || exit 1

CMD ["uvicorn", "app_12_deployment:app", "--host", "0.0.0.0", "--port", "8000"]
```

`.dockerignore`:

```
.venv/
__pycache__/
.pytest_cache/
*.db
.env
```

`docker-compose.yml`:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      APP_VERSION: "1.0.0"
      APP_ENVIRONMENT: "production"
      APP_DOCS_ENABLED: "false"
    restart: unless-stopped
```

Build and run:

```powershell
docker build -t fastapi-course .
docker run --rm -p 8000:8000 -e APP_VERSION=1.0.0 fastapi-course
curl.exe http://127.0.0.1:8000/health
docker compose up --build
```

## 3. Configuration and secrets

- Everything that changes between machines goes in environment variables (`pydantic-settings`, Module 22, lesson 10).
- Secrets (database password, JWT key, API keys) come from the platform's secret store, never from the image or from Git.
- A `.env` file is for local development only; it is in `.gitignore` and `.dockerignore`.

## 4. Health checks

- Liveness (`/health`): the process answers. If it fails, restart the container.
- Readiness (`/ready`): the database and other dependencies are reachable. If it fails, the load balancer stops sending traffic, but the container is not killed.

## 5. Before going live: checklist

| Check | Done when |
|---|---|
| HTTPS | A proxy or load balancer terminates TLS; HTTP redirects to HTTPS |
| Docs | `/docs` and `/openapi.json` off, or behind a login |
| CORS | Only your real front-end origins are allowed (Module 23, lesson 09) |
| Secrets | Not in Git, not in the image |
| Hosts | `TrustedHostMiddleware` lists your domain names |
| Database | Migrations run (Alembic); backups exist |
| Logs and errors | Logs go to stdout; errors are collected somewhere |
| Limits | Request size and rate limits at the proxy |
| Tests | CI runs `pytest` on every push, and the image is built in CI |