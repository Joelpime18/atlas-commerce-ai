from fastapi import APIRouter, status

from app.assistant.service import AssistantService
from app.customers.service import CustomerService
from app.models.webhook import WebhookMessageRequest, WebhookMessageResponse

router = APIRouter(tags=["webhook"])


@router.post(
    "/webhook",
    response_model=WebhookMessageResponse,
    status_code=status.HTTP_200_OK,
)
def receive_whatsapp_message(
    payload: WebhookMessageRequest,
) -> WebhookMessageResponse:
    customer = CustomerService.identify_customer(phone_number=payload.from_phone)
    reply = AssistantService.generate_reply(
        customer_name=customer.name,
        message=payload.message,
    )

    return WebhookMessageResponse(
        customer_id=customer.id,
        reply=reply,
    )
