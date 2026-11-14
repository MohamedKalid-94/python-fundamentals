from fastapi.testclient import TestClient

from app_10_errors_and_settings import Settings, app

client = TestClient(app)


def test_settings_defaults(monkeypatch):
    for variable in ("APP_NAME", "APP_DEBUG", "APP_MAX_ITEMS"):
        monkeypatch.delenv(variable, raising=False)
    settings = Settings()
    assert settings.name == "my-api"
    assert settings.debug is False
    assert settings.max_items == 100


def test_settings_from_environment(monkeypatch):
    monkeypatch.setenv("APP_MAX_ITEMS", "5")
    monkeypatch.setenv("APP_DEBUG", "true")
    settings = Settings()
    assert settings.max_items == 5                  # converted from the text "5"
    assert settings.debug is True


def test_http_exception():
    response = client.get("/sensors/missing")
    assert response.status_code == 404
    assert response.json() == {"detail": "Sensor not found"}
    assert response.headers["x-error"] == "no-sensor"


def test_custom_exception_handler():
    response = client.get("/sensors/broken")
    assert response.status_code == 503
    assert response.json() == {"error": "sensor broken is offline"}


def test_custom_validation_error_format():
    response = client.get("/double/abc")
    assert response.status_code == 422
    assert response.json()["errors"][0]["field"] == "number"


def test_unhandled_error_is_500():
    safe_client = TestClient(app, raise_server_exceptions=False)
    response = safe_client.get("/crash")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"