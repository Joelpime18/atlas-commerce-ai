import re
from enum import StrEnum

from pydantic import BaseModel


class ProductCategory(StrEnum):
    COFFEE_CAKE = "coffee_cake"
    COOKIE = "cookie"
    SWEET_TABLE = "sweet_table"
    SHOT_DESSERT = "shot_dessert"
    CUSTOM_CAKE = "custom_cake"


class Product(BaseModel):
    code: str
    name: str
    price_cop: int | None
    category: ProductCategory
    unit: str = "unidad"
    minimum_quantity: int = 1
    requires_quote: bool = False
    available_for_new_customers: bool = False
    available_for_frequent_customers: bool = True
    aliases: list[str] = []


ROSA_PISTACHO_CATALOG = [
    Product(
        code="TCP001",
        name="Torta de Chocolate",
        price_cop=54000,
        category=ProductCategory.COFFEE_CAKE,
        aliases=["torta de chocolate", "chocolate"],
    ),
    Product(
        code="TCP002",
        name="Torta de Zanahoria y Nueces",
        price_cop=54000,
        category=ProductCategory.COFFEE_CAKE,
        aliases=["zanahoria", "zanahoria y nueces"],
    ),
    Product(
        code="TCP003",
        name="Torta de Limon y Arandanos",
        price_cop=60000,
        category=ProductCategory.COFFEE_CAKE,
        aliases=["limon arandanos", "limon y arandanos"],
    ),
    Product(
        code="TCP004",
        name="Torta de Amapola con Frutos Rojos",
        price_cop=60000,
        category=ProductCategory.COFFEE_CAKE,
        aliases=["amapola", "frutos rojos"],
    ),
    Product(
        code="TCP005",
        name="Torta Red Velvet",
        price_cop=60000,
        category=ProductCategory.COFFEE_CAKE,
        aliases=["red velvet", "torta red velvet"],
    ),
    Product(
        code="GAL001",
        name="Galleta NY Nutella",
        price_cop=4500,
        category=ProductCategory.COOKIE,
        minimum_quantity=6,
        aliases=["galleta ny nutella", "nutella"],
    ),
    Product(
        code="GAL002",
        name="Galleta NY Oreo",
        price_cop=4500,
        category=ProductCategory.COOKIE,
        minimum_quantity=6,
        aliases=["galleta ny oreo", "galletas ny oreo", "oreo"],
    ),
    Product(
        code="GAL003",
        name="Galleta NY Red Velvet",
        price_cop=4500,
        category=ProductCategory.COOKIE,
        minimum_quantity=6,
        aliases=["galleta ny red velvet", "galletas ny red velvet"],
    ),
    Product(
        code="GAL004",
        name="Galleta de Avena",
        price_cop=3000,
        category=ProductCategory.COOKIE,
        minimum_quantity=6,
        aliases=["galleta de avena", "galletas de avena", "avena"],
    ),
    Product(
        code="MD001",
        name="Brownie",
        price_cop=8000,
        category=ProductCategory.SWEET_TABLE,
        minimum_quantity=6,
        aliases=["brownie", "brownies"],
    ),
    Product(
        code="MD002",
        name="Paleta",
        price_cop=8000,
        category=ProductCategory.SWEET_TABLE,
        minimum_quantity=6,
        aliases=["paleta", "paletas"],
    ),
    Product(
        code="MD003",
        name="Galleta",
        price_cop=4500,
        category=ProductCategory.SWEET_TABLE,
        minimum_quantity=6,
        aliases=["galleta mesa dulce", "galletas mesa dulce"],
    ),
    Product(
        code="MD004",
        name="Cupcake en crema",
        price_cop=7500,
        category=ProductCategory.SWEET_TABLE,
        minimum_quantity=6,
        aliases=["cupcake en crema", "cupcakes en crema"],
    ),
    Product(
        code="MD005",
        name="Cupcake en fondant",
        price_cop=8500,
        category=ProductCategory.SWEET_TABLE,
        minimum_quantity=6,
        aliases=["cupcake en fondant", "cupcakes en fondant"],
    ),
    Product(
        code="SH001",
        name="Postre en Shot de Maracuya",
        price_cop=5500,
        category=ProductCategory.SHOT_DESSERT,
        minimum_quantity=6,
        aliases=["shot de maracuya", "maracuya"],
    ),
    Product(
        code="SH002",
        name="Postre en Shot de Oreo",
        price_cop=5500,
        category=ProductCategory.SHOT_DESSERT,
        minimum_quantity=6,
        aliases=["shot de oreo", "postre oreo"],
    ),
    Product(
        code="SH003",
        name="Postre en Shot de Frutos Rojos",
        price_cop=5500,
        category=ProductCategory.SHOT_DESSERT,
        minimum_quantity=6,
        aliases=["shot de frutos rojos", "postre frutos rojos"],
    ),
    Product(
        code="SH004",
        name="Postre en Shot de Limon",
        price_cop=5500,
        category=ProductCategory.SHOT_DESSERT,
        minimum_quantity=6,
        aliases=["shot de limon", "postre limon"],
    ),
    Product(
        code="SH005",
        name="Postre en Shot de Cafe",
        price_cop=5500,
        category=ProductCategory.SHOT_DESSERT,
        minimum_quantity=6,
        aliases=["shot de cafe", "postre cafe"],
    ),
    Product(
        code="SH006",
        name="Postre en Shot de Chocolate",
        price_cop=5500,
        category=ProductCategory.SHOT_DESSERT,
        minimum_quantity=6,
        aliases=["shot de chocolate", "postre chocolate"],
    ),
    Product(
        code="TP001",
        name="Torta Personalizada",
        price_cop=None,
        category=ProductCategory.CUSTOM_CAKE,
        requires_quote=True,
        available_for_new_customers=True,
        aliases=["torta personalizada", "torta de cumpleanos", "torta tematica"],
    ),
]


