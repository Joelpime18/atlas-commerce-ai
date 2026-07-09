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
    assert body["intent"] == "order"
    assert body["stage"] == "order_details"
    assert "fecha de entrega" in body["reply"]


def test_webhook_returns_catalog_for_price_question() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "Me compartes el catalogo y precios?",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "catalog"
    assert "Torta de pistacho" in body["reply"]
    assert "Cheesecake de pistacho" in body["reply"]


def test_webhook_guides_unknown_message() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "Necesito ayuda",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "unknown"
    assert "ver el catalogo" in body["reply"]
