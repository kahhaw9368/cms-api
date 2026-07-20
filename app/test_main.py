from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").status_code == 200


def test_ready():
    assert client.get("/ready").status_code == 200


def test_root_names_service():
    assert client.get("/").json()["service"] == "cms-api"


def test_sample_reports_environment(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "dev")
    body = client.get("/api/sample").json()
    assert body["message"] == "this is sample api sitting in dev environment"
    assert body["environment"] == "dev"


def test_sample_prod_environment(monkeypatch):
    monkeypatch.setenv("ENVIRONMENT", "prod")
    body = client.get("/api/sample").json()
    assert body["message"] == "this is sample api sitting in prod environment"


def test_sample_falls_back_to_local(monkeypatch):
    monkeypatch.delenv("ENVIRONMENT", raising=False)
    body = client.get("/api/sample").json()
    assert body["environment"] == "local"
    assert "local" in body["message"]
