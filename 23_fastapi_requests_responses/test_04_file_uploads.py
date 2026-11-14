from fastapi.testclient import TestClient

import app_04_file_uploads as module
from app_04_file_uploads import app

client = TestClient(app)


def test_bytes_upload():
    response = client.post("/upload/bytes", files={"file": ("a.bin", b"12345")})
    assert response.json() == {"size": 5}


def test_upload_file_metadata():
    response = client.post("/upload", files={"file": ("notes.txt", b"hello\nworld\n", "text/plain")})
    assert response.json() == {"filename": "notes.txt", "content_type": "text/plain", "size": 12}


def test_missing_file_is_422():
    response = client.post("/upload")
    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "file"]


def test_many_files_and_a_form_field():
    response = client.post(
        "/upload/many",
        files=[("files", ("a.txt", b"1", "text/plain")), ("files", ("b.txt", b"2", "text/plain"))],
        data={"description": "two"},
    )
    assert response.json() == {"names": ["a.txt", "b.txt"], "description": "two"}


def test_csv_is_accepted():
    response = client.post("/upload/csv", files={"file": ("d.csv", b"a,b\n1,2\n", "text/csv")})
    assert response.json() == {"filename": "d.csv", "lines": 2}


def test_wrong_type_is_415():
    response = client.post("/upload/csv", files={"file": ("p.png", b"x", "image/png")})
    assert response.status_code == 415


def test_too_large_is_413():
    big = b"x" * (module.MAX_BYTES + 1)
    response = client.post("/upload/csv", files={"file": ("big.txt", big, "text/plain")})
    assert response.status_code == 413


def test_saved_file_uses_a_safe_name(tmp_path, monkeypatch):
    monkeypatch.setattr(module, "UPLOAD_DIR", tmp_path / "uploads")
    response = client.post("/upload/save", files={"file": ("../../evil.txt", b"data", "text/plain")})
    assert response.status_code == 201
    assert response.json() == {"saved_as": "evil.txt", "size": 4}
    assert (tmp_path / "uploads" / "evil.txt").read_bytes() == b"data"
    assert not (tmp_path / "evil.txt").exists()