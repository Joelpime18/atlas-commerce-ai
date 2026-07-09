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
- Atlas returns a basic assistant reply.
- Automated tests verify the first flow.

## Development discipline

Every version must:

- Work.
- Be testable with a real customer scenario.
- Add value.
