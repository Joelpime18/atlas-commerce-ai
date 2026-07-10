from enum import StrEnum

from pydantic import BaseModel


class ConversationIntent(StrEnum):
    GREETING = "greeting"
    CATALOG = "catalog"
    QUOTE = "quote"
    ORDER = "order"
    DELIVERY = "delivery"
    FAQ = "faq"
    HUMAN_SUPPORT = "human_support"
    UNKNOWN = "unknown"


class ConversationStage(StrEnum):
    WELCOME = "welcome"
    MAIN_MENU = "main_menu"
    PRODUCT_DISCOVERY = "product_discovery"
    QUOTE_DETAILS = "quote_details"
    ORDER_DETAILS = "order_details"
    DELIVERY_DETAILS = "delivery_details"
    FAQ_RESPONSE = "faq_response"
    HUMAN_REVIEW = "human_review"


class AssistantReply(BaseModel):
    message: str
    intent: ConversationIntent
    stage: ConversationStage
    suggested_actions: list[str]
