from fastapi.testclient import TestClient
import pytest

from app.assistant.memory import ConversationMemory
from app.main import app


client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_conversation_memory() -> None:
    ConversationMemory.clear_all()


def test_health_check_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_demo_page_loads() -> None:
    response = client.get("/demo")

    assert response.status_code == 200
    assert "Prueba de conversación para Rosa Pistacho" in response.text
    assert "Enviar a Atlas" in response.text


def test_catalog_pdf_is_available() -> None:
    response = client.get("/static/catalogo-rosa-pistacho.pdf")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")


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
    assert "1. Cotizar una torta personalizada" in body["reply"]
    assert "3. Catalogo" in body["reply"]
    assert "6. Quiero que mi cafe sea cliente frecuente" in body["reply"]


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
    assert "A nombre de quien" in body["reply"]
    assert "no realiza domicilios" in body["reply"]


def test_webhook_asks_for_order_number() -> None:
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
    assert "numero de pedido" in body["reply"]


def test_webhook_returns_catalog_for_price_question() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "3",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "catalog"
    assert "catalogo-rosa-pistacho.pdf" in body["reply"]
    assert "Las tortas personalizadas se cotizan" in body["reply"]


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
    assert "1 cotizar una torta personalizada" in body["reply"]
    assert "6 informacion para cafes frecuentes" in body["reply"]


def test_webhook_answers_hours_question() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "5",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "faq"
    assert body["stage"] == "faq_response"
    assert "horario" in body["reply"]
    assert "Domingos: cerrado" in body["reply"]


def test_webhook_explains_no_delivery_policy() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001112233",
            "message": "Hacen domicilios?",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "delivery"
    assert "no realiza domicilios" in body["reply"]
    assert "Cra 39 # 15 - 56" in body["reply"]


def test_frequent_cafe_customer_gets_fixed_price_quote() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573009990001",
            "message": "Necesitamos 2 tortas de chocolate, 18 brownies y 12 galletas NY Oreo",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["customer_id"] == "CL0001"
    assert body["intent"] == "order"
    assert "Torta de Chocolate" in body["reply"]
    assert "Brownie" in body["reply"]
    assert "Galleta NY Oreo" in body["reply"]
    assert "$306.000 COP" in body["reply"]
    assert "credito" not in body["reply"]
    assert "condiciones acordadas con Rosa Pistacho" in body["reply"]
    assert "soporte de pago" not in body["reply"]
    assert "duena" not in body["reply"]


def test_frequent_cafe_customer_gets_custom_greeting() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573009990001",
            "message": "Hola",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["customer_id"] == "CL0001"
    assert "Latidos" in body["reply"]


def test_frequent_cafe_customer_does_not_get_custom_cake_quote_flow() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573009990001",
            "message": "1",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["customer_id"] == "CL0001"
    assert "envianos el pedido" in body["reply"]
    assert "productos y cantidades" in body["reply"]
    assert "color o colores" not in body["reply"]
    assert "imagenes obscenas" not in body["reply"]


def test_frequent_cafe_customer_gets_warm_thanks_reply() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573009990001",
            "message": "Gracias",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["customer_id"] == "CL0001"
    assert "Gracias a ustedes" in body["reply"]
    assert "sigan eligiendo a Rosa Pistacho" in body["reply"]


def test_new_cafe_application_option_routes_to_human_review() -> None:
    response = client.post(
        "/webhook",
        json={
            "from_phone": "573001116666",
            "message": "6",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "cafe_application"
    assert body["stage"] == "human_review"
    assert "nombre del cafe" in body["reply"]
    assert "se pondra en contacto" in body["reply"]


def test_custom_quote_conversation_memory_flow() -> None:
    phone = "573001114444"

    first = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "1"},
    )
    assert first.status_code == 200
    assert "cuantas personas" in first.json()["reply"]

    second = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "20 personas"},
    )
    assert second.status_code == 200
    assert "imagen de referencia" in second.json()["reply"]
    assert "color o colores" not in second.json()["reply"]

    third = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "Si, ya la envie"},
    )
    assert third.status_code == 200
    body = third.json()
    assert body["stage"] == "human_review"
    assert "20 personas" in body["reply"]
    assert "Si, ya la envie" in body["reply"]
    assert "pastelera" in body["reply"]
    assert "asesora" not in body["reply"]


def test_order_conversation_memory_flow() -> None:
    phone = "573001115555"

    first = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "2"},
    )
    assert first.status_code == 200
    assert "A nombre de quien" in first.json()["reply"]

    second = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "Maria Lopez"},
    )
    assert second.status_code == 200
    assert "fecha necesitas" in second.json()["reply"]

    third = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "15 de julio"},
    )
    assert third.status_code == 200
    assert "tipo de producto" in third.json()["reply"]

    fourth = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "Torta personalizada"},
    )
    assert fourth.status_code == 200
    assert "cuantas personas" in fourth.json()["reply"]

    fifth = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "30 personas"},
    )
    assert fifth.status_code == 200
    assert "imagen de referencia" in fifth.json()["reply"]

    sixth = client.post(
        "/webhook",
        json={"from_phone": phone, "message": "No tengo imagen"},
    )
    assert sixth.status_code == 200
    body = sixth.json()
    assert body["stage"] == "human_review"
    assert "Maria Lopez" in body["reply"]
    assert "15 de julio" in body["reply"]
    assert "Torta personalizada" in body["reply"]
