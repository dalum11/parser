"""Разбор страницы одной книги (детальная)."""

from decimal import Decimal, InvalidOperation
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

from parser.models.items import Item
from parser.utils.logger import get_logger

logger = get_logger(__name__)

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def parse_book_detail(html: str, url: str) -> Item | None:
    """Разбирает детальную страницу книги. Возвращает Item или None."""
    soup = BeautifulSoup(html, "html.parser")

    product = soup.select_one("div.product_main")
    if product is None:
        logger.warning("Нет div.product_main на %s", url)
        return None

    try:
        title = product.select_one("h1").get_text(strip=True)
    except AttributeError:
        logger.warning("Нет заголовка на %s", url)
        return None

    price = _parse_price(_text(product, "p.price_color"))

    rating = _parse_rating(product.select_one("p.star-rating"))

    in_stock_text = _text(product, "p.instock.availability")
    in_stock = "In stock" in in_stock_text

    desc_header = soup.select_one("#product_description")
    description = None
    if desc_header is not None:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p is not None:
            description = desc_p.get_text(strip=True)

    category = _parse_category(soup)

    sku = _parse_table_value(soup, "UPC")

    img = soup.select_one("#product_gallery img")
    image_url = urljoin(url, img["src"]) if img and img.get("src") else None

    return Item(
        title=title,
        url=url,
        price=price,
        currency="GBP",
        rating=rating,
        in_stock=in_stock,
        description=description,
        category=category,
        sku=sku,
        image_url=image_url,
        source="books.toscrape.com",
    )

def _text(node: Tag, selector: str) -> str:
    """Текст первого элемента по селектору или пустая строка."""
    el = node.select_one(selector)
    return el.get_text(strip=True) if el else ""

def _parse_price(text: str) -> Decimal | None:
    cleaned = text.replace("£", "").replace("$", "").replace("€", "").strip()
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None

def _parse_rating(node: Tag | None) -> int | None:
    if node is None:
        return None
    for cls in node.get("class", []):
        if cls in RATING_MAP:
            return RATING_MAP[cls]
    return None

def _parse_category(soup: BeautifulSoup) -> str | None:
    """
    Категория — предпоследний <li> в .breadcrumb.
    [Home, Books, Poetry, <название книги>] → 'Poetry'
    """
    crumbs = soup.select("ul.breadcrumb li")
    if len(crumbs) < 3:
        return None
    return crumbs[-2].get_text(strip=True)

def _parse_table_value(soup: BeautifulSoup, key: str) -> str | None:
    """Значение из таблицы product_page по имени строки (например, 'UPC')."""
    table = soup.select_one("table.table-striped")
    if table is None:
        return None
    for row in table.select("tr"):
        th = row.select_one("th")
        td = row.select_one("td")
        if th and td and th.get_text(strip=True) == key:
            return td.get_text(strip=True)
    return None