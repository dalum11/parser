"""Разбор страницы со списком книг"""

from bs4 import BeautifulSoup
from parser.models.items import Item
from parser.parsers.book import parse_book
from parser.utils.logger import get_logger

logger = get_logger(__name__)

def parse_books_page(html: str, base_url:str) -> list[Item]:
    soup = BeautifulSoup(html, "html.parser")

    cards = soup.select("article.product_pod")
    logger.info("Найдено %d карточек", len(cards))

    items: list[Item] = []
    for card in cards:
        item = parse_book(card, base_url)
        if item is not None:
            items.append(item)

    logger.info("Разобрано %d из %d карточек", len(items), len(cards))
    return items