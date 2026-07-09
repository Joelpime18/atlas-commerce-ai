# Atlas Commerce AI

Atlas Commerce AI is the SaaS foundation for commerce conversations over WhatsApp.

## Version

`v0.1.0`

## Sprint 1 goal

Build the backend base that can receive a WhatsApp-style webhook, identify the customer, generate a basic reply, and return it.

## Current scope

- FastAPI backend.
- `/health` endpoint.
- `POST /webhook` endpoint.
- Initial project structure for assistant, customers, orders, database, services, config, and tests.
- First-phase Rosa Pistacho conversation logic.
- PostgreSQL service definition with Docker Compose.

## Not included yet

- Dashboard.
- Login.
- Users and roles.
- Reports.
- Billing.
- Real Meta Cloud API integration.
- Real OpenAI API responses.

## Local setup

Create a virtual environment, install dependencies, and run the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Run tests:

```bash
pytest
```

Start PostgreSQL:

```bash
docker compose up -d postgres
```

## Test webhook

```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"from_phone":"573001112233","message":"Hola, quiero comprar una torta pistacho."}'
```
