from app.models.customer import Customer, CustomerLevel, CustomerType


LATIDO_COFFEE_PHONE = "573009990001"


class CustomerService:
    @staticmethod
    def identify_customer(phone_number: str) -> Customer:
        if phone_number == LATIDO_COFFEE_PHONE:
            return Customer(
                id="CL0001",
                phone_number=phone_number,
                name="Latido Coffee",
                customer_type=CustomerType.CAFE,
                customer_level=CustomerLevel.FREQUENT,
                alias="Latidos",
                average_orders_per_week=3,
                has_credit=True,
            )

        return Customer(
            id=f"wa:{phone_number}",
            phone_number=phone_number,
            name="Cliente",
        )
