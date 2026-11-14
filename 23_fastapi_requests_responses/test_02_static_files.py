from fastapi.testclient import TestClient

from app_02_static_files import app

client = TestClient(app)


def test_css_is_served():
    response = client.get("/static/style.css")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/css")
    assert "font-family" in response.text


def test_missing_static_file_is_404():
    assert client.get("/static/nope.css").status_code == 404


def test_template_links_to_static_file():
    response = client.get("/page")
    assert response.status_code == 200
    assert "/static/style.css" in response.text


def test_cannot_escape_the_static_folder():
    assert client.get("/static/%2e%2e/app_02_static_files.py").status_code == 404