from pydantic import BaseModel, Field


class WebhookMessageRequest(BaseModel):
    from_phone: str = Field(..., min_length=5)
    message: str


class WebhookMessageResponse(BaseModel):
    customer_id: str
    reply: str
