# ADR 003 - Temporary Conversation Memory

## Status

Accepted for local testing

## Context

Atlas needs to support complete test conversations before PostgreSQL persistence
is implemented.

For the first browser demo, it is enough for Atlas to remember the current
conversation while the server is running.

## Decision

Atlas will use an in-memory conversation store for now.

This memory stores:

- Customer id.
- Current flow.
- Current step.
- Data collected so far.

Supported flows:

- Custom cake quote.
- Basic order capture.

## Limitations

This memory is temporary.

If the server is restarted, the conversation state is lost.

This is acceptable for the current testing phase, but it must later be replaced
with persistent storage in PostgreSQL.

## Consequences

We can now test a conversation from beginning to end in the browser demo.

Atlas can ask one question at a time and remember the previous answer during
the same local session.
