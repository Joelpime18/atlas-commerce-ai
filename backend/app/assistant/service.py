from app.assistant.catalog import (
    find_product_in_message,
    format_catalog,
    format_cop,
    quote_fixed_products_from_message,
)
from app.assistant.conversation import (
    AssistantReply,
    ConversationIntent,
    ConversationStage,
)
from app.config.business_rules import (
    DELIVERY_POLICY,
    ROSA_PISTACHO_ADDRESS,
    ROSA_PISTACHO_HOURS,
)
from app.models.customer import Customer, CustomerType


class AssistantService:
    @staticmethod
    def generate_reply(customer: Customer, message: str) -> AssistantReply:
        normalized_message = message.lower().strip()

        if not normalized_message:
            return AssistantService._main_menu_reply(customer)

        if customer.customer_type == CustomerType.CAFE:
            cafe_reply = AssistantService._generate_cafe_reply(customer, normalized_message)
            if cafe_reply:
                return cafe_reply

        if AssistantService._selects_quote(normalized_message):
            return AssistantReply(
                message=(
                    "Perfecto, con gusto te ayudamos a cotizar tu torta. "
                    "Para empezar, cuentanos:\n\n"
                    "1. ¿Para cuantas personas es la torta?\n"
                    "2. ¿Que color o colores te gustaria que tuviera?\n"
                    "3. ¿Tienes una imagen de referencia? Si la tienes, por favor "
                    "enviala en este chat.\n\n"
                    "Ten presente que en Rosa Pistacho no trabajamos con imagenes "
                    "obscenas o contenido inapropiado."
                ),
                intent=ConversationIntent.QUOTE,
                stage=ConversationStage.QUOTE_DETAILS,
                suggested_actions=[
                    "Pedir numero de personas",
                    "Pedir colores",
                    "Pedir imagen de referencia",
                ],
            )

        if AssistantService._selects_order(normalized_message):
            return AssistantReply(
                message=(
                    "Listo. Para realizar tu pedido necesitamos estos datos:\n\n"
                    "1. Nombre completo\n"
                    "2. Fecha de entrega\n"
                    "3. Tipo de producto\n"
                    "4. Numero de personas\n"
                    "5. Imagen de referencia de la torta\n\n"
                    "Importante: Rosa Pistacho no realiza domicilios. Los pedidos "
                    f"se recogen en: {ROSA_PISTACHO_ADDRESS}."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=[
                    "Pedir nombre",
                    "Pedir fecha de entrega",
                    "Pedir tipo de producto",
                    "Pedir numero de personas",
                    "Pedir imagen de referencia",
                ],
            )

        if AssistantService._selects_status(normalized_message):
            return AssistantReply(
                message=(
                    "Claro. Para consultar tu pedido, por favor enviame el numero "
                    "de pedido."
                ),
                intent=ConversationIntent.FAQ,
                stage=ConversationStage.FAQ_RESPONSE,
                suggested_actions=["Pedir numero de pedido"],
            )

        if AssistantService._asks_for_hours(normalized_message):
            return AssistantReply(
                message=f"Nuestro horario de atencion es:\n\n{ROSA_PISTACHO_HOURS}",
                intent=ConversationIntent.FAQ,
                stage=ConversationStage.FAQ_RESPONSE,
                suggested_actions=["Iniciar pedido"],
            )

        if AssistantService._asks_for_catalog(normalized_message):
            return AssistantReply(
                message=(
                    "Claro. Este es el catalogo base de productos con precio fijo:\n"
                    f"{format_catalog()}\n\n"
                    "Las tortas personalizadas se cotizan segun el diseno."
                ),
                intent=ConversationIntent.CATALOG,
                stage=ConversationStage.PRODUCT_DISCOVERY,
                suggested_actions=["Elegir producto", "Indicar fecha"],
            )

        if AssistantService._mentions_delivery(normalized_message):
            return AssistantReply(
                message=(
                    f"{DELIVERY_POLICY}\n\n"
                    f"Puedes recoger tu pedido en: {ROSA_PISTACHO_ADDRESS}."
                ),
                intent=ConversationIntent.DELIVERY,
                stage=ConversationStage.DELIVERY_DETAILS,
                suggested_actions=["Confirmar fecha y hora de recogida"],
            )

        product = find_product_in_message(normalized_message)
        if AssistantService._wants_to_order(normalized_message) or product:
            if product and product.requires_quote:
                return AssistantService.generate_reply(customer=customer, message="1")

            product_name = product.name if product else "el producto que quieres"
            return AssistantReply(
                message=(
                    f"Perfecto. Puedo ayudarte a iniciar el pedido de {product_name}. "
                    "Para continuar necesito: nombre, fecha de entrega, tipo de "
                    "producto, numero de personas e imagen de referencia de la torta."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=[
                    "Pedir nombre",
                    "Pedir fecha de entrega",
                    "Pedir tipo de producto",
                    "Pedir numero de personas",
                    "Pedir imagen de referencia",
                ],
            )

        if AssistantService._is_greeting(normalized_message):
            return AssistantService._main_menu_reply(customer)

        return AssistantReply(
            message=(
                "Gracias por escribir a Rosa Pistacho. Para ayudarte mejor, "
                "responde con una opcion: 1 cotizar una torta, 2 realizar un "
                "pedido, 3 consultar un pedido o 4 conocer horarios."
            ),
            intent=ConversationIntent.UNKNOWN,
            stage=ConversationStage.MAIN_MENU,
            suggested_actions=[
                "Cotizar torta",
                "Realizar pedido",
                "Consultar pedido",
                "Conocer horarios",
            ],
        )

    @staticmethod
    def _generate_cafe_reply(
        customer: Customer,
        normalized_message: str,
    ) -> AssistantReply | None:
        if AssistantService._is_greeting(normalized_message):
            alias = customer.alias or customer.name
            return AssistantReply(
                message=(
                    f"Buenos dias, {alias}. Que gusto atenderlos nuevamente. "
                    "¿Que productos necesitan para esta semana?"
                ),
                intent=ConversationIntent.GREETING,
                stage=ConversationStage.PRODUCT_DISCOVERY,
                suggested_actions=["Recibir pedido de precio fijo"],
            )

        quote = quote_fixed_products_from_message(normalized_message)
        if not quote:
            return None

        lines = [
            f"- {line.quantity} x {line.product.name}: {format_cop(line.subtotal_cop)}"
            for line in quote.lines
        ]
        summary = "\n".join(lines)

        return AssistantReply(
            message=(
                f"Perfecto, {customer.alias or customer.name}. Este es el resumen "
                f"de tu pedido:\n\n{summary}\n\n"
                f"Total: {format_cop(quote.total_cop)}\n\n"
                "Una vez recibamos el soporte de pago, la duena validara el ingreso. "
                "Cuando el pago quede confirmado, iniciaremos la preparacion."
            ),
            intent=ConversationIntent.ORDER,
            stage=ConversationStage.ORDER_DETAILS,
            suggested_actions=["Confirmar pedido", "Solicitar soporte de pago"],
        )

    @staticmethod
    def _main_menu_reply(customer: Customer) -> AssistantReply:
        return AssistantReply(
            message=(
                "¡Hola! 🌸✨ Qué alegría tenerte aquí. Bienvenido(a) a "
                "Rosa Pistacho. Estamos felices de acompañarte y ayudarte a "
                "encontrar justo lo que buscas. ¿En qué podemos ayudarte hoy?\n\n"
                "Deseas:\n"
                "1. Cotizar una torta\n"
                "2. Realizar un pedido\n"
                "3. Consultar un pedido\n"
                "4. Conocer horarios"
            ),
            intent=ConversationIntent.GREETING,
            stage=ConversationStage.MAIN_MENU,
            suggested_actions=[
                "Cotizar torta",
                "Realizar pedido",
                "Consultar pedido",
                "Conocer horarios",
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
        keywords = {"4", "horario", "horarios", "hora", "atienden", "domingo"}
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
        keywords = {
            "domicilio",
            "domicilios",
            "entrega",
            "direccion",
            "envio",
            "recoger",
            "recojo",
            "recogida",
            "paso por",
            "pasar por",
        }
        return any(keyword in message for keyword in keywords)
