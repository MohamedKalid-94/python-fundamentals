from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# FastAPI mostly returns JSON, but it can also return HTML pages built from TEMPLATES (Jinja2).
# A template is an HTML file with placeholders. You pass a CONTEXT (a dict) and get a finished page.
# Your Next.js front end handles most pages, so this lesson is short; it is still the right tool for
# small admin pages, e-mails and simple tools.
#
# JINJA2 SYNTAX
#   {{ name }}                         print a value (HTML-escaped automatically)
#   {% for x in items %} ... {% endfor %}      loop
#   {% if cond %} ... {% else %} ... {% endif %}   condition
#   {% extends "base.html" %}  {% block content %} ... {% endblock %}     inheritance
#   {{ sensor.name }}                  works for attributes AND dictionary keys
#   {{ url_for('static', path='/style.css') }}   a URL built from a route name (lesson 02)
#
# RUN:  fastapi dev app_01_templates.py      then open  http://127.0.0.1:8000/hello/Ann

BASE_DIR = Path(__file__).parent                           # not the current folder: works from anywhere
templates = Jinja2Templates(directory=BASE_DIR / "templates")

app = FastAPI()


@app.get("/hello/{name}", response_class=HTMLResponse)     # response_class = how /docs describes the answer
def hello(request: Request, name: str):
    sensors = [
        {"name": "temp", "value": 21.5, "unit": "C"},
        {"name": "humidity", "value": 40, "unit": "%"},
    ]
    return templates.TemplateResponse(
        request=request,                                    # always pass the request
        name="hello.html",
        context={"title": "Sensors", "name": name, "sensors": sensors},
    )


@app.get("/empty", response_class=HTMLResponse)
def empty(request: Request):
    return templates.TemplateResponse(
        request=request, name="hello.html",
        context={"title": "Empty", "name": "nobody", "sensors": []},
    )


# SECURITY: Jinja2 escapes < > & and quotes in {{ }} for .html templates, so user input cannot inject
# a <script> tag (cross-site scripting). Never switch this off for text a user typed.
# Older tutorials write TemplateResponse("page.html", {"request": request}); that form is deprecated.