import pytest
from fastapi.testclient import TestClient

from app_08_dependencies import (Settings, app, calls, events, get_api_key, get_settings)

client = TestClient(app)
KEY = {"X-API-Key": "secret-key"}


@pytest.fixture(autouse=True)
def clean_state():
    events.clear()
    calls["n"] = 0
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def test_function_dependency_defaults():
    assert client.get("/items").json() == list(range(1, 11))


def test_function_dependency_values():
    assert client.get("/items", params={"skip": 2, "limit": 3}).json() == [3, 4, 5]


def test_dependency_parameters_are_validated():
    response = client.get("/items", params={"limit": 101})
    error = response.json()["detail"][0]
    assert response.status_code == 422
    assert error["loc"] == ["query", "limit"]
    assert error["type"] == "less_than_equal"


def test_class_dependency():
    assert client.get("/pages", params={"skip": 4}).json() == {"skip": 4, "limit": 10}


def test_missing_api_key_is_401():
    response = client.get("/profile")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid API key"}


def test_sub_dependency_chain_with_a_valid_key():
    assert client.get("/profile", headers=KEY).json() == {"name": "ann"}


def test_dependencies_in_the_decorator():
    assert client.get("/admin").status_code == 401
    assert client.get("/admin", headers=KEY).json() == {"admin": True}


def test_yield_dependency_cleans_up():
    assert client.get("/db/21").json() == {"result": 42}
    assert events == ["open", "close"]


def test_dependency_is_cached_inside_one_request():
    assert client.get("/cached").json() == {"a": 1, "b": 1, "calls": 1}


def test_use_cache_false_runs_it_twice():
    assert client.get("/uncached").json() == {"a": 1, "b": 2, "calls": 2}


def test_override_settings_in_a_test():
    app.dependency_overrides[get_settings] = lambda: Settings(app_name="test", max_items=5)
    assert client.get("/info").json() == {"app_name": "test", "max_items": 5}


def test_override_authentication_in_a_test():
    app.dependency_overrides[get_api_key] = lambda: "test-key"
    assert client.get("/profile").json() == {"name": "ann"}         # no header needed


def test_lru_cache_returns_the_same_object():
    assert get_settings() is get_settings()