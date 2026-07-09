from app.assistant.catalog import find_product_in_message, format_catalog
from app.assistant.conversation import (
    AssistantReply,
    ConversationIntent,
    ConversationStage,
)


class AssistantService:
    @staticmethod
    def generate_reply(customer_name: str, message: str) -> AssistantReply:
        normalized_message = message.lower().strip()

        if not normalized_message:
            return AssistantReply(
                message=(
                    f"Hola {customer_name}, soy Atlas, el asistente digital de "
                    "Rosa Pistacho. Cuentame que producto te interesa y te ayudo "
                    "con disponibilidad, precio y datos del pedido."
                ),
                intent=ConversationIntent.GREETING,
                stage=ConversationStage.WELCOME,
                suggested_actions=["Ver catalogo", "Hacer pedido"],
            )

        if AssistantService._asks_for_catalog(normalized_message):
            return AssistantReply(
                message=(
                    "Claro. Estos son los productos disponibles para esta primera "
                    f"version:\n{format_catalog()}\n"
                    "Dime cual te gusta y para que fecha lo necesitas."
                ),
                intent=ConversationIntent.CATALOG,
                stage=ConversationStage.PRODUCT_DISCOVERY,
                suggested_actions=["Elegir producto", "Indicar fecha"],
            )

        product = find_product_in_message(normalized_message)
        if AssistantService._wants_to_order(normalized_message) or product:
            product_name = product.name if product else "el producto que quieres"
            return AssistantReply(
                message=(
                    f"Perfecto. Puedo ayudarte a iniciar el pedido de {product_name}. "
                    "Para continuar necesito tres datos: fecha de entrega, cantidad "
                    "y si prefieres recogerlo o recibirlo a domicilio."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=[
                    "Pedir fecha de entrega",
                    "Pedir cantidad",
                    "Pedir metodo de entrega",
                ],
            )

        if AssistantService._is_greeting(normalized_message):
            return AssistantReply(
                message=(
                    f"Hola {customer_name}, bienvenido a Rosa Pistacho. "
                    "Puedo ayudarte a elegir un postre, revisar precios o iniciar "
                    "un pedido. Nuestro catalogo inicial es:\n"
                    f"{format_catalog()}"
                ),
                intent=ConversationIntent.GREETING,
                stage=ConversationStage.PRODUCT_DISCOVERY,
                suggested_actions=["Elegir producto", "Preguntar precios"],
            )

        if AssistantService._mentions_delivery(normalized_message):
            return AssistantReply(
                message=(
                    "Tenemos opcion de recogida y domicilio. Para confirmar el "
                    "domicilio necesito barrio, direccion y hora estimada de entrega."
                ),
                intent=ConversationIntent.DELIVERY,
                stage=ConversationStage.DELIVERY_DETAILS,
                suggested_actions=["Pedir direccion", "Pedir hora"],
            )

        return AssistantReply(
            message=(
                "Gracias por escribir a Rosa Pistacho. Para ayudarte mejor, dime "
                "si quieres ver el catalogo, conocer precios o iniciar un pedido."
            ),
            intent=ConversationIntent.UNKNOWN,
            stage=ConversationStage.HUMAN_REVIEW,
            suggested_actions=["Ver catalogo", "Iniciar pedido", "Escalar a humano"],
        )

    @staticmethod
    def _is_greeting(message: str) -> bool:
        keywords = {"hola", "buenas", "buenos dias", "buenas tardes", "buenas noches"}
        return any(keyword in message for keyword in keywords)

    @staticmethod
    def _asks_for_catalog(message: str) -> bool:
        keywords = {"catalogo", "menu", "productos", "precio", "precios", "venden"}
        return any(keyword in message for keyword in keywords)

    @staticmethod
    def _wants_to_order(message: str) -> bool:
        keywords = {"comprar", "pedido", "encargar", "ordenar", "quiero"}
        return any(keyword in message for keyword in keywords)

    @staticmethod
    def _mentions_delivery(message: str) -> bool:
        keywords = {"domicilio", "entrega", "recoger", "direccion", "envio"}
        return any(keyword in message for keyword in keywords)
