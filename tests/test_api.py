import os

os.environ["USE_FAKE_MODEL"] = "true"
os.environ["APP_ENV"] = "test"

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_endpoint_responds():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["environment"] == "test"


def test_prediction_endpoint_responds_with_category():
    response = client.post(
        "/predict",
        json={
            "text": "Quiero denunciar una obra pública abandonada en mi municipio"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "category" in data
    assert "score" in data
    assert "recommendation" in data
    assert "route" in data


def test_prediction_metric_threshold():
    response = client.post(
        "/predict",
        json={
            "text": "Quiero aprender sobre SECOP y contratación pública"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["score"] >= 0.20
