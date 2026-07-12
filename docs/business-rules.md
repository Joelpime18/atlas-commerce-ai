# Business Rules

## RB-001 - Payment Confirmation

No order can start production until the owner confirms the payment, unless the
owner explicitly authorizes an exception.

Payment status is separate from order status.

Payment statuses:

- Pending.
- Proof received.
- Validating.
- Paid.
- Rejected.

Order statuses:

- New.
- Payment pending.
- Payment confirmed.
- In production.
- Ready for pickup.
- Delivered.

## RB-002 - Customer Type Flow

Atlas changes the conversation depending on the customer type.

New individual customers usually request custom cakes. Atlas must collect
information and never invent a fixed price.

Frequent cafe customers can order fixed-price products from the catalog. Atlas
can calculate totals for those products.

Latido Coffee has credit with Rosa Pistacho. For this customer, Atlas must not
ask for payment proof before preparation in the fixed-price order response.

## RB-003 - Delivery Policy

Rosa Pistacho does not offer delivery service.

Orders are picked up at:

Cra 39 # 15 - 56, Barrio Villa Aurora II, Acacias, Meta.

Exceptions can be authorized only by the owner.

## RB-004 - Operating Schedule

Rosa Pistacho does not work on Sundays.

Current schedule:

- Monday to Friday: 9:00 a.m. to 12:00 p.m. and 2:00 p.m. to 6:00 p.m.
- Saturday: 9:00 a.m. to 5:00 p.m.
- Sunday: closed.

## RB-005 - Order Timeline

Atlas should record each important event in the order timeline.

Examples:

- Conversation started.
- Order created.
- Payment proof received.
- Payment confirmed.
- Production started.
- Ready for pickup.
- Delivered.

This will support traceability and future business analytics.
