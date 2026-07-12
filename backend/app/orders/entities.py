from enum import StrEnum

from pydantic import BaseModel


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PROOF_RECEIVED = "proof_received"
    VALIDATING = "validating"
    PAID = "paid"
    REJECTED = "rejected"


class OrderStatus(StrEnum):
    NEW = "new"
    PAYMENT_PENDING = "payment_pending"
    PAYMENT_CONFIRMED = "payment_confirmed"
    IN_PRODUCTION = "in_production"
    READY_FOR_PICKUP = "ready_for_pickup"
    DELIVERED = "delivered"


class TimelineEventType(StrEnum):
    CONVERSATION_STARTED = "conversation_started"
    ORDER_CREATED = "order_created"
    PAYMENT_PROOF_RECEIVED = "payment_proof_received"
    PAYMENT_CONFIRMED = "payment_confirmed"
    PRODUCTION_STARTED = "production_started"
    READY_FOR_PICKUP = "ready_for_pickup"
    ORDER_DELIVERED = "order_delivered"


class TimelineEvent(BaseModel):
    event_type: TimelineEventType
    description: str


class OrderDraft(BaseModel):
    order_id: str
    customer_id: str
    payment_status: PaymentStatus = PaymentStatus.PENDING
    order_status: OrderStatus = OrderStatus.NEW
    total_cop: int | None = None
    next_action: str = "Esperar informacion del cliente"
    timeline: list[TimelineEvent] = []