class QuotedLine(BaseModel):
    product: Product
    quantity: int
    subtotal_cop: int


class FixedPriceQuote(BaseModel):
    lines: list[QuotedLine]

    @property
    def total_cop(self) -> int:
        return sum(line.subtotal_cop for line in self.lines)


def format_cop(value: int) -> str:
    return f"${value:,} COP".replace(",", ".")


def format_catalog() -> str:
    lines = []
    for product in ROSA_PISTACHO_CATALOG:
        if product.price_cop is None:
            lines.append(f"- {product.name}: se cotiza")
            continue

        minimum = (
            f" minimo {product.minimum_quantity}"
            if product.minimum_quantity > 1
            else ""
        )
        lines.append(f"- {product.name}: {format_cop(product.price_cop)}{minimum}")

    return "\n".join(lines)


def find_product_in_message(message: str) -> Product | None:
    normalized_message = message.lower()

    for product in ROSA_PISTACHO_CATALOG:
        if any(alias in normalized_message for alias in product.aliases):
            return product

    return None


def quote_fixed_products_from_message(message: str) -> FixedPriceQuote | None:
    normalized_message = message.lower()
    lines: list[QuotedLine] = []
    matched_codes: set[str] = set()

    for product in ROSA_PISTACHO_CATALOG:
        if product.price_cop is None:
            continue

        quantity = _extract_quantity_for_product(normalized_message, product)
        if quantity is None or product.code in matched_codes:
            continue

        lines.append(
            QuotedLine(
                product=product,
                quantity=quantity,
                subtotal_cop=quantity * product.price_cop,
            )
        )
        matched_codes.add(product.code)

    if not lines:
        return None

    return FixedPriceQuote(lines=lines)


def _extract_quantity_for_product(message: str, product: Product) -> int | None:
    for alias in sorted(product.aliases, key=len, reverse=True):
        alias_index = message.find(alias)
        if alias_index >= 0:
            text_before_alias = message[:alias_index]
            quantities_before_alias = re.findall(r"\d+", text_before_alias)
            if quantities_before_alias:
                return int(quantities_before_alias[-1])

        after = re.search(rf"{re.escape(alias)}\s+(\d+)", message)
        if after:
            return int(after.group(1))

        if alias in message:
            return 1

    return None
