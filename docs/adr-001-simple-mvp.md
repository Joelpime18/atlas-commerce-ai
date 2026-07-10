# ADR 001 - Simple MVP

## Status

Accepted

## Context

Rosa Pistacho does not need image analysis or automatic pricing in the first
version. The urgent problem is operational: clients write through WhatsApp,
orders can be lost, and the business needs a reliable way to capture and
organize requests.

## Decision

Atlas v0.1.0 will be a reliable order capture assistant.

It will:

- Respond immediately.
- Answer basic questions.
- Ask for order information step by step.
- Register the customer and conversation flow.
- Prepare order information for human review.

It will not:

- Analyze images.
- Recognize colors or objects.
- Generate designs.
- Decide final prices.
- Confirm availability.
- Validate payment.

## Consequences

The MVP remains easier to test with Rosa Pistacho and safer for real clients.
Advanced AI features can be added later only after the capture flow works
reliably.
