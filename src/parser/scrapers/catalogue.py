"""Обход каталога с пагинацией"""

from parser.models.items import Item
from parser.parsers.book_list import parse_books_page
from parser.parsers.pagination import get_next_page_url
from parser.utils.http_client import fetch
from parser.utils.logger import get_logger
from parser.parsers.book_details import parse_book_detail
from parser.config import Settings
import time
import random

logger = get_logger(__name__)

START_URL = Settings.base_url + "/catalogue/page-1.html"

def scrape_catalogue(
        start_url: str = START_URL,
        max_pages: int | None = None,
        fetch_details: bool = True,
) -> list[Item]:
    all_items: list[Item] = []
    url = start_url
    page_num = 0

    while url:
        page_num +=1
        logger.info("Страница %d: %s", page_num, url)

        try:
            response = fetch(url)
            logger.info("Получено %s символов", len(response.text))
        except Exception:
            logger.exception("Парсер упал")
            return 1

        items = parse_books_page(response.content, url)
        for base_item in items:
            if not fetch_details:
                items.append(base_item)
                continue

            try:
                detail_response = fetch(base_item.url)
                detail_item = parse_book_detail(detail_response.content, base_item.url)
                all_items.append(detail_item or base_item)
            except Exception:
                logger.exception("Не удалось получить детали книги")
                all_items.append(base_item)

            time.sleep(random.uniform(0.4, 0.9))

        if max_pages is not None and page_num >= max_pages:
            break

        next_url = get_next_page_url(response.content, url)
        if next_url is None:
            break

        url = next_url
        logger.info("Собрано %d книг с %d страниц", len(all_items), page_num)
    return all_items