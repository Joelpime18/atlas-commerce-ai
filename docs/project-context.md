# Atlas Commerce AI - Project Context

## Current date

July 9, 2026

## Product thesis

Atlas Commerce AI is not a generic chatbot. It is the SaaS foundation for small
commerce businesses that need to sell, answer and manage orders through
WhatsApp.

## Client Zero

Rosa Pistacho is the first real business scenario for Atlas. Every feature must
be useful enough to test with this client before it becomes part of the next
version.

## Development rule

No feature enters the product unless it meets three conditions:

- It works.
- It can be tested with a real customer.
- It adds value.

## v0.1.0 scope

The first version focuses on the backend foundation and the first customer
conversation phase.

Included:

- FastAPI backend.
- WhatsApp-style `POST /webhook` endpoint.
- Customer identification by phone number.
- Deterministic first-phase assistant logic.
- Basic Rosa Pistacho catalog.
- Intent and conversation stage classification.
- Automated tests.

Not included yet:

- Dashboard.
- Login.
- Users and roles.
- Reports.
- Billing.
- Real Meta Cloud API integration.
- Real OpenAI API integration.
- Persistent conversation history.

## First conversation phase

Atlas can currently handle:

- Greeting.
- Catalog and price questions.
- Initial order intent.
- Delivery or pickup questions.
- Unknown messages that need guidance or human review.

The goal is not to close a full sale yet. The goal is to ask for the next useful
piece of information so Rosa Pistacho can continue the conversation clearly.

## Next likely commits

1. Persist customers and conversations in PostgreSQL.
2. Add order draft model.
3. Add WhatsApp webhook verification for Meta Cloud API.
4. Add outbound WhatsApp message service.
5. Replace deterministic replies with an OpenAI-assisted conversation service.
