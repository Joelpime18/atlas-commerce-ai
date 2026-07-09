from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_webhook_returns_customer_reply() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "Hola, quiero comprar una torta pistacho.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["customer_id"] == "wa:573001112233"
    assert "Atlas" in body["reply"]
