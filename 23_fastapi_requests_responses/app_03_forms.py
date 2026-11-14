from html import escape
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field

# HTML FORMS send data as  application/x-www-form-urlencoded  (key=value&key=value), not JSON.
# Declare each field with Form(). It needs the package python-multipart (included in fastapi[standard]).
#   username: Annotated[str, Form()]          required field
#   age: Annotated[int, Form(ge=18)]          same validation rules as Query and Path
# A request is either a form OR JSON: one function cannot accept both kinds of body.
#
# THE USUAL FLOW (post, redirect, get)
#   GET  /login   show the form (a template)
#   POST /login   read the form; wrong data -> show the form again with an error (401)
#                 correct data -> redirect with 303, so a page refresh does not send the form twice
#   GET  /welcome/ann   the page after the redirect
#
# REAL APPLICATIONS never keep plain-text passwords. This lesson uses one only to stay short.

BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI()

USERS = {"ann": "secret"}


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


@app.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    if USERS.get(username) != password:
        return templates.TemplateResponse(
            request=request, name="login.html",
            context={"error": "Wrong username or password"}, status_code=401,
        )
    return RedirectResponse(url=f"/welcome/{username}", status_code=303)


@app.get("/welcome/{username}", response_class=HTMLResponse)
def welcome(username: str):
    return f"<h1>Welcome {escape(username)}</h1>"


# A whole form as ONE Pydantic model (FastAPI 0.113 and newer)
class Signup(BaseModel):
    model_config = ConfigDict(extra="forbid")       # unknown form fields are an error
    email: str
    age: int = Field(ge=18)


@app.post("/signup")
def signup(data: Annotated[Signup, Form()]):
    return data