from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# STATIC FILES are files sent as they are: CSS, JavaScript, images, fonts, downloads.
# app.mount("/static", StaticFiles(directory=...), name="static") hands every URL that starts with
# /static to a separate mini-application that serves the files of that folder.
#   - the "name" lets templates build the URL:  url_for('static', path='/style.css')
#   - StaticFiles(directory=...) raises an error at start-up if the folder does not exist
#   - StaticFiles(directory=..., html=True) also serves index.html for a folder URL
#   - the content type comes from the file extension; the browser can cache the file (ETag, Last-Modified)
#   - it cannot read outside its folder: ../ tricks give 404
#   - mounted apps do not appear in /docs
# In production a web server or a CDN (nginx, S3) usually serves static files, not Python.

BASE_DIR = Path(__file__).parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/page", response_class=HTMLResponse)
def page(request: Request):
    return templates.TemplateResponse(request=request, name="page.html", context={})