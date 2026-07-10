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


def test_webhook_returns_main_menu_for_greeting() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "Hola",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "greeting"
    assert body["stage"] == "main_menu"
    assert "1. Cotizar una torta" in body["reply"]
    assert "4. Conocer horarios" in body["reply"]


def test_webhook_starts_quote_flow_from_menu_option() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "1",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "quote"
    assert body["stage"] == "quote_details"
    assert "cuantas personas" in body["reply"]
    assert "color o colores" in body["reply"]
    assert "imagen de referencia" in body["reply"]
    assert "obscenas" in body["reply"]


def test_webhook_starts_order_flow_from_menu_option() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "2",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "order"
    assert body["stage"] == "order_details"
    assert "Nombre completo" in body["reply"]
    assert "Imagen de referencia" in body["reply"]


def test_webhook_asks_for_order_number() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "3",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "faq"
    assert "numero de pedido" in body["reply"]


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
    assert "1 cotizar una torta" in body["reply"]
    assert "4 conocer horarios" in body["reply"]


def test_webhook_answers_hours_question() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "4",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "faq"
    assert body["stage"] == "faq_response"
    assert "horario" in body["reply"]


def test_webhook_sends_pickup_address_message() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "Quiero recoger la torta",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "delivery"
    assert "direccion de Rosa Pistacho" in body["reply"]
