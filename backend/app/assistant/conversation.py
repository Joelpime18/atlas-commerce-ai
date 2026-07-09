from enum import StrEnum

from pydantic import BaseModel


class ConversationIntent(StrEnum):
    GREETING = "greeting"
    CATALOG = "catalog"
    ORDER = "order"
    DELIVERY = "delivery"
    UNKNOWN = "unknown"


class ConversationStage(StrEnum):
    WELCOME = "welcome"
    PRODUCT_DISCOVERY = "product_discovery"
    ORDER_DETAILS = "order_details"
    DELIVERY_DETAILS = "delivery_details"
    HUMAN_REVIEW = "human_review"


class AssistantReply(BaseModel):
    message: str
    intent: ConversationIntent
    stage: ConversationStage
    suggested_actions: list[str]
