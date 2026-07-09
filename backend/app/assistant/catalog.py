from pydantic import BaseModel


class Product(BaseModel):
    code: str
    name: str
    price_cop: int
    description: str


ROSA_PISTACHO_CATALOG = [
    Product(
        code="torta-pistacho",
        name="Torta de pistacho",
        price_cop=85000,
        description="Torta artesanal de pistacho para celebraciones.",
    ),
    Product(
        code="cheesecake-pistacho",
        name="Cheesecake de pistacho",
        price_cop=72000,
        description="Cheesecake cremoso con cobertura de pistacho.",
    ),
    Product(
        code="mini-postres",
        name="Caja de mini postres",
        price_cop=48000,
        description="Caja surtida para reuniones y regalos.",
    ),
]


def format_catalog() -> str:
    lines = [
        f"- {product.name}: ${product.price_cop:,} COP"
        for product in ROSA_PISTACHO_CATALOG
    ]
    return "\n".join(lines).replace(",", ".")


def find_product_in_message(message: str) -> Product | None:
    normalized_message = message.lower()

    for product in ROSA_PISTACHO_CATALOG:
        product_words = product.name.lower().split()
        if any(word in normalized_message for word in product_words):
            return product

    return None
