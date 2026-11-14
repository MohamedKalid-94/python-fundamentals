from fastapi.testclient import TestClient

from app_01_templates import app

client = TestClient(app)


def test_template_renders_context():
    response = client.get("/hello/Ann")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "<title>Sensors</title>" in response.text              # block from the child template
    assert "<h1>Hello Ann</h1>" in response.text
    assert "<li>temp: 21.5 C</li>" in response.text
    assert "<li>humidity: 40 %</li>" in response.text


def test_html_is_escaped():
    response = client.get("/hello/<i>")
    assert "&lt;i&gt;" in response.text
    assert "<i>" not in response.text


def test_empty_list_branch():
    response = client.get("/empty")
    assert "No sensors." in response.text
    assert "<li>" not in response.text