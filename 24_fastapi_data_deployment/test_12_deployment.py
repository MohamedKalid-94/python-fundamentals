from fastapi.testclient import TestClient

from app_12_deployment import Settings, app, create_app


def test_health():
    assert TestClient(app).get("/health").json() == {"status": "ok"}


def test_version_comes_from_the_settings():
    client = TestClient(create_app(Settings(version="1.2.3", environment="staging")))
    assert client.get("/version").json() == {"version": "1.2.3", "environment": "staging"}


def test_readiness_reports_the_failed_checks():
    application = create_app(Settings())
    client = TestClient(application)
    assert client.get("/ready").json() == {"status": "ready"}
    application.state.checks["database"] = False
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "not ready", "failed": ["database"]}


def test_docs_can_be_switched_off():
    client = TestClient(create_app(Settings(environment="production", docs_enabled=False)))
    assert client.get("/docs").status_code == 404
    assert client.get("/openapi.json").status_code == 404
    assert client.get("/health").status_code == 200


def test_settings_come_from_the_environment(monkeypatch):
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("APP_DOCS_ENABLED", "false")
    settings = Settings()
    assert settings.version == "9.9.9"
    assert settings.docs_enabled is False