from fastapi.testclient import TestClient

from app_07_routers_and_sub_apps import app

client = TestClient(app)


def test_router_prefixes_are_combined():
    assert client.get("/api/users").json() == [{"id": 1, "name": "ann"}, {"id": 2, "name": "bo"}]
    assert client.get("/api/users/7").json() == {"id": 7, "name": "ann"}


def test_dependency_on_a_whole_router():
    assert client.get("/api/admin/stats").status_code == 403
    response = client.get("/api/admin/stats", headers={"X-Role": "admin"})
    assert response.json() == {"users": 2}


def test_router_tags_reach_the_documentation():
    paths = client.get("/openapi.json").json()["paths"]
    assert paths["/api/users"]["get"]["tags"] == ["users"]
    assert paths["/api/admin/stats"]["get"]["tags"] == ["admin"]


def test_mounted_sub_apps_answer_under_their_prefix():
    assert client.get("/v1/status").json() == {"version": 1}
    assert client.get("/v2/status").json() == {"version": 2}


def test_a_sub_app_has_its_own_documentation():
    assert client.get("/v1/docs").status_code == 200
    assert client.get("/v1/openapi.json").json()["info"]["title"] == "API v1"
    main_paths = client.get("/openapi.json").json()["paths"]
    assert "/v1/status" not in main_paths