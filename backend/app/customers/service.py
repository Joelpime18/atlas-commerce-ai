from app.models.customer import Customer


class CustomerService:
    @staticmethod
    def identify_customer(phone_number: str) -> Customer:
        return Customer(
            id=f"wa:{phone_number}",
            phone_number=phone_number,
            name="Cliente",
        )
