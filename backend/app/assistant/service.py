class AssistantService:
    @staticmethod
    def generate_reply(customer_name: str, message: str) -> str:
        if not message.strip():
            return f"Hola {customer_name}, cuentame que necesitas y te ayudo."

        return (
            f"Hola {customer_name}, soy Atlas. Recibi tu mensaje: "
            f"'{message}'. Pronto conectaremos esta respuesta con IA."
        )
