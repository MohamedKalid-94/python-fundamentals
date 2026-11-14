import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# THE FLOW (OAuth2 "password" flow with bearer tokens)
#   1. POST /token with form fields username and password
#   2. the server checks the password against a HASH and returns a signed JWT (access_token)
#   3. the client sends   Authorization: Bearer <token>   on every later request
#   4. a dependency (get_current_user) checks the signature and expiry and loads the user
#
# PASSWORDS: never store them; store a HASH made with a slow algorithm (Argon2 here, via pwdlib).
#            Verify with password_hash.verify(plain, stored_hash).
# JWT (JSON Web Token): three Base64 parts: header.payload.signature.
#   The payload is READABLE by anyone (do not put secrets in it); the signature proves it was not changed.
#   "sub" = who the token is about, "exp" = when it expires.
#   The signing key must be long, random and secret: set JWT_SECRET_KEY in the environment
#   (for example:  python -c "import secrets; print(secrets.token_hex(32))").
# ALSO: use HTTPS only; keep tokens short-lived; browsers can hold the token in an httponly cookie;
#       an API key header (Module 23, lesson 08) is simpler for machine-to-machine calls.
#       This lesson keeps users in a dict: a real application loads them from a database (lesson 02).

SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-only-change-me-dev-only-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy-password")       # makes unknown users take as long as known ones

USERS = {
    "ann": {"username": "ann", "full_name": "Ann A", "disabled": False,
            "hashed_password": password_hash.hash("secret")},
    "bo": {"username": "bo", "full_name": "Bo B", "disabled": True,
           "hashed_password": password_hash.hash("pw")},
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")      # also adds the "Authorize" button to /docs


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool = False


def authenticate_user(username: str, password: str) -> dict | None:
    user = USERS.get(username)
    if user is None:
        password_hash.verify(password, DUMMY_HASH)          # spend the same time, then fail
        return None
    if not password_hash.verify(password, user["hashed_password"]):
        return None
    return user


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_MINUTES))
    return jwt.encode({"sub": subject, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    credentials_error = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])     # checks signature AND expiry
    except InvalidTokenError:
        raise credentials_error
    username = payload.get("sub")
    if username is None or username not in USERS:
        raise credentials_error
    return User(**USERS[username])                          # the hash is not copied: User has no such field


def get_current_active_user(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


app = FastAPI()


@app.post("/token")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(form.username, form.password)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=create_access_token(user["username"]), token_type="bearer")


@app.get("/users/me")
def read_me(user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return user