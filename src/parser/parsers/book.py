from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag
from parser.models.items import Item
from parser.utils.logger import get_logger
from parser.config import Settings

logger = get_logger(__name__)
RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def parse_book(node: Tag, base_url:str = Settings.base_url) -> Item | None:
    try:
        link = node.select_one("h3 > a")
        if link is None or not link.get("href"):
            logger.warning("Пропускаю карточку - нет ссылки на книгу")

        title = (link.get("title") or link.get_text(strip=True)).strip()
        url = urljoin(base_url, link["href"])

        price_node = node.select_one("p.price_color")
        price = _parse_price(price_node.get_text(strip=True)) if price_node else None

        # --- рейтинг ---
        rating = _parse_rating(node.select_one("p.star-rating"))

        # --- наличие ---
        stock_node = node.select_one("p.instock.availability")
        in_stock = bool(stock_node and "In stock" in stock_node.get_text())

        # --- картинка ---
        image_url = None
        img_node = node.select_one("img.thumbnail")
        if img_node and img_node.get("src"):
            image_url = urljoin(base_url, img_node["src"])

        return Item(
            title=title,
            url=url,
            price=price,
            currency="GBP",
            rating=rating,
            in_stock=in_stock,
            image_url=image_url,
            source="books.toscrape.com",
        )

    except (AttributeError, KeyError, InvalidOperation) as e:
        logger.warning("Не удалось разобрать карточку: %s", e)
        return None

def _parse_price(text: str) -> Decimal | None:
    """'£51.77' → Decimal('51.77'). None, если распарсить не удалось."""
    cleaned = (
        text.strip()
        .replace("£", "")
        .replace("$", "")
        .replace("€", "")
        .strip()
    )
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)   # Decimal принимает строку, не float
    except InvalidOperation:
        logger.warning("Не смог распарсить цену: %r", text)
        return None

def _parse_rating(node: Tag | None) -> int | None:
    """<p class='star-rating Three'> → 3."""
    if node is None:
        return None
    # классы: ['star-rating', 'Three'] — ищем известное слово
    for cls in node.get("class", []):
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return None