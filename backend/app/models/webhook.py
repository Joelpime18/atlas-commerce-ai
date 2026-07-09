from pydantic import BaseModel, Field

from app.assistant.conversation import ConversationIntent, ConversationStage


class WebhookMessageRequest(BaseModel):
    from_phone: str = Field(..., min_length=5)
    message: str


class WebhookMessageResponse(BaseModel):
    customer_id: str
    reply: str
    intent: ConversationIntent
    stage: ConversationStage
    suggested_actions: list[str]
