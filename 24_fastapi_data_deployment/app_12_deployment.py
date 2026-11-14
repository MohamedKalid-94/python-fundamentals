from fastapi import FastAPI, Response
from pydantic_settings import BaseSettings, SettingsConfigDict

# A DEPLOYABLE application:
#   - configuration from ENVIRONMENT VARIABLES (APP_VERSION, APP_ENVIRONMENT, APP_DOCS_ENABLED ...)
#   - /health   "the process is alive"     (liveness: restart me if this fails)
#   - /ready    "I can serve traffic"      (readiness: send me no traffic until this is OK; 503 otherwise)
#   - a factory function, create_app(settings), so tests can build an app with any settings
#   - /docs and /openapi.json can be switched off in production
# The deployment notes (12_deployment_notes.md), the Dockerfile and docker-compose.yml are in this folder.


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_")

    version: str = "0.1.0"
    environment: str = "development"
    docs_enabled: bool = True


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    application = FastAPI(
        version=settings.version,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url=None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
    )
    application.state.checks = {"database": True}       # pretend dependencies; set False to simulate an outage

    @application.get("/health")
    def health():
        return {"status": "ok"}

    @application.get("/ready")
    def ready(response: Response):
        failed = [name for name, ok in application.state.checks.items() if not ok]
        if failed:
            response.status_code = 503
            return {"status": "not ready", "failed": failed}
        return {"status": "ready"}

    @application.get("/version")
    def version():
        return {"version": settings.version, "environment": settings.environment}

    return application


app = create_app()