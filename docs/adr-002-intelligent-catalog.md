# ADR 002 - Intelligent Product Catalog

## Status

Accepted

## Context

Rosa Pistacho has two different product behaviors:

- Fixed-price products for frequent business customers such as cafes.
- Custom cakes for new individual customers, where the final price varies by
  design and must be reviewed by the owner.

Atlas must not invent prices for custom cakes.

## Decision

The product catalog stores business rules, not only names and prices.

Each product may define:

- Code.
- Name.
- Category.
- Price.
- Unit.
- Minimum quantity.
- Whether it requires a quote.
- Whether it is available for new customers.
- Whether it is available for frequent customers.
- Search aliases.

## Consequences

Atlas can automatically quote fixed-price products for frequent cafe customers,
while guiding new customers through a custom quote flow.

The owner remains responsible for final custom cake pricing.
