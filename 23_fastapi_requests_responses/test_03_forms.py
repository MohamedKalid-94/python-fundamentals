from fastapi.testclient import TestClient

from app_03_forms import app

client = TestClient(app)


def test_form_page():
    response = client.get("/login")
    assert response.status_code == 200
    assert '<form action="/login" method="post">' in response.text
    assert 'name="username"' in response.text


def test_login_success_redirects_with_303():
    response = client.post(
        "/login", data={"username": "ann", "password": "secret"}, follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/welcome/ann"


def test_login_success_after_following_redirect():
    response = client.post("/login", data={"username": "ann", "password": "secret"})
    assert response.status_code == 200
    assert "Welcome ann" in response.text


def test_wrong_password_shows_the_form_again():
    response = client.post("/login", data={"username": "ann", "password": "nope"})
    assert response.status_code == 401
    assert "Wrong username or password" in response.text


def test_missing_form_field_is_422():
    response = client.post("/login", data={"username": "ann"})
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "password"]


def test_json_is_not_accepted_for_a_form():
    response = client.post("/login", json={"username": "ann", "password": "secret"})
    assert response.status_code == 422


def test_pydantic_form_ok():
    response = client.post("/signup", data={"email": "a@b.c", "age": "20"})
    assert response.status_code == 200
    assert response.json() == {"email": "a@b.c", "age": 20}


def test_pydantic_form_rule_fails():
    response = client.post("/signup", data={"email": "a@b.c", "age": "17"})
    error = response.json()["detail"][0]
    assert response.status_code == 422
    assert error["type"] == "greater_than_equal"
    assert error["loc"] == ["body", "age"]


def test_pydantic_form_rejects_extra_fields():
    response = client.post("/signup", data={"email": "a@b.c", "age": "20", "colour": "red"})
    assert response.status_code == 422