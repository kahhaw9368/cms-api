from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_healthz():
    assert client.get("/healthz").status_code == 200


def test_ready():
    assert client.get("/ready").status_code == 200


def test_root_names_service():
    assert client.get("/").json()["service"] == "cms-api"
