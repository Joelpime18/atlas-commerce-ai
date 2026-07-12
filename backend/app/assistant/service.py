from app.assistant.catalog import (
    find_product_in_message,
    format_cop,
    quote_fixed_products_from_message,
)
from app.assistant.conversation import (
    AssistantReply,
    ConversationIntent,
    ConversationStage,
)
from app.assistant.memory import ConversationMemory, ConversationSession
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

        session = ConversationMemory.get(customer.id)
        session_reply = AssistantService._continue_session(customer, session, message)
        if session_reply:
            return session_reply

        if AssistantService._selects_quote(normalized_message):
            ConversationMemory.start(
                customer_id=customer.id,
                flow="custom_quote",
                step="people",
            )
            return AssistantReply(
                message=(
                    "Perfecto, con gusto te ayudamos a cotizar tu torta "
                    "personalizada. Para empezar: ¿para cuantas personas es la torta?"
                ),
                intent=ConversationIntent.QUOTE,
                stage=ConversationStage.QUOTE_DETAILS,
                suggested_actions=["Pedir numero de personas"],
            )

        if AssistantService._selects_order(normalized_message):
            ConversationMemory.start(
                customer_id=customer.id,
                flow="order",
                step="name",
            )
            return AssistantReply(
                message=(
                    "Listo. Para realizar tu pedido, empecemos por el nombre. "
                    "¿A nombre de quien registramos el pedido?\n\n"
                    "Importante: Rosa Pistacho no realiza domicilios. Los pedidos "
                    f"se recogen en: {ROSA_PISTACHO_ADDRESS}."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=["Pedir nombre"],
            )

        if AssistantService._asks_for_catalog(normalized_message):
            return AssistantService._catalog_reply()

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

        if AssistantService._selects_cafe_application(normalized_message):
            return AssistantService._cafe_application_reply()

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
            ConversationMemory.clear(customer.id)
            return AssistantService._main_menu_reply(customer)

        return AssistantReply(
            message=(
                "Gracias por escribir a Rosa Pistacho. Para ayudarte mejor, "
                "responde con una opcion: 1 cotizar una torta personalizada, "
                "2 realizar un pedido, 3 ver catalogo, 4 consultar un pedido, "
                "5 conocer horarios o 6 informacion para cafes frecuentes."
            ),
            intent=ConversationIntent.UNKNOWN,
            stage=ConversationStage.MAIN_MENU,
            suggested_actions=AssistantService._main_menu_actions(),
        )

    @staticmethod
    def _continue_session(
        customer: Customer,
        session: ConversationSession,
        message: str,
    ) -> AssistantReply | None:
        normalized_message = message.lower().strip()

        if not session.flow or not session.step:
            return None

        if normalized_message in {"cancelar", "salir", "reiniciar"}:
            ConversationMemory.clear(customer.id)
            return AssistantReply(
                message=(
                    "Listo, reiniciamos la conversacion. Cuando quieras, escribe "
                    "Hola para ver el menu principal."
                ),
                intent=ConversationIntent.UNKNOWN,
                stage=ConversationStage.MAIN_MENU,
                suggested_actions=["Volver al menu"],
            )

        if session.flow == "custom_quote":
            return AssistantService._continue_custom_quote(customer, session, message)

        if session.flow == "order":
            return AssistantService._continue_order(customer, session, message)

        return None

    @staticmethod
    def _continue_custom_quote(
        customer: Customer,
        session: ConversationSession,
        message: str,
    ) -> AssistantReply:
        if session.step == "people":
            session.data["people"] = message.strip()
            session.step = "colors"
            return AssistantReply(
                message="Gracias. ¿Que color o colores te gustaria que tuviera?",
                intent=ConversationIntent.QUOTE,
                stage=ConversationStage.QUOTE_DETAILS,
                suggested_actions=["Pedir colores"],
            )

        if session.step == "colors":
            session.data["colors"] = message.strip()
            session.step = "reference_image"
            return AssistantReply(
                message=(
                    "Perfecto. ¿Tienes una imagen de referencia? Si la tienes, "
                    "por favor enviala en este chat.\n\n"
                    "Ten presente que en Rosa Pistacho no trabajamos con imagenes "
                    "obscenas o contenido inapropiado."
                ),
                intent=ConversationIntent.QUOTE,
                stage=ConversationStage.QUOTE_DETAILS,
                suggested_actions=["Pedir imagen de referencia"],
            )

        if session.step == "reference_image":
            session.data["reference_image"] = message.strip()
            summary = AssistantService._format_custom_quote_summary(session)
            ConversationMemory.clear(customer.id)
            return AssistantReply(
                message=(
                    "Gracias. Ya tenemos la informacion inicial para cotizar tu "
                    f"torta personalizada:\n\n{summary}\n\n"
                    "Una asesora de Rosa Pistacho revisara los detalles y te "
                    "compartira la cotizacion."
                ),
                intent=ConversationIntent.QUOTE,
                stage=ConversationStage.HUMAN_REVIEW,
                suggested_actions=["Enviar a revision humana"],
            )

        ConversationMemory.clear(customer.id)
        return AssistantService._main_menu_reply(customer)

    @staticmethod
    def _continue_order(
        customer: Customer,
        session: ConversationSession,
        message: str,
    ) -> AssistantReply:
        if session.step == "name":
            session.data["name"] = message.strip()
            session.step = "delivery_date"
            return AssistantReply(
                message="Gracias. ¿Para que fecha necesitas el pedido?",
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=["Pedir fecha de entrega"],
            )

        if session.step == "delivery_date":
            session.data["delivery_date"] = message.strip()
            session.step = "product_type"
            return AssistantReply(
                message="Perfecto. ¿Que tipo de producto necesitas?",
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=["Pedir tipo de producto"],
            )

        if session.step == "product_type":
            session.data["product_type"] = message.strip()
            session.step = "people"
            return AssistantReply(
                message="Entendido. ¿Para cuantas personas es?",
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=["Pedir numero de personas"],
            )

        if session.step == "people":
            session.data["people"] = message.strip()
            session.step = "reference_image"
            return AssistantReply(
                message=(
                    "Gracias. Por favor envia la imagen de referencia de la torta "
                    "o cuentanos si no tienes una."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.ORDER_DETAILS,
                suggested_actions=["Pedir imagen de referencia"],
            )

        if session.step == "reference_image":
            session.data["reference_image"] = message.strip()
            summary = AssistantService._format_order_summary(session)
            ConversationMemory.clear(customer.id)
            return AssistantReply(
                message=(
                    "Gracias. Ya tenemos la informacion inicial de tu pedido:\n\n"
                    f"{summary}\n\n"
                    f"Recuerda que los pedidos se recogen en: {ROSA_PISTACHO_ADDRESS}. "
                    "Una asesora revisara la informacion y continuara el proceso."
                ),
                intent=ConversationIntent.ORDER,
                stage=ConversationStage.HUMAN_REVIEW,
                suggested_actions=["Enviar a revision humana"],
            )

        ConversationMemory.clear(customer.id)
        return AssistantService._main_menu_reply(customer)

    @staticmethod
    def _format_custom_quote_summary(session: ConversationSession) -> str:
        return "\n".join(
            [
                f"- Personas: {session.data.get('people', 'pendiente')}",
                f"- Colores: {session.data.get('colors', 'pendiente')}",
                f"- Imagen de referencia: {session.data.get('reference_image', 'pendiente')}",
            ]
        )

    @staticmethod
    def _format_order_summary(session: ConversationSession) -> str:
        return "\n".join(
            [
                f"- Nombre: {session.data.get('name', 'pendiente')}",
                f"- Fecha de entrega: {session.data.get('delivery_date', 'pendiente')}",
                f"- Tipo de producto: {session.data.get('product_type', 'pendiente')}",
                f"- Personas: {session.data.get('people', 'pendiente')}",
                f"- Imagen de referencia: {session.data.get('reference_image', 'pendiente')}",
            ]
        )

    @staticmethod
    def _generate_cafe_reply(
        customer: Customer,
        normalized_message: str,
    ) -> AssistantReply | None:
        if (
            AssistantService._selects_quote(normalized_message)
            or AssistantService._selects_order(normalized_message)
            or AssistantService._is_greeting(normalized_message)
        ):
            return AssistantService._frequent_customer_order_prompt(customer)

        quote = quote_fixed_products_from_message(normalized_message)
        if not quote:
            return None

        lines = [
            f"- {line.quantity} x {line.product.name}: {format_cop(line.subtotal_cop)}"
            for line in quote.lines
        ]
        summary = "\n".join(lines)
        payment_message = (
            "Este cliente cuenta con credito en Rosa Pistacho. "
            "Registraremos el pedido para preparacion segun las condiciones "
            "acordadas con el negocio."
            if customer.has_credit
            else (
                "Una vez recibamos el soporte de pago, Rosa Pistacho validara "
                "el ingreso. Cuando el pago quede confirmado, iniciaremos la "
                "preparacion."
            )
        )
        suggested_actions = (
            ["Confirmar pedido con credito", "Registrar pedido"]
            if customer.has_credit
            else ["Confirmar pedido", "Solicitar soporte de pago"]
        )

        return AssistantReply(
            message=(
                f"Perfecto, {customer.alias or customer.name}. Este es el resumen "
                f"de tu pedido:\n\n{summary}\n\n"
                f"Total: {format_cop(quote.total_cop)}\n\n"
                f"{payment_message}"
            ),
            intent=ConversationIntent.ORDER,
            stage=ConversationStage.ORDER_DETAILS,
            suggested_actions=suggested_actions,
        )

    @staticmethod
    def _frequent_customer_order_prompt(customer: Customer) -> AssistantReply:
        alias = customer.alias or customer.name
        return AssistantReply(
            message=(
                f"Buenos dias, {alias}. Que gusto atenderlos nuevamente. "
                "Por favor envianos el pedido con los productos y cantidades "
                "que necesitan. Por ejemplo: 2 tortas de chocolate, 18 brownies "
                "y 12 galletas NY Oreo."
            ),
            intent=ConversationIntent.GREETING,
            stage=ConversationStage.PRODUCT_DISCOVERY,
            suggested_actions=["Recibir pedido de precio fijo"],
        )

    @staticmethod
    def _main_menu_reply(customer: Customer) -> AssistantReply:
        return AssistantReply(
            message=(
                "¡Hola! 🌸✨ Qué alegría tenerte aquí. Bienvenido(a) a "
                "Rosa Pistacho. Estamos felices de acompañarte y ayudarte a "
                "encontrar justo lo que buscas. ¿En qué podemos ayudarte hoy?\n\n"
                "Deseas:\n"
                "1. Cotizar una torta personalizada\n"
                "2. Realizar un pedido\n"
                "3. Catalogo\n"
                "4. Consultar un pedido\n"
                "5. Conocer horarios\n"
                "6. Quiero que mi cafe sea cliente frecuente"
            ),
            intent=ConversationIntent.GREETING,
            stage=ConversationStage.MAIN_MENU,
            suggested_actions=AssistantService._main_menu_actions(),
        )

    @staticmethod
    def _catalog_reply() -> AssistantReply:
        return AssistantReply(
            message=(
                "Claro. Puedes consultar el catalogo de Rosa Pistacho en este PDF:\n\n"
                "http://127.0.0.1:8000/static/catalogo-rosa-pistacho.pdf\n\n"
                "Las tortas personalizadas se cotizan segun el diseno."
            ),
            intent=ConversationIntent.CATALOG,
            stage=ConversationStage.PRODUCT_DISCOVERY,
            suggested_actions=["Enviar catalogo PDF", "Indicar fecha"],
        )

    @staticmethod
    def _cafe_application_reply() -> AssistantReply:
        return AssistantReply(
            message=(
                "¡Nos encanta que quieras que tu cafe trabaje con Rosa Pistacho! "
                "Por favor dejanos el nombre del cafe, nombre de contacto y numero "
                "de telefono. Rosa Pistacho revisara la informacion y se pondra "
                "en contacto contigo."
            ),
            intent=ConversationIntent.CAFE_APPLICATION,
            stage=ConversationStage.HUMAN_REVIEW,
            suggested_actions=["Solicitar datos del cafe", "Enviar a Rosa Pistacho"],
        )

    @staticmethod
    def _main_menu_actions() -> list[str]:
        return [
            "Cotizar torta personalizada",
            "Realizar pedido",
            "Ver catalogo",
            "Consultar pedido",
            "Conocer horarios",
            "Cafe cliente frecuente",
        ]

    @staticmethod
    def _is_greeting(message: str) -> bool:
        keywords = {"hola", "buenas", "buenos dias", "buenas tardes", "buenas noches"}
        return any(keyword in message for keyword in keywords)

    @staticmethod
    def _selects_quote(message: str) -> bool:
        return message == "1" or "cotizar" in message or "cotizacion" in message

    @staticmethod
    def _selects_order(message: str) -> bool:
        keywords = {"realizar pedido", "hacer pedido"}
        return message == "2" or any(keyword in message for keyword in keywords)

    @staticmethod
    def _asks_for_catalog(message: str) -> bool:
        keywords = {"catalogo", "catalogo", "menu", "productos", "precio", "precios", "venden"}
        return message == "3" or any(keyword in message for keyword in keywords)

    @staticmethod
    def _selects_status(message: str) -> bool:
        keywords = {"consultar pedido", "estado pedido", "estado del pedido"}
        return message == "4" or any(keyword in message for keyword in keywords)

    @staticmethod
    def _asks_for_hours(message: str) -> bool:
        keywords = {"horario", "horarios", "hora", "atienden", "domingo"}
        return message == "5" or any(keyword in message for keyword in keywords)

    @staticmethod
    def _selects_cafe_application(message: str) -> bool:
        keywords = {
            "cliente frecuente",
            "cafe frecuente",
            "mi cafe",
            "cafeteria",
            "café",
            "cafe",
        }
        return message == "6" or any(keyword in message for keyword in keywords)

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
