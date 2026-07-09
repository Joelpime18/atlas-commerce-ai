from pydantic import BaseModel


class Customer(BaseModel):
    id: str
    phone_number: str
    name: str
