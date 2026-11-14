from datetime import datetime, timedelta, timezone

import jwt
from fastapi.testclient import TestClient

from app_11_security_jwt import (ALGORITHM, SECRET_KEY, USERS, app, create_access_token,
                                 password_hash)

client = TestClient(app)


def login(username="ann", password="secret"):
    return client.post("/token", data={"username": username, "password": password})


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


def test_login_returns_a_signed_token():
    response = login()
    body = response.json()
    assert response.status_code == 200
    assert body["token_type"] == "bearer"
    payload = jwt.decode(body["access_token"], SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "ann"
    assert "exp" in payload


def test_wrong_password_is_401():
    response = login(password="wrong")
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"
    assert response.json() == {"detail": "Incorrect username or password"}


def test_unknown_user_is_401():
    assert login(username="nobody").status_code == 401


def test_protected_route_with_a_valid_token():
    token = login().json()["access_token"]
    response = client.get("/users/me", headers=bearer(token))
    assert response.json() == {"username": "ann", "full_name": "Ann A", "disabled": False}


def test_no_token_is_401():
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_garbage_token_is_401():
    response = client.get("/users/me", headers=bearer("not-a-jwt"))
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_expired_token_is_401():
    expired = create_access_token("ann", timedelta(minutes=-1))
    assert client.get("/users/me", headers=bearer(expired)).status_code == 401


def test_token_signed_with_another_key_is_401():
    forged = jwt.encode(
        {"sub": "ann", "exp": datetime.now(timezone.utc) + timedelta(minutes=5)},
        "another-secret-key-of-32-characters!!",
        algorithm=ALGORITHM,
    )
    assert client.get("/users/me", headers=bearer(forged)).status_code == 401


def test_disabled_user_can_log_in_but_not_use_the_api():
    token = login("bo", "pw").json()["access_token"]
    response = client.get("/users/me", headers=bearer(token))
    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}


def test_passwords_are_stored_as_hashes():
    stored = USERS["ann"]["hashed_password"]
    assert stored != "secret"
    assert stored.startswith("$argon2")
    assert password_hash.verify("secret", stored)