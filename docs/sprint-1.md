# Sprint 1 - Atlas v0.1.0

## Objective

Create the initial professional structure for Atlas Commerce AI and expose the first testable backend flow.

## Functional flow

Customer -> WhatsApp -> Webhook -> Atlas -> Assistant -> Response -> Customer

## Acceptance criteria

- The backend starts with FastAPI.
- `GET /health` returns service status.
- `POST /webhook` receives a simple WhatsApp-style message.
- Atlas identifies the customer by phone number.
- Atlas classifies the first customer intent.
- Atlas returns a first-phase commercial reply for Rosa Pistacho.
- Automated tests verify the first flow.

## First conversation phase

This version handles the first commercial conversation without external AI:

- Greeting.
- Catalog and price questions.
- Initial order intent.
- Delivery or pickup questions.
- Unknown message guidance.

The assistant must ask for the next useful piece of information instead of trying
to close the whole sale at once.

## Development discipline

Every version must:

- Work.
- Be testable with a real customer scenario.
- Add value.
