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

The first version focuses on the backend foundation and a reliable order capture
flow. Atlas v0.1.0 is not a visual AI assistant and not a pricing engine.

Included:

- FastAPI backend.
- WhatsApp-style `POST /webhook` endpoint.
- Customer identification by phone number.
- Deterministic first-phase assistant logic.
- Basic Rosa Pistacho catalog.
- Intent and conversation stage classification.
- Main menu for the first WhatsApp interaction.
- Real fixed-price catalog for Rosa Pistacho.
- Recognition of Latido Coffee as a frequent cafe customer.
- Business rules for payments, pickup and operating hours.
- Temporary conversation memory for local browser testing.
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
- Image analysis.
- Automatic design recognition.
- Automatic final pricing.

## Architectural decision 001

Keep the MVP extremely simple. Atlas v0.1.0 is a reliable order capture system
for Rosa Pistacho.

The owner still decides:

- Final price.
- Design approval.
- Availability.
- Payment validation.
- Order confirmation.

Atlas should respond immediately, organize the information and guide the client
to the next useful question.

## First conversation phase

Atlas can currently handle:

- Greeting with menu options.
- Catalog and price questions.
- Quote requests with number of people, colors and reference image guidance.
- Initial order intent with name, delivery date, product type, number of people,
  delivery method and cake reference image.
- Delivery or pickup questions. Pickup replies include the Rosa Pistacho address
  placeholder until the official address is confirmed.
- Frequent cafe customer flow with automatic fixed-price quote.
- New cafe lead flow so Rosa Pistacho can contact potential frequent customers.
- Basic FAQ routing.
- Unknown messages that need guidance or human review.

The goal is not to close a full sale yet. The goal is to ask for the next useful
piece of information so Rosa Pistacho can continue the conversation clearly.

## Next likely commits

1. Persist customers and conversations in PostgreSQL.
2. Persist order drafts.
3. Add WhatsApp webhook verification for Meta Cloud API.
4. Add outbound WhatsApp message service.
5. Replace deterministic replies with an OpenAI-assisted conversation service.
