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
            return AssistantService._main_menu_reply(customer_name)

        if AssistantService._selects_quote(normalized_message):
            return AssistantReply(
                message=(
                    "Perfecto. Para ayudarte con la cotizacion necesito empezar "
                    "con un dato: para cuantas personas es la torta?"
                ),
                intent=ConversationIntent.QUOTE,
                stage=ConversationStage.QUOTE_DETAILS,
                suggested_actions=["Pedir numero de personas"],
            )

        if AssistantService._selects_order(normalized_message):
            return AssistantReply(
                message=(
                    "Listo. Para iniciar tu pedido necesito: nombre, fecha de "
                    "entrega, tipo de producto, numero de personas y si deseas "
                    "recogerlo o recibirlo a domicilio."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=[
                    "Pedir nombre",
                    "Pedir fecha de entrega",
                    "Pedir tipo de producto",
                    "Pedir numero de personas",
                ],
            )

        if AssistantService._selects_status(normalized_message):
            return AssistantReply(
                message=(
                    "Claro. Para consultar un pedido necesito el nombre con el "
                    "que fue registrado o el numero de telefono usado en WhatsApp."
                ),
                intent=ConversationIntent.FAQ,
                stage=ConversationStage.FAQ_RESPONSE,
                suggested_actions=["Pedir nombre o telefono"],
            )

        if AssistantService._asks_for_hours(normalized_message):
            return AssistantReply(
                message=(
                    "Nuestro horario de atencion se confirmara con Rosa Pistacho. "
                    "Por ahora puedo ayudarte a dejar tu solicitud registrada para "
                    "que una asesora la revise."
                ),
                intent=ConversationIntent.FAQ,
                stage=ConversationStage.FAQ_RESPONSE,
                suggested_actions=["Iniciar pedido", "Hablar con asesor"],
            )

        if AssistantService._asks_for_human(normalized_message):
            return AssistantReply(
                message=(
                    "Claro. Voy a dejar tu conversacion lista para que una asesora "
                    "de Rosa Pistacho te contacte y continue la atencion."
                ),
                intent=ConversationIntent.HUMAN_SUPPORT,
                stage=ConversationStage.HUMAN_REVIEW,
                suggested_actions=["Escalar a humano"],
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
            return AssistantService._main_menu_reply(customer_name)

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
                "Gracias por escribir a Rosa Pistacho. Para ayudarte mejor, "
                "responde con una opcion: 1 cotizar una torta, 2 realizar un "
                "pedido, 3 consultar un pedido, 4 conocer horarios o 5 hablar "
                "con un asesor."
            ),
            intent=ConversationIntent.UNKNOWN,
            stage=ConversationStage.MAIN_MENU,
            suggested_actions=[
                "Cotizar torta",
                "Realizar pedido",
                "Consultar pedido",
                "Conocer horarios",
                "Hablar con asesor",
            ],
        )

    @staticmethod
    def _main_menu_reply(customer_name: str) -> AssistantReply:
        return AssistantReply(
            message=(
                f"Hola {customer_name}, bienvenido(a) a Rosa Pistacho. "
                "Con gusto te ayudamos.\n\n"
                "Deseas:\n"
                "1. Cotizar una torta\n"
                "2. Realizar un pedido\n"
                "3. Consultar un pedido\n"
                "4. Conocer horarios\n"
                "5. Hablar con un asesor"
            ),
            intent=ConversationIntent.GREETING,
            stage=ConversationStage.MAIN_MENU,
            suggested_actions=[
                "Cotizar torta",
                "Realizar pedido",
                "Consultar pedido",
                "Conocer horarios",
                "Hablar con asesor",
            ],
        )

    @staticmethod
    def _is_greeting(message: str) -> bool:
        keywords = {"hola", "buenas", "buenos dias", "buenas tardes", "buenas noches"}
        return any(keyword in message for keyword in keywords)

    @staticmethod
    def _selects_quote(message: str) -> bool:
        keywords = {"1", "cotizar", "cotizacion"}
        return message in keywords or "cotizar" in message

    @staticmethod
    def _selects_order(message: str) -> bool:
        keywords = {"2", "realizar pedido", "hacer pedido"}
        return message in keywords or any(keyword in message for keyword in keywords)

    @staticmethod
    def _selects_status(message: str) -> bool:
        keywords = {"3", "consultar pedido", "estado pedido", "estado del pedido"}
        return message in keywords or any(keyword in message for keyword in keywords)

    @staticmethod
    def _asks_for_hours(message: str) -> bool:
        keywords = {"4", "horario", "horarios", "hora", "atienden"}
        return message in keywords or any(keyword in message for keyword in keywords)

    @staticmethod
    def _asks_for_human(message: str) -> bool:
        keywords = {"5", "asesor", "asesora", "humano", "persona"}
        return message in keywords or any(keyword in message for keyword in keywords)

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
