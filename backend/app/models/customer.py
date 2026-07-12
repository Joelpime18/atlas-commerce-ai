from enum import StrEnum

from pydantic import BaseModel


class CustomerType(StrEnum):
    INDIVIDUAL = "individual"
    CAFE = "cafe"
    BUSINESS = "business"


class CustomerLevel(StrEnum):
    NEW = "new"
    FREQUENT = "frequent"
    VIP = "vip"


class Customer(BaseModel):
    id: str
    phone_number: str
    name: str
    customer_type: CustomerType = CustomerType.INDIVIDUAL
    customer_level: CustomerLevel = CustomerLevel.NEW
    alias: str | None = None
    average_orders_per_week: int | None = None
    has_credit: bool = False
